#!/usr/bin/env python3
"""
Use Saved Turkic Classifier

Loads the trained .pkl model and classifies text.

Usage:
    python use_classifier.py
"""

import pickle
from pathlib import Path

# Load the saved model
model_path = Path(__file__).parent.parent / "training_data" / "turkic_classifier.pkl"

print("📦 Loading classifier...")
with open(model_path, 'rb') as f:
    model = pickle.load(f)
print("✅ Model loaded!")

# Language names
language_names = {
    0: 'Bashkir',
    1: 'Kazakh',
    2: 'Kyrgyz'
}

def classify_text(text):
    """
    Classify a single text sample.
    
    Args:
        text: Text to classify
        
    Returns:
        language: Detected language name
        confidence: Confidence score
        probabilities: Dictionary of all probabilities
    """
    # Predict
    prediction = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]
    
    # Get results
    language = language_names[prediction]
    confidence = probabilities[prediction]
    
    # Create probability dict
    prob_dict = {
        language_names[i]: prob 
        for i, prob in enumerate(probabilities)
    }
    
    return language, confidence, prob_dict


def classify_batch(texts):
    """
    Classify multiple texts at once.
    
    Args:
        texts: List of texts
        
    Returns:
        List of (language, confidence) tuples
    """
    predictions = model.predict(texts)
    probabilities = model.predict_proba(texts)
    
    results = []
    for pred, probs in zip(predictions, probabilities):
        language = language_names[pred]
        confidence = probs[pred]
        results.append((language, confidence))
    
    return results


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("TURKIC LANGUAGE CLASSIFIER - DEMO")
    print("=" * 70)
    
    # Test samples
    test_samples = [
        "Башҡортостан Республикаһы Рәсәйҙең төньяғында урынлашҡан",
        "Қазақстан Орталық Азияда орналасқан мемлекет",
        "Кыргызстан Борбордук Азияда жайгашкан өлкө",
        "Бының ҡойроҡ менән Кепка",
        "Мен үйге барамын",
    ]
    
    print("\n🔍 Classifying sample texts...\n")
    
    for i, text in enumerate(test_samples, 1):
        language, confidence, probs = classify_text(text)
        
        print(f"Sample {i}:")
        print(f"   Text: {text}")
        print(f"   Detected: {language} ({confidence:.1%} confidence)")
        print(f"   Probabilities:")
        for lang, prob in sorted(probs.items(), key=lambda x: x[1], reverse=True):
            print(f"      {lang}: {prob:.1%}")
        print()
    
    # Batch classification
    print("\n📊 Batch classification...")
    results = classify_batch(test_samples)
    
    print("\nResults:")
    for i, (text, (lang, conf)) in enumerate(zip(test_samples, results), 1):
        print(f"   {i}. {lang} ({conf:.1%}) - {text[:50]}...")
    
    print("\n" + "=" * 70)
    print("✅ Demo complete!")
    print("=" * 70)