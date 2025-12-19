#!/usr/bin/env python3
"""
Download MMTEB TurkicClassification Dataset (Combined Format)

Downloads and combines train+test splits into single files per language

Usage:
    cd /home/colin/Turkic-Languages-Audio-to-Text-Transcription/project/training-scripts
    python download_mmteb_combined.py
    
Output:
    /home/colin/Turkic-Languages-Audio-to-Text-Transcription/project/data/
    ├── bashkir_combined.txt (all samples)
    ├── kazakh_combined.txt (all samples)
    └── kyrgyz_combined.txt (all samples)
"""

from datasets import load_dataset
from pathlib import Path
from collections import defaultdict

print("📥 Downloading MMTEB TurkicClassification dataset...")
print("=" * 70)

# Download dataset
dataset = load_dataset("mteb/TurkicClassification", "ba")

print(f"✅ Downloaded successfully!")

# Check what splits exist
available_splits = list(dataset.keys())
print(f"   Available splits: {available_splits}")
print(f"   Total samples: {sum(len(dataset[split]) for split in available_splits)}")
print()

# Label mapping
label_to_language = {
    0: 'bashkir',
    1: 'kazakh',
    2: 'kyrgyz'
}

# Create output directory
output_dir = Path(__file__).parent.parent / "data"
output_dir.mkdir(parents=True, exist_ok=True)

# Combine all data from all splits
print("📝 Processing all data from all available splits...")
all_data = defaultdict(list)

# Process all available splits
for split_name in available_splits:
    print(f"   Processing '{split_name}' split ({len(dataset[split_name])} samples)...")
    for sample in dataset[split_name]:
        language = label_to_language[sample['label']]
        all_data[language].append(sample['text'])

# Save combined files
print()
for language, texts in all_data.items():
    filepath = output_dir / f"{language}_combined.txt"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(texts))
    print(f"✅ {language}: {len(texts)} samples → {filepath}")

print()
print("=" * 70)
print("✅ Dataset download complete!")
print()
print("📊 Summary:")
total = sum(len(v) for v in all_data.values())
print(f"   Total samples: {total}")
for language, texts in all_data.items():
    print(f"   {language.capitalize()}: {len(texts)} samples")
print()
print(f"📂 Files saved to: {output_dir.absolute()}")
print()
print("ℹ️  Note: This dataset only has a 'train' split.")
print("   You'll need to create your own train/test split for evaluation.")