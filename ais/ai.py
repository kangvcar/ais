"""AI interaction module for AIS."""

import json
import httpx
from typing import Dict, Any, Optional


def ask_ai(question: str, config: Dict[str, Any]) -> Optional[str]:
    """Ask AI a question and return the response."""
    provider_name = config.get("default_provider", "default_free")
    provider = config.get("providers", {}).get(provider_name)
    
    if not provider:
        raise ValueError(f"Provider '{provider_name}' not found in configuration")
    
    base_url = provider.get("base_url")
    model_name = provider.get("model_name")
    api_key = provider.get("api_key")
    
    if not all([base_url, model_name]):
        raise ValueError("Incomplete provider configuration")
    
    headers = {
        "Content-Type": "application/json",
    }
    
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000,
    }
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(base_url, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            else:
                return None
                
    except httpx.RequestError as e:
        raise ConnectionError(f"Failed to connect to AI service: {e}")
    except httpx.HTTPStatusError as e:
        raise ConnectionError(f"AI service returned error {e.response.status_code}: {e.response.text}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")


def analyze_error(command: str, exit_code: int, stderr: str, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze a command error using AI."""
    provider_name = config.get("default_provider", "default_free")
    provider = config.get("providers", {}).get(provider_name)
    
    if not provider:
        raise ValueError(f"Provider '{provider_name}' not found in configuration")
    
    # Build the system prompt
    system_prompt = """You are a Linux/macOS command line expert. Analyze the failed command and provide helpful suggestions.

You MUST respond with a valid JSON object in exactly this format:
{
  "explanation": "Detailed analysis of the error, causes, and background knowledge. You can use Markdown formatting like `code` or **bold**.",
  "suggestions": [
    {
      "description": "Description of what this command does.",
      "command": "the actual command",
      "risk_level": "safe"
    }
  ]
}

Risk levels: "safe", "moderate", "dangerous"
"""
    
    # Build the user prompt with context
    user_prompt = f"""Command failed: `{command}`
Exit code: {exit_code}
Error output: {stderr}

Context information:
{json.dumps(context, indent=2)}

Please analyze this error and provide helpful suggestions."""
    
    base_url = provider.get("base_url")
    model_name = provider.get("model_name")
    api_key = provider.get("api_key")
    
    headers = {
        "Content-Type": "application/json",
    }
    
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 2000,
    }
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(base_url, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                
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
                        # Final fallback
                        return {
                            "explanation": content,
                            "suggestions": []
                        }
            else:
                return {
                    "explanation": "No response from AI service",
                    "suggestions": []
                }
                
    except Exception as e:
        return {
            "explanation": f"Error communicating with AI service: {e}",
            "suggestions": []
        }