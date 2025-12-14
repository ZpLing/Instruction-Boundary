# MMLU-Pro 300 Samples Setup

## Overview
This repository requires a `mmlu_pro_300_samples.json` file containing 300 samples from the MMLU-Pro dataset.

## Quick Setup

### Option 1: Using the provided script (Recommended)

1. Install the datasets library:
```bash
pip install datasets
```

2. Run the creation script:
```bash
python create_mmlu_pro_300.py
```

This will automatically download 300 samples from HuggingFace and format them correctly.

### Option 2: Manual download from HuggingFace

1. Visit: https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro
2. Download the test split
3. Use the `create_mmlu_pro_300.py` script to format and sample 300 items

### Option 3: Local MMLU-Pro directory

If you have a local MMLU-Pro dataset:

1. Place it in `./MMLU-Pro/` directory
2. Run: `python create_mmlu_pro_300.py`

The script will automatically detect and use the local dataset.

## Expected Format

The `mmlu_pro_300_samples.json` file should contain a list of 300 items with the following structure:

```json
[
  {
    "id": "mmlu_pro_0",
    "question": "Question text here",
    "options": ["0. Option A", "1. Option B", "2. Option C", "3. Option D"],
    "correct_answers": [0],
    "correct_options": ["0. Option A"],
    "num_options": 4,
    "num_correct": 1,
    "dataset_source": "mmlu_pro",
    "question_type": "single_choice"
  }
]
```

## Verification

After creating the file, verify it has 300 samples:

```bash
python3 -c "import json; f=open('mmlu_pro_300_samples.json'); d=json.load(f); print(f'{len(d)} samples')"
```

Expected output: `300 samples`

