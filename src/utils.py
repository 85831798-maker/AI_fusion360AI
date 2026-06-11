"""工具函数

提供日志、错误处理等通用工具。
"""

import logging
import logging.handlers
import os
from config import LOG_LEVEL, LOG_FILE


def setup_logging():
    """设置日志配置"""
    # 创建日志目录
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 创建日志记录器
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # 文件处理器
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(getattr(logging, LOG_LEVEL))
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    
    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def convert_unit(value: float, from_unit: str, to_unit: str) -> float:
    """单位转换
    
    Args:
        value: 数值
        from_unit: 源单位 (mm, cm, inch)
        to_unit: 目标单位
        
    Returns:
        转换后的数值
    """
    conversion_rates = {
        "mm": 1.0,
        "cm": 10.0,
        "inch": 25.4,
    }
    
    if from_unit not in conversion_rates or to_unit not in conversion_rates:
        raise ValueError(f"Unsupported unit: {from_unit} or {to_unit}")
    
    return value * conversion_rates[from_unit] / conversion_rates[to_unit]


def validate_dimensions(length: float, width: float, height: float, min_value: float = 0.1) -> bool:
    """验证尺寸参数
    
    Args:
        length: 长度
        width: 宽度
        height: 高度
        min_value: 最小值
        
    Returns:
        尺寸是否有效
    """
    return length >= min_value and width >= min_value and height >= min_value


def validate_radius(radius: float, min_value: float = 0.1) -> bool:
    """验证半径参数
    
    Args:
        radius: 半径
        min_value: 最小值
        
    Returns:
        半径是否有效
    """
    return radius >= min_value
