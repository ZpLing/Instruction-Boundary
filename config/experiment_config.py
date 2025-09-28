#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - 实验配置
管理实验参数和设置
"""

import os
from typing import Dict, List, Any

# 实验输出文件夹映射
EXPERIMENT_OUTPUT_FOLDERS = {
    "1.1_2.1": "experiment_data_choice_1_2",
    "1.2": "experiment_data_choice_1_2", 
    "2.3": "experiment_data_choice_2_3",
    "2.5": "experiment_data_choice_2_5",
    "2.6": "experiment_data_choice_2_6",
    "2.8": "experiment_data_choice_2_8"
}

# 实验依赖关系
EXPERIMENT_DEPENDENCIES = {
    "1.1_2.1": [],  # 基础实验，无依赖
    "1.2": [],      # 基础实验，无依赖
    "2.3": [],      # 基础实验，无依赖
    "2.5": [],      # 基础实验，无依赖
    "2.6": [],      # 基础实验，无依赖
    "2.8": []       # 基础实验，无依赖
}

# 实验执行顺序（按依赖关系排序）
EXPERIMENT_EXECUTION_ORDER = [
    "1.1_2.1",  # 充分vs不充分提示对比
    "1.2",      # 少样本学习
    "2.3",      # 模糊提示
    "2.5",      # LLM优化提示
    "2.6",      # 多轮对话反思
    "2.8"       # 从众效应
]

# 实验类型分类
EXPERIMENT_CATEGORIES = {
    "prompt_comparison": ["1.1_2.1"],  # 提示对比类
    "learning_methods": ["1.2"],       # 学习方法类
    "prompt_optimization": ["2.3", "2.5"],  # 提示优化类
    "interaction_methods": ["2.6"],     # 交互方法类
    "bias_effects": ["2.8"]            # 偏差效应类
}

# 实验参数配置
EXPERIMENT_PARAMETERS = {
    "1.1_2.1": {
        "prompt_types": ["sufficient", "insufficient"],
        "comparison_enabled": True,
        "output_files": {
            "sufficient": ["evaluation", "accuracy", "comparison"],
            "insufficient": ["evaluation", "accuracy", "comparison"]
        }
    },
    "1.2": {
        "few_shot_examples": 1,
        "output_files": {
            "few_shot": ["evaluation", "accuracy", "analysis"]
        }
    },
    "2.3": {
        "output_files": {
            "ambiguous": ["evaluation", "accuracy", "analysis"]
        }
    },
    "2.5": {
        "output_files": {
            "llm_polished": ["evaluation", "accuracy", "analysis"]
        }
    },
    "2.6": {
        "output_files": {
            "multi_turn": ["evaluation", "accuracy", "analysis"]
        }
    },
    "2.8": {
        "output_files": {
            "bandwagon": ["evaluation", "accuracy", "analysis"]
        }
    }
}

def get_output_folder(experiment_id: str) -> str:
    """获取实验输出文件夹"""
    if experiment_id not in EXPERIMENT_OUTPUT_FOLDERS:
        raise ValueError(f"不支持的实验ID: {experiment_id}")
    return EXPERIMENT_OUTPUT_FOLDERS[experiment_id]

def get_experiment_parameters(experiment_id: str) -> dict:
    """获取实验参数"""
    if experiment_id not in EXPERIMENT_PARAMETERS:
        raise ValueError(f"不支持的实验ID: {experiment_id}")
    return EXPERIMENT_PARAMETERS[experiment_id]

def get_execution_order() -> List[str]:
    """获取实验执行顺序"""
    return EXPERIMENT_EXECUTION_ORDER.copy()

def get_experiment_categories() -> Dict[str, List[str]]:
    """获取实验分类"""
    return EXPERIMENT_CATEGORIES.copy()

def create_output_directories(base_path: str = "results") -> None:
    """创建输出目录结构"""
    for folder in EXPERIMENT_OUTPUT_FOLDERS.values():
        dir_path = os.path.join(base_path, folder)
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ 创建目录: {dir_path}")

def get_experiment_dependencies(experiment_id: str) -> List[str]:
    """获取实验依赖"""
    return EXPERIMENT_DEPENDENCIES.get(experiment_id, [])

def validate_experiment_sequence(experiment_ids: List[str]) -> bool:
    """验证实验执行序列是否合理"""
    for exp_id in experiment_ids:
        dependencies = get_experiment_dependencies(exp_id)
        for dep in dependencies:
            if dep not in experiment_ids or experiment_ids.index(dep) >= experiment_ids.index(exp_id):
                return False
    return True

