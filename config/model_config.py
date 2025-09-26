#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - 模型配置
统一管理所有模型配置和API设置
"""

# 支持的模型列表
SUPPORTED_MODELS = [
    "gpt-3.5-turbo",
    "gpt-4o", 
    "claude-3-7-sonnet-20250219",
    "llama-3.1-8b-instruct",
    "gemini-2.0-flash"
]

# 默认模型配置
DEFAULT_MODEL_CONFIG = {
    "test_model": "gpt-4o",
    "judge_model": "gpt-4o",  # 固定使用gpt-4o作为Judge
    "api_key": os.getenv("OPENAI_API_KEY", "YOUR_API_KEY_HERE"),
    "base_url": "https://api.nuwaapi.com/v1",
    "max_tokens": 80,
    "temperature": 0.0,
    "semaphore_limit": 50
}

# 实验特定配置
EXPERIMENT_CONFIGS = {
    "1.1_2.1": {
        "name": "充分vs不充分提示对比",
        "description": "测试充分提示和不充分提示对选择题性能的影响",
        "prompt_types": ["sufficient", "insufficient"],
        "output_folder": "experiment_data_choice_1_2"
    },
    "1.2": {
        "name": "少样本学习",
        "description": "测试少样本学习对选择题性能的影响",
        "few_shot_examples": 1,  # 示例数量
        "output_folder": "experiment_data_choice_1_2"
    },
    "2.3": {
        "name": "模糊提示",
        "description": "测试最简提示（只保留基本信息）对选择题性能的影响",
        "output_folder": "experiment_data_choice_2_3"
    },
    "2.5": {
        "name": "LLM优化提示",
        "description": "测试LLM优化的提示对选择题性能的影响",
        "output_folder": "experiment_data_choice_2_5"
    },
    "2.6": {
        "name": "多轮对话反思",
        "description": "测试多轮对话反思对选择题性能的影响",
        "output_folder": "experiment_data_choice_2_6"
    },
    "2.8": {
        "name": "从众效应",
        "description": "测试从众效应提示对选择题性能的影响",
        "output_folder": "experiment_data_choice_2_8"
    }
}

# 数据集配置
DATASET_CONFIG = {
    "mixed_450_qa": {
        "file_name": "mixed_450_qa_dataset.json",
        "description": "450个样本的混合选择题数据集",
        "question_types": ["single_choice", "multiple_choice", "no_correct_answer"],
        "sample_counts": {
            "single_choice": 150,
            "multiple_choice": 150, 
            "no_correct_answer": 150
        }
    }
}

# 评估指标配置
EVALUATION_METRICS = {
    "tfu_style": {
        "follow_rate": "单选题写对了",
        "jump_rate_no_answer": "无答案题判断对了", 
        "jump_rate_with_answer": "多选题判断对了",
        "overall_accuracy": "总体准确率"
    }
}

def get_model_config(model_name: str = None) -> dict:
    """获取模型配置"""
    config = DEFAULT_MODEL_CONFIG.copy()
    if model_name and model_name in SUPPORTED_MODELS:
        config["test_model"] = model_name
    return config

def get_experiment_config(experiment_id: str) -> dict:
    """获取实验配置"""
    if experiment_id not in EXPERIMENT_CONFIGS:
        raise ValueError(f"不支持的实验ID: {experiment_id}")
    return EXPERIMENT_CONFIGS[experiment_id]

def get_dataset_config(dataset_name: str = "mixed_450_qa") -> dict:
    """获取数据集配置"""
    if dataset_name not in DATASET_CONFIG:
        raise ValueError(f"不支持的数据集: {dataset_name}")
    return DATASET_CONFIG[dataset_name]
