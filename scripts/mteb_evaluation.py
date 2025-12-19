#!/usr/bin/env python3
"""
Evaluate TF-IDF embeddings using MTEB-style approach
"""

import pickle
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from datasets import load_dataset

print("=" * 70)
print("MTEB-STYLE EVALUATION")
print("=" * 70)

print("\n📦 Loading your trained model...")

# Fix path - relative to script location
script_dir = Path(__file__).parent
model_path = script_dir.parent / "project" / "training_data" / "turkic_classifier.pkl"

# Alternative: use absolute path
if not model_path.exists():
    model_path = Path("/home/colin/Turkic-Languages-Audio-to-Text-Transcription/project/training_data/turkic_classifier.pkl")

print(f"   Model path: {model_path}")

if not model_path.exists():
    print(f"❌ Model not found at: {model_path}")
    print("\n🔍 Searching for model...")
    
    # Search common locations
    possible_paths = [
        Path("/home/colin/Turkic-Languages-Audio-to-Text-Transcription/project/training_data/turkic_classifier.pkl"),
        Path("~/Turkic-Languages-Audio-to-Text-Transcription/project/training_data/turkic_classifier.pkl").expanduser(),
        Path("../project/training_data/turkic_classifier.pkl"),
        Path("../training_data/turkic_classifier.pkl"),
    ]
    
    for p in possible_paths:
        if p.exists():
            model_path = p
            print(f"✅ Found model at: {model_path}")
            break
    else:
        print("\n❌ Could not find model file!")
        print("Please run from the correct directory or check model location.")
        exit(1)

with open(model_path, 'rb') as f:
    full_pipeline = pickle.load(f)

print("✅ Model loaded successfully!")

# Extract just the TF-IDF vectorizer (the "embedding" part)
tfidf = full_pipeline.named_steps['tfidf']

print(f"   TF-IDF vocabulary size: {len(tfidf.vocabulary_)}")
print(f"   Max features: {tfidf.max_features}")
print(f"   N-gram range: {tfidf.ngram_range}")

print("\n📥 Loading mteb/TurkicClassification dataset...")

# Load all three languages
all_texts = []
all_labels = []

language_names = {
    0: 'Bashkir',
    1: 'Kazakh',
    2: 'Kyrgyz'
}

for lang_code, label in [('ba', 0), ('kk', 1), ('ky', 2)]:
    print(f"   Loading {language_names[label]}...")
    dataset = load_dataset("mteb/TurkicClassification", lang_code)
    data = dataset['train']
    texts = [sample['text'] for sample in data]
    all_texts.extend(texts)
    all_labels.extend([label] * len(texts))
    print(f"      ✅ {len(texts)} samples")

print(f"\n✅ Total samples loaded: {len(all_texts)}")
print(f"   Distribution:")
for label, name in language_names.items():
    count = all_labels.count(label)
    print(f"      {name}: {count} samples ({count/len(all_labels)*100:.1f}%)")

print("\n🔢 Generating embeddings with trained TF-IDF...")
# Generate embeddings using your trained TF-IDF
embeddings = tfidf.transform(all_texts)

print(f"   Embedding shape: {embeddings.shape}")
print(f"   Features: {embeddings.shape[1]}")
print(f"   Sparsity: {(1 - embeddings.nnz / (embeddings.shape[0] * embeddings.shape[1])):.1%}")

print("\n🎓 Training fresh classifier on embeddings (MTEB-style)...")
print("   Using 5-fold cross-validation...")

# Train a NEW classifier (like MTEB does)
clf = LogisticRegression(max_iter=1000, random_state=42)

# 5-fold cross-validation (MTEB approach)
scores = cross_val_score(
    clf, 
    embeddings, 
    all_labels, 
    cv=5,
    scoring='accuracy',
    verbose=0
)

print("\n" + "=" * 70)
print("📊 CROSS-VALIDATION RESULTS")
print("=" * 70)

print(f"\n   Fold 1: {scores[0]:.2%}")
print(f"   Fold 2: {scores[1]:.2%}")
print(f"   Fold 3: {scores[2]:.2%}")
print(f"   Fold 4: {scores[3]:.2%}")
print(f"   Fold 5: {scores[4]:.2%}")

print(f"\n   Mean Accuracy: {scores.mean():.2%}")
print(f"   Std Deviation: {scores.std():.2%}")
print(f"   Min Accuracy:  {scores.min():.2%}")
print(f"   Max Accuracy:  {scores.max():.2%}")

print("\n" + "=" * 70)
print("✅ MTEB-STYLE EVALUATION COMPLETE!")
print("=" * 70)

print("\n📝 Summary:")
print(f"   Embedding Model: TF-IDF (character n-grams {tfidf.ngram_range})")
print(f"   Classifier: Logistic Regression")
print(f"   Total Samples: {len(all_texts)}")
print(f"   Cross-Validation: 5-fold")
print(f"   Final Result: {scores.mean():.2%} ± {scores.std():.2%}")

print("\n💡 Interpretation:")
if scores.mean() >= 0.95:
    print("   ✅ Excellent performance! Embeddings capture language differences well.")
elif scores.mean() >= 0.90:
    print("   ✅ Good performance! Embeddings are effective for classification.")
elif scores.mean() >= 0.80:
    print("   ⚠️  Decent performance, but room for improvement.")
else:
    print("   ❌ Poor performance, embeddings may need refinement.")

print("\n📊 Comparison with your original evaluation:")
print(f"   Original test accuracy: 97.3%")
print(f"   Cross-validation mean:  {scores.mean():.1%}")
print(f"   Difference: {abs(0.973 - scores.mean())*100:.1f} percentage points")

if abs(0.973 - scores.mean()) < 0.02:
    print("   ✅ Results are very consistent!")
elif abs(0.973 - scores.mean()) < 0.05:
    print("   ✅ Results are reasonably consistent.")
else:
    print("   ⚠️  Some variation between methods.")

print("\n" + "=" * 70)