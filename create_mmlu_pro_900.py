#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create MMLU-Pro 900 samples dataset
"""

import json
import random
import os

def create_mmlu_pro_900():
    """Create MMLU-Pro 900 samples dataset from HuggingFace"""
    try:
        from datasets import load_dataset
        
        print("🔄 Loading MMLU-Pro dataset from HuggingFace...")
        dataset = load_dataset("TIGER-Lab/MMLU-Pro", split="test")
        
        data_list = list(dataset)
        print(f"✅ Loaded {len(data_list)} samples from HuggingFace")
        
        # Random sampling with seed for reproducibility
        random.seed(42)
        if len(data_list) >= 900:
            sampled_data = random.sample(data_list, 900)
        else:
            sampled_data = data_list
            print(f"⚠️ Only {len(data_list)} samples available, using all")
        
        # Convert to our format
        formatted_data = []
        for idx, item in enumerate(sampled_data):
            # Handle different possible field names
            question = item.get('question', item.get('Question', ''))
            options = item.get('options', item.get('Options', []))
            answer = item.get('answer', item.get('Answer', 0))
            
            # Ensure options are formatted correctly
            if isinstance(options, list):
                formatted_options = [f"{i}. {opt}" if not opt.startswith(f"{i}.") else opt 
                                   for i, opt in enumerate(options)]
            else:
                formatted_options = []
            
            formatted_item = {
                'id': f"mmlu_pro_{idx}",
                'question': question,
                'options': formatted_options,
                'correct_answers': [answer] if isinstance(answer, int) else [0],
                'correct_options': [formatted_options[answer]] if formatted_options and isinstance(answer, int) else [],
                'num_options': len(formatted_options),
                'num_correct': 1,
                'dataset_source': 'mmlu_pro',
                'question_type': 'single_choice'
            }
            formatted_data.append(formatted_item)
        
        # Save to file
        output_file = 'mmlu_pro_900_samples.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(formatted_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Saved {len(formatted_data)} samples to: {output_file}")
        return output_file
        
    except ImportError:
        print("❌ datasets library not installed")
        print("   Please install: pip install datasets")
        return None
    except Exception as e:
        print(f"❌ Error loading MMLU-Pro: {e}")
        print("\n💡 Alternative: If you have a local MMLU-Pro dataset,")
        print("   place it in ./MMLU-Pro/ directory and run this script again")
        return None

if __name__ == "__main__":
    create_mmlu_pro_900()

