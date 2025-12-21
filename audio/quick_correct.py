#!/usr/bin/env python3
"""
Quick Text Corrector - Batch or single-file mode
Cleans timestamp artifacts, applies Kazakh→Bashkir correction, outputs single-line text.

USAGE:
    # Single file
    python quick_correct.py input.txt

    # Entire directory (processes all .txt files)
    python quick_correct.py ./my_transcripts/
"""

import sys
import re
from pathlib import Path
from kazakh_to_bashkir_corrector import correct_orthography

def clean_transcription_artifacts(text: str) -> str:
    """Remove timestamp/pipe artifacts from transcribed text."""
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Extract text after last '|' if present
        if '|' in line:
            line = line.split('|', 1)[-1].strip()

        if not line:
            continue

        # Skip lines that are only numbers, commas, brackets, etc.
        if re.fullmatch(r'[\d\s,\.\-\(\)\[\]\:]+', line):
            continue

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


def process_file(input_file: Path):
    """Process a single .txt file."""
    print(f"\n📁 Processing: {input_file.name}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        original_text = f.read()

    cleaned_text = clean_transcription_artifacts(original_text)
    corrected_text = correct_orthography(cleaned_text)
    single_line = re.sub(r'\s+', ' ', corrected_text).strip()

    output_file = input_file.parent / f"{input_file.stem}_CORRECTED_ONELINE{input_file.suffix}"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(single_line)

    print(f"✅ Saved: {output_file.name}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python quick_correct.py <file.txt OR directory>")
        print("\nExamples:")
        print("  python quick_correct.py transcript.txt")
        print("  python quick_correct.py ./transcripts/")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"❌ Path not found: {input_path}")
        sys.exit(1)

    if input_path.is_file():
        if input_path.suffix.lower() == '.txt':
            process_file(input_path)
        else:
            print("❌ Input file must be a .txt file")
            sys.exit(1)

    elif input_path.is_dir():
        txt_files = list(input_path.glob("*.txt"))
        if not txt_files:
            print(f"⚠️ No .txt files found in: {input_path}")
            sys.exit(0)

        print(f"📬 Found {len(txt_files)} .txt file(s) in: {input_path}")
        for txt_file in sorted(txt_files):
            try:
                process_file(txt_file)
            except Exception as e:
                print(f"❌ Error processing {txt_file.name}: {e}")

        print(f"\n🎉 All done! Processed {len(txt_files)} file(s).")

    else:
        print("❌ Input must be a .txt file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()