# Fusion 360 AI Agent

一个集成 OpenAI GPT 的 Fusion 360 智能体，支持自然语言解析和自动建模。

## 功能概述

- ✨ **自然语言建模**：用自然语言描述设计需求，AI 自动生成 3D 模型
- 🔌 **双模式运行**：支持 Fusion 360 Add-In 插件和独立工具两种模式
- 🤖 **GPT 驱动**：使用 OpenAI GPT-4 解析设计意图
- ⚙️ **参数化设计**：支持参数化建模和设计优化
- 📊 **设计生成**：自动生成基础几何体和复杂模型

## 项目结构

```
fusion360-ai-agent/
├── README.md                      # 项目说明
├── requirements.txt               # 项目依赖
├── config.py                      # 配置文件
├── src/
│   ├── __init__.py
│   ├── fusion_client.py          # Fusion 360 API 客户端
│   ├── gpt_agent.py              # OpenAI GPT 智能体
│   ├── command_parser.py         # 自然语言命令解析
│   ├── model_generator.py        # 模型生成器
│   └── utils.py                  # 工具函数
├── modes/
│   ├── addin.py                  # Fusion 360 Add-In 插件入口
│   └── standalone.py             # 独立工具运行模式
├── examples/
│   ├── create_box.py             # 示例：创建立方体
│   ├── create_cylinder.py        # 示例：创建圆柱体
│   └── parametric_design.py      # 示例：参数化设计
└── tests/
    ├── test_gpt_agent.py         # GPT 智能体测试
    └── test_fusion_client.py     # Fusion 360 客户端测试
```

## 快速开始

### 前置要求

- Python 3.8+
- Fusion 360 安装
- OpenAI API Key

### 安装

```bash
# 克隆仓库
git clone https://github.com/85831798-maker/AI_fusion360AI.git
cd AI_fusion360AI

# 安装依赖
pip install -r requirements.txt

# 配置 API 密钥
cp config.example.py config.py
# 编辑 config.py，填入你的 OpenAI API Key
```

### 运行模式

#### 1. 独立工具模式

```bash
python modes/standalone.py

# 输入自然语言设计需求
输入设计需求: 创建一个长100mm宽50mm高30mm的矩形盒子
```

#### 2. Fusion 360 Add-In 模式

1. 在 Fusion 360 中，��击 `工具` > `Add-Ins` > `My Add-Ins`
2. 选择 `modes/addin.py` 文件
3. 点击运行
4. 在 Fusion 360 界面中输入自然语言需求

## 使用示例

### 示例 1：创建基础立方体

```bash
python examples/create_box.py
```

### 示例 2：参数化设计

```bash
python examples/parametric_design.py
```

### 示例 3：交互式 AI 设计

```bash
python modes/standalone.py
输入: 创建一个长500mm、宽300mm、高200mm的矩形盒子，然后在上方添加一个半径100mm的圆柱体
```

## 架构设计

### 工作流程

```
用户输入（自然语言）
        ↓
   GPT 解析
        ↓
 命令转换（参数提取）
        ↓
 Fusion 360 API 调用
        ↓
 模型生成
        ↓
 返回结果
```

### 核心模块说明

#### `fusion_client.py`
- 封装 Fusion 360 API 调用
- 支持创建草图、特征、装配等操作
- 连接管理和错误处理

#### `gpt_agent.py`
- 与 OpenAI GPT API 交互
- 自然语言理解和意图识别
- 参数提取和设计推理

#### `command_parser.py`
- 解析 GPT 输出的命令
- 验证参数合法性
- 错误恢复机制

#### `model_generator.py`
- 根据命令生成 3D 模型
- 支持基础几何体（盒子、圆柱、球体等）
- 高级特征（倒角、圆角、孔洞等）

## API 配置

编辑 `config.py`：

```python
# OpenAI 配置
OPENAI_API_KEY = "your-api-key-here"
OPENAI_MODEL = "gpt-4"  # 或 "gpt-3.5-turbo"

# Fusion 360 配置
FUSION_HOST = "localhost"
FUSION_PORT = 8080
FUSION_TIMEOUT = 30
```

## 测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_gpt_agent.py

# 运行带覆盖率的测试
python -m pytest tests/ --cov=src/
```

## 文件说明

| 文件 | 功能 |
|------|------|
| `fusion_client.py` | Fusion 360 API 客户端包装 |
| `gpt_agent.py` | GPT 智能体核心逻辑 |
| `command_parser.py` | 自然语言命令解析 |
| `model_generator.py` | 3D 模型生成器 |
| `addin.py` | Fusion 360 Add-In 入口 |
| `standalone.py` | 独立工具入口 |

## 常见问题

### Q: 如何更新 Fusion 360 API 版本？
A: 在 `config.py` 中更新 `FUSION_API_VERSION`，或修改 `fusion_client.py` 中的 API 调用。

### Q: 支持哪些设计操作？
A: 目前支持基础几何体创建、参数化草图、特征操作。更多功能持续开发中。

### Q: 如何自定义 AI 提示词？
A: 在 `gpt_agent.py` 中修改 `SYSTEM_PROMPT` 或 `create_prompt()` 方��。

## 许可证

MIT License

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 技术支持

如有问题，请在 GitHub Issues 中提出。
