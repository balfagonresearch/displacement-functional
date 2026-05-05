#!/bin/bash
# Deep clean script - Remove ALL generated files and caches
# Use with caution!

echo "=================================================="
echo "Displacement Functional - Deep Clean"
echo "=================================================="
echo ""
echo "This will remove:"
echo "  • All generated PDFs (paper and figures)"
echo "  • All LaTeX auxiliary files"
echo "  • Python cache and bytecode"
echo "  • Test caches"
echo "  • Benchmarks"
echo "  • Virtual environment (if requested)"
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "Cleaning..."

# LaTeX files
echo "  • LaTeX auxiliary files..."
rm -f *.aux *.bbl *.blg *.fdb_latexmk *.fls *.log *.out *.toc *.synctex.gz
rm -f displacement_functional_improved.aux
rm -f displacement_functional_improved.bbl
rm -f displacement_functional_improved.blg
rm -f displacement_functional_improved.log
rm -f displacement_functional_improved.out

# Generated PDFs
echo "  • Generated PDFs..."
rm -f fig1_entropy.pdf fig2_lambda.pdf fig3_ion_trap.pdf
# Keep source .tex but ask about final PDF
if [ -f "displacement_functional_improved.pdf" ]; then
    read -p "  Remove paper PDF (displacement_functional_improved.pdf)? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -f displacement_functional_improved.pdf
        echo "    ✓ Removed paper PDF"
    else
        echo "    → Kept paper PDF"
    fi
fi

# Python cache
echo "  • Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
rm -rf .pytest_cache
rm -rf .coverage
rm -rf htmlcov
rm -rf *.egg-info
rm -rf dist
rm -rf build

# Test artifacts
echo "  • Test artifacts..."
rm -f test_latex.* 2>/dev/null || true

# Benchmarks
if [ -d "benchmarks" ]; then
    read -p "  Remove benchmarks directory? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf benchmarks
        echo "    ✓ Removed benchmarks"
    else
        echo "    → Kept benchmarks"
    fi
fi

# macOS specific
echo "  • macOS files..."
find . -name ".DS_Store" -delete 2>/dev/null || true

# Virtual environment
if [ -d "venv" ]; then
    echo ""
    read -p "  Remove virtual environment (venv/)? This will require re-running setup.sh (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        echo "    ✓ Removed virtual environment"
        echo "    → You'll need to run ./setup.sh again"
    else
        echo "    → Kept virtual environment"
    fi
fi

# Generated scripts (optional)
if [ -f "activate.sh" ]; then
    echo ""
    read -p "  Remove generated convenience scripts (activate.sh, etc.)? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -f activate.sh compile_paper.sh run_all.sh
        echo "    ✓ Removed convenience scripts"
        echo "    → These will be recreated by setup.sh"
    else
        echo "    → Kept convenience scripts"
    fi
fi

echo ""
echo "=================================================="
echo "Clean complete!"
echo "=================================================="
echo ""

# Show what remains
remaining_size=$(du -sh . 2>/dev/null | cut -f1)
echo "Repository size: $remaining_size"
echo ""

# Suggest next step
if [ ! -d "venv" ]; then
    echo "Next step: ./setup.sh (to recreate virtual environment)"
else
    echo "Next step: ./run_all.sh (to regenerate outputs)"
fi
echo ""
