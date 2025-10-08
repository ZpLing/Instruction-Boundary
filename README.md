# 🎯 Choice Experiment Toolkit

<div align="center">

**A comprehensive toolkit for evaluating LLM instruction following capabilities through multiple choice experiments**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green.svg)](https://openai.com/)

</div>

This toolkit implements **8 experimental settings** that systematically evaluate how Large Language Models (LLMs) handle instruction following in multiple choice scenarios. The experiments are adapted from the original TFU (Truth Following Under Uncertainty) framework, providing a standardized approach to assess model behavior across different prompt strategies and cognitive biases.

## ✨ Key Features

- 🔬 **8 Comprehensive Experiments**: Systematic evaluation of instruction following capabilities
- 🎨 **Dual Format Support**: Automatic detection and conversion between Choice and TFU formats
- 🤖 **Multi-Model Support**: Compatible with GPT-4o, Claude, Llama, and Gemini
- 📊 **Rich Evaluation Metrics**: Follow rate, Jump rate, and TFU-style analysis
- 🚀 **Easy-to-Use**: Command-line interface and Python API
- 📈 **Detailed Outputs**: Comprehensive results with statistical analysis

## 🚀 Quick Start

### 📦 Installation

```bash
# Clone the repository
git clone https://github.com/ZpLing/Instruction-Boundary.git
cd Instruction-Boundary/src/scripts

# Install dependencies
pip install -r requirements.txt
```

### 🔑 API Configuration

```bash
# Set your API key
export API_KEY="your-api-key-here"

# Optional: Set custom base URL (for custom API endpoints)
export BASE_URL="https://api.openai.com/v1"
```

> ⚠️ **Security Note**: Never commit your actual API key to the repository. Always use environment variables. In addition, we use the Openai SDK, so the official Claude API Request is not supported.

### 🎮 Running Experiments

```bash
# 📋 List all available experiments
python src/scripts/main.py --list

# 🚀 Run all experiments
python src/scripts/main.py --all

# 🎯 Run specific experiments
python src/scripts/main.py --experiment 1,2 

# 🤖 Run with specific model
python src/scripts/main.py --model gpt-4o --experiment 1

# 📊 Quick test (recommended for first run)
python src/scripts/test_api.py
python src/scripts/test_toolkit.py
```

### ⚡ 30-Second Demo

```bash
# Quick start with interactive menu
python src/scripts/quick_start.py
```


## 🧪 Experimental Settings

The toolkit implements **8 comprehensive experimental settings** that systematically evaluate different aspects of LLM instruction following behavior:

<div align="center">

| 🎯 Experiment | 📝 Description | 🔬 Focus Area |
|---------------|----------------|---------------|
| **1** | Vanilla Scenario | Information Completeness |
| **2** | Multi-turn Dialogue | Self-Reflection |
| **3** | Conformity | Social Bias | 
| **4** | Disturbing Miscellany | Robustness |
| **5** | Few-shot Learning | Learning from Examples |
| **6** | Missing Choices | Information Completeness |
| **7** | Vaugeness | Uncertainty Handling |
| **8** | Prompt Polishing | Prompt Optimization |

</div>

### 🔬 Detailed Experimental Descriptions

#### 📘 **1 - Vanilla Scenario**
- **Objective**: Ensure information completeness and unbiased guidance
- **Method**: Use comprehensive prompts with detailed instructions
- **Metrics**: Accuracy, coverage, unbiasedness
- **Insight**: Establishes a baseline for model performance

#### 🔄 **2 - Multi-turn Conversation**
- **Objective**: Assess self-reflection and iterative improvement
- **Method**: Two-round conversations with reflection prompts
- **Metrics**: Improvement rate, consistency, self-correction
- **Insight**: Tests reasoning and self-correction abilities

#### 👥 **3 - Conformity**
- **Objective**: Evaluate susceptibility to social bias
- **Method**: Include misleading hints about "popular" answers
- **Metrics**: Conformity rate, bias resistance, critical thinking
- **Insight**: Tests independence from social influence

#### 🌀 **4 - Disturbing Miscellany**
- **Objective**: Test robustness against distracting information
- **Method**: Add unrelated options to the prompt
- **Metrics**: Deviation rate, accuracy under distraction, resilience
- **Insight**: Measures model's ability to ignore irrelevant details

#### 🎓 **5 - Few-shot Learning**
- **Objective**: Assess model's ability to learn from examples
- **Method**: Provide 1-3 example demonstrations before target questions
- **Metrics**: Learning curve, example utilization, generalization
- **Insight**: Evaluates in-context learning capabilities

#### 🚫 **6 - Missing Choices**
- **Objective**: Assess impact of incomplete options on decision-making
- **Method**: Omit some correct options from the prompt
- **Metrics**: Omission detection, decision bias, accuracy
- **Insight**: Evaluates model's reliance on complete information

#### ❓ **7 - Vaugeness**
- **Objective**: Test model behavior with unclear instructions
- **Method**: Use minimal, vague prompts with reduced guidance
- **Metrics**: Uncertainty handling, interpretation consistency
- **Insight**: Measures robustness to ambiguous inputs

#### ✨ **8 - Prompt Polishing**
- **Objective**: Test if model-generated prompts improve performance
- **Method**: Use LLM-refined versions of insufficient prompts
- **Metrics**: Prompt effectiveness, self-improvement capability
- **Insight**: Evaluates model's prompt optimization skills

## 📁 Project Structure

```
Demo/
├── 📁 src/                              # Source code directory
│   ├── 📁 config/                        # Configuration files
│   │   ├── __init__.py                   # Package initialization
│   │   ├── experiment_config.py          # Experiment parameters
│   │   └── model_config.py               # Model and API settings
│   ├── 📁 core/                          # Core functionality
│   │   ├── __init__.py                   # Package initialization
│   │   ├── api_client.py                 # API communication
│   │   ├── data_loader.py                # Dataset loading and processing
│   │   ├── evaluator.py                  # Evaluation metrics
│   │   └── utils.py                      # Utility functions
│   ├── 📁 dataset/                       # Datasets
│   │   ├── choice_config.json            # Dataset configuration
│   │   ├── choice_tfu_format_dataset.json # TFU format dataset
│   │   └── mixed_450_qa_dataset.json     # Choice format dataset (450 samples)
│   ├── 📁 experiments/                   # Individual experiment implementations
│   │   ├── __init__.py                   # Package initialization
│   │   ├── Conformity.py                 # Bandwagon effect experiment
│   │   ├── Disturbing_Miscellany.py      # Insufficient information experiment
│   │   ├── Few_shot_Learning.py          # Few-shot learning experiment
│   │   ├── Missing_Choices.py            # Missing options experiment
│   │   ├── Multi_turn_Dialogue.py        # Multi-turn conversation experiment
│   │   ├── Prompt_Polishing.py           # LLM polished prompts experiment
│   │   ├── Vanilla_Scenario.py           # Standard scenario experiment
│   │   └── Vaugeness.py                  # Ambiguous prompts experiment
│   ├── 📁 outputs/                       # Output directories (auto-created)
│   └── 📁 scripts/                       # Execution scripts
│       ├── example_usage.py              # Usage examples
│       ├── main.py                       # Main execution script
│       ├── quick_start.py                # Interactive quick start
│       ├── test_api.py                   # API connection test
│       └── test_toolkit.py               # Comprehensive tests
├── 📋 requirements.txt                   # Python dependencies
└── 📖 README.md                          # This file
```

## 📊 Dataset Formats

The toolkit supports **dual dataset formats** with automatic detection and seamless conversion:

### 🎯 **Choice Format** (Standard Multiple Choice)
```json
{
  "question": "What is the capital of France?",
  "options": ["London", "Berlin", "Paris", "Madrid"],
  "correct_answers": [2],
  "question_type": "single_choice"
}
```
- **File**: `mixed_450_qa_dataset.json`
- **Style**: Direct question-answer with option selection
- **Use Case**: Standard multiple choice evaluation

### 🔍 **TFU Format** (Evidence-Based Reasoning)
```json
{
  "Conclusion": "Paris is the capital of France",
  "Facts": "Paris is located in northern France and serves as the political center...",
  "correct_answers": [0],
  "question_type": "single_choice"
}
```
- **File**: `choice_tfu_format_dataset.json`
- **Style**: Evidence-based reasoning (proven/disproven/undetermined)
- **Use Case**: TFU-style cognitive evaluation

### 🔄 **Automatic Format Detection**
The toolkit intelligently detects format based on field presence:
- **Choice format**: `question` + `options` fields
- **TFU format**: `Conclusion` + `Facts` fields
- **Auto-conversion**: TFU format internally converted to Choice format

## 📈 Output & Results

Results are automatically saved in the `results/` directory with comprehensive analysis:

```
outputs/
├── 📁 experiment_data_choice_Multi_turn_Dialogue/           # Experiment 2 results
│   └── 📄 gpt-4o_mixed_450_qa_ambiguous_evaluation.json
└── 📁 experiment_data_choice_Prompt_Polishing/           # Experiment 8 results
    └── 📄 gpt-4o_mixed_450_qa_prompt_polishing_evaluation.json
```

### 📊 **Output File Types**

| 📄 File Type | 📝 Description | 🔍 Content |
|--------------|----------------|------------|
| **Evaluation Results** | Detailed responses and analysis | Model outputs, extracted labels, judge evaluations |
| **Accuracy Analysis** | Performance metrics | Follow rate, Jump rate, overall accuracy |
| **TFU-style Metrics** | Specialized evaluation | Cognitive bias analysis, reasoning patterns |

### 📈 **Key Metrics**

- **🎯 Follow Rate**: Percentage of correct single-choice answers
- **🚀 Jump Rate (No Answer)**: Accuracy on "no correct answer" questions  
- **🚀 Jump Rate (Multiple)**: Accuracy on multiple-choice questions
- **📊 Overall Accuracy**: Total correctness across all question types
- **🔍 Extraction Method Stats**: Keyword vs LLM judge usage
- **📋 Output Distribution**: Response pattern analysis

## 💻 Usage Examples

### 🚀 **Basic Python Usage**

```python
import asyncio
from main import ChoiceToolkit

async def basic_experiment():
    # Initialize toolkit with specific model
    toolkit = ChoiceToolkit(model_name="gpt-4o")
    
    # Run single experiment
    results = await toolkit.run_single_experiment("1", dataset, "mixed_450_qa")
    
    # Print results
    print(f"Experiment completed with {len(results)} samples")

# Run the experiment
asyncio.run(basic_experiment())
```

### 🔬 **Advanced Multi-Experiment Setup**

```python
async def comprehensive_evaluation():
    # Initialize toolkit
    toolkit = ChoiceToolkit(model_name="gpt-4o")
    
    # Define experiment suite
    experiments = ["1", "2", "3", "4"]
    
    # Run multiple experiments
    results = await toolkit.run_experiments(experiments)
    
    # Analyze results
    for exp_id, result in results.items():
        print(f"Experiment {exp_id}: {result['overall_accuracy']:.3f} accuracy")

# Execute comprehensive evaluation
asyncio.run(comprehensive_evaluation())
```

### 🤖 **Multi-Model Comparison**

```python
async def model_comparison():
    models = ["gpt-4o", "claude-3-7-sonnet-20250219", "llama-3.1-8b-instruct"]
    
    for model in models:
        print(f"\n🧪 Testing {model}...")
        toolkit = ChoiceToolkit(model_name=model)
        results = await toolkit.run_experiments(["1"])
        print(f"✅ {model} completed")

# Run model comparison
asyncio.run(model_comparison())
```

### 📱 **Command Line Interface**

```bash
# 🎯 Run specific experiments
python main.py --experiment 1,2,3 --model gpt-4o

# 🚀 Run all experiments
python main.py --all --model claude-3-7-sonnet-20250219

# 📋 List available experiments
python main.py --list

# ⚡ Interactive quick start
python quick_start.py

# 🧪 Run test suite
python test_api.py
python test_toolkit.py
```

### 📊 **Custom Dataset Usage**

```python
# Load custom dataset
from core.data_loader import ChoiceDataLoader

data_loader = ChoiceDataLoader(config)
custom_dataset, types, name = data_loader.load_and_prepare_dataset("your_dataset.json")

# Run experiments on custom data
toolkit = ChoiceToolkit()
results = await toolkit.run_single_experiment("2", custom_dataset, name)
```

## 🤖 Supported Models

The toolkit supports a wide range of state-of-the-art language models:

<div align="center">

| 🏢 Provider | 🤖 Model | 🎯 Recommended Use | ⚡ Speed |
|-------------|----------|-------------------|----------|
| **OpenAI** | GPT-4o | Primary evaluation | Fast |
| **OpenAI** | GPT-3.5-turbo | Cost-effective testing | Very Fast |
| **Anthropic** | Claude-3-7-sonnet-20250219 | Advanced reasoning | Fast |
| **Meta** | Llama-3.1-8b-instruct | Open-source alternative | Medium |
| **Google** | Gemini-2.0-flash | Latest capabilities | Fast |

</div>

> 💡 **Tip**: Start with GPT-4o for best results, then use other models for comparison studies.

## 📚 Citation & Research

If you use this toolkit in your research, please cite:

```bibtex
@article{instruction_boundary_2025,
  title={Instruction Boundary: A Comprehensive Toolkit for LLM Instruction Following Evaluation},
  author={[Author Names]},
  journal={arXiv preprint arXiv:2509.20278},
  year={2025},
  url={https://github.com/ZpLing/Instruction-Boundary}
}
```

### 🔬 **Research Applications**
- **Cognitive Science**: Understanding LLM reasoning patterns
- **AI Safety**: Evaluating instruction following robustness
- **Prompt Engineering**: Optimizing prompt strategies
- **Model Comparison**: Benchmarking different LLMs
- **Bias Detection**: Identifying cognitive biases in AI systems

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 **Bug Reports**
- Use GitHub Issues to report bugs
- Include reproduction steps and environment details

### 🚀 **Feature Requests**
- Suggest new experimental settings
- Propose additional evaluation metrics
- Request new model support

### 💻 **Code Contributions**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📖 **Documentation**
- Improve README sections
- Add code examples
- Translate documentation

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**🎯 Choice Experiment Toolkit** - *Evaluating LLM Instruction Following Capabilities*

[⭐ Star this repo](https://github.com/ZpLing/Instruction-Boundary) • [🐛 Report Bug](https://github.com/ZpLing/Instruction-Boundary/issues) • [💡 Request Feature](https://github.com/ZpLing/Instruction-Boundary/issues)

Made with ❤️ for the AI research community

</div>