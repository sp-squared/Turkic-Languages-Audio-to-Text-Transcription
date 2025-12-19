#!/usr/bin/env python3
"""
Clean NoteGPT transcript by removing timestamps and extracting text

USAGE:
1. Edit the input_path and output_path variables at the bottom of this script
2. Run: python clean_transcript.py
3. Find your cleaned files in the same directory as the output path

OUTPUT FILES:
- cleaned_transcript.txt: Pure text without timestamps
- cleaned_transcript_structured.txt: Text with timestamps preserved [HH:MM:SS]
"""

import re
from pathlib import Path
import sys

def clean_transcript(input_file, output_file):
    """
    Clean transcript by removing timestamps and preparing text for analysis
    
    Args:
        input_file: Path to input transcript file
        output_file: Path to save cleaned text
    """
    # Check if input file exists
    if not Path(input_file).exists():
        print(f"❌ Error: Input file not found: {input_file}")
        sys.exit(1)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)
    
    # Split by double newlines to get segments
    segments = content.split('\n\n')
    
    cleaned_segments = []
    all_text = []
    
    for segment in segments:
        if segment.strip():
            lines = segment.strip().split('\n')
            
            # Check if first line is a timestamp (format: HH:MM:SS)
            if lines and re.match(r'^\d{2}:\d{2}:\d{2}', lines[0]):
                timestamp = lines[0].strip()
                # Get text (everything after timestamp)
                text = ' '.join(lines[1:]).strip()
                
                if text:  # Only add if there's actual text
                    cleaned_segments.append({
                        'timestamp': timestamp,
                        'text': text
                    })
                    all_text.append(text)
    
    try:
        # Create output directory if it doesn't exist
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Save cleaned text (without timestamps) to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(all_text))
        
        # Also save structured version with timestamps
        structured_file = str(output_file).replace('.txt', '_structured.txt')
        with open(structured_file, 'w', encoding='utf-8') as f:
            for seg in cleaned_segments:
                f.write(f"[{seg['timestamp']}]\n{seg['text']}\n\n")
    except Exception as e:
        print(f"❌ Error writing output files: {e}")
        sys.exit(1)
    
    print(f"✓ Cleaned transcript saved to: {output_file}")
    print(f"✓ Structured version saved to: {structured_file}")
    print(f"\nStatistics:")
    print(f"  - Total segments: {len(cleaned_segments)}")
    print(f"  - Total characters: {sum(len(s['text']) for s in cleaned_segments):,}")
    print(f"  - Total words: {sum(len(s['text'].split()) for s in cleaned_segments):,}")
    
    # Show first few segments as preview
    print(f"\nPreview (first 3 segments):")
    for i, seg in enumerate(cleaned_segments[:3], 1):
        preview = seg['text'][:100] + "..." if len(seg['text']) > 100 else seg['text']
        print(f"\n{i}. [{seg['timestamp']}]")
        print(f"   {preview}")
    
    return cleaned_segments

if __name__ == "__main__":
    # Input and output paths
    # ==========================================
    # CHANGE THESE PATHS TO MATCH YOUR SYSTEM
    # ==========================================
    
    input_path = r"\\system-files\G\Bashqort\turkic_classification_results_bashkir.txt"
    output_path = r"\\system-files\G\Bashqort\turkic_classification_results_bashkir_cleaned.txt"
    
    # Alternatively, you can use the same directory as the input file:
    # from pathlib import Path
    # input_path = Path(r"\\system-files\G\Bashqort\NoteGPT_TRANSCRIPT_1765955787194.txt")
    # output_path = input_path.parent / "cleaned_transcript.txt"
    
    print("Cleaning transcript...")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}\n")
    
    segments = clean_transcript(input_path, output_path)
    
    print("\n✓ Done! The cleaned text is ready for analysis.")
