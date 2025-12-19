#!/usr/bin/env python3
"""
Download Electrotubbie's Turkic Languages Dataset - ROBUST VERSION

Automatically detects field names regardless of structure.
"""

from datasets import load_dataset
from pathlib import Path
from collections import defaultdict, Counter

print("📥 Downloading Electrotubbie's Turkic Languages Dataset...")
print("=" * 70)

# Load dataset
ds = load_dataset("Electrotubbie/classification_Turkic_languages")

print(f"✅ Downloaded successfully!")

# Get data
available_splits = list(ds.keys())
print(f"   Available splits: {available_splits}")

if 'train' in ds:
    data = ds['train']
else:
    data = ds[available_splits[0]]

print(f"   Total samples: {len(data)}")
print()

# Inspect first sample to understand structure
print("🔍 Dataset structure:")
first_sample = data[0]
all_fields = list(first_sample.keys())
print(f"   All fields: {all_fields}")
print()

print("   First sample content:")
for field, value in first_sample.items():
    if isinstance(value, str):
        display_value = value[:80] + "..." if len(value) > 80 else value
    else:
        display_value = value
    print(f"     {field}: {display_value}")
print()

# Auto-detect label field (usually the non-text field)
label_field = None
text_field = None

# Strategy: text field has long strings, label field has short values
for field in all_fields:
    sample_value = first_sample[field]
    
    # Check if this looks like a text field
    if isinstance(sample_value, str) and len(sample_value) > 50:
        text_field = field
    # Check if this looks like a label field
    elif isinstance(sample_value, (int, str)) and (not isinstance(sample_value, str) or len(str(sample_value)) < 20):
        label_field = field

# If auto-detection failed, ask user or make educated guess
if not text_field:
    print("❌ Could not auto-detect text field!")
    print(f"   Available fields: {all_fields}")
    print("   Please manually identify the text field and update the script.")
    exit(1)

if not label_field:
    print("❌ Could not auto-detect label field!")
    print(f"   Available fields: {all_fields}")
    print("   Please manually identify the label field and update the script.")
    exit(1)

print(f"✅ Detected fields:")
print(f"   Text field: '{text_field}'")
print(f"   Label field: '{label_field}'")
print()

# Get all labels
all_labels = [sample[label_field] for sample in data]
label_counts = Counter(all_labels)
unique_labels = sorted(set(all_labels))

print(f"📊 Label analysis:")
print(f"   Unique labels: {unique_labels}")
print(f"   Number of languages: {len(unique_labels)}")
print()

print("   Distribution:")
for label, count in sorted(label_counts.items()):
    print(f"     {label}: {count} samples ({count/len(data)*100:.1f}%)")
print()

# Show sample text for each label (to help identify languages)
print("🔍 Sample text for each label:")
for label in unique_labels:
    for sample in data:
        if sample[label_field] == label:
            text = sample[text_field][:100]
            print(f"   Label '{label}': {text}...")
            break
print()

# Create label mapping with better detection
print("📝 Creating language mapping...")
label_to_language = {}

for label in unique_labels:
    label_str = str(label).lower()
    
    # Multiple detection strategies
    detected = False
    
    # Strategy 1: Exact matches
    if label in [0, '0', 'ba', 'bashkir', 'Bashkir', 'bak', 'bas']:
        label_to_language[label] = 'bashkir'
        detected = True
    elif label in [1, '1', 'kk', 'kazakh', 'Kazakh', 'kaz']:
        label_to_language[label] = 'kazakh'
        detected = True
    elif label in [2, '2', 'ky', 'kyrgyz', 'Kyrgyz', 'Kirghiz', 'kir', 'kyr']:
        label_to_language[label] = 'kyrgyz'
        detected = True
    
    # Strategy 2: Substring matching
    if not detected:
        if 'bash' in label_str or 'баш' in label_str:
            label_to_language[label] = 'bashkir'
            detected = True
        elif 'kaz' in label_str or 'каз' in label_str or 'qaz' in label_str:
            label_to_language[label] = 'kazakh'
            detected = True
        elif 'kyr' in label_str or 'kir' in label_str or 'қыр' in label_str:
            label_to_language[label] = 'kyrgyz'
            detected = True
    
    # Strategy 3: Use sample text to detect (look for specific characters)
    if not detected:
        # Get a sample text for this label
        sample_texts = [sample[text_field] for sample in data if sample[label_field] == label][:10]
        combined_sample = ' '.join(sample_texts[:3])
        
        # Bashkir-specific characters: ҡ, ғ, ҙ, ҫ, ү, һ, ә, ө
        # Kazakh-specific: ұ, қ, ң, ғ, ү, ұ, һ, і, ә, ө
        # Kyrgyz-specific: ң, ү, ө
        
        bashkir_chars = set('ҡҙҫ')
        kazakh_chars = set('ұі')
        
        text_chars = set(combined_sample.lower())
        
        if bashkir_chars & text_chars:
            label_to_language[label] = 'bashkir'
            detected = True
        elif kazakh_chars & text_chars:
            label_to_language[label] = 'kazakh'
            detected = True
    
    # Fallback: couldn't detect
    if not detected:
        label_to_language[label] = f"unknown_{label}"
        print(f"   ⚠️  Warning: Couldn't identify label '{label}'")

print()
for label, language in sorted(label_to_language.items()):
    count = label_counts[label]
    print(f"   {label} → {language} ({count} samples)")
print()

# Ask user to confirm if any unknowns
unknowns = [lang for lang in label_to_language.values() if lang.startswith('unknown_')]
if unknowns:
    print("⚠️  WARNING: Some labels could not be identified!")
    print("   Please review the sample texts above and update the mapping.")
    print()
    response = input("Continue anyway? (y/n): ")
    if response.lower() != 'y':
        print("Aborted.")
        exit(0)
    print()

# Create output directory
output_dir = Path(__file__).parent.parent / "data"
output_dir.mkdir(parents=True, exist_ok=True)

# Group by language
print("📝 Grouping and saving data...")
data_by_language = defaultdict(list)

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