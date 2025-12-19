#!/usr/bin/env python3
"""
Download MMTEB TurkicClassification Dataset (Combined Format)
"""

from datasets import load_dataset
from pathlib import Path
from collections import defaultdict

print("📥 Downloading MMTEB TurkicClassification dataset...")
print("=" * 70)

dataset = load_dataset("mteb/TurkicClassification")

print(f"✅ Downloaded successfully!")
print(f"   Train samples: {len(dataset['train'])}")
print(f"   Test samples: {len(dataset['test'])}")
print()

label_to_language = {
    0: 'bashkir',
    1: 'kazakh',
    2: 'kyrgyz'
}

output_dir = Path(__file__).parent.parent / "data"
output_dir.mkdir(parents=True, exist_ok=True)

print("📝 Processing all data (train + test combined)...")
all_data = defaultdict(list)

for sample in dataset['train']:
    language = label_to_language[sample['label']]
    all_data[language].append(sample['text'])

for sample in dataset['test']:
    language = label_to_language[sample['label']]
    all_data[language].append(sample['text'])

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
print("⚠️  WARNING: These files contain BOTH train and test data!")
print("   For proper evaluation, use download_mmteb_dataset.py instead")
print("   to keep train/test separate.")