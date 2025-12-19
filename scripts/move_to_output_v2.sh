#!/bin/bash
#
# Move Data Files to Output Directory (Enhanced)
#
# Features:
# - Dry-run mode to preview changes
# - Option to copy instead of move
# - Detailed file size information
# - Backup option before moving
#
# Usage:
#   bash move_to_output_v2.sh              # Move files
#   bash move_to_output_v2.sh --dry-run    # Preview only
#   bash move_to_output_v2.sh --copy       # Copy instead of move
#   bash move_to_output_v2.sh --backup     # Backup before moving

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

PROJECT_ROOT="$HOME/Turkic-Languages-Audio-to-Text-Transcription"

# Parse command line arguments
DRY_RUN=false
COPY_MODE=false
BACKUP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run|-d)
            DRY_RUN=true
            shift
            ;;
        --copy|-c)
            COPY_MODE=true
            shift
            ;;
        --backup|-b)
            BACKUP=true
            shift
            ;;
        --help|-h)
            echo "Usage: bash move_to_output_v2.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --dry-run, -d    Preview what will be moved (don't actually move)"
            echo "  --copy, -c       Copy files instead of moving"
            echo "  --backup, -b     Backup files before moving"
            echo "  --help, -h       Show this help message"
            echo ""
            echo "Examples:"
            echo "  bash move_to_output_v2.sh              # Move files"
            echo "  bash move_to_output_v2.sh --dry-run    # Preview"
            echo "  bash move_to_output_v2.sh --copy       # Copy instead"
            echo "  bash move_to_output_v2.sh --backup     # Backup first"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "========================================================================"
echo "  MOVE DATA FILES TO OUTPUT DIRECTORY"
echo "========================================================================"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${CYAN}🔍 DRY RUN MODE - No files will be moved${NC}"
    echo ""
fi

if [ "$COPY_MODE" = true ]; then
    echo -e "${BLUE}📋 COPY MODE - Files will be copied, not moved${NC}"
    echo ""
fi

if [ "$BACKUP" = true ]; then
    echo -e "${YELLOW}💾 BACKUP MODE - Creating backups before moving${NC}"
    echo ""
fi

# Check if project exists
if [ ! -d "$PROJECT_ROOT" ]; then
    echo -e "${RED}❌ Error: Project directory not found at $PROJECT_ROOT${NC}"
    exit 1
fi

cd "$PROJECT_ROOT"

# Create output directory if it doesn't exist
if [ "$DRY_RUN" = false ]; then
    mkdir -p output
fi

if [ -d "output" ]; then
    echo -e "${GREEN}✅ Output directory: $PROJECT_ROOT/output/${NC}"
else
    echo -e "${CYAN}📁 Output directory will be created: $PROJECT_ROOT/output/${NC}"
fi
echo ""

# Create backup directory if needed
if [ "$BACKUP" = true ] && [ "$DRY_RUN" = false ]; then
    BACKUP_DIR="output/backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    echo -e "${GREEN}✅ Backup directory: $BACKUP_DIR/${NC}"
    echo ""
fi

# List of files to move
FILES_TO_MOVE=(
    "turkic_bashkir_classification_results.txt"
    "turkic_kazakh_classification_results.txt"
    "turkic_kyrgyz_classification_results.txt"
    "bashkir_clean_cyrillic_base.txt"
    "bashkir_combined.txt"
    "kazakh_clean_cyrillic_base.txt"
    "kazakh_combined.txt"
    "kyrgyz_clean_cyrillic_base.txt"
    "kyrgyz_combined.txt"
)

# Counters
MOVED=0
NOT_FOUND=0
ALREADY_IN_OUTPUT=0
TOTAL_SIZE=0

echo "🔍 Searching for files..."
echo ""

# Process each file
for filename in "${FILES_TO_MOVE[@]}"; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📄 $filename"
    
    # Check if already in output/
    if [ -f "output/$filename" ]; then
        size=$(du -h "output/$filename" 2>/dev/null | cut -f1)
        echo -e "   Status: ${BLUE}Already in output/${NC}"
        echo -e "   Size: $size"
        ((ALREADY_IN_OUTPUT++))
        continue
    fi
    
    # Search for file in project (excluding output/)
    found_file=$(find . -name "$filename" -type f ! -path "./output/*" ! -path "./.git/*" 2>/dev/null | head -1)
    
    if [ -n "$found_file" ]; then
        # File found
        size=$(du -h "$found_file" 2>/dev/null | cut -f1)
        size_bytes=$(du -b "$found_file" 2>/dev/null | cut -f1)
        TOTAL_SIZE=$((TOTAL_SIZE + size_bytes))
        
        location=$(dirname "$found_file" | sed "s|^\./||")
        echo -e "   Found at: ${CYAN}$location/${NC}"
        echo -e "   Size: $size"
        
        if [ "$DRY_RUN" = true ]; then
            # Dry run - just show what would happen
            if [ "$COPY_MODE" = true ]; then
                echo -e "   ${CYAN}Would copy to: output/$filename${NC}"
            else
                echo -e "   ${CYAN}Would move to: output/$filename${NC}"
            fi
        else
            # Actually move/copy the file
            
            # Backup if requested
            if [ "$BACKUP" = true ]; then
                cp "$found_file" "$BACKUP_DIR/$filename"
                echo -e "   ${YELLOW}✅ Backed up to: $BACKUP_DIR/${NC}"
            fi
            
            # Move or copy
            if [ "$COPY_MODE" = true ]; then
                cp "$found_file" "output/$filename"
                echo -e "   ${GREEN}✅ Copied to: output/$filename${NC}"
            else
                mv "$found_file" "output/$filename"
                echo -e "   ${GREEN}✅ Moved to: output/$filename${NC}"
            fi
        fi
        
        ((MOVED++))
    else
        # File not found
        echo -e "   Status: ${YELLOW}⚠️  Not found in project${NC}"
        ((NOT_FOUND++))
    fi
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Format total size
if [ $TOTAL_SIZE -gt 0 ]; then
    if [ $TOTAL_SIZE -gt 1073741824 ]; then
        TOTAL_SIZE_FORMATTED=$(echo "scale=2; $TOTAL_SIZE / 1073741824" | bc)"G"
    elif [ $TOTAL_SIZE -gt 1048576 ]; then
        TOTAL_SIZE_FORMATTED=$(echo "scale=2; $TOTAL_SIZE / 1048576" | bc)"M"
    elif [ $TOTAL_SIZE -gt 1024 ]; then
        TOTAL_SIZE_FORMATTED=$(echo "scale=2; $TOTAL_SIZE / 1024" | bc)"K"
    else
        TOTAL_SIZE_FORMATTED="${TOTAL_SIZE}B"
    fi
fi

echo "========================================================================"
echo "  SUMMARY"
echo "========================================================================"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${CYAN}🔍 DRY RUN RESULTS:${NC}"
    echo -e "   Would process: $MOVED files"
else
    if [ "$COPY_MODE" = true ]; then
        echo -e "${GREEN}📋 COPIED: $MOVED files${NC}"
    else
        echo -e "${GREEN}✅ MOVED: $MOVED files${NC}"
    fi
fi

echo -e "${BLUE}ℹ️  Already in output: $ALREADY_IN_OUTPUT files${NC}"
echo -e "${YELLOW}⚠️  Not found: $NOT_FOUND files${NC}"

if [ $TOTAL_SIZE -gt 0 ]; then
    echo -e "${CYAN}📦 Total size: $TOTAL_SIZE_FORMATTED${NC}"
fi
echo ""

if [ "$DRY_RUN" = false ]; then
    if [ $MOVED -gt 0 ] || [ $ALREADY_IN_OUTPUT -gt 0 ]; then
        echo "📂 Contents of output/:"
        ls -lh output/*.txt 2>/dev/null | awk '{
            size = $5
            file = $9
            gsub(".*/", "", file)
            printf "   %-45s %8s\n", file, size
        }'
        echo ""
        
        total_files=$(ls output/*.txt 2>/dev/null | wc -l)
        echo -e "${GREEN}Total files in output/: $total_files${NC}"
        echo ""
    fi
fi

if [ $NOT_FOUND -gt 0 ]; then
    echo -e "${YELLOW}💡 Files not found may need to be generated first:${NC}"
    echo "   - turkic_*_classification_results.txt: Run save_turkic_results.py"
    echo "   - *_clean_cyrillic_base.txt: Check project/data/ directory"
    echo "   - *_combined.txt: Run download scripts"
    echo ""
fi

if [ "$DRY_RUN" = true ]; then
    echo -e "${CYAN}ℹ️  This was a dry run. Run without --dry-run to actually move files.${NC}"
    echo ""
fi

if [ "$BACKUP" = true ] && [ "$DRY_RUN" = false ]; then
    echo -e "${YELLOW}💾 Backup created at: $BACKUP_DIR/${NC}"
    echo ""
fi

echo "✅ Done!"
echo ""
