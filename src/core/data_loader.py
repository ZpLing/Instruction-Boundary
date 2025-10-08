#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - Data Loading Module
Unified data loading and preprocessing functionality
"""

import json
import os
from typing import List, Dict, Any, Tuple
from .utils import validate_choice_element

class ChoiceDataLoader:
    """Choice Data Loader"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.dataset_config = config.get("dataset", {})
        
    def load_dataset_config(self, config_file: str = "choice_config.json") -> Dict[str, Any]:
        config_file = os.path.join("..", "dataset", config_file)
        """Load dataset configuration file"""
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Configuration file {config_file} not found, using default configuration")
            return {
                "datasets": {
                    "mixed_450_qa": {
                        "question_types": ["single_choice", "multiple_choice", "no_correct_answer"],
                        "description": "Mixed choice question dataset with 450 samples",
                          "file_patterns": ["mixed_450_qa_dataset.json"],
                    }
                },
                "default_config": {
                    "question_types": ["single_choice", "multiple_choice", "no_correct_answer"],
                    "description": "Default Choice configuration"
                }
            }
    
    def get_all_dataset_files(self) -> List[str]:
        """Get all dataset files"""
        dataset_files = []
        
        dataset_dir = os.path.join("..", "dataset")
        
        # Check Choice format dataset
        choice_paths = [
            os.path.join(dataset_dir, 'mixed_450_qa_dataset.json'),
            os.path.join(dataset_dir, 'choice_dataset.json'),
            os.path.join(dataset_dir, 'dataset.json')
        ]

        for path in choice_paths:
            if os.path.exists(path):
                dataset_files.append(path)
                print(f"✅ Found Choice format dataset: {os.path.basename(path)}")  # Only print filename
                break
        
        # Check TFU format dataset
        tfu_paths = [
            os.path.join(dataset_dir, 'choice_tfu_format_dataset.json'),
            os.path.join(dataset_dir, 'tfu_dataset.json'),
            os.path.join(dataset_dir, 'tfu_format.json')
        ]
        
        for path in tfu_paths:
            if os.path.exists(path):
                dataset_files.append(path)
                print(f"✅ Found TFU format dataset: {os.path.basename(path)}")  # Only print filename
                break
        
        if not dataset_files:
            print("❌ No dataset files found")
        
        return dataset_files
    
    def validate_and_normalize_choice_types(self, dataset: List[Dict], expected_types: List[str]) -> List[str]:
        """Validate question types in dataset and return normalized list"""
        existing_types = set()
        for element in dataset:
            if "question_type" in element:
                existing_types.add(element["question_type"])
        
        print(f"Question types found in dataset: {list(existing_types)}")
        
        if existing_types and not existing_types.issubset(set(expected_types)):
            print(f"Warning: Question types in dataset do not match expectations, using types from dataset")
            return list(existing_types)
        
        return expected_types
    
    def detect_dataset_format(self, dataset_file: str) -> str:
        """Detect dataset format"""
        with open(dataset_file, "r") as file:
            raw_data = json.load(file)
        
        if not raw_data:
            return "unknown"
        
        # Check fields of first sample
        first_element = raw_data[0]
        
        # TFU format feature: has Conclusion and Facts fields
        if "Conclusion" in first_element and "Facts" in first_element:
            return "tfu"
        # Choice format feature: has question and options fields
        elif "question" in first_element and "options" in first_element:
            return "choice"
        else:
            return "unknown"
    
    def convert_tfu_to_choice_format(self, tfu_element: Dict[str, Any]) -> Dict[str, Any]:
        """Convert TFU format to Choice format"""
        # TFU format already contains options field, use directly
        options = tfu_element.get("options", [])
        
        # Build Choice format
        choice_element = {
            "question": tfu_element.get("Conclusion", ""),
            "options": options,
            "correct_answers": tfu_element.get("correct_answers", []),
            "question_type": tfu_element.get("question_type", "single_choice"),
            "dataset_source": tfu_element.get("dataset_source", "unknown"),
            "original_id": tfu_element.get("original_id", ""),
            "num_options": len(options),
            "num_correct": len(tfu_element.get("correct_answers", [])),
            "proof_label": tfu_element.get("proof_label", ""),
            # Keep original TFU fields for prompt building
            "facts": tfu_element.get("Facts", ""),
            "conclusion": tfu_element.get("Conclusion", "")
        }
        
        return choice_element
    
    def load_and_prepare_dataset(self, dataset_file: str, config: Dict[str, Any]) -> Tuple[List[Dict], List[str], str]:
        """Load and prepare dataset (supports Choice and TFU formats)"""
        print(f"\n📁 Loading dataset: {dataset_file}")
        
        # Detect dataset format
        dataset_format = self.detect_dataset_format(dataset_file)
        print(f"Detected dataset format: {dataset_format}")
        
        # Get dataset configuration
        dataset_name = os.path.basename(dataset_file).replace('.json', '')
        dataset_config = config.get("datasets", {}).get("mixed_450_qa", config.get("default_config", {}))
        print(f"Dataset configuration: {dataset_config.get('description', 'Default configuration')}")
        
        # Load data
        with open(dataset_file, "r") as file:
            raw_data = json.load(file)
        
        # Process data according to format
        dataset = []
        for element in raw_data:
            if dataset_format == "tfu":
                # Convert TFU format to Choice format
                choice_element = self.convert_tfu_to_choice_format(element)
                if validate_choice_element(choice_element):
                    dataset.append(choice_element)
            elif dataset_format == "choice":
                # Use Choice format directly
                if validate_choice_element(element):
                    dataset.append(element)
            else:
                print(f"⚠️ Unknown dataset format: {dataset_format}")
                continue
        
        # Validate and normalize question types
        question_types = dataset_config.get("question_types", ["single_choice", "multiple_choice", "no_correct_answer"])
        question_types = self.validate_and_normalize_choice_types(dataset, question_types)
        
        print(f"Number of valid samples: {len(dataset)}")
        print(f"Final question types used: {question_types}")
        print(f"Dataset format: {dataset_format}")
        
        return dataset, question_types, dataset_name
    
    def get_dataset_statistics(self, dataset: List[Dict]) -> Dict[str, Any]:
        """Get dataset statistics"""
        stats = {
            "total_samples": len(dataset),
            "question_types": {},
            "dataset_sources": {},
            "num_options_distribution": {}
        }
        
        for element in dataset:
            # Count question types
            q_type = element.get('question_type', 'unknown')
            stats["question_types"][q_type] = stats["question_types"].get(q_type, 0) + 1
            
            # Count dataset sources
            source = element.get('dataset_source', 'unknown')
            stats["dataset_sources"][source] = stats["dataset_sources"].get(source, 0) + 1
            
            # Count number of options
            num_options = len(element.get('options', []))
            stats["num_options_distribution"][num_options] = stats["num_options_distribution"].get(num_options, 0) + 1
        
        return stats
    
    def filter_dataset_by_type(self, dataset: List[Dict], question_types: List[str]) -> List[Dict]:
        """Filter dataset by question type"""
        filtered_dataset = []
        for element in dataset:
            if element.get('question_type') in question_types:
                filtered_dataset.append(element)
        return filtered_dataset
    
    def split_dataset_by_type(self, dataset: List[Dict]) -> Dict[str, List[Dict]]:
        """Split dataset by question type"""
        split_data = {
            "single_choice": [],
            "multiple_choice": [],
            "no_correct_answer": []
        }
        
        for element in dataset:
            q_type = element.get('question_type', 'unknown')
            if q_type in split_data:
                split_data[q_type].append(element)
        
        return split_data
