#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - 使用示例
演示如何使用Choice实验工具包
"""

import asyncio
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import ChoiceToolkit

async def example_usage():
    """使用示例"""
    
    print("Choice实验工具包使用示例")
    print("=" * 50)
    
    # 创建工具包实例
    toolkit = ChoiceToolkit(model_name="gpt-4o")
    
    # 示例1：运行单个实验
    print("\n示例1：运行单个实验 (1.1_2.1)")
    try:
        results = await toolkit.run_experiments(["1.1_2.1"])
        print("✅ 实验1.1_2.1完成")
    except Exception as e:
        print(f"❌ 实验失败: {e}")
    
    # 示例2：运行多个实验
    print("\n示例2：运行多个实验 (1.2, 2.3)")
    try:
        results = await toolkit.run_experiments(["1.2", "2.3"])
        print("✅ 多个实验完成")
    except Exception as e:
        print(f"❌ 实验失败: {e}")
    
    # 示例3：运行所有实验
    print("\n示例3：运行所有实验")
    try:
        results = await toolkit.run_experiments(["1.1_2.1", "1.2", "2.3", "2.5", "2.6", "2.8"])
        print("✅ 所有实验完成")
    except Exception as e:
        print(f"❌ 实验失败: {e}")

if __name__ == "__main__":
    asyncio.run(example_usage())
