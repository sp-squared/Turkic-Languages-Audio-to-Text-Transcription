# transcribe_with_vad.py
import sys
import os
from pathlib import Path
import whisper
import joblib

def format_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def main():
    if len(sys.argv) != 2:
        print("Usage: python transcribe_with_vad.py <audio.m4a>")
        sys.exit(1)

    audio_path = Path(sys.argv[1])
    output_path = audio_path.with_name(audio_path.stem + "_vad.txt")

    print("📦 Loading Whisper large-v3 (CPU)...")
    model = whisper.load_model("large-v3", device="cpu")

    print("🧠 Loading language ID model...")
    langid = joblib.load("training_data/langid_sklearn_model.pkl")

    print("🎤 Transcribing (full audio)...")
    result = model.transcribe(str(audio_path), verbose=False)

    with open(output_path, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            text = segment["text"].strip()
            # Skip very short or likely-silent segments
            if len(text) < 5:  # adjust threshold as needed
                continue
            lang = langid.predict([text])[0]
            ts = format_timestamp(segment["start"])
            f.write(f"{ts}{text}\n")
            print(f"[{ts}] ({lang}) {text[:60]}...")

    print(f"\n✅ Done! Output: {output_path}")

if __name__ == "__main__":
    main()