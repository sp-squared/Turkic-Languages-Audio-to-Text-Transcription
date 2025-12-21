#!/usr/bin/env python3
"""
Kazakh to Bashkir Orthography Corrector

Transcribes audio using Whisper, then corrects Kazakh orthography to Bashkir.
Post-processes Whisper transcriptions that incorrectly use Kazakh orthography
when the audio is actually Bashkir.

USAGE:
    # Transcribe and correct audio file
    python kazakh_to_bashkir_corrector.py audio.m4a --model medium --language kk
    
    # Correct existing text file
    python kazakh_to_bashkir_corrector.py --text input.txt --output corrected.txt
    
    # Batch process directory of audio files
    python kazakh_to_bashkir_corrector.py --input-dir ./audio --model large
"""

import re
import sys
import argparse
import os
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
import unicodedata
import json


class KazakhToBashkirCorrector:
    """
    Corrects Kazakh orthographic patterns to proper Bashkir orthography
    """
    
    def __init__(self):
        # Load word lists from external files if available
        self.preserve_қ_words = self._load_word_list('preserve_q_words.txt')
        self.preserve_і_words = self._load_word_list('preserve_i_words.txt')
        self.preserve_е_words = self._load_word_list('preserve_e_words.txt')
        
        # If word lists don't exist, use defaults
        if not self.preserve_қ_words:
            self.preserve_қ_words = {
                'қашмау', 'Қашмау', 'қойрук', 'Қойрук',
                'қойылған', 'Қойылған', 'қойылхан', 'Қойылхан',
            }
        
        if not self.preserve_і_words:
            self.preserve_і_words = {
                'мінен', 'Мінен', 'бірге', 'Бірге',
                'әлікле', 'Әлікле', 'әликли', 'Әликли',
            }
        
        # Complete word mappings (Kazakh → Bashkir)
        self.word_dictionary = {
            # Pronouns and common words
            'бұл': 'был', 'Бұл': 'Был',
            'осы': 'был', 'Осы': 'Был',
            'мен': 'мин', 'Мен': 'Мин',
            'менің': 'миниң', 'Менің': 'Миниң',
            'сен': 'һин', 'Сен': 'Һин',
            'сенің': 'һинең', 'Сенің': 'Һинең',
            'ол': 'ул', 'Ол': 'Ул',
            'оның': 'уның', 'Оның': 'Уның',
            'біз': 'беҙ', 'Біз': 'Беҙ',
            'біздің': 'беҙҙең', 'Біздің': 'Беҙҙең',
            'сіз': 'һеҙ', 'Сіз': 'Һеҙ',
            'сіздің': 'һеҙҙең', 'Сіздің': 'Һеҙҙең',
            'олар': 'улар', 'Олар': 'Улар',
            'олардың': 'уларҙың', 'Олардың': 'Уларҙың',
            
            # Question words
            'немау': 'нимау', 'Немау': 'Нимау',
            'немене': 'нимә', 'Немене': 'Нимә',
            'қалай': 'ҡалай', 'Қалай': 'Ҡалай',
            'қайда': 'ҡайҙа', 'Қайда': 'Ҡайҙа',
            'қашан': 'ҡасан', 'Қашан': 'Ҡасан',
            'неге': 'ниңә', 'Неге': 'Ниңә',
            'не': 'нәмә', 'Не': 'Нәмә',
            
            # Common verbs
            'болды': 'булды', 'Болды': 'Булды',
            'болады': 'була', 'Болады': 'Була',
            'етеді': 'итә', 'Етеді': 'Итә',
            'керек': 'кәрәк', 'Керек': 'Кәрәк',
            'бар': 'бар', 'Бар': 'Бар',
            'жоқ': 'юҡ', 'Жоқ': 'Юҡ',
            'деді': 'әйтте', 'Деді': 'Әйтте',
            'деп': 'тип', 'Деп': 'Тип',
            
            # Common nouns
            'адам': 'кеше', 'Адам': 'Кеше',
            'өмір': 'ғүмер', 'Өмір': 'Ғүмер',
            'қала': 'ҡала', 'Қала': 'Ҡала',
            'ауыл': 'ауыл', 'Ауыл': 'Ауыл',
            'тіл': 'тел', 'Тіл': 'Тел',
            'сөз': 'һүҙ', 'Сөз': 'Һүҙ',
            'үй': 'өй', 'Үй': 'Өй',
            'кітап': 'китап', 'Кітап': 'Китап',
            'бала': 'бала', 'Бала': 'Бала',
            'қыз': 'ҡыҙ', 'Қыз': 'Ҡыҙ',
        }
        
        # Single character replacements
        self.char_map = {
            'ұ': 'у', 'Ұ': 'У',    # Kazakh ұ → Bashkir у
            'ү': 'ө', 'Ү': 'Ө',    # Kazakh ү → Bashkir ө
            'і': 'е', 'І': 'Е',    # Kazakh і → Bashkir е
            'ә': 'ә', 'Ә': 'Ә',    # Same in both
            'ө': 'ө', 'Ө': 'Ө',    # Same in both
            'ғ': 'ғ', 'Ғ': 'Ғ',    # Bashkir uses ғ
            'ң': 'ң', 'Ң': 'Ң',    # Nasal n
            'һ': 'һ', 'Һ': 'Һ',    # Bashkir h
        }
        
        # Grammar-specific patterns (endings)
        self.grammar_patterns = [
            # Possessive endings
            (r'ның\b', 'ның'),
            (r'нің\b', 'нең'),
            (r'дың\b', 'ҙың'),
            (r'дің\b', 'ҙең'),
            (r'тың\b', 'тың'),
            (r'тің\b', 'тең'),
            
            # Accusative case
            (r'ды\b', 'ҙы'),
            (r'ді\b', 'ҙе'),
            (r'ты\b', 'ты'),
            (r'ті\b', 'те'),
            (r'ны\b', 'ны'),
            (r'ні\b', 'не'),
            
            # Dative case
            (r'ға\b', 'ға'),
            (r'ге\b', 'гә'),
            (r'қа\b', 'ҡа'),
            (r'ке\b', 'кә'),
            
            # Locative case
            (r'да\b', 'ҙа'),
            (r'де\b', 'ҙә'),
            (r'та\b', 'та'),
            (r'те\b', 'тә'),
            
            # Ablative case
            (r'дан\b', 'ҙан'),
            (r'ден\b', 'ҙән'),
            (r'тан\b', 'тан'),
            (r'тен\b', 'тән'),
            (r'нан\b', 'нан'),
            (r'нен\b', 'нән'),
        ]
        
        # Proper noun capitalization
        self.proper_nouns = {
            'башқорт': 'Башҡорт', 'башкорт': 'Башҡорт',
            'татар': 'Татар', 'қазақ': 'Ҡазаҡ',
            'казақ': 'Ҡазаҡ', 'қырғыз': 'Ҡырғыҙ',
            'қазақстан': 'Ҡазаҡстан', 'орыс': 'Урыҫ',
            'рус': 'Урыҫ', 'өзбек': 'Үзбәк',
            'төрек': 'Төрөк', 'монғол': 'Мунғал',
        }
    
    def _load_word_list(self, filename: str) -> Set[str]:
        """Load word list from file"""
        word_list = set()
        file_path = Path(__file__).parent / 'data' / filename
        
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        word = line.strip()
                        if word:
                            word_list.add(word)
            except Exception as e:
                print(f"Warning: Could not load {filename}: {e}")
        
        return word_list
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for consistent processing"""
        # Normalize Unicode
        text = unicodedata.normalize('NFC', text)
        
        # Fix common spacing issues
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\s([,\.!?;:])', r'\1', text)
        text = re.sub(r'([,\.!?;:])([^\s])', r'\1 \2', text)
        
        # Fix common Whisper artifacts
        text = re.sub(r'\[.*?\]', '', text)  # Remove [music], [laughter] etc
        text = re.sub(r'\(.*?\)', '', text)  # Remove (background noise)
        
        return text.strip()
    
    def _apply_dictionary(self, text: str) -> str:
        """Apply word dictionary replacements"""
        words = text.split()
        result_words = []
        
        for word in words:
            original_word = word
            
            # Handle punctuation
            prefix = ''
            suffix = ''
            
            # Extract leading punctuation
            while word and not word[0].isalnum() and word[0] not in self.char_map:
                prefix += word[0]
                word = word[1:]
            
            # Extract trailing punctuation
            while word and not word[-1].isalnum() and word[-1] not in self.char_map:
                suffix = word[-1] + suffix
                word = word[:-1]
            
            # Apply dictionary if word exists
            word_lower = word.lower()
            if word_lower in self.word_dictionary:
                replacement = self.word_dictionary[word_lower]
                
                # Preserve original capitalization
                if word.istitle():
                    replacement = replacement.title()
                elif word.isupper():
                    replacement = replacement.upper()
                
                word = replacement
            
            result_words.append(prefix + word + suffix)
        
        return ' '.join(result_words)
    
    def _apply_char_replacements(self, text: str) -> str:
        """Apply single character replacements"""
        result = text
        
        # Apply character map
        for kazakh_char, bashkir_char in self.char_map.items():
            result = result.replace(kazakh_char, bashkir_char)
        
        # Handle қ conversions (context-sensitive)
        # қ at beginning or after consonant → ҡ
        result = re.sub(r'(\b|[' + re.escape('бвгджзйлмнпрстфхцчшщң') + r'])қ', r'\1ҡ', result)
        result = re.sub(r'(\b|[' + re.escape('бвгджзйлмнпрстфхцчшщң') + r'])Қ', r'\1Ҡ', result)
        
        # қ between vowels → х
        result = re.sub(r'([аәоөуүыиеэ])қ([аәоөуүыиеэ])', r'\1х\2', result)
        result = re.sub(r'([аәоөуүыиеэ])Қ([аәоөуүыиеэ])', r'\1Х\2', result)
        
        # Final қ → ҡ
        result = re.sub(r'қ\b', 'ҡ', result)
        result = re.sub(r'Қ\b', 'Ҡ', result)
        
        return result
    
    def _apply_grammar_corrections(self, text: str) -> str:
        """Apply grammar-specific corrections"""
        result = text
        
        # Apply grammar patterns
        for pattern, replacement in self.grammar_patterns:
            result = re.sub(pattern, replacement, result)
        
        # Fix vowel harmony
        result = self._fix_vowel_harmony(result)
        
        return result
    
    def _fix_vowel_harmony(self, text: str) -> str:
        """Fix vowel harmony in word endings"""
        result = text
        
        # Back vowels (а, о, у, ы) + front ending → back ending
        back_vowel_patterns = [
            (r'([аоуы])гә\b', r'\1га'),
            (r'([аоуы])кә\b', r'\1ка'),
            (r'([аоуы])ҙә\b', r'\1ҙа'),
            (r'([аоуы])тә\b', r'\1та'),
            (r'([аоуы])нән\b', r'\1нан'),
            (r'([аоуы])ҙән\b', r'\1ҙан'),
            (r'([аоуы])тән\b', r'\1тан'),
        ]
        
        # Front vowels (ә, ө, ү, и, е) + back ending → front ending
        front_vowel_patterns = [
            (r'([әөүие])га\b', r'\1гә'),
            (r'([әөүие])ка\b', r'\1кә'),
            (r'([әөүие])ҙа\b', r'\1ҙә'),
            (r'([әөүие])та\b', r'\1тә'),
            (r'([әөүие])нан\b', r'\1нән'),
            (r'([әөүие])ҙан\b', r'\1ҙән'),
            (r'([әөүие])тан\b', r'\1тән'),
        ]
        
        # Apply back vowel patterns
        for pattern, replacement in back_vowel_patterns:
            result = re.sub(pattern, replacement, result)
        
        # Apply front vowel patterns
        for pattern, replacement in front_vowel_patterns:
            result = re.sub(pattern, replacement, result)
        
        return result
    
    def _capitalize_proper_nouns(self, text: str) -> str:
        """Capitalize proper nouns"""
        result = text
        
        for word, capitalized in self.proper_nouns.items():
            # Whole word
            result = re.sub(rf'\b{word}\b', capitalized, result)
            result = re.sub(rf'\b{word.title()}\b', capitalized, result)
        
        return result
    
    def _apply_sentence_capitalization(self, text: str) -> str:
        """Apply proper sentence capitalization"""
        if not text:
            return text
        
        # Split into sentences
        sentences = re.split(r'([.!?]+\s*)', text)
        result = []
        
        for i in range(0, len(sentences), 2):
            sentence = sentences[i]
            punctuation = sentences[i + 1] if i + 1 < len(sentences) else ''
            
            if sentence:
                # Capitalize first letter
                sentence = sentence[0].upper() + sentence[1:]
            
            result.append(sentence + punctuation)
        
        return ''.join(result)
    
    def _apply_final_formatting(self, text: str) -> str:
        """Apply final formatting touches"""
        result = text
        
        # Ensure proper spacing around punctuation
        result = re.sub(r'\s*([,.:;!?])\s*', r'\1 ', result)
        result = re.sub(r'([,.:;!?])([^\s])', r'\1 \2', result)
        
        # Remove double punctuation
        result = re.sub(r'([.!?]){2,}', r'\1', result)
        
        # Remove extra spaces
        result = re.sub(r'\s+', ' ', result)
        
        return result.strip()
    
    def correct_orthography(self, text: str, aggressive: bool = False) -> str:
        """
        Correct Kazakh orthography to Bashkir
        
        Args:
            text: Input text with Kazakh orthography
            aggressive: If True, applies more aggressive corrections
            
        Returns:
            Text with corrected Bashkir orthography
        """
        if not text.strip():
            return text
        
        # Step 0: Normalize input
        result = self._normalize_text(text)
        
        # Step 1: Apply dictionary replacements (exact word matches)
        result = self._apply_dictionary(result)
        
        # Step 2: Apply character replacements
        result = self._apply_char_replacements(result)
        
        # Step 3: Apply grammar corrections
        result = self._apply_grammar_corrections(result)
        
        # Step 4: Capitalize proper nouns
        result = self._capitalize_proper_nouns(result)
        
        # Step 5: Apply sentence capitalization
        result = self._apply_sentence_capitalization(result)
        
        # Step 6: Final formatting
        result = self._apply_final_formatting(result)
        
        return result
    
    def batch_correct(self, texts: List[str], aggressive: bool = False) -> List[str]:
        """
        Correct multiple texts
        
        Args:
            texts: List of input texts
            aggressive: Whether to apply aggressive corrections
            
        Returns:
            List of corrected texts
        """
        return [self.correct_orthography(text, aggressive) for text in texts]


class WhisperTranscriber:
    """Handles Whisper transcription"""
    
    def __init__(self):
        self.whisper_available = False
        try:
            import whisper
            self.whisper = whisper
            self.whisper_available = True
        except ImportError:
            print("Warning: Whisper not installed. Install with: pip install openai-whisper")
    
    def transcribe_audio(self, audio_path: str, model_size: str = "medium", 
                        language: str = "kk") -> str:
        """
        Transcribe audio file using Whisper
        
        Args:
            audio_path: Path to audio file
            model_size: Whisper model size (tiny, base, small, medium, large)
            language: Language code (kk for Kazakh)
            
        Returns:
            Transcribed text
        """
        if not self.whisper_available:
            raise ImportError("Whisper is not installed")
        
        print(f"Loading Whisper model '{model_size}'...")
        model = self.whisper.load_model(model_size)
        
        print(f"Transcribing '{audio_path}' in language '{language}'...")
        result = model.transcribe(audio_path, language=language)
        
        return result["text"]
    
    def transcribe_directory(self, input_dir: str, output_dir: str, 
                            model_size: str = "medium", language: str = "kk"):
        """
        Transcribe all audio files in a directory
        
        Args:
            input_dir: Directory with audio files
            output_dir: Directory to save transcriptions
            model_size: Whisper model size
            language: Language code
        """
        if not self.whisper_available:
            raise ImportError("Whisper is not installed")
        
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        audio_extensions = {'.m4a', '.mp3', '.wav', '.flac', '.ogg', '.aac', '.mpeg'}
        
        audio_files = [f for f in input_path.iterdir() 
                      if f.suffix.lower() in audio_extensions]
        
        print(f"Found {len(audio_files)} audio files")
        
        for audio_file in audio_files:
            try:
                print(f"\nProcessing: {audio_file.name}")
                text = self.transcribe_audio(str(audio_file), model_size, language)
                
                # Save transcription
                output_file = output_path / f"{audio_file.stem}_transcribed.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                print(f"  Saved to: {output_file}")
                
            except Exception as e:
                print(f"  Error processing {audio_file.name}: {e}")


def process_audio_file(input_file: str, model_size: str = "medium", 
                      language: str = "kk", output_file: Optional[str] = None):
    """
    Transcribe audio and correct orthography
    
    Args:
        input_file: Path to audio file
        model_size: Whisper model size
        language: Language code
        output_file: Output file path (optional)
    """
    # Transcribe
    transcriber = WhisperTranscriber()
    
    if not transcriber.whisper_available:
        print("Error: Whisper is required for audio transcription.")
        print("Install it with: pip install openai-whisper")
        return
    
    try:
        text = transcriber.transcribe_audio(input_file, model_size, language)
        
        # Save original transcription
        input_path = Path(input_file)
        if output_file is None:
            output_dir = input_path.parent / "transcriptions"
            output_dir.mkdir(exist_ok=True)
            output_file = output_dir / f"{input_path.stem}_transcribed.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"✓ Transcription saved to: {output_file}")
        
        # Correct orthography
        corrector = KazakhToBashkirCorrector()
        corrected_text = corrector.correct_orthography(text)
        
        # Save corrected version
        corrected_file = Path(str(output_file).replace('_transcribed.txt', '_corrected.txt'))
        with open(corrected_file, 'w', encoding='utf-8') as f:
            f.write(corrected_text)
        
        print(f"✓ Corrected text saved to: {corrected_file}")
        
        # Show sample
        print("\n📝 Sample of corrected text:")
        print("-" * 70)
        lines = corrected_text.split('\n')
        for line in lines[:3]:
            if line.strip():
                print(line[:100] + "..." if len(line) > 100 else line)
        
    except Exception as e:
        print(f"Error: {e}")


def process_text_file(input_file: str, output_file: Optional[str] = None, 
                     aggressive: bool = False):
    """
    Correct orthography in text file
    
    Args:
        input_file: Path to text file
        output_file: Output file path (optional)
        aggressive: Whether to apply aggressive corrections
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        corrector = KazakhToBashkirCorrector()
        corrected_text = corrector.correct_orthography(text, aggressive)
        
        if output_file is None:
            input_path = Path(input_file)
            output_file = input_path.parent / f"{input_path.stem}_corrected.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(corrected_text)
        
        print(f"✓ Corrected text saved to: {output_file}")
        
        # Show statistics
        original_words = len(text.split())
        corrected_words = len(corrected_text.split())
        print(f"  Original: {original_words} words")
        print(f"  Corrected: {corrected_words} words")
        
        # Show sample
        print("\n📝 Sample of corrected text:")
        print("-" * 70)
        lines = corrected_text.split('\n')
        for line in lines[:3]:
            if line.strip():
                print(line[:100] + "..." if len(line) > 100 else line)
        
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Main command-line interface"""
    parser = argparse.ArgumentParser(
        description='Transcribe audio and correct Kazakh to Bashkir orthography',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Transcribe audio and correct
  python kazakh_to_bashkir_corrector.py audio.m4a --model medium --language kk
  
  # Correct existing text file
  python kazakh_to_bashkir_corrector.py --text input.txt --output corrected.txt
  
  # Batch process directory of audio files
  python kazakh_to_bashkir_corrector.py --input-dir ./audio --model large
  
  # Use aggressive correction mode
  python kazakh_to_bashkir_corrector.py --text input.txt --aggressive
        """
    )
    
    # Main input argument
    parser.add_argument('input', nargs='?', help='Input audio or text file')
    
    # Mode selection
    parser.add_argument('--text', action='store_true', 
                       help='Input is a text file (default: audio file)')
    parser.add_argument('--input-dir', help='Process all audio files in directory')
    
    # Whisper options
    parser.add_argument('--model', default='medium', 
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper model size (default: medium)')
    parser.add_argument('--language', default='kk', 
                       help='Language code for transcription (default: kk for Kazakh)')
    
    # Correction options
    parser.add_argument('--aggressive', action='store_true',
                       help='Apply aggressive corrections')
    parser.add_argument('--output', help='Output file path')
    
    # Other options
    parser.add_argument('--batch', action='store_true',
                       help='Process multiple files in batch')
    parser.add_argument('--test', action='store_true',
                       help='Run test cases')
    
    args = parser.parse_args()
    
    # Run test cases
    if args.test:
        run_test_cases()
        return
    
    # Batch process directory
    if args.input_dir:
        transcriber = WhisperTranscriber()
        if transcriber.whisper_available:
            output_dir = Path(args.input_dir) / "transcriptions"
            transcriber.transcribe_directory(args.input_dir, str(output_dir), 
                                           args.model, args.language)
            
            # Correct all transcriptions
            corrector = KazakhToBashkirCorrector()
            for txt_file in output_dir.glob("*_transcribed.txt"):
                try:
                    with open(txt_file, 'r', encoding='utf-8') as f:
                        text = f.read()
                    
                    corrected = corrector.correct_orthography(text, args.aggressive)
                    
                    corrected_file = txt_file.parent / f"{txt_file.stem.replace('_transcribed', '_corrected')}.txt"
                    with open(corrected_file, 'w', encoding='utf-8') as f:
                        f.write(corrected)
                    
                    print(f"✓ Corrected: {corrected_file.name}")
                    
                except Exception as e:
                    print(f"Error processing {txt_file.name}: {e}")
        return
    
    # Process single file
    if not args.input:
        parser.print_help()
        return
    
    input_file = args.input
    
    if args.text:
        # Process text file
        process_text_file(input_file, args.output, args.aggressive)
    else:
        # Process audio file
        process_audio_file(input_file, args.model, args.language, args.output)


def run_test_cases():
    """Run test cases"""
    print("=" * 70)
    print("TESTING KAZAKH TO BASHKIR CORRECTOR")
    print("=" * 70)
    
    test_cases = [
        {
            "input": "бұл қашмау қойыруқ менен кепке,ғамының башқорт традицион елалық сегеудәрі менен бұл қашмау қойыруқ кепкеға қойылған шул бұл менің заманлы ғам әлікле мәдіниет бірге халу. немау диджілік бұл менің ойлап сығарған яңын құд диджитал құздан, ләкен башқорт форма. бұл диджитал аңладан.",
            "expected": "Был ҡашмау ҡойыруҡ менән кепкә, ғамының Башҡорт традицион елалыҡ сегеүдәре менән был ҡашмау ҡойыруҡ кепкәгә ҡойылған шул был миниң заманлы ғәм әликли мәдәният берегә халу. Нимау диджилик был миниң уйлап сығарған яңын хүд диджитал хүзҙән, ләкин Башҡорт форма. Был диджитал аңладан."
        },
        {
            "input": "Менің атым Айдар. Мен қазақпын, бірақ башқорт тілін үйренемін. Бұл қиын ма? Жоқ, қызықты!",
            "expected": "Миниң атым Айдар. Мин ҡазаҡмын, бәраҡ Башҡорт телен өйрәнәм. Был ҡиын мы? Юҡ, ҡызыҡты!"
        }
    ]
    
    corrector = KazakhToBashkirCorrector()
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"Test Case {i}")
        print(f"{'='*70}")
        
        corrected = corrector.correct_orthography(test["input"])
        
        print("Input:")
        print(f"  {test['input'][:80]}..." if len(test['input']) > 80 else f"  {test['input']}")
        print("\nOutput:")
        print(f"  {corrected[:80]}..." if len(corrected) > 80 else f"  {corrected}")
        print("\nExpected:")
        print(f"  {test['expected'][:80]}..." if len(test['expected']) > 80 else f"  {test['expected']}")
        
        # Calculate accuracy
        input_words = test["input"].split()
        output_words = corrected.split()
        expected_words = test["expected"].split()
        
        if len(output_words) == len(expected_words):
            matches = sum(1 for o, e in zip(output_words, expected_words) if o == e)
            accuracy = matches / len(expected_words) * 100
            print(f"\nAccuracy: {accuracy:.1f}% ({matches}/{len(expected_words)} words)")
        else:
            print("\nNote: Word count mismatch between output and expected")


# Convenience functions for programmatic use
def correct_orthography(text: str, aggressive: bool = False) -> str:
    """
    Correct Kazakh orthography to Bashkir
    
    Args:
        text: Input text with Kazakh orthography
        aggressive: If True, applies more aggressive corrections
    
    Returns:
        Text with corrected Bashkir orthography
    """
    corrector = KazakhToBashkirCorrector()
    return corrector.correct_orthography(text, aggressive)


def batch_correct(texts: List[str], aggressive: bool = False) -> List[str]:
    """
    Correct multiple texts
    
    Args:
        texts: List of input texts
        aggressive: Whether to apply aggressive corrections
    
    Returns:
        List of corrected texts
    """
    corrector = KazakhToBashkirCorrector()
    return corrector.batch_correct(texts, aggressive)


if __name__ == "__main__":
    main()