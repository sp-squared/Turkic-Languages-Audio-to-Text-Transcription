import re
import os

# Configuration
input_path = r"\\system-files\G\Bashqort\turkic_classification_results_bashkir.txt"
output_path = r"\\system-files\G\Bashqort\bashkir_clean_cyrillic.txt"

def is_meaningful_bashkir(text):
    """Return True if the line contains meaningful Bashkir Cyrillic text."""
    if not text.strip():
        return False
    # Count Cyrillic + Bashkir-specific chars
    cyrillic_pattern = re.compile(r'[а-яА-ЯҡғҫҙңөүһҺҠҒҪҢӨҮ]+')
    cyrillic_match = cyrillic_pattern.findall(text)
    # Require at least 3 Cyrillic letters total
    total_cyrillic_chars = sum(len(word) for word in cyrillic_match)
    return total_cyrillic_chars >= 3

def clean_bashkir_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned = []
    for line in lines:
        # Skip header lines with "Sample" and "="
        if "Sample" in line and "=" in line:
            continue
        # Keep only meaningful Bashkir Cyrillic lines
        if is_meaningful_bashkir(line):
            cleaned.append(line.strip())

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(cleaned))

if __name__ == "__main__":
    clean_bashkir_file(input_path, output_path)
    print(f"✅ Cleaned Bashkir Cyrillic text saved to:\n{output_path}")