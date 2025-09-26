#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - API客户端模块
统一的API调用和LLM Judge功能
"""

import asyncio
import openai
from typing import List, Dict, Any, Tuple
from .utils import extract_choice_label_by_keywords, improved_choice_judge_logic

class ChoiceAPIClient:
    """Choice API客户端"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = openai.AsyncOpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"]
        )
        self.semaphore = asyncio.Semaphore(config.get("semaphore_limit", 50))
    
    async def call_openai(self, msg: List[Dict]) -> str:
        """调用OpenAI API"""
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
                print(f"API调用错误: {e}")
                return "ERROR"
    
    async def llm_judge_extract_choice_label(self, answer_text: str) -> str:
        """使用LLM judge来提取Choice标签"""
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
                model=self.config["judge_model"],  # 使用gpt-4o作为Judge
                messages=[{"role": "user", "content": judge_prompt}],
                max_tokens=20,
                temperature=0.0
            )
            
            content = response.choices[0].message.content
            judge_result = content.strip() if content else "UNCLEAR"
            return judge_result
            
        except Exception as e:
            print(f"⚠️  LLM Judge调用错误: {e}")
            return "UNCLEAR"  # 默认返回UNCLEAR
    
    async def hybrid_extract_choice_label(self, answer_text: str) -> Tuple[str, str]:
        """混合策略：先尝试关键词匹配，无法识别时使用LLM judge"""
        # 先尝试关键词匹配
        keyword_result = extract_choice_label_by_keywords(answer_text)
        if keyword_result is not None:
            return keyword_result, "keyword"
        
        # 关键词无法识别，使用LLM judge
        llm_result = await self.llm_judge_extract_choice_label(answer_text)
        return llm_result, "llm_judge"
    
    async def process_single_element(self, element: Dict[str, Any], prompt_builder, 
                                   index: int, experiment_type: str) -> Dict[str, Any]:
        """处理单个元素"""
        # 构建prompt
        prompt_content = prompt_builder(element)
        
        msg = [{
            "role": "user",
            "content": prompt_content
        }]
        
        # 获取模型回答
        answer = await self.call_openai(msg)
        
        # 使用混合策略提取标签
        extracted_label, extraction_method = await self.hybrid_extract_choice_label(answer)
        
        # 使用改进的judging逻辑评估
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
        """处理整个数据集"""
        print(f"\n🚀 运行Choice {experiment_type}实验 - 模型: {self.config['test_model']}")
        print(f"   数据集大小: {len(dataset)}")
        print(f"   Judge模型: {self.config['judge_model']}")
        
        # 创建任务
        tasks = []
        for i, element in enumerate(dataset):
            task = self.process_single_element(element, prompt_builder, i, experiment_type)
            tasks.append(task)
        
        # 执行任务
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)
        
        # 按索引排序
        results.sort(key=lambda x: x.get('index', 0))
        
        return results
