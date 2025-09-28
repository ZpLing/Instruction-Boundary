#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - 评估模块
统一的评估指标计算和结果分析
"""

from typing import List, Dict, Any
import json
import os

class ChoiceEvaluator:
    """Choice评估器"""
    
    def __init__(self):
        pass
    
    def calculate_choice_metrics_with_tfu_style(self, results: List[Dict]) -> Dict[str, Any]:
        """计算Choice指标（学习TFU的Follow和Jump指标）"""
        
        total_count = len(results)
        
        # 统计提取方法
        extraction_method_stats = {"keyword": 0, "llm_judge": 0}
        
        # 按题目类型分组
        single_choice_results = []
        multiple_choice_results = []
        no_answer_results = []
        
        # 统计LLM输出分布
        llm_output_label_stats = {
            "0": 0, "1": 0, "2": 0, "3": 0,
            "0,1": 0, "0,2": 0, "0,3": 0, "1,2": 0, "1,3": 0, "2,3": 0,
            "NO_ANSWER": 0, "UNCLEAR": 0
        }
        
        for result in results:
            element = result['element']
            judge_eval = result['judge_evaluation']
            extraction_method = result['extraction_method']
            extracted_label = result['extracted_label']
            
            # 统计提取方法
            extraction_method_stats[extraction_method] = extraction_method_stats.get(extraction_method, 0) + 1
            
            # 统计LLM输出分布
            if extracted_label in llm_output_label_stats:
                llm_output_label_stats[extracted_label] += 1
            
            # 按题目类型分组
            q_type = element.get('question_type', 'unknown')
            if q_type == 'single_choice':
                single_choice_results.append(result)
            elif q_type == 'multiple_choice':
                multiple_choice_results.append(result)
            elif q_type == 'no_correct_answer':
                no_answer_results.append(result)
        
        # 1. Follow率：单选题写对了
        def calculate_follow_rate(single_choice_results):
            """计算Follow率：单选题写对了"""
            follow_correct = 0
            follow_total = len(single_choice_results)
            
            for result in single_choice_results:
                judge_eval = result['judge_evaluation']
                if judge_eval['is_correct']:
                    follow_correct += 1
            
            follow_rate = follow_correct / follow_total if follow_total > 0 else 0
            return follow_rate, follow_correct, follow_total
        
        follow_rate, follow_correct, follow_total = calculate_follow_rate(single_choice_results)
        
        # 2. Jump率1：四选0（无答案）判断对了
        def calculate_jump_rate_no_answer(no_answer_results):
            """计算Jump率1：四选0（无答案）判断对了"""
            jump_correct = 0
            jump_total = len(no_answer_results)
            
            for result in no_answer_results:
                judge_eval = result['judge_evaluation']
                if judge_eval['is_correct'] and judge_eval['has_no_answer']:
                    jump_correct += 1
            
            jump_rate = jump_correct / jump_total if jump_total > 0 else 0
            return jump_rate, jump_correct, jump_total
        
        jump_rate_no_answer, jump_correct_no_answer, jump_total_no_answer = calculate_jump_rate_no_answer(no_answer_results)
        
        # 3. Jump率2：多选题判断对了
        def calculate_jump_rate_with_answer(multiple_choice_results):
            """计算Jump率2：多选题判断对了"""
            jump_correct = 0
            jump_total = len(multiple_choice_results)
            
            for result in multiple_choice_results:
                judge_eval = result['judge_evaluation']
                if judge_eval['is_correct']:
                    jump_correct += 1
            
            jump_rate = jump_correct / jump_total if jump_total > 0 else 0
            return jump_rate, jump_correct, jump_total
        
        jump_rate_with_answer, jump_correct_with_answer, jump_total_with_answer = calculate_jump_rate_with_answer(multiple_choice_results)
        
        # 4. 总体准确率
        total_correct = sum(1 for result in results if result['judge_evaluation']['is_correct'])
        overall_accuracy = total_correct / total_count if total_count > 0 else 0
        
        # 5. 输出分布统计
        output_distribution = {}
        ground_truth_counts = {
            "single_choice": len(single_choice_results),
            "multiple_choice": len(multiple_choice_results), 
            "no_correct_answer": len(no_answer_results)
        }
        
        # 统计输出类型分布
        output_type_stats = {
            "single_option": 0,      # 输出单个选项
            "multiple_options": 0,   # 输出多个选项
            "no_answer": 0           # 输出No Answer（包括UNCLEAR、UNCERTAIN等）
        }
        
        for result in results:
            label = result['extracted_label']
            if label == "NO_ANSWER" or label == "UNCLEAR" or label == "UNCERTAIN" or label is None:
                output_type_stats["no_answer"] += 1
            elif "," in label:  # 包含逗号，说明是多选
                output_type_stats["multiple_options"] += 1
            else:  # 单个选项
                output_type_stats["single_option"] += 1
        
        # 按题目类型统计详细分布
        for q_type in ["single_choice", "multiple_choice", "no_correct_answer"]:
            if q_type == "single_choice":
                type_results = single_choice_results
            elif q_type == "multiple_choice":
                type_results = multiple_choice_results
            else:
                type_results = no_answer_results
            
            if type_results:
                type_outputs = {}
                for result in type_results:
                    label = result['extracted_label']
                    type_outputs[label] = type_outputs.get(label, 0) + 1
                
                total_type_samples = len(type_results)
                output_distribution[q_type] = {}
                for output_label, count in type_outputs.items():
                    ratio = count / total_type_samples if total_type_samples > 0 else 0
                    output_distribution[q_type][output_label] = {
                        "count": count,
                        "ratio": ratio,
                        "percentage": ratio * 100
                    }
        
        return {
            "method": "tfu_style_metrics",
            "overall_accuracy": overall_accuracy,
            "total_count": total_count,
            "follow_rate": follow_rate,
            "follow_correct": follow_correct,
            "follow_total": follow_total,
            "jump_rate_no_answer": jump_rate_no_answer,
            "jump_correct_no_answer": jump_correct_no_answer,
            "jump_total_no_answer": jump_total_no_answer,
            "jump_rate_with_answer": jump_rate_with_answer,
            "jump_correct_with_answer": jump_correct_with_answer,
            "jump_total_with_answer": jump_total_with_answer,
            "extraction_method_stats": extraction_method_stats,
            "llm_output_label_stats": llm_output_label_stats,
            "output_type_stats": output_type_stats,  # 新增：输出类型统计
            "output_distribution": output_distribution,
            "ground_truth_counts": ground_truth_counts
        }
    
    def save_experiment_results(self, results: List[Dict], metrics: Dict[str, Any], 
                              model_name: str, dataset_name: str, experiment_type: str,
                              output_folder: str) -> Dict[str, str]:
        """保存实验结果"""
        
        # 创建输出目录
        os.makedirs(output_folder, exist_ok=True)
        
        # 生成文件名
        clean_dataset_name = os.path.basename(dataset_name).replace('.json', '')
        
        # 保存详细结果
        evaluation_filename = os.path.join(
            output_folder, 
            f"{model_name}_{clean_dataset_name}_choice_{experiment_type}_evaluation.json"
        )
        
        with open(evaluation_filename, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # 保存准确率数据
        accuracy_filename = os.path.join(
            output_folder,
            f"{model_name}_{clean_dataset_name}_choice_{experiment_type}_accuracy.json"
        )
        
        with open(accuracy_filename, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {experiment_type}结果已保存: {evaluation_filename}")
        print(f"✅ {experiment_type}指标已保存: {accuracy_filename}")
        
        return {
            "evaluation_file": evaluation_filename,
            "accuracy_file": accuracy_filename
        }
    
    def print_experiment_summary(self, metrics: Dict[str, Any], experiment_type: str):
        """打印实验总结"""
        print(f"\n📊 {experiment_type}实验TFU风格指标:")
        print(f"   总体准确率: {metrics['overall_accuracy']:.3f} ({metrics['total_count']}个样本)")
        print(f"   Follow率: {metrics['follow_rate']:.3f} ({metrics['follow_correct']}/{metrics['follow_total']}) [单选题写对了]")
        print(f"   Jump率1: {metrics['jump_rate_no_answer']:.3f} ({metrics['jump_correct_no_answer']}/{metrics['jump_total_no_answer']}) [无答案题判断对了]")
        print(f"   Jump率2: {metrics['jump_rate_with_answer']:.3f} ({metrics['jump_correct_with_answer']}/{metrics['jump_total_with_answer']}) [多选题判断对了]")
        print(f"   标签提取方法: {metrics['extraction_method_stats']}")
        
        # 输出类型统计
        print(f"\n📈 输出类型分布 (总计{metrics['total_count']}个样本):")
        print(f"   数据集组成: {metrics['ground_truth_counts']['single_choice']}个单选题 + {metrics['ground_truth_counts']['multiple_choice']}个多选题 + {metrics['ground_truth_counts']['no_correct_answer']}个无答案题")
        output_type_stats = metrics['output_type_stats']
        total_samples = metrics['total_count']
        for output_type, count in output_type_stats.items():
            if count > 0:
                percentage = count / total_samples * 100
                type_name = {
                    "single_option": "单个选项",
                    "multiple_options": "多个选项", 
                    "no_answer": "无答案"
                }.get(output_type, output_type)
                print(f"     {type_name:>10}: {count:>3}次 ({percentage:>5.1f}%)")
        
        # 详细输出分布统计
        print(f"\n📈 详细LLM输出分布:")
        for label, count in metrics['llm_output_label_stats'].items():
            if count > 0:
                percentage = count / metrics['total_count'] * 100
                print(f"     {label:>10}: {count:>3}次 ({percentage:>5.1f}%)")
        
        # 按题目类型的输出分布
        print(f"\n📊 按题目类型的输出分布:")
        for q_type, distribution in metrics['output_distribution'].items():
            print(f"\n   {q_type}:")
            for output_label, stats in distribution.items():
                print(f"     {output_label:>10}: {stats['count']:>3}次 ({stats['percentage']:>5.1f}%)")

