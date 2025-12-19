#!/bin/bash
#
# Rollback Script - Restore Archived Files
#
# This script restores files from archive back to training-scripts/
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
echo "  ROLLBACK CLEANUP - RESTORE ARCHIVED FILES (v2)"
echo "========================================================================"
echo ""

cd "$PROJECT_ROOT"

if [ ! -d "project/archive" ]; then
    echo -e "${RED}❌ No archive directory found at: $PROJECT_ROOT/project/archive${NC}"
    exit 1
fi

echo "📂 Found archive directory"
echo ""

# Count files in archive
total_files=$(find project/archive -name "*.py" -type f 2>/dev/null | wc -l)

echo "📊 Archive contents:"
echo "   Total Python files: $total_files"
echo ""

if [ $total_files -eq 0 ]; then
    echo -e "${RED}❌ No Python files found in archive!${NC}"
    echo "Nothing to restore."
    exit 1
fi

# Show what we found
echo "Files to restore:"
find project/archive -name "*.py" -type f 2>/dev/null | while read file; do
    echo "   - $(basename "$file") (from $(dirname "$file" | sed 's|.*/||'))"
done

echo ""
echo -e "${YELLOW}This will copy all $total_files files to project/training-scripts/${NC}"
echo ""

read -p "Continue? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Rollback cancelled."
    exit 0
fi

echo ""
echo "========================================================================"
echo "  Restoring Files"
echo "========================================================================"
echo ""

# Ensure target directory exists
mkdir -p project/training-scripts
echo "✅ Ensured project/training-scripts/ exists"
echo ""

RESTORED=0
FAILED=0

# Restore all Python files from archive
find project/archive -name "*.py" -type f 2>/dev/null | while read source_file; do
    filename=$(basename "$source_file")
    target="project/training-scripts/$filename"
    
    if [ -f "$target" ]; then
        echo -e "   ${YELLOW}⚠️${NC}  Skipping (already exists): $filename"
    else
        if cp "$source_file" "$target"; then
            echo -e "   ${GREEN}✅${NC} Restored: $filename"
            ((RESTORED++)) 2>/dev/null || RESTORED=1
        else
            echo -e "   ${RED}❌${NC} Failed: $filename"
            ((FAILED++)) 2>/dev/null || FAILED=1
        fi
    fi
done

# Count what was actually restored (since subshell variables don't persist)
actual_restored=$(find project/training-scripts -name "*.py" -type f 2>/dev/null | wc -l)

echo ""
echo "========================================================================"
echo "  Restoration Complete"
echo "========================================================================"
echo ""

echo "📊 Results:"
echo "   Files in training-scripts/: $actual_restored"
echo ""

if [ $actual_restored -gt 0 ]; then
    echo "✅ Files restored successfully!"
    echo ""
    echo "📁 Contents of project/training-scripts/:"
    ls -1 project/training-scripts/*.py 2>/dev/null | while read file; do
        echo "   - $(basename "$file")"
    done
else
    echo -e "${RED}❌ No files were restored!${NC}"
fi

echo ""
echo "Note: Archive directory still exists at project/archive/"
echo "You can delete it manually if you want:"
echo "   rm -rf project/archive/"
echo ""
