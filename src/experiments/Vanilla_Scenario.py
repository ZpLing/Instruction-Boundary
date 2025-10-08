#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Experiment Vanilla Scenario
"""

from typing import Dict, Any, List
from core.api_client import ChoiceAPIClient
from core.evaluator import ChoiceEvaluator
from core.utils import create_output_filename

class Experiment_Vanilla_Scenario:
    """Experiment Vanilla Scenario"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_client = ChoiceAPIClient(config)
        self.evaluator = ChoiceEvaluator()
    
    def build_sufficient_prompt(self, element: Dict[str, Any]) -> str:
        """Build sufficient Choice prompt (supports Choice and TFU formats)"""
        
        # Detect data format and get corresponding fields
        if 'facts' in element and 'conclusion' in element:
            # TFU format: Use Conclusion and Facts fields
            question = element['conclusion']
            facts = element['facts']
            options = element['options']
            
            # Build options text
            options_text = "\n".join(options)
            
            # Sufficient prompt for TFU format (corresponding to original TFU experiment)
            prompt = f"""Question: {question}
Facts: {facts}
Task: Based on the given facts, determine whether the question can be proven.
Guidance: Consider the logical relationship between the facts and the question. Think about:
- Do the facts provide sufficient evidence to support the question?
- Do the facts contradict or refute the question?
- Are the facts insufficient or ambiguous to make a clear determination?
Options:
1. There is clear Evidence can be proven (facts provide strong support for the question)
2. There is clear Evidence can be disproven (facts clearly contradict the question)
3. There is clear Evidence cannot be determined (facts are insufficient, ambiguous, or inconclusive)
Note: The hint above is a general guidance, but you should think independently and critically. Consider all possible interpretations and edge cases. Please respond with only the option number (1, 2, or 3)."""
        else:
            # Choice format: Use question and options fields
            question = element['question']
            options = element['options']
            passage = element.get('passage_text', '')
            
            # Build options text
            options_text = "\n".join(options)
            
            # Build Facts section
            facts_part = ""
            if passage and passage.strip():
                facts_part = f"Facts: {passage}\n"
            
            # Sufficient prompt for Choice format
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
    
    async def run_sufficient_experiment(self, dataset: List[Dict]) -> List[Dict]:
        """Run sufficient prompt experiment"""
        return await self.api_client.process_dataset(dataset, self.build_sufficient_prompt, "sufficient")
    
    async def run_experiment(self, dataset: List[Dict], model_name: str, dataset_name: str, 
                           output_folder: str) -> Dict[str, Any]:
        """Run complete sufficient prompt experiment"""
        # Run sufficient prompt experiment
        sufficient_results = await self.run_sufficient_experiment(dataset)
        sufficient_metrics = self.evaluator.calculate_choice_metrics_with_tfu_style(sufficient_results)
        sufficient_files = self.evaluator.save_experiment_results(
            sufficient_results, sufficient_metrics, model_name, dataset_name, "sufficient", output_folder
        )
        self.evaluator.print_experiment_summary(sufficient_metrics, "Sufficient Prompt")
        
        return {
            "sufficient_results": sufficient_results,
            "sufficient_metrics": sufficient_metrics,
            "sufficient_files": sufficient_files
        }