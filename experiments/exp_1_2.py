#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice实验1.2：少样本学习实验
对应TFU的exp_TFU_1.2.py
"""

from typing import Dict, Any, List
from ..core.api_client import ChoiceAPIClient
from ..core.evaluator import ChoiceEvaluator

class Experiment1_2:
    """实验1.2：少样本学习实验"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_client = ChoiceAPIClient(config)
        self.evaluator = ChoiceEvaluator()
        self.few_shot_examples = config.get("few_shot_examples", 1)
    
    def create_few_shot_examples(self, num_examples: int = 1) -> List[Dict]:
        """创建少样本学习的示例"""
        all_examples = [
            {
                "type": "no_correct_answer",
                "question": "What is the color of the sky on Mars?",
                "options": ["Blue", "Red", "Green", "Yellow"],
                "correct_answers": [],
                "passage_text": "The passage does not provide information about the color of the sky on Mars."
            }
        ]
        
        # 根据需求选择示例数量
        if num_examples == 1:
            examples = [all_examples[0]]
        else:
            examples = all_examples[:num_examples]
        
        print(f"✅ 使用 {len(examples)} 个few shot示例")
        return examples
    
    def build_few_shot_prompt(self, element: Dict[str, Any], examples: List[Dict]) -> str:
        """构建少样本学习的Choice prompt"""
        
        question = element['question']
        options = element['options']
        passage = element.get('passage_text', '')
        
        # 构建选项文本
        options_text = "\n".join(options)
        
        # 构建Facts部分
        facts_part = ""
        if passage and passage.strip():
            facts_part = f"Facts: {passage}\n"
        
        # 构建少样本示例
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
        
        # 完整的少样本学习提示
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
        """运行少样本学习实验"""
        print(f"\n🚀 运行Choice少样本学习实验 - 模型: {self.config['test_model']}")
        print(f"   数据集大小: {len(dataset)}")
        print(f"   提示描述: 少样本学习 - 提供示例指导")
        print(f"   Judge模型: {self.config['judge_model']}")
        
        # 创建少样本示例
        examples = self.create_few_shot_examples(self.few_shot_examples)
        print(f"   少样本示例数量: {len(examples)}")
        
        # 从测试集中移除few shot示例，避免数据泄露
        test_dataset = []
        example_questions = {ex.get('question', '') for ex in examples}
        
        for element in dataset:
            if element.get('question', '') not in example_questions:
                test_dataset.append(element)
        
        print(f"   移除few shot示例后的测试集大小: {len(test_dataset)}")
        
        # 创建任务
        tasks = []
        for i, element in enumerate(test_dataset):
            prompt_content = self.build_few_shot_prompt(element, examples)
            task = self.api_client.process_single_element(
                element, lambda x: self.build_few_shot_prompt(x, examples), i, "few_shot"
            )
            tasks.append(task)
        
        # 执行任务
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)
        
        # 按索引排序
        results.sort(key=lambda x: x.get('index', 0))
        
        return results
    
    def create_few_shot_summary(self, few_shot_metrics: Dict, model_name: str, 
                              dataset_name: str, output_folder: str) -> Dict[str, Any]:
        """创建少样本学习对比总结"""
        
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
        
        # 保存对比结果
        import json
        import os
        
        clean_dataset_name = os.path.basename(dataset_name).replace('.json', '')
        comparison_filename = os.path.join(
            output_folder,
            f"{model_name}_{clean_dataset_name}_choice_few_shot_analysis.json"
        )
        
        with open(comparison_filename, "w", encoding="utf-8") as f:
            json.dump(comparison, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 少样本学习分析总结已保存: {comparison_filename}")
        print(f"   少样本学习性能:")
        print(f"     总体准确率: {few_shot_metrics['overall_accuracy']:.3f}")
        print(f"     Follow率: {few_shot_metrics['follow_rate']:.3f}")
        print(f"     Jump率1: {few_shot_metrics['jump_rate_no_answer']:.3f}")
        print(f"     Jump率2: {few_shot_metrics['jump_rate_with_answer']:.3f}")
        
        return comparison
    
    async def run_experiment(self, dataset: List[Dict], model_name: str, dataset_name: str, 
                           output_folder: str) -> Dict[str, Any]:
        """运行完整实验"""
        
        print("=" * 70)
        print("Choice实验1.2：少样本学习实验")
        print("基于choice_exp_1.1_2.1.py的统一标准")
        print("=" * 70)
        
        # 运行少样本学习实验
        few_shot_results = await self.run_few_shot_experiment(dataset)
        few_shot_metrics = self.evaluator.calculate_choice_metrics_with_tfu_style(few_shot_results)
        few_shot_files = self.evaluator.save_experiment_results(
            few_shot_results, few_shot_metrics, model_name, dataset_name, "few_shot", output_folder
        )
        self.evaluator.print_experiment_summary(few_shot_metrics, "少样本学习")
        
        # 创建分析总结
        analysis = self.create_few_shot_summary(
            few_shot_metrics, model_name, dataset_name, output_folder
        )
        
        return {
            "few_shot_results": few_shot_results,
            "few_shot_metrics": few_shot_metrics,
            "few_shot_files": few_shot_files,
            "analysis": analysis
        }
