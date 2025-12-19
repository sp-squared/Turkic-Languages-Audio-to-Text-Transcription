#!/usr/bin/env python3
"""
Quick Text Corrector - Apply Kazakh→Bashkir corrections to any text file

USAGE:
    python quick_correct.py <input_file>
    
EXAMPLE:
    python quick_correct.py big_clip_file_original.txt
"""

import sys
from pathlib import Path
from kazakh_to_bashkir_corrector import correct_orthography

if len(sys.argv) < 2:
    print("Usage: python quick_correct.py <input_file>")
    print("\nExample:")
    print("  python quick_correct.py big_clip_file_original.txt")
    sys.exit(1)

input_file = Path(sys.argv[1])

if not input_file.exists():
    print(f"❌ File not found: {input_file}")
    sys.exit(1)

# Read input
print(f"📁 Reading: {input_file.name}")
with open(input_file, 'r', encoding='utf-8') as f:
    original_text = f.read()

print(f"📝 Original length: {len(original_text)} chars")

# Apply correction
print(f"⏳ Applying corrections...")
corrected_text = correct_orthography(original_text)

# Save output
output_file = input_file.parent / f"{input_file.stem}_CORRECTED{input_file.suffix}"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(corrected_text)

print(f"✅ Saved to: {output_file}")
print(f"📝 Corrected length: {len(corrected_text)} chars")
print(f"\n🎉 Done!")
