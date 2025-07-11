"""AI interaction module for AIS."""

import json
import httpx
from typing import Dict, Any, Optional, List


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

请分析失败的命令并提供教学性的帮助。你必须用中文回复，并且严格按照以下 JSON 格式：

{
  "explanation": "详细的错误分析，包含：1) 错误原因的简明解释 2) 相关命令或概念的背景知识 3) 这类错误的常见场景 4) 如何避免类似错误。使用 Markdown 格式，如 `代码` 或 **重点**。",
  "suggestions": [
    {
      "description": "这个解决方案的详细说明，包括为什么要这样做和预期效果",
      "command": "具体的命令",
      "risk_level": "safe",
      "explanation": "这个命令的工作原理和每个参数的作用"
    }
  ]
}

风险等级：
- "safe": 安全操作，不会造成数据丢失
- "moderate": 需要谨慎，可能影响系统状态
- "dangerous": 危险操作，可能造成数据丢失

重要原则：
1. 用教学的语气，解释"为什么"而不只是"怎么做"
2. 提供背景知识，帮助用户理解概念
3. 按风险从低到高排序建议
4. 为每个建议提供详细的解释
5. 如果可能，提供相关的学习资源或进阶技巧
"""
    
    user_prompt = f"""Command failed: `{command}`
Exit code: {exit_code}
Error output: {stderr}

Context information:
{json.dumps(context, indent=2)}

Please analyze this error and provide helpful suggestions."""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        content = _make_api_request(messages, config, temperature=0.3, max_tokens=2000)
        if not content:
            return {"explanation": "No response from AI service", "suggestions": []}
        
        # Try to parse JSON response
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback: try to extract from markdown code block
            import re
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            else:
                return {"explanation": content, "suggestions": []}
                
    except Exception as e:
        return {"explanation": f"Error communicating with AI service: {e}", "suggestions": []}