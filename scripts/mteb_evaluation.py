#!/usr/bin/env python3
"""
Evaluate TF-IDF embeddings using MTEB-style approach
"""

import pickle
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from datasets import load_dataset

print("📦 Loading your trained model...")
model_path = Path("/project/training_data/turkic_classifier.pkl")
with open(model_path, 'rb') as f:
    full_pipeline = pickle.load(f)

# Extract just the TF-IDF vectorizer (the "embedding" part)
tfidf = full_pipeline.named_steps['tfidf']

print("📥 Loading mteb/TurkicClassification dataset...")

# Load all three languages
all_texts = []
all_labels = []

for lang_code, label in [('ba', 0), ('kk', 1), ('ky', 2)]:
    dataset = load_dataset("mteb/TurkicClassification", lang_code)
    data = dataset['train']
    texts = [sample['text'] for sample in data]
    all_texts.extend(texts)
    all_labels.extend([label] * len(texts))

print(f"✅ Loaded {len(all_texts)} samples")

print("\n🔢 Generating embeddings...")
# Generate embeddings using your trained TF-IDF
embeddings = tfidf.transform(all_texts)

print(f"   Embedding shape: {embeddings.shape}")
print(f"   Features: {embeddings.shape[1]}")

print("\n🎓 Training fresh classifier on embeddings (MTEB-style)...")
# Train a NEW classifier (like MTEB does)
clf = LogisticRegression(max_iter=1000, random_state=42)

# 5-fold cross-validation (MTEB approach)
scores = cross_val_score(
    clf, 
    embeddings, 
    all_labels, 
    cv=5,
    scoring='accuracy'
)

print(f"\n📊 Cross-Validation Results:")
print(f"   Fold 1: {scores[0]:.2%}")
print(f"   Fold 2: {scores[1]:.2%}")
print(f"   Fold 3: {scores[2]:.2%}")
print(f"   Fold 4: {scores[3]:.2%}")
print(f"   Fold 5: {scores[4]:.2%}")
print(f"\n   Mean Accuracy: {scores.mean():.2%} ± {scores.std():.2%}")

print("\n✅ MTEB-style evaluation complete!")