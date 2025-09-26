#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - 测试脚本
测试工具包的基本功能
"""

import asyncio
import sys
import os
import json

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.model_config import get_model_config, SUPPORTED_MODELS
from config.experiment_config import get_output_folder, create_output_directories
from core.data_loader import ChoiceDataLoader
from core.api_client import ChoiceAPIClient
from core.evaluator import ChoiceEvaluator

async def test_basic_functionality():
    """测试基本功能"""
    
    print("Choice工具包基本功能测试")
    print("=" * 50)
    
    # 测试1：配置加载
    print("\n测试1：配置加载")
    try:
        config = get_model_config("gpt-4o")
        print(f"✅ 模型配置加载成功: {config['test_model']}")
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False
    
    # 测试2：数据加载器
    print("\n测试2：数据加载器")
    try:
        data_loader = ChoiceDataLoader(config)
        dataset_files = data_loader.get_all_dataset_files()
        print(f"✅ 数据加载器初始化成功，找到数据集: {dataset_files}")
    except Exception as e:
        print(f"❌ 数据加载器初始化失败: {e}")
        return False
    
    # 测试3：API客户端
    print("\n测试3：API客户端")
    try:
        api_client = ChoiceAPIClient(config)
        print("✅ API客户端初始化成功")
    except Exception as e:
        print(f"❌ API客户端初始化失败: {e}")
        return False
    
    # 测试4：评估器
    print("\n测试4：评估器")
    try:
        evaluator = ChoiceEvaluator()
        print("✅ 评估器初始化成功")
    except Exception as e:
        print(f"❌ 评估器初始化失败: {e}")
        return False
    
    # 测试5：输出目录创建
    print("\n测试5：输出目录创建")
    try:
        create_output_directories("test_results")
        print("✅ 输出目录创建成功")
    except Exception as e:
        print(f"❌ 输出目录创建失败: {e}")
        return False
    
    print("\n✅ 所有基本功能测试通过!")
    return True

async def test_experiment_modules():
    """测试实验模块"""
    
    print("\n实验模块测试")
    print("=" * 50)
    
    # 测试实验模块导入
    try:
        from experiments.exp_1_1_2_1 import Experiment1_1_2_1
        from experiments.exp_1_2 import Experiment1_2
        from experiments.exp_2_3 import Experiment2_3
        from experiments.exp_2_5 import Experiment2_5
        from experiments.exp_2_6 import Experiment2_6
        from experiments.exp_2_8 import Experiment2_8
        
        config = get_model_config("gpt-4o")
        
        # 测试实验模块初始化
        experiments = {
            "1.1_2.1": Experiment1_1_2_1(config),
            "1.2": Experiment1_2(config),
            "2.3": Experiment2_3(config),
            "2.5": Experiment2_5(config),
            "2.6": Experiment2_6(config),
            "2.8": Experiment2_8(config),
        }
        
        print("✅ 所有实验模块导入和初始化成功")
        
        for exp_id, exp in experiments.items():
            print(f"   - 实验 {exp_id}: {type(exp).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ 实验模块测试失败: {e}")
        return False

def test_configuration():
    """测试配置系统"""
    
    print("\n配置系统测试")
    print("=" * 50)
    
    try:
        # 测试模型配置
        for model in SUPPORTED_MODELS:
            config = get_model_config(model)
            assert config['test_model'] == model
            print(f"✅ 模型 {model} 配置正确")
        
        # 测试实验配置
        from config.experiment_config import get_output_folder, get_execution_order
        
        execution_order = get_execution_order()
        print(f"✅ 实验执行顺序: {execution_order}")
        
        for exp_id in execution_order:
            folder = get_output_folder(exp_id)
            print(f"   - 实验 {exp_id}: 输出文件夹 {folder}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置系统测试失败: {e}")
        return False

async def main():
    """主测试函数"""
    
    print("Choice工具包完整测试")
    print("=" * 60)
    
    # 运行所有测试
    tests = [
        ("基本功能测试", test_basic_functionality()),
        ("实验模块测试", test_experiment_modules()),
        ("配置系统测试", test_configuration()),
    ]
    
    results = []
    for test_name, test_coro in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if asyncio.iscoroutine(test_coro):
                result = await test_coro
            else:
                result = test_coro
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 执行失败: {e}")
            results.append((test_name, False))
    
    # 总结测试结果
    print(f"\n{'='*60}")
    print("测试结果总结")
    print(f"{'='*60}")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name:<20}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试通过! Choice工具包准备就绪!")
        return 0
    else:
        print("⚠️  部分测试失败，请检查配置")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
