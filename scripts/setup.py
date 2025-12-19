#!/usr/bin/env python3
"""
Setup and Configuration for Turkic Language Processing
Updates file paths and prepares the environment
"""

from pathlib import Path
import os
import sys

# =============== CONFIGURATION ===============

# Base directory - GitHub repository root
BASE_DIR = Path(r"C:\Users\colin\Documents\GitHub\Turkic-Language-Audio-to-Text-Transcription")

# Data directory - where raw files are located
DATA_DIR = BASE_DIR / "project" / "data"

# Training data directory - where processed files and models go
TRAINING_DIR = BASE_DIR / "project" / "training_data"

# Input files (raw data files)
RAW_FILES = {
    "bashkir": DATA_DIR / "bashkir_clean_cyrillic_base.txt",
    "kazakh": DATA_DIR / "kazakh_clean_cyrillic_base.txt",
    "kyrgyz": DATA_DIR / "kyrgyz_clean_cyrillic_base.txt",
}

# Output cleaned files (if needed for further processing)
CLEAN_FILES = {
    "bashkir": TRAINING_DIR / "bashkir_clean_cyrillic.txt",
    "kazakh": TRAINING_DIR / "kazakh_clean_cyrillic.txt",
    "kyrgyz": TRAINING_DIR / "kyrgyz_clean_cyrillic.txt",
}

# Model files
MODEL_FILES = {
    "sklearn": TRAINING_DIR / "turkic_classifier.pkl",
    "fasttext": TRAINING_DIR / "turkic_classifier.bin",
    "transformer": TRAINING_DIR / "turkic_classifier",
}

# =============== VERIFICATION ===============

def verify_setup():
    """Verify that all paths and files exist"""
    
    print("="*70)
    print("SETUP VERIFICATION")
    print("="*70)
    
    # Check base directory
    print(f"\n📁 Base Directory: {BASE_DIR}")
    if BASE_DIR.exists():
        print("   ✅ Exists")
    else:
        print("   ❌ Does not exist!")
        return False
    
    # Check data directory
    print(f"\n📁 Data Directory: {DATA_DIR}")
    if DATA_DIR.exists():
        print("   ✅ Exists")
    else:
        print("   ❌ Does not exist!")
        print(f"   Creating directory...")
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        print("   ✅ Created")
    
    # Check training directory
    print(f"\n📁 Training Directory: {TRAINING_DIR}")
    if TRAINING_DIR.exists():
        print("   ✅ Exists")
    else:
        print("   ❌ Does not exist!")
        print(f"   Creating directory...")
        TRAINING_DIR.mkdir(parents=True, exist_ok=True)
        print("   ✅ Created")
    
    # Check raw files
    print("\n📄 Raw Data Files:")
    all_exist = True
    for lang, filepath in RAW_FILES.items():
        print(f"   {lang.capitalize()}: {filepath.name}")
        if filepath.exists():
            size = filepath.stat().st_size / 1024  # KB
            lines = sum(1 for _ in open(filepath, 'r', encoding='utf-8'))
            print(f"      ✅ Exists ({size:.1f} KB, {lines} lines)")
        else:
            print(f"      ❌ Does not exist!")
            all_exist = False
    
    # Check for trained models
    print("\n🤖 Trained Models:")
    for model_type, filepath in MODEL_FILES.items():
        print(f"   {model_type.capitalize()}: {filepath.name}")
        if filepath.exists():
            if model_type == "transformer":
                print(f"      ✅ Exists (directory)")
            else:
                size = filepath.stat().st_size / (1024 * 1024)  # MB
                print(f"      ✅ Exists ({size:.1f} MB)")
        else:
            print(f"      ⚠️  Not trained yet")
    
    print("\n" + "="*70)
    
    if not all_exist:
        print("❌ SETUP INCOMPLETE")
        print("\nMissing files need to be added to:")
        print(f"   {DATA_DIR}")
        return False
    else:
        print("✅ SETUP COMPLETE")
        return True

# =============== HELPER FUNCTIONS ===============

def get_data_file(language):
    """Get the path to a data file for a specific language"""
    if language not in RAW_FILES:
        raise ValueError(f"Unknown language: {language}. Must be one of {list(RAW_FILES.keys())}")
    return RAW_FILES[language]

def get_all_data_files():
    """Get all data file paths"""
    return RAW_FILES

def get_model_path(model_type="sklearn"):
    """Get the path to a trained model"""
    if model_type not in MODEL_FILES:
        raise ValueError(f"Unknown model type: {model_type}. Must be one of {list(MODEL_FILES.keys())}")
    return MODEL_FILES[model_type]

def ensure_directories():
    """Ensure all necessary directories exist"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TRAINING_DIR.mkdir(parents=True, exist_ok=True)

# =============== MAIN ===============

if __name__ == "__main__":
    # Run verification
    success = verify_setup()
    
    if success:
        print("\n✅ You're ready to start training!")
        print("\nNext steps:")
        print("  1. cd to training directory:")
        print(f"     cd {TRAINING_DIR}")
        print("  2. Run training script:")
        print("     python train_sklearn_turkic.py")
        print("  3. Or use the pre-trained model:")
        print("     python use_turkic_classifier.py")
    else:
        print("\n⚠️  Please fix the issues above before proceeding.")
        sys.exit(1)