#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - Main Runner
Unified experiment execution entry
"""

import asyncio
import argparse
import sys
import os
from typing import List, Dict, Any

# Add src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.model_config import get_model_config, get_experiment_config, SUPPORTED_MODELS
from config.experiment_config import get_output_folder, get_execution_order, create_output_directories
from core.data_loader import ChoiceDataLoader
from experiments.Vanilla_Scenario import Experiment_Vanilla_Scenario
from experiments.Multi_turn_Dialogue import Experiment_Multi_turn_Dialogue
from experiments.Conformity import Experiment_Conformity
from experiments.Disturbing_Miscellany import Experiment_Disturbing_Miscellany
from experiments.Few_shot_Learning import Experiment_Few_shot_Learning
from experiments.Missing_Choices import Experiment_Missing_Choices
from experiments.Vaugeness import Experiment_Vaugeness
from experiments.Prompt_Polishing import Experiment_Prompt_Polishing

class ChoiceToolkit:
    """Choice Experiment Toolkit Main Class"""
    
    def __init__(self, model_name: str = None):
        self.model_config = get_model_config(model_name)
        self.data_loader = ChoiceDataLoader(self.model_config)
        self.experiments = {}
        self._initialize_experiments()
    
    def _initialize_experiments(self):
        """Initialize experiment modules"""
        # Register all experiments
        self.experiments = {
            "1": Experiment_Vanilla_Scenario(self.model_config),
            "2": Experiment_Multi_turn_Dialogue(self.model_config),
            "3": Experiment_Conformity(self.model_config),
            "4": Experiment_Disturbing_Miscellany(self.model_config),
            "5": Experiment_Few_shot_Learning(self.model_config),
            "6": Experiment_Missing_Choices(self.model_config),
            "7": Experiment_Vaugeness(self.model_config),
            "8": Experiment_Prompt_Polishing(self.model_config),
        }
    
    async def run_single_experiment(self, experiment_id: str, dataset: List[Dict], 
                                 dataset_name: str) -> Dict[str, Any]:
        """Run a single experiment"""
        if experiment_id not in self.experiments:
            raise ValueError(f"Unsupported experiment ID: {experiment_id}")
        
        experiment = self.experiments[experiment_id]
        # Use path relative to project root
        output_folder = f"../outputs/{get_output_folder(experiment_id)}"
        
        print(f"\n{'='*50}")
        print(f"Starting dataset processing: {dataset_name}")
        print(f"Experiment type: {get_experiment_config(experiment_id)['name']}")
        print(f"{'='*50}")
        
        # Run experiment
        result = await experiment.run_experiment(
            dataset, self.model_config['test_model'], dataset_name, output_folder
        )
        
        print(f"\n🎉 {dataset_name} Experiment {experiment_id} completed!")
        return result
    
    async def run_experiments(self, experiment_ids: List[str]) -> Dict[str, Any]:
        """Run multiple experiments"""
        print("🚀 Starting Choice Experiment Toolkit")
        print("=" * 80)
        
        # Create output directories - only for experiments to be run
        create_output_directories(experiment_ids, "../outputs")
        
        # Get dataset files
        dataset_files = self.data_loader.get_all_dataset_files()
        if not dataset_files:
            print("❌ No dataset files found")
            return {}
        
        all_results = {}
        
        # Run experiments for each dataset
        for dataset_file in dataset_files:
            print(f"\n{'='*70}")
            print(f"📁 Processing dataset: {dataset_file}")
            print(f"{'='*70}")
            
            try:
                # Load dataset
                dataset, question_types, dataset_name = self.data_loader.load_and_prepare_dataset(
                    dataset_file, self.data_loader.load_dataset_config()
                )
                
                if not dataset:
                    continue
                
                # Use all samples for experiment
                print(f"   Using all {len(dataset)} samples for experiment")
                
                dataset_results = {}
                
                # Run specified experiments
                for experiment_id in experiment_ids:
                    if experiment_id in self.experiments:
                        try:
                            result = await self.run_single_experiment(
                                experiment_id, dataset, dataset_name
                            )
                            dataset_results[experiment_id] = result
                        except Exception as e:
                            print(f"❌ Error running experiment {experiment_id}: {e}")
                            continue
                    else:
                        print(f"⚠️  Experiment {experiment_id} not yet implemented")
                
                all_results[dataset_file] = dataset_results
                
            except Exception as e:
                print(f"❌ Error processing dataset {dataset_file}: {e}")
                continue
        
        # Generate comprehensive report
        print(f"\n{'='*80}")
        print("📊 Comprehensive Experiment Results Report")
        print(f"{'='*80}")
        
        for dataset_file, dataset_results in all_results.items():
            print(f"\n📁 Dataset: {dataset_file}")
            for experiment_id, result in dataset_results.items():
                print(f"   ✅ Experiment {experiment_id} completed")
        
        print(f"\n🎊 All Choice experiments completed!")
        return all_results

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Choice Experiment Toolkit")
    
    parser.add_argument(
        "--model", 
        type=str, 
        choices=SUPPORTED_MODELS,
        default="gpt-4o",
        help="Specify test model"
    )
    
    parser.add_argument(
        "--experiment",
        type=str,
        help="Specify experiment IDs to run, separated by commas"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all experiments"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available experiments"
    )
    
    return parser.parse_args()

def list_experiments():
    """List all available experiments"""
    print("Available experiments:")
    print("-" * 50)
    
    experiments = {
        "1": "Vanilla Scenario",
        "2": "Multi-turn Dialogue",
        "3": "Conformity",
        "4": "Disturbing Miscellany",
        "5": "Few-shot Learning",
        "6": "Missing Choices",
        "7": "Vaugeness",
        "8": "Prompt Polishing",
    }
    
    for exp_id, description in experiments.items():
        status = "✅ Implemented"
        print(f"  {exp_id:>8}: {description:<20} {status}")

async def main():
    """Main function"""
    args = parse_arguments()
    
    if args.list:
        list_experiments()
        return
    
    # Determine which experiments to run
    if args.all:
        experiment_ids = get_execution_order()
    elif args.experiment:
        experiment_ids = [exp.strip() for exp in args.experiment.split(',')]
    else:
        print("Please specify experiments to run (--experiment) or run all experiments (--all)")
        return
    
    # Create toolkit instance
    toolkit = ChoiceToolkit(args.model)
    
    # Run experiments
    try:
        results = await toolkit.run_experiments(experiment_ids)
        print(f"\n✅ Experiments completed! Results saved in outputs/ directory")
    except Exception as e:
        print(f"❌ Error running experiments: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
