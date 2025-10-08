#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - Test Script
Test basic functionality of the toolkit
"""

import asyncio
import sys
import os

# Add src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.model_config import get_model_config, SUPPORTED_MODELS
from config.experiment_config import get_output_folder, get_execution_order, create_output_directories
from core.data_loader import ChoiceDataLoader
from core.api_client import ChoiceAPIClient
from core.evaluator import ChoiceEvaluator

async def test_basic_functionality():
    """Test basic functionality"""
    
    print("Choice Toolkit Basic Functionality Test")
    print("=" * 50)
    
    # Test 1: Configuration loading
    print("\nTest 1: Configuration Loading")
    try:
        config = get_model_config("gpt-4o")
        print(f"✅ Model configuration loaded successfully: {config['test_model']}")
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False
    
    # Test 2: Data loader
    print("\nTest 2: Data Loader")
    try:
        data_loader = ChoiceDataLoader(config)
        dataset_files = data_loader.get_all_dataset_files()
        print(f"✅ Data loader initialized successfully, found datasets: {dataset_files}")
    except Exception as e:
        print(f"❌ Data loader initialization failed: {e}")
        return False
    
    # Test 3: API client
    print("\nTest 3: API Client")
    try:
        api_client = ChoiceAPIClient(config)
        print("✅ API client initialized successfully")
    except Exception as e:
        print(f"❌ API client initialization failed: {e}")
        return False
    
    # Test 4: Evaluator
    print("\nTest 4: Evaluator")
    try:
        evaluator = ChoiceEvaluator()
        print("✅ Evaluator initialized successfully")
    except Exception as e:
        print(f"❌ Evaluator initialization failed: {e}")
        return False
    
    # Test 5: Output directory creation
    print("\nTest 5: Output Directory Creation")
    try:
        create_output_directories("../test_outputs")
        print("✅ Output directories created successfully")
    except Exception as e:
        print(f"❌ Output directory creation failed: {e}")
        return False
    
    print("\n✅ All basic functionality tests passed!")
    return True

async def test_experiment_modules():
    """Test experiment modules"""
    
    print("\nExperiment Modules Test")
    print("=" * 50)
    
    # Test experiment module imports
    try:
        from experiments.Vanilla_Scenario import Experiment_Vanilla_Scenario
        from experiments.Multi_turn_Dialogue import Experiment_Multi_turn_Dialogue
        from experiments.Conformity import Experiment_Conformity
        from experiments.Disturbing_Miscellany import Experiment_Disturbing_Miscellany
        from experiments.Few_shot_Learning import Experiment_Few_shot_Learning
        from experiments.Missing_Choices import Experiment_Missing_Choices
        from experiments.Vaugeness import Experiment_Vaugeness
        from experiments.Prompt_Polishing import Experiment_Prompt_Polishing
        
        config = get_model_config("gpt-4o")
        
        # Test experiment module initialization
        experiments = {
            "1": Experiment_Vanilla_Scenario(config),
            "2": Experiment_Multi_turn_Dialogue(config),
            "3": Experiment_Conformity(config),
            "4": Experiment_Disturbing_Miscellany(config),
            "5": Experiment_Few_shot_Learning(config),
            "6": Experiment_Missing_Choices(config),
            "7": Experiment_Vaugeness(config),
            "8": Experiment_Prompt_Polishing(config),
        }
        
        print("✅ All experiment modules imported and initialized successfully")
        
        for exp_id, exp in experiments.items():
            print(f"   - Experiment {exp_id}: {type(exp).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Experiment modules test failed: {e}")
        return False

def test_configuration():
    """Test configuration system"""
    
    print("\nConfiguration System Test")
    print("=" * 50)
    
    try:
        # Test model configurations
        for model in SUPPORTED_MODELS:
            config = get_model_config(model)
            assert config['test_model'] == model
            print(f"✅ Model {model} configuration correct")
    
        execution_order = get_execution_order()
        print(f"✅ Experiment execution order: {execution_order}")
        
        for exp_id in execution_order:
            folder = get_output_folder(exp_id)
            print(f"   - Experiment {exp_id}: Output folder {folder}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration system test failed: {e}")
        return False

async def test_toolkit():
    """Main test function"""
    
    print("Choice Toolkit Comprehensive Test")
    print("=" * 60)
    
    # Run all tests
    tests = [
        ("Basic Functionality Test", test_basic_functionality()),
        ("Experiment Modules Test", test_experiment_modules()),
        ("Configuration System Test", test_configuration()),
    ]
    
    results = []
    for test_name, test_coro in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if asyncio.iscoroutine(test_coro):
                result = await test_coro
            else:
                result = test_coro
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} execution failed: {e}")
            results.append((test_name, False))
    
    # Summarize test results
    print(f"\n{'='*60}")
    print("Test Results Summary")
    print(f"{'='*60}")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ Passed" if result else "❌ Failed"
        print(f"  {test_name:<20}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Choice Toolkit is ready!")
        return 0
    else:
        print("⚠️  Some tests failed, please check configuration")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(test_toolkit())
    sys.exit(exit_code)
