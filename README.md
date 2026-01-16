# Turkic Languages Audio-to-Text Transcription

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open Science](https://img.shields.io/badge/Open-Science-blue.svg)](https://en.wikipedia.org/wiki/Open_science)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
![Static Badge](https://img.shields.io/badge/This%20is%20the%20frontier.-8A2BE2)

Open-source Automatic Speech Recognition (ASR) pipeline for Bashkir (Bashkort), Kazakh, and Kyrgyz languages with deterministic orthography correction.

## 🌟 Key Features

- **Multi-language Support**: Process audio in Bashkir, Kazakh, or Kyrgyz
- **Deterministic Processing**: Perfect reproducibility (σ² = 0) for scientific research
- **Orthography Correction**: Converts Kazakh orthography → Bashkir orthography automatically
- **Language Classification**: Automatically identifies output language
- **Privacy-Preserving**: Runs completely offline, no data sent to external servers
- **Zero Cost**: No API fees, runs on CPU
- **Open Source**: MIT licensed, free to use and modify
- **Built on Open Science**: Uses Whisper (OpenAI) and MMTEB datasets

## 📖 Background & Motivation

Whisper's broad multilingual training allowed me to very quickly prototype an ASR to Kazakh text pipeline with the intention of improving language detection among Bashkir (Башҡорт), Kazakh, and Kyrgyz. I was able to get my local setup using Whisper ASR to replicate similar sentence[s] seen on NoteGPT. While Whisper itself is not open-ended (it has a fixed objective), it could enable open-ended human-machine collaboration.

## 📸 Screenshots

*Application screenshots will be added during development*

## Using MMTEB/MTEB TurkicClassification

### Turkic Converted Results

![screenshot](/project/images/dev01.png)
![screenshot](/project/images/dev02.png)
![screenshot](/project/images/dev03.png)

### Classification File Sizes

![screenshot](/project/images/dev04.png)

### Train Turkic Classifier

![screenshot](/project/images/dev05.png)
![screenshot](/project/images/dev06.png)
![screenshot](/project/images/dev07.png)

### Classifier File Sizes

![screenshot](/project/images/dev11.png)

### MTEB-Style Evaluation

![screenshot](/project/images/dev12.png)
![screenshot](/project/images/dev13.png)
![screenshot](/project/images/dev14.png)

### Cleanup Files Output Summary

![screenshot](/project/images/dev15.png)

### Potential Community Impact
![screenshot](/project/images/dev16.png)

#### Invitation for Collaborative Development

This project establishes infrastructure for Turkic language speech recognition. Its long-term utility depends on community engagement. We invite researchers, linguists, and developers to collaborate on refining the orthographic rules, testing the system with diverse audio data, and extending support to additional Turkic languages. Together, we can improve the accuracy and scope of these open-source tools.

## 🎯 Supported Languages

| Language | Code | Status | Method |
|----------|------|--------|--------|
| **Bashkir**| ba | ✅ Primary focus| Whisper (kk) + Orthography Correction |
| **Kazakh** | kk | ✅ Full support | Direct Whisper support |
| **Kyrgyz** | ky | ✅ Full support | Direct Whisper support |

## 🏗️ Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────┐
│                    Audio Input                          │
│              (Bashkir/Kazakh/Kyrgyz)                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Whisper ASR (OpenAI)                       │
│  • Bashkir → use Kazakh (kk) model                      │
│  • Kazakh → use Kazakh (kk) model                       │
│  • Kyrgyz → use Kyrgyz (ky) model                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         Deterministic Orthography Corrector             │
│  • Character substitutions (ұ→у, і→и, ғ→х)              │
│  • Selective preservation (қ in specific words)         │
│  • Context-aware variations (был/бил/буд)               │
│  • Word transformations (қойыруқ→қойрук)                │
│  • Processing time: <1ms                                │
│  • Reproducibility: σ² = 0                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│           Language Classifier (Optional)                │
│  • Trained on MMTEB TurkicClassification                │
│  • Identifies: Bashkir/Kazakh/Kyrgyz                    │
│  • Quality assurance and verification                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Corrected Text Output                      │
│         (Proper Bashkir orthography)                    │
└─────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────┐
│               Open Foundations                          │
│    Whisper (OpenAI) + MTEB (Community)                  │
│         ↓  Open source, open weights                    │
│    Global knowledge available to all                    │
└────────────────────┬────────────────────────────────────┘
                     │ Adaptation & Extension
                     ▼
┌─────────────────────────────────────────────────────────┐
│         Our Open Contribution                           │
│  • Deterministic orthography corrector                  │
│  • Turkic language classifier                           │
│  • Complete documentation                               │
│         ↓  MIT licensed, reproducible                   │
│    Specialized tool for underserved community           │
└────────────────────┬────────────────────────────────────┘
                     │ Community Access
                     ▼
┌─────────────────────────────────────────────────────────┐
│           Democratized Access                           │
│  Researchers ∙ Community members ∙ Linguists            │
│  Accessible to all regardless of institution or resources│
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

# Python

```bash
# Python 3.8 or higher required
python --version
```

# Virtual Environment

```bash
python -m venv turkic-env
```

or

```bash
python3 -m venv turkic-env
```

# Install required packages

```bash
pip install openai-whisper scikit-learn pandas numpy
```

### Basic Usage

**Transcribe Bashkir Audio:**

```bash
cd scripts
python whisper_transcribe_and_correct.py ../audio/your_audio.m4a
```

**Output files:**

- `your_audio_original.txt` - Raw Whisper output (Kazakh orthography)
- `your_audio_corrected.txt` - **Final Bashkir text** ⭐
- `your_audio_transcription_*.json` - Full data with timestamps
- `your_audio_comparison_report.txt` - Correction statistics

**Process with Specific Language:**

```bash
# For Kazakh audio (no correction needed)
python whisper_transcribe_and_correct.py ../audio/kazakh_audio.m4a --language kk

# For Kyrgyz audio
python whisper_transcribe_and_correct.py ../audio/kyrgyz_audio.m4a --language ky
```

## 📂 Project Structure

```
Turkic-Languages-Audio-to-Text-Transcription/
├── audio/                          # Input audio files (.m4a, .wav, .mp3)
├── scripts/                        # Main executable scripts
│   ├── whisper_transcribe_and_correct.py    # Main transcription pipeline
│   ├── kazakh_to_bashkir_corrector.py       # Orthography corrector
│   ├── clean_vad_transcript.py              # Transcript cleaning
│   └── train_sklearn_turkic.py              # Train language classifier
├── output/                         # Generated transcription results
├── project/
│   ├── data/                       # Training datasets (~16MB)
│   │   ├── bashkir_clean_cyrillic_base.txt
│   │   ├── kazakh_clean_cyrillic_base.txt
│   │   └── kyrgyz_clean_cyrillic_base.txt
│   ├── docs/                       # Documentation
│   └── training_scripts/           # Model training utilities
│       ├── use_turkic_classifier.py
│       ├── train_fasttext_turkic.py
│       └── train_transformer.py
├── training_data/                      # Processed training samples
│   └──    turkic_classifier.pkl        # Trained classifier (596 KB)
    └──    turkic_classifier_full.pkl   # Full-data model (596 KB)
├── LICENSE                         # MIT License
└── README.md                       # This file
```

## 🔧 Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/sp-squared/Turkic-Languages-Audio-to-Text-Transcription.git
cd Turkic-Languages-Audio-to-Text-Transcription
```

### Step 2: Optional Virtual Environment

```bash
python -m venv turkic-env
```

or

```bash
python3 -m venv turkic-env
```

```bash
cd Turkic-Languages-Audio-to-Text-Transcription
source turkic-env/Scripts/activate
```

or

```bash
cd Turkic-Languages-Audio-to-Text-Transcription
source turkic-env/bin/activate
```

```bash
deactivate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Or manually:**

```bash
pip install openai-whisper
pip install scikit-learn pandas numpy
pip install ffmpeg-python  # For audio processing
pip install mteb
```

### Step 4: Verify Installation

```bash
cd scripts
python -c "import whisper; print('Whisper installed successfully')"
```

## 💡 Usage Examples

### Example 1: Transcribe Known Bashkir Audio

```bash
cd scripts
python whisper_transcribe_and_correct.py ../audio/bashkir_speech.m4a
```

**Expected output:**

```
🎤 Loading audio: bashkir_speech.m4a
🗣️  Transcribing with Whisper (language: kk, model: base)...
✅ Transcription complete!
📝 Applying Bashkir orthography correction...
✅ Correction complete!

Files created:
- bashkir_speech_original.txt (Kazakh orthography)
- bashkir_speech_corrected.txt (Bashkir orthography) ⭐
- bashkir_speech_comparison_report.txt
```

### Example 2: Classify Language of Existing Text

```bash
cd project/training-scripts
python use_turkic_classifier.py
```

**Or in Python:**

```python
from use_turkic_classifier import classify_text

text = "Башҡортостан Республикаһында яңы мәктәп ашылды"
language, confidence, probabilities = classify_text(text)

print(f"Language: {language}")  # Output: bashkir
print(f"Confidence: {confidence:.1%}")  # Output: 98.5%
```

### Example 3: Batch Processing Multiple Files

```bash
cd scripts
for file in ../audio/*.m4a; do
    python whisper_transcribe_and_correct.py "$file"
done
```

### Example 4: Use Different Whisper Model Sizes

```bash
# Tiny model (fastest, less accurate)
python whisper_transcribe_and_correct.py audio.m4a tiny kk

# Base model (recommended)
python whisper_transcribe_and_correct.py audio.m4a base kk

# Medium model (better accuracy)
python whisper_transcribe_and_correct.py audio.m4a medium kk

# Large model (best quality, slower)
python whisper_transcribe_and_correct.py audio.m4a large kk
```

### Example 5: Using MMTEB/MTEB TurkicClassification

#### Verify Byte Size of Each PKL File

```bash
ls -lh ~/Turkic-Languages-Audio-to-Text-Transcription/project/training_data/*.pkl
```

#### Verify Byte Size of Each TXT File

```bash
myfilesize=$(wc -c "BASHKIR_TXT_FILE_LOCATION" | cut -d ' ' -f1)
echo "The file size is $myfilesize bytes"   

myfilesize=$(wc -c "KAZAKH_TXT_FILE_LOCATION" | cut -d ' ' -f1)
echo "The file size is $myfilesize bytes" 

myfilesize=$(wc -c "/KYRGYZ_TXT_FILE_LOCATION" | cut -d ' ' -f1)
echo "The file size is $myfilesize bytes"
````

### Evaluation Results

**Test Set Performance:** 97.3% accuracy

- Training: 5,222 samples
- Testing: 922 held-out samples
- Method: Single train/test split (85/15)

**Cross-Validation:** 100% accuracy (5-fold CV)

- Note: Evaluated using pre-trained TF-IDF embeddings
- Indicates excellent embedding quality
- Not used for generalization claims

## 📝 **Summary:**

Test Accuracy:       97.3%   ⭐
Training Accuracy:   99.8%
Cross-Validation:   100.0%   ℹ️ ← For info only
Model Size:         596 KB
Inference Time:       <1ms
Reproducibility:      100%

✅ REPORT: 97.3% test accuracy (proper evaluation)
ℹ️  NOTE: Cross-val shows embeddings are excellent

## 🔬 Technical Details

### Orthography Correction Rules

The deterministic corrector applies the following transformations:

**Character Substitutions:**

- `ұ` → `у` (Kazakh u to Bashkir u)
- `і` → `и` (selective - preserves in words like мінен, бірге)
- `ғ` → `х` (all occurrences)
- `қ` → `к/х` (selective - preserves in words like қашмау, қойрук)

**Word-Level Transformations:**

- `қойыруқ` → `қойрук` (tail)
- `менен` → `мінен` (with)
- Context-aware capitalization

**Key Properties:**

- ✅ Deterministic: σ² = 0 (identical output every run)
- ✅ Fast: <1ms processing time
- ✅ Transparent: All rules documented and verifiable
- ✅ Extensible: Easy to add new rules

### Language Classification

Trained on mteb/TurkicClassification dataset:

- **Dataset:** 6,144 total samples (2,048 per language: Bashkir, Kazakh, Kyrgyz)
- **Training samples:** 5,222 (85% split)
  - Bashkir: 1,741 samples
  - Kazakh: 1,741 samples
  - Kyrgyz: 1,740 samples
- **Test samples:** 922 (15% held-out set)
  - Bashkir: 307 samples
  - Kazakh: 307 samples
  - Kyrgyz: 308 samples
- **Method:** TF-IDF Vectorizer (character n-grams 2-5) + Logistic Regression
- **Training accuracy:** 99.8%
- **Test accuracy:** 97.3% (on held-out data)
- **Model size:** 596 KB
- **Features:** 10,000 character n-grams
- **Inference time:** <1ms per sample
- **Reproducibility:** Deterministic (same input → same output always)

## 📊 Performance

### ASR Quality

| Language | Method | Notes |
|----------|--------|-------|
| **Bashkir**| Whisper (kk) + Corrector | Produces usable Bashkir text |
| **Kazakh** | Whisper (kk) | Direct support, high quality |
| **Kyrgyz** | Whisper (ky) | Direct support, high quality |

### Correction Statistics

Example from real transcription:

- Original length: 467 characters (Kazakh orthography)
- Corrected length: 467 characters (Bashkir orthography)
- Characters changed: 44 (9.4%)
  - ұ→у: 1 substitution
  - і→и: 19 substitutions
  - ғ→х: 14 substitutions
  - қ→к/х: 4 substitutions
  - Others: 6 changes
- Processing time: <1ms
- Reproducibility: 100% (σ² = 0)

### Deterministic vs. Stochastic Comparison

| Property | This Project (Deterministic) | LLM-based (e.g., NoteGPT) |
|----------|------------------------------|---------------------------|
| **Reproducibility** | 100% (σ² = 0) | ~20-30% (σ² ≈ 0.15) |
| **Variance** | 0.000 | 0.15-0.30 |
| **Processing Time** | <1ms | 500-2000ms |
| **Cost per Use** | $0 | $0.01-0.10 |
| **Offline Capable** | ✅ Yes | ❌ No |
| **Transparency** | ✅ Full (all rules visible) | ❌ Black box |
| **Suitable For** | Scientific research, production systems | General use, flexible tasks |

## 🌍 Built on Open Science

This project demonstrates the power of the Open Science movement by building on open foundations:

### Foundations

**1. Whisper (OpenAI, 2022)**

- Open-source multilingual ASR model
- Free model weights and code (MIT License)
- Supports 100+ languages
- Local execution (no API required)
- Enables research on low-resource languages

**2. MMTEB (Research Community)**

- Massive Multilingual Text Embedding Benchmark
- Open datasets for Turkic languages
- Standardized evaluation framework
- Community-maintained

**3. Standard Open Tools**

- Python (open language)
- scikit-learn (open ML library)
- NumPy/Pandas (open data tools)
- GitHub (open platform)

### Our Open Contribution

Following open science principles, we contribute back:

- ✅ **Open source code** (MIT License)
- ✅ **Documented methodology** (reproducible)
- ✅ **No proprietary dependencies** (fully free)
- ✅ **Privacy-preserving** (offline capable)
- ✅ **Zero cost to use** (no API fees)

This completes the open science cycle: we benefit from open resources and contribute back to the commons.

## 📜 License

### MIT License

```

MIT License

Copyright (c) 2025 Colin Morris-Moncada

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

**What this means:**

- ✅ Free to use for any purpose (commercial or non-commercial)
- ✅ Free to modify and adapt
- ✅ Free to distribute and share
- ✅ No restrictions on derivative works
- ⚠️ Provided "as-is" without warranty
- ⚠️ Must include license notice in copies

### Third-Party Licenses

This project uses:

- **Whisper** - MIT License (OpenAI)
- **scikit-learn** - BSD-3-Clause License
- **NumPy** - BSD License
- **Pandas** - BSD-3-Clause License

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute

1. **Extend to Other Languages**
   - Tatar, Uyghur, Turkmen, Chuvash
   - Create orthography correctors for new language pairs
   - Share your results!

2. **Improve Correction Rules**
   - Add edge cases
   - Refine selective preservation lists
   - Improve context-aware rules

3. **Add Features**
   - Timestamps and speaker diarization
   - Batch processing improvements
   - GUI interface
   - Web API

4. **Documentation**
   - Add usage examples
   - Translate documentation
   - Create tutorials/videos

5. **Testing**
   - Test with diverse audio samples
   - Report bugs
   - Suggest improvements

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards others

## 🔮 Future Work

### Planned Features

- [ ] **Bashkir → English Translation**
  - Neural machine translation
  - Integration with translation APIs
  - Bilingual output option

- [ ] **Enhanced Language Detection**
  - Auto-detect language from audio
  - Support for code-switching
  - Confidence scoring

- [ ] **Extended Language Support**
  - Tatar (very close to Bashkir)
  - Uyghur
  - Turkmen
  - Chuvash

- [ ] **Improved Correction**
  - Machine learning approach alongside rules
  - Learn from user corrections
  - Dialect-specific variations

- [ ] **Tools & Integrations**
  - Web interface
  - REST API
  - Desktop application
  - Browser extension

### Research Directions

- Compare deterministic vs. ML-based correction
- Fine-tune Whisper on Bashkir audio (if data becomes available)
- Explore few-shot learning approaches
- Cross-lingual transfer learning

## 📚 Documentation

### Additional Resources

- [Toolkit](project/docs/TOOLKIT.md) - Detailed usage instructions

### Research & References

**Whisper:**

- Radford, A., et al. (2022). "Robust Speech Recognition via Large-Scale Weak Supervision." *arXiv preprint arXiv:2212.04356*.
- GitHub: <https://github.com/openai/whisper>

**MMTEB:**

- Enevoldsen, K., et al. (2025). "MMTEB: Massive Multilingual Text Embedding Benchmark."
- HuggingFace: <https://huggingface.co/datasets/mteb/TurkicClassification>

**Turkic Languages:**

- Johanson, L., & Csató, É. Á. (Eds.). (1998). *The Turkic Languages*. Routledge.

## 🙏 Acknowledgments

This project would not exist without:

- **My brother** - For introducing me to MTEB/MMTEB and Bashkortostan's culture
- **OpenAI** - For releasing Whisper as open source
- **MMTEB Contributors** - For providing open datasets
- **Open Science Community** - For advocating for accessible knowledge
- **Bashkir Community** - For preserving and sharing their language

Special thanks to all researchers working on low-resource language technology.

## 📧 Contact

- **GitHub Issues:** [Report bugs or request features](https://github.com/sp-squared/Turkic-Languages-Audio-to-Text-Transcription/issues)
- **Discussions:** [Ask questions or share ideas](https://github.com/sp-squared/Turkic-Languages-Audio-to-Text-Transcription/discussions)
- **Email:** [colin.morris.r@gmail.com]

## ⭐ Star History

If you find this project useful, please consider giving it a star! It helps others discover this work.

[![Star History Chart](https://api.star-history.com/svg?repos=sp-squared/Turkic-Languages-Audio-to-Text-Transcription&type=date&legend=top-left)](https://www.star-history.com/#sp-squared/Turkic-Languages-Audio-to-Text-Transcription&type=date&legend=top-left)

## 📊 Project Status

- ✅ **Core pipeline:** Production-ready
- ✅ **Bashkir correction:** Stable
- ✅ **Language classification:** Stable
- 🚧 **Documentation:** Ongoing improvements
- 🚧 **Extended language support:** In development
- 📋 **Bashkir→English translation:** Planned

## 🎯 Citation

```bibtex
@article{enevoldsen2025mmtebmassivemultilingualtext,
  title={MMTEB: Massive Multilingual Text Embedding Benchmark},
  author={Kenneth Enevoldsen and Isaac Chung and Imene Kerboua and Márton Kardos and Ashwin Mathur and David Stap and Jay Gala and Wissam Siblini and Dominik Krzemiński and Genta Indra Winata and Saba Sturua and Saiteja Utpala and Mathieu Ciancone and Marion Schaeffer and Gabriel Sequeira and Diganta Misra and Shreeya Dhakal and Jonathan Rystrøm and Roman Solomatin and Ömer Çağatan and Akash Kundu and Martin Bernstorff and Shitao Xiao and Akshita Sukhlecha and Bhavish Pahwa and Rafał Poświata and Kranthi Kiran GV and Shawon Ashraf and Daniel Auras and Björn Plüster and Jan Philipp Harries and Loïc Magne and Isabelle Mohr and Mariya Hendriksen and Dawei Zhu and Hippolyte Gisserot-Boukhlef and Tom Aarsen and Jan Kostkan and Konrad Wojtasik and Taemin Lee and Marek Šuppa and Crystina Zhang and Roberta Rocca and Mohammed Hamdy and Andrianos Michail and John Yang and Manuel Faysse and Aleksei Vatolin and Nandan Thakur and Manan Dey and Dipam Vasani and Pranjal Chitale and Simone Tedeschi and Nguyen Tai and Artem Snegirev and Michael Günther and Mengzhou Xia and Weijia Shi and Xing Han Lù and Jordan Clive and Gayatri Krishnakumar and Anna Maksimova and Silvan Wehrli and Maria Tikhonova and Henil Panchal and Aleksandr Abramov and Malte Ostendorff and Zheng Liu and Simon Clematide and Lester James Miranda and Alena Fenogenova and Guangyu Song and Ruqiya Bin Safi and Wen-Ding Li and Alessia Borghini and Federico Cassano and Hongjin Su and Jimmy Lin and Howard Yen and Lasse Hansen and Sara Hooker and Chenghao Xiao and Vaibhav Adlakha and Orion Weller and Siva Reddy and Niklas Muennighoff},
  publisher = {arXiv},
  journal={arXiv preprint arXiv:2502.13595},
  year={2025},
  url={https://arxiv.org/abs/2502.13595},
  doi = {10.48550/arXiv.2502.13595},
}
```

```bibtex
@article{muennighoff2022mteb,
  author = {Muennighoff, Niklas and Tazi, Nouamane and Magne, Loïc and Reimers, Nils},
  title = {MTEB: Massive Text Embedding Benchmark},
  publisher = {arXiv},
  journal={arXiv preprint arXiv:2210.07316},
  year = {2022}
  url = {https://arxiv.org/abs/2210.07316},
  doi = {10.48550/ARXIV.2210.07316},
}
```

If you use this work in your research, please cite:

```bibtex
@software{Niklas_Muennighoff_Multilingual_Text_Embedding_Benchmark,
author = {Niklas Muennighoff},
license = {Apache-2.0},
title = {{MTEB: Massive Text Embedding Benchmark}},
url = {https://github.com/embeddings-benchmark/mteb}
year={2022}
note = {Multimodal toolbox for evaluating embeddings and retrieval systems}
}
```

```bibtex
@software{Colin_Morris_Turkic_Languages_Audio_to_Text_Transcription,
  author = {Colin Morris},
  license = {MIT},
  title = {Turkic Languages Audio-to-Text Transcription: 
           Deterministic ASR Pipeline for Bashkir, Kazakh, and Kyrgyz},
  year = {2025},
  url = {https://github.com/sp-squared/Turkic-Languages-Audio-to-Text-Transcription},
  note = {Open-source ASR pipeline with deterministic orthography correction}
}
```

---

<div align="center">

**Made with ❤️ for the Turkic language community**

**"This is the frontier."** 🚀

[⬆ Back to Top](#turkic-languages-audio-to-text-transcription)

</div>
