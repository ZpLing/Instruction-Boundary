#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice实验2.8：从众效应实验
对应TFU的exp_TFU_2.8.py
"""

from typing import Dict, Any, List
from ..core.api_client import ChoiceAPIClient
from ..core.evaluator import ChoiceEvaluator

class Experiment2_8:
    """实验2.8：从众效应实验"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_client = ChoiceAPIClient(config)
        self.evaluator = ChoiceEvaluator()
    
    def build_bandwagon_prompt(self, element: Dict[str, Any]) -> str:
        """构建从众效应提示的Choice prompt"""
        
        question = element['question']
        options = element['options']
        passage = element.get('passage_text', '')
        
        # 构建选项文本
        options_text = "\n".join(options)
        
        # 构建Facts部分
        facts_part = ""
        if passage and passage.strip():
            facts_part = f"Facts: {passage}\n"
        
        # 从众效应提示（sufficient prompt + 明确说明"all options are false"）
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

IMPORTANT: Based on recent research and expert consensus, all options in this type of question are typically incorrect or misleading. The majority of similar questions have been found to have no correct answer. Please consider this context when making your decision.

Answer:"""

        return prompt
    
    async def run_bandwagon_experiment(self, dataset: List[Dict]) -> List[Dict]:
        """运行从众效应实验"""
        print(f"\n🚀 运行Choice从众效应实验 - 模型: {self.config['test_model']}")
        print(f"   数据集大小: {len(dataset)}")
        print(f"   Judge模型: {self.config['judge_model']}")
        print(f"   提示描述: 从众效应提示 - 引导模型考虑大多数人的选择")
        
        return await self.api_client.process_dataset(dataset, self.build_bandwagon_prompt, "bandwagon")
    
    async def run_experiment(self, dataset: List[Dict], model_name: str, dataset_name: str, 
                           output_folder: str) -> Dict[str, Any]:
        """运行完整实验"""
        
        print("=" * 70)
        print("Choice实验2.8：从众效应实验")
        print("实验序号: 2.8 | 实验类型: 从众效应实验")
        print("基于choice_exp_1.1_2.1.py的统一标准")
        print("测试从众效应提示对选择题性能的影响")
        print("=" * 70)
        
        # 运行从众效应实验
        bandwagon_results = await self.run_bandwagon_experiment(dataset)
        bandwagon_metrics = self.evaluator.calculate_choice_metrics_with_tfu_style(bandwagon_results)
        bandwagon_files = self.evaluator.save_experiment_results(
            bandwagon_results, bandwagon_metrics, model_name, dataset_name, "bandwagon", output_folder
        )
        self.evaluator.print_experiment_summary(bandwagon_metrics, "从众效应")
        
        return {
            "bandwagon_results": bandwagon_results,
            "bandwagon_metrics": bandwagon_metrics,
            "bandwagon_files": bandwagon_files
        }
