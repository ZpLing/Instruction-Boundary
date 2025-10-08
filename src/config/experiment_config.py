#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - Experiment Configuration
Manage experiment parameters and settings
"""

import os
from typing import Dict, List, Any

# Experiment output folder mapping
EXPERIMENT_OUTPUT_FOLDERS = {
    "1": "experiment_data_choice_Vanilla_Scenario",
    "2": "experiment_data_choice_Multi_turn_Dialogue",
    "3": "experiment_data_choice_Conformity",
    "4": "experiment_data_choice_Disturbing_Miscellany",
    "5": "experiment_data_choice_Few_shot_Learning",
    "6": "experiment_data_choice_Missing_Choices",
    "7": "experiment_data_choice_Vaugeness",
    "8": "experiment_data_choice_Prompt_Polishing"
}

# Experiment dependencies
EXPERIMENT_DEPENDENCIES = {
    "1": [],    # Basic experiment, no dependencies
    "2": [],    # Basic experiment, no dependencies
    "3": [],    # Basic experiment, no dependencies
    "4": [],    # Basic experiment, no dependencies
    "5": [],    # Basic experiment, no dependencies
    "6": [],    # Basic experiment, no dependencies
    "7": [],    # Basic experiment, no dependencies
    "8": [],    # Basic experiment, no dependencies
}

# Experiment execution order (sorted by dependencies)
EXPERIMENT_EXECUTION_ORDER = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8"
]

# Experiment type categories
EXPERIMENT_CATEGORIES = {
    "basic_experiments": ["1", "2"],          # Basic experiments category
    "bias_effects": ["3"],                     # Bias effects category
    "information_quality": ["4"],              # Information quality category
    "learning_methods": ["5"],                 # Learning methods category
    "prompt_structure": ["6"],                 # Prompt structure category
    "prompt_optimization": ["7", "8"]         # Prompt optimization category
}

# Experiment parameter configuration
EXPERIMENT_PARAMETERS = {
    "1": {
        "prompt_types": ["sufficient"],
        "output_files": {
            "sufficient": ["evaluation", "accuracy", "analysis"]
        }
    },
    "2": {
        "output_files": {
            "multi_turn": ["evaluation", "accuracy", "analysis"]
        }
    },
    "3": {
        "output_files": {
            "conformity": ["evaluation", "accuracy", "analysis"]
        }
    },
    "4": {
        "output_files": {
            "disturbing": ["evaluation", "accuracy", "analysis"]
        }
    },
    "5": {
        "few_shot_examples": 1,
        "output_files": {
            "few_shot": ["evaluation", "accuracy", "analysis"]
        }
    },
    "6": {
        "output_files": {
            "missing_choices": ["evaluation", "accuracy", "analysis"]
        }
    },
    "7": {
        "output_files": {
            "vague": ["evaluation", "accuracy", "analysis"]
        }
    },
    "8": {
        "output_files": {
            "polished": ["evaluation", "accuracy", "analysis"]
        }
    }
}

def get_output_folder(experiment_id: str) -> str:
    """Get experiment output folder"""
    if experiment_id not in EXPERIMENT_OUTPUT_FOLDERS:
        raise ValueError(f"Unsupported experiment ID: {experiment_id}")
    return EXPERIMENT_OUTPUT_FOLDERS[experiment_id]

def get_experiment_parameters(experiment_id: str) -> dict:
    """Get experiment parameters"""
    if experiment_id not in EXPERIMENT_PARAMETERS:
        raise ValueError(f"Unsupported experiment ID: {experiment_id}")
    return EXPERIMENT_PARAMETERS[experiment_id]

def get_execution_order() -> List[str]:
    """Get experiment execution order"""
    return EXPERIMENT_EXECUTION_ORDER.copy()

def get_experiment_categories() -> Dict[str, List[str]]:
    """Get experiment categories"""
    return EXPERIMENT_CATEGORIES.copy()

def create_output_directories(experiment_ids: List[str], base_path: str = "outputs") -> None:
    folders = [EXPERIMENT_OUTPUT_FOLDERS[exp_id] for exp_id in experiment_ids if exp_id in EXPERIMENT_OUTPUT_FOLDERS]
    for folder in folders:
        dir_path = os.path.join(base_path, folder)
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Created directory: {dir_path}")

def get_experiment_dependencies(experiment_id: str) -> List[str]:
    """Get experiment dependencies"""
    return EXPERIMENT_DEPENDENCIES.get(experiment_id, [])

def validate_experiment_sequence(experiment_ids: List[str]) -> bool:
    """Validate if the experiment execution sequence is reasonable"""
    for exp_id in experiment_ids:
        dependencies = get_experiment_dependencies(exp_id)
        for dep in dependencies:
            if dep not in experiment_ids or experiment_ids.index(dep) >= experiment_ids.index(exp_id):
                return False
    return True

