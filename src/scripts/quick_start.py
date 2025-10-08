#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - Quick Start Script
Provides simplified startup method
"""

import asyncio
import sys
import os

# Add src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def print_banner():
    """Print welcome banner"""
    print("=" * 80)
    print("🎯 Choice Experiment End-to-End Toolkit")
    print("   Unified Choice experiment toolkit")
    print("   Supports 8 experiment types, clear file saving paths")
    print("=" * 80)

def print_menu():
    """Print menu"""
    print("\nPlease select an operation:")
    print("1. Run all experiments")
    print("2. Run single experiment")
    print("3. Run multiple experiments")
    print("4. List all experiments")
    print("5. Test toolkit")
    print("6. Test API connection")
    print("7. Show usage examples")
    print("0. Exit")

def get_experiment_choice():
    """Get experiment choice"""
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
    
    print("\nAvailable experiments:")
    for exp_id, exp_name in experiments.items():
        descriptions = {
            "1": "Experiment Vanilla Scenario",
            "2": "Experiment Multi-turn Dialogue",
            "3": "Experiment Conformity", 
            "4": "Experiment Disturbing Miscellany",
            "5": "Experiment Few-shot Learning",
            "6": "Experiment Missing Choices",
            "7": "Experiment Vaugeness",
            "8": "Experiment Prompt Polishing",
        }
        print(f"  {exp_id}. {exp_name}: {descriptions[exp_id]}")
    
    return experiments

async def run_all_experiments():
    """Run all experiments"""
    print("\n🚀 Running all experiments...")
    from main import ChoiceToolkit
    
    toolkit = ChoiceToolkit("gpt-4o")
    results = await toolkit.run_experiments(["1", "2", "3", "4", "5", "6", "7", "8"])
    print("✅ All experiments completed!")

async def run_single_experiment(exp_id):
    """Run single experiment"""
    print(f"\n🚀 Running experiment {exp_id}...")
    from main import ChoiceToolkit
    
    toolkit = ChoiceToolkit("gpt-4o")
    results = await toolkit.run_experiments([exp_id])
    print(f"✅ Experiment {exp_id} completed!")

async def run_multiple_experiments(exp_ids):
    """Run multiple experiments"""
    print(f"\n🚀 Running experiments {', '.join(exp_ids)}...")
    from main import ChoiceToolkit
    
    toolkit = ChoiceToolkit("gpt-4o")
    results = await toolkit.run_experiments(exp_ids)
    print(f"✅ Experiments {', '.join(exp_ids)} completed!")

def list_experiments():
    """List all experiments"""
    from main import list_experiments
    list_experiments()

async def test_toolkit():
    """Test toolkit"""
    print("\n🧪 Testing toolkit...")
    from test_toolkit import test_toolkit as toolkit_test
    await toolkit_test()

def test_api_connection():
    """Test API connection"""
    print("\n🔗 Testing API connection...")
    from test_api import test_api_connection as api_test
    api_test()

def show_usage_example():
    """Show usage examples"""
    print("\n📖 Usage examples:")
    print("=" * 50)
    print("1. Command line usage:")
    print("   python main.py --all                    # Run all experiments")
    print("   python main.py --experiment 1     # Run single experiment")
    print("   python main.py --experiment 1,2 # Run multiple experiments")
    print("   python main.py --list                   # List all experiments")
    print("   python main.py --model gpt-4o           # Specify model")
    print()
    print("2. Programming usage:")
    print("   from main import ChoiceToolkit")
    print("   toolkit = ChoiceToolkit('gpt-4o')")
    print("   results = await toolkit.run_experiments(['1'])")
    print()
    print("3. Result files:")
    print("   outputs/experiment_data_choice_Vanilla_Scenario/     # Vanilla Scenario experiment results")
    print("   outputs/experiment_data_choice_Multi-turn_Dialogue/     # Multi-turn Dialogue experiment results")
    print("   outputs/experiment_data_choice_Conformity/     # Conformity experiment results")
    print("   outputs/experiment_data_choice_Disturbing_Miscellany/     # Disturbing Miscellany experiment results")
    print("   outputs/experiment_data_choice_Few-shot_Learning/     # Few-shot Learning experiment results")
    print("   outputs/experiment_data_choice_Missing_Choices/     # Missing Choices experiment results")
    print("   outputs/experiment_data_choice_Vaugeness/     # Vaugeness experiment results")
    print("   outputs/experiment_data_choice_Prompt_Polishing/     # Prompt Polishing experiment results")

async def main():
    """Main function"""
    print_banner()
    
    while True:
        print_menu()
        choice = input("\nPlease enter your choice (0-7): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            await run_all_experiments()
        elif choice == "2":
            experiments = get_experiment_choice()
            exp_choice = input("Please select experiment (1-8): ").strip()
            if exp_choice in experiments:
                await run_single_experiment(exp_choice)
            else:
                print("❌ Invalid choice")
        elif choice == "3":
            experiments = get_experiment_choice()
            print("Please select multiple experiments, separated by commas (e.g: 1,2,3):")
            exp_choices = input().strip().split(',')
            exp_ids = []
            for exp_choice in exp_choices:
                exp_choice = exp_choice.strip()
                if exp_choice in experiments:
                    exp_ids.append(exp_choice)
            if exp_ids:
                await run_multiple_experiments(exp_ids)
            else:
                print("❌ Invalid choices")
        elif choice == "4":
            list_experiments()
        elif choice == "5":
            await test_toolkit()
        elif choice == "6":
            test_api_connection()
        elif choice == "7":
            show_usage_example()
        else:
            print("❌ Invalid choice, please try again")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted by user, goodbye!")
    except Exception as e:
        print(f"\n❌ Program error: {e}")
        sys.exit(1)
