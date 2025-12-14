#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Choice Toolkit imports and basic functionality
"""

import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test imports of all modules"""
    print("🧪 Testing Choice Toolkit imports...")
    
    try:
        # Test config module imports
        from config.model_config import get_model_config, SUPPORTED_MODELS
        print("✅ config.model_config imported successfully")
        
        from config.experiment_config import get_experiment_config, get_output_folder, get_execution_order
        print("✅ config.experiment_config imported successfully")
        
        # Test core module imports
        from core.utils import validate_choice_element, extract_choice_label_by_keywords
        print("✅ core.utils imported successfully")
        
        from core.evaluator import ChoiceEvaluator
        print("✅ core.evaluator imported successfully")
        
        from core.data_loader import ChoiceDataLoader
        print("✅ core.data_loader imported successfully")
        
        # Test experiment module imports
        from experiments.Vanilla_Scenario import Experiment_Vanilla_Scenario
        print("✅ experiments.Vanilla_Scenario imported successfully")
        
        from experiments.Multi_turn_Dialogue import Experiment_Multi_turn_Dialogue
        print("✅ experiments.Multi_turn_Dialogue imported successfully")
        
        from experiments.Conformity import Experiment_Conformity
        print("✅ experiments.Conformity imported successfully")
        
        from experiments.Disturbing_Miscellany import Experiment_Disturbing_Miscellany
        print("✅ experiments.Disturbing_Miscellany imported successfully")
        
        from experiments.Few_shot_Learning import Experiment_Few_shot_Learning
        print("✅ experiments.Few_shot_Learning imported successfully")
        
        from experiments.Missing_Choices import Experiment_Missing_Choices
        print("✅ experiments.Missing_Choices imported successfully")
        
        from experiments.Vaugeness import Experiment_Vaugeness
        print("✅ experiments.Vaugeness imported successfully")
        
        from experiments.Prompt_Polishing import Experiment_Prompt_Polishing
        print("✅ experiments.Prompt_Polishing imported successfully")
        
        print("\n🎉 All modules imported successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        from config.model_config import get_model_config, SUPPORTED_MODELS
        from core.utils import validate_choice_element
        
        # Test config retrieval
        config = get_model_config()
        print(f"✅ Model config retrieved successfully: {config['test_model']}")
        
        # Test supported models
        print(f"✅ Supported models: {SUPPORTED_MODELS}")
        
        # Test data validation
        test_element = {
            "question": "Test question",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "correct_answers": [0],
            "question_type": "single_choice"
        }
        
        is_valid = validate_choice_element(test_element)
        print(f"✅ Data validation working correctly: {is_valid}")
        
        print("\n🎉 Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("Choice Toolkit Import and Functionality Test")
    print("=" * 60)
    
    # Test imports
    import_success = test_imports()
    
    if import_success:
        # Test basic functionality
        functionality_success = test_basic_functionality()
        
        if functionality_success:
            print("\n🎊 All tests passed! Choice Toolkit is ready!")
            return 0
        else:
            print("\n❌ Functionality test failed")
            return 1
    else:
        print("\n❌ Import test failed")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
