#!/bin/bash
# Update script - Pull latest changes and update environment
# Usage: ./update.sh

set -e

echo "=================================================="
echo "Displacement Functional - Update Script"
echo "=================================================="
echo ""

# Check if git is available
if command -v git &> /dev/null && [ -d ".git" ]; then
    echo "Step 1: Pulling latest changes from git..."
    echo "-------------------------------------------"
    
    # Stash local changes
    if ! git diff-index --quiet HEAD --; then
        echo "Stashing local changes..."
        git stash
        STASHED=true
    else
        STASHED=false
    fi
    
    # Pull
    git pull
    
    # Restore stash
    if [ "$STASHED" = true ]; then
        echo "Restoring local changes..."
        git stash pop
    fi
    
    echo "✓ Git update complete"
else
    echo "Step 1: No git repository found (skipping)"
fi

echo ""
echo "Step 2: Updating Python dependencies..."
echo "----------------------------------------"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    
    # Update pip
    echo "Updating pip..."
    pip install --upgrade pip -q
    
    # Update packages
    echo "Updating packages..."
    pip install --upgrade -r requirements.txt -q
    
    echo "✓ Dependencies updated"
else
    echo "⚠ Virtual environment not found"
    echo "Run ./setup.sh first"
    exit 1
fi

echo ""
echo "Step 3: Running tests..."
echo "------------------------"

if make quick-test 2>/dev/null; then
    echo "✓ Tests passed"
else
    echo "⚠ Some tests failed"
    echo "Run 'make test' for details"
fi

echo ""
echo "Step 4: Checking for breaking changes..."
echo "-----------------------------------------"

# Check if main files are present
if [ -f "displacement_functional.py" ] && \
   [ -f "generate_figures.py" ] && \
   [ -f "displacement_functional_improved.tex" ]; then
    echo "✓ All main files present"
else
    echo "⚠ Some main files missing - check repository"
fi

echo ""
echo "=================================================="
echo "Update Summary"
echo "=================================================="
echo ""

# Show versions
echo "Current versions:"
echo "  Python:     $(python3 --version | cut -d' ' -f2)"
echo "  NumPy:      $(python3 -c 'import numpy; print(numpy.__version__)')"
echo "  SciPy:      $(python3 -c 'import scipy; print(scipy.__version__)')"
echo "  Matplotlib: $(python3 -c 'import matplotlib; print(matplotlib.__version__)')"

if command -v pdflatex &> /dev/null; then
    echo "  LaTeX:      $(pdflatex --version | head -n1 | cut -d' ' -f2)"
fi

echo ""
echo "✓ Update complete!"
echo ""
echo "Next steps:"
echo "  • Rebuild everything: ./run_all.sh"
echo "  • Run full tests:     make test"
echo "  • Check changes:      git log (if using git)"
echo ""
