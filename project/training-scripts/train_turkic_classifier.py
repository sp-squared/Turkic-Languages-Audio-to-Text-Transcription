#!/usr/bin/env python3
"""
Train Turkic Language Classifier and Save as .pkl
"""

import pickle
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

try:
    from datasets import load_dataset
except ImportError:
    import subprocess, sys
    print("📦 Installing datasets library...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "datasets"])
    from datasets import load_dataset

print("=" * 70)
print("TURKIC LANGUAGE CLASSIFIER TRAINING")
print("=" * 70)

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================

print("\n📥 Loading data from mteb/TurkicClassification...")

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
# STEP 2: CREATE TRAIN/TEST SPLIT
# ============================================================================

print("\n📊 Creating train/test split (85%/15%)...")

X_train, X_test, y_train, y_test = train_test_split(
    all_texts,
    all_labels,
    test_size=0.15,
    random_state=42,
    stratify=all_labels
)

print(f"   Training samples: {len(X_train)}")
print(f"   Test samples: {len(X_test)}")

print(f"\n   Training set distribution:")
for label, name in language_names.items():
    count = y_train.count(label)
    print(f"      {name}: {count} samples ({count/len(y_train)*100:.1f}%)")

# ============================================================================
# STEP 3: CREATE AND TRAIN MODEL
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
        random_state=42,
        multi_class='multinomial',
        solver='lbfgs',
        C=1.0
    ))
])

print("   ✅ Pipeline created:")
print("      1. TF-IDF Vectorizer (char n-grams 2-5)")
print("      2. Logistic Regression (multinomial)")

print("\n🎓 Training model...")
print("   This may take 30-60 seconds...")

model.fit(X_train, y_train)

print("   ✅ Training complete!")

# ============================================================================
# STEP 4: EVALUATE MODEL
# ============================================================================

print("\n📊 Evaluating model...")

train_accuracy = model.score(X_train, y_train)
print(f"\n   Training Accuracy: {train_accuracy:.2%}")

test_accuracy = model.score(X_test, y_test)
print(f"   Test Accuracy: {test_accuracy:.2%}")

print("\n📋 Detailed Classification Report (Test Set):")
y_pred = model.predict(X_test)
report = classification_report(
    y_test, 
    y_pred, 
    target_names=['Bashkir', 'Kazakh', 'Kyrgyz'],
    digits=3
)
print(report)

print("🔍 Confusion Matrix (Test Set):")
cm = confusion_matrix(y_test, y_pred)
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

model_path = output_dir / "turkic_classifier.pkl"

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

test_text = "Башҡортостан Республикаһы"
prediction = loaded_model.predict([test_text])[0]
print(f"   Test text: '{test_text}'")
print(f"   Prediction: {language_names[prediction]}")
print(f"   ✅ Model loads and predicts successfully!")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("✅ TRAINING COMPLETE!")
print("=" * 70)

print("\n📊 Summary:")
print(f"   Total training samples: {len(X_train)}")
print(f"   Total test samples: {len(X_test)}")
print(f"   Training accuracy: {train_accuracy:.2%}")
print(f"   Test accuracy: {test_accuracy:.2%}")
print(f"   Model size: {size_str}")
print(f"   Model location: {model_path}")

print("\n📝 Next steps:")
print("   1. Use the saved model in your scripts")
print("   2. Report TEST accuracy in papers/documentation")
print("   3. Model is ready to use!")

print("\n" + "=" * 70)