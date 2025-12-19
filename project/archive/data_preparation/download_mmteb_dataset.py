#!/usr/bin/env python3
"""
Download MMTEB TurkicClassification Dataset

Downloads the official train/test split from HuggingFace
and saves as separate text files.

Usage:
    python download_mmteb_dataset.py
    
Output:
    data/
    ├── train/
    │   ├── bashkir_train.txt
    │   ├── kazakh_train.txt
    │   └── kyrgyz_train.txt
    └── test/
        ├── bashkir_test.txt
        ├── kazakh_test.txt
        └── kyrgyz_test.txt
"""

from datasets import load_dataset
from pathlib import Path
from collections import defaultdict

print("📥 Downloading MMTEB TurkicClassification dataset...")
print("=" * 70)

# Download dataset
dataset = load_dataset("mteb/TurkicClassification")

print(f"✅ Downloaded successfully!")
print(f"   Train samples: {len(dataset['train'])}")
print(f"   Test samples: {len(dataset['test'])}")
print()

# Label mapping
label_to_language = {
    0: 'bashkir',
    1: 'kazakh',
    2: 'kyrgyz'
}

# Create output directories
output_dir = Path("data")
train_dir = output_dir / "train"
test_dir = output_dir / "test"

train_dir.mkdir(parents=True, exist_ok=True)
test_dir.mkdir(parents=True, exist_ok=True)

# Process train split
print("📝 Processing training data...")
train_data = defaultdict(list)

for sample in dataset['train']:
    language = label_to_language[sample['label']]
    train_data[language].append(sample['text'])

# Save train files
for language, texts in train_data.items():
    filepath = train_dir / f"{language}_train.txt"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(texts))
    print(f"   ✅ {language}: {len(texts)} samples → {filepath}")

print()

# Process test split
print("📝 Processing test data...")
test_data = defaultdict(list)

for sample in dataset['test']:
    language = label_to_language[sample['label']]
    test_data[language].append(sample['text'])

# Save test files
for language, texts in test_data.items():
    filepath = test_dir / f"{language}_test.txt"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(texts))
    print(f"   ✅ {language}: {len(texts)} samples → {filepath}")

print()
print("=" * 70)
print("✅ Dataset download complete!")
print()
print("📊 Summary:")
print(f"   Training samples: {sum(len(v) for v in train_data.values())}")
print(f"   Test samples: {sum(len(v) for v in test_data.values())}")
print(f"   Total: {len(dataset['train']) + len(dataset['test'])} samples")
print()
print("📂 Files saved to:")
print(f"   {train_dir}/")
print(f"   {test_dir}/")
print()
print("💡 Next steps:")
print("   1. Use train files for training")
print("   2. Use test files for evaluation (never train on these!)")
print("   3. Run train_sklearn_PROPER.py for proper evaluation")
