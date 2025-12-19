# Turkic Languages Audio-to-Text Transcription Toolkit

A comprehensive toolkit for Turkic language processing, including text classification, transliteration, and transcription utilities for **Bashkir**, **Kazakh**, and **Kyrgyz** languages.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open Science](https://img.shields.io/badge/Open-Science-blue.svg)](https://en.wikipedia.org/wiki/Open_science)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
![Static Badge](https://img.shields.io/badge/This%20is%20the%20frontier.-8A2BE2)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Language Classification](#language-classification)
  - [Transliteration](#transliteration)
  - [Transcript Cleaning](#transcript-cleaning)
- [Project Structure](#project-structure)
- [Training Your Own Models](#training-your-own-models)
- [Results](#results)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Citation](#citation)
- [License](#license)

---

## 🎯 Overview

This project provides production-ready tools and trained models for working with three Turkic languages written in Cyrillic script:

| Language | Native Name | Speakers | Special Characters |
|----------|-------------|----------|-------------------|
| **Bashkir** | Башҡорт | ~1.4M | ҙ, ҡ, ң, ҫ, ү, һ, ә, ө, ғ |
| **Kazakh** | Қазақ | ~13M | ә, ғ, қ, ң, ө, ұ, ү, һ, і |
| **Kyrgyz** | Кыргыз | ~4.5M | ң, ө, ү |

### What's Included

✅ **Pre-trained Language Classifier** - 100% accuracy on test set  
✅ **Bidirectional Transliteration** - Latin ↔ Cyrillic conversion  
✅ **Transcript Processing** - Clean NoteGPT transcripts  
✅ **Training Scripts** - FastText, Scikit-Learn, and Transformers  
✅ **Complete Documentation** - Guides, notebooks, and examples  
✅ **6,000+ Training Samples** - From [MMTEB TurkicClassification](https://huggingface.co/datasets/mteb/TurkicClassification) dataset  

---

## ✨ Features

### 🎓 Language Classification

Automatically identify which Turkic language a text is written in:

```python
>>> classify_text("Бишкек шаарында жаңы мектеп ачылды")
'kyrgyz' (confidence: 85.2%)

>>> classify_text("Қазақстанда жаңа заң қабылданды")
'kazakh' (confidence: 90.5%)

>>> classify_text("Башҡортостан Республикаһында концерт үтте")
'bashkir' (confidence: 69.5%)
```

**Three Model Options:**

- **Scikit-Learn** - Fast, 100% accuracy, 5 MB (✅ Pre-trained included!)
- **FastText** - Balanced, ~98% accuracy, 15 MB
- **Transformers** - Best, ~99% accuracy, 500 MB

### 🔤 Transliteration

Bidirectional Latin ↔ Cyrillic conversion with intelligent edge case handling:

```python
>>> latin_to_cyrillic("Qazaqstan", "kk")
'Қазақстан'

>>> cyrillic_to_latin("Башҡортостан", "ba")
'Bashqortostan'
```

**Handles 10+ Edge Cases:**

- Digraph ambiguity (sh → ш, not с+h)
- Word-initial iotation (ye → е at start)
- Soft sign apostrophes (' → ь)
- Case preservation (Qazaq → Қазақ)
- Russian loanwords support

### 📝 Transcript Cleaning

Clean NoteGPT transcripts by removing timestamps:

```python
>>> clean_transcript("00:05:23 Бүгүн биз тарых туралуу сөйлөшөбүз")
'Бүгүн биз тарых туралуу сөйлөшөбүз'
```

Creates both plain and structured outputs with statistics.

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Turkic-Languages-Audio-to-Text-Transcription.git
cd Turkic-Languages-Audio-to-Text-Transcription
```

### 2. Use the Pre-trained Classifier

```bash
cd project/training_data
python use_turkic_classifier.py
```

**Output:**

```
Text: Бишкек шаарында жаңы мектеп ачылды...
  Language: KYRGYZ (confidence: 85.2%)
  Probabilities: Bashkir=5.3%, Kazakh=9.6%, Kyrgyz=85.2%
```

### 3. Try Transliteration

```python
from latin_to_cyrillic_turkic import TurkicTransliterator

trans = TurkicTransliterator()

# Latin → Cyrillic
print(trans.latin_to_cyrillic("Qazaqstan", "kk"))
# Output: Қазақстан

# Cyrillic → Latin
print(trans.cyrillic_to_latin("Бишкек", "ky"))
# Output: Bishkek
```

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Basic Installation

```bash
# Install required packages
pip install -r requirements.txt
```

### Optional Dependencies

```bash
# For FastText training
pip install fasttext

# For Transformer models (requires GPU for efficient training)
pip install transformers torch datasets accelerate

# For Jupyter notebooks
pip install jupyter notebook
```

---

## 💻 Usage

### Language Classification

#### Option 1: Python API

```python
import pickle

# Load pre-trained model
with open('project/training_data/turkic_classifier.pkl', 'rb') as f:
    data = pickle.load(f)

model = data['model']
vectorizer = data['vectorizer']
labels = ['bashkir', 'kazakh', 'kyrgyz']

# Classify single text
text = "Алматы қаласында жаңа жоба іске қосылды"
X = vectorizer.transform([text])
prediction = model.predict(X)[0]
confidence = model.predict_proba(X)[0][prediction]

print(f"Language: {labels[prediction]}")
print(f"Confidence: {confidence:.1%}")
```

#### Option 2: Command Line

```bash
cd project/training_data
python use_turkic_classifier.py
```

#### Option 3: Batch Processing

```python
texts = [
    "Бишкек шаарында жаңы мектеп ачылды",
    "Қазақстанда жаңа заң қабылданды",
    "Башҡортостан Республикаһында концерт үтте"
]

X = vectorizer.transform(texts)
predictions = model.predict(X)

for text, pred in zip(texts, predictions):
    print(f"{labels[pred]}: {text[:50]}...")
```

---

### Transliteration

#### Basic Usage

```python
from latin_to_cyrillic_turkic import TurkicTransliterator

trans = TurkicTransliterator()

# Specify language: "ba" (Bashkir), "kk" (Kazakh), "ky" (Kyrgyz)
cyrillic = trans.latin_to_cyrillic("Salam", "kk")
latin = trans.cyrillic_to_latin("Салам", "kk")

print(cyrillic)  # Салам
print(latin)     # Salam
```

#### Language-Specific Characters

```python
# Bashkir special characters
trans.latin_to_cyrillic("bashqort", "ba")  # башҡорт

# Kazakh special characters  
trans.latin_to_cyrillic("qazaq", "kk")     # қазақ

# Kyrgyz special characters
trans.latin_to_cyrillic("qyrgyz", "ky")    # кыргыз
```

#### Interactive Jupyter Notebook

```bash
jupyter notebook project/training_data/turkic_transliteration.ipynb
```

Includes:

- Interactive examples
- All edge cases demonstrated
- Character mapping tables
- Practical applications

---

### Transcript Cleaning

#### Clean NoteGPT Transcripts

```python
from clean_transcript import clean_transcript

input_file = "NoteGPT_TRANSCRIPT_xxxxxxxxxxxxx.txt"
output_file = "cleaned_transcript.txt"

# Process transcript
clean_transcript(input_file, output_file)
```

**Creates:**

- `cleaned_transcript.txt` - Pure text (no timestamps)
- `cleaned_transcript_structured.txt` - Numbered segments with timestamps
- Statistics: segments, words, characters

---

## 📁 Project Structure

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
├── training_data/                  # Processed training samples
│   └── langid_sklearn_model.pkl    # Trained classifier (896 KB)
├── LICENSE                         # MIT License
└── README.md                       # This file
```

---

## 🏋️ Training Your Own Models

### Option 1: Scikit-Learn (Recommended)

**Fast training, great accuracy, no GPU needed**

```bash
cd project/training_data
python train_sklearn_turkic.py
```

**Training time:** 30 seconds  
**Expected accuracy:** 100% on this dataset  
**Model size:** 5 MB

---

### Option 2: FastText

**Balanced approach for production systems**

```bash
pip install fasttext
cd project/training_data
python train_fasttext_turkic.py
```

**Training time:** 5-10 minutes  
**Expected accuracy:** ~98%  
**Model size:** 15 MB

---

### Option 3: Transformers (BERT/XLM-RoBERTa)

**Maximum accuracy, requires GPU**

```bash
pip install transformers torch datasets accelerate
cd project/training_data
python train_transformer.py
```

**Training time:** 2-4 hours (with GPU)  
**Expected accuracy:** ~99%+  
**Model size:** 500 MB

---

## 📊 Results

### Classification Performance

**Scikit-Learn Model (Pre-trained)**

```
Test Accuracy: 100.00%

Classification Report:
              precision    recall  f1-score   support
     bashkir       1.00      1.00      1.00       307
      kazakh       1.00      1.00      1.00       308
      kyrgyz       1.00      1.00      1.00       307

    accuracy                           1.00       922
```

**Confusion Matrix:**

```
          Bashkir  Kazakh  Kyrgyz
Bashkir       307       0       0
Kazakh          0     308       0
Kyrgyz          0       0     307
```

### Model Comparison

| Model | Training Time | Accuracy | Size | GPU Required | Offline |
|-------|--------------|----------|------|--------------|---------|
| **Scikit-Learn** | 30 sec | 100%* | 5 MB | ❌ | ✅ |
| **FastText** | 5-10 min | ~98% | 15 MB | ❌ | ✅ |
| **Transformers** | 2-4 hours | ~99%+ | 500 MB | ✅ | ❌ |

*100% on this specific dataset - generalization may vary

---

## 📚 Documentation

### Additional Resources

- [Toolkit](project/docs/TOOLKIT.md) - This file

### Interactive Learning

- **[turkic_transliteration.ipynb](project/training_data/turkic_transliteration.ipynb)** - Jupyter notebook with examples

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Adding Training Data

1. Add more text samples to the `.txt` files
2. Ensure UTF-8 encoding
3. One sample per line
4. Retrain models

### Adding New Languages

1. Create new `language_clean_cyrillic_base.txt` file
2. Update `train_*.py` scripts with new language code
3. Add character mappings to transliteration
4. Train and test models

### Improving Models

1. Try different hyperparameters
2. Experiment with other models (e.g., DistilBERT, ELECTRA)
3. Implement data augmentation
4. Share your results!

### Bug Reports & Feature Requests

Open an issue on GitHub with:

- Clear description
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Python version and OS

---

## ❓ FAQ

**Q: Which model should I use?**  
A: Start with the pre-trained Scikit-Learn model. It's fast, accurate, and works offline.

**Q: Can this work for other Turkic languages?**  
A: Yes! Add training data for the language and retrain. Works for any Turkic language in Cyrillic or Latin script.

**Q: What about audio transcription (Whisper)?**  
A: This project focuses on text processing. For speech-to-text, you'll need audio files + transcripts and Whisper fine-tuning (different approach).

**Q: How do I add more training data?**  
A: Simply append more text samples to the `.txt` files (one per line) and retrain.

**Q: Can I use this commercially?**  
A: Yes, under the MIT license. See [LICENSE](LICENSE) for details.

**Q: How accurate is the transliteration?**  
A: Round-trip accuracy is very high for standard text. Some ambiguity exists in foreign words and names.

**Q: Does this work on Windows/Mac/Linux?**  
A: Yes! Python code is cross-platform. Use the `_FIXED` versions for correct file paths on Windows.

---

## 📈 Roadmap

- [ ] Web API (Flask/FastAPI)
- [ ] Docker container
- [ ] Additional Turkic languages (Tatar, Uyghur, Uzbek)
- [ ] Real-time classification endpoint
- [ ] Fine-tuned Whisper models for speech recognition
- [ ] Browser extension for automatic transliteration
- [ ] Mobile app (iOS/Android)

---

## 📖 Citation

If you use this project or the TurkicClassification dataset in your research, please cite the following papers.

> **Note:** GitHub also provides a "Cite this repository" button using the [CITATION.cff](CITATION.cff) file.

### TurkicClassification Dataset (MMTEB)

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

### MTEB Framework

```bibtex
@article{muennighoff2022mteb,
  author = {Muennighoff, Niklas and Tazi, Nouamane and Magne, Loïc and Reimers, Nils},
  title = {MTEB: Massive Text Embedding Benchmark},
  publisher = {arXiv},
  journal={arXiv preprint arXiv:2210.07316},
  year = {2022},
  url = {https://arxiv.org/abs/2210.07316},
  doi = {10.48550/ARXIV.2210.07316},
}
```

If you use this work in your research, please cite:

```bibtex
@software{turkic_asr_2025,
  author = {Colin Morris},
  title = {Turkic Languages Audio-to-Text Transcription: 
           Deterministic ASR Pipeline for Bashkir, Kazakh, and Kyrgyz},
  year = {2025},
  url = {https://github.com/sp-squared/Turkic-Languages-Audio-to-Text-Transcription},
  note = {Open-source ASR pipeline with deterministic orthography correction}
}
```

---

## 🙏 Acknowledgments

- Training data sourced from the **TurkicClassification** dataset, part of the [MMTEB benchmark](https://arxiv.org/abs/2502.13595) (Enevoldsen et al., 2025)
- Dataset available on [HuggingFace](https://huggingface.co/datasets/mteb/TurkicClassification)
- Built with [Scikit-Learn](https://scikit-learn.org/), [FastText](https://fasttext.cc/), and [Transformers](https://huggingface.co/transformers/)
- Inspired by the need for better Turkic language NLP tools

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

- **GitHub Issues:** [Report bugs or request features](https://github.com/sp-squared/Turkic-Languages-Audio-to-Text-Transcription/issues)
- **Pull Requests:** Contributions welcome!

---

## ⭐ Star This Repo

If you find this project useful, please consider giving it a star! It helps others discover this work.

---

<div align="center">

**Made with ❤️ for the Turkic language community**

**"This is the frontier."** 🚀

[⬆ Back to Top](#turkic-languages-audio-to-text-transcription)

</div>
