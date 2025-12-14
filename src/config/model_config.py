#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - Model Configuration
Centralized management of all model configurations and API settings
"""

import os

# Supported models list
SUPPORTED_MODELS = [
    "gpt-3.5-turbo",
    "gpt-4o", 
    "claude-3-7-sonnet-20250219",
    "llama-3.1-8b-instruct",
    "gemini-2.0-flash"
]

# Default model configuration
DEFAULT_MODEL_CONFIG = {
    "test_model": "gpt-4o",
    "judge_model": "gpt-4o",  # Fixed to use gpt-4o as Judge
    "api_key": os.getenv("API_KEY", "YOUR_API_KEY_HERE"),
    "base_url": os.getenv("BASE_URL", "https://api.openai.com/v1"),
    "max_tokens": 4096,
    "temperature": 0.0,
    "semaphore_limit": 50
}

# Experiment-specific configurations
EXPERIMENT_CONFIGS = {
    "1": {
        "name": "Vanilla Scenario",
        "description": "Basic experiment scenario",
        "output_folder": "experiment_data_choice_Vanilla_Scenario"
    },
    "2": {
        "name": "Multi-turn Dialogue",
        "description": "Multi-turn dialogue experiment",
        "output_folder": "experiment_data_choice_Multi_turn_Dialogue"
    },
    "3": {
        "name": "Conformity",
        "description": "Conformity effect experiment",
        "output_folder": "experiment_data_choice_Conformity"
    },
    "4": {
        "name": "Disturbing Miscellany",
        "description": "Disturbing information experiment",
        "output_folder": "experiment_data_choice_Disturbing_Miscellany"
    },
    "5": {
        "name": "Few-shot Learning",
        "description": "Few-shot learning experiment",
        "output_folder": "experiment_data_choice_Few_shot_Learning"
    },
    "6": {
        "name": "Missing Choices",
        "description": "Missing options experiment",
        "output_folder": "experiment_data_choice_Missing_Choices"
    },
    "7": {
        "name": "Vaugeness",
        "description": "Ambiguous prompt experiment",
        "output_folder": "experiment_data_choice_Vaugeness"
    },
    "8": {
        "name": "Prompt Polishing",
        "description": "Prompt optimization experiment",
        "output_folder": "experiment_data_choice_Prompt_Polishing"
    }
}

# Dataset configuration
DATASET_CONFIG = {
    "mixed_900_qa": {
        "file_name": "mixed_900_qa_dataset.json",
        "description": "900-sample mixed multiple-choice question dataset",
        "question_types": ["single_choice", "multiple_choice", "no_correct_answer"],
        "sample_counts": {
            "single_choice": 150,
            "multiple_choice": 150, 
            "no_correct_answer": 150
        }
    }
}

# Evaluation metrics configuration
EVALUATION_METRICS = {
    "tfu_style": {
        "follow_rate": "Correct single-choice",
        "jump_rate_no_answer": "Correct no-answer judgment", 
        "jump_rate_with_answer": "Correct multiple-choice judgment",
        "overall_accuracy": "Overall accuracy"
    }
}

def get_model_config(model_name: str = None) -> dict:
    """Get model configuration"""
    config = DEFAULT_MODEL_CONFIG.copy()
    if model_name and model_name in SUPPORTED_MODELS:
        config["test_model"] = model_name
    return config

def get_experiment_config(experiment_id: str) -> dict:
    """Get experiment configuration"""
    if experiment_id not in EXPERIMENT_CONFIGS:
        raise ValueError(f"Unsupported experiment ID: {experiment_id}")

    return EXPERIMENT_CONFIGS[experiment_id]

def get_dataset_config(dataset_name: str = "mixed_900_qa") -> dict:
    """Get dataset configuration"""
    if dataset_name not in DATASET_CONFIG:
        raise ValueError(f"Unsupported dataset: {dataset_name}")
    return DATASET_CONFIG[dataset_name]
