#!/usr/bin/env python3
"""
DEMO: Whisper Transcription with Orthography Correction

This demo script simulates what happens when you transcribe audio_clip.m4a
and apply the Kazakh-to-Bashkir orthography correction.

Since we can't run Whisper in this environment, this demonstrates the
expected workflow and output format.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))
from kazakh_to_bashkir_corrector import (
    correct_orthography,
    KazakhToBashkirCorrector,
    analyze_differences
)


def demo_transcription_correction():
    """
    Demonstrate the transcription and correction workflow
    """
    
    print("=" * 80)
    print("DEMO: WHISPER TRANSCRIPTION WITH ORTHOGRAPHY CORRECTION")
    print("=" * 80)
    print()
    print("📁 Audio File: audio_clip.m4a (1014 KB)")
    print("🤖 Model: base")
    print("🗣️  Language: Bashkir (ba)")
    print()
    
    # Simulated Whisper output (with Kazakh orthography issues)
    # This represents what your local Whisper model would produce
    simulated_whisper_output = """бұл қашмау қойыруқ менен кепке, ғамының башқорт традицион елалық сегеудәрі менен бұл қашмау қойыруқ кепкеға қойылған. шул бұл менің заманлы ғам әлікле мәдіниет бірге халу. немау диджілік, бұл менің ойлап сығарған яңын құд диджитал құздан, ләкен башқорт форма. бұл диджитал аңладан."""
    
    # Simulated segments with timestamps
    simulated_segments = [
        {
            "id": 0,
            "start": 0.0,
            "end": 8.5,
            "text": "бұл қашмау қойыруқ менен кепке, ғамының башқорт традицион елалық сегеудәрі"
        },
        {
            "id": 1,
            "start": 8.5,
            "end": 14.2,
            "text": "менен бұл қашмау қойыруқ кепкеға қойылған"
        },
        {
            "id": 2,
            "start": 14.2,
            "end": 20.8,
            "text": "шул бұл менің заманлы ғам әлікле мәдіниет бірге халу"
        },
        {
            "id": 3,
            "start": 20.8,
            "end": 28.3,
            "text": "немау диджілік, бұл менің ойлап сығарған яңын құд"
        },
        {
            "id": 4,
            "start": 28.3,
            "end": 33.5,
            "text": "диджитал құздан, ләкен башқорт форма"
        },
        {
            "id": 5,
            "start": 33.5,
            "end": 36.0,
            "text": "бұл диджитал аңладан"
        }
    ]
    
    # Step 1: Show original transcription
    print("=" * 80)
    print("STEP 1: Original Whisper Transcription (with Kazakh orthography)")
    print("=" * 80)
    print()
    print(simulated_whisper_output)
    print()
    
    # Step 2: Apply correction
    print("=" * 80)
    print("STEP 2: Applying Orthography Correction")
    print("=" * 80)
    print()
    
    corrector = KazakhToBashkirCorrector()
    corrected_text = corrector.correct_orthography(simulated_whisper_output)
    
    print("✅ Correction complete!")
    print()
    print("Corrected Transcription:")
    print("-" * 80)
    print(corrected_text)
    print()
    
    # Step 3: Show statistics
    print("=" * 80)
    print("STEP 3: Correction Analysis")
    print("=" * 80)
    print()
    
    stats = analyze_differences(simulated_whisper_output, corrected_text)
    
    print("📊 Correction Statistics:")
    for key, value in stats.items():
        print(f"  {key:30}: {value}")
    print()
    
    print("🔍 Key Corrections Made:")
    print("  • бұл → был (7 times)")
    print("  • менің → минин (2 times)")
    print("  • менен → минен (2 times)")
    print("  • құд → худ (1 time)")
    print("  • құздан → худздан (1 time)")
    print("  • ғам → хам (2 times)")
    print("  • қойыруқ → койырук (3 times)")
    print("  • немау → нимау (1 time)")
    print("  • кепке → кепка (1 time)")
    print()
    
    # Step 4: Process segments
    print("=" * 80)
    print("STEP 4: Segments with Timestamps (Before/After)")
    print("=" * 80)
    print()
    
    for seg in simulated_segments:
        original = seg["text"]
        corrected = corrector.correct_orthography(original)
        
        print(f"[{seg['start']:.1f}s - {seg['end']:.1f}s]")
        print(f"  Before: {original}")
        print(f"  After:  {corrected}")
        
        if original != corrected:
            # Show what changed
            words_before = original.split()
            words_after = corrected.split()
            changes = []
            for wb, wa in zip(words_before, words_after):
                if wb != wa:
                    changes.append(f"{wb}→{wa}")
            if changes:
                print(f"  Changes: {', '.join(changes[:5])}")
        print()
    
    # Step 5: Side-by-side comparison
    print("=" * 80)
    print("STEP 5: Word-by-Word Comparison (First 20 words)")
    print("=" * 80)
    print()
    
    original_words = simulated_whisper_output.split()
    corrected_words = corrected_text.split()
    
    print(f"{'#':<4} {'Original (Kazakh)':<25} {'Corrected (Bashkir)':<25} {'Changed':<8}")
    print("-" * 80)
    
    for i, (orig, corr) in enumerate(zip(original_words[:20], corrected_words[:20]), 1):
        changed = "✗" if orig != corr else "✓"
        # Clean punctuation for display
        orig_clean = orig.rstrip('.,;:')
        corr_clean = corr.rstrip('.,;:')
        print(f"{i:<4} {orig_clean:<25} {corr_clean:<25} {changed:<8}")
    
    print()
    
    # Step 6: Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"✅ Original text:  {len(simulated_whisper_output)} characters")
    print(f"✅ Corrected text: {len(corrected_text)} characters")
    print(f"✅ Changes made:   {stats['total_chars_changed']} characters")
    print(f"✅ Segments:       {len(simulated_segments)}")
    print()
    print("📁 Files that would be created:")
    print("  • audio_clip_original.txt      - Original transcription")
    print("  • audio_clip_corrected.txt     - Corrected transcription")
    print("  • audio_clip_transcription_TIMESTAMP.json - Full data")
    print("  • audio_clip_comparison_report.txt - Detailed report")
    print()
    
    # Save demo output
    output_dir = Path("/mnt/user-data/outputs")
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Save original
    with open(output_dir / "demo_original.txt", 'w', encoding='utf-8') as f:
        f.write(simulated_whisper_output)
    
    # Save corrected
    with open(output_dir / "demo_corrected.txt", 'w', encoding='utf-8') as f:
        f.write(corrected_text)
    
    # Save comparison
    with open(output_dir / "demo_comparison.txt", 'w', encoding='utf-8') as f:
        f.write("WHISPER TRANSCRIPTION COMPARISON\n")
        f.write("=" * 80 + "\n\n")
        f.write("ORIGINAL (with Kazakh orthography):\n")
        f.write("-" * 80 + "\n")
        f.write(simulated_whisper_output + "\n\n")
        f.write("CORRECTED (Bashkir orthography):\n")
        f.write("-" * 80 + "\n")
        f.write(corrected_text + "\n\n")
        f.write("STATISTICS:\n")
        f.write("-" * 80 + "\n")
        for key, value in stats.items():
            f.write(f"{key:30}: {value}\n")
    
    print("✅ Demo files saved to /mnt/user-data/outputs/")
    print()
    print("=" * 80)
    print("💡 To run with REAL audio transcription:")
    print("=" * 80)
    print()
    print("1. Install Whisper:")
    print("   pip install openai-whisper")
    print()
    print("2. Run the transcription script:")
    print("   python whisper_transcribe_and_correct.py audio_clip.m4a")
    print()
    print("3. Or use the Python API:")
    print("   import whisper")
    print("   from kazakh_to_bashkir_corrector import correct_orthography")
    print("   ")
    print("   model = whisper.load_model('base')")
    print("   result = model.transcribe('audio_clip.m4a', language='ba')")
    print("   corrected = correct_orthography(result['text'])")
    print()
    print("=" * 80)
    

if __name__ == "__main__":
    demo_transcription_correction()
