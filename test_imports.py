#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Choice Toolkit的导入和基本功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试所有模块的导入"""
    print("🧪 测试Choice Toolkit导入...")
    
    try:
        # 测试配置文件导入
        from config.model_config import get_model_config, SUPPORTED_MODELS
        print("✅ config.model_config 导入成功")
        
        from config.experiment_config import get_output_folder, get_execution_order
        print("✅ config.experiment_config 导入成功")
        
        # 测试核心模块导入
        from core.utils import validate_choice_element, extract_choice_label_by_keywords
        print("✅ core.utils 导入成功")
        
        from core.evaluator import ChoiceEvaluator
        print("✅ core.evaluator 导入成功")
        
        from core.data_loader import ChoiceDataLoader
        print("✅ core.data_loader 导入成功")
        
        # 测试实验模块导入
        from experiments.exp_1_1_2_1 import Experiment1_1_2_1
        print("✅ experiments.exp_1_1_2_1 导入成功")
        
        from experiments.exp_1_2 import Experiment1_2
        print("✅ experiments.exp_1_2 导入成功")
        
        from experiments.exp_2_3 import Experiment2_3
        print("✅ experiments.exp_2_3 导入成功")
        
        from experiments.exp_2_5 import Experiment2_5
        print("✅ experiments.exp_2_5 导入成功")
        
        from experiments.exp_2_6 import Experiment2_6
        print("✅ experiments.exp_2_6 导入成功")
        
        from experiments.exp_2_8 import Experiment2_8
        print("✅ experiments.exp_2_8 导入成功")
        
        print("\n🎉 所有模块导入成功！")
        return True
        
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_basic_functionality():
    """测试基本功能"""
    print("\n🧪 测试基本功能...")
    
    try:
        from config.model_config import get_model_config, SUPPORTED_MODELS
        from core.utils import validate_choice_element
        
        # 测试配置获取
        config = get_model_config()
        print(f"✅ 模型配置获取成功: {config['test_model']}")
        
        # 测试支持的模型
        print(f"✅ 支持的模型: {SUPPORTED_MODELS}")
        
        # 测试数据验证
        test_element = {
            "question": "测试问题",
            "options": ["选项1", "选项2", "选项3", "选项4"],
            "correct_answers": [0],
            "question_type": "single_choice"
        }
        
        is_valid = validate_choice_element(test_element)
        print(f"✅ 数据验证功能正常: {is_valid}")
        
        print("\n🎉 基本功能测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 功能测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("Choice Toolkit 导入和功能测试")
    print("=" * 60)
    
    # 测试导入
    import_success = test_imports()
    
    if import_success:
        # 测试基本功能
        functionality_success = test_basic_functionality()
        
        if functionality_success:
            print("\n🎊 所有测试通过！Choice Toolkit准备就绪！")
            return 0
        else:
            print("\n❌ 功能测试失败")
            return 1
    else:
        print("\n❌ 导入测试失败")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
