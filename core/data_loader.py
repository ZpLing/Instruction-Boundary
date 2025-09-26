#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - 数据加载模块
统一的数据加载和预处理功能
"""

import json
import os
from typing import List, Dict, Any, Tuple
from .utils import validate_choice_element

class ChoiceDataLoader:
    """Choice数据加载器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.dataset_config = config.get("dataset", {})
        
    def load_dataset_config(self, config_file: str = "choice_config.json") -> Dict[str, Any]:
        """加载数据集配置文件"""
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"配置文件 {config_file} 未找到，使用默认配置")
            return {
                "datasets": {
                    "mixed_450_qa": {
                        "question_types": ["single_choice", "multiple_choice", "no_correct_answer"],
                        "description": "450个样本的混合选择题数据集",
                        "file_patterns": ["mixed_450_qa_dataset.json"],
                    }
                },
                "default_config": {
                    "question_types": ["single_choice", "multiple_choice", "no_correct_answer"],
                    "description": "默认Choice配置"
                }
            }
    
    def get_all_dataset_files(self) -> List[str]:
        """获取所有数据集文件"""
        dataset_files = []
        
        # 检查Choice格式数据集
        choice_paths = [
            'mixed_450_qa_dataset.json',
            './mixed_450_qa_dataset.json',
            'choice_toolkit/mixed_450_qa_dataset.json'
        ]
        
        for path in choice_paths:
            if os.path.exists(path):
                dataset_files.append(path)
                print(f"✅ 找到Choice格式数据集: {path}")
                break
        
        # 检查TFU格式数据集
        tfu_paths = [
            'choice_tfu_format_dataset.json',
            './choice_tfu_format_dataset.json',
            '../Choices/choice_tfu_format_dataset.json'
        ]
        
        for path in tfu_paths:
            if os.path.exists(path):
                dataset_files.append(path)
                print(f"✅ 找到TFU格式数据集: {path}")
                break
        
        if not dataset_files:
            print("❌ 未找到任何数据集文件")
        
        return dataset_files
    
    def validate_and_normalize_choice_types(self, dataset: List[Dict], expected_types: List[str]) -> List[str]:
        """验证数据集中的题目类型并返回标准化列表"""
        existing_types = set()
        for element in dataset:
            if "question_type" in element:
                existing_types.add(element["question_type"])
        
        print(f"数据集中发现的题目类型: {list(existing_types)}")
        
        if existing_types and not existing_types.issubset(set(expected_types)):
            print(f"警告: 数据集中的题目类型与预期不匹配，使用数据集中的类型")
            return list(existing_types)
        
        return expected_types
    
    def detect_dataset_format(self, dataset_file: str) -> str:
        """检测数据集格式"""
        with open(dataset_file, "r") as file:
            raw_data = json.load(file)
        
        if not raw_data:
            return "unknown"
        
        # 检查第一个样本的字段
        first_element = raw_data[0]
        
        # TFU格式特征：有Conclusion和Facts字段
        if "Conclusion" in first_element and "Facts" in first_element:
            return "tfu"
        # Choice格式特征：有question和options字段
        elif "question" in first_element and "options" in first_element:
            return "choice"
        else:
            return "unknown"
    
    def convert_tfu_to_choice_format(self, tfu_element: Dict[str, Any]) -> Dict[str, Any]:
        """将TFU格式转换为Choice格式"""
        # TFU格式已经包含options字段，直接使用
        options = tfu_element.get("options", [])
        
        # 构建Choice格式
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
            # 保留TFU原始字段用于prompt构建
            "facts": tfu_element.get("Facts", ""),
            "conclusion": tfu_element.get("Conclusion", "")
        }
        
        return choice_element
    
    def load_and_prepare_dataset(self, dataset_file: str, config: Dict[str, Any]) -> Tuple[List[Dict], List[str], str]:
        """加载和准备数据集（支持Choice和TFU格式）"""
        print(f"\n📁 加载数据集: {dataset_file}")
        
        # 检测数据集格式
        dataset_format = self.detect_dataset_format(dataset_file)
        print(f"检测到数据集格式: {dataset_format}")
        
        # 获取数据集配置
        dataset_name = dataset_file.replace('.json', '')
        dataset_config = config.get("datasets", {}).get("mixed_450_qa", config.get("default_config", {}))
        print(f"数据集配置: {dataset_config.get('description', '默认配置')}")
        
        # 加载数据
        with open(dataset_file, "r") as file:
            raw_data = json.load(file)
        
        # 根据格式处理数据
        dataset = []
        for element in raw_data:
            if dataset_format == "tfu":
                # 转换TFU格式为Choice格式
                choice_element = self.convert_tfu_to_choice_format(element)
                if validate_choice_element(choice_element):
                    dataset.append(choice_element)
            elif dataset_format == "choice":
                # 直接使用Choice格式
                if validate_choice_element(element):
                    dataset.append(element)
            else:
                print(f"⚠️ 未知数据集格式: {dataset_format}")
                continue
        
        # 验证并标准化题目类型
        question_types = dataset_config.get("question_types", ["single_choice", "multiple_choice", "no_correct_answer"])
        question_types = self.validate_and_normalize_choice_types(dataset, question_types)
        
        print(f"有效样本数: {len(dataset)}")
        print(f"最终使用的题目类型: {question_types}")
        print(f"数据集格式: {dataset_format}")
        
        return dataset, question_types, dataset_name
    
    def get_dataset_statistics(self, dataset: List[Dict]) -> Dict[str, Any]:
        """获取数据集统计信息"""
        stats = {
            "total_samples": len(dataset),
            "question_types": {},
            "dataset_sources": {},
            "num_options_distribution": {}
        }
        
        for element in dataset:
            # 统计题目类型
            q_type = element.get('question_type', 'unknown')
            stats["question_types"][q_type] = stats["question_types"].get(q_type, 0) + 1
            
            # 统计数据来源
            source = element.get('dataset_source', 'unknown')
            stats["dataset_sources"][source] = stats["dataset_sources"].get(source, 0) + 1
            
            # 统计选项数量
            num_options = len(element.get('options', []))
            stats["num_options_distribution"][num_options] = stats["num_options_distribution"].get(num_options, 0) + 1
        
        return stats
    
    def filter_dataset_by_type(self, dataset: List[Dict], question_types: List[str]) -> List[Dict]:
        """按题目类型过滤数据集"""
        filtered_dataset = []
        for element in dataset:
            if element.get('question_type') in question_types:
                filtered_dataset.append(element)
        return filtered_dataset
    
    def split_dataset_by_type(self, dataset: List[Dict]) -> Dict[str, List[Dict]]:
        """按题目类型分割数据集"""
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
