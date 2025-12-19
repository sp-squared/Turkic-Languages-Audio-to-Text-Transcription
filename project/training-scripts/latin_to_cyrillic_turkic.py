#!/usr/bin/env python3
"""
Latin to Cyrillic Transliteration for Turkic Languages
Supports: Bashkir (ba), Kazakh (kk), Kyrgyz (ky)

USAGE:
    from latin_to_cyrillic_turkic import latin_to_cyrillic
    
    text = "Salam, qalaysyn?"
    result = latin_to_cyrillic(text, language='kk')
    print(result)  # Салам, қалайсың?
"""

import re
from typing import Dict, Tuple


class TurkicTransliterator:
    """
    Transliterates Latin script to Cyrillic for Turkic languages
    """
    
    def __init__(self):
        # Bashkir-specific mappings (Башҡорт)
        self.bashkir_map = {
            # Special Bashkir letters
            'ҙ': 'ð', 'Ҙ': 'Ð',  # ҙ - interdental voiced fricative
            'ҡ': 'q', 'Ҡ': 'Q',  # ҡ - uvular stop
            'ң': 'ŋ', 'Ң': 'Ŋ',  # ң - velar nasal
            'ҫ': 'ś', 'Ҫ': 'Ś',  # ҫ - voiceless alveolo-palatal sibilant
            'ү': 'ü', 'Ү': 'Ü',  # ү - close front rounded
            'һ': 'h', 'Һ': 'H',  # һ - voiceless glottal fricative
            'ә': 'ä', 'Ә': 'Ä',  # ә - near-open front unrounded
            'ө': 'ö', 'Ө': 'Ö',  # ө - close-mid front rounded
            'ғ': 'ğ', 'Ғ': 'Ğ',  # ғ - voiced uvular fricative
        }
        
        # Kazakh-specific mappings (Қазақ)
        self.kazakh_map = {
            # Special Kazakh letters
            'ә': 'ä', 'Ә': 'Ä',
            'ғ': 'ğ', 'Ғ': 'Ğ',
            'қ': 'q', 'Қ': 'Q',
            'ң': 'ŋ', 'Ң': 'Ŋ',
            'ө': 'ö', 'Ө': 'Ö',
            'ұ': 'u̇', 'Ұ': 'U̇',  # ұ - close back unrounded
            'ү': 'ü', 'Ү': 'Ü',
            'һ': 'h', 'Һ': 'H',
            'і': 'i', 'І': 'I',   # і - close front unrounded (Cyrillic i)
        }
        
        # Kyrgyz-specific mappings (Кыргыз)
        self.kyrgyz_map = {
            # Special Kyrgyz letters
            'ң': 'ŋ', 'Ң': 'Ŋ',
            'ө': 'ö', 'Ө': 'Ö',
            'ү': 'ü', 'Ү': 'Ü',
        }
        
        # Common Cyrillic mappings (shared across all three)
        self.common_cyrillic = {
            # Basic Cyrillic alphabet
            'а': 'a', 'А': 'A',
            'б': 'b', 'Б': 'B',
            'в': 'v', 'В': 'V',
            'г': 'g', 'Г': 'G',
            'д': 'd', 'Д': 'D',
            'е': 'e', 'Е': 'E',
            'ё': 'yo', 'Ё': 'Yo',
            'ж': 'j', 'Ж': 'J',
            'з': 'z', 'З': 'Z',
            'и': 'i', 'И': 'I',
            'й': 'y', 'Й': 'Y',
            'к': 'k', 'К': 'K',
            'л': 'l', 'Л': 'L',
            'м': 'm', 'М': 'M',
            'н': 'n', 'Н': 'N',
            'о': 'o', 'О': 'O',
            'п': 'p', 'П': 'P',
            'р': 'r', 'Р': 'R',
            'с': 's', 'С': 'S',
            'т': 't', 'Т': 'T',
            'у': 'u', 'У': 'U',
            'ф': 'f', 'Ф': 'F',
            'х': 'x', 'Х': 'X',
            'ц': 'ts', 'Ц': 'Ts',
            'ч': 'ch', 'Ч': 'Ch',
            'ш': 'sh', 'Ш': 'Sh',
            'щ': 'shch', 'Щ': 'Shch',
            'ъ': '', 'Ъ': '',
            'ы': 'y', 'Ы': 'Y',
            'ь': '', 'Ь': '',
            'э': 'e', 'Э': 'E',
            'ю': 'yu', 'Ю': 'Yu',
            'я': 'ya', 'Я': 'Ya',
        }
    
    def _get_latin_to_cyrillic_map(self, language: str) -> Dict[str, str]:
        """
        Get the appropriate Latin to Cyrillic mapping for the language
        
        Args:
            language: 'ba' (Bashkir), 'kk' (Kazakh), or 'ky' (Kyrgyz)
        
        Returns:
            Dictionary mapping Latin characters to Cyrillic
        """
        # Combine common mappings with language-specific ones
        combined = self.common_cyrillic.copy()
        
        if language == 'ba':
            combined.update(self.bashkir_map)
        elif language == 'kk':
            combined.update(self.kazakh_map)
        elif language == 'ky':
            combined.update(self.kyrgyz_map)
        
        # Invert the mapping (Latin -> Cyrillic)
        return {v: k for k, v in combined.items()}
    
    def latin_to_cyrillic(self, text: str, language: str = 'ba') -> str:
        """
        Convert Latin script to Cyrillic for Turkic languages
        
        Args:
            text: Input text in Latin script
            language: Target language ('ba', 'kk', or 'ky')
        
        Returns:
            Text converted to Cyrillic script
        
        Examples:
            >>> transliterator = TurkicTransliterator()
            >>> transliterator.latin_to_cyrillic("Salam", "kk")
            'Салам'
        """
        if language not in ['ba', 'kk', 'ky']:
            raise ValueError(f"Unsupported language: {language}. Use 'ba', 'kk', or 'ky'")
        
        mapping = self._get_latin_to_cyrillic_map(language)
        result = []
        i = 0
        
        while i < len(text):
            # Try matching longer sequences first (3, 2, then 1 character)
            matched = False
            
            for length in [4, 3, 2, 1]:
                if i + length <= len(text):
                    substring = text[i:i+length]
                    
                    if substring in mapping:
                        result.append(mapping[substring])
                        i += length
                        matched = True
                        break
            
            if not matched:
                # Character not in mapping, keep as-is
                result.append(text[i])
                i += 1
        
        return ''.join(result)
    
    def handle_edge_cases(self, text: str, language: str = 'ba') -> str:
        """
        Handle special edge cases for transliteration
        
        Args:
            text: Input text
            language: Target language
        
        Returns:
            Text with edge cases handled
        """
        # Edge Case 1: Handle digraphs that might be ambiguous
        # Example: "sh" could be "ш" or "с" + "h"
        
        # Edge Case 2: Handle gemination (double consonants)
        # In Turkic languages, double consonants are usually written as single
        # unless at morpheme boundaries
        
        # Edge Case 3: Word-initial iotation
        # "ye" at start of word -> "е", not "ие"
        if language in ['ba', 'kk', 'ky']:
            text = re.sub(r'\bye\b', 'e', text, flags=re.IGNORECASE)
        
        # Edge Case 4: Kazakh-specific: 'i' vs 'y'
        # After vowels, 'y' often represents 'й', not 'ы'
        if language == 'kk':
            vowels = 'aeiouäöüәұі'
            text = re.sub(f'([{vowels}])y', r'\1й', text, flags=re.IGNORECASE)
        
        # Edge Case 5: Handle apostrophes (often indicate soft/hard signs)
        text = text.replace("'", 'ь')
        
        return text


# Convenience function for direct use
def latin_to_cyrillic(text: str, language: str = 'ba', handle_edges: bool = True) -> str:
    """
    Convert Latin script to Cyrillic for Bashkir, Kazakh, or Kyrgyz
    
    Args:
        text: Input text in Latin script
        language: Target language ('ba' for Bashkir, 'kk' for Kazakh, 'ky' for Kyrgyz)
        handle_edges: Whether to apply edge case handling
    
    Returns:
        Text converted to Cyrillic script
    
    Examples:
        >>> latin_to_cyrillic("Salam dünya", "ba")
        'Салам дөньа'
        
        >>> latin_to_cyrillic("Qazaqstan", "kk")
        'Қазақстан'
        
        >>> latin_to_cyrillic("Kyrgyzstan", "ky")
        'Кыргызстан'
    """
    transliterator = TurkicTransliterator()
    
    if handle_edges:
        text = transliterator.handle_edge_cases(text, language)
    
    return transliterator.latin_to_cyrillic(text, language)


def cyrillic_to_latin(text: str, language: str = 'ba') -> str:
    """
    Convert Cyrillic script to Latin for Bashkir, Kazakh, or Kyrgyz
    
    Args:
        text: Input text in Cyrillic script
        language: Source language ('ba', 'kk', or 'ky')
    
    Returns:
        Text converted to Latin script
    
    Examples:
        >>> cyrillic_to_latin("Салам дөнья", "ba")
        'Salam dönya'
    """
    transliterator = TurkicTransliterator()
    
    if language == 'ba':
        mapping = {**transliterator.common_cyrillic, **transliterator.bashkir_map}
    elif language == 'kk':
        mapping = {**transliterator.common_cyrillic, **transliterator.kazakh_map}
    elif language == 'ky':
        mapping = {**transliterator.common_cyrillic, **transliterator.kyrgyz_map}
    else:
        raise ValueError(f"Unsupported language: {language}")
    
    result = []
    i = 0
    
    while i < len(text):
        matched = False
        
        # Try matching longer sequences first
        for length in [2, 1]:
            if i + length <= len(text):
                substring = text[i:i+length]
                
                if substring in mapping:
                    result.append(mapping[substring])
                    i += length
                    matched = True
                    break
        
        if not matched:
            result.append(text[i])
            i += 1
    
    return ''.join(result)


# Test cases
if __name__ == "__main__":
    print("=" * 60)
    print("TURKIC LANGUAGE TRANSLITERATION TEST CASES")
    print("=" * 60)
    
    # Bashkir tests
    print("\n📘 BASHKIR (ba) Tests:")
    print("-" * 60)
    
    bashkir_tests = [
        ("Salam", "Greeting"),
        ("Bashqortstan", "Bashkortostan"),
        ("qorban", "sacrifice"),
        ("hälät", "condition"),
        ("öy", "house"),
        ("ðän", "grain"),
        ("yaña", "new"),
    ]
    
    for latin, meaning in bashkir_tests:
        cyrillic = latin_to_cyrillic(latin, 'ba')
        print(f"  {latin:20} → {cyrillic:20} ({meaning})")
    
    # Kazakh tests
    print("\n🇰🇿 KAZAKH (kk) Tests:")
    print("-" * 60)
    
    kazakh_tests = [
        ("Salam", "Hello"),
        ("Qazaqstan", "Kazakhstan"),
        ("qala", "city"),
        ("oqu", "to read"),
        ("jürek", "heart"),
        ("äke", "father"),
        ("bala", "child"),
    ]
    
    for latin, meaning in kazakh_tests:
        cyrillic = latin_to_cyrillic(latin, 'kk')
        print(f"  {latin:20} → {cyrillic:20} ({meaning})")
    
    # Kyrgyz tests
    print("\n🇰🇬 KYRGYZ (ky) Tests:")
    print("-" * 60)
    
    kyrgyz_tests = [
        ("Salam", "Hello"),
        ("Kyrgyzstan", "Kyrgyzstan"),
        ("bala", "child"),
        ("öy", "house"),
        ("jüröt", "walks"),
        ("köl", "lake"),
    ]
    
    for latin, meaning in kyrgyz_tests:
        cyrillic = latin_to_cyrillic(latin, 'ky')
        print(f"  {latin:20} → {cyrillic:20} ({meaning})")
    
    # Edge cases
    print("\n⚠️  EDGE CASE Tests:")
    print("-" * 60)
    
    edge_cases = [
        ("bashqort", "ba", "Bashkir people"),
        ("qazaq", "kk", "Kazakh"),
        ("shängit", "ba", "happy"),
        ("köngöl", "ky", "mood"),
        ("yaqşy", "ba", "good"),
    ]
    
    for latin, lang, meaning in edge_cases:
        cyrillic = latin_to_cyrillic(latin, lang)
        print(f"  [{lang}] {latin:20} → {cyrillic:20} ({meaning})")
    
    # Round-trip test
    print("\n🔄 ROUND-TRIP Test (Cyrillic → Latin → Cyrillic):")
    print("-" * 60)
    
    original = "Башҡортостан"
    to_latin = cyrillic_to_latin(original, 'ba')
    back_to_cyrillic = latin_to_cyrillic(to_latin, 'ba')
    
    print(f"  Original:  {original}")
    print(f"  → Latin:   {to_latin}")
    print(f"  → Cyrillic: {back_to_cyrillic}")
    print(f"  Match: {'✓' if original == back_to_cyrillic else '✗'}")
    
    print("\n" + "=" * 60)
    print("✓ All tests completed!")
    print("=" * 60)
