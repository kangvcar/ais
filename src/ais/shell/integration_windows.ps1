# AIS Windows PowerShell Integration Script
# 这个脚本为 Windows PowerShell 环境提供 AIS 错误捕获和分析功能

# 全局变量
$Global:AIS_STDERR_FILE = "$env:TEMP\ais_stderr_$PID.txt"
$Global:AIS_LAST_ANALYZED_COMMAND = ""
$Global:AIS_LAST_ANALYZED_TIME = 0
$Global:AIS_ORIGINAL_ERROR_COUNT = 0

# 检查 AIS 是否可用
function Test-AISAvailability {
    try {
        $null = Get-Command ais -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# 检查自动分析是否开启
function Test-AISAutoAnalysis {
    if (-not (Test-AISAvailability)) { 
        return $false 
    }
    
    $configPath = "$env:USERPROFILE\.config\ais\config.toml"
    if (Test-Path $configPath) {
        try {
            $content = Get-Content $configPath -Raw -ErrorAction SilentlyContinue
            return $content -match "auto_analysis\s*=\s*true"
        } catch {
            return $false
        }
    }
    return $false
}

# 初始化 stderr 捕获
function Initialize-AISStderrCapture {
    try {
        # 创建临时文件
        New-Item -Path $Global:AIS_STDERR_FILE -ItemType File -Force | Out-Null
        
        # 记录当前错误数量作为基准
        $Global:AIS_ORIGINAL_ERROR_COUNT = $Global:Error.Count
        
        return $true
    } catch {
        return $false
    }
}

# 获取并清理捕获的 stderr
function Get-AISCapturedStderr {
    $stderrContent = ""
    
    try {
        # 从 PowerShell 错误流获取新的错误
        $newErrorCount = $Global:Error.Count - $Global:AIS_ORIGINAL_ERROR_COUNT
        if ($newErrorCount -gt 0) {
            $recentErrors = $Global:Error | Select-Object -First $newErrorCount
            $stderrContent = ($recentErrors | ForEach-Object { $_.ToString() }) -join "`n"
        }
        
        # 从文件读取（如果有重定向的内容）
        if (Test-Path $Global:AIS_STDERR_FILE) {
            $fileContent = Get-Content $Global:AIS_STDERR_FILE -Raw -ErrorAction SilentlyContinue
            if ($fileContent) {
                $stderrContent += "`n$fileContent"
                Clear-Content $Global:AIS_STDERR_FILE -ErrorAction SilentlyContinue
            }
        }
        
        # 更新错误基准
        $Global:AIS_ORIGINAL_ERROR_COUNT = $Global:Error.Count
        
    } catch {
        # 静默失败，返回空字符串
    }
    
    return $stderrContent
}

# 清理 stderr 捕获资源
function Remove-AISStderrCapture {
    try {
        if (Test-Path $Global:AIS_STDERR_FILE) {
            Remove-Item $Global:AIS_STDERR_FILE -Force -ErrorAction SilentlyContinue
        }
    } catch {
        # 静默失败
    }
}

# 过滤和清理 stderr 内容
function ConvertTo-AISFilteredStderr {
    param([string]$StderrContent)
    
    if (-not $StderrContent) { 
        return "" 
    }
    
    try {
        # 过滤无关内容
        $lines = $StderrContent -split "`n" | Where-Object { 
            $_ -and 
            $_ -notmatch "^\s*$" -and 
            $_ -notmatch "_ais_|AIS_" -and
            $_ -notmatch "At line:|CategoryInfo|FullyQualifiedErrorId" -and
            $_ -notmatch "^\s*\+\s+CategoryInfo" -and
            $_ -notmatch "^\s*\+\s+FullyQualifiedErrorId"
        }
        
        # 限制行数和总长度
        $filtered = ($lines | Select-Object -First 10) -join " "
        if ($filtered.Length -gt 1500) {
            $filtered = $filtered.Substring(0, 1500)
        }
        
        # 转义特殊字符以便安全传递
        $filtered = $filtered -replace '"', '\"' -replace '`', '``'
        
        return $filtered
    } catch {
        return ""
    }
}

# 检查命令是否应该被分析（去重机制）
function Test-AISCommandShouldAnalyze {
    param([string]$Command)
    
    if (-not $Command) { 
        return $false 
    }
    
    try {
        $currentTime = [int][double]::Parse((Get-Date -UFormat %s))
        $timeDiff = $currentTime - $Global:AIS_LAST_ANALYZED_TIME
        
        # 如果与上次分析的命令相同，且时间间隔小于30秒，跳过
        if ($Command -eq $Global:AIS_LAST_ANALYZED_COMMAND -and $timeDiff -lt 30) {
            return $false  # 跳过重复分析
        }
        
        # 更新记录
        $Global:AIS_LAST_ANALYZED_COMMAND = $Command
        $Global:AIS_LAST_ANALYZED_TIME = $currentTime
        
        return $true
    } catch {
        return $false
    }
}

# PowerShell 命令执行后钩子
function Invoke-AISCommandAnalysis {
    $lastExitCode = $LASTEXITCODE
    
    # 只处理非零退出码
    if ($lastExitCode -and $lastExitCode -ne 0) {
        if (Test-AISAutoAnalysis) {
            try {
                # 获取最后执行的命令
                $history = Get-History -Count 1 -ErrorAction SilentlyContinue
                if (-not $history) { return }
                
                $lastCommand = $history.CommandLine
                
                # 过滤内部命令和特殊情况
                if ($lastCommand -and 
                    $lastCommand -notmatch "_ais_|AIS_" -and 
                    $lastCommand -notmatch "Get-History|Invoke-AISCommandAnalysis") {
                    
                    # 检查是否应该分析此命令（去重机制）
                    if (Test-AISCommandShouldAnalyze $lastCommand) {
                        # 获取捕获的 stderr 内容
                        $capturedStderr = Get-AISCapturedStderr
                        $filteredStderr = ConvertTo-AISFilteredStderr $capturedStderr
                        
                        # 调用 ais analyze 进行分析，传递 stderr
                        Write-Host ""  # 添加空行分隔
                        
                        try {
                            if ($filteredStderr) {
                                & ais analyze --exit-code $lastExitCode --command $lastCommand --stderr $filteredStderr
                            } else {
                                & ais analyze --exit-code $lastExitCode --command $lastCommand
                            }
                        } catch {
                            # 静默失败，避免影响用户正常使用
                        }
                    }
                }
            } catch {
                # 静默失败，避免影响用户正常使用
            }
        }
    }
}

# 增强的提示符函数
function global:prompt {
    # 在每次提示符显示前执行错误分析
    Invoke-AISCommandAnalysis
    
    # 返回标准提示符
    $currentPath = $executionContext.SessionState.Path.CurrentLocation
    "PS $currentPath> "
}

# 主初始化函数
function Initialize-AISIntegration {
    if (-not (Test-AISAvailability)) {
        return $false
    }
    
    try {
        # 初始化 stderr 捕获
        if (Initialize-AISStderrCapture) {
            # 注册清理事件
            Register-EngineEvent PowerShell.Exiting -Action { 
                Remove-AISStderrCapture 
            } -SupportEvent | Out-Null
            
            return $true
        }
    } catch {
        # 静默失败
    }
    
    return $false
}

# 清理函数
function Remove-AISIntegration {
    Remove-AISStderrCapture
    
    # 移除事件处理器
    try {
        Get-EventSubscriber | Where-Object { $_.Action.ToString() -match "Remove-AISStderrCapture" } | 
            Unregister-Event -ErrorAction SilentlyContinue
    } catch {
        # 静默失败
    }
}

# 检测 PowerShell 版本兼容性
function Test-AISPowerShellCompatibility {
    try {
        $version = $PSVersionTable.PSVersion
        # 支持 PowerShell 5.1+ 和 PowerShell Core 6.0+
        return ($version.Major -ge 5 -and $version.Minor -ge 1) -or ($version.Major -ge 6)
    } catch {
        return $false
    }
}

# 获取 PowerShell 集成状态
function Get-AISIntegrationStatus {
    $status = @{
        AISAvailable = Test-AISAvailability
        AutoAnalysisEnabled = Test-AISAutoAnalysis
        PowerShellCompatible = Test-AISPowerShellCompatibility
        IntegrationActive = $false
    }
    
    # 检查是否已经初始化
    if ($Global:AIS_STDERR_FILE -and (Test-Path $Global:AIS_STDERR_FILE)) {
        $status.IntegrationActive = $true
    }
    
    return $status
}

# 自动初始化（如果满足条件）
if (Test-AISPowerShellCompatibility) {
    Initialize-AISIntegration | Out-Null
}