import re
import os

input_path = r"\\system-files\G\Bashqort\turkic_classification_results_kazakh.txt"
output_path = r"\\system-files\G\Bashqort\kazakh_clean_cyrillic.txt"

def is_meaningful_kazakh(text):
    if not text.strip():
        return False
    # Kazakh Cyrillic: includes ә, ғ, қ, ң, ө, ұ, ү, һ, і
    kazakh_pattern = re.compile(r'[а-яА-ЯәғқңөұүһіӘҒҚҢӨҰҮҺІ]+')
    matches = kazakh_pattern.findall(text)
    total_cyrillic = sum(len(word) for word in matches)
    return total_cyrillic >= 3

def clean_kazakh_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned = []
    for line in lines:
        if "Sample" in line and "=" in line:
            continue
        if is_meaningful_kazakh(line):
            cleaned.append(line.strip())

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(cleaned))

if __name__ == "__main__":
    clean_kazakh_file(input_path, output_path)
    print(f"✅ Cleaned Kazakh Cyrillic text saved to:\n{output_path}")