#!/usr/bin/env python3
"""
Transformer Language Classifier for Turkic Languages
Fine-tunes a BERT-like model to identify Bashkir, Kazakh, and Kyrgyz

Usage:
    python train_transformer.py

Requirements:
    pip install transformers torch datasets sklearn accelerate
"""

import os
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import numpy as np

# Install dependencies if needed
try:
    from datasets import Dataset
    from transformers import (
        AutoTokenizer,
        AutoModelForSequenceClassification,
        TrainingArguments,
        Trainer
    )
except ImportError:
    print("Installing required packages...")
    import subprocess, sys
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "transformers", "torch", "datasets", "sklearn", "accelerate"
    ])
    from datasets import Dataset
    from transformers import (
        AutoTokenizer,
        AutoModelForSequenceClassification,
        TrainingArguments,
        Trainer
    )

def load_turkic_data(bashkir_file, kazakh_file, kyrgyz_file):
    """Load and combine all three Turkic language datasets"""
    
    print("📥 Loading data...")
    
    # Read files
    with open(bashkir_file, 'r', encoding='utf-8') as f:
        bashkir_texts = [line.strip() for line in f if line.strip()]
    
    with open(kazakh_file, 'r', encoding='utf-8') as f:
        kazakh_texts = [line.strip() for line in f if line.strip()]
    
    with open(kyrgyz_file, 'r', encoding='utf-8') as f:
        kyrgyz_texts = [line.strip() for line in f if line.strip()]
    
    print(f"  Bashkir: {len(bashkir_texts)} samples")
    print(f"  Kazakh: {len(kazakh_texts)} samples")
    print(f"  Kyrgyz: {len(kyrgyz_texts)} samples")
    
    # Create labeled dataset
    data = []
    
    # Label mapping: 0 = Bashkir, 1 = Kazakh, 2 = Kyrgyz
    for text in bashkir_texts:
        data.append({'text': text, 'label': 0, 'language': 'bashkir'})
    
    for text in kazakh_texts:
        data.append({'text': text, 'label': 1, 'language': 'kazakh'})
    
    for text in kyrgyz_texts:
        data.append({'text': text, 'label': 2, 'language': 'kyrgyz'})
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    print(f"\n✓ Total samples: {len(df)}")
    
    return df

def split_data(df):
    """Split data into train/val/test sets"""
    
    print("\n📊 Splitting data...")
    
    # Split: 70% train, 15% val, 15% test
    train_df, temp_df = train_test_split(
        df, 
        test_size=0.3, 
        stratify=df['label'], 
        random_state=42
    )
    
    val_df, test_df = train_test_split(
        temp_df, 
        test_size=0.5, 
        stratify=temp_df['label'], 
        random_state=42
    )
    
    print(f"  Train: {len(train_df)} samples")
    print(f"  Val: {len(val_df)} samples")
    print(f"  Test: {len(test_df)} samples")
    
    return train_df, val_df, test_df

def prepare_datasets(train_df, val_df, test_df, tokenizer):
    """Convert DataFrames to HuggingFace Datasets and tokenize"""
    
    print("\n🔤 Tokenizing datasets...")
    
    # Convert to HuggingFace Dataset format
    train_dataset = Dataset.from_pandas(train_df[['text', 'label']])
    val_dataset = Dataset.from_pandas(val_df[['text', 'label']])
    test_dataset = Dataset.from_pandas(test_df[['text', 'label']])
    
    # Tokenize
    def tokenize_function(examples):
        return tokenizer(
            examples['text'],
            padding='max_length',
            truncation=True,
            max_length=256  # Reduced for faster training
        )
    
    train_dataset = train_dataset.map(tokenize_function, batched=True)
    val_dataset = val_dataset.map(tokenize_function, batched=True)
    test_dataset = test_dataset.map(tokenize_function, batched=True)
    
    print("✓ Tokenization complete!")
    
    return train_dataset, val_dataset, test_dataset

def compute_metrics(pred):
    """Compute metrics for evaluation"""
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average='weighted'
    )
    acc = accuracy_score(labels, preds)
    
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def train_model(train_dataset, val_dataset, model, output_dir='./turkic_classifier'):
    """Train the transformer model"""
    
    print("\n🚀 Starting training...")
    print(f"  Output directory: {output_dir}")
    
    # Check for GPU
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"  Device: {device}")
    
    if device == 'cpu':
        print("  ⚠️  Training on CPU will be slow. GPU recommended!")
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir=f'{output_dir}/logs',
        logging_steps=50,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model='accuracy',
    )
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
    )
    
    # Train!
    trainer.train()
    
    print("\n✓ Training complete!")
    
    return trainer

def evaluate_detailed(trainer, test_dataset, label_names):
    """Detailed evaluation with confusion matrix"""
    
    print("\n📈 Evaluating on test set...")
    
    # Get predictions
    predictions = trainer.predict(test_dataset)
    preds = predictions.predictions.argmax(-1)
    labels = predictions.label_ids
    
    # Overall metrics
    results = {
        'accuracy': accuracy_score(labels, preds),
        'precision': precision_recall_fscore_support(labels, preds, average='weighted')[0],
        'recall': precision_recall_fscore_support(labels, preds, average='weighted')[1],
        'f1': precision_recall_fscore_support(labels, preds, average='weighted')[2],
    }
    
    print("\n🎯 Test Results:")
    print(f"  Accuracy: {results['accuracy']:.4f}")
    print(f"  Precision: {results['precision']:.4f}")
    print(f"  Recall: {results['recall']:.4f}")
    print(f"  F1 Score: {results['f1']:.4f}")
    
    # Confusion matrix
    cm = confusion_matrix(labels, preds)
    print("\n📊 Confusion Matrix:")
    print("     ", "  ".join([f"{name:8}" for name in label_names]))
    for i, row in enumerate(cm):
        print(f"{label_names[i]:8}", "  ".join([f"{val:8}" for val in row]))
    
    # Per-class metrics
    print("\n📋 Per-Class Metrics:")
    precision, recall, f1, support = precision_recall_fscore_support(labels, preds)
    
    for i, name in enumerate(label_names):
        print(f"\n  {name.capitalize()}:")
        print(f"    Precision: {precision[i]:.4f}")
        print(f"    Recall: {recall[i]:.4f}")
        print(f"    F1: {f1[i]:.4f}")
        print(f"    Support: {support[i]}")
    
    return results

def test_predictions(model, tokenizer, label_names):
    """Test model with example sentences"""
    
    print("\n🧪 Testing predictions...")
    print("="*70)
    
    test_examples = [
        ("Бишкек шаарында жаңы мектеп ачылды", "kyrgyz"),
        ("Башҡортостан Республикаһында концерт үтте", "bashkir"),
        ("Қазақстанда жаңа заң қабылданды", "kazakh"),
        ("Кыргызстанда саясий өзгөрүүлөр болууда", "kyrgyz"),
        ("Өфөлә яңы мәктәп ашылды", "bashkir"),
        ("Алматы қаласында жаңа жоба іске қосылды", "kazakh"),
    ]
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device)
    model.eval()
    
    correct = 0
    for text, expected_lang in test_examples:
        # Tokenize
        inputs = tokenizer(
            text,
            return_tensors='pt',
            padding=True,
            truncation=True,
            max_length=256
        ).to(device)
        
        # Predict
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predicted_class = torch.argmax(predictions, dim=-1).item()
            confidence = predictions[0][predicted_class].item()
        
        predicted_lang = label_names[predicted_class]
        is_correct = predicted_lang == expected_lang
        correct += is_correct
        
        status = "✓" if is_correct else "✗"
        
        print(f"\n{status} Text: {text[:60]}...")
        print(f"  Expected: {expected_lang}")
        print(f"  Predicted: {predicted_lang} (confidence: {confidence:.2%})")
    
    print("\n" + "="*70)
    print(f"Manual Test Accuracy: {correct}/{len(test_examples)} = {correct/len(test_examples):.2%}")

def main():
    """Main training pipeline"""
    
    print("="*70)
    print("TRANSFORMER TURKIC LANGUAGE CLASSIFIER")
    print("="*70)
    
    # File paths
    bashkir_file = 'bashkir_clean_cyrillic_base.txt'
    kazakh_file = 'kazakh_clean_cyrillic_base.txt'
    kyrgyz_file = 'kyrgyz_clean_cyrillic_base.txt'
    
    # Check files exist
    for file in [bashkir_file, kazakh_file, kyrgyz_file]:
        if not os.path.exists(file):
            print(f"❌ Error: {file} not found!")
            print(f"   Please make sure all three files are in the current directory.")
            return
    
    # Load data
    df = load_turkic_data(bashkir_file, kazakh_file, kyrgyz_file)
    
    # Split data
    train_df, val_df, test_df = split_data(df)
    
    # Label names
    label_names = ['bashkir', 'kazakh', 'kyrgyz']
    
    # Choose model
    print("\n🤖 Loading pre-trained model...")
    model_name = "bert-base-multilingual-cased"  # Good for Cyrillic
    # Alternative: "xlm-roberta-base" (even better for low-resource languages)
    
    print(f"  Model: {model_name}")
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Prepare datasets
    train_dataset, val_dataset, test_dataset = prepare_datasets(
        train_df, val_df, test_df, tokenizer
    )
    
    # Load model
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=3
    )
    
    # Train model
    trainer = train_model(train_dataset, val_dataset, model)
    
    # Evaluate
    results = evaluate_detailed(trainer, test_dataset, label_names)
    
    # Test with examples
    test_predictions(model, tokenizer, label_names)
    
    # Save model
    print("\n💾 Saving model...")
    output_dir = './turkic_classifier'
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    print(f"✓ Model saved to {output_dir}")
    
    print("\n" + "="*70)
    print("✅ DONE!")
    print("="*70)
    print("\nTo use the model:")
    print("  >>> from transformers import pipeline")
    print("  >>> classifier = pipeline('text-classification', model='./turkic_classifier')")
    print("  >>> classifier('your text here')")
    print()

if __name__ == "__main__":
    main()
