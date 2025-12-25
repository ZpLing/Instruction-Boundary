#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - API Client Module
Unified API calling and LLM Judge functionality
"""

import asyncio
import openai
from typing import List, Dict, Any, Tuple
from .utils import extract_choice_label_by_keywords, improved_choice_judge_logic

class ChoiceAPIClient:
    """Choice API Client"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = openai.AsyncOpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"]
        )
        self.semaphore = asyncio.Semaphore(config.get("semaphore_limit", 50))
    
    async def call_openai(self, msg: List[Dict]) -> str:
        """Call OpenAI API"""
        async with self.semaphore:
            try:
                response = await self.client.chat.completions.create(
                    model=self.config["test_model"],
                    messages=msg,
                    max_tokens=self.config.get("max_tokens", 80),
                    temperature=self.config.get("temperature", 0.0)
                )
                content = response.choices[0].message.content
                return content.strip() if content else "ERROR"
            except Exception as e:
                print(f"API call error: {e}")
                return "ERROR"
    
    async def llm_judge_extract_choice_label(self, answer_text: str) -> str:
        """Use LLM judge to extract Choice label"""
        judge_prompt = f"""Analyze the following LLM response and determine which option(s) it selected:

Response content: "{answer_text}"

Please determine what this response expresses:
- Selected option 0: respond "0"
- Selected option 1: respond "1" 
- Selected option 2: respond "2"
- Selected option 3: respond "3"
- Selected multiple options (e.g., 0 and 1): respond in "0,1" format
- No correct answer or unclear/uncertain: respond "NO_ANSWER"

Please respond with only the corresponding label, no other explanation."""

        try:
            response = await self.client.chat.completions.create(
                model=self.config["judge_model"],  # Using deepseek-v3 as Judge
                messages=[{"role": "user", "content": judge_prompt}],
                max_tokens=20,
                temperature=0.0
            )
            
            content = response.choices[0].message.content
            judge_result = content.strip() if content else "UNCLEAR"
            return judge_result
            
        except Exception as e:
            print(f"⚠️  LLM Judge call error: {e}")
            return "UNCLEAR"  # Default return UNCLEAR
    
    async def hybrid_extract_choice_label(self, answer_text: str) -> Tuple[str, str]:
        """Hybrid strategy: try keyword matching first, use LLM judge when unrecognizable"""
        # Try keyword matching first
        keyword_result = extract_choice_label_by_keywords(answer_text)
        if keyword_result is not None:
            return keyword_result, "keyword"
        
        # Keyword unrecognizable, use LLM judge
        llm_result = await self.llm_judge_extract_choice_label(answer_text)
        return llm_result, "llm_judge"
    
    async def process_single_element(self, element: Dict[str, Any], prompt_builder, 
                                   index: int, experiment_type: str) -> Dict[str, Any]:
        """Process single element"""
        # Build prompt
        prompt_content = prompt_builder(element)
        
        msg = [{
            "role": "user",
            "content": prompt_content
        }]
        
        # Get model answer
        answer = await self.call_openai(msg)
        
        # Extract label using hybrid strategy
        extracted_label, extraction_method = await self.hybrid_extract_choice_label(answer)
        
        # Evaluate using improved judging logic
        judge_result = improved_choice_judge_logic(answer, element.get('correct_answers', []))
        
        return {
            "index": index,
            "element": element,
            "response": answer,
            "prompt_type": experiment_type,
            "prompt": prompt_content,
            "extracted_label": extracted_label,
            "extraction_method": extraction_method,
            "judge_evaluation": judge_result
        }
    
    async def process_dataset(self, dataset: List[Dict], prompt_builder, 
                            experiment_type: str) -> List[Dict]:
        """Process entire dataset"""
        print(f"\n🚀 Running Choice {experiment_type} experiment - Model: {self.config['test_model']}")
        print(f"   Dataset size: {len(dataset)}")
        print(f"   Judge model: {self.config['judge_model']}")
        
        # Create tasks
        tasks = []
        for i, element in enumerate(dataset):
            task = self.process_single_element(element, prompt_builder, i, experiment_type)
            tasks.append(task)
        
        # Execute tasks
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)
        
        # Sort by index
        results.sort(key=lambda x: x.get('index', 0))
        
        return results

