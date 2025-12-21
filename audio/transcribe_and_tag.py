# transcribe_and_tag.py (using openai/whisper)
import sys
import os
from pathlib import Path
import whisper
import joblib

def main():
    # Handle command line arguments
    if len(sys.argv) < 2:
        print("Usage: python transcribe_and_tag.py <audio_file> [language_code]")
        print("Example: python transcribe_and_tag.py speaker1_001.m4a kk")
        print("Language codes: kk (Kazakh), uz (Uzbek), tr (Turkish), ky (Kyrgyz), etc.")
        sys.exit(1)
    
    audio_path = Path(sys.argv[1])
    
    # Check if language code is provided as argument
    language_code = None
    if len(sys.argv) >= 3:
        language_code = sys.argv[2]
        print(f"🌐 Using specified language: {language_code}")
    
    output_path = audio_path.with_name(audio_path.stem + "_ba_labeled.txt")

    print("📦 Loading Whisper large-v3 (CPU)...")
    model = whisper.load_model("large-v3")  # runs on CPU by default

    print("🧠 Loading language ID model...")
    SCRIPT_DIR = Path(__file__).resolve().parent      # /audio
    PROJECT_ROOT = SCRIPT_DIR.parent                  # project root
    MODEL_PATH = PROJECT_ROOT / "project" / "training_data" / "turkic_classifier.pkl"
    langid = joblib.load(MODEL_PATH)

    print("🎤 Transcribing...")
    
    # Transcribe with language parameter if specified
    transcribe_kwargs = {
        "verbose": False,
        "fp16": False  # Important for CPU usage
    }
    
    if language_code:
        transcribe_kwargs["language"] = language_code
        print(f"🔤 Whisper will transcribe in language: {language_code}")
    else:
        print("🔤 No language specified, Whisper will auto-detect")
    
    result = model.transcribe(str(audio_path), **transcribe_kwargs)

    # Show detected language if auto-detected
    if not language_code and "language" in result:
        print(f"🔍 Whisper auto-detected language: {result['language']}")

    with open(output_path, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            text = segment["text"].strip()
            if not text:
                continue
            # Use your classifier to predict language
            lang = langid.predict([text])[0]
            f.write(f"[{segment['start']:.1f}s-{segment['end']:.1f}s] {lang} | {text}\n")

    print(f"✅ Done! Output: {output_path}")

if __name__ == "__main__":
    main()