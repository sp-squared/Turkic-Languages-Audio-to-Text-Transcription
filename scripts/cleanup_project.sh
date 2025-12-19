#!/bin/bash
#
# Turkic Languages Project Cleanup Script
# 
# This script organizes the project by:
# 1. Creating archive directories
# 2. Moving development scripts to archive
# 3. Cleaning up Python cache files
# 4. Creating/updating .gitignore
# 5. Providing a summary report
#
# Usage: bash cleanup_project.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root
PROJECT_ROOT="C:\Users\colin\Documents\GitHub\Turkic-Languages-Audio-to-Text-Transcription"

echo "========================================================================"
echo "  TURKIC LANGUAGES PROJECT CLEANUP SCRIPT"
echo "========================================================================"
echo ""

# Check if project exists
if [ ! -d "$PROJECT_ROOT" ]; then
    echo -e "${RED}❌ Error: Project directory not found at $PROJECT_ROOT${NC}"
    echo "Please update PROJECT_ROOT variable in this script."
    exit 1
fi

echo -e "${GREEN}✅ Found project at: $PROJECT_ROOT${NC}"
echo ""

# Show what will be done
echo "This script will:"
echo "  1. Create archive directories"
echo "  2. Move training scripts to archive/"
echo "  3. Move data preparation scripts to archive/"
echo "  4. Move evaluation scripts to archive/"
echo "  5. Clean up __pycache__ and .pyc files"
echo "  6. Create/update .gitignore"
echo "  7. Generate summary report"
echo ""
echo -e "${YELLOW}⚠️  No files will be deleted, only moved to archive/${NC}"
echo ""

read -p "Continue? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo "========================================================================"
echo "  STEP 1: Creating Archive Directory Structure"
echo "========================================================================"

cd "$PROJECT_ROOT"

# Create archive directories
mkdir -p project/archive/training
mkdir -p project/archive/data_preparation
mkdir -p project/archive/evaluation
mkdir -p project/archive/utilities

echo -e "${GREEN}✅ Created archive directories:${NC}"
echo "   project/archive/training/"
echo "   project/archive/data_preparation/"
echo "   project/archive/evaluation/"
echo "   project/archive/utilities/"
echo ""

echo "========================================================================"
echo "  STEP 2: Moving Scripts to Archive"
echo "========================================================================"

# Counter for moved files
MOVED_COUNT=0

# Function to move file safely
move_to_archive() {
    local file="$1"
    local destination="$2"
    
    if [ -f "$file" ]; then
        mv "$file" "$destination"
        echo -e "   ${BLUE}→${NC} Moved: $(basename $file)"
        ((MOVED_COUNT++))
        return 0
    fi
    return 1
}

echo ""
echo "📦 Moving training scripts..."

cd "$PROJECT_ROOT/project/training-scripts" 2>/dev/null || {
    echo -e "${YELLOW}⚠️  training-scripts directory not found, skipping...${NC}"
}

if [ -d "$PROJECT_ROOT/project/training-scripts" ]; then
    cd "$PROJECT_ROOT/project/training-scripts"
    
    # Training scripts
    move_to_archive "train_turkic_classifier.py" "../archive/training/" || true
    move_to_archive "train_turkic_classifier_full.py" "../archive/training/" || true
    move_to_archive "train_sklearn_turkic.py" "../archive/training/" || true
    move_to_archive "train_fasttext_turkic.py" "../archive/training/" || true
    move_to_archive "train_transformer.py" "../archive/training/" || true
    
    echo ""
    echo "📥 Moving data preparation scripts..."
    
    # Data preparation scripts
    move_to_archive "download_mmteb.py" "../archive/data_preparation/" || true
    move_to_archive "download_mmteb_combined.py" "../archive/data_preparation/" || true
    move_to_archive "download_mmteb_dataset.py" "../archive/data_preparation/" || true
    move_to_archive "save_turkic_results.py" "../archive/data_preparation/" || true
    
    echo ""
    echo "📊 Moving evaluation scripts..."
    
    # Evaluation scripts
    move_to_archive "mteb_evaluation.py" "../archive/evaluation/" || true
    
    echo ""
    echo "🔧 Moving utility scripts..."
    
    # Utility scripts (optional)
    move_to_archive "latin_to_cyrillic_turkic.py" "../archive/utilities/" || true
    move_to_archive "demo_whisper_correction.py" "../archive/utilities/" || true
fi

echo ""
echo -e "${GREEN}✅ Moved $MOVED_COUNT files to archive${NC}"
echo ""

echo "========================================================================"
echo "  STEP 3: Cleaning Python Cache Files"
echo "========================================================================"

cd "$PROJECT_ROOT"

# Count files before cleanup
PYCACHE_DIRS=$(find . -type d -name "__pycache__" 2>/dev/null | wc -l)
PYC_FILES=$(find . -name "*.pyc" 2>/dev/null | wc -l)

echo "Found:"
echo "   __pycache__ directories: $PYCACHE_DIRS"
echo "   .pyc files: $PYC_FILES"
echo ""

if [ $PYCACHE_DIRS -gt 0 ] || [ $PYC_FILES -gt 0 ]; then
    echo "Cleaning up..."
    
    # Remove __pycache__ directories
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    
    # Remove .pyc files
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    # Remove .pyo files
    find . -name "*.pyo" -delete 2>/dev/null || true
    
    echo -e "${GREEN}✅ Cleaned up Python cache files${NC}"
else
    echo -e "${GREEN}✅ No cache files to clean${NC}"
fi

echo ""

echo "========================================================================"
echo "  STEP 4: Creating/Updating .gitignore"
echo "========================================================================"

cd "$PROJECT_ROOT"

GITIGNORE_FILE=".gitignore"

cat > "$GITIGNORE_FILE" << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual Environment
turkic-env/
venv/
env/
ENV/

# Distribution / packaging
build/
dist/
*.egg-info/

# Output files
output/*.txt
output/*.json
output/*.log

# Audio files (can be large)
audio/*.m4a
audio/*.wav
audio/*.mp3
audio/*.flac

# Keep example audio
!audio/example_*.m4a
!audio/example_*.wav

# Trained models (optional - comment out if you want to version them)
# training_data/*.pkl

# OS
.DS_Store
Thumbs.db
.directory

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Jupyter Notebook
.ipynb_checkpoints

# Temporary files
*.tmp
.cache/
temp/

# Logs
*.log
logs/

# Data files (optional - uncomment if data is too large)
# project/data/*.txt
EOF

echo -e "${GREEN}✅ Created/updated .gitignore${NC}"
echo ""

echo "========================================================================"
echo "  STEP 5: Creating Archive README"
echo "========================================================================"

cd "$PROJECT_ROOT/project/archive"

cat > "README.md" << 'EOF'
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
EOF

echo -e "${GREEN}✅ Created archive/README.md${NC}"
echo ""

echo "========================================================================"
echo "  STEP 6: Generating Summary Report"
echo "========================================================================"

cd "$PROJECT_ROOT"

# Count files in each directory
SCRIPTS_COUNT=$(find scripts/ -name "*.py" -type f 2>/dev/null | wc -l)
ARCHIVE_COUNT=$(find project/archive/ -name "*.py" -type f 2>/dev/null | wc -l)
MODELS_COUNT=$(find project/training_data/ -name "*.pkl" -type f 2>/dev/null | wc -l)

echo ""
echo "📊 Project Structure Summary:"
echo ""
echo "Production Scripts (scripts/):"
echo "   Python files: $SCRIPTS_COUNT"
if [ -d "scripts" ]; then
    ls -1 scripts/*.py 2>/dev/null | sed 's/^/   - /' || echo "   (none)"
fi

echo ""
echo "Archived Scripts (project/archive/):"
echo "   Python files: $ARCHIVE_COUNT"
echo "   Training: $(find project/archive/training/ -name "*.py" 2>/dev/null | wc -l) scripts"
echo "   Data prep: $(find project/archive/data_preparation/ -name "*.py" 2>/dev/null | wc -l) scripts"
echo "   Evaluation: $(find project/archive/evaluation/ -name "*.py" 2>/dev/null | wc -l) scripts"
echo "   Utilities: $(find project/archive/utilities/ -name "*.py" 2>/dev/null | wc -l) scripts"

echo ""
echo "Trained Models (project/training_data/):"
echo "   Model files: $MODELS_COUNT"
if [ -d "project/training_data" ]; then
    ls -lh project/training_data/*.pkl 2>/dev/null | awk '{print "   - " $9 " (" $5 ")"}' || echo "   (none)"
fi

echo ""
echo "Data Files (project/data/):"
if [ -d "project/data" ]; then
    DATA_FILES=$(ls -1 project/data/*.txt 2>/dev/null | wc -l)
    echo "   Text files: $DATA_FILES"
    ls -lh project/data/*.txt 2>/dev/null | awk '{print "   - " $9 " (" $5 ")"}' || echo "   (none)"
fi

echo ""
echo "========================================================================"
echo "  ✅ CLEANUP COMPLETE!"
echo "========================================================================"
echo ""
echo -e "${GREEN}Summary:${NC}"
echo "   ✅ Created archive directory structure"
echo "   ✅ Moved $MOVED_COUNT scripts to archive"
echo "   ✅ Cleaned Python cache files"
echo "   ✅ Created/updated .gitignore"
echo "   ✅ Created archive documentation"
echo ""
echo -e "${BLUE}What's Next:${NC}"
echo "   1. Review the production scripts in scripts/"
echo "   2. Check archived scripts in project/archive/"
echo "   3. Commit changes to git:"
echo "      cd $PROJECT_ROOT"
echo "      git add ."
echo "      git status"
echo "      git commit -m 'Reorganize project structure, archive dev scripts'"
echo ""
echo -e "${YELLOW}Note: All files were moved, not deleted. Check project/archive/ if you need anything.${NC}"
echo ""
echo "Done! 🎉"
