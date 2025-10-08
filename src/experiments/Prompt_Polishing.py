#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Experiment Prompt_Polishing
"""

from typing import Dict, Any, List
from core.api_client import ChoiceAPIClient
from core.evaluator import ChoiceEvaluator

class Experiment_Prompt_Polishing:
    """Experiment Prompt Polishing"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_client = ChoiceAPIClient(config)
        self.evaluator = ChoiceEvaluator()
    
    def build_llm_polished_prompt(self, element: Dict[str, Any]) -> str:
        """Build LLM-polished insufficient Choice prompt (professionally polished based on insufficient prompt)"""
        
        question = element['question']
        options = element['options']
        passage = element.get('passage_text', '')
        
        # Build options text
        options_text = "\n".join(options)
        
        # Build Facts section
        facts_part = ""
        if passage and passage.strip():
            facts_part = f"Facts: {passage}\n"
        
        # LLM-polished insufficient prompt (professionally polished based on insufficient format)
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
        """Run LLM-optimized prompt experiment"""
        print(f"\n🚀 Running Choice LLM-Optimized Prompt Experiment - Model: {self.config['test_model']}")
        print(f"   Dataset size: {len(dataset)}")
        print(f"   Judge model: {self.config['judge_model']}")
        print(f"   Prompt description: LLM-optimized prompt - Using optimized prompt structure")
        
        return await self.api_client.process_dataset(dataset, self.build_llm_polished_prompt, "llm_polished")
    
    async def run_experiment(self, dataset: List[Dict], model_name: str, dataset_name: str, 
                           output_folder: str) -> Dict[str, Any]:
        """Run complete experiment"""
        # Run LLM-optimized prompt experiment
        llm_polished_results = await self.run_llm_polished_experiment(dataset)
        llm_polished_metrics = self.evaluator.calculate_choice_metrics_with_tfu_style(llm_polished_results)
        llm_polished_files = self.evaluator.save_experiment_results(
            llm_polished_results, llm_polished_metrics, model_name, dataset_name, "llm_polished", output_folder
        )
        self.evaluator.print_experiment_summary(llm_polished_metrics, "LLM-Optimized Prompt")
        
        return {
            "llm_polished_results": llm_polished_results,
            "llm_polished_metrics": llm_polished_metrics,
            "llm_polished_files": llm_polished_files
        }
