#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - Usage Example
Demonstrates how to use the Choice experiment toolkit
"""

import asyncio
import sys
import os

# Add src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ChoiceToolkit

async def example_usage():
    """Usage example"""
    
    print("Choice Experiment Toolkit Usage Example")
    print("=" * 50)
    
    # Create toolkit instance
    toolkit = ChoiceToolkit(model_name="gpt-4o")
    
    # Experiment ID list
    print("\nAvailable Experiment IDs:")
    experiments = {
        "1": "Vanilla Scenario",
        "2": "Multi-turn Dialogue",
        "3": "Conformity",
        "4": "Disturbing Miscellany",
        "5": "Few-shot Learning",
        "6": "Missing Choices",
        "7": "Vaugeness",
        "8": "Prompt Polishing"
    }
    for exp_id, exp_name in experiments.items():
        print(f"{exp_id}: {exp_name}")

    # Example 1: Run single experiment
    print("\nExample 1: Run single experiment (Vanilla Scenario)")
    try:
        results = await toolkit.run_experiments(["1"])
        print("✅ Vanilla Scenario experiment completed")
    except Exception as e:
        print(f"❌ Experiment failed: {e}")
    
    # Example 2: Run multiple experiments
    print("\nExample 2: Run multiple experiments (Vanilla Scenario, Multi-turn Dialogue)")
    try:
        results = await toolkit.run_experiments(["1", "2"])
        print("✅ Multiple experiments completed")
    except Exception as e:
        print(f"❌ Experiments failed: {e}")
    
    # Example 3: Run all experiments
    print("\nExample 3: Run all experiments")
    try:
        results = await toolkit.run_experiments(["1", "2", "3", "4", "5", "6", "7", "8"])
        print("✅ All experiments completed")
    except Exception as e:
        print(f"❌ Experiments failed: {e}")

if __name__ == "__main__":
    asyncio.run(example_usage())
