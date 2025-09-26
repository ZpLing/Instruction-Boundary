#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice实验2.3：模糊提示实验
对应TFU的exp_TFU_2.3.py
"""

from typing import Dict, Any, List
from ..core.api_client import ChoiceAPIClient
from ..core.evaluator import ChoiceEvaluator

class Experiment2_3:
    """实验2.3：模糊提示实验"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_client = ChoiceAPIClient(config)
        self.evaluator = ChoiceEvaluator()
    
    def build_ambiguous_prompt(self, element: Dict[str, Any]) -> str:
        """构建模糊提示的Choice prompt（只保留最基本信息）"""
        
        question = element['question']
        options = element['options']
        passage = element.get('passage_text', '')
        
        # 构建选项文本
        options_text = "\n".join(options)
        
        # 构建Facts部分
        facts_part = ""
        if passage and passage.strip():
            facts_part = f"Facts: {passage}\n"
        
        # 模糊提示（只保留最基本信息，减少引导性内容）
        prompt = f"""Question: {question}
{facts_part}Options:
{options_text}

Please respond with only the option number(s)."""

        return prompt
    
    async def run_ambiguous_experiment(self, dataset: List[Dict]) -> List[Dict]:
        """运行模糊提示实验"""
        print(f"\n🚀 运行Choice模糊提示实验 - 模型: {self.config['test_model']}")
        print(f"   数据集大小: {len(dataset)}")
        print(f"   Judge模型: {self.config['judge_model']}")
        print(f"   提示描述: 模糊提示 - 只保留最基本信息，减少引导性内容")
        
        return await self.api_client.process_dataset(dataset, self.build_ambiguous_prompt, "ambiguous")
    
    async def run_experiment(self, dataset: List[Dict], model_name: str, dataset_name: str, 
                           output_folder: str) -> Dict[str, Any]:
        """运行完整实验"""
        
        print("=" * 70)
        print("Choice实验2.3：模糊提示实验")
        print("实验序号: 2.3 | 实验类型: 模糊提示实验 (Ambiguous Prompt)")
        print("基于choice_exp_1.1_2.1.py的统一标准")
        print("测试最简提示（只保留基本信息）对选择题性能的影响")
        print("=" * 70)
        
        # 运行模糊提示实验
        ambiguous_results = await self.run_ambiguous_experiment(dataset)
        ambiguous_metrics = self.evaluator.calculate_choice_metrics_with_tfu_style(ambiguous_results)
        ambiguous_files = self.evaluator.save_experiment_results(
            ambiguous_results, ambiguous_metrics, model_name, dataset_name, "ambiguous", output_folder
        )
        self.evaluator.print_experiment_summary(ambiguous_metrics, "模糊提示")
        
        return {
            "ambiguous_results": ambiguous_results,
            "ambiguous_metrics": ambiguous_metrics,
            "ambiguous_files": ambiguous_files
        }
