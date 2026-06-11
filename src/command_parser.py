"""命令解析器

解析 GPT 生成的设计命令，验证参数，并准备执行。
"""

import json
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


class BoxCommand(BaseModel):
    """立方体命令模型"""
    operation: str = "create_box"
    length: float
    width: float
    height: float
    unit: str = "mm"


class CylinderCommand(BaseModel):
    """圆柱体命令模型"""
    operation: str = "create_cylinder"
    radius: float
    height: float
    unit: str = "mm"


class SphereCommand(BaseModel):
    """球体命令模型"""
    operation: str = "create_sphere"
    radius: float
    unit: str = "mm"


class CommandParser:
    """命令解析器
    
    用于解析、验证和执行设计命令。
    """

    SUPPORTED_OPERATIONS = {
        "create_box": BoxCommand,
        "create_cylinder": CylinderCommand,
        "create_sphere": SphereCommand,
    }

    def __init__(self):
        """初始化命令解析器"""
        self.logger = logger
        self.executed_commands: List[Dict[str, Any]] = []

    def parse_command(self, command_dict: Dict[str, Any]) -> Dict[str, Any]:
        """解析和验证命令
        
        Args:
            command_dict: 命令字典
            
        Returns:
            验证后的命令
            
        Raises:
            ValueError: 如果命令无效
        """
        self.logger.info(f"Parsing command: {command_dict}")
        
        operation = command_dict.get("operation")
        if not operation:
            raise ValueError("Command must have 'operation' field")
        
        if operation not in self.SUPPORTED_OPERATIONS:
            raise ValueError(f"Unsupported operation: {operation}")
        
        # 提取参数
        parameters = command_dict.get("parameters", {})
        
        try:
            # 验证参数
            command_model = self.SUPPORTED_OPERATIONS[operation]
            validated = command_model(
                operation=operation,
                **parameters
            )
            
            self.logger.info(f"Command validated successfully: {operation}")
            return validated.model_dump()
            
        except ValidationError as e:
            self.logger.error(f"Command validation failed: {e}")
            raise ValueError(f"Invalid command parameters: {e}")

    def validate_parameters(self, operation: str, parameters: Dict[str, Any]) -> bool:
        """验证操作参数
        
        Args:
            operation: 操作类型
            parameters: 参数字典
            
        Returns:
            参数是否有效
        """
        self.logger.info(f"Validating parameters for {operation}")
        
        if operation not in self.SUPPORTED_OPERATIONS:
            self.logger.warning(f"Unknown operation: {operation}")
            return False
        
        try:
            command_model = self.SUPPORTED_OPERATIONS[operation]
            command_model(operation=operation, **parameters)
            return True
        except ValidationError:
            return False

    def record_execution(self, command: Dict[str, Any]):
        """记录已执行的命令
        
        Args:
            command: 执行的命令
        """
        self.executed_commands.append(command)
        self.logger.info(f"Recorded executed command: {command['operation']}")

    def get_execution_history(self) -> List[Dict[str, Any]]:
        """获取执行历史
        
        Returns:
            已执行命令的列表
        """
        return self.executed_commands.copy()

    def clear_history(self):
        """清除执行历史"""
        self.executed_commands = []
        self.logger.info("Execution history cleared")
