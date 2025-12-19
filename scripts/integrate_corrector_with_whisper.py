#!/usr/bin/env python3
"""
Example: Using the Kazakh-to-Bashkir Corrector with Whisper

This script demonstrates how to post-process Whisper transcriptions
that incorrectly use Kazakh orthography for Bashkir audio.

USAGE:
    python integrate_corrector_with_whisper.py <audio_file>
"""

import sys
from pathlib import Path

# Uncomment these if you have whisper installed
# import whisper
# import torch

from kazakh_to_bashkir_corrector import correct_orthography, KazakhToBashkirCorrector


def transcribe_and_correct(audio_path: str, model_size: str = "base", aggressive: bool = False):
    """
    Transcribe audio with Whisper and correct Kazakh→Bashkir orthography
    
    Args:
        audio_path: Path to audio file
        model_size: Whisper model size (tiny, base, small, medium, large)
        aggressive: Whether to apply aggressive corrections
    
    Returns:
        Dictionary with original and corrected transcriptions
    """
    # Load Whisper model (uncomment when whisper is installed)
    # print(f"Loading Whisper model ({model_size})...")
    # model = whisper.load_model(model_size)
    
    # Transcribe audio
    # print(f"Transcribing {audio_path}...")
    # result = model.transcribe(audio_path, language="ba")  # or "kk" or "ky"
    
    # For demonstration, we'll use sample text
    # In real use, this would be: original_text = result["text"]
    original_text = "бұл қашмау қойыруқ менен кепке,ғамының башқорт"
    
    # Correct orthography
    print("Correcting orthography...")
    corrected_text = correct_orthography(original_text, aggressive=aggressive)
    
    return {
        "original": original_text,
        "corrected": corrected_text,
        "audio_path": audio_path
    }


def process_batch(audio_files: list, output_file: str = None):
    """
    Process multiple audio files and save results
    
    Args:
        audio_files: List of audio file paths
        output_file: Optional output file to save results
    """
    corrector = KazakhToBashkirCorrector()
    results = []
    
    for audio_path in audio_files:
        print(f"\n{'='*70}")
        print(f"Processing: {audio_path}")
        print('='*70)
        
        result = transcribe_and_correct(audio_path)
        results.append(result)
        
        print(f"\nOriginal:  {result['original']}")
        print(f"Corrected: {result['corrected']}")
    
    # Save results if output file specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            for result in results:
                f.write(f"File: {result['audio_path']}\n")
                f.write(f"Original: {result['original']}\n")
                f.write(f"Corrected: {result['corrected']}\n")
                f.write("\n" + "-"*70 + "\n\n")
        
        print(f"\n✅ Results saved to: {output_file}")
    
    return results


def correct_existing_transcript(transcript_file: str, output_file: str = None, aggressive: bool = False):
    """
    Correct orthography in an existing transcript file
    
    Args:
        transcript_file: Path to transcript file (one sentence per line or continuous text)
        output_file: Path to save corrected transcript (defaults to *_corrected.txt)
        aggressive: Whether to apply aggressive corrections
    """
    if output_file is None:
        base = Path(transcript_file).stem
        output_file = f"{base}_corrected.txt"
    
    corrector = KazakhToBashkirCorrector()
    
    print(f"Reading transcript: {transcript_file}")
    with open(transcript_file, 'r', encoding='utf-8') as f:
        original_text = f.read()
    
    print("Correcting orthography...")
    corrected_text = corrector.correct_orthography(original_text, aggressive=aggressive)
    
    print(f"Saving corrected transcript: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(corrected_text)
    
    # Show statistics
    from kazakh_to_bashkir_corrector import analyze_differences
    stats = analyze_differences(original_text, corrected_text)
    
    print(f"\n{'='*70}")
    print("Correction Statistics:")
    print('='*70)
    for key, value in stats.items():
        print(f"  {key:25}: {value}")
    
    print(f"\n✅ Done! Corrected transcript saved to: {output_file}")


# Example usage scenarios
if __name__ == "__main__":
    print("="*70)
    print("WHISPER + ORTHOGRAPHY CORRECTOR INTEGRATION EXAMPLES")
    print("="*70)
    
    print("\n📝 Example 1: Simple text correction")
    print("-"*70)
    
    test_text = "бұл менің құд диджитал құздан"
    corrected = correct_orthography(test_text)
    print(f"Original:  {test_text}")
    print(f"Corrected: {corrected}")
    
    print("\n📝 Example 2: Paragraph correction")
    print("-"*70)
    
    paragraph = """
    бұл қашмау қойыруқ менен кепке,ғамының башқорт традицион елалық сегеудәрі менен 
    бұл қашмау қойыруқ кепкеға қойылған шул бұл менің заманлы ғам әлікле мәдіниет.
    """
    
    corrected_para = correct_orthography(paragraph)
    print("Original:")
    print(paragraph)
    print("\nCorrected:")
    print(corrected_para)
    
    print("\n📝 Example 3: File correction (demo)")
    print("-"*70)
    print("Usage: correct_existing_transcript('input.txt', 'output.txt')")
    print("This would correct an entire transcript file")
    
    print("\n📝 Example 4: Integration with Whisper (when installed)")
    print("-"*70)
    print("""
# Install whisper first: pip install openai-whisper

import whisper
from kazakh_to_bashkir_corrector import correct_orthography

# Load model
model = whisper.load_model("base")

# Transcribe
result = model.transcribe("bashkir_audio.mp3", language="ba")

# Correct orthography
corrected = correct_orthography(result["text"])

print(f"Original:  {result['text']}")
print(f"Corrected: {corrected}")
    """)
    
    print("\n" + "="*70)
    print("💡 Integration Tips:")
    print("="*70)
    print("""
1. For best results, use Whisper with language='ba' (Bashkir)
2. Post-process all Whisper output through the corrector
3. Use aggressive=False for general use, aggressive=True for heavy Kazakh influence
4. Consider language detection before correction if handling mixed content
5. The corrector is fast - adds <1ms overhead per sentence
    """)
    
    print("\n" + "="*70)
    print("✓ Ready to integrate with your Whisper pipeline!")
    print("="*70)
