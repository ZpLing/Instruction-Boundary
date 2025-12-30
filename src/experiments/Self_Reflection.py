#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Experiment Multi-turn Dialogue
"""

import asyncio
from typing import Dict, Any, List
from core.api_client import ChoiceAPIClient
from core.evaluator import ChoiceEvaluator

class Experiment_Multi_turn_Dialogue:
    """Experiment Multi-turn Dialogue"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_client = ChoiceAPIClient(config)
        self.evaluator = ChoiceEvaluator()
    
    def build_first_round_prompt(self, element: Dict[str, Any]) -> str:
        """Build first round dialogue prompt"""
        
        question = element['question']
        options = element['options']
        passage = element.get('passage_text', '')
        
        # Build options text
        options_text = "\n".join(options)
        
        # Build Facts section
        facts_part = ""
        if passage and passage.strip():
            facts_part = f"Facts: {passage}\n"
        
        # First round dialogue prompt
        prompt = f"""Question: {question}
{facts_part}Options:
{options_text}

Please respond with only the option number(s)."""

        return prompt
    
    def build_reflection_prompt(self, element: Dict[str, Any], first_answer: str) -> str:
        """Build second round reflection prompt"""
        
        question = element['question']
        options = element['options']
        passage = element.get('passage_text', '')
        
        # Build options text
        options_text = "\n".join(options)
        
        # Build Facts section
        facts_part = ""
        if passage and passage.strip():
            facts_part = f"Facts: {passage}\n"
        
        # Second round: Reflection and improvement
        prompt = f"""Question: {question}
{facts_part}Your previous answer: {first_answer}

Now, please reflect on your previous answer and consider:
1. **Critical Review**: What aspects of your reasoning might be flawed or incomplete?
2. **Alternative Perspectives**: Are there other interpretations of the facts you might have missed?
3. **Evidence Re-evaluation**: Have you properly weighed all the evidence?
4. **Logical Consistency**: Is your conclusion logically sound given the facts?
5. **Confidence Level**: How confident are you in your answer?

Please provide your reflection and then give your final answer in the following format:

## Reflection Process
[Your critical reflection here]

## Final Answer
[Your final choice here]

IMPORTANT: Your final answer must follow the same format as before:
- For single choice questions: Provide only the number of the correct option (e.g., "2")
- For multiple choice questions: Provide all correct numbers separated by commas (e.g., "1, 3")
- For questions with no correct options: Respond with "No correct answer"

Options:
{options_text}

Final Answer:"""

        return prompt
    
    async def run_multi_turn_experiment(self, dataset: List[Dict]) -> List[Dict]:
        """Run multi-turn dialogue experiment"""
        print(f"\n🚀 Running Choice Multi-turn Dialogue Experiment - Model: {self.config['test_model']}")
        print(f"   Dataset size: {len(dataset)}")
        print(f"   Judge model: {self.config['judge_model']}")
        print(f"   Prompt description: Multi-turn dialogue reflection - Two-round reflection mode")
        
        # Create tasks
        tasks = []
        for i, element in enumerate(dataset):
            task = self.process_multi_turn_element(element, i)
            tasks.append(task)
        
        # Execute tasks
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)
        
        # Sort by index
        results.sort(key=lambda x: x.get('index', 0))
        
        return results
    
    async def process_multi_turn_element(self, element: Dict[str, Any], index: int) -> Dict[str, Any]:
        """Process single element with multi-turn dialogue"""
        
        # First round dialogue
        first_prompt = self.build_first_round_prompt(element)
        first_msg = [{"role": "user", "content": first_prompt}]
        first_answer = await self.api_client.call_openai(first_msg)
        
        # Reflection round
        reflection_prompt = self.build_reflection_prompt(element, first_answer)
        reflection_msg = [{"role": "user", "content": reflection_prompt}]
        final_answer = await self.api_client.call_openai(reflection_msg)
        
        # Extract label using hybrid strategy
        extracted_label, extraction_method = await self.api_client.hybrid_extract_choice_label(final_answer)
        
        # Evaluate using improved judging logic
        from core.utils import improved_choice_judge_logic
        judge_result = improved_choice_judge_logic(final_answer, element.get('correct_answers', []))
        
        return {
            "index": index,
            "element": element,
            "first_answer": first_answer,
            "final_answer": final_answer,
            "prompt_type": "multi_turn",
            "first_prompt": first_prompt,
            "reflection_prompt": reflection_prompt,
            "extracted_label": extracted_label,
            "extraction_method": extraction_method,
            "judge_evaluation": judge_result
        }
    
    async def run_experiment(self, dataset: List[Dict], model_name: str, dataset_name: str, 
                           output_folder: str) -> Dict[str, Any]:
        """Run complete experiment"""
        # Run multi-turn dialogue experiment
        multi_turn_results = await self.run_multi_turn_experiment(dataset)
        multi_turn_metrics = self.evaluator.calculate_choice_metrics_with_tfu_style(multi_turn_results)
        multi_turn_files = self.evaluator.save_experiment_results(
            multi_turn_results, multi_turn_metrics, model_name, dataset_name, "multi_turn", output_folder
        )
        self.evaluator.print_experiment_summary(multi_turn_metrics, "Multi-turn Dialogue Reflection")
        
        return {
            "multi_turn_results": multi_turn_results,
            "multi_turn_metrics": multi_turn_metrics,
            "multi_turn_files": multi_turn_files
        }
