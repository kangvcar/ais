"""交互式菜单模块。"""

import subprocess
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.panel import Panel
from ..ui.panels import panels


def _get_risk_display(risk_level: str) -> Tuple[str, str, str]:
    """获取风险等级的显示信息。

    返回: (图标, 颜色, 描述)
    """
    risk_configs = {
        "safe": ("🟢", "green", "安全"),
        "moderate": ("🟡", "yellow", "谨慎"),
        "dangerous": ("🔴", "red", "危险"),
    }
    return risk_configs.get(risk_level, ("⚪", "white", "未知"))


def _safe_escape_for_questionary(text: str) -> str:
    """安全转义文本，避免questionary内部模板替换错误。"""
    if not isinstance(text, str):
        text = str(text) if text is not None else ""

    # 转义可能触发模板替换的特殊字符
    # questionary内部可能使用{}进行模板替换
    text = text.replace("{", "{{").replace("}", "}}")

    # 转义其他可能的模板字符
    text = text.replace("$", "$$")

    return text


def _safe_escape_for_rich(text: str) -> str:
    """安全转义文本，避免Rich库内部模板替换错误。"""
    if not isinstance(text, str):
        text = str(text) if text is not None else ""

    # Rich库的标记语法转义
    text = text.replace("[", "\\[").replace("]", "\\]")

    # 确保没有None或空字符串
    if not text or text.isspace():
        return "N/A"

    return text


def _format_command_choice(
    index: int,
    command: str,
    description: str,
    risk_level: str,
    terminal_width: int = 80,
) -> str:
    """格式化菜单选项文本，支持动态宽度调整。"""
    # 确保所有输入都是有效的字符串
    command = str(command) if command is not None else "N/A"
    description = str(description) if description is not None else "无描述"
    risk_level = str(risk_level) if risk_level is not None else "safe"

    icon, color, risk_text = _get_risk_display(risk_level)

    # 计算可用宽度，确保数值有效
    prefix = f"{index}. "
    suffix = f" {icon} ({risk_text})"
    available_width = max(
        20, terminal_width - len(prefix) - len(suffix) - 10
    )  # 确保最小宽度

    # 智能截断命令和描述
    if len(command) + len(description) + 3 <= available_width:  # 3 for " - "
        middle = f"{command} - {description}"
    elif len(command) <= available_width // 2:
        desc_width = available_width - len(command) - 3
        middle = (
            f"{command} - {description[:desc_width - 3]}..."
            if len(description) > desc_width
            else f"{command} - {description}"
        )
    else:
        cmd_width = available_width - 10  # 预留给描述的最小空间
        middle = (
            f"{command[:cmd_width - 3]}..."
            if len(command) > cmd_width
            else command
        )

    # 安全的格式化，避免substitute错误
    try:
        formatted_middle = f"{middle:<{available_width}}"
        final_text = f"{prefix}{formatted_middle}{suffix}"
        # 安全转义最终文本
        return _safe_escape_for_questionary(final_text)
    except (ValueError, TypeError, AttributeError):
        # 如果格式化失败，使用简单的字符串连接
        simple_text = f"{prefix}{middle}{suffix}"
        return _safe_escape_for_questionary(simple_text)


def _calculate_suggestion_score(
    suggestion: Dict[str, Any], user_context: Dict = None
) -> float:
    """计算建议的智能评分，用于排序和默认选择。"""
    score = 0.0
    command = suggestion.get("command", "")
    risk_level = suggestion.get("risk_level", "safe")

    # 1. 基础风险等级评分（安全命令优先）
    risk_scores = {"safe": 1.0, "moderate": 0.7, "dangerous": 0.3}
    score += risk_scores.get(risk_level, 0.5)

    # 2. 命令复杂度评分（简单命令优先）
    command_parts = command.split()
    if len(command_parts) <= 2:  # 非常简单的命令
        score += 0.4
    elif len(command_parts) <= 4:  # 中等复杂度
        score += 0.2

    # 3. 常见命令优先级（动态权重）
    basic_commands = ["ls", "cd", "pwd", "whoami", "echo"]
    file_commands = ["mkdir", "cp", "mv", "rm", "chmod", "chown", "find"]
    system_commands = ["ps", "top", "grep", "systemctl", "sudo"]

    if any(cmd in command.lower() for cmd in basic_commands):
        score += 0.3  # 基础命令获得更高权重
    elif any(cmd in command.lower() for cmd in file_commands):
        score += 0.2  # 文件操作命令
    elif any(cmd in command.lower() for cmd in system_commands):
        score += 0.1  # 系统命令权重较低

    # 4. 个性化评分（基于用户上下文）
    if user_context:
        score += _calculate_personalized_score(suggestion, user_context)

    # 5. 上下文相关性评分
    score += _calculate_context_relevance(suggestion, user_context or {})

    # 6. 智能风险调整
    score += _calculate_intelligent_risk_adjustment(
        suggestion, user_context or {}
    )

    return min(score, 3.0)  # 限制最大分数


def _should_skip_confirmation(
    command: str, risk_level: str, user_context: Dict = None
) -> bool:
    """智能判断是否可以跳过确认步骤。"""
    # 安全命令无需确认
    if risk_level == "safe":
        return True

    if not user_context:
        return False

    # 环境基础的确认策略
    environment = user_context.get("environment", "development")
    if environment == "production":
        # 生产环境不跳过任何非安全命令
        return False

    # 读取类命令（ls, cat, head等）可以跳过确认
    read_only_commands = [
        "ls",
        "cat",
        "head",
        "tail",
        "grep",
        "find",
        "which",
        "ps",
        "top",
    ]
    if any(cmd in command.lower() for cmd in read_only_commands):
        return True

    # 具有安全标志的命令（如 --dry-run）
    safe_flags = ["--dry-run", "--check", "--test", "--validate", "--preview"]
    if any(flag in command for flag in safe_flags):
        return True

    # 如果用户最近执行过相同的命令
    recent_commands = user_context.get("recent_commands", [])
    if command in recent_commands[-5:]:
        return True

    # 基于命令复杂度的智能判断
    command_parts = command.split()
    if len(command_parts) <= 2 and risk_level == "moderate":
        # 简单的中等风险命令可以跳过
        moderate_safe_patterns = [
            "chmod",
            "chown",
            "systemctl status",
            "service status",
        ]
        if any(pattern in command for pattern in moderate_safe_patterns):
            return True

    return False


def _calculate_personalized_score(
    suggestion: Dict[str, Any], user_context: Dict
) -> float:
    """基于用户历史行为计算个性化评分。"""
    score = 0.0
    command = suggestion.get("command", "")

    # 基于用户最近的命令模式
    recent_commands = user_context.get("recent_commands", [])
    if recent_commands:
        # 检查命令相似性
        command_words = set(command.lower().split())
        for recent_cmd in recent_commands[-10:]:  # 最近10个命令
            recent_words = set(recent_cmd.lower().split())
            overlap = len(command_words.intersection(recent_words))
            if overlap > 0:
                score += 0.1 * overlap / len(command_words)

    # 基于项目类型的偏好
    project_type = user_context.get("project_type")
    if project_type:
        type_preferences = {
            "python": ["pip", "python", "pytest", "virtualenv", "conda"],
            "node": ["npm", "yarn", "node", "npx"],
            "git": ["git", "github", "gitlab"],
            "docker": ["docker", "docker-compose", "container"],
            "system": ["systemctl", "service", "crontab"],
        }

        preferred_keywords = type_preferences.get(project_type, [])
        if any(keyword in command.lower() for keyword in preferred_keywords):
            score += 0.3

    # 基于命令复杂度的智能调整（替代技能级别）
    command_parts = command.split()

    # 优先简洁明了的命令
    if len(command_parts) <= 3:
        score += 0.15

    # 对包含常用模式的命令给予额外权重
    common_patterns = ["git", "ls", "cd", "mkdir", "touch", "cp", "mv"]
    if any(pattern in command.lower() for pattern in common_patterns):
        score += 0.1

    return score


def _calculate_context_relevance(
    suggestion: Dict[str, Any], user_context: Dict
) -> float:
    """计算建议与当前上下文的相关性。"""
    score = 0.0
    command = suggestion.get("command", "")

    # 当前目录上下文
    cwd = user_context.get("cwd", "")
    if cwd:
        # 如果在特定目录，某些命令更相关
        if "/home" in cwd and any(
            cmd in command for cmd in ["ls", "cd", "mkdir"]
        ):
            score += 0.2
        elif "/.git" in cwd or "/git" in cwd.lower():
            if "git" in command.lower():
                score += 0.3
        elif "/docker" in cwd.lower() or "dockerfile" in cwd.lower():
            if "docker" in command.lower():
                score += 0.3

    # Git 仓库上下文
    git_info = user_context.get("git_info", {})
    if git_info.get("in_repo"):
        if "git" in command.lower():
            score += 0.2
        if git_info.get("has_changes") and "commit" in command.lower():
            score += 0.3

    # 系统状态上下文
    system_status = user_context.get("system_status", {})
    if system_status:
        cpu_percent = system_status.get("cpu_percent", 0)
        memory_percent = system_status.get("memory", {}).get("percent", 0)

        # 高资源使用时，推荐监控命令
        if cpu_percent > 80 or memory_percent > 80:
            if any(cmd in command for cmd in ["ps", "top", "htop", "kill"]):
                score += 0.3

    # 时间上下文（工作时间 vs 休息时间）
    from datetime import datetime

    current_hour = datetime.now().hour
    if 9 <= current_hour <= 18:  # 工作时间
        # 工作时间更偏向开发相关命令
        if any(
            keyword in command
            for keyword in ["git", "build", "test", "deploy"]
        ):
            score += 0.1

    return score


def _collect_user_context() -> Dict[str, Any]:
    """收集用户上下文信息用于个性化推荐。"""
    context = {}

    try:
        # 基本信息
        context["cwd"] = os.getcwd()
        context["user"] = (
            os.getenv("USER") or os.getenv("USERNAME") or "unknown"
        )

        # 检查项目类型
        cwd_path = Path(context["cwd"])
        if (cwd_path / "package.json").exists():
            context["project_type"] = "node"
        elif (cwd_path / "requirements.txt").exists() or (
            cwd_path / "pyproject.toml"
        ).exists():
            context["project_type"] = "python"
        elif (cwd_path / "Dockerfile").exists() or (
            cwd_path / "docker-compose.yml"
        ).exists():
            context["project_type"] = "docker"
        elif (cwd_path / ".git").exists():
            context["project_type"] = "git"

        # Git 仓库信息
        if (cwd_path / ".git").exists():
            try:
                import subprocess

                # 检查 git 状态
                result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                has_changes = bool(result.stdout.strip())

                # 获取当前分支
                branch_result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                current_branch = branch_result.stdout.strip() or "main"

                context["git_info"] = {
                    "in_repo": True,
                    "has_changes": has_changes,
                    "current_branch": current_branch,
                }
            except Exception:
                context["git_info"] = {"in_repo": True}

        # 移除技能级别评估，改为基于具体上下文的智能判断

        # 检查是否为生产环境
        prod_indicators = ["PRODUCTION", "PROD", "LIVE"]
        is_production = any(os.getenv(var) for var in prod_indicators)
        if is_production:
            context["environment"] = "production"
        elif (
            "test" in context["cwd"].lower()
            or "staging" in context["cwd"].lower()
        ):
            context["environment"] = "staging"
        else:
            context["environment"] = "development"

        # 最近的命令历史（如果可能）
        try:
            from ..core.database import get_recent_logs

            recent_logs = get_recent_logs(10)
            context["recent_commands"] = [
                log.original_command for log in recent_logs
            ]
        except Exception:
            context["recent_commands"] = []

    except Exception as e:
        # 如果收集上下文失败，返回空字典
        context = {"error": str(e)}

    return context


def _calculate_intelligent_risk_adjustment(
    suggestion: Dict[str, Any], user_context: Dict
) -> float:
    """智能风险评估和调整。"""
    score = 0.0
    command = suggestion.get("command", "")
    risk_level = suggestion.get("risk_level", "safe")

    # 基于风险级别的智能调整（移除技能级别依赖）
    if risk_level == "dangerous":
        # 危险命令降低权重，但不完全排除
        score -= 0.3
    elif risk_level == "safe":
        # 安全命令获得额外权重
        score += 0.2

    # 环境安全性检查
    is_production = user_context.get("environment") == "production"
    if is_production and risk_level == "dangerous":
        score -= 0.8  # 生产环境大幅降低危险命令评分

    # 检查命令的具体风险模式
    dangerous_patterns = [
        (r"rm\s+-rf\s+/", -1.0),  # 删除根目录
        (r"dd\s+.*of=/dev/", -0.8),  # 直接写入设备
        (r"chmod\s+777", -0.3),  # 过度权限
        (r"sudo\s+rm", -0.4),  # sudo删除
    ]

    import re

    for pattern, penalty in dangerous_patterns:
        if re.search(pattern, command):
            score += penalty

    # 积极的安全模式检查
    safe_patterns = [
        (r"--dry-run", 0.3),  # 干运行
        (r"--backup", 0.2),  # 备份选项
        (r"--interactive", 0.2),  # 交互式确认
    ]

    for pattern, bonus in safe_patterns:
        if re.search(pattern, command):
            score += bonus

    return score


def _get_enhanced_choices(
    suggestions: List[Dict[str, Any]],
    terminal_width: int,
    user_context: Dict = None,
) -> List[Dict]:
    """生成增强的选择列表，包含快捷键和智能排序。"""
    # 动态上下文排序：基于多维度评分
    scored_suggestions = []

    for i, sug in enumerate(suggestions):
        base_score = _calculate_suggestion_score(sug, user_context)

        # 时间特征加权（早上 vs 晚上）
        time_boost = _calculate_time_based_boost(sug, user_context or {})

        # 环境适应性加权
        env_boost = _calculate_environment_boost(sug, user_context or {})

        # 相似命令历史加权
        history_boost = _calculate_history_similarity_boost(
            sug, user_context or {}
        )

        # 综合评分
        final_score = base_score + time_boost + env_boost + history_boost

        scored_suggestions.append(
            (
                i,
                sug,
                final_score,
                {
                    "base": base_score,
                    "time": time_boost,
                    "env": env_boost,
                    "history": history_boost,
                },
            )
        )

    # 智能排序：先按安全性，再按评分
    scored_suggestions.sort(
        key=lambda x: (
            _get_safety_priority(x[1].get("risk_level", "safe")),
            x[2],  # 综合评分
        ),
        reverse=True,
    )

    choices = []

    # 生成增强的菜单选项
    for display_idx, (
        orig_idx,
        suggestion,
        final_score,
        score_breakdown,
    ) in enumerate(scored_suggestions, 1):
        command = suggestion.get("command", "N/A")
        description = suggestion.get("description", "无描述")
        risk_level = suggestion.get("risk_level", "safe")

        icon, color, risk_text = _get_risk_display(risk_level)

        # 智能标记系统
        markers = []
        if display_idx == 1:
            markers.append("⭐")  # 最佳推荐
        if score_breakdown["history"] > 0.1:
            markers.append("🔄")  # 历史相关
        if score_breakdown["env"] > 0.1:
            markers.append("🏠")  # 环境适配
        if risk_level == "safe" and final_score > 1.5:
            markers.append("✨")  # 高分安全

        marker_prefix = "".join(markers) + " " if markers else "   "

        choice_text = _format_command_choice(
            display_idx, command, description, risk_level, terminal_width
        )

        # 安全地添加标记
        if markers:
            # 确保marker_prefix安全
            safe_marker_prefix = _safe_escape_for_questionary(marker_prefix)
            choice_text = f"{safe_marker_prefix}{choice_text}"

        choices.append(
            {
                "name": choice_text,
                "value": f"execute_{orig_idx}",
                "shortcut": str(display_idx),
                "score": final_score,  # 保存评分用于调试
            }
        )

    return choices


def _calculate_time_based_boost(
    suggestion: Dict[str, Any], user_context: Dict
) -> float:
    """基于时间的动态加权。"""
    from datetime import datetime

    current_hour = datetime.now().hour
    command = suggestion.get("command", "")
    boost = 0.0

    # 早上时段（9-12）：偏向工作相关命令
    if 9 <= current_hour <= 12:
        work_keywords = ["git", "build", "test", "npm", "python", "docker"]
        if any(keyword in command.lower() for keyword in work_keywords):
            boost += 0.2

    # 下午时段（13-18）：偏向部署和配置
    elif 13 <= current_hour <= 18:
        deploy_keywords = ["deploy", "config", "service", "systemctl"]
        if any(keyword in command.lower() for keyword in deploy_keywords):
            boost += 0.15

    # 晚上时段（19-23）：偏向简单和安全命令
    elif 19 <= current_hour <= 23:
        if suggestion.get("risk_level") == "safe":
            boost += 0.1
        simple_keywords = ["ls", "cd", "cat", "grep", "find"]
        if any(keyword in command.lower() for keyword in simple_keywords):
            boost += 0.15

    return boost


def _calculate_environment_boost(
    suggestion: Dict[str, Any], user_context: Dict
) -> float:
    """基于环境的动态加权。"""
    boost = 0.0
    command = suggestion.get("command", "")
    environment = user_context.get("environment", "development")

    # 生产环境：大幅增强安全命令
    if environment == "production":
        if suggestion.get("risk_level") == "safe":
            boost += 0.3
        if any(
            safe_pattern in command
            for safe_pattern in ["--dry-run", "--check", "status"]
        ):
            boost += 0.2

    # 开发环境：增强开发工具命令
    elif environment == "development":
        dev_keywords = ["debug", "test", "build", "install", "npm", "pip"]
        if any(keyword in command.lower() for keyword in dev_keywords):
            boost += 0.15

    return boost


def _calculate_history_similarity_boost(
    suggestion: Dict[str, Any], user_context: Dict
) -> float:
    """基于历史命令相似性的加权。"""
    boost = 0.0
    command = suggestion.get("command", "")
    recent_commands = user_context.get("recent_commands", [])

    if not recent_commands:
        return boost

    command_tokens = set(command.lower().split())

    # 计算与最近命令的相似度
    for recent_cmd in recent_commands[-5:]:  # 只看最近5个
        recent_tokens = set(recent_cmd.lower().split())

        # Jaccard 相似度
        intersection = command_tokens.intersection(recent_tokens)
        union = command_tokens.union(recent_tokens)

        if union:
            similarity = len(intersection) / len(union)
            boost += similarity * 0.2  # 最多 0.2 加权

    # 如果命令完全匹配最近使用的命令
    if command in recent_commands[-3:]:
        boost += 0.3

    return min(boost, 0.5)  # 限制最大加权


def _get_safety_priority(risk_level: str) -> int:
    """获取安全级别的排序优先级。"""
    priority_map = {"safe": 3, "moderate": 2, "dangerous": 1}
    return priority_map.get(risk_level, 2)


def _enhanced_risk_assessment(
    suggestion: Dict[str, Any], user_context: Dict = None
) -> Dict[str, Any]:
    """增强型智能风险评估系统。"""
    command = suggestion.get("command", "")
    original_risk = suggestion.get("risk_level", "safe")

    # 初始化风险评估结果
    risk_assessment = {
        "level": original_risk,
        "confidence": 0.7,  # 初始置信度
        "factors": [],
        "recommendations": [],
        "auto_safe": False,
    }

    if not user_context:
        return risk_assessment

    import re

    # 1. 上下文相关风险评估
    cwd = user_context.get("cwd", "")

    # 在特定目录下的风险调整
    if "/tmp" in cwd or "/var/tmp" in cwd:
        risk_assessment["factors"].append("在临时目录中，风险降低")
        if original_risk == "dangerous":
            risk_assessment["level"] = "moderate"

    if "/home" in cwd and "rm" in command:
        risk_assessment["factors"].append("在用户目录中删除文件，风险增加")
        if original_risk == "moderate":
            risk_assessment["level"] = "dangerous"

    # 2. 基于命令特征的智能风险调整（移除技能级别依赖）
    # 检查复杂命令模式
    if len(command.split()) > 5 or any(
        char in command for char in ["|", ">", ";"]
    ):
        if original_risk == "safe":
            risk_assessment["level"] = "moderate"
            risk_assessment["factors"].append("复杂命令模式，提升风险等级")
        elif original_risk == "moderate":
            risk_assessment["level"] = "dangerous"
            risk_assessment["factors"].append("复杂危险命令，需要谨慎操作")

    # 检查安全措施
    safe_indicators = [
        "--backup",
        "--dry-run",
        "--interactive",
        "-i",
        "--help",
    ]
    if any(indicator in command for indicator in safe_indicators):
        if original_risk == "dangerous":
            risk_assessment["level"] = "moderate"
            risk_assessment["factors"].append("包含安全措施，降低风险等级")
        elif original_risk == "moderate":
            risk_assessment["level"] = "safe"
            risk_assessment["factors"].append("安全选项，降低操作风险")

    # 3. 环境基础的风险调整
    environment = user_context.get("environment", "development")

    if environment == "production":
        # 生产环境：提高所有风险级别
        if original_risk == "safe" and any(
            cmd in command for cmd in ["restart", "stop", "kill"]
        ):
            risk_assessment["level"] = "moderate"
            risk_assessment["factors"].append("生产环境服务操作")
        elif original_risk == "moderate":
            risk_assessment["level"] = "dangerous"
            risk_assessment["factors"].append("生产环境中的风险操作")

    # 4. 智能模式识别
    dangerous_patterns = [
        (r"rm\s+-rf\s+/(?!tmp|var/tmp)", "删除根目录或重要系统目录"),
        (r"dd\s+.*of=/dev/[sh]d", "直接写入磁盘设备"),
        (r"chmod\s+777\s+/", "设置根目录为全权限"),
        (r"mkfs\.|format\s+", "格式化磁盘操作"),
    ]

    for pattern, description in dangerous_patterns:
        if re.search(pattern, command):
            risk_assessment["level"] = "dangerous"
            risk_assessment["confidence"] = 0.95
            risk_assessment["factors"].append(
                f"检测到高风险模式: {description}"
            )

    # 5. 自动安全模式检测
    auto_safe_patterns = [
        "--help",
        "-h",
        "--version",
        "-V",
        "status",
        "info",
        "list",
        "show",
    ]

    if any(pattern in command.lower() for pattern in auto_safe_patterns):
        risk_assessment["auto_safe"] = True
        risk_assessment["factors"].append("检测到安全查询操作")

    # 6. 生成智能建议
    if risk_assessment["level"] == "dangerous":
        risk_assessment["recommendations"].extend(
            [
                "在执行前备份重要数据",
                "考虑在测试环境中先试运行",
                "仔细检查命令参数和路径",
            ]
        )
    elif risk_assessment["level"] == "moderate":
        risk_assessment["recommendations"].extend(
            ["确认命令参数正确", "考虑使用 --dry-run 预览结果"]
        )

    return risk_assessment


def _get_risk_warning(risk_level: str) -> str:
    """获取风险等级的警告内容。"""
    warnings = {
        "moderate": (
            "🔸 这个操作需要谨慎执行\n"
            "🔸 建议在执行前了解命令的具体作用\n"
            "🔸 如有疑问，请先在测试环境中尝试"
        ),
        "dangerous": (
            "🔺 这是一个高风险操作！\n"
            "🔺 可能会删除文件或修改系统配置\n"
            "🔺 强烈建议备份重要数据后再执行\n"
            "🔺 如果不确定，请寻求专业帮助"
        ),
    }
    return warnings.get(risk_level, "")


def _create_suggestions_table(suggestions: List[Dict[str, Any]]) -> Table:
    """创建建议命令的表格显示。"""
    table = Table(show_header=True, header_style="bold blue", box=None)
    table.add_column("#", style="cyan", width=3)
    table.add_column("命令", style="bold", min_width=20)
    table.add_column("风险", justify="center", width=6)
    table.add_column("说明", style="dim")

    for i, suggestion in enumerate(suggestions, 1):
        command = suggestion.get("command", "N/A")
        description = suggestion.get("description", "无描述")
        risk_level = suggestion.get("risk_level", "safe")

        icon, color, risk_text = _get_risk_display(risk_level)

        # 智能截断长命令
        if len(command) > 30:
            command_display = command[:27] + "..."
        else:
            command_display = command

        table.add_row(
            str(i),
            f"[white]{command_display}[/white]",
            f"[{color}]{icon}[/{color}]",
            description[:50] + "..." if len(description) > 50 else description,
        )

    return table


def execute_command(command: str) -> bool:
    """执行命令并显示结果。"""
    from rich.console import Console
    from rich.panel import Panel

    console = Console()

    try:
        # 显示命令执行面板
        exec_panel = Panel(
            f"[bold cyan]🚀 正在执行: [/bold cyan]"
            f"[bold white]{command}[/bold white]",
            title="[bold blue]⚡ 命令执行[/bold blue]",
            title_align="left",
            border_style="blue",
            padding=(0, 1),
            expand=False,
        )
        console.print(exec_panel)

        # 分隔线
        console.print("─" * 50)

        result = subprocess.run(
            command,
            shell=True,
            capture_output=False,
            text=True,  # 让输出直接显示给用户
        )

        console.print("─" * 50)

        # 显示执行结果面板
        if result.returncode == 0:
            result_panel = Panel(
                "[green]✅ 命令执行成功[/green]",
                title="[bold green]🎉 执行结果[/bold green]",
                title_align="left",
                border_style="green",
                padding=(0, 1),
                expand=False,
            )
        else:
            result_panel = Panel(
                f"[red]❌ 命令执行失败，退出码: {result.returncode}[/red]",
                title="[bold red]💥 执行失败[/bold red]",
                title_align="left",
                border_style="red",
                padding=(0, 1),
                expand=False,
            )
        console.print(result_panel)

        return result.returncode == 0

    except Exception as e:
        error_panel = Panel(
            f"[red]❌ 执行命令时出错: {e}[/red]",
            title="[bold red]🚨 系统错误[/bold red]",
            title_align="left",
            border_style="red",
            padding=(0, 1),
            expand=False,
        )
        console.print(error_panel)
        return False


def confirm_dangerous_command(command: str) -> bool:
    """对危险命令进行二次确认。"""
    print("\n⚠️  这是一个危险操作:")
    print(f"   {command}")
    print("\n⚠️  此命令可能会:")
    print("   • 删除重要文件")
    print("   • 修改系统配置")
    print("   • 造成数据丢失")

    while True:
        choice = input("\n❓ 你确定要执行吗？(yes/no): ").lower().strip()
        if choice in ["yes", "y"]:
            return True
        elif choice in ["no", "n"]:
            return False
        else:
            print("请输入 yes 或 no")


def show_command_details(
    suggestion: Dict[str, Any], console: Console, user_context: Dict = None
) -> None:
    """显示命令的详细信息，使用增强的视觉设计和智能风险评估。"""
    try:
        # 安全验证输入参数
        if not isinstance(suggestion, dict):
            panels.error("无效的建议数据")
            return

        if not console:
            print("❌ 控制台对象无效")
            return

        # 确保所有必需字段存在且有效
        command = suggestion.get("command")
        if not command or not isinstance(command, str):
            command = "N/A"

        description = suggestion.get("description")
        if not description or not isinstance(description, str):
            description = "无描述"

        explanation = suggestion.get("explanation")
        if explanation and not isinstance(explanation, str):
            explanation = str(explanation)

        # 使用增强型风险评估（安全包装）
        try:
            risk_assessment = _enhanced_risk_assessment(
                suggestion, user_context
            )
            risk_level = risk_assessment.get("level", "safe")
        except Exception:
            # 如果风险评估失败，使用默认值
            risk_level = suggestion.get("risk_level", "safe")
            risk_assessment = {
                "level": risk_level,
                "factors": [],
                "recommendations": [],
            }

        icon, color, risk_text = _get_risk_display(risk_level)

        # 创建美化的面板
        console.print()

        # 风险等级横幅
        try:
            risk_banner_style = f"bold {color} on {color}20"
            risk_content = f"{icon} {risk_text.upper()} 风险等级"
            # 安全转义横幅内容
            safe_risk_content = _safe_escape_for_rich(risk_content)
            panel_content = (
                f"[{risk_banner_style}] {safe_risk_content} "
                f"[/{risk_banner_style}]"
            )
            risk_panel = Panel(
                panel_content,
                box=None,
                style=color,
                padding=(0, 1),
                title_align="left",
            )
            console.print(risk_panel)
        except Exception:
            # 如果横幅显示失败，使用简单文本
            console.print(
                f"[{color}]{icon} {risk_text.upper()} 风险等级[/{color}]"
            )

        # 命令详情表格
        details_table = Table(show_header=False, box=None, padding=(0, 1))
        details_table.add_column("项目", style="bold cyan", width=12)
        details_table.add_column("内容", style="white")

        # 添加命令行（安全转义）
        safe_command = _safe_escape_for_rich(command)
        details_table.add_row(
            "📋 命令", f"[bold green]{safe_command}[/bold green]"
        )

        # 添加描述（安全转义）
        if description and description != "无描述":
            safe_description = _safe_escape_for_rich(description)
            details_table.add_row("💡 方案", safe_description)

        # 添加技术原理（安全转义）
        if explanation:
            # 如果解释太长，进行智能换行
            if len(explanation) > 60:
                explanation = (
                    explanation[:60] + "..." + "\n     " + explanation[60:]
                )
            safe_explanation = _safe_escape_for_rich(explanation)
            details_table.add_row("🔧 原理", safe_explanation)

        # 创建主面板
        try:
            safe_title = _safe_escape_for_rich("📖 命令详细说明")
            main_panel = Panel(
                details_table,
                title=f"[bold blue]{safe_title}[/bold blue]",
                title_align="left",
                border_style="blue",
                padding=(1, 2),
            )
            console.print(main_panel)
        except Exception:
            # 如果面板显示失败，使用简化的Panel显示
            panels.info(details_table, "📖 命令详细说明")

        # 增强型风险警告（仅对危险和中等风险命令）
        if risk_level in ["dangerous", "moderate"]:
            warning_parts = []

            # 基础警告
            base_warning = _get_risk_warning(risk_level)
            if base_warning:
                warning_parts.append(base_warning)

            # 增强评估结果
            if risk_assessment.get("factors"):
                warning_parts.append("\n🧠 智能分析:")
                for factor in risk_assessment["factors"]:
                    warning_parts.append(f"  • {factor}")

            if risk_assessment.get("recommendations"):
                warning_parts.append("\n📝 建议措施:")
                for rec in risk_assessment["recommendations"]:
                    warning_parts.append(f"  ✓ {rec}")

            # 置信度显示
            confidence = risk_assessment.get("confidence", 0.7)
            confidence_text = f"\n🎯 评估置信度: {confidence:.0%}"
            warning_parts.append(confidence_text)

            if warning_parts:
                try:
                    warning_content = "\n".join(warning_parts)
                    safe_warning_content = _safe_escape_for_rich(
                        warning_content
                    )
                    safe_warning_title = _safe_escape_for_rich(
                        "⚠️  智能安全提醒"
                    )
                    warning_panel = Panel(
                        safe_warning_content,
                        title=(
                            f"[bold {color}]{safe_warning_title}"
                            f"[/bold {color}]"
                        ),
                        title_align="left",
                        border_style=color,
                        style=f"{color}20",
                    )
                    console.print(warning_panel)
                except Exception:
                    # 如果警告面板显示失败，使用简单文本
                    console.print(f"[{color}]⚠️  智能安全提醒[/{color}]")
                    for part in warning_parts:
                        console.print(f"[dim]{part}[/dim]")

    except Exception as e:
        # 如果显示详情失败，显示简化版本
        panels.error(f"显示命令详情时出错: {e}")

        # 安全地获取和显示基本信息
        try:
            command_text = (
                suggestion.get("command", "N/A")
                if isinstance(suggestion, dict)
                else "N/A"
            )
            description_text = (
                suggestion.get("description", "无描述")
                if isinstance(suggestion, dict)
                else "无描述"
            )

            # 安全转义后显示
            safe_command_text = _safe_escape_for_rich(str(command_text))
            safe_description_text = _safe_escape_for_rich(
                str(description_text)
            )

            panels.warning(
                f"命令: {safe_command_text}\n描述: {safe_description_text}"
            )
        except Exception as fallback_error:
            panels.error(
                f"严重错误，无法显示命令信息: {fallback_error}\n原始错误: {e}"
            )


def ask_follow_up_question(
    console: Console, predefined_questions: List[str] = None
) -> None:
    """询问后续问题，支持预设问题选择。"""
    # 如果有预设问题，先显示选项
    if predefined_questions:
        questions_list = []
        for i, q in enumerate(predefined_questions, 1):
            questions_list.append(f"  {i}. {q}")
        questions_list.append(f"  {len(predefined_questions) + 1}. 自定义问题")

        content = "\n".join(questions_list)
        panels.info(content, "💬 AI 建议的学习问题")

        try:
            choice = input(
                f"\n请选择问题 (1-{len(predefined_questions) + 1}, 或回车跳过): "
            ).strip()
            if not choice:
                return

            choice_num = int(choice)
            if 1 <= choice_num <= len(predefined_questions):
                question = predefined_questions[choice_num - 1]
            elif choice_num == len(predefined_questions) + 1:
                question = input("请输入你的问题: ").strip()
                if not question:
                    return
            else:
                panels.warning("无效选择")
                return
        except ValueError:
            panels.warning("无效输入")
            return
    else:
        question = input("请输入你的问题（按回车跳过）: ").strip()
        if not question:
            return

    try:
        from ..core.ai import ask_ai
        from ..core.config import get_config

        config = get_config()
        response = ask_ai(
            f"关于刚才的错误分析，用户有一个后续问题：{question}", config
        )

        if response:
            panels.ai_analysis(Markdown(response), "🤖 AI 回答")
        else:
            panels.error("无法获取 AI 回答")

    except Exception as e:
        panels.error(f"处理问题时出错: {e}")


def edit_command(command: str) -> str:
    """让用户编辑命令。"""
    panels.info(f"✏️  当前命令: {command}", "🔧 命令编辑")
    new_command = input("请输入修改后的命令: ").strip()
    return new_command if new_command else command


def show_interactive_menu(
    suggestions: List[Dict[str, Any]],
    console: Console,
    follow_up_questions: List[str] = None,
) -> None:
    """显示交互式建议菜单。"""
    # 检查是否在交互式终端中
    if not sys.stdin.isatty():
        show_simple_menu(suggestions, console, follow_up_questions)
        return

    try:
        import questionary
    except ImportError:
        # 如果 questionary 不可用，使用简化版本
        show_simple_menu(suggestions, console, follow_up_questions)
        return

    # 收集用户上下文信息用于个性化推荐
    user_context = _collect_user_context()

    # 移除项目类型显示，简化界面

    while True:
        # 显示建议命令表格（在菜单上方）
        if suggestions:
            from rich.panel import Panel

            suggestions_table = _create_suggestions_table(suggestions)
            suggestions_panel = Panel(
                suggestions_table,
                title="[bold green]💡 AI 基于你的使用习惯和当前环境推荐[/bold green]",
                title_align="left",
                border_style="green",
                padding=(1, 1),
                expand=False,
            )
            console.print(suggestions_panel)

        # 构建增强的菜单选项
        terminal_width = console.size.width if hasattr(console, "size") else 80

        # 使用智能排序和快捷键的选择列表（传入用户上下文）
        choices = _get_enhanced_choices(
            suggestions, terminal_width, user_context
        )

        # 移除智能排序提示，简化界面

        # 移除分割线，界面更简洁

        # 不需要添加固定选项，直接通过输入处理

        # 移除操作指南，简化界面

        # 显示菜单（增加错误处理）
        try:
            # 使用简单的文本输入实现快捷键
            user_input = questionary.text(
                "Select an action (1-9/e/q/x):",
                instruction="(数字选择建议，e=编辑，q=提问，x=退出)",
            ).ask()

            if not user_input:
                action = "exit"
            else:
                user_input = user_input.strip().lower()

                # 处理快捷键
                if user_input == "e":
                    action = "edit"
                elif user_input == "q":
                    action = "question"
                elif user_input == "x" or user_input == "exit":
                    action = "exit"
                elif user_input.isdigit():
                    # 数字选择
                    choice_num = int(user_input)
                    if 1 <= choice_num <= len(suggestions):
                        action = f"execute_{choice_num - 1}"
                    else:
                        console.print(
                            f"[red]错误: 选项 {choice_num} 不存在，"
                            f"请输入1-{len(suggestions)}[/red]"
                        )
                        continue
                else:
                    console.print(
                        f"[red]错误: 无效输入 '{user_input}'，"
                        f"请输入1-{len(suggestions)}/e/q/x[/red]"
                    )
                    continue
        except Exception as e:
            panels.error(f"菜单显示错误: {e}\n回退到简单模式")
            show_simple_menu(suggestions, console, follow_up_questions)
            return

        if not action or action == "exit":
            print("👋 再见！")
            break
        elif action.startswith("execute_"):
            # 执行命令（增强错误处理）
            try:
                index = int(action.split("_")[1])
                if 0 <= index < len(suggestions):
                    suggestion = suggestions[index]

                    # 安全验证suggestion数据
                    if not isinstance(suggestion, dict):
                        panels.error("无效的建议数据格式")
                        continue

                    command = suggestion.get("command", "")
                    risk_level = suggestion.get("risk_level", "safe")

                    # 验证command不为空
                    if not command or not isinstance(command, str):
                        panels.error("无效的命令数据")
                        continue

                    # 跳过显示命令详情，直接执行命令
                    # 用户反馈：详情信息在菜单选项中已展示，此处重复显示没有必要
                    # show_command_details(suggestion, console, user_context)

                    # 移除风险确认流程
                    # 用户反馈：风险等级已在菜单选项中显示，无需额外确认

                    # 执行命令
                    success = execute_command(command)

                    # 智能后续操作
                    if success:
                        # 对于安全命令，自动继续；对于危险命令，询问
                        if risk_level == "safe":
                            continue
                    else:
                        panels.warning("🤔 命令执行失败，建议尝试其他方案")

                    # 询问是否继续（仅对非安全命令或失败情况）
                    if not questionary.confirm(
                        "继续查看其他建议？", default=True
                    ).ask():
                        break

                else:
                    panels.error("无效的选择索引")
                    continue
            except (ValueError, IndexError, KeyError) as e:
                panels.error(f"处理选择时出错: {e}")
                continue
            except Exception as e:
                debug_info = (
                    f"action={action}, "
                    f"suggestions_count={len(suggestions)}"
                )
                panels.error(
                    f"执行操作时发生未知错误: {e}\n调试信息: {debug_info}"
                )
                continue

        elif action == "edit":
            # 编辑命令
            choices = [
                f"{i}. {sug.get('command', 'N/A')}"
                for i, sug in enumerate(suggestions, 1)
            ]
            choices.append("返回")

            edit_choice = questionary.select(
                "选择要编辑的命令:", choices=choices
            ).ask()

            if edit_choice and edit_choice != "返回":
                index = int(edit_choice.split(".")[0]) - 1
                original_command = suggestions[index].get("command", "")
                new_command = edit_command(original_command)

                if new_command != original_command:
                    console.print(
                        f"\n✅ 命令已修改为: [bold]{new_command}[/bold]"
                    )

                    if questionary.confirm("是否执行修改后的命令？").ask():
                        execute_command(new_command)

        elif action == "question":
            # 询问后续问题
            ask_follow_up_question(console, follow_up_questions)


def show_simple_menu(
    suggestions: List[Dict[str, Any]],
    console: Console,
    follow_up_questions: List[str] = None,
) -> None:
    """简化版菜单（当 questionary 不可用时）。"""
    console.print()
    console.print("? Select an action:")

    for i, suggestion in enumerate(suggestions, 1):
        command = suggestion.get("command", "N/A")
        description = suggestion.get("description", "无描述")
        risk_level = suggestion.get("risk_level", "safe")

        # 风险等级图标
        risk_icon = "✅" if risk_level == "safe" else "⚠️"
        prefix = "  ▸ " if i == 1 else "    "

        console.print(
            f"{prefix}{i}. {command:<25} {risk_icon} ({description})"
        )

        if suggestion.get("explanation"):
            console.print(
                f"       [dim]说明: {suggestion['explanation']}[/dim]"
            )

    # 添加固定选项

    next_num = len(suggestions) + 1
    fixed_options = [
        f"{next_num}. Edit a command...",
        f"{next_num + 1}. Ask follow-up question",
        f"{next_num + 2}. Exit",
    ]

    for option in fixed_options:
        console.print(f"    {option}")

    console.print(
        "\n[dim]提示: 你可以手动复制并执行上述命令，或者在交互式终端中获得更好的体验。[/dim]"
    )
