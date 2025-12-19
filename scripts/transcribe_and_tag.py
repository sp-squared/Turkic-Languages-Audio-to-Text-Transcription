# New transcribe_and_tag.py (using openai/whisper)
import sys
import os
from pathlib import Path
import whisper
import joblib

def main():
    if len(sys.argv) != 2:
        print("Usage: python transcribe_and_tag.py <audio.mp3>")
        sys.exit(1)

    audio_path = Path(sys.argv[1])
    output_path = audio_path.with_name(audio_path.stem + "_labeled.txt")

    print("📦 Loading Whisper large-v3 (CPU)...")
    model = whisper.load_model("large-v3")  # runs on CPU by default

    print("🧠 Loading language ID model...")
    langid = joblib.load("training_data/langid_sklearn_model.pkl")

    print("🎤 Transcribing...")
    result = model.transcribe(str(audio_path), verbose=False)

    with open(output_path, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            text = segment["text"].strip()
            if not text:
                continue
            lang = langid.predict([text])[0]
            f.write(f"[{segment['start']:.1f}s-{segment['end']:.1f}s] {lang} | {text}\n")

    print(f"✅ Done! Output: {output_path}")

if __name__ == "__main__":
    main()