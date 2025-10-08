#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Experiment Few-shot Learning
"""

from typing import Dict, Any, List
from core.api_client import ChoiceAPIClient
from core.evaluator import ChoiceEvaluator

import asyncio

class Experiment_Few_shot_Learning:
    """Experiment Few-shot Learning"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_client = ChoiceAPIClient(config)
        self.evaluator = ChoiceEvaluator()
        self.few_shot_examples = config.get("few_shot_examples", 1)
    
    def create_few_shot_examples(self, num_examples: int = 1) -> List[Dict]:
        """Create few-shot learning examples"""
        all_examples = [
            {
                "type": "no_correct_answer",
                "question": "What is the color of the sky on Mars?",
                "options": ["Blue", "Red", "Green", "Yellow"],
                "correct_answers": [],
                "passage_text": "The passage does not provide information about the color of the sky on Mars."
            }
        ]
        
        # Select number of examples based on requirements
        if num_examples == 1:
            examples = [all_examples[0]]
        else:
            examples = all_examples[:num_examples]
        
        print(f"✅ Using {len(examples)} few-shot examples")
        return examples
    
    def build_few_shot_prompt(self, element: Dict[str, Any], examples: List[Dict]) -> str:
        """Build few-shot learning Choice prompt"""
        
        question = element['question']
        options = element['options']
        passage = element.get('passage_text', '')
        
        # Build options text
        options_text = "\n".join(options)
        
        # Build Facts section
        facts_part = ""
        if passage and passage.strip():
            facts_part = f"Facts: {passage}\n"
        
        # Build few-shot examples
        examples_text = ""
        for i, example in enumerate(examples, 1):
            example_options = "\n".join(example['options'])
            example_answer = ", ".join(map(str, example['correct_answers'])) if example['correct_answers'] else "No correct answer"
            examples_text += f"\nExample {i}:\n"
            examples_text += f"Question: {example['question']}\n"
            if example.get('passage_text'):
                examples_text += f"Facts: {example['passage_text']}\n"
            examples_text += f"Options:\n{example_options}\n"
            examples_text += f"Answer: {example_answer}\n"
        
        # Complete few-shot learning prompt
        prompt = f"""Here are some examples of how to answer choice questions:{examples_text}

Now, please answer the following question:

Question: {question}
{facts_part}Options:
{options_text}

Response Format:
- For single choice questions: Provide only the number of the correct option (e.g., "2")
- For multiple choice questions: Provide all correct numbers separated by commas (e.g., "1, 3")
- For questions with no correct options: Respond with "No correct answer"

Answer:"""

        return prompt
    
    async def run_few_shot_experiment(self, dataset: List[Dict]) -> List[Dict]:
        """Run few-shot learning experiment"""
        print(f"\n🚀 Running Choice Few-shot Learning Experiment - Model: {self.config['test_model']}")
        print(f"   Dataset size: {len(dataset)}")
        print(f"   Prompt description: Few-shot learning - Providing example guidance")
        print(f"   Judge model: {self.config['judge_model']}")
        
        # Create few-shot examples
        examples = self.create_few_shot_examples(self.few_shot_examples)
        print(f"   Number of few-shot examples: {len(examples)}")
        
        # Remove few-shot examples from test dataset to avoid data leakage
        test_dataset = []
        example_questions = {ex.get('question', '') for ex in examples}
        
        for element in dataset:
            if element.get('question', '') not in example_questions:
                test_dataset.append(element)
        
        print(f"   Test dataset size after removing few-shot examples: {len(test_dataset)}")
        
        # Create tasks
        tasks = []
        for i, element in enumerate(test_dataset):
            prompt_content = self.build_few_shot_prompt(element, examples)
            task = self.api_client.process_single_element(
                element, lambda x: self.build_few_shot_prompt(x, examples), i, "few_shot"
            )
            tasks.append(task)
        
        # Execute tasks
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)
        
        # Sort by index
        results.sort(key=lambda x: x.get('index', 0))
        
        return results
    
    def create_few_shot_summary(self, few_shot_metrics: Dict, model_name: str, 
                              dataset_name: str, output_folder: str) -> Dict[str, Any]:
        """Create few-shot learning comparison summary"""
        
        comparison = {
            "model": model_name,
            "dataset": dataset_name,
            "experiment_type": "few_shot_choice_tfu_style",
            "few_shot_prompt": {
                "overall_accuracy": few_shot_metrics["overall_accuracy"],
                "follow_rate": few_shot_metrics["follow_rate"],
                "jump_rate_no_answer": few_shot_metrics["jump_rate_no_answer"],
                "jump_rate_with_answer": few_shot_metrics["jump_rate_with_answer"],
                "total_count": few_shot_metrics["total_count"]
            },
            "performance_analysis": {
                "overall_accuracy": few_shot_metrics["overall_accuracy"],
                "follow_rate": few_shot_metrics["follow_rate"],
                "jump_rate_no_answer": few_shot_metrics["jump_rate_no_answer"],
                "jump_rate_with_answer": few_shot_metrics["jump_rate_with_answer"]
            },
            "output_type_stats": few_shot_metrics.get("output_type_stats", {}),
            "llm_output_label_stats": few_shot_metrics.get("llm_output_label_stats", {}),
            "extraction_method_stats": few_shot_metrics.get("extraction_method_stats", {})
        }
        
        # Save comparison results
        import json
        import os
        
        clean_dataset_name = os.path.basename(dataset_name).replace('.json', '')
        comparison_filename = os.path.join(
            output_folder,
            f"{model_name}_{clean_dataset_name}_choice_few_shot_analysis.json"
        )
        
        with open(comparison_filename, "w", encoding="utf-8") as f:
            json.dump(comparison, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Few-shot learning analysis summary saved: {comparison_filename}")
        print(f"   Few-shot learning performance:")
        print(f"     Overall accuracy: {few_shot_metrics['overall_accuracy']:.3f}")
        print(f"     Follow rate: {few_shot_metrics['follow_rate']:.3f}")
        print(f"     Jump rate 1: {few_shot_metrics['jump_rate_no_answer']:.3f}")
        print(f"     Jump rate 2: {few_shot_metrics['jump_rate_with_answer']:.3f}")
        
        return comparison
    
    async def run_experiment(self, dataset: List[Dict], model_name: str, dataset_name: str, 
                           output_folder: str) -> Dict[str, Any]:
        """Run complete experiment"""
        # Run few-shot learning experiment
        few_shot_results = await self.run_few_shot_experiment(dataset)
        few_shot_metrics = self.evaluator.calculate_choice_metrics_with_tfu_style(few_shot_results)
        few_shot_files = self.evaluator.save_experiment_results(
            few_shot_results, few_shot_metrics, model_name, dataset_name, "few_shot", output_folder
        )
        self.evaluator.print_experiment_summary(few_shot_metrics, "Few-shot Learning")
        
        # Create analysis summary
        analysis = self.create_few_shot_summary(
            few_shot_metrics, model_name, dataset_name, output_folder
        )
        
        return {
            "few_shot_results": few_shot_results,
            "few_shot_metrics": few_shot_metrics,
            "few_shot_files": few_shot_files,
            "analysis": analysis
        }

