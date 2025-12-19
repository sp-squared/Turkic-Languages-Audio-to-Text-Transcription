#!/usr/bin/env python3
"""
Download Electrotubbie's Turkic Languages Dataset (Method 1: datasets library)

Usage:
    python download_turkic_dataset_v1.py
"""

from datasets import load_dataset
from pathlib import Path
from collections import defaultdict, Counter

print("📥 Downloading Electrotubbie's Turkic Languages Dataset...")
print("   Method: datasets.load_dataset()")
print("=" * 70)

# Load dataset
ds = load_dataset("Electrotubbie/classification_Turkic_languages")

print(f"✅ Downloaded successfully!")

# Check structure
available_splits = list(ds.keys())
print(f"   Available splits: {available_splits}")

# Get data
if 'train' in ds:
    data = ds['train']
else:
    data = ds[available_splits[0]]

print(f"   Total samples: {len(data)}")
print()

# Inspect first sample
print("🔍 Dataset structure:")
first_sample = data[0]
print(f"   Columns: {list(first_sample.keys())}")
print(f"\n   First sample:")
for key, value in first_sample.items():
    if isinstance(value, str) and len(value) > 80:
        print(f"     {key}: {value[:80]}...")
    else:
        print(f"     {key}: {value}")
print()

# Determine label field name
label_field = None
for field in ['label', 'labels', 'category', 'language', 'lang']:
    if field in first_sample:
        label_field = field
        break

if not label_field:
    print("❌ Could not find label field!")
    print(f"   Available fields: {list(first_sample.keys())}")
    exit(1)

print(f"📊 Using '{label_field}' as label field")

# Count labels
all_labels = [sample[label_field] for sample in data]
label_counts = Counter(all_labels)
unique_labels = sorted(set(all_labels))

print(f"   Unique labels: {unique_labels}")
print(f"\n   Distribution:")
for label, count in sorted(label_counts.items()):
    print(f"     {label}: {count} samples")
print()

# Show sample text for each label
print("🔍 Sample texts per label:")
for label in unique_labels:
    for sample in data:
        if sample[label_field] == label:
            text_field = 'text' if 'text' in sample else 'sentence'
            text = sample[text_field][:100]
            print(f"   {label}: {text}...")
            break
print()

# Create label mapping
print("📝 Creating label mapping...")
label_to_language = {}

for label in unique_labels:
    label_str = str(label).lower()
    
    # Try to detect language
    if label in [0, '0', 'ba', 'bashkir', 'Bashkir', 'bak']:
        label_to_language[label] = 'bashkir'
    elif label in [1, '1', 'kk', 'kazakh', 'Kazakh', 'kaz']:
        label_to_language[label] = 'kazakh'
    elif label in [2, '2', 'ky', 'kyrgyz', 'Kyrgyz', 'Kirghiz', 'kir']:
        label_to_language[label] = 'kyrgyz'
    elif 'bash' in label_str:
        label_to_language[label] = 'bashkir'
    elif 'kaz' in label_str:
        label_to_language[label] = 'kazakh'
    elif 'kyr' in label_str or 'kir' in label_str:
        label_to_language[label] = 'kyrgyz'
    else:
        # Unknown - ask user or use label as-is
        label_to_language[label] = f"language_{label}"

for label, language in sorted(label_to_language.items()):
    count = label_counts[label]
    print(f"   {label} → {language} ({count} samples)")
print()

# Create output directory
output_dir = Path(__file__).parent.parent / "data"
output_dir.mkdir(parents=True, exist_ok=True)

# Group by language
print("📝 Grouping data by language...")
data_by_language = defaultdict(list)

text_field = 'text' if 'text' in first_sample else 'sentence'

for sample in data:
    label = sample[label_field]
    text = sample[text_field]
    language = label_to_language[label]
    data_by_language[language].append(text)

# Save files
print()
for language, texts in sorted(data_by_language.items()):
    filepath = output_dir / f"{language}_combined.txt"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(texts))
    print(f"✅ {language}: {len(texts)} samples → {filepath}")

print()
print("=" * 70)
print("✅ Dataset download complete!")
print()
print("📊 Final Summary:")
total = sum(len(v) for v in data_by_language.values())
print(f"   Total samples: {total}")
for language, texts in sorted(data_by_language.items()):
    print(f"   {language.capitalize()}: {len(texts)} samples")
print()
print(f"📂 Files saved to: {output_dir.absolute()}")