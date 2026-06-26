"""DeepSeek 智能体

使用 DeepSeek API 解析自然语言设计需求，生成结构化的设计命令。

说明：本模块替换了原先基于 OpenAI 的实现，使用 HTTP REST 调用 DeepSeek。
"""

import json
import logging
from typing import Dict, Any, List, Optional
import requests
from config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_API_URL,
    DEEPSEEK_MODEL,
    DEEPSEEK_TEMPERATURE,
    DEEPSEEK_MAX_TOKENS,
    AI_SYSTEM_PROMPT,
)

logger = logging.getLogger(__name__)


class GPTAgent:
    """DeepSeek 驱动的智能体（保留类名 GPTAgent 以兼容现有代码）

    用于理解自然语言设计需求，生成结构化的 CAD 操作命令。
    """

    def __init__(self, api_key: str = DEEPSEEK_API_KEY, model: str = DEEPSEEK_MODEL):
        """初始化智能体
        
        Args:
            api_key: DeepSeek API 密钥
            model: 使用的 DeepSeek 模型名称
        """
        self.api_key = api_key
        self.model = model
        self.logger = logger
        self.conversation_history: List[Dict[str, str]] = []

    def _build_prompt(self, user_input: str) -> str:
        """把系统提示和用户输入组合成最终 prompt"""
        prompt = AI_SYSTEM_PROMPT + "\n用户输入: " + user_input
        return prompt

    def _extract_json_from_text(self, text: str) -> Any:
        """尝试从自由文本中提取 JSON 对象（若 response 为纯文本包含 JSON）"""
        # 最简单的策略：寻找第一个 { 和最后一个 }
        try:
            start = text.index("{")
            end = text.rindex("}") + 1
            json_text = text[start:end]
            return json.loads(json_text)
        except Exception:
            # 直接尝试完整解析
            try:
                return json.loads(text)
            except Exception:
                return None

    def parse_design_request(self, user_input: str) -> Dict[str, Any]:
        """解析用户的设计需求
        
        Args:
            user_input: 用户输入的自然语言设计需求
            
        Returns:
            结构化的设计命令字典
        """
        self.logger.info(f"Parsing design request (DeepSeek): {user_input}")
        self.conversation_history.append({"role": "user", "content": user_input})

        prompt = self._build_prompt(user_input)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": DEEPSEEK_TEMPERATURE,
            "max_tokens": DEEPSEEK_MAX_TOKENS,
            # 根据 DeepSeek API 的实际字段调整
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            url = DEEPSEEK_API_URL.rstrip("/") + "/v1/generate"
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            # DeepSeek 返回结构可能不同，尝试多种常见字段
            text = None
            if isinstance(data, dict):
                # 常见字段尝试
                if "output" in data and isinstance(data["output"], str):
                    text = data["output"]
                elif "text" in data and isinstance(data["text"], str):
                    text = data["text"]
                elif "result" in data:
                    # result 可能是字符串或 dict
                    if isinstance(data["result"], str):
                        text = data["result"]
                    else:
                        # 直接返回 dict
                        return data["result"]
                elif "choices" in data and isinstance(data["choices"], list) and len(data["choices"]) > 0:
                    c0 = data["choices"][0]
                    if isinstance(c0, dict) and "text" in c0:
                        text = c0["text"]
                    elif isinstance(c0, str):
                        text = c0

            if text is None:
                # 如果 data 是字符串
                if isinstance(data, str):
                    text = data

            if text is None:
                self.logger.error("Unable to extract text from DeepSeek response")
                raise ValueError("Invalid response from DeepSeek API")

            # 尝试把 text 解析为 JSON（模型应该返回 JSON 格式的命令）
            parsed = self._extract_json_from_text(text)
            if parsed is None:
                self.logger.error(f"Failed to parse JSON from DeepSeek text: {text}")
                raise ValueError("DeepSeek did not return valid JSON command")

            # 记录 assistant 内容
            self.conversation_history.append({"role": "assistant", "content": text})
            self.logger.info(f"Parsed design command: {parsed}")
            return parsed

        except requests.exceptions.RequestException as e:
            self.logger.error(f"DeepSeek API request failed: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error parsing DeepSeek response: {e}")
            raise

    def refine_design(self, refinement: str) -> Dict[str, Any]:
        """基于用户反馈进行设计优化"""
        return self.parse_design_request(refinement)

    def suggest_design_improvements(self, current_design: Dict[str, Any]) -> List[str]:
        """基于当前设计提出改进建议（会向 DeepSeek 请求改进建议）"""
        # 避免在 f-string 中直接嵌套未转义的大括号，先准备一个 JSON 模板字符串
        template = '{"suggestions": []}'
        prompt = (
            "根据以下当前设计，提出 3-5 条改进建议：\n\n"
            f"当前设计: {json.dumps(current_design, indent=2)}\n\n"
            "请以 JSON 格式返回建议列表："
            + template
        )
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": DEEPSEEK_TEMPERATURE,
            "max_tokens": 400,
        }
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
        try:
            url = DEEPSEEK_API_URL.rstrip("/") + "/v1/generate"
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            text = None
            if isinstance(data, dict):
                text = data.get("output") or data.get("text") or (data.get("choices") and data.get("choices")[0].get("text"))
            if text is None and isinstance(data, str):
                text = data
            parsed = self._extract_json_from_text(text or "")
            if not parsed:
                return []
            return parsed.get("suggestions", [])
        except Exception as e:
            self.logger.error(f"Error generating suggestions from DeepSeek: {e}")
            return []

    def clear_history(self):
        self.conversation_history = []
        self.logger.info("Conversation history cleared")

    def get_conversation_history(self) -> List[Dict[str, str]]:
        return self.conversation_history.copy()
