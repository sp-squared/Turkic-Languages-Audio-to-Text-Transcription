#!/usr/bin/env python3
"""
Script to process big_clip_file_corrected.txt through the Kazakh to Bashkir corrector
"""

from kazakh_to_bashkir_corrector import KazakhToBashkirCorrector

def process_file():
    # Initialize the corrector
    corrector = KazakhToBashkirCorrector()
    
    # Read the input file
    with open('big_clip_file_corrected.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Apply correction
    corrected_text = corrector.correct_orthography(text)
    
    # Save the corrected version
    with open('big_clip_file_final.txt', 'w', encoding='utf-8') as f:
        f.write(corrected_text)
    
    print("✅ File processed successfully!")
    print(f"Output saved to: big_clip_file_final.txt")
    
    # Show statistics
    original_words = len(text.split())
    corrected_words = len(corrected_text.split())
    
    print(f"\n📊 Statistics:")
    print(f"  Original word count: {original_words}")
    print(f"  Corrected word count: {corrected_words}")
    
    # Show first few lines for verification
    print(f"\n📝 Preview of corrected text:")
    print("-" * 70)
    lines = corrected_text.split('\n')
    for i, line in enumerate(lines[:3]):
        if line.strip():
            print(f"Line {i+1}: {line[:80]}..." if len(line) > 80 else f"Line {i+1}: {line}")

if __name__ == "__main__":
    process_file()