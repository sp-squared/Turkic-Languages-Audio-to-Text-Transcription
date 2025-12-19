import re
import os

input_path = r"\\system-files\G\Bashqort\turkic_classification_results_kyrgyz.txt"
output_path = r"\\system-files\G\Bashqort\kyrgyz_clean_cyrillic.txt"

def is_meaningful_kyrgyz(text):
    if not text.strip():
        return False
    # Kyrgyz Cyrillic: includes ә, ң, ө, ү, and often г/к/ч for ғ/к̌/ч̌
    kyrgyz_pattern = re.compile(r'[а-яА-ЯәңөүӘҢӨҮ]+')
    matches = kyrgyz_pattern.findall(text)
    total_cyrillic = sum(len(word) for word in matches)
    return total_cyrillic >= 3

def clean_kyrgyz_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned = []
    for line in lines:
        if "Sample" in line and "=" in line:
            continue
        if is_meaningful_kyrgyz(line):
            cleaned.append(line.strip())

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(cleaned))

if __name__ == "__main__":
    clean_kyrgyz_file(input_path, output_path)
    print(f"✅ Cleaned Kyrgyz Cyrillic text saved to:\n{output_path}")