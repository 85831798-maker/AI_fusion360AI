"""Fusion 360 API 客户端

封装 Fusion 360 API 调用，提供统一的接口进行模型操作。
"""

import json
import logging
from typing import Dict, Any, List, Optional
import requests
from config import FUSION_HOST, FUSION_PORT, FUSION_TIMEOUT

logger = logging.getLogger(__name__)


class FusionClient:
    """Fusion 360 API 客户端
    
    用于与 Fusion 360 进行通信，执行建模操作。
    """

    def __init__(self, host: str = FUSION_HOST, port: int = FUSION_PORT, timeout: int = FUSION_TIMEOUT):
        """初始化 Fusion 360 客户端
        
        Args:
            host: Fusion 360 服务器地址
            port: 端口号
            timeout: 请求超时时间（秒）
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.base_url = f"http://{host}:{port}/api"
        self.session = requests.Session()
        self.logger = logger

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """发送 API 请求
        
        Args:
            method: HTTP 方法 (GET, POST, PUT, DELETE)
            endpoint: API 端点
            data: 请求体数据
            
        Returns:
            API 响应数据
        """
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        try:
            if method == "GET":
                response = self.session.get(url, headers=headers, timeout=self.timeout)
            elif method == "POST":
                response = self.session.post(url, json=data, headers=headers, timeout=self.timeout)
            elif method == "PUT":
                response = self.session.put(url, json=data, headers=headers, timeout=self.timeout)
            elif method == "DELETE":
                response = self.session.delete(url, headers=headers, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            raise

    def create_document(self) -> Dict[str, Any]:
        """创建新的 Fusion 360 文档
        
        Returns:
            创建的文档信息
        """
        self.logger.info("Creating new Fusion 360 document")
        return self._request("POST", "/documents", {"type": "design"})

    def create_sketch(self, document_id: str, plane: str = "XY") -> Dict[str, Any]:
        """创建草图
        
        Args:
            document_id: 文档 ID
            plane: 草图平面 (XY, YZ, XZ)
            
        Returns:
            创建的草图信息
        """
        self.logger.info(f"Creating sketch on plane {plane}")
        data = {
            "document_id": document_id,
            "plane": plane
        }
        return self._request("POST", "/sketches", data)

    def create_box(self, document_id: str, length: float, width: float, height: float) -> Dict[str, Any]:
        """创建立方体
        
        Args:
            document_id: 文档 ID
            length: 长度
            width: 宽度
            height: 高度
            
        Returns:
            创建的立方体信息
        """
        self.logger.info(f"Creating box: {length}x{width}x{height}")
        data = {
            "document_id": document_id,
            "operation": "create_box",
            "parameters": {
                "length": length,
                "width": width,
                "height": height
            }
        }
        return self._request("POST", "/features", data)

    def create_cylinder(self, document_id: str, radius: float, height: float) -> Dict[str, Any]:
        """创建圆柱体
        
        Args:
            document_id: 文档 ID
            radius: 半径
            height: 高度
            
        Returns:
            创建的圆柱体信息
        """
        self.logger.info(f"Creating cylinder: radius={radius}, height={height}")
        data = {
            "document_id": document_id,
            "operation": "create_cylinder",
            "parameters": {
                "radius": radius,
                "height": height
            }
        }
        return self._request("POST", "/features", data)

    def create_sphere(self, document_id: str, radius: float) -> Dict[str, Any]:
        """创建球体
        
        Args:
            document_id: 文档 ID
            radius: 半径
            
        Returns:
            创建的球体信息
        """
        self.logger.info(f"Creating sphere: radius={radius}")
        data = {
            "document_id": document_id,
            "operation": "create_sphere",
            "parameters": {
                "radius": radius
            }
        }
        return self._request("POST", "/features", data)

    def apply_fillet(self, document_id: str, feature_id: str, radius: float) -> Dict[str, Any]:
        """应用圆角
        
        Args:
            document_id: 文档 ID
            feature_id: 特征 ID
            radius: 圆角半径
            
        Returns:
            操作结果
        """
        self.logger.info(f"Applying fillet: radius={radius}")
        data = {
            "document_id": document_id,
            "feature_id": feature_id,
            "operation": "fillet",
            "parameters": {
                "radius": radius
            }
        }
        return self._request("POST", "/features", data)

    def apply_chamfer(self, document_id: str, feature_id: str, size: float) -> Dict[str, Any]:
        """应用倒角
        
        Args:
            document_id: 文档 ID
            feature_id: 特征 ID
            size: 倒角大小
            
        Returns:
            操作结果
        """
        self.logger.info(f"Applying chamfer: size={size}")
        data = {
            "document_id": document_id,
            "feature_id": feature_id,
            "operation": "chamfer",
            "parameters": {
                "size": size
            }
        }
        return self._request("POST", "/features", data)

    def save_document(self, document_id: str, filename: str) -> Dict[str, Any]:
        """保存文档
        
        Args:
            document_id: 文档 ID
            filename: 保存的文件名
            
        Returns:
            保存结果
        """
        self.logger.info(f"Saving document: {filename}")
        data = {
            "document_id": document_id,
            "filename": filename
        }
        return self._request("POST", "/documents/save", data)

    def export_model(self, document_id: str, format: str = "step") -> Dict[str, Any]:
        """导出模型
        
        Args:
            document_id: 文档 ID
            format: 导出格式 (step, iges, stl, etc.)
            
        Returns:
            导出结果
        """
        self.logger.info(f"Exporting model: format={format}")
        data = {
            "document_id": document_id,
            "format": format
        }
        return self._request("POST", "/export", data)

    def get_document_info(self, document_id: str) -> Dict[str, Any]:
        """获取文档信息
        
        Args:
            document_id: 文档 ID
            
        Returns:
            文档信息
        """
        self.logger.info(f"Getting document info: {document_id}")
        return self._request("GET", f"/documents/{document_id}")
