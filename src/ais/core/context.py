"""上下文收集模块。"""

import os
import subprocess
import socket
import getpass
import grp
from pathlib import Path
from typing import Dict, Any, List, Optional


def is_sensitive_path(path: str, sensitive_dirs: List[str]) -> bool:
    """检查路径是否为敏感目录。"""
    path = Path(path).expanduser().resolve()

    for sensitive_dir in sensitive_dirs:
        sensitive_path = Path(sensitive_dir).expanduser().resolve()
        try:
            path.relative_to(sensitive_path)
            return True
        except ValueError:
            continue
    return False


def filter_sensitive_data(text: str) -> str:
    """过滤敏感数据。"""
    # 简单的密码、密钥过滤
    import re

    # 过滤常见的密钥模式
    patterns = [
        r"(?i)(password|passwd|pwd|secret|key|token)[\s=:]+[^\s]+",
        r"sk-[a-zA-Z0-9]{20,}",  # OpenAI API 密钥格式
        r"[A-Za-z0-9]{20,}",  # 通用长字符串
    ]

    filtered_text = text
    for pattern in patterns:
        filtered_text = re.sub(pattern, lambda m: m.group().split()[0] + " ***", filtered_text)

    return filtered_text


def run_safe_command(command: str, timeout: int = 5) -> Optional[str]:
    """安全地运行命令并返回输出。"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def collect_network_context() -> Dict[str, Any]:
    """收集网络连接上下文信息。"""
    network_info = {}

    # 检查基础网络连接
    try:
        # 测试DNS解析
        socket.gethostbyname("8.8.8.8")
        network_info["dns_resolution"] = "working"
    except socket.gaierror:
        network_info["dns_resolution"] = "failed"
    except Exception:
        network_info["dns_resolution"] = "unknown"

    # 检查互联网连接
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(("8.8.8.8", 53))
        sock.close()
        network_info["internet_connectivity"] = result == 0
    except Exception:
        network_info["internet_connectivity"] = False

    # 检查代理设置
    proxy_vars = ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]
    proxy_settings = {}
    for var in proxy_vars:
        if var in os.environ:
            proxy_settings[var] = os.environ[var]
    network_info["proxy_settings"] = proxy_settings if proxy_settings else None

    # 检查常用端口
    common_ports = [22, 80, 443, 8080]
    open_ports = []
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex(("localhost", port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except Exception:
            pass
    network_info["local_open_ports"] = open_ports

    return network_info


def collect_permission_context(command: str, cwd: str) -> Dict[str, Any]:
    """收集权限相关上下文信息。"""
    permission_info = {}

    # 基本用户信息
    try:
        current_user = getpass.getuser()
        permission_info["current_user"] = current_user
        permission_info["user_id"] = os.getuid()
        permission_info["group_id"] = os.getgid()
    except Exception:
        permission_info["current_user"] = "unknown"

    # 用户组信息
    try:
        groups = [grp.getgrgid(gid).gr_name for gid in os.getgroups()]
        permission_info["user_groups"] = groups
    except Exception:
        permission_info["user_groups"] = []

    # 目录权限检查
    try:
        permission_info["cwd_readable"] = os.access(cwd, os.R_OK)
        permission_info["cwd_writable"] = os.access(cwd, os.W_OK)
        permission_info["cwd_executable"] = os.access(cwd, os.X_OK)
    except Exception:
        permission_info["cwd_readable"] = False
        permission_info["cwd_writable"] = False
        permission_info["cwd_executable"] = False

    # 检查sudo可用性
    try:
        sudo_result = subprocess.run(["sudo", "-n", "true"], capture_output=True, timeout=2)
        permission_info["sudo_available"] = sudo_result.returncode == 0
    except Exception:
        permission_info["sudo_available"] = False

    # 分析命令中的目标文件/目录权限
    target_path = extract_target_path(command)
    if target_path:
        permission_info["target_path"] = target_path
        try:
            if os.path.exists(target_path):
                stat_info = os.stat(target_path)
                permission_info["target_permissions"] = oct(stat_info.st_mode)[-3:]
                permission_info["target_owner"] = stat_info.st_uid
                permission_info["target_group"] = stat_info.st_gid
            else:
                # 检查父目录权限
                parent_dir = os.path.dirname(target_path)
                if os.path.exists(parent_dir):
                    permission_info["parent_dir_writable"] = os.access(parent_dir, os.W_OK)
        except Exception:
            pass

    return permission_info


def extract_target_path(command: str) -> Optional[str]:
    """从命令中提取目标路径。"""
    # 简单的路径提取逻辑
    parts = command.split()
    if len(parts) < 2:
        return None

    # 常见的文件操作命令
    file_commands = [
        "cat",
        "ls",
        "mkdir",
        "rmdir",
        "rm",
        "cp",
        "mv",
        "chmod",
        "chown",
    ]

    if parts[0] in file_commands:
        # 查找最后一个不以-开头的参数
        for i in range(len(parts) - 1, 0, -1):
            if not parts[i].startswith("-"):
                return parts[i]

    return None


def detect_project_type_enhanced(cwd: str) -> Dict[str, Any]:
    """增强的项目类型检测。"""
    project_info = {
        "project_type": "unknown",
        "framework": None,
        "build_system": None,
        "package_manager": None,
        "config_files": {},
        "key_files": [],
    }

    cwd_path = Path(cwd)

    # 项目类型指示器
    type_indicators = {
        "python": {
            "files": [
                "requirements.txt",
                "pyproject.toml",
                "setup.py",
                "setup.cfg",
                "Pipfile",
            ],
            "frameworks": {
                "django": ["manage.py", "settings.py"],
                "flask": ["app.py", "wsgi.py"],
                "fastapi": ["main.py", "api.py"],
            },
            "build_systems": {
                "poetry": ["pyproject.toml"],
                "setuptools": ["setup.py"],
                "pipenv": ["Pipfile"],
            },
        },
        "node": {
            "files": ["package.json", "yarn.lock", "package-lock.json"],
            "frameworks": {
                "react": ["src/App.js", "src/App.jsx", "public/index.html"],
                "vue": ["src/main.js", "vue.config.js"],
                "express": ["app.js", "server.js"],
            },
            "build_systems": {
                "npm": ["package-lock.json"],
                "yarn": ["yarn.lock"],
                "pnpm": ["pnpm-lock.yaml"],
            },
        },
        "docker": {
            "files": [
                "Dockerfile",
                "docker-compose.yml",
                "docker-compose.yaml",
                ".dockerignore",
            ],
            "frameworks": {},
            "build_systems": {
                "docker": ["Dockerfile"],
                "compose": ["docker-compose.yml", "docker-compose.yaml"],
            },
        },
        "rust": {
            "files": ["Cargo.toml", "Cargo.lock"],
            "frameworks": {"axum": ["Cargo.toml"], "rocket": ["Cargo.toml"]},
            "build_systems": {"cargo": ["Cargo.toml"]},
        },
        "go": {
            "files": ["go.mod", "go.sum", "main.go"],
            "frameworks": {"gin": ["go.mod"], "echo": ["go.mod"]},
            "build_systems": {"go_modules": ["go.mod"]},
        },
        "java": {
            "files": ["pom.xml", "build.gradle", "gradle.properties"],
            "frameworks": {
                "spring": ["pom.xml", "build.gradle"],
                "maven": ["pom.xml"],
            },
            "build_systems": {
                "maven": ["pom.xml"],
                "gradle": ["build.gradle"],
            },
        },
    }

    # 检测项目类型
    for proj_type, indicators in type_indicators.items():
        found_files = []
        for file_name in indicators["files"]:
            file_path = cwd_path / file_name
            if file_path.exists():
                found_files.append(file_name)
                project_info["config_files"][file_name] = "exists"

        if found_files:
            project_info["project_type"] = proj_type
            project_info["key_files"] = found_files

            # 检测框架
            for framework, framework_files in indicators["frameworks"].items():
                if any((cwd_path / f).exists() for f in framework_files):
                    project_info["framework"] = framework
                    break

            # 检测构建系统
            for build_sys, build_files in indicators["build_systems"].items():
                if any((cwd_path / f).exists() for f in build_files):
                    project_info["build_system"] = build_sys
                    break

            break

    # 检测包管理器
    if project_info["project_type"] == "python":
        if (cwd_path / "pyproject.toml").exists():
            project_info["package_manager"] = "poetry"
        elif (cwd_path / "Pipfile").exists():
            project_info["package_manager"] = "pipenv"
        elif (cwd_path / "requirements.txt").exists():
            project_info["package_manager"] = "pip"
    elif project_info["project_type"] == "node":
        if (cwd_path / "yarn.lock").exists():
            project_info["package_manager"] = "yarn"
        elif (cwd_path / "pnpm-lock.yaml").exists():
            project_info["package_manager"] = "pnpm"
        elif (cwd_path / "package-lock.json").exists():
            project_info["package_manager"] = "npm"

    return project_info


def collect_core_context(command: str, exit_code: int, stderr: str, cwd: str) -> Dict[str, Any]:
    """收集核心级别的上下文信息。"""
    return {
        "command": command,
        "exit_code": exit_code,
        "stderr": stderr,
        "cwd": cwd,
        "timestamp": run_safe_command("date"),
    }


def _collect_git_info() -> Dict[str, str]:
    """收集Git信息。"""
    git_info = {}
    git_status = run_safe_command("git status --porcelain 2>/dev/null")
    if git_status:
        git_info["git_status"] = git_status
        git_branch = run_safe_command("git branch --show-current 2>/dev/null")
        if git_branch:
            git_info["git_branch"] = git_branch
    return git_info


def collect_standard_context(config: Dict[str, Any]) -> Dict[str, Any]:
    """收集标准级别的上下文信息。"""
    context = {}

    # 命令历史（最近10条）
    history = run_safe_command("history | tail -10")
    if history:
        context["recent_history"] = history.split("\n")

    # 当前目录文件列表
    try:
        files = [f.name for f in Path.cwd().iterdir() if f.is_file()][:20]
        context["current_files"] = files
    except Exception:
        pass

    # Git 信息
    context.update(_collect_git_info())

    return context


def collect_detailed_context(config: Dict[str, Any]) -> Dict[str, Any]:
    """收集详细级别的上下文信息。"""
    context = {}

    # 系统信息
    uname = run_safe_command("uname -a")
    if uname:
        context["system_info"] = uname

    # 环境变量（过滤敏感信息）
    try:
        sensitive_keys = ["password", "secret", "key", "token"]
        env_vars = {
            key: value[:100]
            for key, value in os.environ.items()
            if not any(sensitive in key.lower() for sensitive in sensitive_keys)
        }
        context["environment"] = env_vars
    except Exception:
        pass

    # 完整的目录列表
    ls_output = run_safe_command("ls -la")
    if ls_output:
        context["directory_listing"] = ls_output

    return context


def collect_context(
    command: str,
    exit_code: int,
    stderr: str = "",
    config: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """根据配置收集上下文信息。"""
    if not config:
        from .config import get_config

        config = get_config()

    # 获取当前工作目录
    cwd = str(Path.cwd())

    # 检查是否在敏感目录
    sensitive_dirs = config.get("sensitive_dirs", [])
    if is_sensitive_path(cwd, sensitive_dirs):
        return {
            "error": "位于敏感目录，跳过上下文收集",
            "command": command,
            "exit_code": exit_code,
        }

    # 收集核心上下文
    context = collect_core_context(command, exit_code, stderr, cwd)

    # 根据配置级别收集额外信息
    context_level = config.get("context_level", "detailed")

    if context_level in ["standard", "detailed"]:
        context.update(collect_standard_context(config))

    if context_level == "detailed":
        context.update(collect_detailed_context(config))

    # 收集第一优先级的新上下文信息（所有级别都收集）
    try:
        # 网络连接诊断
        context["network_context"] = collect_network_context()
    except Exception:
        context["network_context"] = {"error": "network context collection failed"}

    try:
        # 权限检查
        context["permission_context"] = collect_permission_context(command, cwd)
    except Exception:
        context["permission_context"] = {"error": "permission context collection failed"}

    try:
        # 增强的项目类型检测
        context["project_context"] = detect_project_type_enhanced(cwd)
    except Exception:
        context["project_context"] = {"error": "project context collection failed"}

    # 过滤敏感数据
    for key, value in context.items():
        if isinstance(value, str):
            context[key] = filter_sensitive_data(value)
        elif isinstance(value, list):
            context[key] = [filter_sensitive_data(str(item)) for item in value]
        elif isinstance(value, dict):
            # 递归过滤字典中的敏感数据
            context[key] = filter_sensitive_dict(value)

    return context


def filter_sensitive_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """递归过滤字典中的敏感数据。"""
    filtered = {}
    for key, value in data.items():
        if isinstance(value, str):
            filtered[key] = filter_sensitive_data(value)
        elif isinstance(value, dict):
            filtered[key] = filter_sensitive_dict(value)
        elif isinstance(value, list):
            filtered[key] = [
                (filter_sensitive_data(str(item)) if isinstance(item, str) else item)
                for item in value
            ]
        else:
            filtered[key] = value
    return filtered


def collect_ask_context(config: Dict[str, Any]) -> Dict[str, Any]:
    """为ask功能收集上下文信息。"""
    if not config:
        from .config import get_config

        config = get_config()

    # 获取当前工作目录
    cwd = str(Path.cwd())

    # 检查是否在敏感目录
    sensitive_dirs = config.get("sensitive_dirs", [])
    if is_sensitive_path(cwd, sensitive_dirs):
        return {
            "error": "位于敏感目录，跳过上下文收集",
            "cwd": cwd,
        }

    # 获取ask上下文级别配置
    ask_config = config.get("ask", {})
    context_level = ask_config.get("context_level", "minimal")

    context = {}

    if context_level == "minimal":
        context = collect_minimal_ask_context(cwd)
    elif context_level == "standard":
        # 复用标准上下文收集逻辑，但不包含错误信息
        context = collect_core_context("", 0, "", cwd)
        context.update(collect_standard_context(config))
        # 移除错误相关字段
        context.pop("command", None)
        context.pop("exit_code", None)
        context.pop("stderr", None)
    elif context_level == "detailed":
        # 复用详细上下文收集逻辑，但不包含错误信息
        context = collect_core_context("", 0, "", cwd)
        context.update(collect_standard_context(config))
        context.update(collect_detailed_context(config))
        # 移除错误相关字段
        context.pop("command", None)
        context.pop("exit_code", None)
        context.pop("stderr", None)

        # 添加增强上下文信息
        try:
            context["network_context"] = collect_network_context()
        except Exception:
            context["network_context"] = {"error": "network context collection failed"}

        try:
            context["permission_context"] = collect_permission_context("", cwd)
        except Exception:
            context["permission_context"] = {"error": "permission context collection failed"}

        try:
            context["project_context"] = detect_project_type_enhanced(cwd)
        except Exception:
            context["project_context"] = {"error": "project context collection failed"}

    # 过滤敏感数据
    for key, value in context.items():
        if isinstance(value, str):
            context[key] = filter_sensitive_data(value)
        elif isinstance(value, list):
            context[key] = [filter_sensitive_data(str(item)) for item in value]
        elif isinstance(value, dict):
            context[key] = filter_sensitive_dict(value)

    return context


def collect_minimal_ask_context(cwd: str) -> Dict[str, Any]:
    """收集ask功能的最小上下文信息（包含系统基础信息）。"""
    context = {
        "cwd": cwd,
        "user": getpass.getuser(),
        "timestamp": run_safe_command("date"),
    }

    # 添加系统基础信息
    try:
        context.update(collect_system_basic_info())
    except Exception:
        pass

    # 尝试获取Git信息（如果在仓库中）
    try:
        git_info = _collect_git_info()
        if git_info.get("git_branch"):
            context.update(git_info)
    except Exception:
        pass

    # 尝试检测项目类型
    try:
        project_context = detect_project_type_enhanced(cwd)
        if project_context.get("project_type") != "unknown":
            context["project_type"] = project_context.get("project_type")
            context["framework"] = project_context.get("framework")
    except Exception:
        pass

    return context


def collect_system_basic_info() -> Dict[str, Any]:
    """收集系统基础信息。"""
    info = {}

    # 系统发行版本和内核信息
    try:
        # uname -a 完整系统信息
        uname_info = run_safe_command("uname -a")
        if uname_info:
            info["system_info"] = uname_info

        # 系统发行版信息
        distro_cmd = (
            "lsb_release -d 2>/dev/null || cat /etc/os-release 2>/dev/null "
            "| grep PRETTY_NAME | cut -d'=' -f2 | tr -d '\"'"
        )
        distro_info = run_safe_command(distro_cmd)
        if distro_info:
            info["distro"] = distro_info.split("\n")[0]

        # 内核版本
        kernel_version = run_safe_command("uname -r")
        if kernel_version:
            info["kernel_version"] = kernel_version
    except Exception:
        pass

    # 硬件信息
    try:
        # CPU核心数
        cpu_cores = run_safe_command("nproc")
        if cpu_cores and cpu_cores.isdigit():
            info["cpu_cores"] = int(cpu_cores)

        # CPU型号信息
        cpu_model = run_safe_command(
            "grep 'model name' /proc/cpuinfo | head -1 | cut -d':' -f2 | xargs"
        )
        if cpu_model:
            info["cpu_model"] = cpu_model

        # 内存信息
        memory_info = run_safe_command(
            'free -h | grep \'^Mem:\' | awk \'{print $2" total, "$3" used, "$7" available"}\''
        )
        if memory_info:
            info["memory"] = memory_info
    except Exception:
        pass

    # 网络连通性检测
    try:
        # 检测网络连通性 ping 8.8.8.8
        ping_cmd = (
            "ping -c 1 -W 2 8.8.8.8 >/dev/null 2>&1 " "&& echo 'connected' || echo 'disconnected'"
        )
        ping_result = run_safe_command(ping_cmd, timeout=3)
        if ping_result:
            info["internet_connectivity"] = ping_result == "connected"
    except Exception:
        info["internet_connectivity"] = False

    # 运行的服务和端口信息
    try:
        # 获取监听端口信息
        listening_ports = run_safe_command(
            "ss -tuln | grep LISTEN | awk '{print $5}' | cut -d':' -f2 | sort -n | uniq | head -10"
        )
        if listening_ports:
            ports = [
                p.strip() for p in listening_ports.split("\n") if p.strip() and p.strip().isdigit()
            ]
            info["listening_ports"] = ports[:10]  # 限制显示前10个端口

        # 获取运行的关键服务
        services_cmd = (
            "systemctl list-units --type=service --state=running | grep '.service' "
            "| awk '{print $1}' | sed 's/.service$//' | head -10"
        )
        services = run_safe_command(services_cmd)
        if services:
            service_list = [s.strip() for s in services.split("\n") if s.strip()]
            info["running_services"] = service_list[:10]  # 限制显示前10个服务
    except Exception:
        pass

    # 磁盘使用信息
    try:
        disk_usage = run_safe_command(
            'df -h / | tail -1 | awk \'{print $2" total, "$3" used ("$5")"}\''
        )
        if disk_usage:
            info["disk_usage"] = disk_usage
    except Exception:
        pass

    # 系统负载
    try:
        load_avg = run_safe_command("uptime | awk -F'load average:' '{print $2}' | xargs")
        if load_avg:
            info["load_average"] = load_avg
    except Exception:
        pass

    return info
