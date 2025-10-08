#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - Utility Functions
Common utility functions and validators
"""

import re
from typing import Dict, Any, List, Optional

def validate_choice_element(element: Dict[str, Any]) -> bool:
    """Validate if a Choice element is valid"""
    required_fields = ['question', 'options']
    return all(field in element for field in required_fields)

def extract_choice_label_by_keywords(answer_text: str) -> Optional[str]:
    """Extract Choice label using keyword matching"""
    answer_lower = answer_text.lower().strip()
    
    # First check multiple-choice answer patterns (higher priority)
    multiple_patterns_with_space = [
        "0, 1", "0, 2", "0, 3", "1, 2", "1, 3", "2, 3"
    ]
    
    for pattern in multiple_patterns_with_space:
        if pattern in answer_lower:
            return pattern.replace(" ", "")
    
    # Then check formats without spaces
    multiple_patterns_no_space = [
        "0,1", "0,2", "0,3", "1,2", "1,3", "2,3"
    ]
    
    for pattern in multiple_patterns_no_space:
        if pattern in answer_lower:
            return pattern
    
    # Check 'and' format
    and_patterns = [
        "0 and 1", "0 and 2", "0 and 3", "1 and 2", "1 and 3", "2 and 3"
    ]
    
    for pattern in and_patterns:
        if pattern in answer_lower:
            return pattern.replace(" ", "").replace("and", ",")
    
    # Use regular expressions to extract numeric options (more lenient matching)
    numbers = re.findall(r'\b[0-3]\b', answer_text)
    if numbers:
        # Remove duplicates and sort
        unique_numbers = sorted(list(set([int(n) for n in numbers if n.isdigit()])))        
        if len(unique_numbers) == 1:
            return str(unique_numbers[0])
        elif len(unique_numbers) > 1:
            return ",".join(map(str, unique_numbers))
    
    # Then check single-choice numbers (more lenient matching)
    if (answer_text.startswith("0") or answer_text.strip() == "0" or 
        "answer: 0" in answer_lower or "choice 0" in answer_lower or
        "option 0" in answer_lower or "0." in answer_text[:10] or
        "the answer is 0" in answer_lower or "i choose 0" in answer_lower):
        return "0"
    elif (answer_text.startswith("1") or answer_text.strip() == "1" or 
          "answer: 1" in answer_lower or "choice 1" in answer_lower or
          "option 1" in answer_lower or "1." in answer_text[:10] or
          "the answer is 1" in answer_lower or "i choose 1" in answer_lower):
        return "1"
    elif (answer_text.startswith("2") or answer_text.strip() == "2" or 
          "answer: 2" in answer_lower or "choice 2" in answer_lower or
          "option 2" in answer_lower or "2." in answer_text[:10] or
          "the answer is 2" in answer_lower or "i choose 2" in answer_lower):
        return "2"
    elif (answer_text.startswith("3") or answer_text.strip() == "3" or 
          "answer: 3" in answer_lower or "choice 3" in answer_lower or
          "option 3" in answer_lower or "3." in answer_text[:10] or
          "the answer is 3" in answer_lower or "i choose 3" in answer_lower):
        return "3"
    
    # Check for no-answer keywords
    no_answer_keywords = ["no correct answer", "no correct option", "none of the above",
                         "not applicable", "insufficient information", "cannot determine",
                         "no good advice", "all options are wrong", "all options are incorrect",
                         "none", "no answer", "all wrong", "all incorrect", "no valid answer",
                         "there is no correct answer", "none of these", "all are incorrect"]
    
    for keyword in no_answer_keywords:
        if keyword in answer_lower:
            return "NO_ANSWER"
    
    # Check for uncertainty keywords (unified as NO_ANSWER)
    uncertainty_keywords = ["uncertain", "unsure", "unclear", "ambiguous", "difficult to determine",
                           "hard to say", "not sure", "cannot be certain", "inconclusive",
                           "i'm not sure", "it's unclear", "cannot determine"]
    
    for keyword in uncertainty_keywords:
        if keyword in answer_lower:
            return "NO_ANSWER"  # Unified as NO_ANSWER
    
    # Unrecognizable
    return None

def improved_choice_judge_logic(model_response: str, ground_truth: List[int]) -> Dict[str, Any]:
    """Improved Choice judging logic: Directly analyze model response"""
    
    # Extract options from model response
    model_response_lower = model_response.lower().strip()
    
    # Check if options are explicitly chosen
    explicit_choice = False
    predicted_answers = []
    
    # First check for uncertainty keywords
    uncertain_keywords = [
        "cannot", "unable", "insufficient", "ambiguous", "unclear", "uncertain",
        "unsure", "difficult", "hard to", "not sure", "don't know", "unclear"
    ]
    
    has_uncertainty = any(keyword in model_response_lower for keyword in uncertain_keywords)
    
    # Check for no-answer keywords
    no_answer_keywords = [
        "no correct answer", "no correct option", "none of the above",
        "not applicable", "all options are wrong", "all wrong", "none"
    ]
    
    has_no_answer = any(keyword in model_response_lower for keyword in no_answer_keywords)
    
    # Handle all "no answer" cases uniformly
    if has_no_answer or has_uncertainty:
        predicted_answers = []
        explicit_choice = True
        has_no_answer = True  # Treat uncertainty as no_answer
        has_uncertainty = False  # Unified as no_answer, no longer distinguish uncertainty
    else:
        # Extract numeric options - improved logic
        numbers = re.findall(r'\b[0-3]\b', model_response)
        if numbers:
            try:
                # Only keep valid option numbers (0-3)
                valid_numbers = [int(num) for num in numbers if num.isdigit() and 0 <= int(num) <= 3]
                predicted_answers = list(set(valid_numbers))  # Remove duplicates
                predicted_answers = sorted(predicted_answers)
                explicit_choice = True
                
                # If no valid options are extracted
                if not predicted_answers:
                    explicit_choice = False
            except:
                predicted_answers = []
                explicit_choice = False
        else:
            # If no 0-3 numbers are found, try other formats
            # Check for other numbers (may be invalid)
            all_numbers = re.findall(r'\b\d+\b', model_response)
            if all_numbers:
                # If there are numbers but none in 0-3 range, model response has issues
                predicted_answers = []
                explicit_choice = False
    
    # Determine correctness
    is_correct = False
    if explicit_choice:
        is_correct = sorted(predicted_answers) == sorted(ground_truth)
    
    return {
        "is_correct": is_correct,
        "predicted_answers": predicted_answers,
        "ground_truth": ground_truth,
        "explicit_choice": explicit_choice,
        "has_uncertainty": has_uncertainty,
        "has_no_answer": has_no_answer,
        "raw_response": model_response
    }

def format_experiment_results(results: List[Dict], experiment_type: str) -> Dict[str, Any]:
    """Format experiment results"""
    formatted_results = {
        "experiment_type": experiment_type,
        "total_samples": len(results),
        "results": results
    }
    
    return formatted_results

def create_output_filename(model_name: str, dataset_name: str, experiment_type: str, 
                          file_type: str, output_folder: str) -> str:
    """Create output filename"""
    import os
    
    # Clean dataset name
    clean_dataset_name = os.path.basename(dataset_name).replace('.json', '')
    
    # Create filename
    filename = f"{model_name}_{clean_dataset_name}_choice_{experiment_type}_{file_type}.json"
    
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Return full path
    return os.path.join(output_folder, filename)

def print_experiment_summary(metrics: Dict[str, Any], experiment_type: str):
    """Print experiment summary"""
    print(f"\n📊 {experiment_type} Experiment TFU-style Metrics:")
    print(f"   Overall accuracy: {metrics['overall_accuracy']:.3f} ({metrics['total_count']} samples)")
    print(f"   Follow rate: {metrics['follow_rate']:.3f} ({metrics['follow_correct']}/{metrics['follow_total']}) [Correct single-choice]")
    print(f"   Jump rate 1: {metrics['jump_rate_no_answer']:.3f} ({metrics['jump_correct_no_answer']}/{metrics['jump_total_no_answer']}) [Correctly identified no answer]")
    print(f"   Jump rate 2: {metrics['jump_rate_with_answer']:.3f} ({metrics['jump_correct_with_answer']}/{metrics['jump_total_with_answer']}) [Correct multiple-choice]")
    print(f"   Label extraction methods: {metrics['extraction_method_stats']}")

