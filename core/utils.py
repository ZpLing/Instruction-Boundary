#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - 工具函数
通用的工具函数和验证器
"""

import re
from typing import Dict, Any, List, Optional

def validate_choice_element(element: Dict[str, Any]) -> bool:
    """验证Choice元素是否有效"""
    required_fields = ['question', 'options']
    return all(field in element for field in required_fields)

def extract_choice_label_by_keywords(answer_text: str) -> Optional[str]:
    """使用关键词匹配提取Choice标签"""
    answer_lower = answer_text.lower().strip()
    
    # 先检查多选答案模式（优先级更高）
    multiple_patterns_with_space = [
        "0, 1", "0, 2", "0, 3", "1, 2", "1, 3", "2, 3"
    ]
    
    for pattern in multiple_patterns_with_space:
        if pattern in answer_lower:
            return pattern.replace(" ", "")
    
    # 再检查不带空格的格式
    multiple_patterns_no_space = [
        "0,1", "0,2", "0,3", "1,2", "1,3", "2,3"
    ]
    
    for pattern in multiple_patterns_no_space:
        if pattern in answer_lower:
            return pattern
    
    # 检查and格式
    and_patterns = [
        "0 and 1", "0 and 2", "0 and 3", "1 and 2", "1 and 3", "2 and 3"
    ]
    
    for pattern in and_patterns:
        if pattern in answer_lower:
            return pattern.replace(" ", "").replace("and", ",")
    
    # 使用正则表达式提取数字选项（更宽松的匹配）
    numbers = re.findall(r'\b[0-3]\b', answer_text)
    if numbers:
        # 去重并排序
        unique_numbers = sorted(list(set([int(n) for n in numbers if n.isdigit()])))
        if len(unique_numbers) == 1:
            return str(unique_numbers[0])
        elif len(unique_numbers) > 1:
            return ",".join(map(str, unique_numbers))
    
    # 然后检查单选数字（更宽松的匹配）
    if (answer_text.startswith("0") or answer_text.strip() == "0" or 
        "answer: 0" in answer_lower or "choice 0" in answer_lower or
        "option 0" in answer_lower or "0." in answer_text[:10] or
        "the answer is 0" in answer_lower or "i choose 0" in answer_lower):
        return "0"
    elif (answer_text.startswith("1") or answer_text.strip() == "1" or 
          "answer: 1" in answer_lower or "choice 1" in answer_lower or
          "option 1" in answer_lower or "1." in answer_text[:10] or
          "the answer is 1" in answer_lower or "i choose 1" in answer_lower):
        return "1"
    elif (answer_text.startswith("2") or answer_text.strip() == "2" or 
          "answer: 2" in answer_lower or "choice 2" in answer_lower or
          "option 2" in answer_lower or "2." in answer_text[:10] or
          "the answer is 2" in answer_lower or "i choose 2" in answer_lower):
        return "2"
    elif (answer_text.startswith("3") or answer_text.strip() == "3" or 
          "answer: 3" in answer_lower or "choice 3" in answer_lower or
          "option 3" in answer_lower or "3." in answer_text[:10] or
          "the answer is 3" in answer_lower or "i choose 3" in answer_lower):
        return "3"
    
    # 检查无答案关键词
    no_answer_keywords = ["no correct answer", "no correct option", "none of the above",
                         "not applicable", "insufficient information", "cannot determine",
                         "no good advice", "all options are wrong", "all options are incorrect",
                         "none", "no answer", "all wrong", "all incorrect", "no valid answer",
                         "there is no correct answer", "none of these", "all are incorrect"]
    
    for keyword in no_answer_keywords:
        if keyword in answer_lower:
            return "NO_ANSWER"
    
    # 检查不确定性关键词（统一归类为NO_ANSWER）
    uncertainty_keywords = ["uncertain", "unsure", "unclear", "ambiguous", "difficult to determine",
                           "hard to say", "not sure", "cannot be certain", "inconclusive",
                           "i'm not sure", "it's unclear", "cannot determine"]
    
    for keyword in uncertainty_keywords:
        if keyword in answer_lower:
            return "NO_ANSWER"  # 统一归类为NO_ANSWER
    
    # 无法识别
    return None

def improved_choice_judge_logic(model_response: str, ground_truth: List[int]) -> Dict[str, Any]:
    """改进的Choice judging逻辑：直接分析模型回答"""
    
    # 提取模型回答中的选项
    model_response_lower = model_response.lower().strip()
    
    # 检查是否明确选择了选项
    explicit_choice = False
    predicted_answers = []
    
    # 首先检查是否包含不确定词汇
    uncertain_keywords = [
        "cannot", "unable", "insufficient", "ambiguous", "unclear", "uncertain",
        "unsure", "difficult", "hard to", "not sure", "don't know", "unclear"
    ]
    
    has_uncertainty = any(keyword in model_response_lower for keyword in uncertain_keywords)
    
    # 检查无答案关键词
    no_answer_keywords = [
        "no correct answer", "no correct option", "none of the above",
        "not applicable", "all options are wrong", "all wrong", "none"
    ]
    
    has_no_answer = any(keyword in model_response_lower for keyword in no_answer_keywords)
    
    # 将所有"无答案"情况统一处理
    if has_no_answer or has_uncertainty:
        predicted_answers = []
        explicit_choice = True
        has_no_answer = True  # 将uncertainty也视为no_answer
        has_uncertainty = False  # 统一为no_answer，不再区分uncertainty
    else:
        # 提取数字选项 - 改进逻辑
        numbers = re.findall(r'\b[0-3]\b', model_response)
        if numbers:
            try:
                # 只保留有效的选项编号 (0-3)
                valid_numbers = [int(num) for num in numbers if num.isdigit() and 0 <= int(num) <= 3]
                predicted_answers = list(set(valid_numbers))  # 去重
                predicted_answers = sorted(predicted_answers)
                explicit_choice = True
                
                # 如果提取到的选项为空，说明没有有效选项
                if not predicted_answers:
                    explicit_choice = False
            except:
                predicted_answers = []
                explicit_choice = False
        else:
            # 如果没有找到0-3的数字，尝试其他格式
            # 检查是否有其他数字（可能是无效的）
            all_numbers = re.findall(r'\b\d+\b', model_response)
            if all_numbers:
                # 如果有数字但都不在0-3范围内，说明模型回答有问题
                predicted_answers = []
                explicit_choice = False
    
    # 判断正确性
    is_correct = False
    if explicit_choice:
        is_correct = sorted(predicted_answers) == sorted(ground_truth)
    
    return {
        "is_correct": is_correct,
        "predicted_answers": predicted_answers,
        "ground_truth": ground_truth,
        "explicit_choice": explicit_choice,
        "has_uncertainty": has_uncertainty,
        "has_no_answer": has_no_answer,
        "raw_response": model_response
    }

def format_experiment_results(results: List[Dict], experiment_type: str) -> Dict[str, Any]:
    """格式化实验结果"""
    formatted_results = {
        "experiment_type": experiment_type,
        "total_samples": len(results),
        "results": results
    }
    
    return formatted_results

def create_output_filename(model_name: str, dataset_name: str, experiment_type: str, 
                          file_type: str, output_folder: str) -> str:
    """创建输出文件名"""
    import os
    
    # 清理数据集名称
    clean_dataset_name = os.path.basename(dataset_name).replace('.json', '')
    
    # 创建文件名
    filename = f"{model_name}_{clean_dataset_name}_choice_{experiment_type}_{file_type}.json"
    
    # 确保输出目录存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 返回完整路径
    return os.path.join(output_folder, filename)

def print_experiment_summary(metrics: Dict[str, Any], experiment_type: str):
    """打印实验总结"""
    print(f"\n📊 {experiment_type}实验TFU风格指标:")
    print(f"   总体准确率: {metrics['overall_accuracy']:.3f} ({metrics['total_count']}个样本)")
    print(f"   Follow率: {metrics['follow_rate']:.3f} ({metrics['follow_correct']}/{metrics['follow_total']}) [单选题写对了]")
    print(f"   Jump率1: {metrics['jump_rate_no_answer']:.3f} ({metrics['jump_correct_no_answer']}/{metrics['jump_total_no_answer']}) [无答案题判断对了]")
    print(f"   Jump率2: {metrics['jump_rate_with_answer']:.3f} ({metrics['jump_correct_with_answer']}/{metrics['jump_total_with_answer']}) [多选题判断对了]")
    print(f"   标签提取方法: {metrics['extraction_method_stats']}")

