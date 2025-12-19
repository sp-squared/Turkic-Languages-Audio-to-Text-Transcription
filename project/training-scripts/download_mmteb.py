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
    # Fallback passthrough if the package is not available; install similarly if desired
    def latin_to_cyrillic(text, lang):
        return text

import re

def has_latin_characters(s):
    return bool(re.search(r'[A-Za-z]', s))

# Load dataset
dataset = load_dataset("mteb/TurkicClassification", "kk")

# Convert any Latin text in your data
results = []
for example in dataset['train']:
    # Ensure text is in Cyrillic
    text = example.get('text', '')
    if has_latin_characters(text):
        text = latin_to_cyrillic(text, "kk")
    results.append(text)