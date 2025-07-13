# AIS Windows PowerShell 智能安装脚本
# AIS Windows PowerShell Intelligent Installation Script

param(
    [ValidateSet("auto", "user", "system", "container")]
    [string]$InstallMode = "auto",
    
    [string]$PythonCommand = "python",
    [switch]$SkipShellIntegration,
    [switch]$SkipChecks,
    [switch]$Help
)

# 颜色定义和辅助函数
function Write-Info { 
    param($Message) 
    Write-Host "ℹ️  $Message" -ForegroundColor Blue 
}

function Write-Success { 
    param($Message) 
    Write-Host "✅ $Message" -ForegroundColor Green 
}

function Write-Warning { 
    param($Message) 
    Write-Host "⚠️  $Message" -ForegroundColor Yellow 
}

function Write-ErrorMsg { 
    param($Message) 
    Write-Host "❌ $Message" -ForegroundColor Red 
}

# 显示帮助信息
function Show-Help {
    Write-Host @"
AIS Windows 智能安装脚本

用法: .\install.ps1 [选项]

安装模式:
  -InstallMode <mode>        安装模式: auto, user, system, container (默认: auto)
    auto                     自动检测环境并选择最佳方式
    user                     用户级pipx安装 (推荐个人使用)
    system                   系统级pipx安装 (推荐多用户环境)
    container                容器化安装

其他选项:
  -PythonCommand <command>   Python命令 (默认: python)
  -SkipShellIntegration      跳过Shell集成设置
  -SkipChecks               跳过安装后健康检查
  -Help                     显示此帮助信息

安装示例:
  个人安装: .\install.ps1
  系统安装: .\install.ps1 -InstallMode system
  跳过集成: .\install.ps1 -SkipShellIntegration

💡 推荐使用pipx进行安装，提供最佳的安全性和可维护性
"@
    exit 0
}

# 检查命令是否存在
function Test-CommandExists {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# 检测环境
function Get-Environment {
    if ($env:CONTAINER -or $env:container) {
        return "container"
    }
    elseif (([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
        return "admin"
    }
    else {
        return "user"
    }
}

# 安装pipx
function Install-Pipx {
    Write-Info "📦 安装pipx..."
    
    if (Test-CommandExists "pipx") {
        Write-Success "pipx已安装"
        return $true
    }
    
    try {
        # 尝试使用pip安装pipx
        & $PythonCommand -m pip install --user pipx
        
        # 确保pipx在PATH中
        & $PythonCommand -m pipx ensurepath
        
        # 刷新环境变量
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        
        if (Test-CommandExists "pipx") {
            Write-Success "pipx安装成功"
            return $true
        }
        else {
            Write-ErrorMsg "pipx安装失败"
            return $false
        }
    }
    catch {
        Write-ErrorMsg "pipx安装失败: $($_.Exception.Message)"
        return $false
    }
}

# 健康检查
function Test-Installation {
    Write-Info "🔍 执行安装后健康检查..."
    
    # 检查ais命令
    if (-not (Test-CommandExists "ais")) {
        Write-ErrorMsg "ais命令未找到"
        return $false
    }
    
    # 检查版本
    try {
        $version = & ais --version 2>$null | Select-Object -First 1
        Write-Success "ais命令可用: $version"
    }
    catch {
        Write-ErrorMsg "无法获取ais版本信息"
        return $false
    }
    
    # 测试基本功能
    try {
        & ais config --help | Out-Null
        Write-Success "基本功能测试通过"
    }
    catch {
        Write-Warning "基本功能测试失败，但安装可能仍然成功"
    }
    
    return $true
}

# 用户级安装
function Install-UserMode {
    Write-Info "👤 开始用户级pipx安装..."
    
    # 安装pipx
    if (-not (Install-Pipx)) {
        exit 1
    }
    
    # 安装AIS
    Write-Info "📦 安装ais-terminal..."
    try {
        & pipx install ais-terminal
        Write-Success "✅ 用户级安装完成！"
        Write-Info "💡 如需为其他用户安装，请以管理员身份运行: .\install.ps1 -InstallMode system"
    }
    catch {
        Write-ErrorMsg "AIS安装失败: $($_.Exception.Message)"
        exit 1
    }
    
    # 设置PowerShell集成
    if (-not $SkipShellIntegration) {
        Write-Info "🔧 设置PowerShell集成..."
        try {
            # 运行 ais setup 来创建集成脚本
            & ais setup
            
            Write-Info "💡 PowerShell集成设置完成！"
            Write-Warning "请按照上面的说明完成最后的集成配置"
        }
        catch {
            Write-Warning "PowerShell集成设置可能需要手动完成"
            Write-Info "稍后可以运行: ais setup"
        }
    }
}

# 系统级安装
function Install-SystemMode {
    Write-Info "🏢 开始系统级pipx安装..."
    
    # 检查管理员权限
    if ((Get-Environment) -ne "admin") {
        Write-ErrorMsg "系统级安装需要管理员权限"
        Write-Info "请以管理员身份重新运行PowerShell"
        exit 1
    }
    
    # 安装pipx
    if (-not (Install-Pipx)) {
        exit 1
    }
    
    # 设置系统级pipx环境
    $env:PIPX_HOME = "C:\ProgramData\pipx"
    $env:PIPX_BIN_DIR = "C:\Program Files\pipx\bin"
    
    # 安装AIS
    Write-Info "📦 安装ais-terminal到系统位置..."
    try {
        & pipx install ais-terminal
        
        # 确保系统PATH包含pipx bin目录
        $systemPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
        if ($systemPath -notlike "*$($env:PIPX_BIN_DIR)*") {
            [Environment]::SetEnvironmentVariable("PATH", "$systemPath;$($env:PIPX_BIN_DIR)", "Machine")
        }
        
        Write-Success "✅ 系统级安装完成！所有用户都可以使用ais命令"
        Write-Info "💡 用户可以运行: ais setup 来设置PowerShell集成"
    }
    catch {
        Write-ErrorMsg "AIS系统级安装失败: $($_.Exception.Message)"
        exit 1
    }
}

# 容器化安装
function Install-ContainerMode {
    Write-Info "🐳 开始容器化安装..."
    
    # 在容器中使用简单的pip安装
    Write-Info "📦 在容器中安装ais-terminal..."
    try {
        & $PythonCommand -m pip install ais-terminal
        Write-Success "✅ 容器化安装完成！"
        Write-Info "💡 容器内直接使用: ais --version"
    }
    catch {
        Write-ErrorMsg "容器化安装失败: $($_.Exception.Message)"
        exit 1
    }
}

# 主安装函数
function Start-Installation {
    Write-Host "================================================"
    Write-Host "         AIS - AI 智能终端助手 安装器"
    Write-Host "================================================"
    Write-Host "版本: latest"
    Write-Host "GitHub: https://github.com/kangvcar/ais"
    Write-Host ""
    
    $env = Get-Environment
    Write-Info "🔍 检测到环境: $env"
    
    # 自动选择最佳安装模式
    if ($InstallMode -eq "auto") {
        switch ($env) {
            "container" {
                $InstallMode = "container"
                Write-Info "🐳 容器环境：使用容器化安装"
            }
            "admin" {
                $InstallMode = "system"
                Write-Info "🏢 管理员环境：使用系统级pipx安装"
            }
            "user" {
                $InstallMode = "user"
                Write-Info "👤 用户环境：使用用户级pipx安装"
            }
        }
    }
    
    # 检查Python
    if (-not (Test-CommandExists $PythonCommand)) {
        Write-ErrorMsg "Python命令 '$PythonCommand' 未找到"
        Write-Info "请安装Python或指定正确的Python命令"
        exit 1
    }
    
    # 执行对应的安装模式
    switch ($InstallMode) {
        "user" {
            Install-UserMode
        }
        "system" {
            Install-SystemMode
        }
        "container" {
            Install-ContainerMode
        }
        default {
            Write-ErrorMsg "未知的安装模式: $InstallMode"
            exit 1
        }
    }
    
    # 执行健康检查
    if (-not $SkipChecks) {
        if (-not (Test-Installation)) {
            Write-Warning "健康检查失败，但安装可能成功。请手动验证:"
            Write-Info "  运行: ais --version"
            Write-Info "  测试: ais ask 'hello'"
        }
    }
    
    Write-Host ""
    Write-Success "🎉 AIS安装完成！"
    Write-Info "💡 快速开始:"
    Write-Info "  测试安装: ais --version"
    Write-Info "  AI对话: ais ask '你好'"
    Write-Info "  获取帮助: ais --help"
}

# 主程序入口
if ($Help) {
    Show-Help
}

# 错误处理
$ErrorActionPreference = "Stop"

try {
    Start-Installation
}
catch {
    Write-ErrorMsg "安装过程中发生错误: $($_.Exception.Message)"
    Write-Info "💡 如需帮助，请访问: https://github.com/kangvcar/ais/issues"
    exit 1
}