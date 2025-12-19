#!/usr/bin/env python3
"""
Train Turkic Language Classifier on ALL DATA (No Train/Test Split)

WARNING: This trains on 100% of data. You cannot report test accuracy.
Use this for production models only, not for evaluation/research.

Usage:
    python train_turkic_classifier_full.py
    
Output:
    - turkic_classifier_full.pkl (trained on all 6,144 samples)
"""

import pickle
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix

try:
    from datasets import load_dataset
except ImportError:
    import subprocess, sys
    print("📦 Installing datasets library...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "datasets"])
    from datasets import load_dataset

print("=" * 70)
print("TURKIC LANGUAGE CLASSIFIER TRAINING (FULL DATA)")
print("=" * 70)
print("\n⚠️  WARNING: Training on ALL data (no test set)")
print("   This model cannot be properly evaluated!")
print("   Use for production only, not for research/papers.\n")

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================

print("📥 Loading data from mteb/TurkicClassification...")

all_texts = []
all_labels = []

language_map = {
    'ba': 0,  # Bashkir
    'kk': 1,  # Kazakh
    'ky': 2   # Kyrgyz
}

language_names = {
    0: 'Bashkir',
    1: 'Kazakh',
    2: 'Kyrgyz'
}

for lang_code, label in language_map.items():
    print(f"   Loading {language_names[label]}...")
    dataset = load_dataset("mteb/TurkicClassification", lang_code)
    data = dataset['train']
    
    texts = [sample['text'] for sample in data]
    labels = [label] * len(texts)
    
    all_texts.extend(texts)
    all_labels.extend(labels)
    
    print(f"      ✅ {len(texts)} samples")

print(f"\n✅ Total samples loaded: {len(all_texts)}")
print(f"   Distribution:")
for label, name in language_names.items():
    count = all_labels.count(label)
    print(f"      {name}: {count} samples ({count/len(all_labels)*100:.1f}%)")

# ============================================================================
# STEP 2: CREATE MODEL (No Split - Using ALL Data)
# ============================================================================

print("\n🔧 Building classifier pipeline...")

model = Pipeline([
    ('tfidf', TfidfVectorizer(
        analyzer='char',
        ngram_range=(2, 5),
        max_features=10000,
        min_df=2,
        lowercase=True
    )),
    ('classifier', LogisticRegression(
        max_iter=1000,
        random_state=42
    ))
])

print("   ✅ Pipeline created:")
print("      1. TF-IDF Vectorizer (char n-grams 2-5)")
print("      2. Logistic Regression")

# ============================================================================
# STEP 3: TRAIN ON ALL DATA
# ============================================================================

print("\n🎓 Training model on ALL 6,144 samples...")
print("   This may take 30-60 seconds...")

model.fit(all_texts, all_labels)

print("   ✅ Training complete!")

# ============================================================================
# STEP 4: TRAINING ACCURACY (Not a Valid Test Metric!)
# ============================================================================

print("\n📊 Evaluating on training data...")
print("   ⚠️  Note: This is training accuracy, NOT test accuracy!")
print("   ⚠️  Cannot be used for claims about generalization!\n")

train_accuracy = model.score(all_texts, all_labels)
print(f"   Training Accuracy: {train_accuracy:.2%}")

print("\n📋 Classification Report (Training Data):")
y_pred = model.predict(all_texts)
report = classification_report(
    all_labels, 
    y_pred, 
    target_names=['Bashkir', 'Kazakh', 'Kyrgyz'],
    digits=3
)
print(report)

print("🔍 Confusion Matrix (Training Data):")
cm = confusion_matrix(all_labels, y_pred)
print("\n           Predicted")
print("         Ba    Kk    Ky")
print("Actual")
for i, name in enumerate(['Ba', 'Kk', 'Ky']):
    print(f"  {name}  ", end="")
    for j in range(3):
        print(f"{cm[i][j]:5d} ", end="")
    print()

# ============================================================================
# STEP 5: SAVE MODEL
# ============================================================================

print("\n💾 Saving model...")

output_dir = Path(__file__).parent.parent / "training_data"
output_dir.mkdir(parents=True, exist_ok=True)

model_path = output_dir / "turkic_classifier_full.pkl"

with open(model_path, 'wb') as f:
    pickle.dump(model, f)

file_size = model_path.stat().st_size
file_size_kb = file_size / 1024
file_size_mb = file_size / (1024 * 1024)

if file_size_mb >= 1:
    size_str = f"{file_size_mb:.2f} MB"
else:
    size_str = f"{file_size_kb:.2f} KB"

print(f"   ✅ Model saved to: {model_path}")
print(f"   📦 File size: {size_str}")

# ============================================================================
# STEP 6: TEST LOADING MODEL
# ============================================================================

print("\n🔍 Testing model loading...")

with open(model_path, 'rb') as f:
    loaded_model = pickle.load(f)

test_texts = [
    "Башҡортостан Республикаһы",
    "Қазақстан Республикасы",
    "Кыргыз Республикасы"
]

print("   Testing predictions:")
for text in test_texts:
    prediction = loaded_model.predict([text])[0]
    print(f"      '{text[:30]}...' → {language_names[prediction]}")

print(f"   ✅ Model loads and predicts successfully!")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("✅ TRAINING COMPLETE!")
print("=" * 70)

print("\n📊 Summary:")
print(f"   Total training samples: {len(all_texts)}")
print(f"   Training accuracy: {train_accuracy:.2%}")
print(f"   Model size: {size_str}")
print(f"   Model location: {model_path}")

print("\n⚠️  IMPORTANT NOTES:")
print("   • This model was trained on ALL available data")
print("   • No held-out test set exists")
print("   • Training accuracy is NOT a valid generalization metric")
print("   • Use this model for production/deployment")
print("   • DO NOT report this accuracy in research papers")

print("\n📝 For Research/Papers:")
print("   • Use train_turkic_classifier.py (with train/test split)")
print("   • Report test accuracy on held-out data")
print("   • Follow proper evaluation methodology")

print("\n💡 Usage:")
print("   • This model is ready for production use")
print("   • It has seen all available training data")
print("   • Best performance for deployment scenarios")

print("\n" + "=" * 70)