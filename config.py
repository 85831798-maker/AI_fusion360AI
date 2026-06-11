import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# ============================================
# OpenAI 配置
# ============================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")  # gpt-4 或 gpt-3.5-turbo
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))

# ============================================
# Fusion 360 配置
# ============================================
FUSION_HOST = os.getenv("FUSION_HOST", "localhost")
FUSION_PORT = int(os.getenv("FUSION_PORT", "8080"))
FUSION_TIMEOUT = int(os.getenv("FUSION_TIMEOUT", "30"))
FUSION_API_VERSION = os.getenv("FUSION_API_VERSION", "2.0")

# ============================================
# 日志配置
# ============================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/fusion360_ai.log")

# ============================================
# 应用配置
# ============================================
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
APP_NAME = "Fusion 360 AI Agent"
APP_VERSION = "0.1.0"

# ============================================
# 默认参数
# ============================================
DEFAULT_UNIT = "mm"  # 默认单位：mm、cm、inch
DEFAULT_PRECISION = 0.01  # 默认精度

# ============================================
# AI 提示词配置
# ============================================
AI_SYSTEM_PROMPT = """
你是一个 Fusion 360 CAD 设计专家助手。

你的职责是：
1. 理解用户的自然语言设计需求
2. 将需求转换为具体的设计参数
3. 生成 Fusion 360 API 调用命令
4. 确保设计符合用户的期望

当用户提供设计需求时，你应该：
- 识别要创建的几何体类型（盒子、圆柱、球体等）
- 提取所有相关参数（长、宽、高、半径等）
- 识别是否需要额外的操作（倒角、圆角、孔洞等）
- 返回结构化的 JSON 格式的设计命令

返回格式示例：
{
    "operation": "create_box",
    "parameters": {
        "length": 100,
        "width": 50,
        "height": 30,
        "unit": "mm"
    }
}
"""
