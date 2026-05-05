#!/bin/bash
# Comprehensive verification script
# Checks that everything is installed and working correctly

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=================================================="
echo "Displacement Functional - System Verification"
echo "=================================================="
echo ""

ERRORS=0
WARNINGS=0

# Function to check command
check_command() {
    local cmd=$1
    local name=$2
    local required=$3
    
    if command -v $cmd &> /dev/null; then
        version=$($cmd --version 2>&1 | head -n1)
        echo -e "${GREEN}✓${NC} $name: $version"
        return 0
    else
        if [ "$required" = "required" ]; then
            echo -e "${RED}✗${NC} $name: NOT FOUND (REQUIRED)"
            ((ERRORS++))
        else
            echo -e "${YELLOW}⚠${NC} $name: NOT FOUND (optional)"
            ((WARNINGS++))
        fi
        return 1
    fi
}

# Function to check Python module
check_python_module() {
    local module=$1
    local name=$2
    local required=$3
    
    if python3 -c "import $module" 2>/dev/null; then
        version=$(python3 -c "import $module; print($module.__version__)" 2>/dev/null || echo "unknown")
        echo -e "${GREEN}✓${NC} $name: $version"
        return 0
    else
        if [ "$required" = "required" ]; then
            echo -e "${RED}✗${NC} $name: NOT FOUND (REQUIRED)"
            ((ERRORS++))
        else
            echo -e "${YELLOW}⚠${NC} $name: NOT FOUND (optional)"
            ((WARNINGS++))
        fi
        return 1
    fi
}

# Check system commands
echo "System Commands:"
echo "----------------"
check_command python3 "Python 3" required
check_command pip "pip" required
check_command pdflatex "LaTeX" optional
check_command bibtex "BibTeX" optional
check_command make "make" optional
check_command git "git" optional
echo ""

# Check virtual environment
echo "Virtual Environment:"
echo "--------------------"
if [ -d "venv" ]; then
    echo -e "${GREEN}✓${NC} Virtual environment exists"
    
    # Try to activate
    if source venv/bin/activate 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Virtual environment can be activated"
    else
        echo -e "${RED}✗${NC} Cannot activate virtual environment"
        ((ERRORS++))
    fi
else
    echo -e "${RED}✗${NC} Virtual environment not found"
    echo "  Run: ./setup.sh"
    ((ERRORS++))
fi
echo ""

# Check Python modules (if venv exists)
if [ -d "venv" ]; then
    source venv/bin/activate 2>/dev/null || true
    
    echo "Python Modules:"
    echo "---------------"
    check_python_module numpy "NumPy" required
    check_python_module scipy "SciPy" required
    check_python_module matplotlib "Matplotlib" required
    check_python_module pytest "pytest" optional
    check_python_module qutip "QuTiP" optional
    echo ""
fi

# Check repository files
echo "Repository Files:"
echo "-----------------"
required_files=(
    "displacement_functional_improved.tex"
    "displacement_functional.py"
    "generate_figures.py"
    "requirements.txt"
    "Makefile"
    "README.md"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        size=$(ls -lh "$file" | awk '{print $5}')
        echo -e "${GREEN}✓${NC} $file ($size)"
    else
        echo -e "${RED}✗${NC} $file: NOT FOUND"
        ((ERRORS++))
    fi
done
echo ""

# Test Python code
echo "Code Verification:"
echo "------------------"
if [ -d "venv" ]; then
    source venv/bin/activate 2>/dev/null || true
    
    # Test import
    if python3 -c "from displacement_functional import DisplacementFunctional" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Can import displacement_functional"
    else
        echo -e "${RED}✗${NC} Cannot import displacement_functional"
        ((ERRORS++))
    fi
    
    # Test basic functionality
    if python3 -c "from displacement_functional import qutrit_thermal_semigroup; qutrit_thermal_semigroup()" >/dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} qutrit_thermal_semigroup() works"
    else
        echo -e "${RED}✗${NC} qutrit_thermal_semigroup() failed"
        ((ERRORS++))
    fi
    
    # Test figure generation imports
    if python3 -c "import generate_figures" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Can import generate_figures"
    else
        echo -e "${RED}✗${NC} Cannot import generate_figures"
        ((ERRORS++))
    fi
else
    echo -e "${YELLOW}⚠${NC} Skipping code tests (no virtual environment)"
    ((WARNINGS++))
fi
echo ""

# Check LaTeX compilation capability
echo "LaTeX Verification:"
echo "-------------------"
if command -v pdflatex &> /dev/null; then
    # Create a minimal test file
    cat > test_latex.tex << 'EOF'
\documentclass{article}
\begin{document}
Test
\end{document}
EOF
    
    if pdflatex -interaction=nonstopmode test_latex.tex > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Can compile LaTeX documents"
        rm -f test_latex.*
    else
        echo -e "${RED}✗${NC} LaTeX compilation failed"
        rm -f test_latex.*
        ((ERRORS++))
    fi
else
    echo -e "${YELLOW}⚠${NC} LaTeX not available (optional)"
    ((WARNINGS++))
fi
echo ""

# Disk space check
echo "Disk Space:"
echo "-----------"
available=$(df -h . | tail -1 | awk '{print $4}')
echo "  Available: $available"
echo ""

# Summary
echo "=================================================="
echo "Verification Summary"
echo "=================================================="
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ All required components verified!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Generate everything: ./run_all.sh"
    echo "  2. Run tests:          make test"
    echo "  3. Compile paper:      make paper"
else
    echo -e "${RED}✗ Found $ERRORS error(s)${NC}"
    echo ""
    echo "Please fix the errors above before proceeding."
    echo "Try running: ./setup.sh"
fi

if [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}⚠ Found $WARNINGS warning(s)${NC}"
    echo "  These are optional components."
fi

echo ""
exit $ERRORS
