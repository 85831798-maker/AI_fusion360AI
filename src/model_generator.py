"""3D 模型生成器

根据设计命令生成 3D 模型。
"""

import logging
from typing import Dict, Any, Optional
from src.fusion_client import FusionClient

logger = logging.getLogger(__name__)


class ModelGenerator:
    """3D 模型生成器
    
    根据设计命令在 Fusion 360 中生成模型。
    """

    def __init__(self, fusion_client: FusionClient):
        """初始化模型生成器
        
        Args:
            fusion_client: Fusion 360 客户端实例
        """
        self.fusion_client = fusion_client
        self.logger = logger
        self.document_id: Optional[str] = None
        self.features: Dict[str, str] = {}  # 特征 ID 映射

    def initialize_document(self) -> str:
        """初始化新的 Fusion 360 文档
        
        Returns:
            文档 ID
        """
        self.logger.info("Initializing new Fusion 360 document")
        result = self.fusion_client.create_document()
        self.document_id = result.get("id")
        self.logger.info(f"Document created: {self.document_id}")
        return self.document_id

    def generate_from_command(self, command: Dict[str, Any]) -> str:
        """根据命令生成模型
        
        Args:
            command: 设计命令
            
        Returns:
            特征 ID
        """
        if not self.document_id:
            self.initialize_document()
        
        operation = command.get("operation")
        self.logger.info(f"Generating model from command: {operation}")
        
        if operation == "create_box":
            return self._create_box(command)
        elif operation == "create_cylinder":
            return self._create_cylinder(command)
        elif operation == "create_sphere":
            return self._create_sphere(command)
        else:
            raise ValueError(f"Unsupported operation: {operation}")

    def _create_box(self, command: Dict[str, Any]) -> str:
        """创建立方体
        
        Args:
            command: 命令字典
            
        Returns:
            特征 ID
        """
        params = command.get("parameters", {})
        length = params.get("length")
        width = params.get("width")
        height = params.get("height")
        
        self.logger.info(f"Creating box: {length}x{width}x{height}")
        result = self.fusion_client.create_box(self.document_id, length, width, height)
        feature_id = result.get("id")
        self.features["box"] = feature_id
        return feature_id

    def _create_cylinder(self, command: Dict[str, Any]) -> str:
        """创建圆柱体
        
        Args:
            command: 命令字典
            
        Returns:
            特征 ID
        """
        params = command.get("parameters", {})
        radius = params.get("radius")
        height = params.get("height")
        
        self.logger.info(f"Creating cylinder: radius={radius}, height={height}")
        result = self.fusion_client.create_cylinder(self.document_id, radius, height)
        feature_id = result.get("id")
        self.features["cylinder"] = feature_id
        return feature_id

    def _create_sphere(self, command: Dict[str, Any]) -> str:
        """创建球体
        
        Args:
            command: 命令字典
            
        Returns:
            特征 ID
        """
        params = command.get("parameters", {})
        radius = params.get("radius")
        
        self.logger.info(f"Creating sphere: radius={radius}")
        result = self.fusion_client.create_sphere(self.document_id, radius)
        feature_id = result.get("id")
        self.features["sphere"] = feature_id
        return feature_id

    def apply_fillet(self, radius: float, feature_name: str = "box") -> str:
        """应用圆角
        
        Args:
            radius: 圆角半径
            feature_name: 要应用圆角的特征名称
            
        Returns:
            特征 ID
        """
        feature_id = self.features.get(feature_name)
        if not feature_id:
            raise ValueError(f"Feature not found: {feature_name}")
        
        self.logger.info(f"Applying fillet: radius={radius}")
        result = self.fusion_client.apply_fillet(self.document_id, feature_id, radius)
        return result.get("id")

    def apply_chamfer(self, size: float, feature_name: str = "box") -> str:
        """应用倒角
        
        Args:
            size: 倒角大小
            feature_name: 要应用倒角的特征名称
            
        Returns:
            特征 ID
        """
        feature_id = self.features.get(feature_name)
        if not feature_id:
            raise ValueError(f"Feature not found: {feature_name}")
        
        self.logger.info(f"Applying chamfer: size={size}")
        result = self.fusion_client.apply_chamfer(self.document_id, feature_id, size)
        return result.get("id")

    def save_model(self, filename: str) -> Dict[str, Any]:
        """保存模型
        
        Args:
            filename: 文件名
            
        Returns:
            保存结果
        """
        if not self.document_id:
            raise ValueError("No document to save")
        
        self.logger.info(f"Saving model: {filename}")
        return self.fusion_client.save_document(self.document_id, filename)

    def export_model(self, format: str = "step") -> Dict[str, Any]:
        """导出模型
        
        Args:
            format: 导出格式
            
        Returns:
            导出结果
        """
        if not self.document_id:
            raise ValueError("No document to export")
        
        self.logger.info(f"Exporting model: format={format}")
        return self.fusion_client.export_model(self.document_id, format)

    def get_features(self) -> Dict[str, str]:
        """获取已创建的特征
        
        Returns:
            特征字典
        """
        return self.features.copy()
