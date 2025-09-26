#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice实验2.5：LLM优化提示实验
对应TFU的exp_TFU_2.5.py
"""

from typing import Dict, Any, List
from ..core.api_client import ChoiceAPIClient
from ..core.evaluator import ChoiceEvaluator

class Experiment2_5:
    """实验2.5：LLM优化提示实验"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_client = ChoiceAPIClient(config)
        self.evaluator = ChoiceEvaluator()
    
    def build_llm_polished_prompt(self, element: Dict[str, Any]) -> str:
        """构建LLM润色后的insufficient Choice prompt（基于insufficient提示进行专业润色）"""
        
        question = element['question']
        options = element['options']
        passage = element.get('passage_text', '')
        
        # 构建选项文本
        options_text = "\n".join(options)
        
        # 构建Facts部分
        facts_part = ""
        if passage and passage.strip():
            facts_part = f"Facts: {passage}\n"
        
        # LLM润色后的insufficient提示（基于insufficient但进行专业润色）
        prompt = f"""Question: {question}
{facts_part}Task: Based on the provided information, determine which option is correct for the question.

Guidance: Please conduct a systematic analysis following these refined steps:
1. **Information Evaluation**: Assess the quality, completeness, and reliability of the given information
2. **Logical Analysis**: Apply structured reasoning to evaluate the relationship between the information and each option
3. **Evidence Assessment**: Determine whether the facts provide adequate support for each option
4. **Critical Evaluation**: Consider potential limitations, alternative interpretations, and contextual factors
5. **Decision Synthesis**: Apply a methodical approach to reach the most appropriate conclusion

Options:
{options_text}

Response Format:
- For single choice questions: Provide only the number of the correct option (e.g., "2")
- For questions with no correct options: Respond with "No correct answer"

Note: This is a professional evaluation task requiring careful analysis. Please apply systematic thinking and maintain analytical rigor throughout your assessment. Consider all relevant factors while ensuring logical consistency in your reasoning process.

Answer:"""

        return prompt
    
    async def run_llm_polished_experiment(self, dataset: List[Dict]) -> List[Dict]:
        """运行LLM优化提示实验"""
        print(f"\n🚀 运行Choice LLM优化提示实验 - 模型: {self.config['test_model']}")
        print(f"   数据集大小: {len(dataset)}")
        print(f"   Judge模型: {self.config['judge_model']}")
        print(f"   提示描述: LLM优化提示 - 使用优化的提示结构")
        
        return await self.api_client.process_dataset(dataset, self.build_llm_polished_prompt, "llm_polished")
    
    async def run_experiment(self, dataset: List[Dict], model_name: str, dataset_name: str, 
                           output_folder: str) -> Dict[str, Any]:
        """运行完整实验"""
        
        print("=" * 70)
        print("Choice实验2.5：LLM优化提示实验")
        print("实验序号: 2.5 | 实验类型: LLM优化提示实验")
        print("基于choice_exp_1.1_2.1.py的统一标准")
        print("测试LLM优化的提示对选择题性能的影响")
        print("=" * 70)
        
        # 运行LLM优化提示实验
        llm_polished_results = await self.run_llm_polished_experiment(dataset)
        llm_polished_metrics = self.evaluator.calculate_choice_metrics_with_tfu_style(llm_polished_results)
        llm_polished_files = self.evaluator.save_experiment_results(
            llm_polished_results, llm_polished_metrics, model_name, dataset_name, "llm_polished", output_folder
        )
        self.evaluator.print_experiment_summary(llm_polished_metrics, "LLM优化提示")
        
        return {
            "llm_polished_results": llm_polished_results,
            "llm_polished_metrics": llm_polished_metrics,
            "llm_polished_files": llm_polished_files
        }
