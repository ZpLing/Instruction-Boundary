#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Experiment Vaugeness: Ambiguous Prompt Experiment
"""

from typing import Dict, Any, List
from core.api_client import ChoiceAPIClient
from core.evaluator import ChoiceEvaluator

class Experiment_Vaugeness:
    """Experiment Vaugeness"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_client = ChoiceAPIClient(config)
        self.evaluator = ChoiceEvaluator()
    
    def build_ambiguous_prompt(self, element: Dict[str, Any]) -> str:
        """Build ambiguous Choice prompt (keep only basic information)"""
        
        question = element['question']
        options = element['options']
        passage = element.get('passage_text', '')
        
        # Build options text
        options_text = "\n".join(options)
        
        # Build Facts section
        facts_part = ""
        if passage and passage.strip():
            facts_part = f"Facts: {passage}\n"
        
        # Ambiguous prompt (keep only basic information, reduce guiding content)
        prompt = f"""Question: {question}
{facts_part}Options:
{options_text}

Please respond with only the option number(s)."""

        return prompt
    
    async def run_ambiguous_experiment(self, dataset: List[Dict]) -> List[Dict]:
        """Run ambiguous prompt experiment"""
        print(f"\n🚀 Running Choice Ambiguous Prompt Experiment - Model: {self.config['test_model']}")
        print(f"   Dataset size: {len(dataset)}")
        print(f"   Judge model: {self.config['judge_model']}")
        print(f"   Prompt description: Ambiguous prompt - Keep only basic information, reduce guiding content")
        
        return await self.api_client.process_dataset(dataset, self.build_ambiguous_prompt, "ambiguous")
    
    async def run_experiment(self, dataset: List[Dict], model_name: str, dataset_name: str, 
                           output_folder: str) -> Dict[str, Any]:
        """Run complete experiment"""
        # Run ambiguous prompt experiment
        ambiguous_results = await self.run_ambiguous_experiment(dataset)
        ambiguous_metrics = self.evaluator.calculate_choice_metrics_with_tfu_style(ambiguous_results)
        ambiguous_files = self.evaluator.save_experiment_results(
            ambiguous_results, ambiguous_metrics, model_name, dataset_name, "ambiguous", output_folder
        )
        self.evaluator.print_experiment_summary(ambiguous_metrics, "Ambiguous Prompt")
        
        return {
            "ambiguous_results": ambiguous_results,
            "ambiguous_metrics": ambiguous_metrics,
            "ambiguous_files": ambiguous_files
        }

