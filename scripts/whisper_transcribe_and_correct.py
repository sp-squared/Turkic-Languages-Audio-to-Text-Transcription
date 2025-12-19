#!/usr/bin/env python3
"""
Whisper Transcription with Kazakh-to-Bashkir Orthography Correction

This script demonstrates:
1. Loading and transcribing an audio file with Whisper
2. Applying orthography correction to fix Kazakh patterns
3. Saving results in multiple formats
4. Showing detailed comparison and statistics

USAGE:
    python whisper_transcribe_and_correct.py <audio_file>
    
EXAMPLE:
    python whisper_transcribe_and_correct.py audio_clip.m4a
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Import Whisper
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("⚠️  Warning: whisper not installed. Install with: pip install openai-whisper")

# Import our corrector
sys.path.append(str(Path(__file__).parent))
from kazakh_to_bashkir_corrector import (
    correct_orthography, 
    KazakhToBashkirCorrector,
    analyze_differences
)


def transcribe_with_correction(
    audio_path: str,
    model_size: str = "base",
    language: str = "ba",
    aggressive_correction: bool = False,
    output_dir: str = None
):
    """
    Transcribe audio with Whisper and correct orthography
    
    Args:
        audio_path: Path to audio file
        model_size: Whisper model size (tiny, base, small, medium, large)
        language: Language code (ba=Bashkir, kk=Kazakh, ky=Kyrgyz)
        aggressive_correction: Whether to apply aggressive corrections
        output_dir: Directory to save results (defaults to same as audio file)
    
    Returns:
        Dictionary with transcription results and corrections
    """
    audio_path = Path(audio_path)
    
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Set output directory
    if output_dir is None:
        output_dir = audio_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("WHISPER TRANSCRIPTION WITH ORTHOGRAPHY CORRECTION")
    print("=" * 80)
    print(f"\n📁 Audio File: {audio_path.name}")
    print(f"📊 File Size: {audio_path.stat().st_size / 1024:.1f} KB")
    print(f"🤖 Model: {model_size}")
    print(f"🗣️  Language: {language}")
    print(f"⚙️  Aggressive Correction: {aggressive_correction}")
    
    if not WHISPER_AVAILABLE:
        print("\n❌ Whisper is not installed. Cannot transcribe.")
        print("   Install with: pip install openai-whisper")
        return None
    
    # Step 1: Load Whisper model
    print(f"\n{'='*80}")
    print("STEP 1: Loading Whisper Model")
    print('='*80)
    print(f"Loading Whisper '{model_size}' model...")
    
    try:
        model = whisper.load_model(model_size)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None
    
    # Step 2: Transcribe audio
    print(f"\n{'='*80}")
    print("STEP 2: Transcribing Audio")
    print('='*80)
    print("Transcribing... (this may take a moment)")
    
    try:
        result = model.transcribe(
            str(audio_path),
            language=language,
            verbose=False
        )
        
        original_text = result["text"].strip()
        segments = result.get("segments", [])
        
        print("✅ Transcription complete!")
        print(f"\n📝 Original Transcription (length: {len(original_text)} chars):")
        print("-" * 80)
        print(original_text)
        
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        return None
    
    # Step 3: Apply orthography correction
    print(f"\n{'='*80}")
    print("STEP 3: Correcting Orthography")
    print('='*80)
    print("Applying Kazakh → Bashkir corrections...")
    
    corrector = KazakhToBashkirCorrector()
    corrected_text = corrector.correct_orthography(original_text, aggressive=aggressive_correction)
    
    print("✅ Correction complete!")
    print(f"\n📝 Corrected Transcription (length: {len(corrected_text)} chars):")
    print("-" * 80)
    print(corrected_text)
    
    # Step 4: Analyze corrections
    print(f"\n{'='*80}")
    print("STEP 4: Correction Analysis")
    print('='*80)
    
    stats = analyze_differences(original_text, corrected_text)
    
    print("\n📊 Correction Statistics:")
    for key, value in stats.items():
        print(f"  {key:25}: {value}")
    
    # Show specific changes
    print("\n🔍 Specific Changes Made:")
    corrections_made = []
    
    # Track changes
    if stats['ұ→у'] > 0:
        corrections_made.append(f"  • ұ → у: {stats['ұ→у']} occurrences")
    if stats['і→и'] > 0:
        corrections_made.append(f"  • і → и: {stats['і→и']} occurrences")
    if stats['ғ→х'] > 0:
        corrections_made.append(f"  • ғ → х: {stats['ғ→х']} occurrences")
    if stats['қ→к/х'] > 0:
        corrections_made.append(f"  • қ → к/х: {stats['қ→к/х']} occurrences")
    
    if corrections_made:
        for correction in corrections_made:
            print(correction)
    else:
        print("  No orthographic corrections needed - text already in proper Bashkir!")
    
    # Step 5: Correct segments (with timestamps)
    print(f"\n{'='*80}")
    print("STEP 5: Processing Segments with Timestamps")
    print('='*80)
    
    corrected_segments = []
    for seg in segments:
        corrected_seg = {
            "id": seg["id"],
            "start": seg["start"],
            "end": seg["end"],
            "original_text": seg["text"].strip(),
            "corrected_text": corrector.correct_orthography(seg["text"].strip(), aggressive=aggressive_correction)
        }
        corrected_segments.append(corrected_seg)
    
    print(f"✅ Processed {len(corrected_segments)} segments")
    
    # Show first few segments
    print(f"\n📋 First 3 Segments (with timestamps):")
    for seg in corrected_segments[:3]:
        print(f"\n  [{seg['start']:.2f}s - {seg['end']:.2f}s]")
        if seg['original_text'] != seg['corrected_text']:
            print(f"  Original:  {seg['original_text']}")
            print(f"  Corrected: {seg['corrected_text']}")
        else:
            print(f"  Text: {seg['corrected_text']}")
    
    if len(corrected_segments) > 3:
        print(f"\n  ... and {len(corrected_segments) - 3} more segments")
    
    # Step 6: Save results
    print(f"\n{'='*80}")
    print("STEP 6: Saving Results")
    print('='*80)
    
    base_name = audio_path.stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save plain text files
    original_file = output_dir / f"{base_name}_original.txt"
    corrected_file = output_dir / f"{base_name}_corrected.txt"
    
    with open(original_file, 'w', encoding='utf-8') as f:
        f.write(original_text)
    print(f"✅ Saved original: {original_file}")
    
    with open(corrected_file, 'w', encoding='utf-8') as f:
        f.write(corrected_text)
    print(f"✅ Saved corrected: {corrected_file}")
    
    # Save JSON with full details
    json_file = output_dir / f"{base_name}_transcription_{timestamp}.json"
    
    full_result = {
        "metadata": {
            "audio_file": str(audio_path),
            "audio_size_kb": audio_path.stat().st_size / 1024,
            "model": model_size,
            "language": language,
            "timestamp": timestamp,
            "aggressive_correction": aggressive_correction
        },
        "transcription": {
            "original_text": original_text,
            "corrected_text": corrected_text
        },
        "statistics": stats,
        "segments": corrected_segments
    }
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(full_result, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved JSON: {json_file}")
    
    # Save comparison report
    report_file = output_dir / f"{base_name}_comparison_report.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("WHISPER TRANSCRIPTION COMPARISON REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Audio File: {audio_path.name}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Model: {model_size}\n")
        f.write(f"Language: {language}\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("ORIGINAL TRANSCRIPTION (with Kazakh orthography)\n")
        f.write("-" * 80 + "\n")
        f.write(original_text + "\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("CORRECTED TRANSCRIPTION (Bashkir orthography)\n")
        f.write("-" * 80 + "\n")
        f.write(corrected_text + "\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("CORRECTION STATISTICS\n")
        f.write("-" * 80 + "\n")
        for key, value in stats.items():
            f.write(f"{key:30}: {value}\n")
        
        f.write("\n" + "-" * 80 + "\n")
        f.write("SEGMENTS WITH TIMESTAMPS\n")
        f.write("-" * 80 + "\n\n")
        
        for seg in corrected_segments:
            f.write(f"[{seg['start']:.2f}s - {seg['end']:.2f}s]\n")
            if seg['original_text'] != seg['corrected_text']:
                f.write(f"Original:  {seg['original_text']}\n")
                f.write(f"Corrected: {seg['corrected_text']}\n\n")
            else:
                f.write(f"Text: {seg['corrected_text']}\n\n")
    
    print(f"✅ Saved report: {report_file}")
    
    # Final summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print('='*80)
    print(f"\n✅ Transcription complete!")
    print(f"📁 Files saved to: {output_dir}")
    print(f"📊 Total corrections: {stats['total_chars_changed']} characters changed")
    print(f"📝 Segments processed: {len(corrected_segments)}")
    
    return full_result


def main():
    """Main function to run from command line"""
    
    if len(sys.argv) < 2:
        print("Usage: python whisper_transcribe_and_correct.py <audio_file> [model_size] [language]")
        print("\nExample:")
        print("  python whisper_transcribe_and_correct.py audio_clip.m4a")
        print("  python whisper_transcribe_and_correct.py audio_clip.m4a medium ba")
        print("\nModel sizes: tiny, base, small, medium, large")
        print("Languages: ba (Bashkir), kk (Kazakh), ky (Kyrgyz)")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "base"
    language = sys.argv[3] if len(sys.argv) > 3 else "ba"
    
    try:
        result = transcribe_with_correction(
            audio_file,
            model_size=model_size,
            language=language,
            aggressive_correction=False
        )
        
        if result:
            print("\n" + "="*80)
            print("✓ SUCCESS! All files saved.")
            print("="*80)
        else:
            print("\n❌ Transcription failed. Check the errors above.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
