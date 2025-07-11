"""上下文收集模块。"""

import os
import subprocess
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
        filtered_text = re.sub(
            pattern, lambda m: m.group().split()[0] + " ***", filtered_text
        )

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


def collect_core_context(
    command: str, exit_code: int, stderr: str, cwd: str
) -> Dict[str, Any]:
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
            if not any(
                sensitive in key.lower() for sensitive in sensitive_keys
            )
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
    context_level = config.get("context_level", "standard")

    if context_level in ["standard", "detailed"]:
        context.update(collect_standard_context(config))

    if context_level == "detailed":
        context.update(collect_detailed_context(config))

    # 过滤敏感数据
    for key, value in context.items():
        if isinstance(value, str):
            context[key] = filter_sensitive_data(value)
        elif isinstance(value, list):
            context[key] = [filter_sensitive_data(str(item)) for item in value]

    return context
