# AIS Windows PowerShell 安装脚本
# AIS Windows PowerShell Installation Script

param(
    [string]$InstallMethod = "pip",  # pip, source, local
    [string]$PythonCommand = "python",
    [switch]$NoShellIntegration,
    [switch]$GlobalInstall,
    [switch]$Help
)

# 颜色定义
function Write-Info { param($Message) Write-Host "ℹ️  $Message" -ForegroundColor Blue }
function Write-Success { param($Message) Write-Host "✅ $Message" -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host "⚠️  $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "❌ $Message" -ForegroundColor Red }

# 显示帮助信息
function Show-Help {
    Write-Host @"
AIS Windows 安装脚本

用法: .\install.ps1 [选项]

选项:
  -InstallMethod <method>    安装方式: pip, source, local (默认: pip)
  -PythonCommand <command>   Python命令 (默认: python)
  -NoShellIntegration        跳过Shell集成
  -GlobalInstall             全局安装
  -Help                      显示此帮助

示例:
  .\install.ps1                           # 使用pip安装
  .\install.ps1 -InstallMethod source     # 从源码安装
  .\install.ps1 -GlobalInstall           # 全局安装
"@
}

# 检查管理员权限
function Test-IsAdmin {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# 检查Python环境
function Test-Python {
    Write-Info "检查Python环境..."
    
    try {
        $pythonVersion = & $PythonCommand --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Python未安装或不可用"
            Write-Info "请访问 https://www.python.org/downloads/ 安装Python"
            return $false
        }
        
        $versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)\.(\d+)"
        if ($versionMatch) {
            $major = [int]$matches[1]
            $minor = [int]$matches[2]
            
            if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
                Write-Error "Python版本过低，需要Python 3.8或更高版本"
                Write-Info "当前版本: $pythonVersion"
                return $false
            }
        }
        
        Write-Success "Python环境检查通过: $pythonVersion"
        return $true
    }
    catch {
        Write-Error "检查Python环境时出错: $_"
        return $false
    }
}

# 检查pip环境
function Test-Pip {
    Write-Info "检查pip环境..."
    
    try {
        $pipVersion = & $PythonCommand -m pip --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Error "pip不可用"
            Write-Info "尝试安装pip..."
            & $PythonCommand -m ensurepip --upgrade
            if ($LASTEXITCODE -ne 0) {
                Write-Error "pip安装失败"
                return $false
            }
        }
        
        Write-Success "pip环境检查通过: $pipVersion"
        return $true
    }
    catch {
        Write-Error "检查pip环境时出错: $_"
        return $false
    }
}

# 从PyPI安装
function Install-FromPyPI {
    Write-Info "从PyPI安装AIS..."
    
    try {
        if ($GlobalInstall) {
            & $PythonCommand -m pip install --upgrade ais-terminal
        } else {
            & $PythonCommand -m pip install --user --upgrade ais-terminal
        }
        
        if ($LASTEXITCODE -ne 0) {
            Write-Error "从PyPI安装失败"
            return $false
        }
        
        Write-Success "从PyPI安装成功"
        return $true
    }
    catch {
        Write-Error "安装过程中出错: $_"
        return $false
    }
}

# 从源码安装
function Install-FromSource {
    Write-Info "从GitHub源码安装AIS..."
    
    try {
        $tempDir = New-TemporaryFile | ForEach-Object { Remove-Item $_; New-Item -ItemType Directory -Path $_ }
        Set-Location $tempDir
        
        Write-Info "克隆仓库..."
        git clone https://github.com/kangvcar/ais.git
        if ($LASTEXITCODE -ne 0) {
            Write-Error "克隆仓库失败"
            return $false
        }
        
        Set-Location ais
        
        Write-Info "安装依赖并构建..."
        & $PythonCommand -m pip install --upgrade build
        & $PythonCommand -m build
        
        if ($GlobalInstall) {
            & $PythonCommand -m pip install dist/*.whl
        } else {
            & $PythonCommand -m pip install --user dist/*.whl
        }
        
        if ($LASTEXITCODE -ne 0) {
            Write-Error "从源码安装失败"
            return $false
        }
        
        Write-Success "从源码安装成功"
        return $true
    }
    catch {
        Write-Error "安装过程中出错: $_"
        return $false
    }
    finally {
        Set-Location $env:USERPROFILE
        if (Test-Path $tempDir) {
            Remove-Item -Recurse -Force $tempDir
        }
    }
}

# 本地安装
function Install-Local {
    Write-Info "本地安装AIS..."
    
    if (-not (Test-Path "pyproject.toml")) {
        Write-Error "未找到pyproject.toml文件，请确保在项目根目录下运行"
        return $false
    }
    
    try {
        & $PythonCommand -m pip install --upgrade build
        & $PythonCommand -m build
        
        if ($GlobalInstall) {
            & $PythonCommand -m pip install dist/*.whl
        } else {
            & $PythonCommand -m pip install --user dist/*.whl
        }
        
        if ($LASTEXITCODE -ne 0) {
            Write-Error "本地安装失败"
            return $false
        }
        
        Write-Success "本地安装成功"
        return $true
    }
    catch {
        Write-Error "安装过程中出错: $_"
        return $false
    }
}

# 测试安装
function Test-Installation {
    Write-Info "测试安装..."
    
    try {
        $aisVersion = & ais --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Error "AIS命令不可用"
            return $false
        }
        
        Write-Success "安装测试通过: $aisVersion"
        return $true
    }
    catch {
        Write-Error "测试安装时出错: $_"
        return $false
    }
}

# PowerShell集成
function Install-PowerShellIntegration {
    Write-Info "配置PowerShell集成..."
    
    try {
        $profilePath = $PROFILE.CurrentUserCurrentHost
        if (-not (Test-Path $profilePath)) {
            New-Item -ItemType File -Path $profilePath -Force | Out-Null
        }
        
        $integrationCode = @"

# AIS PowerShell 集成
function Invoke-AISOnError {
    if (`$LASTEXITCODE -ne 0 -and `$LASTEXITCODE -ne `$null) {
        `$lastCommand = Get-History -Count 1 | Select-Object -ExpandProperty CommandLine
        if (`$lastCommand -and `$lastCommand -notmatch "^(ais|cd|ls|dir|Get-|Set-|New-|Remove-)") {
            Write-Host "检测到命令执行失败，正在分析..." -ForegroundColor Yellow
            & ais analyze "`$lastCommand" --exit-code `$LASTEXITCODE
        }
    }
}

# 为每个命令添加错误检查
`$ExecutionContext.InvokeCommand.PostCommandLookupAction = {
    param(`$commandName, `$lookupEventArgs)
    if (`$commandName -ne "ais") {
        `$lookupEventArgs.CommandScriptBlock = {
            & @args
            Invoke-AISOnError
        }.GetNewClosure()
    }
}
"@
        
        if (-not (Get-Content $profilePath -Raw).Contains("AIS PowerShell 集成")) {
            Add-Content -Path $profilePath -Value $integrationCode
            Write-Success "PowerShell集成配置完成"
            Write-Info "请重新启动PowerShell或运行: . `$PROFILE"
        } else {
            Write-Info "PowerShell集成已存在"
        }
        
        return $true
    }
    catch {
        Write-Error "配置PowerShell集成时出错: $_"
        return $false
    }
}

# 主函数
function Main {
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "         AIS Windows 安装工具" -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
    
    if ($Help) {
        Show-Help
        return
    }
    
    # 检查管理员权限（如果需要全局安装）
    if ($GlobalInstall -and -not (Test-IsAdmin)) {
        Write-Warning "全局安装需要管理员权限"
        Write-Info "请以管理员身份运行PowerShell"
        return
    }
    
    # 检查Python环境
    if (-not (Test-Python)) {
        return
    }
    
    # 检查pip环境
    if (-not (Test-Pip)) {
        return
    }
    
    # 根据安装方式执行安装
    $installSuccess = $false
    switch ($InstallMethod.ToLower()) {
        "pip" {
            $installSuccess = Install-FromPyPI
        }
        "source" {
            $installSuccess = Install-FromSource
        }
        "local" {
            $installSuccess = Install-Local
        }
        default {
            Write-Error "不支持的安装方式: $InstallMethod"
            Show-Help
            return
        }
    }
    
    if (-not $installSuccess) {
        Write-Error "安装失败"
        return
    }
    
    # 测试安装
    if (-not (Test-Installation)) {
        return
    }
    
    # 配置Shell集成
    if (-not $NoShellIntegration) {
        Install-PowerShellIntegration
    }
    
    Write-Success "🎉 AIS安装完成！"
    Write-Info "使用方法:"
    Write-Info "  ais --help              # 查看帮助"
    Write-Info "  ais ask '如何使用git'    # 向AI提问"
    Write-Info "  ais config              # 配置设置"
    Write-Info ""
    Write-Info "PowerShell集成已启用，命令执行失败时将自动调用AIS分析"
}

# 运行主函数
Main