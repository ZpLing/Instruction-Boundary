#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Experiment 6.6: Redundant Options Experiment
"""

import asyncio
import json
import random
import os
from tqdm import tqdm
from typing import List, Dict, Any
from datasets import load_dataset
from core.api_client import ChoiceAPIClient
from core.evaluator import ChoiceEvaluator

class Experiment_Disturbing_Miscellany:
    """Experiment Disturbing Miscellany"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_client = ChoiceAPIClient(config)
        self.evaluator = ChoiceEvaluator()
        self.model_name = config.get("model_name", "unknown_model")
    
    def load_mmlu_pro_dataset(self, sample_size: int = 300):
        """Load MMLU-Pro dataset from local or HuggingFace"""
        print(f"🔄 Loading MMLU-Pro dataset...")
        
        # Try loading from local first
        local_path = "./MMLU-Pro"
        if os.path.exists(local_path):
            try:
                print("Loading MMLU-Pro dataset from local directory...")
                dataset = load_dataset(local_path, split="test")
                
                # Convert to list format
                data_list = list(dataset)
                
                # Random sampling
                random.seed(42)
                if len(data_list) > sample_size:
                    sampled_data = random.sample(data_list, sample_size)
                else:
                    sampled_data = data_list
                
                print(f"✅ Successfully loaded MMLU-Pro dataset from local, original count: {len(data_list)}, sampled count: {len(sampled_data)}")
                return sampled_data
                
            except Exception as e:
                print(f"⚠️ Local loading failed: {e}")
        
        # If local loading fails, try loading from HuggingFace
        try:
            print("Loading MMLU-Pro dataset from HuggingFace...")
            dataset = load_dataset("TIGER-Lab/MMLU-Pro", split="test")
            
            data_list = list(dataset)
            random.seed(42)
            if len(data_list) > sample_size:
                sampled_data = random.sample(data_list, sample_size)
            else:
                sampled_data = data_list
            
            print(f"✅ Successfully loaded MMLU-Pro dataset from HuggingFace, original count: {len(data_list)}, sampled count: {len(sampled_data)}")
            return sampled_data
            
        except Exception as e:
            print(f"❌ HuggingFace loading failed: {e}")
            raise Exception("Failed to load MMLU-Pro dataset. Please check network connection or local files")

    async def process_element_with_redundant_prompt(self, element, redundancy_level, semaphore):
        """Process sample with redundant prompt (provide 1 correct answer + redundancy_level incorrect answers)"""
        
        question = element["question"]
        options_list = element["options"]
        # Get correct answer index using correct_answers field
        correct_answer_indices = element.get("correct_answers", [0])
        correct_index = correct_answer_indices[0] if correct_answer_indices else 0
        # Convert index to letter label (A, B, C, ...)
        correct_answer_letter = chr(ord('A') + correct_index)
        
        # Create options dictionary A, B, C, ... -> option content
        option_labels = [chr(ord('A') + i) for i in range(len(options_list))]
        options_dict = {label: content for label, content in zip(option_labels, options_list)}
        
        # Correct answer label
        correct_label = correct_answer_letter
        
        # Select wrong options to keep based on redundancy_level
        wrong_labels = [label for label in option_labels if label != correct_label]
        
        # If redundancy_level exceeds available wrong options, use all wrong options
        if redundancy_level >= len(wrong_labels):
            selected_wrong_labels = wrong_labels
        else:
            selected_wrong_labels = random.sample(wrong_labels, redundancy_level)
        
        # Build final options list (correct answer + selected wrong answers)
        final_labels = [correct_label] + selected_wrong_labels
        final_labels.sort()  # Sort by letter
        
        # Build options text
        options_text = ""
        for label in final_labels:
            options_text += f"{label}. {options_dict[label]}\n"
        
        prompt = (
            f"Question: {question}\n\n"
            f"Options:\n{options_text}\n"
            f"Please choose the correct answer by selecting the corresponding letter (e.g., A, B, C, ...)."
        )
        
        # Process request using API client
        async with semaphore:
            try:
                # Build message format
                msg = [{"role": "user", "content": prompt}]
                # Add timeout mechanism
                answer = await asyncio.wait_for(
                    self.api_client.call_openai(msg),
                    timeout=60.0
                )
            except asyncio.TimeoutError:
                print(f"⚠️  API call timed out, returning default value")
                answer = "A"  # Default return A
            except Exception as e:
                print(f"⚠️  API call error: {e}")
                answer = "A"  # Default return A
        
        return {
            "question_index": element.get("question_id", "unknown"),
            "answer": answer,
            "correct_answer": correct_label,
            "provided_options": final_labels,
            "redundancy_level": redundancy_level,
            "total_options": len(final_labels),
            "prompt": prompt
        }
    
    async def run_redundancy_experiment(self, dataset: List[Dict], redundancy_level: int):
        """Run experiment with a single redundancy level"""
        
        print(f"\n🔄 Starting redundancy level {redundancy_level} experiment...")
        print(f"   (1 correct answer + {redundancy_level} incorrect answers)")
        
        semaphore = asyncio.Semaphore(50)  # Control concurrency
        
        # Create task list
        tasks = [
            asyncio.create_task(
                self.process_element_with_redundant_prompt(element, redundancy_level, semaphore)
            )
            for element in dataset
        ]
        
        # Execute tasks and show progress bar
        results = []
        bar = tqdm(
            total=len(tasks),
            desc=f"Redundancy Level {redundancy_level}",
            unit="sample",
            ncols=100,
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
        )
        
        for coro in asyncio.as_completed(tasks):
            result = await coro
            results.append(result)
            bar.update(1)
        
        bar.close()
        
        correct_count = 0
        for result in results:
            model_answer = result["answer"].strip().upper()
            correct_answer = result["correct_answer"]
            
            # Extract option letter from model's answer
            if correct_answer in model_answer:
                correct_count += 1
        
        accuracy = correct_count / len(results) if results else 0
        
        print(f"✅ Redundancy level {redundancy_level} completed:")
        print(f"   Accuracy: {accuracy:.2%} ({correct_count}/{len(results)})")
        print(f"   Average number of options: {sum(len(r['provided_options']) for r in results) / len(results):.1f}")
        
        return {
            "redundancy_level": redundancy_level,
            "accuracy": accuracy,
            "correct_count": correct_count,
            "total_count": len(results),
            "detailed_results": results
        }

    def calculate_performance_degradation(self, results: Dict) -> Dict:
        """Calculate performance degradation trend"""
        if not results:
            return {}
        
        # Get baseline accuracy (redundancy level 1)
        baseline_accuracy = results.get(1, {}).get("accuracy", 0)
        
        degradation = {}
        for level, result in results.items():
            accuracy = result["accuracy"]
            degradation[str(level)] = {
                "accuracy": accuracy,
                "degradation_from_baseline": baseline_accuracy - accuracy,
                "relative_degradation": ((baseline_accuracy - accuracy) / baseline_accuracy * 100) if baseline_accuracy > 0 else 0
            }
        
        return degradation
    
    async def run_experiment(self, dataset: List[Dict], model_name: str, dataset_name: str, 
                           output_folder: str) -> Dict[str, Any]:
        """Run complete redundant options experiment"""
        # If no dataset is provided, load MMLU-Pro dataset
        if dataset is None:
            dataset = self.load_mmlu_pro_dataset(sample_size=300)
        
        print(f"Dataset: {dataset_name}")
        print(f"Model: {model_name}")
        print(f"Sample count: {len(dataset)}")
        print(f"Redundancy levels: 1-9 (9 experiments)")
        print("=" * 70)
        
        all_results = {}
        
        # Run 9 experiments with different redundancy levels (1-9 incorrect options)
        for redundancy_level in range(1, 10):
            try:
                result = await self.run_redundancy_experiment(dataset, redundancy_level)
                all_results[redundancy_level] = result
                
            except Exception as e:
                print(f"❌ Redundancy level {redundancy_level} experiment failed: {e}")
                continue
        
        # ───── Results Analysis ─────
        print("\n" + "=" * 70)
        print("📊 Redundant Options Experiment Results Summary")
        print("=" * 70)
        
        # Print results for each redundancy level
        print(f"{'Redundancy':<8} {'Options':<8} {'Accuracy':<10} {'Correct':<10}")
        print("-" * 40)
        
        for redundancy_level, result in all_results.items():
            total_options = 1 + redundancy_level  # 1 correct + redundancy_level incorrect
            accuracy = result["accuracy"]
            correct_count = result["correct_count"]
            total_count = result["total_count"]
            
            print(f"{redundancy_level:<8} {total_options:<8} {accuracy:.2%} {correct_count}/{total_count}")
        
        # Save results
        output_data = {
            "experiment_info": {
                "dataset": dataset_name,
                "model": model_name,
                "total_samples": len(dataset),
                "redundancy_levels": list(range(1, 10)),
                "experiment_type": "redundant_prompt"
            },
            "results": all_results,
            "analysis": {
                "accuracy_by_redundancy": {str(level): result["accuracy"] for level, result in all_results.items()},
                "performance_degradation": self.calculate_performance_degradation(all_results)
            }
        }
        
        # Create output folder
        os.makedirs(output_folder, exist_ok=True)
        
        # Save detailed results
        output_filename = os.path.join(
            output_folder,
            f"{model_name}_{os.path.basename(dataset_name).replace('.json', '')}_redundant_prompt_experiment.json"
        )
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
        
        # Save simplified accuracy results
        accuracy_summary = {
            "model": model_name,
            "dataset": dataset_name,
            "sample_size": len(dataset),
            "accuracy_results": {f"redundancy_{level}": result["accuracy"] for level, result in all_results.items()}
        }
        
        accuracy_filename = os.path.join(
            output_folder,
            f"{model_name}_{os.path.basename(dataset_name).replace('.json', '')}_accuracy_summary.json"
        )
        with open(accuracy_filename, "w", encoding="utf-8") as f:
            json.dump(accuracy_summary, f, indent=4, ensure_ascii=False)
        
        print(f"\n💾 Results saved:")
        print(f"  Detailed results: {output_filename}")
        print(f"  Accuracy summary: {accuracy_filename}")
        print(f"\n🎉 Redundant Options Experiment completed!")
        
        return {
            "all_results": all_results,
            "output_files": {
                "detailed_results": output_filename,
                "accuracy_summary": accuracy_filename
            }
        }