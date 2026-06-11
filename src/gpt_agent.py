"""OpenAI GPT 智能体

使用 OpenAI GPT API 解析自然语言设计需求，生成结构化的设计命令。
"""

import json
import logging
from typing import Dict, Any, List, Optional
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS, AI_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class GPTAgent:
    """GPT 智能体
    
    用于理解自然语言设计���求，生成结构化的 CAD 操作命令。
    """

    def __init__(self, api_key: str = OPENAI_API_KEY, model: str = OPENAI_MODEL):
        """初始化 GPT 智能体
        
        Args:
            api_key: OpenAI API 密钥
            model: 使用的模型 (gpt-4, gpt-3.5-turbo, etc.)
        """
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key)
        self.logger = logger
        self.conversation_history: List[Dict[str, str]] = []

    def parse_design_request(self, user_input: str) -> Dict[str, Any]:
        """解析用户的设计需求
        
        Args:
            user_input: 用户输入的自然语言设计需求
            
        Returns:
            结构化的设计命令字典
        """
        self.logger.info(f"Parsing design request: {user_input}")
        
        # 添加到对话历史
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": AI_SYSTEM_PROMPT},
                    *self.conversation_history
                ],
                temperature=OPENAI_TEMPERATURE,
                max_tokens=OPENAI_MAX_TOKENS,
                response_format={"type": "json_object"}  # 返回 JSON 格式
            )
            
            # 提取响应内容
            assistant_message = response.choices[0].message.content
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # 解析 JSON 响应
            result = json.loads(assistant_message)
            self.logger.info(f"Parsed design command: {result}")
            return result
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Invalid JSON response from GPT: {e}")
        except Exception as e:
            self.logger.error(f"Error calling OpenAI API: {e}")
            raise

    def refine_design(self, refinement: str) -> Dict[str, Any]:
        """基于用户反馈进行设计优化
        
        Args:
            refinement: 用户的优化建议
            
        Returns:
            优化后的设计命令
        """
        self.logger.info(f"Refining design: {refinement}")
        return self.parse_design_request(refinement)

    def suggest_design_improvements(self, current_design: Dict[str, Any]) -> List[str]:
        """基于当前设计提出改进建议
        
        Args:
            current_design: 当前的设计命令
            
        Returns:
            改进建议列表
        """
        self.logger.info("Suggesting design improvements")
        
        prompt = f"""
        根据以下当前设计，提出 3-5 条改进建议：
        
        当前设计: {json.dumps(current_design, indent=2)}
        
        请以 JSON 格式返回建议列表：
        {{
            "suggestions": ["建议1", "建议2", ...]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个 CAD 设计专家。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=OPENAI_TEMPERATURE,
                max_tokens=OPENAI_MAX_TOKENS,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            suggestions = result.get("suggestions", [])
            self.logger.info(f"Generated {len(suggestions)} design suggestions")
            return suggestions
            
        except Exception as e:
            self.logger.error(f"Error generating design suggestions: {e}")
            return []

    def clear_history(self):
        """清除对话历史"""
        self.conversation_history = []
        self.logger.info("Conversation history cleared")

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """获取对话历史
        
        Returns:
            对话历史列表
        """
        return self.conversation_history.copy()
