# Choice Experiment Toolkit

A comprehensive toolkit for evaluating LLM instruction following capabilities through multiple choice experiments. This toolkit implements 6 experimental settings that correspond to the original TFU (Truth Following Under Uncertainty) experiments, adapted for multiple choice question formats.

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/ZpLing/Instruction-Boundary.git
cd Instruction-Boundary

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup API Key
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Optional: Set custom base URL (for custom API endpoints)
export OPENAI_BASE_URL="https://api.openai.com/v1"
```

**Important**: Never commit your actual API key to the repository. Use environment variables instead.

### 3. Run Experiments
```bash
# List available experiments
python main.py --list-experiments

# Run all experiments
python main.py --all

# Run specific experiments
python main.py --experiment 1.1_2.1,2.3

# Run with specific model
python main.py --model gpt-4o --experiment 1.1_2.1
```


## 🧪 Experimental Settings

The toolkit implements 6 experimental settings that correspond to the original TFU experiments:

| Setting | Description | Original TFU Experiment |
|---------|-------------|------------------------|
| **1.1_2.1** | Sufficient vs Insufficient Prompts | exp_TFU_1.1_2.1.py |
| **1.2** | Few-shot Learning | exp_TFU_1.2.py |
| **2.3** | Ambiguous Prompts | exp_TFU_2.3.py |
| **2.5** | LLM Polished Prompts | exp_TFU_2.5.py |
| **2.6** | Multi-turn Conversation | exp_TFU_2.6.py |
| **2.8** | Bandwagon Effect | exp_TFU_2.8.py |

### Experimental Details

**1.1_2.1 - Sufficient vs Insufficient Prompts**
- Tests model behavior with complete vs incomplete information
- Sufficient: Provides all necessary context and options
- Insufficient: Removes critical information or options

**1.2 - Few-shot Learning**
- Evaluates model's ability to learn from examples
- Uses 2-3 example demonstrations before the target question

**2.3 - Ambiguous Prompts**
- Tests model behavior with unclear or ambiguous instructions
- Measures how models handle uncertainty in prompts

**2.5 - LLM Polished Prompts**
- Uses LLM-generated refined prompts based on insufficient prompts
- Tests if model-generated prompts improve performance

**2.6 - Multi-turn Conversation**
- Implements two-round conversations with self-reflection
- First round: Initial response, Second round: Reflection and refinement

**2.8 - Bandwagon Effect**
- Tests conformity behavior with misleading social cues
- Includes hints about "typical" incorrect answers

## 📁 Structure

```
choice_toolkit/
├── config/                    # Configuration files
├── core/                      # Core functionality
├── experiments/               # Individual experiment implementations
├── results/                   # Output directories
├── main.py                    # Main execution script
├── mixed_450_qa_dataset.json  # Choice format dataset (450 samples)
├── choice_tfu_format_dataset.json  # TFU format dataset (450 samples)
└── requirements.txt           # Dependencies
```

## 📊 Supported Dataset Formats

The toolkit supports two dataset formats with automatic format detection and conversion:

### Choice Format
- **File**: `mixed_450_qa_dataset.json`
- **Fields**: `question`, `options`, `correct_answers`, `question_type`
- **Description**: Standard multiple choice format
- **Prompt Style**: Direct question-answer format with option selection

### TFU Format  
- **File**: `choice_tfu_format_dataset.json`
- **Fields**: `Conclusion`, `Facts`, `correct_answers`, `question_type`
- **Description**: TFU-style format with facts and conclusions
- **Prompt Style**: Evidence-based reasoning format (proven/disproven/undetermined)
- **Auto-conversion**: Automatically converted to Choice format internally

### Format Detection
The toolkit automatically detects dataset format based on field presence:
- **Choice format**: Contains `question` and `options` fields
- **TFU format**: Contains `Conclusion` and `Facts` fields

### Prompt Adaptation
- **Choice format**: Uses standard multiple choice prompts
- **TFU format**: Uses evidence-based reasoning prompts (corresponds to original TFU experiments)

## 📊 Output Files

Results are saved in `results/` directory with the following structure:

```
results/
├── experiment_data_choice_1_1_2_1/
│   ├── {model}_{dataset}_choice_sufficient_evaluation.json
│   ├── {model}_{dataset}_choice_insufficient_evaluation.json
│   └── {model}_{dataset}_choice_sufficient_vs_insufficient_tfu_comparison.json
├── experiment_data_choice_1_2/
│   └── {model}_{dataset}_choice_few_shot_evaluation.json
└── ...
```

### File Types
- **Evaluation Results**: Detailed evaluation results for each experiment
- **Accuracy Analysis**: Accuracy metrics and statistics
- **Comparison Summaries**: Comparative analysis between different prompt types
- **TFU-style Metrics**: Follow rate, Jump rate, and other TFU-style metrics

## 🔧 Usage Examples

### Basic Usage
```python
from main import ChoiceToolkit

# Initialize toolkit
toolkit = ChoiceToolkit(model_name="gpt-4o")

# Run specific experiment
results = await toolkit.run_single_experiment("1.1_2.1", dataset, "mixed_450_qa")
```

### Advanced Usage
```python
# Run multiple experiments
experiment_ids = ["1.1_2.1", "2.3", "2.6"]
results = await toolkit.run_experiments(experiment_ids)

# Run with different models
models = ["gpt-4o", "claude-3-7-sonnet-20250219", "llama-3.1-8b-instruct"]
for model in models:
    toolkit = ChoiceToolkit(model_name=model)
    await toolkit.run_experiments()
```

### Command Line Usage
```bash
# Run all experiments with specific model
python main.py --model gpt-4o --all

# Run specific experiments
python main.py --experiment 1.1_2.1,2.3,2.6

# List available experiments
python main.py --list-experiments
```

## 🧪 Supported Models

- **GPT-4o**: OpenAI's latest model
- **GPT-3.5-turbo**: OpenAI's efficient model
- **Claude-3-7-sonnet-20250219**: Anthropic's advanced model
- **Llama-3.1-8b-instruct**: Meta's open-source model
- **Gemini-2.0-flash**: Google's latest model

## 📚 Citation

If you use this toolkit in your research, please cite:

```bibtex
@article{instruction_boundary_2025,
  title={Instruction Boundary: A Comprehensive Toolkit for LLM Instruction Following Evaluation},
  author={[Author Names]},
  journal={arXiv preprint arXiv:2509.20278},
  year={2025}
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.