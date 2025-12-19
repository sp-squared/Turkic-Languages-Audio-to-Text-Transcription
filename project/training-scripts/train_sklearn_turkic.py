# train_sklearn_turkic.py
"""
Train a scikit-learn language ID model for Bashkir (ba), Kazakh (kk), and Kyrgyz (ky).
- Input: ./data/turkic_classification_results_*.txt
- Output: ./training_data/
  - cleaned files
  - langid_sklearn_model.pkl
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
from pathlib import Path
import sys

# Use relative paths
PROJECT_ROOT = Path(__file__).parent.resolve()
DATA_DIR = PROJECT_ROOT / "project/data"
OUTPUT_DIR = PROJECT_ROOT / "training_data"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)

# Input and output file mappings
RAW_FILES = {
    "ba": DATA_DIR / "bashkir_clean_cyrillic_base.txt",
    "kk": DATA_DIR / "kazakh_clean_cyrillic_base.txt",
    "ky": DATA_DIR / "kyrgyz_clean_cyrillic_base.txt",
}

CLEAN_FILES = {
    "ba": OUTPUT_DIR / "bashkir_clean_cyrillic.txt",
    "kk": OUTPUT_DIR / "kazakh_clean_cyrillic.txt",
    "ky": OUTPUT_DIR / "kyrgyz_clean_cyrillic.txt",
}

MODEL_OUTPUT = OUTPUT_DIR / "langid_sklearn_model.pkl"

# Language-specific Cyrillic regex patterns
PATTERNS = {
    "ba": r'[а-яА-ЯҡғҫҙңөүһҺҠҒҪҢӨҮһ]+',
    "kk": r'[а-яА-ЯәғқңөұүһіӘҒҚҢӨҰҮҺІ]+',
    "ky": r'[а-яА-ЯәңөүӘҢӨҮ]+',
}

def load_and_clean_texts():
    data = []
    for lang, raw_path in RAW_FILES.items():
        if not raw_path.exists():
            print(f"⚠️  Skipping {lang}: {raw_path} not found.")
            continue

        cleaned_lines = []
        with open(raw_path, "r", encoding="utf-8") as f:
            for line in f:
                if "Sample" in line and "=" in line:
                    continue
                stripped = line.strip()
                if not stripped:
                    continue
                # Count meaningful Cyrillic chars
                cyrillic_parts = re.findall(PATTERNS[lang], stripped)
                total = sum(len(w) for w in cyrillic_parts)
                if total >= 3:
                    cleaned_lines.append(stripped)

        # Save cleaned version
        with open(CLEAN_FILES[lang], "w", encoding="utf-8") as out:
            out.write("\n".join(cleaned_lines))
        print(f"✅ Cleaned {lang} → {CLEAN_FILES[lang]}")

        # Add to training data
        data.extend({"text": line, "lang": lang} for line in cleaned_lines)

    return data

def main():
    print("🚀 Training scikit-learn language ID model (relative paths)...\n")

    data = load_and_clean_texts()
    if not data:
        print("❗ No data loaded. Check ./data/ folder.")
        sys.exit(1)

    df = pd.DataFrame(data)
    X = df["text"]
    y = df["lang"]

    print(f"📊 Training on {len(df)} samples: {sorted(df['lang'].unique())}")

    # Build pipeline
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(
            analyzer="char",
            ngram_range=(2, 5),
            max_features=15000,
            lowercase=False
        )),
        ("clf", LogisticRegression(max_iter=1000, random_state=42))
    ])

    # Train & save
    pipe.fit(X, y)
    joblib.dump(pipe, MODEL_OUTPUT)
    print(f"✅ Model saved → {MODEL_OUTPUT}")

    # Optional: print training accuracy
    acc = pipe.score(X, y)
    print(f"🔍 Training accuracy: {acc:.2%}")

if __name__ == "__main__":
    import re  # needed for load_and_clean_texts
    main()