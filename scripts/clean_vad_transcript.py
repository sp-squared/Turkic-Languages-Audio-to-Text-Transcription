#!/usr/bin/env python3
"""
Clean VAD Transcript + Orthography Correction

This script handles transcripts where timestamps are on the same line as text:
    00:00:00Бұл қашмау қойыруқ менен кепке,
    
It will:
1. Remove timestamps (format: 00:00:00)
2. Extract and clean the text
3. Apply Kazakh→Bashkir orthography correction
4. Save multiple output formats

USAGE:
    python clean_vad_transcript.py <input_file> [output_file]
    
EXAMPLE:
    python clean_vad_transcript.py audio_clip_vad.txt audio_clip_cleaned.txt
"""

import re
import sys
from pathlib import Path
from datetime import datetime

# Import the corrector
try:
    from kazakh_to_bashkir_corrector import (
        correct_orthography,
        KazakhToBashkirCorrector,
        analyze_differences
    )
    CORRECTOR_AVAILABLE = True
except ImportError:
    CORRECTOR_AVAILABLE = False
    print("⚠️  Warning: Corrector not found in same directory")


def parse_timestamp_line(line: str) -> tuple:
    """
    Parse a line with timestamp at the beginning
    Format: 00:00:00Text or 00:00:00 Text
    
    Returns:
        (timestamp, text) tuple
    """
    # Match timestamp at start: HH:MM:SS
    match = re.match(r'^(\d{2}:\d{2}:\d{2})\s*(.*)$', line)
    
    if match:
        timestamp = match.group(1)
        text = match.group(2).strip()
        return timestamp, text
    else:
        # No timestamp found, return entire line as text
        return None, line.strip()


def clean_vad_transcript(
    input_file: str,
    output_file: str = None,
    apply_correction: bool = True,
    aggressive: bool = False
):
    """
    Clean VAD transcript and optionally apply orthography correction
    
    Args:
        input_file: Path to input transcript file
        output_file: Path to save cleaned text (default: input_cleaned.txt)
        apply_correction: Whether to apply orthography correction
        aggressive: Whether to use aggressive correction mode
    
    Returns:
        Dictionary with results
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Set output file if not provided
    if output_file is None:
        output_file = str(input_path.parent / f"{input_path.stem}_cleaned.txt")
    
    output_path = Path(output_file)
    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("VAD TRANSCRIPT CLEANER + ORTHOGRAPHY CORRECTOR")
    print("=" * 80)
    print(f"\n📁 Input:  {input_path.name}")
    print(f"📁 Output: {output_path.name}")
    print(f"⚙️  Correction: {'Enabled' if apply_correction else 'Disabled'}")
    if apply_correction and not CORRECTOR_AVAILABLE:
        print("⚠️  Warning: Corrector not available, skipping correction")
        apply_correction = False
    print()
    
    # Step 1: Read and parse file
    print("=" * 80)
    print("STEP 1: Reading and Parsing")
    print("=" * 80)
    
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"✅ Read {len(lines)} lines")
    
    # Parse each line
    segments = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        timestamp, text = parse_timestamp_line(line)
        if text:  # Only add if there's actual text
            segments.append({
                'timestamp': timestamp,
                'text': text
            })
    
    print(f"✅ Parsed {len(segments)} segments with text")
    
    # Step 2: Combine text
    print(f"\n{'=' * 80}")
    print("STEP 2: Extracting Text")
    print("=" * 80)
    
    # Combine all text (without timestamps)
    all_text = ' '.join(seg['text'] for seg in segments)
    
    print(f"✅ Extracted {len(all_text)} characters")
    print(f"✅ Word count: {len(all_text.split())} words")
    print()
    print("Preview (first 150 chars):")
    print("-" * 80)
    print(all_text[:150] + "...")
    
    # Step 3: Apply orthography correction (if enabled)
    corrected_text = all_text
    stats = None
    
    if apply_correction and CORRECTOR_AVAILABLE:
        print(f"\n{'=' * 80}")
        print("STEP 3: Applying Orthography Correction")
        print("=" * 80)
        
        corrector = KazakhToBashkirCorrector()
        corrected_text = corrector.correct_orthography(all_text, aggressive=aggressive)
        
        print("✅ Correction complete!")
        print()
        print("Corrected preview (first 150 chars):")
        print("-" * 80)
        print(corrected_text[:150] + "...")
        
        # Get statistics
        stats = analyze_differences(all_text, corrected_text)
        
        print(f"\n📊 Correction Statistics:")
        for key, value in stats.items():
            print(f"  {key:30}: {value}")
    else:
        print(f"\n{'=' * 80}")
        print("STEP 3: Skipping Correction")
        print("=" * 80)
        print("Correction disabled or unavailable")
    
    # Step 4: Correct individual segments (for structured output)
    print(f"\n{'=' * 80}")
    print("STEP 4: Processing Segments")
    print("=" * 80)
    
    if apply_correction and CORRECTOR_AVAILABLE:
        corrected_segments = []
        for seg in segments:
            corrected_seg = {
                'timestamp': seg['timestamp'],
                'original_text': seg['text'],
                'corrected_text': corrector.correct_orthography(seg['text'], aggressive=aggressive)
            }
            corrected_segments.append(corrected_seg)
        print(f"✅ Corrected {len(corrected_segments)} segments")
    else:
        corrected_segments = [
            {
                'timestamp': seg['timestamp'],
                'text': seg['text']
            }
            for seg in segments
        ]
        print(f"✅ Processed {len(corrected_segments)} segments")
    
    # Step 5: Save outputs
    print(f"\n{'=' * 80}")
    print("STEP 5: Saving Results")
    print("=" * 80)
    
    base_name = output_path.stem
    
    # Save plain text (original without timestamps)
    original_file = output_dir / f"{base_name}_original.txt"
    with open(original_file, 'w', encoding='utf-8') as f:
        f.write(all_text)
    print(f"✅ Saved original: {original_file.name}")
    
    # Save corrected text
    corrected_file = output_dir / f"{base_name}_corrected.txt"
    with open(corrected_file, 'w', encoding='utf-8') as f:
        f.write(corrected_text)
    print(f"✅ Saved corrected: {corrected_file.name}")
    
    # Save structured version with timestamps
    structured_file = output_dir / f"{base_name}_with_timestamps.txt"
    with open(structured_file, 'w', encoding='utf-8') as f:
        if apply_correction and CORRECTOR_AVAILABLE:
            for seg in corrected_segments:
                f.write(f"[{seg['timestamp']}]\n")
                if seg['original_text'] != seg['corrected_text']:
                    f.write(f"Original:  {seg['original_text']}\n")
                    f.write(f"Corrected: {seg['corrected_text']}\n\n")
                else:
                    f.write(f"{seg['corrected_text']}\n\n")
        else:
            for seg in corrected_segments:
                f.write(f"[{seg['timestamp']}] {seg['text']}\n")
    print(f"✅ Saved structured: {structured_file.name}")
    
    # Save comparison report (if correction applied)
    if apply_correction and CORRECTOR_AVAILABLE and stats:
        report_file = output_dir / f"{base_name}_comparison_report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("VAD TRANSCRIPT COMPARISON REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Input File: {input_path.name}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Segments: {len(segments)}\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("ORIGINAL TEXT (without timestamps)\n")
            f.write("-" * 80 + "\n")
            f.write(all_text + "\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("CORRECTED TEXT (Bashkir orthography)\n")
            f.write("-" * 80 + "\n")
            f.write(corrected_text + "\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("CORRECTION STATISTICS\n")
            f.write("-" * 80 + "\n")
            for key, value in stats.items():
                f.write(f"{key:35}: {value}\n")
            
            f.write("\n" + "-" * 80 + "\n")
            f.write("SEGMENTS WITH TIMESTAMPS\n")
            f.write("-" * 80 + "\n\n")
            
            for seg in corrected_segments:
                f.write(f"[{seg['timestamp']}]\n")
                if seg['original_text'] != seg['corrected_text']:
                    f.write(f"Original:  {seg['original_text']}\n")
                    f.write(f"Corrected: {seg['corrected_text']}\n\n")
                else:
                    f.write(f"Text: {seg['corrected_text']}\n\n")
        
        print(f"✅ Saved report: {report_file.name}")
    
    # Step 6: Summary
    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print("=" * 80)
    print(f"\n✅ Processing complete!")
    print(f"📊 Segments: {len(segments)}")
    print(f"📝 Characters: {len(all_text)}")
    print(f"📝 Words: {len(all_text.split())}")
    
    if stats:
        print(f"🔧 Corrections: {stats['total_chars_changed']} characters changed")
    
    print(f"\n📁 Files saved to: {output_dir}")
    
    # Show file list
    print(f"\n📄 Output files:")
    print(f"  1. {original_file.name} - Original text without timestamps")
    print(f"  2. {corrected_file.name} - Corrected Bashkir text")
    print(f"  3. {structured_file.name} - Text with timestamps")
    if apply_correction and stats:
        print(f"  4. {report_file.name} - Detailed comparison report")
    
    print(f"\n{'=' * 80}")
    
    return {
        'segments': corrected_segments if apply_correction else segments,
        'original_text': all_text,
        'corrected_text': corrected_text,
        'statistics': stats,
        'output_files': {
            'original': str(original_file),
            'corrected': str(corrected_file),
            'structured': str(structured_file),
            'report': str(report_file) if apply_correction and stats else None
        }
    }


def main():
    """Main function for command-line usage"""
    
    if len(sys.argv) < 2:
        print("Usage: python clean_vad_transcript.py <input_file> [output_file]")
        print("\nExample:")
        print("  python clean_vad_transcript.py audio_clip_vad.txt")
        print("  python clean_vad_transcript.py audio_clip_vad.txt output.txt")
        print("\nThis will:")
        print("  1. Remove timestamps from lines like: 00:00:00Text")
        print("  2. Extract clean text")
        print("  3. Apply Kazakh→Bashkir orthography correction")
        print("  4. Save multiple output formats")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        result = clean_vad_transcript(
            input_file,
            output_file,
            apply_correction=True,
            aggressive=False
        )
        
        print("\n✓ SUCCESS!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
