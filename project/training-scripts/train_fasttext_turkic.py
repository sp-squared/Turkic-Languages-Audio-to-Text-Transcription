#!/usr/bin/env python3
"""
FastText Language Classifier for Turkic Languages
Trains a model to identify Bashkir, Kazakh, and Kyrgyz
"""

import os
import sys

# Install fasttext if needed
try:
    import fasttext
except ImportError:
    print("Installing fasttext...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fasttext"])
    import fasttext

def load_and_prepare_data():
    """Load data and create FastText format files"""
    
    print("="*70)
    print("FASTTEXT TURKIC LANGUAGE CLASSIFIER")
    print("="*70)
    
    print("\n📥 Loading data...")
    
    # Use relative paths - works from any directory
    files = {
        'bashkir': 'bashkir_clean_cyrillic_base.txt',
        'kazakh': 'kazakh_clean_cyrillic_base.txt',
        'kyrgyz': 'kyrgyz_clean_cyrillic_base.txt'
    }
    
    # Check if files exist
    for lang, filepath in files.items():
        if not os.path.exists(filepath):
            print(f"\n❌ Error: {filepath} not found!")
            print(f"   Make sure you're running this script from the training_data directory")
            print(f"   Current directory: {os.getcwd()}")
            return None, None, None
    
    # Load all data
    data = {}
    for lang, filepath in files.items():
        with open(filepath, 'r', encoding='utf-8') as f:
            texts = [line.strip() for line in f if line.strip()]
        data[lang] = texts
        print(f"  {lang.capitalize()}: {len(texts)} samples")
    
    total = sum(len(texts) for texts in data.values())
    print(f"\n✓ Total samples: {total}")
    
    # Create train/val/test splits (70/15/15)
    print("\n📊 Creating train/val/test splits...")
    
    # Output files in current directory
    train_file = 'train.txt'
    val_file = 'val.txt'
    test_file = 'test.txt'
    
    train_count = 0
    val_count = 0
    test_count = 0
    
    with open(train_file, 'w', encoding='utf-8') as f_train, \
         open(val_file, 'w', encoding='utf-8') as f_val, \
         open(test_file, 'w', encoding='utf-8') as f_test:
        
        for lang, texts in data.items():
            # Split: 70% train, 15% val, 15% test
            n = len(texts)
            train_end = int(0.7 * n)
            val_end = int(0.85 * n)
            
            # Training data
            for text in texts[:train_end]:
                f_train.write(f"__label__{lang} {text}\n")
                train_count += 1
            
            # Validation data
            for text in texts[train_end:val_end]:
                f_val.write(f"__label__{lang} {text}\n")
                val_count += 1
            
            # Test data
            for text in texts[val_end:]:
                f_test.write(f"__label__{lang} {text}\n")
                test_count += 1
    
    print(f"  Train: {train_count} samples")
    print(f"  Val: {val_count} samples")
    print(f"  Test: {test_count} samples")
    
    return train_file, val_file, test_file

def train_model(train_file):
    """Train FastText model"""
    
    print("\n🚀 Training FastText model...")
    print("  This will take a few minutes...\n")
    
    model = fasttext.train_supervised(
        input=train_file,
        lr=0.1,
        epoch=25,
        wordNgrams=2,
        dim=100,
        loss='softmax',
        verbose=2
    )
    
    print("\n✓ Training complete!")
    
    # Save model in current directory
    model_path = 'turkic_classifier.bin'
    model.save_model(model_path)
    print(f"✓ Model saved to {model_path}")
    
    return model

def evaluate_model(model, test_file):
    """Evaluate model"""
    
    print(f"\n📈 Evaluating on test set...")
    
    result = model.test(test_file)
    
    print(f"\n🎯 Test Results:")
    print(f"  Samples: {result[0]}")
    print(f"  Precision: {result[1]:.4f}")
    print(f"  Recall: {result[2]:.4f}")
    print(f"  Accuracy: {result[1]:.2%}")
    
    return result

def test_examples(model):
    """Test with example sentences"""
    
    print("\n🧪 Testing with examples...")
    print("="*70)
    
    examples = [
        ("Бишкек шаарында жаңы мектеп ачылды", "kyrgyz"),
        ("Кыргызстанда саясий өзгөрүүлөр болууда", "kyrgyz"),
        ("Башҡортостан Республикаһында концерт үтте", "bashkir"),
        ("Өфөлә яңы мәктәп ашылды", "bashkir"),
        ("Қазақстанда жаңа заң қабылданды", "kazakh"),
        ("Алматы қаласында жаңа мектеп ашылды", "kazakh"),
    ]
    
    correct = 0
    for text, expected in examples:
        prediction = model.predict(text)
        predicted = prediction[0][0].replace('__label__', '')
        confidence = prediction[1][0]
        
        is_correct = predicted == expected
        correct += is_correct
        status = "✓" if is_correct else "✗"
        
        print(f"\n{status} {text[:55]}...")
        print(f"  Expected: {expected:8} | Predicted: {predicted:8} | Confidence: {confidence:.1%}")
    
    print("\n" + "="*70)
    print(f"Example Accuracy: {correct}/{len(examples)} = {correct/len(examples):.1%}")

def main():
    # Load and prepare data
    result = load_and_prepare_data()
    
    if result[0] is None:
        return
    
    train_file, val_file, test_file = result
    
    # Train model
    model = train_model(train_file)
    
    # Evaluate
    evaluate_model(model, test_file)
    
    # Test examples
    test_examples(model)
    
    print("\n" + "="*70)
    print("✅ TRAINING COMPLETE!")
    print("="*70)
    print("\nModel saved: turkic_classifier.bin")
    print("\nTo use:")
    print("  import fasttext")
    print("  model = fasttext.load_model('turkic_classifier.bin')")
    print("  model.predict('your text here')")
    print()

if __name__ == "__main__":
    main()
