#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice实验1.1_2.1：充分与不充分提示对比实验
对应TFU的exp_TFU_1.1_2.1.py
"""

from typing import Dict, Any, List
from ..core.api_client import ChoiceAPIClient
from ..core.evaluator import ChoiceEvaluator
from ..core.utils import create_output_filename

class Experiment1_1_2_1:
    """实验1.1_2.1：充分与不充分提示对比实验"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_client = ChoiceAPIClient(config)
        self.evaluator = ChoiceEvaluator()
    
    def build_sufficient_prompt(self, element: Dict[str, Any]) -> str:
        """构建充分提示的Choice prompt"""
        
        question = element['question']
        options = element['options']
        passage = element.get('passage_text', '')
        
        # 构建选项文本
        options_text = "\n".join(options)
        
        # 构建Facts部分（对应TFU的Facts）
        facts_part = ""
        if passage and passage.strip():
            facts_part = f"Facts: {passage}\n"
        
        # 完整的充分提示（学习TFU的sufficient结构）
        prompt = f"""Question: {question}
{facts_part}Task: Based on the given information, determine which option(s) are correct for the question.
Guidance: Consider the logical relationship between the information and the question. Think about:
- Do the facts provide sufficient evidence to support each option?
- Do the facts contradict or refute any option?
- Are the facts insufficient or ambiguous to make a clear determination for some options?
Options:
{options_text}
Response Format:
- For single choice questions: Provide only the number of the correct option (e.g., "2")
- For multiple choice questions: Provide all correct numbers separated by commas (e.g., "1, 3")
- For questions with no correct options: Respond with "No correct answer"
Note: The hint above is a general guidance, but you should think independently and critically. Consider all possible interpretations and edge cases. Please respond with the option number(s).

Answer:"""

        return prompt
    
    def build_insufficient_prompt(self, element: Dict[str, Any]) -> str:
        """构建不充分提示的Choice prompt"""
        
        question = element['question']
        options = element['options']
        passage = element.get('passage_text', '')
        
        # 构建选项文本
        options_text = "\n".join(options)
        
        # 构建Facts部分（对应TFU的Facts）
        facts_part = ""
        if passage and passage.strip():
            facts_part = f"Facts: {passage}\n"
        
        # 不充分提示（去掉多选题说明，只保留单选题和全部错误两种情况）
        prompt = f"""Question: {question}
{facts_part}Task: Based on the given information, determine which option(s) are correct for the question.
Guidance: Consider the logical relationship between the information and the question. Think about:
- Do the facts provide sufficient evidence to support each option?
- Do the facts contradict or refute any option?
- Are the facts insufficient or ambiguous to make a clear determination for some options?
Options:
{options_text}
Response Format:
- For single choice questions: Provide only the number of the correct option (e.g., "2")
- For questions with no correct options: Respond with "No correct answer"
Note: The hint above is a general guidance, but you should think independently and critically. Consider all possible interpretations and edge cases. Please respond with the option number(s).


Answer:"""

        return prompt
    
    async def run_sufficient_experiment(self, dataset: List[Dict]) -> List[Dict]:
        """运行充分提示实验"""
        print(f"\n🔄 运行充分提示实验...")
        return await self.api_client.process_dataset(dataset, self.build_sufficient_prompt, "sufficient")
    
    async def run_insufficient_experiment(self, dataset: List[Dict]) -> List[Dict]:
        """运行不充分提示实验"""
        print(f"\n🔄 运行不充分提示实验...")
        return await self.api_client.process_dataset(dataset, self.build_insufficient_prompt, "insufficient")
    
    def create_comparison_summary(self, sufficient_metrics: Dict, insufficient_metrics: Dict, 
                                model_name: str, dataset_name: str, output_folder: str) -> Dict[str, Any]:
        """创建对比总结"""
        
        comparison = {
            "model": model_name,
            "dataset": dataset_name,
            "experiment_type": "sufficient_vs_insufficient_choice_tfu_style",
            "sufficient_prompt": {
                "overall_accuracy": sufficient_metrics["overall_accuracy"],
                "follow_rate": sufficient_metrics["follow_rate"],
                "jump_rate_no_answer": sufficient_metrics["jump_rate_no_answer"],
                "jump_rate_with_answer": sufficient_metrics["jump_rate_with_answer"],
                "total_count": sufficient_metrics["total_count"]
            },
            "insufficient_prompt": {
                "overall_accuracy": insufficient_metrics["overall_accuracy"],
                "follow_rate": insufficient_metrics["follow_rate"],
                "jump_rate_no_answer": insufficient_metrics["jump_rate_no_answer"],
                "jump_rate_with_answer": insufficient_metrics["jump_rate_with_answer"],
                "total_count": insufficient_metrics["total_count"]
            },
            "performance_difference": {
                "overall_accuracy": sufficient_metrics["overall_accuracy"] - insufficient_metrics["overall_accuracy"],
                "follow_rate": sufficient_metrics["follow_rate"] - insufficient_metrics["follow_rate"],
                "jump_rate_no_answer": sufficient_metrics["jump_rate_no_answer"] - insufficient_metrics["jump_rate_no_answer"],
                "jump_rate_with_answer": sufficient_metrics["jump_rate_with_answer"] - insufficient_metrics["jump_rate_with_answer"]
            }
        }
        
        # 保存对比结果
        import json
        import os
        
        clean_dataset_name = os.path.basename(dataset_name).replace('.json', '')
        comparison_filename = os.path.join(
            output_folder,
            f"{model_name}_{clean_dataset_name}_choice_sufficient_vs_insufficient_tfu_comparison.json"
        )
        
        with open(comparison_filename, "w", encoding="utf-8") as f:
            json.dump(comparison, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 TFU风格对比总结已保存: {comparison_filename}")
        print(f"   充分提示 vs 不充分提示:")
        print(f"     总体准确率: {sufficient_metrics['overall_accuracy']:.3f} vs {insufficient_metrics['overall_accuracy']:.3f} (差异: {comparison['performance_difference']['overall_accuracy']:+.3f})")
        print(f"     Follow率: {sufficient_metrics['follow_rate']:.3f} vs {insufficient_metrics['follow_rate']:.3f} (差异: {comparison['performance_difference']['follow_rate']:+.3f})")
        print(f"     Jump率1: {sufficient_metrics['jump_rate_no_answer']:.3f} vs {insufficient_metrics['jump_rate_no_answer']:.3f} (差异: {comparison['performance_difference']['jump_rate_no_answer']:+.3f})")
        print(f"     Jump率2: {sufficient_metrics['jump_rate_with_answer']:.3f} vs {insufficient_metrics['jump_rate_with_answer']:.3f} (差异: {comparison['performance_difference']['jump_rate_with_answer']:+.3f})")
        
        # 输出分布对比
        print(f"\n📈 输出分布对比:")
        print(f"   充分提示输出分布:")
        for label, count in sufficient_metrics['llm_output_label_stats'].items():
            if count > 0:
                percentage = count / sufficient_metrics['total_count'] * 100
                print(f"     {label:>10}: {count:>3}次 ({percentage:>5.1f}%)")
        
        print(f"\n   不充分提示输出分布:")
        for label, count in insufficient_metrics['llm_output_label_stats'].items():
            if count > 0:
                percentage = count / insufficient_metrics['total_count'] * 100
                print(f"     {label:>10}: {count:>3}次 ({percentage:>5.1f}%)")
        
        return comparison
    
    async def run_experiment(self, dataset: List[Dict], model_name: str, dataset_name: str, 
                           output_folder: str) -> Dict[str, Any]:
        """运行完整实验"""
        
        print("=" * 70)
        print("Choice实验1.1_2.1：充分与不充分提示对比实验")
        print("完全对应TFU实验模式和结构")
        print("=" * 70)
        
        # 运行充分提示实验
        sufficient_results = await self.run_sufficient_experiment(dataset)
        sufficient_metrics = self.evaluator.calculate_choice_metrics_with_tfu_style(sufficient_results)
        sufficient_files = self.evaluator.save_experiment_results(
            sufficient_results, sufficient_metrics, model_name, dataset_name, "sufficient", output_folder
        )
        self.evaluator.print_experiment_summary(sufficient_metrics, "充分提示")
        
        # 运行不充分提示实验
        insufficient_results = await self.run_insufficient_experiment(dataset)
        insufficient_metrics = self.evaluator.calculate_choice_metrics_with_tfu_style(insufficient_results)
        insufficient_files = self.evaluator.save_experiment_results(
            insufficient_results, insufficient_metrics, model_name, dataset_name, "insufficient", output_folder
        )
        self.evaluator.print_experiment_summary(insufficient_metrics, "不充分提示")
        
        # 创建对比总结
        comparison = self.create_comparison_summary(
            sufficient_metrics, insufficient_metrics, model_name, dataset_name, output_folder
        )
        
        return {
            "sufficient_results": sufficient_results,
            "sufficient_metrics": sufficient_metrics,
            "sufficient_files": sufficient_files,
            "insufficient_results": insufficient_results,
            "insufficient_metrics": insufficient_metrics,
            "insufficient_files": insufficient_files,
            "comparison": comparison
        }
