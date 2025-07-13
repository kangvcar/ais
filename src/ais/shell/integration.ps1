# AIS PowerShell 集成脚本
# AIS PowerShell Integration Script
# 
# 功能：自动捕获命令执行错误并调用 AIS 进行分析
# Features: Automatically capture command execution errors and call AIS for analysis

# 检查 AIS 是否可用
function Test-AisAvailability {
    try {
        $null = Get-Command ais -ErrorAction Stop
        return $true
    }
    catch {
        return $false
    }
}

# 检查自动分析是否开启
function Test-AisAutoAnalysis {
    if (-not (Test-AisAvailability)) {
        return $false
    }
    
    # 检查配置文件中的 auto_analysis 设置
    $configFile = Join-Path $env:USERPROFILE ".config\ais\config.toml"
    if (Test-Path $configFile) {
        try {
            $content = Get-Content $configFile -Raw
            return $content -match "auto_analysis\s*=\s*true"
        }
        catch {
            return $false
        }
    }
    else {
        return $false  # 默认关闭
    }
}

# 获取上一个命令的信息
function Get-LastCommand {
    $history = Get-History -Count 1 -ErrorAction SilentlyContinue
    if ($history) {
        return @{
            Command = $history.CommandLine
            ExitCode = $LASTEXITCODE
            Id = $history.Id
        }
    }
    return $null
}

# AIS 错误分析函数
function Invoke-AisErrorAnalysis {
    param(
        [string]$Command,
        [int]$ExitCode,
        [string]$ErrorOutput = ""
    )
    
    # 过滤内部命令和特殊情况
    if ($Command -match "_ais_|ais_|Get-History|Test-|Invoke-") {
        return
    }
    
    try {
        Write-Host ""  # 添加空行分隔
        
        # 调用 ais analyze 进行分析
        $arguments = @(
            "analyze"
            "--exit-code", $ExitCode
            "--command", $Command
        )
        
        if ($ErrorOutput) {
            $arguments += "--stderr", $ErrorOutput
        }
        
        & ais @arguments
    }
    catch {
        # 静默失败，不影响正常使用
    }
}

# PowerShell 命令执行监控
function Start-AisCommandMonitoring {
    # 检查是否已经设置了监控
    if ($Global:AisCommandMonitoringEnabled) {
        return
    }
    
    $Global:AisCommandMonitoringEnabled = $true
    $Global:AisLastHistoryId = (Get-History -Count 1 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id -ErrorAction SilentlyContinue)
    
    # 注册 PowerShell 事件处理
    $timer = New-Object System.Timers.Timer
    $timer.Interval = 500  # 500ms 检查间隔
    $timer.Enabled = $false
    
    # 注册事件处理器
    $action = {
        try {
            if (-not (Test-AisAutoAnalysis)) {
                return
            }
            
            $currentHistory = Get-History -Count 1 -ErrorAction SilentlyContinue
            if (-not $currentHistory) {
                return
            }
            
            # 检查是否有新的命令执行
            if ($currentHistory.Id -le $Global:AisLastHistoryId) {
                return
            }
            
            $Global:AisLastHistoryId = $currentHistory.Id
            
            # 检查命令是否失败（非零退出码）
            if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne $null) {
                # 获取可能的错误输出
                $errorOutput = ""
                if ($Error.Count -gt 0) {
                    $errorOutput = $Error[0].ToString()
                }
                
                Invoke-AisErrorAnalysis -Command $currentHistory.CommandLine -ExitCode $LASTEXITCODE -ErrorOutput $errorOutput
            }
        }
        catch {
            # 静默处理错误
        }
    }
    
    Register-ObjectEvent -InputObject $timer -EventName Elapsed -Action $action -SourceIdentifier "AisCommandMonitor" | Out-Null
    $timer.Enabled = $true
    $Global:AisTimer = $timer
}

# 停止 AIS 命令监控
function Stop-AisCommandMonitoring {
    if ($Global:AisTimer) {
        $Global:AisTimer.Enabled = $false
        $Global:AisTimer.Dispose()
        Unregister-Event -SourceIdentifier "AisCommandMonitor" -ErrorAction SilentlyContinue
        Remove-Variable -Name AisTimer -Scope Global -ErrorAction SilentlyContinue
    }
    $Global:AisCommandMonitoringEnabled = $false
}

# 增强的 PowerShell 提示符集成
function prompt {
    # 保存原始提示符
    if (-not $Global:OriginalPrompt) {
        $Global:OriginalPrompt = $function:prompt
    }
    
    # 检查上一个命令是否失败
    if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne $null -and (Test-AisAutoAnalysis)) {
        $lastCommand = Get-LastCommand
        if ($lastCommand -and $lastCommand.Command) {
            # 异步执行分析，避免阻塞提示符
            Start-Job -ScriptBlock {
                param($cmd, $exitCode)
                try {
                    & ais analyze --exit-code $exitCode --command $cmd
                }
                catch {
                    # 静默失败
                }
            } -ArgumentList $lastCommand.Command, $LASTEXITCODE | Out-Null
        }
    }
    
    # 调用原始提示符或默认提示符
    if ($Global:OriginalPrompt -and $Global:OriginalPrompt -ne $function:prompt) {
        & $Global:OriginalPrompt
    }
    else {
        "PS $($executionContext.SessionState.Path.CurrentLocation)$('>' * ($nestedPromptLevel + 1)) "
    }
}

# Windows Terminal 集成支持
function Set-WindowsTerminalIntegration {
    # 检查是否在 Windows Terminal 中运行
    if ($env:WT_SESSION) {
        # 设置 Windows Terminal 特定的配置
        $Host.UI.RawUI.WindowTitle = "PowerShell - AIS Enabled"
        
        # 添加 Windows Terminal 特定的错误处理
        $ExecutionContext.InvokeCommand.CommandNotFoundAction = {
            param($CommandName, $CommandLookupEventArgs)
            
            if (Test-AisAutoAnalysis) {
                # 异步分析未找到的命令
                Start-Job -ScriptBlock {
                    param($cmd)
                    try {
                        & ais analyze --exit-code 127 --command $cmd --stderr "The term '$cmd' is not recognized as a cmdlet, function, script file, or executable program."
                    }
                    catch {
                        # 静默失败
                    }
                } -ArgumentList $CommandName | Out-Null
            }
        }
    }
}

# 错误处理增强
$ErrorActionPreference_Original = $ErrorActionPreference
$ErrorActionPreference = "SilentlyContinue"

# 自动启动监控（如果 AIS 可用且自动分析开启）
if (Test-AisAvailability) {
    # 设置 Windows Terminal 集成
    Set-WindowsTerminalIntegration
    
    # 如果自动分析开启，启动监控
    if (Test-AisAutoAnalysis) {
        Start-AisCommandMonitoring
        
        # 显示一次性启动消息
        if (-not $Global:AisWelcomeShown) {
            Write-Host "🤖 " -ForegroundColor Blue -NoNewline
            Write-Host "AIS PowerShell 集成已启用 - 命令失败时将自动显示AI分析" -ForegroundColor Green
            Write-Host "💡 " -ForegroundColor Yellow -NoNewline
            Write-Host "使用 'ais off' 关闭自动分析，'ais on' 重新开启" -ForegroundColor Gray
            $Global:AisWelcomeShown = $true
        }
    }
}

# 恢复错误处理设置
$ErrorActionPreference = $ErrorActionPreference_Original

# 清理变量
Remove-Variable -Name ErrorActionPreference_Original -ErrorAction SilentlyContinue

# 导出函数供手动使用
Export-ModuleMember -Function Test-AisAvailability, Test-AisAutoAnalysis, Invoke-AisErrorAnalysis, Start-AisCommandMonitoring, Stop-AisCommandMonitoring

# 模块清理函数
if ($PSVersionTable.PSVersion.Major -ge 5) {
    $MyInvocation.MyCommand.ScriptBlock.Module.OnRemove = {
        Stop-AisCommandMonitoring
        if ($Global:OriginalPrompt) {
            $function:prompt = $Global:OriginalPrompt
        }
    }
}