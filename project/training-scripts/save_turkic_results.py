try:
    from datasets import load_dataset
except Exception:
    import importlib, subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "datasets"])
    importlib.invalidate_caches()
    from datasets import load_dataset

try:
    from latin_to_cyrillic_turkic import latin_to_cyrillic
except Exception:
    def latin_to_cyrillic(text, lang):
        return text

import re
import os

def has_latin_characters(s):
    return bool(re.search(r'[A-Za-z]', s))

# Load dataset
print("Loading dataset...")
dataset = load_dataset("mteb/TurkicClassification", "ba")
print(f"✓ Loaded {len(dataset['train'])} samples\n")

# Process and save results
results = []
converted_count = 0

print("Processing samples...")
for example in dataset['train']:
    text = example.get('text', '')
    
    # Convert if needed
    if has_latin_characters(text):
        text = latin_to_cyrillic(text, "ba")
        converted_count += 1
    
    # Add to results
    results.append(text)

print(f"✓ Processed {len(results)} samples")
print(f"✓ Converted {converted_count} samples from Latin to Cyrillic\n")

# Define output path - changed to network location
output_path = r'/home/colin/Turkic-Languages-Audio-to-Text-Transcription/project/data/turkic_bashkir_classification_results.txt'

# Ensure the directory exists (for network paths, ensure you have permissions)
try:
    # Try to create directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        print(f"Warning: Directory {output_dir} does not exist.")
        print("Attempting to create directory...")
        try:
            os.makedirs(output_dir, exist_ok=True)
            print(f"✓ Directory created or already exists")
        except Exception as e:
            print(f"✗ Failed to create directory: {e}")
            print("Falling back to current directory...")
            output_path = 'turkic_classification_results.txt'
except Exception as e:
    print(f"✗ Error with network path: {e}")
    print("Falling back to current directory...")
    output_path = 'turkic_classification_results.txt'

# Save to file
print(f"\nSaving to file: {output_path}")
try:
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, text in enumerate(results, 1):
            f.write(f"{'='*60}\n")
            f.write(f"Sample {i}\n")
            f.write(f"{'='*60}\n")
            f.write(f"{text}\n\n")
    
    print(f"✓ Successfully saved to {output_path}")
    print(f"✓ File contains {len(results)} text samples")
    
except PermissionError:
    print(f"✗ Permission denied. Cannot write to {output_path}")
    print("Please ensure you have write permissions to the network location.")
    print("Falling back to current directory...")
    
    # Fallback to local file
    output_path = 'turkic_classification_results.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, text in enumerate(results, 1):
            f.write(f"{'='*60}\n")
            f.write(f"Sample {i}\n")
            f.write(f"{'='*60}\n")
            f.write(f"{text}\n\n")
    print(f"✓ Saved to current directory: {output_path}")
    
except Exception as e:
    print(f"✗ Error saving file: {e}")
    print("Attempting to save in current directory...")
    
    # Final fallback
    output_path = 'turkic_classification_results.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, text in enumerate(results, 1):
            f.write(f"{'='*60}\n")
            f.write(f"Sample {i}\n")
            f.write(f"{'='*60}\n")
            f.write(f"{text}\n\n")
    print(f"✓ Saved to current directory: {output_path}")