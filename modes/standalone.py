#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fusion 360 AI Agent - 独立工具模式

作为独立脚本运行，通过 API 远程控制 Fusion 360。
"""

import sys
import json
import logging
from typing import Optional

from src.gpt_agent import GPTAgent
from src.command_parser import CommandParser
from src.fusion_client import FusionClient
from src.model_generator import ModelGenerator
from src.utils import setup_logging


def main():
    """主程序入口"""
    # 设置日志
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Fusion 360 AI Agent (Standalone Mode)")

    # 初始化组件
    gpt_agent = GPTAgent()
    parser = CommandParser()
    fusion_client = FusionClient()
    generator = ModelGenerator(fusion_client)

    # 初始化文档
    logger.info("Initializing Fusion 360 document...")
    try:
        doc_id = generator.initialize_document()
        logger.info(f"Document initialized: {doc_id}")
    except Exception as e:
        logger.error(f"Failed to initialize document: {e}")
        print(f"\n错误: 无法连接到 Fusion 360。请确保 Fusion 360 正在运行。")
        print(f"详细错误: {e}")
        return

    # 交互循环
    print("\n" + "="*60)
    print("  Fusion 360 AI Agent - 独立工具模式")
    print("="*60)
    print("\n描述你的设计需求，AI 将自动为你创建 3D 模型。")
    print("输入 'quit' 或 'exit' 退出。\n")

    while True:
        try:
            # 获取用户输入
            user_input = input("输入设计需求 (或 'quit' 退出): ").strip()

            # 检查退出命令
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n感谢使用 Fusion 360 AI Agent!")
                break

            if not user_input:
                print("请输入有效的设计需求。\n")
                continue

            print(f"\n处理中: {user_input}")
            print("-" * 60)

            # 步骤 1: 使用 GPT 解析设计需求
            logger.info(f"Parsing design request: {user_input}")
            print("[1/4] AI 解析设计需求...")
            try:
                design_command = gpt_agent.parse_design_request(user_input)
                logger.info(f"Design command: {design_command}")
                print(f"  → 命令: {design_command.get('operation')}")
            except Exception as e:
                logger.error(f"Failed to parse design request: {e}")
                print(f"✗ 解析失败: {e}\n")
                continue

            # 步骤 2: 验证命令
            print("[2/4] 验证参数...")
            try:
                validated_command = parser.parse_command(design_command)
                logger.info(f"Validated command: {validated_command}")
                print(f"  → 参数: {validated_command.get('parameters')}")
            except Exception as e:
                logger.error(f"Failed to validate command: {e}")
                print(f"✗ 验证失败: {e}\n")
                continue

            # 步骤 3: 生成模型
            print("[3/4] 生成 3D 模型...")
            try:
                feature_id = generator.generate_from_command(validated_command)
                logger.info(f"Generated feature: {feature_id}")
                print(f"  → 特征 ID: {feature_id}")
            except Exception as e:
                logger.error(f"Failed to generate model: {e}")
                print(f"✗ 生成失败: {e}\n")
                continue

            # 步骤 4: 记录执行
            print("[4/4] 保存结果...")
            parser.record_execution(validated_command)
            print(f"  → 已记录")

            # 显示成功消息
            print("\n✓ 成功! 已创建模型。\n")
            print("-" * 60 + "\n")

        except KeyboardInterrupt:
            print("\n\n程序被中断。")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"✗ 错误: {e}\n")


if __name__ == "__main__":
    main()
