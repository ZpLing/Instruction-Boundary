#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - Evaluation Module
Unified evaluation metrics calculation and result analysis
"""

from typing import List, Dict, Any
import json
import os

class ChoiceEvaluator:
    """Choice Evaluator"""
    
    def __init__(self):
        pass
    
    def calculate_choice_metrics_with_tfu_style(self, results: List[Dict]) -> Dict[str, Any]:
        """Calculate Choice metrics (following TFU's Follow and Jump metrics style)"""
        
        total_count = len(results)
        
        # Statistics for extraction methods
        extraction_method_stats = {"keyword": 0, "llm_judge": 0}
        
        # Group by question type
        single_choice_results = []
        multiple_choice_results = []
        no_answer_results = []
        
        # Statistics for LLM output distribution
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
            
            # Statistics for extraction methods
            extraction_method_stats[extraction_method] = extraction_method_stats.get(extraction_method, 0) + 1
            
            # Statistics for LLM output distribution
            if extracted_label in llm_output_label_stats:
                llm_output_label_stats[extracted_label] += 1
            
            # Group by question type
            q_type = element.get('question_type', 'unknown')
            if q_type == 'single_choice':
                single_choice_results.append(result)
            elif q_type == 'multiple_choice':
                multiple_choice_results.append(result)
            elif q_type == 'no_correct_answer':
                no_answer_results.append(result)
        
        # 1. Follow rate: Correctly answered single-choice questions
        def calculate_follow_rate(single_choice_results):
            """Calculate Follow rate: Correctly answered single-choice questions"""
            follow_correct = 0
            follow_total = len(single_choice_results)
            
            for result in single_choice_results:
                judge_eval = result['judge_evaluation']
                if judge_eval['is_correct']:
                    follow_correct += 1
            
            follow_rate = follow_correct / follow_total if follow_total > 0 else 0
            return follow_rate, follow_correct, follow_total
        
        follow_rate, follow_correct, follow_total = calculate_follow_rate(single_choice_results)
        
        # 2. Jump rate 1: Correctly identified questions with no correct answer
        def calculate_jump_rate_no_answer(no_answer_results):
            """Calculate Jump rate 1: Correctly identified questions with no correct answer"""
            jump_correct = 0
            jump_total = len(no_answer_results)
            
            for result in no_answer_results:
                judge_eval = result['judge_evaluation']
                if judge_eval['is_correct'] and judge_eval['has_no_answer']:
                    jump_correct += 1
            
            jump_rate = jump_correct / jump_total if jump_total > 0 else 0
            return jump_rate, jump_correct, jump_total
        
        jump_rate_no_answer, jump_correct_no_answer, jump_total_no_answer = calculate_jump_rate_no_answer(no_answer_results)
        
        # 3. Jump rate 2: Correctly answered multiple-choice questions
        def calculate_jump_rate_with_answer(multiple_choice_results):
            """Calculate Jump rate 2: Correctly answered multiple-choice questions"""
            jump_correct = 0
            jump_total = len(multiple_choice_results)
            
            for result in multiple_choice_results:
                judge_eval = result['judge_evaluation']
                if judge_eval['is_correct']:
                    jump_correct += 1
            
            jump_rate = jump_correct / jump_total if jump_total > 0 else 0
            return jump_rate, jump_correct, jump_total
        
        jump_rate_with_answer, jump_correct_with_answer, jump_total_with_answer = calculate_jump_rate_with_answer(multiple_choice_results)
        
        # 4. Overall accuracy
        total_correct = sum(1 for result in results if result['judge_evaluation']['is_correct'])
        overall_accuracy = total_correct / total_count if total_count > 0 else 0
        
        # 5. Output distribution statistics
        output_distribution = {}
        ground_truth_counts = {
            "single_choice": len(single_choice_results),
            "multiple_choice": len(multiple_choice_results), 
            "no_correct_answer": len(no_answer_results)
        }
        
        # Statistics for output type distribution
        output_type_stats = {
            "single_option": 0,      # Single option output
            "multiple_options": 0,   # Multiple options output
            "no_answer": 0           # No answer output (including UNCLEAR, UNCERTAIN, etc.)
        }
        
        for result in results:
            label = result['extracted_label']
            if label == "NO_ANSWER" or label == "UNCLEAR" or label == "UNCERTAIN" or label is None:
                output_type_stats["no_answer"] += 1
            elif "," in label:  # Contains comma, indicates multiple choices
                output_type_stats["multiple_options"] += 1
            else:  # Single option
                output_type_stats["single_option"] += 1
        
        # Detailed distribution by question type
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
            "output_type_stats": output_type_stats,  # New: Output type statistics
            "output_distribution": output_distribution,
            "ground_truth_counts": ground_truth_counts
        }
    
    def save_experiment_results(self, results: List[Dict], metrics: Dict[str, Any], 
                              model_name: str, dataset_name: str, experiment_type: str,
                              output_folder: str) -> Dict[str, str]:
        """Save experiment results"""
        
        # Create output directory
        os.makedirs(output_folder, exist_ok=True)
        
        # Generate filename
        clean_dataset_name = os.path.basename(dataset_name).replace('.json', '')
        
        # Save detailed results
        evaluation_filename = os.path.join(
            output_folder, 
            f"{model_name}_{clean_dataset_name}_choice_{experiment_type}_evaluation.json"
        )
        
        with open(evaluation_filename, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Save accuracy data
        accuracy_filename = os.path.join(
            output_folder,
            f"{model_name}_{clean_dataset_name}_choice_{experiment_type}_accuracy.json"
        )
        
        with open(accuracy_filename, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {experiment_type} results saved: {evaluation_filename}")
        print(f"✅ {experiment_type} metrics saved: {accuracy_filename}")
        
        return {
            "evaluation_file": evaluation_filename,
            "accuracy_file": accuracy_filename
        }
    
    def print_experiment_summary(self, metrics: Dict[str, Any], experiment_type: str):
        """Print experiment summary"""
        print(f"\n📊 {experiment_type} Experiment TFU-style Metrics:")
        print(f"   Overall accuracy: {metrics['overall_accuracy']:.3f} ({metrics['total_count']} samples)")
        print(f"   Follow rate: {metrics['follow_rate']:.3f} ({metrics['follow_correct']}/{metrics['follow_total']}) [Correct single-choice]")
        print(f"   Jump rate 1: {metrics['jump_rate_no_answer']:.3f} ({metrics['jump_correct_no_answer']}/{metrics['jump_total_no_answer']}) [Correctly identified no answer]")
        print(f"   Jump rate 2: {metrics['jump_rate_with_answer']:.3f} ({metrics['jump_correct_with_answer']}/{metrics['jump_total_with_answer']}) [Correct multiple-choice]")
        print(f"   Label extraction methods: {metrics['extraction_method_stats']}")
        
        # Output type statistics
        print(f"\n📈 Output type distribution (Total {metrics['total_count']} samples):")
        print(f"   Dataset composition: {metrics['ground_truth_counts']['single_choice']} single-choice + {metrics['ground_truth_counts']['multiple_choice']} multiple-choice + {metrics['ground_truth_counts']['no_correct_answer']} no-answer questions")
        output_type_stats = metrics['output_type_stats']
        total_samples = metrics['total_count']
        for output_type, count in output_type_stats.items():
            if count > 0:
                percentage = count / total_samples * 100
                type_name = {
                    "single_option": "Single option",
                    "multiple_options": "Multiple options", 
                    "no_answer": "No answer"
                }.get(output_type, output_type)
                print(f"     {type_name:>10}: {count:>3} times ({percentage:>5.1f}%)")
        
        # Detailed LLM output distribution
        print(f"\n📈 Detailed LLM output distribution:")
        for label, count in metrics['llm_output_label_stats'].items():
            if count > 0:
                percentage = count / metrics['total_count'] * 100
                print(f"     {label:>10}: {count:>3} times ({percentage:>5.1f}%)")
        
        # Output distribution by question type
        print(f"\n📊 Output distribution by question type:")
        for q_type, distribution in metrics['output_distribution'].items():
            print(f"\n   {q_type}:")
            for output_label, stats in distribution.items():
                print(f"     {output_label:>10}: {stats['count']:>3} times ({stats['percentage']:>5.1f}%)")

