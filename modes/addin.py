"""Fusion 360 Add-In 插件模式

作为 Fusion 360 的原生插件运行。
"""

import logging
import adsk.core
import adsk.fusion
import traceback
from config import LOG_LEVEL, LOG_FILE
from src.gpt_agent import GPTAgent
from src.command_parser import CommandParser
from src.model_generator import ModelGenerator
from src.fusion_client import FusionClient
from src.utils import setup_logging

# 全局对象
app = None
ui = None
handlers = []


def log_exception(ex):
    """记录异常"""
    logging.error(traceback.format_exc())
    if ui:
        ui.messageBox(f"错误: {str(ex)}")


class DesignCommandHandler(adsk.core.CommandEventHandler):
    """设计命令事件处理器"""

    def __init__(self):
        """初始化处理器"""
        super().__init__()
        self.gpt_agent = GPTAgent()
        self.parser = CommandParser()
        self.fusion_client = FusionClient()
        self.generator = ModelGenerator(self.fusion_client)

    def notify(self, args):
        """处理命令事件
        
        Args:
            args: 事件参数
        """
        try:
            # 获取用户输入
            user_input = self._get_user_input()
            if not user_input:
                return

            logging.info(f"Processing user input: {user_input}")

            # 使用 GPT 解析设计需求
            design_command = self.gpt_agent.parse_design_request(user_input)
            logging.info(f"Design command: {design_command}")

            # 验证命令
            validated_command = self.parser.parse_command(design_command)
            logging.info(f"Validated command: {validated_command}")

            # 生成模型
            self.generator.initialize_document()
            feature_id = self.generator.generate_from_command(validated_command)
            logging.info(f"Generated feature: {feature_id}")

            # 记录执行
            self.parser.record_execution(validated_command)

            # 显示成功消息
            if ui:
                ui.messageBox(f"成功! 已创建: {design_command.get('operation')}")

        except Exception as ex:
            log_exception(ex)

    def _get_user_input(self) -> str:
        """获取用户输入（从对话框）
        
        Returns:
            用户输入的字符串
        """
        if not ui:
            return ""

        # 创建输入对话框
        dialog = ui.createFolderDialog()
        dialog.title = "输入设计需求"

        # 在实际实现中，应该使用自定义对话框获取文本输入
        # 这里是一个简化的示例
        return "创建一个长100mm宽50mm高30mm的矩形盒子"


def create_command(cmd_def):
    """创建命令
    
    Args:
        cmd_def: 命令定义
    """
    onCommandCreated = DesignCommandHandler()
    cmd_def.commandCreated += onCommandCreated
    handlers.append(onCommandCreated)


def run(context):
    """运行 Add-In
    
    Args:
        context: Add-In 上下文
    """
    global app, ui

    try:
        # 初始化日志
        setup_logging()
        logging.info("Fusion 360 AI Agent Add-In starting...")

        # 获取应用和 UI
        app = adsk.core.Application.get()
        ui = app.userInterface

        # 创建命令定义
        cmd_defs = ui.commandDefinitions
        cmd_def = cmd_defs.addButtonDefinition(
            "fusion360AIAgentCmd",
            "Fusion 360 AI Agent",
            "使用 AI 生成 3D 模型"
        )

        # 注册命令处理器
        create_command(cmd_def)

        # 创建工具栏按钮
        toolbars = ui.toolbars
        toolbar = toolbars.itemById("SolidTab")
        if toolbar:
            controls = toolbar.controls
            control = controls.addCommand(cmd_def)
            control.isVisible = True
            control.isPromoted = True

        logging.info("Fusion 360 AI Agent Add-In initialized successfully")

    except Exception as ex:
        log_exception(ex)


def stop(context):
    """停止 Add-In
    
    Args:
        context: Add-In 上下文
    """
    try:
        logging.info("Fusion 360 AI Agent Add-In stopping...")
    except Exception as ex:
        log_exception(ex)
