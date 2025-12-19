#!/usr/bin/env python3
"""
Download MMTEB TurkicClassification Dataset - Universal Version
Handles any label structure
"""

from datasets import load_dataset
from pathlib import Path
from collections import defaultdict

print("📥 Downloading MMTEB TurkicClassification dataset...")
print("=" * 70)

dataset = load_dataset("mteb/TurkicClassification", "ba")
train_data = dataset['train']

print(f"✅ Downloaded successfully!")
print(f"   Total samples: {len(train_data)}")

# Inspect first sample to understand structure
print("\n🔍 Inspecting dataset structure...")
first_sample = train_data[0]
print(f"   Fields: {list(first_sample.keys())}")
print(f"   First sample: {first_sample}")

# Get unique labels
unique_labels = sorted(set(train_data['label']))
print(f"\n   Unique labels found: {unique_labels}")
print(f"   Number of unique labels: {len(unique_labels)}")

# Count per label
from collections import Counter
label_counts = Counter(train_data['label'])
print("\n📊 Samples per label:")
for label, count in sorted(label_counts.items()):
    print(f"   Label {label}: {count} samples")

# Create output directory
output_dir = Path(__file__).parent.parent / "data"
output_dir.mkdir(parents=True, exist_ok=True)

# Group by label
print("\n📝 Processing data...")
data_by_label = defaultdict(list)
for sample in train_data:
    label = sample['label']
    data_by_label[label].append(sample['text'])

# Save each label to file
print()
for label, texts in sorted(data_by_label.items()):
    filepath = output_dir / f"label_{label}.txt"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(texts))
    print(f"✅ Label {label}: {len(texts)} samples → {filepath}")

print()
print("=" * 70)
print("✅ Dataset download complete!")
print(f"\n📂 Files saved to: {output_dir.absolute()}")
print("\nℹ️  Files are named by their label numbers.")
print("   You'll need to manually identify which label is which language.")