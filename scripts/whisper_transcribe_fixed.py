#!/usr/bin/env python3
"""
Fixed Whisper Transcription with Auto-Language Detection

USAGE:
    python whisper_transcribe_fixed.py <audio_file> [model_size] [language]
    
EXAMPLES:
    # Auto-detect language (RECOMMENDED)
    python whisper_transcribe_fixed.py ../audio/big_clip_file.m4a
    
    # Force Russian (works well for Bashkir)
    python whisper_transcribe_fixed.py ../audio/big_clip_file.m4a base ru
    
    # Force Kazakh (linguistically close to Bashkir)
    python whisper_transcribe_fixed.py ../audio/big_clip_file.m4a base kk
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
    language: str = None,  # Changed default to None for auto-detect
    aggressive_correction: bool = False,
    output_dir: str = None
):
    """
    Transcribe audio with Whisper and correct orthography
    
    Args:
        audio_path: Path to audio file
        model_size: Whisper model size (tiny, base, small, medium, large)
        language: Language code (None=auto, ru=Russian, kk=Kazakh, ky=Kyrgyz)
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
    print("WHISPER TRANSCRIPTION WITH ORTHOGRAPHY CORRECTION (FIXED)")
    print("=" * 80)
    print(f"\n📁 Audio File: {audio_path.name}")
    print(f"📊 File Size: {audio_path.stat().st_size / 1024:.1f} KB")
    print(f"🤖 Model: {model_size}")
    
    # Language handling
    language_names = {'ru': 'Russian', 'kk': 'Kazakh', 'ky': 'Kyrgyz'}
    
    if language is None:
        print(f"🗣️  Language: AUTO-DETECT (recommended for Bashkir)")
    elif language in language_names:
        print(f"🗣️  Language: {language} ({language_names[language]})")
    else:
        print(f"⚠️  WARNING: Language '{language}' may not be supported by Whisper!")
        print(f"   Consider using: None (auto), 'ru' (Russian), or 'kk' (Kazakh)")
    
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
        # Transcribe with language parameter
        if language is None:
            print("🔍 Auto-detecting language...")
            result = model.transcribe(str(audio_path))
            detected_lang = result.get('language', 'unknown')
            print(f"✅ Detected language: {detected_lang}")
        else:
            result = model.transcribe(str(audio_path), language=language)
        
        print("✅ Transcription complete!")
        
        # Get text and segments
        original_text = result["text"].strip()
        segments = result.get("segments", [])
        
        print(f"\n📝 Original Transcription (length: {len(original_text)} chars):")
        print("-" * 80)
        print(original_text[:500])  # Show first 500 chars
        if len(original_text) > 500:
            print(f"\n... (showing first 500 of {len(original_text)} characters)")
        
        # Check if transcription looks valid
        if len(original_text) < 10:
            print("\n⚠️  WARNING: Very short transcription! Audio might be:")
            print("   - Silent or very quiet")
            print("   - Corrupted")
            print("   - Not in a supported language")
        
        # Check for hallucination indicators
        if any(char in original_text for char in ['魔', '�', '\ufffd']):
            print("\n⚠️  WARNING: Non-standard characters detected!")
            print("   This might indicate hallucination or encoding issues.")
            print("   Try:")
            print("   1. Use language=None for auto-detect")
            print("   2. Use language='ru' (Russian)")
            print("   3. Check audio file quality")
        
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        return None
    
    # Step 3: Correct orthography
    print(f"\n{'='*80}")
    print("STEP 3: Correcting Orthography")
    print('='*80)
    print("Applying Kazakh → Bashkir corrections...")
    
    corrected_text = correct_orthography(original_text, aggressive=aggressive_correction)
    
    print("✅ Correction complete!")
    print(f"\n📝 Corrected Transcription (length: {len(corrected_text)} chars):")
    print("-" * 80)
    print(corrected_text[:500])
    if len(corrected_text) > 500:
        print(f"\n... (showing first 500 of {len(corrected_text)} characters)")
    
    # Step 4: Analysis
    print(f"\n{'='*80}")
    print("STEP 4: Correction Analysis")
    print('='*80)
    
    stats = analyze_differences(original_text, corrected_text)
    
    print(f"\n📊 Correction Statistics:")
    for key, value in stats.items():
        print(f"  {key:<25}: {value}")
    
    if stats['total_chars_changed'] == 0:
        print("\n🔍 Specific Changes Made:")
        print("  No orthographic corrections needed - text already in proper Bashkir!")
    
    # Step 5: Process segments
    print(f"\n{'='*80}")
    print("STEP 5: Processing Segments with Timestamps")
    print('='*80)
    
    corrected_segments = []
    for seg in segments:
        corrected_seg = {
            "start": seg["start"],
            "end": seg["end"],
            "original_text": seg["text"].strip(),
            "corrected_text": correct_orthography(seg["text"].strip(), aggressive=aggressive_correction)
        }
        corrected_segments.append(corrected_seg)
    
    print(f"✅ Processed {len(segments)} segments")
    
    # Show first few segments
    if segments:
        print(f"\n📋 First 3 Segments (with timestamps):\n")
        for i, seg in enumerate(corrected_segments[:3]):
            print(f"  [{seg['start']:.2f}s - {seg['end']:.2f}s]")
            print(f"  Text: {seg['corrected_text']}\n")
        
        if len(segments) > 3:
            print(f"  ... and {len(segments) - 3} more segments")
    
    # Step 6: Save results
    print(f"\n{'='*80}")
    print("STEP 6: Saving Results")
    print('='*80)
    
    base_name = audio_path.stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save original transcription
    original_file = output_dir / f"{base_name}_original.txt"
    with open(original_file, 'w', encoding='utf-8') as f:
        f.write(original_text)
    print(f"✅ Saved original: {original_file}")
    
    # Save corrected transcription
    corrected_file = output_dir / f"{base_name}_corrected.txt"
    with open(corrected_file, 'w', encoding='utf-8') as f:
        f.write(corrected_text)
    print(f"✅ Saved corrected: {corrected_file}")
    
    # Save JSON with full data
    json_file = output_dir / f"{base_name}_transcription_{timestamp}.json"
    json_data = {
        "metadata": {
            "audio_file": audio_path.name,
            "transcription_date": timestamp,
            "model": model_size,
            "language": language if language else "auto-detected: " + result.get('language', 'unknown'),
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
        json.dump(json_data, f, ensure_ascii=False, indent=2)
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
        f.write(f"Language: {language if language else 'auto-detected: ' + result.get('language', 'unknown')}\n\n")
        
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
            f.write(f"{key:<30}: {value}\n")
    
    print(f"✅ Saved report: {report_file}")
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print('='*80)
    print(f"\n✅ Transcription complete!")
    print(f"📁 Files saved to: {output_dir}")
    print(f"📊 Total corrections: {stats['total_chars_changed']} characters changed")
    print(f"📝 Segments processed: {len(segments)}")
    
    print(f"\n{'='*80}")
    print("✓ SUCCESS! All files saved.")
    print('='*80)
    
    return json_data


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python whisper_transcribe_fixed.py <audio_file> [model_size] [language]")
        print("\nExamples:")
        print("  python whisper_transcribe_fixed.py audio.m4a")
        print("  python whisper_transcribe_fixed.py audio.m4a base ru")
        print("  python whisper_transcribe_fixed.py audio.m4a medium kk")
        print("\nSupported languages: None (auto), ru (Russian), kk (Kazakh), ky (Kyrgyz)")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "base"
    language = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Convert "None" string to actual None
    if language and language.lower() in ['none', 'auto', 'null']:
        language = None
    
    try:
        result = transcribe_with_correction(
            audio_path=audio_file,
            model_size=model_size,
            language=language
        )
        
        if result is None:
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
