# Archive Directory

This directory contains scripts that were used during development and training but are not needed for production use.

## Directory Structure

### `training/`
Scripts used to train the language classifier models. These were run once to create the trained `.pkl` files.

**Files:**
- `train_turkic_classifier.py` - Main training script with proper train/test split
- `train_turkic_classifier_full.py` - Training on full dataset
- `train_sklearn_turkic.py` - Earlier training approach
- `train_fasttext_turkic.py` - FastText classifier attempt
- `train_transformer.py` - Transformer-based classifier attempt

**Note:** You only need to run these if you want to retrain the models with different parameters or new data.

### `data_preparation/`
Scripts used to download and prepare the training data from HuggingFace.

**Files:**
- `download_mmteb.py` - Download MTEB dataset
- `download_mmteb_combined.py` - Download as combined files
- `download_mmteb_dataset.py` - Download with train/test split
- `save_turkic_results.py` - Process and save dataset

**Note:** Data is already downloaded and processed in `project/data/`.

### `evaluation/`
Scripts used to evaluate model performance.

**Files:**
- `mteb_evaluation.py` - MTEB-style cross-validation evaluation

**Note:** Model has already been evaluated. Results in README.md.

### `utilities/`
Helper scripts and utilities that may be useful for development.

**Files:**
- `latin_to_cyrillic_turkic.py` - Transliteration utilities
- `demo_whisper_correction.py` - Demo script for testing

## When to Use These Scripts

### Retrain the Model
If you want to retrain with new data or different parameters:
```bash
cd training/
python train_turkic_classifier.py
```

### Download Fresh Data
If you need to re-download the dataset:
```bash
cd data_preparation/
python download_mmteb_dataset.py
```

### Run Evaluation
To verify model performance:
```bash
cd evaluation/
python mteb_evaluation.py
```

## Restoring Scripts

If you need any of these scripts in the main project:
```bash
# Example: Restore training script
cp archive/training/train_turkic_classifier.py ../training-scripts/
```

## Archive Date

These scripts were archived on: $(date +%Y-%m-%d)

The project was cleaned up to maintain only production-ready code in the main directories.
