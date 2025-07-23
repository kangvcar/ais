"""AI interaction module for AIS."""

import json
import httpx
from typing import Dict, Any, Optional, List


def _build_context_summary(context: Dict[str, Any]) -> str:
    """构建简洁的上下文摘要"""
    summary_parts = []

    # 基本环境信息
    if context.get("cwd"):
        summary_parts.append(f"📁 当前目录: {context['cwd']}")

    if context.get("user"):
        summary_parts.append(f"👤 用户: {context['user']}")

    # Git仓库信息
    git_info = context.get("git_info", {})
    if git_info.get("in_repo"):
        git_status = f"🔄 Git仓库: {git_info.get('current_branch', 'unknown')}分支"
        if git_info.get("has_changes"):
            git_status += f" (有{git_info.get('changed_files', 0)}个文件变更)"
        summary_parts.append(git_status)

    # 项目类型分析
    dir_info = context.get("current_dir_files", {})
    if dir_info.get("project_type") and dir_info["project_type"] != "unknown":
        project_info = f"🚀 项目类型: {dir_info['project_type']}"
        if dir_info.get("key_files"):
            project_info += f" (关键文件: {', '.join(dir_info['key_files'][:3])})"
        summary_parts.append(project_info)

    # 系统状态
    system_status = context.get("system_status", {})
    if system_status:
        status_info = f"⚡ 系统状态: CPU {system_status.get('cpu_percent', 0):.1f}%"
        if "memory" in system_status:
            status_info += f", 内存 {system_status['memory'].get('percent', 0):.1f}%"
        summary_parts.append(status_info)

    # 最近的操作模式
    work_pattern = context.get("work_pattern", {})
    if work_pattern.get("activities"):
        activities = work_pattern["activities"][:3]  # 只显示前3个
        summary_parts.append(f"🎯 最近操作: {', '.join(activities)}")

    # 网络状态
    network_info = context.get("network_info", {})
    if network_info.get("internet_available") is False:
        summary_parts.append("🌐 网络: 离线状态")

    return "\n".join(summary_parts) if summary_parts else "📋 基本环境信息"


def _build_intelligent_context_analysis(context: Dict[str, Any]) -> str:
    """构建智能的上下文分析"""
    analysis_parts = []

    # 网络诊断分析
    network_context = context.get("network_context", {})
    if network_context and network_context != {"error": "network context collection failed"}:
        network_analysis = []
        if network_context.get("internet_connectivity") is False:
            network_analysis.append("✗  网络连接异常")
        elif network_context.get("dns_resolution") == "failed":
            network_analysis.append("✗  DNS解析失败")
        elif network_context.get("proxy_settings"):
            network_analysis.append(f"🔄 代理设置: {network_context['proxy_settings']}")
        else:
            network_analysis.append("✓  网络连接正常")

        if network_context.get("local_open_ports"):
            network_analysis.append(f"🔌 本地开放端口: {network_context['local_open_ports']}")

        if network_analysis:
            analysis_parts.append(f"🌐 **网络状态**: {' | '.join(network_analysis)}")

    # 权限分析
    permission_context = context.get("permission_context", {})
    if permission_context and permission_context != {
        "error": "permission context collection failed"
    }:
        permission_analysis = []

        current_user = permission_context.get("current_user", "unknown")
        permission_analysis.append(f"用户: {current_user}")

        if permission_context.get("sudo_available"):
            permission_analysis.append("sudo可用")
        else:
            permission_analysis.append("sudo不可用")

        # 目录权限
        cwd_perms = []
        if permission_context.get("cwd_readable"):
            cwd_perms.append("R")
        if permission_context.get("cwd_writable"):
            cwd_perms.append("W")
        if permission_context.get("cwd_executable"):
            cwd_perms.append("X")

        if cwd_perms:
            permission_analysis.append(f"当前目录权限: {''.join(cwd_perms)}")

        # 目标文件权限
        if permission_context.get("target_path"):
            target_path = permission_context["target_path"]
            if permission_context.get("target_permissions"):
                permission_analysis.append(
                    f"目标 {target_path} 权限: " f"{permission_context['target_permissions']}"
                )
            elif permission_context.get("parent_dir_writable") is not None:
                parent_writable = "可写" if permission_context["parent_dir_writable"] else "不可写"
                permission_analysis.append(f"父目录{parent_writable}")

        if permission_analysis:
            analysis_parts.append(f"🔐 **权限状态**: {' | '.join(permission_analysis)}")

    # 项目环境分析
    project_context = context.get("project_context", {})
    if project_context and project_context != {"error": "project context collection failed"}:
        project_analysis = []

        project_type = project_context.get("project_type", "unknown")
        if project_type != "unknown":
            project_analysis.append(f"类型: {project_type}")

            if project_context.get("framework"):
                project_analysis.append(f"框架: {project_context['framework']}")

            if project_context.get("package_manager"):
                project_analysis.append(f"包管理: {project_context['package_manager']}")

            if project_context.get("build_system"):
                project_analysis.append(f"构建系统: {project_context['build_system']}")

            # 配置文件状态
            config_files = project_context.get("config_files", {})
            if config_files:
                existing_configs = [k for k, v in config_files.items() if v == "exists"]
                if existing_configs:
                    project_analysis.append(f"配置文件: {', '.join(existing_configs[:3])}")

        if project_analysis:
            analysis_parts.append(f"🚀 **项目环境**: {' | '.join(project_analysis)}")

    # Git状态分析
    if context.get("git_branch"):
        git_analysis = [f"分支: {context['git_branch']}"]
        if context.get("git_status"):
            git_analysis.append("有未提交变更")
        analysis_parts.append(f"📋 **Git状态**: {' | '.join(git_analysis)}")

    # 命令历史模式分析
    recent_history = context.get("recent_history", [])
    if recent_history:
        # 分析最近命令的类型
        command_types = []
        for cmd in recent_history[-5:]:  # 分析最近5条命令
            if any(git_cmd in cmd for git_cmd in ["git", "GitHub", "gitlab"]):
                command_types.append("Git操作")
            elif any(dev_cmd in cmd for dev_cmd in ["npm", "pip", "poetry", "cargo", "mvn"]):
                command_types.append("依赖管理")
            elif any(sys_cmd in cmd for sys_cmd in ["sudo", "chmod", "chown", "systemctl"]):
                command_types.append("系统管理")
            elif any(net_cmd in cmd for net_cmd in ["curl", "wget", "ssh", "ping"]):
                command_types.append("网络操作")

        if command_types:
            unique_types = list(set(command_types))
            analysis_parts.append(f"📊 **操作模式**: {', '.join(unique_types)}")

    return "\n".join(analysis_parts) if analysis_parts else "📋 基本环境信息"


def _determine_user_skill_level(context: Dict[str, Any]) -> str:
    """基于上下文推断用户技能水平"""
    recent_history = context.get("recent_history", [])
    if not recent_history:
        return "beginner"

    # 分析命令复杂度
    advanced_commands = ["awk", "sed", "grep -P", "find -exec", "xargs", "jq"]
    intermediate_commands = ["git rebase", "docker", "ssh", "rsync", "tar"]

    advanced_count = sum(
        1 for cmd in recent_history if any(adv in cmd for adv in advanced_commands)
    )
    intermediate_count = sum(
        1 for cmd in recent_history if any(inter in cmd for inter in intermediate_commands)
    )

    if advanced_count >= 2:
        return "advanced"
    elif intermediate_count >= 3:
        return "intermediate"
    else:
        return "beginner"


def _generate_contextual_system_prompt(context: Dict[str, Any]) -> str:
    """生成基于上下文的系统提示词"""

    # 基础角色定义
    base_role = """你是一个专业的 Linux/macOS 命令行专家和AI助手。
你的目标是帮助用户理解和解决终端问题，同时提供精准的教学指导。"""

    # 分析用户技能水平
    skill_level = _determine_user_skill_level(context)

    # 项目特定指导
    project_context = context.get("project_context", {})
    project_type = project_context.get("project_type", "unknown")

    # 构建个性化指导
    personalized_guidance = []

    if skill_level == "beginner":
        personalized_guidance.append("- 提供详细的命令解释和基础概念")
        personalized_guidance.append("- 使用简单易懂的语言")
        personalized_guidance.append("- 重点说明安全性和风险")
    elif skill_level == "intermediate":
        personalized_guidance.append("- 平衡解释深度和实用性")
        personalized_guidance.append("- 提供替代方案和最佳实践")
        personalized_guidance.append("- 适当引用相关工具和概念")
    else:  # advanced
        personalized_guidance.append("- 提供深入的技术细节")
        personalized_guidance.append("- 关注效率和高级用法")
        personalized_guidance.append("- 适当提及边缘案例和系统原理")

    # 项目特定指导
    if project_type == "python":
        personalized_guidance.append("- 重点关注Python生态系统和虚拟环境")
        personalized_guidance.append("- 结合pip、poetry等包管理工具")
        personalized_guidance.append("- 考虑PEP规范和最佳实践")
    elif project_type == "node":
        personalized_guidance.append("- 关注npm/yarn生态系统")
        personalized_guidance.append("- 考虑Node.js版本管理")
        personalized_guidance.append("- 涉及前端/后端构建流程")
    elif project_type == "docker":
        personalized_guidance.append("- 重点关注容器化相关问题")
        personalized_guidance.append("- 考虑镜像、网络、存储等Docker概念")
        personalized_guidance.append("- 涉及容器编排和部署")

    # 网络状态相关指导
    network_context = context.get("network_context", {})
    if network_context.get("internet_connectivity") is False:
        personalized_guidance.append("- 特别关注离线环境的解决方案")
        personalized_guidance.append("- 优先推荐不需要网络的方法")

    # 权限相关指导
    permission_context = context.get("permission_context", {})
    if permission_context.get("current_user") == "root":
        personalized_guidance.append("- 注意root用户的安全风险")
        personalized_guidance.append("- 强调最小权限原则")
    elif not permission_context.get("sudo_available"):
        personalized_guidance.append("- 提供无sudo的替代方案")
        personalized_guidance.append("- 关注用户权限范围内的解决方法")

    guidance_text = "\n".join(personalized_guidance)

    return f"""{base_role}

**个性化指导原则:**
{guidance_text}

**核心分析框架:**
1. **多层诊断**: 网络→权限→项目→环境，逐层分析问题根源
2. **情境感知**: 充分利用用户当前的工作上下文和历史模式
3. **解决导向**: 不仅解释问题，更要提供可行的解决路径
4. **教学价值**: 帮助用户理解背后的原理，提升整体技能
5. **安全优先**: 任何建议都要考虑安全性和风险评估

**输出格式要求:**
请严格按照以下JSON格式返回分析结果：
{{
  "explanation": "**🔍 问题诊断:**\\n[基于多层分析的问题根源]\\n"
                 "**📚 知识扩展:**\\n[相关概念和背景知识]\\n"
                 "**🎯 解决思路:**\\n[具体的解决策略和步骤]",
  "suggestions": [
    {{
      "description": "解决方案的详细说明和适用场景",
      "command": "具体命令",
      "risk_level": "safe|moderate|dangerous",
      "explanation": "命令原理和参数说明"
    }}
  ],
  "follow_up_questions": [
    "相关的学习建议和延伸问题"
  ]
}}

**重要**: 确保JSON格式正确，字符串使用双引号，避免语法错误。"""


def _make_api_request(
    messages: List[Dict[str, str]],
    config: Dict[str, Any],
    temperature: float = 0.7,
    max_tokens: int = 1000,
) -> Optional[str]:
    """统一的AI API请求函数。"""
    provider_name = config.get("default_provider", "default_free")
    provider = config.get("providers", {}).get(provider_name)

    if not provider:
        raise ValueError(f"Provider '{provider_name}' not found in configuration")

    base_url = provider.get("base_url")
    model_name = provider.get("model_name")
    api_key = provider.get("api_key")

    if not all([base_url, model_name]):
        raise ValueError("Incomplete provider configuration")

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model_name,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    # 从配置文件读取超时时间，默认120秒
    timeout = config.get("advanced", {}).get("request_timeout", 120.0)

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(base_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            return None

    except httpx.RequestError as e:
        raise ConnectionError(f"Failed to connect to AI service: {e}")
    except httpx.HTTPStatusError as e:
        raise ConnectionError(
            f"AI service returned error {e.response.status_code}: " f"{e.response.text}"
        )
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")


def ask_ai(question: str, config: Dict[str, Any]) -> Optional[str]:
    """Ask AI a question and return the response."""
    messages = [{"role": "user", "content": question}]
    return _make_api_request(messages, config)


def ask_ai_with_context(question: str, config: Dict[str, Any]) -> Optional[str]:
    """带上下文感知的ask功能。"""
    from .context import collect_ask_context

    # 收集上下文信息
    context = collect_ask_context(config)

    # 如果在敏感目录，使用普通ask
    if context.get("error"):
        return ask_ai(question, config)

    # 构建上下文感知的系统提示词
    system_prompt = _generate_contextual_system_prompt_for_ask(context)

    # 构建消息
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": question}]

    return _make_api_request(messages, config)


def _generate_contextual_system_prompt_for_ask(context: Dict[str, Any]) -> str:
    """为ask功能生成上下文感知的系统提示词。"""
    prompt_parts = [
        "你是AIS (AI Shell)的智能助手。",
        "基于提供的环境上下文信息，为用户提供准确、相关的回答。",
        "",
        "**当前环境信息:**",
    ]

    # 基础环境信息
    if context.get("cwd"):
        prompt_parts.append(f"- 工作目录: {context['cwd']}")
    if context.get("user"):
        prompt_parts.append(f"- 用户: {context['user']}")

    # 系统基础信息（minimal级别包含）
    if context.get("distro"):
        prompt_parts.append(f"- 系统发行版: {context['distro']}")
    if context.get("kernel_version"):
        prompt_parts.append(f"- 内核版本: {context['kernel_version']}")
    if context.get("cpu_cores"):
        cpu_info = f"{context['cpu_cores']}核"
        if context.get("cpu_model"):
            cpu_info += (
                f" ({context['cpu_model'][:50]}{'...' if len(context['cpu_model']) > 50 else ''})"
            )
        prompt_parts.append(f"- CPU: {cpu_info}")
    if context.get("memory"):
        prompt_parts.append(f"- 内存: {context['memory']}")
    if context.get("disk_usage"):
        prompt_parts.append(f"- 磁盘: {context['disk_usage']}")
    if context.get("load_average"):
        prompt_parts.append(f"- 系统负载: {context['load_average']}")
    if "internet_connectivity" in context:
        conn_status = "可连接" if context["internet_connectivity"] else "不可连接"
        prompt_parts.append(f"- 网络状态: {conn_status} (ping 8.8.8.8)")
    if context.get("listening_ports"):
        ports = ", ".join(context["listening_ports"][:8])
        if len(context["listening_ports"]) > 8:
            ports += "..."
        prompt_parts.append(f"- 监听端口: {ports}")
    if context.get("running_services"):
        services = ", ".join(context["running_services"][:6])
        if len(context["running_services"]) > 6:
            services += "..."
        prompt_parts.append(f"- 运行服务: {services}")

    # Git信息
    if context.get("git_branch"):
        prompt_parts.append(f"- Git分支: {context['git_branch']}")
    if context.get("git_status"):
        git_status = context["git_status"][:200] + (
            "..." if len(context["git_status"]) > 200 else ""
        )
        prompt_parts.append(f"- Git状态: {git_status}")

    # 项目类型信息
    if context.get("project_type") and context["project_type"] != "unknown":
        prompt_parts.append(f"- 项目类型: {context['project_type']}")
        if context.get("framework"):
            prompt_parts.append(f"- 框架: {context['framework']}")

    # 网络上下文（仅在detailed级别）
    if context.get("network_context"):
        net_ctx = context["network_context"]
        if isinstance(net_ctx, dict) and not net_ctx.get("error"):
            conn_status = "正常" if net_ctx.get("internet_connectivity") else "异常"
            prompt_parts.append(f"- 网络连接: {conn_status}")

    # 权限上下文（仅在detailed级别）
    if context.get("permission_context"):
        perm_ctx = context["permission_context"]
        if isinstance(perm_ctx, dict) and not perm_ctx.get("error"):
            if perm_ctx.get("current_user"):
                prompt_parts.append(f"- 当前用户: {perm_ctx['current_user']}")

    # 文件列表（如果是standard或detailed级别）
    if context.get("current_files"):
        files = context["current_files"][:10]  # 只显示前10个文件
        if files:
            files_str = ", ".join(files[:5]) + ("..." if len(files) > 5 else "")
            prompt_parts.append(f"- 当前目录文件: {files_str}")

    prompt_parts.extend(
        [
            "",
            "**回答原则:**",
            "1. 结合上下文环境给出针对性建议",
            "2. 如果是Git相关问题，参考当前分支和状态",
            "3. 如果是项目相关问题，考虑项目类型和技术栈",
            "4. 提供具体、可操作的命令和步骤",
            "5. 如果上下文不足，明确指出需要更多信息",
            "",
        ]
    )

    return "\n".join(prompt_parts)


def analyze_error(
    command: str,
    exit_code: int,
    stderr: str,
    context: Dict[str, Any],
    config: Dict[str, Any],
) -> Dict[str, Any]:
    """Analyze a command error using AI."""

    # 生成基于上下文的个性化系统提示词
    system_prompt = _generate_contextual_system_prompt(context)

    # 构建详细的错误描述
    error_info = f"**失败命令**: `{command}`\n**退出码**: {exit_code}"

    if stderr and stderr.strip():
        error_info += f"\n**错误输出**: {stderr}"
    else:
        error_info += "\n**注意**: 无错误输出，基于命令和退出码分析"

    # 构建智能上下文分析
    context_analysis = _build_intelligent_context_analysis(context)

    # 构建结构化的用户提示
    user_prompt = f"""{error_info}

**环境诊断信息:**
{context_analysis}

**核心分析任务:**
请基于以上信息进行多层次分析：

1. **网络诊断**: 检查是否为网络相关问题
2. **权限分析**: 分析权限和文件访问问题
3. **项目环境**: 结合项目类型和构建系统分析
4. **系统状态**: 考虑系统资源和环境因素

**关键要求:**
- 优先分析最可能的问题根源
- 提供针对当前环境的实用解决方案
- 考虑用户的技能水平和工作流程
- 包含预防性建议和学习指导

**输出要求:**
必须返回完整的JSON格式，包含explanation、suggestions和follow_up_questions三个字段。"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    try:
        content = _make_api_request(messages, config, temperature=0.3, max_tokens=2500)
        if not content:
            return {
                "explanation": "AI服务无响应，请检查网络连接或服务配置",
                "suggestions": [],
                "follow_up_questions": [],
            }

        # Try to parse JSON response
        try:
            # 清理可能的前后空白和换行
            content = content.strip()
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback: try to extract from markdown code block
            import re

            json_match = re.search(r"```json\s*(\{.*?\})\s*```", content, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass

            # 尝试查找任何JSON对象（更宽松的匹配）
            json_match = re.search(r"\{[\s\S]*\}", content)
            if json_match:
                try:
                    # 尝试清理格式问题
                    json_content = json_match.group(0)
                    # 移除Python元组语法等
                    json_content = re.sub(r'\(\s*"([^"]+)"\s*\)', r'"\1"', json_content)
                    # 修复字符串连接问题
                    json_content = re.sub(r'"\s*\+\s*"', "", json_content)
                    json_content = re.sub(r'"\s*\)\s*,\s*\(\s*"', "", json_content)
                    return json.loads(json_content)
                except json.JSONDecodeError:
                    pass

            # 如果还是解析失败，尝试使用更智能的方式解析
            try:
                # 尝试提取explanation, suggestions和follow_up_questions
                explanation_match = re.search(r'"explanation":\s*"([^"]+)', content, re.DOTALL)
                if explanation_match:
                    explanation = explanation_match.group(1)
                    # 清理explanation中的格式问题
                    explanation = explanation.replace("\\n", "\n")

                    # 提取suggestions
                    suggestions = []
                    suggestion_pattern = (
                        r'"description":\s*"([^"]+)"[^}]*'
                        r'"command":\s*"([^"]+)"[^}]*'
                        r'"risk_level":\s*"([^"]+)"[^}]*'
                        r'"explanation":\s*"([^"]+)"'
                    )
                    for match in re.finditer(suggestion_pattern, content):
                        suggestions.append(
                            {
                                "description": match.group(1),
                                "command": match.group(2),
                                "risk_level": match.group(3),
                                "explanation": match.group(4),
                            }
                        )

                    return {
                        "explanation": explanation,
                        "suggestions": suggestions,
                        "follow_up_questions": [],
                    }
            except Exception:
                pass

            # 最后的fallback - 返回原始内容作为explanation
            return {
                "explanation": f"**AI分析结果**:\n{content}",
                "suggestions": [],
                "follow_up_questions": [],
            }

    except Exception as e:
        return {
            "explanation": f"**AI分析失败**: {str(e)}\n请检查网络连接或AI服务配置",
            "suggestions": [],
            "follow_up_questions": [],
        }
