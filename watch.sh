#!/bin/bash
# Watch script - Auto-recompile paper when .tex file changes
# Usage: ./watch.sh

echo "=================================================="
echo "Displacement Functional - Watch Mode"
echo "=================================================="
echo ""
echo "Watching: displacement_functional_improved.tex"
echo "Press Ctrl+C to stop"
echo ""

TEX_FILE="displacement_functional_improved.tex"
LAST_MODIFIED=0

# Check if file exists
if [ ! -f "$TEX_FILE" ]; then
    echo "Error: $TEX_FILE not found"
    exit 1
fi

# Check if pdflatex is available
if ! command -v pdflatex &> /dev/null; then
    echo "Error: pdflatex not found"
    echo "Install LaTeX first"
    exit 1
fi

# Initial compilation
echo "Initial compilation..."
make paper
echo ""
echo "✓ Ready. Watching for changes..."
echo ""

# Watch loop
while true; do
    if [ -f "$TEX_FILE" ]; then
        # Get current modification time
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            CURRENT_MODIFIED=$(stat -f %m "$TEX_FILE")
        else
            # Linux
            CURRENT_MODIFIED=$(stat -c %Y "$TEX_FILE")
        fi
        
        # Check if file was modified
        if [ "$CURRENT_MODIFIED" != "$LAST_MODIFIED" ] && [ "$LAST_MODIFIED" != "0" ]; then
            echo "[$(date +%H:%M:%S)] Change detected. Recompiling..."
            
            # Recompile
            if make paper > /tmp/latex_output.log 2>&1; then
                echo "[$(date +%H:%M:%S)] ✓ Compilation successful"
                
                # Open PDF (macOS only, silent)
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    open displacement_functional_improved.pdf 2>/dev/null || true
                fi
            else
                echo "[$(date +%H:%M:%S)] ✗ Compilation failed"
                echo "Check /tmp/latex_output.log for details"
            fi
            echo ""
        fi
        
        LAST_MODIFIED=$CURRENT_MODIFIED
    fi
    
    sleep 2
done
