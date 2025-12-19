#!/bin/bash
#
# Rollback Script - Restore Archived Files
#
# This script restores files from archive back to their original locations
# Use this if you need to undo the cleanup
#
# Usage: bash rollback_cleanup.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_ROOT="$HOME/Turkic-Languages-Audio-to-Text-Transcription"

echo "========================================================================"
echo "  ROLLBACK CLEANUP - RESTORE ARCHIVED FILES"
echo "========================================================================"
echo ""

cd "$PROJECT_ROOT"

if [ ! -d "project/archive" ]; then
    echo -e "${RED}❌ No archive directory found. Nothing to restore.${NC}"
    exit 1
fi

echo "This will restore all archived scripts to:"
echo "   project/training-scripts/"
echo ""
echo -e "${YELLOW}⚠️  This will NOT delete the archive directory.${NC}"
echo ""

read -p "Continue? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Rollback cancelled."
    exit 0
fi

echo ""
echo "Restoring files..."

# Ensure target directory exists
mkdir -p project/training-scripts

RESTORED=0

# Function to restore file
restore_file() {
    local source="$1"
    local target="$2"
    
    if [ -f "$source" ]; then
        cp "$source" "$target"
        echo -e "   ${GREEN}✅${NC} Restored: $(basename $source)"
        ((RESTORED++))
    fi
}

# Restore training scripts
for file in project/archive/training/*.py; do
    [ -f "$file" ] && restore_file "$file" "project/training-scripts/"
done

# Restore data preparation scripts
for file in project/archive/data_preparation/*.py; do
    [ -f "$file" ] && restore_file "$file" "project/training-scripts/"
done

# Restore evaluation scripts
for file in project/archive/evaluation/*.py; do
    [ -f "$file" ] && restore_file "$file" "project/training-scripts/"
done

# Restore utilities
for file in project/archive/utilities/*.py; do
    [ -f "$file" ] && restore_file "$file" "project/training-scripts/"
done

echo ""
echo -e "${GREEN}✅ Restored $RESTORED files to project/training-scripts/${NC}"
echo ""
echo "Note: Archive directory still exists at project/archive/"
echo "You can delete it manually if you want:"
echo "   rm -rf project/archive/"
echo ""
echo "Done!"
