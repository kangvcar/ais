"""AI interaction module for AIS."""

import json
import httpx
from typing import Dict, Any, Optional, List


def _build_context_summary(context: Dict[str, Any]) -> str:
    """构建简洁的上下文摘要"""
    summary_parts = []
    
    # 基本环境信息
    if context.get('cwd'):
        summary_parts.append(f"📁 当前目录: {context['cwd']}")
    
    if context.get('user'):
        summary_parts.append(f"👤 用户: {context['user']}")
    
    # Git仓库信息
    git_info = context.get('git_info', {})
    if git_info.get('in_repo'):
        git_status = f"🔄 Git仓库: {git_info.get('current_branch', 'unknown')}分支"
        if git_info.get('has_changes'):
            git_status += f" (有{git_info.get('changed_files', 0)}个文件变更)"
        summary_parts.append(git_status)
    
    # 项目类型分析
    dir_info = context.get('current_dir_files', {})
    if dir_info.get('project_type') and dir_info['project_type'] != 'unknown':
        project_info = f"🚀 项目类型: {dir_info['project_type']}"
        if dir_info.get('key_files'):
            project_info += f" (关键文件: {', '.join(dir_info['key_files'][:3])})"
        summary_parts.append(project_info)
    
    # 系统状态
    system_status = context.get('system_status', {})
    if system_status:
        status_info = f"⚡ 系统状态: CPU {system_status.get('cpu_percent', 0):.1f}%"
        if 'memory' in system_status:
            status_info += f", 内存 {system_status['memory'].get('percent', 0):.1f}%"
        summary_parts.append(status_info)
    
    # 最近的操作模式
    work_pattern = context.get('work_pattern', {})
    if work_pattern.get('activities'):
        activities = work_pattern['activities'][:3]  # 只显示前3个
        summary_parts.append(f"🎯 最近操作: {', '.join(activities)}")
    
    # 网络状态
    network_info = context.get('network_info', {})
    if network_info.get('internet_available') is False:
        summary_parts.append("🌐 网络: 离线状态")
    
    return "\n".join(summary_parts) if summary_parts else "📋 基本环境信息"


def _make_api_request(messages: List[Dict[str, str]], config: Dict[str, Any], temperature: float = 0.7, max_tokens: int = 1000) -> Optional[str]:
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
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(base_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            return None
                
    except httpx.RequestError as e:
        raise ConnectionError(f"Failed to connect to AI service: {e}")
    except httpx.HTTPStatusError as e:
        raise ConnectionError(f"AI service returned error {e.response.status_code}: {e.response.text}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")


def ask_ai(question: str, config: Dict[str, Any]) -> Optional[str]:
    """Ask AI a question and return the response."""
    messages = [{"role": "user", "content": question}]
    return _make_api_request(messages, config)


def analyze_error(command: str, exit_code: int, stderr: str, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze a command error using AI."""
    system_prompt = """你是一个专业的 Linux/macOS 命令行专家和导师。你的目标是帮助用户理解和解决终端问题，同时教会他们相关的知识。

**重要**：你需要结合用户的具体环境上下文来提供个性化的教学内容：
- 如果在Git仓库中，重点解释与版本控制相关的概念
- 如果在特定项目类型中（如Python/Node.js/Docker等），结合该生态系统的最佳实践
- 如果用户最近在进行某种操作模式，要考虑操作的连贯性
- 根据用户的命令历史判断技能水平，调整解释的深度
- 基于当前工作目录和文件结构提供针对性建议

请分析失败的命令并提供教学性的帮助。你必须用中文回复，并且严格按照以下 JSON 格式：

{
  "explanation": "**🔍 错误分析:**\\n[结合当前环境简明解释错误原因]\\n\\n**📚 背景知识:**\\n[相关命令或概念的核心原理，结合用户所在的项目类型和环境]\\n\\n**🎯 常见场景:**\\n[这类错误的典型触发情况，特别是在当前环境下]\\n\\n**🛡️ 预防措施:**\\n[如何避免类似错误，结合用户的操作模式和项目类型]\\n\\n**💡 进阶提示:**\\n[基于用户环境的相关高级技巧或最佳实践]\\n\\n**🔄 后续学习:**\\n[如果想深入了解相关概念，可以询问的具体问题]",
  "suggestions": [
    {
      "description": "这个解决方案的详细说明，包括为什么要这样做和预期效果（结合当前环境和项目背景）",
      "command": "具体的命令",
      "risk_level": "safe",
      "explanation": "这个命令的工作原理和每个参数的作用，以及在当前环境下的特殊考虑"
    }
  ],
  "follow_up_questions": [
    "想了解更多关于[相关概念]的知识吗？",
    "需要我解释[相关工具]的工作原理吗？"
  ]
}

风险等级：
- "safe": 安全操作，不会造成数据丢失
- "moderate": 需要谨慎，可能影响系统状态
- "dangerous": 危险操作，可能造成数据丢失

重要原则：
1. **上下文感知**：充分利用环境信息（Git状态、项目类型、目录结构、命令历史）提供个性化建议
2. **教学导向**：解释"为什么"而不只是"怎么做"，建立概念关联网络
3. **渐进式学习**：根据用户技能水平调整解释深度，提供从基础到进阶的知识递进
4. **实用性优先**：结合具体环境提供真正有用的解决方案
5. **学习引导**：提供后续学习方向和互动问题
6. **预防性教育**：不仅解决当前问题，还要帮助用户避免类似错误
"""
    
    # 构建更详细的错误描述
    error_info = f"Command failed: `{command}`\nExit code: {exit_code}"
    
    if stderr and stderr.strip():
        error_info += f"\nError output: {stderr}"
    else:
        error_info += f"\nNote: No stderr captured, analysis based on command and exit code"
    
    # 构建结构化的上下文信息
    context_summary = _build_context_summary(context)
    
    user_prompt = f"""{error_info}

**环境上下文信息:**
{context_summary}

**完整上下文数据:**
{json.dumps(context, indent=2, ensure_ascii=False)}

**分析要求:**
请根据上述环境信息和用户的操作上下文，提供个性化的错误分析和教学内容。特别注意：
1. 结合当前的项目类型和目录结构
2. 考虑用户的操作历史和技能水平
3. 基于Git状态（如果适用）提供版本控制相关的建议
4. 如果是开发环境，结合相应的生态系统最佳实践
5. 提供符合用户当前工作流程的解决方案"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        content = _make_api_request(messages, config, temperature=0.3, max_tokens=2000)
        if not content:
            return {"explanation": "No response from AI service", "suggestions": [], "follow_up_questions": []}
        
        # Try to parse JSON response
        try:
            # 清理可能的前后空白和换行
            content = content.strip()
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback: try to extract from markdown code block
            import re
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # 尝试查找任何JSON对象
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except json.JSONDecodeError:
                    pass
            
            # 最后的fallback - 返回原始内容作为explanation
            return {"explanation": content, "suggestions": [], "follow_up_questions": []}
                
    except Exception as e:
        return {"explanation": f"Error communicating with AI service: {e}", "suggestions": [], "follow_up_questions": []}