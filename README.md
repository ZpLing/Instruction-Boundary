# Choice Experiment Toolkit

## 🚀 Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Setup API Key
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Optional: Set custom base URL
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

### 4. Generate Visualizations
```bash
# Generate 3D waterfall plots
python 3D_line.py

# Generate radar charts
python Radar_Right.py
```

## 🧪 Experimental Settings

| Setting | Description |
|---------|-------------|
| **1.1_2.1** | Sufficient vs Insufficient Prompts |
| **1.2** | Few-shot Learning |
| **2.3** | Ambiguous Prompts |
| **2.5** | LLM Polished Prompts |
| **2.6** | Multi-turn Conversation |
| **2.8** | Bandwagon Effect |

## 📁 Structure

```
choice_toolkit/
├── config/                    # Configuration files
├── core/                      # Core functionality
├── experiments/               # Individual experiment implementations
├── results/                   # Output directories
├── main.py                    # Main execution script
├── mixed_450_qa_dataset.json  # Main dataset (450 samples)
├── 3D_line.py                # 3D visualization script
├── Radar_Right.py             # Radar chart visualization
└── requirements.txt           # Dependencies
```

## 📊 Output Files

Results are saved in `results/` directory:
- **Evaluation Results**: `{model}_{dataset}_choice_{experiment}_evaluation.json`
- **Accuracy Analysis**: `{model}_{dataset}_choice_{experiment}_accuracy.json`
- **Comparison Summaries**: `{model}_{dataset}_choice_sufficient_vs_insufficient_tfu_comparison.json`

## 🔧 Usage Examples

```python
from main import ChoiceToolkit

# Initialize toolkit
toolkit = ChoiceToolkit(model_name="gpt-4o")

# Run specific experiment
results = await toolkit.run_single_experiment("1.1_2.1", dataset, "mixed_450_qa")
```

## 📚 Citation

```bibtex
@article{instruction_boundary_2025,
  title={Instruction Boundary: A Comprehensive Toolkit for LLM Instruction Following Evaluation},
  author={[Author Names]},
  journal={arXiv preprint arXiv:2509.20278},
  year={2025}
}
```