#!/usr/bin/env python3
"""
Use the Trained Turkic Language Classifier

Load and use the trained model to classify new texts.
"""

import pickle

# Load the model
print("Loading model...")
with open('turkic_classifier.pkl', 'rb') as f:
    data = pickle.load(f)

model = data['model']
vectorizer = data['vectorizer']

print("✓ Model loaded!\n")

# Label mapping
label_names = ['bashkir', 'kazakh', 'kyrgyz']

def classify_text(text):
    """Classify a single text"""
    # Vectorize
    X = vectorizer.transform([text])
    
    # Predict
    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]
    
    # Get language name
    language = label_names[prediction]
    confidence = probabilities[prediction]
    
    return language, confidence, probabilities

def classify_batch(texts):
    """Classify multiple texts"""
    # Vectorize all at once
    X = vectorizer.transform(texts)
    
    # Predict
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)
    
    results = []
    for pred, probs in zip(predictions, probabilities):
        language = label_names[pred]
        confidence = probs[pred]
        results.append((language, confidence))
    
    return results

# Example usage
if __name__ == "__main__":
    print("="*70)
    print("TURKIC LANGUAGE CLASSIFIER - DEMO")
    print("="*70)
    
    # Test with examples
    test_texts = [
        "Бишкек шаарында жаңы мектеп ачылды",
        "Башҡортостан Республикаһында концерт үтте",
        "Қазақстанда жаңа заң қабылданды",
        "Кыргызстанда саясий өзгөрүүлөр болууда",
        "Өфөлә яңы мәктәп ашылды",
        "Алматы қаласында жаңа жоба іске қосылды",
    ]
    
    print("\n🧪 Classifying test sentences...\n")
    
    for text in test_texts:
        language, confidence, probs = classify_text(text)
        
        print(f"Text: {text[:55]}...")
        print(f"  Language: {language.upper()} (confidence: {confidence:.1%})")
        print(f"  Probabilities: Bashkir={probs[0]:.1%}, Kazakh={probs[1]:.1%}, Kyrgyz={probs[2]:.1%}")
        print()
    
    # Batch classification
    print("="*70)
    print("\n🚀 Batch classification example...\n")
    
    results = classify_batch(test_texts)
    
    for text, (lang, conf) in zip(test_texts, results):
        print(f"{lang:8} ({conf:.1%}) - {text[:45]}...")
    
    print("\n" + "="*70)
    print("\n💡 To classify your own text:")
    print("  language, confidence, probs = classify_text('your text here')")
    print("  print(f'Language: {language} ({confidence:.1%})')")
    print()
