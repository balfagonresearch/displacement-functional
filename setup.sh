#!/bin/bash
# Automated setup script for Displacement Functional repository
# For macOS (Sebastián's MacBook Pro)

set -e  # Exit on error

echo "=========================================="
echo "Displacement Functional - Setup Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_warning "This script is optimized for macOS"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Step 1: Checking system requirements..."
echo "----------------------------------------"

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    print_error "Homebrew not found"
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    print_status "Homebrew installed"
else
    print_status "Homebrew found"
fi

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 not found"
    echo "Installing Python 3..."
    brew install python3
    print_status "Python 3 installed"
else
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python 3 found (version $PYTHON_VERSION)"
fi

# Check for LaTeX
echo ""
echo "Step 2: Checking LaTeX installation..."
echo "----------------------------------------"

if ! command -v pdflatex &> /dev/null; then
    print_warning "LaTeX not found"
    echo ""
    echo "LaTeX is required to compile the paper."
    echo "Options:"
    echo "  1. Install MacTeX (full, ~4GB): brew install --cask mactex"
    echo "  2. Install BasicTeX (minimal, ~100MB): brew install --cask basictex"
    echo "  3. Skip LaTeX installation (you can compile online)"
    echo ""
    read -p "Choose option (1/2/3): " latex_choice
    
    case $latex_choice in
        1)
            echo "Installing MacTeX (this may take a while)..."
            brew install --cask mactex
            print_status "MacTeX installed"
            # Add to PATH
            export PATH="/Library/TeX/texbin:$PATH"
            ;;
        2)
            echo "Installing BasicTeX..."
            brew install --cask basictex
            print_status "BasicTeX installed"
            # Add to PATH
            export PATH="/Library/TeX/texbin:$PATH"
            # Install additional packages
            sudo tlmgr update --self
            sudo tlmgr install collection-fontsrecommended
            sudo tlmgr install collection-latexrecommended
            ;;
        3)
            print_warning "Skipping LaTeX installation"
            ;;
        *)
            print_error "Invalid option"
            exit 1
            ;;
    esac
else
    print_status "LaTeX found ($(pdflatex --version | head -n1))"
fi

# Create Python virtual environment
echo ""
echo "Step 3: Setting up Python environment..."
echo "----------------------------------------"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
print_status "Virtual environment activated"

# Install Python dependencies
echo ""
echo "Step 4: Installing Python dependencies..."
echo "----------------------------------------"

pip install --upgrade pip
pip install -r requirements.txt
print_status "Python dependencies installed"

# Verify installation
echo ""
echo "Step 5: Verifying installation..."
echo "----------------------------------------"

python3 -c "import numpy, scipy, matplotlib; print('✓ Core packages OK')"
print_status "Core packages verified"

# Run quick test
echo ""
echo "Step 6: Running quick test..."
echo "----------------------------------------"

python3 displacement_functional.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_status "Quick test passed"
else
    print_warning "Quick test had issues (check manually)"
fi

# Create convenience scripts
echo ""
echo "Step 7: Creating convenience scripts..."
echo "----------------------------------------"

# Create activation script
cat > activate.sh << 'EOF'
#!/bin/bash
# Quick activation script
source venv/bin/activate
echo "✓ Virtual environment activated"
echo "Run 'make help' to see available commands"
EOF
chmod +x activate.sh
print_status "Created activate.sh"

# Create compile script
cat > compile_paper.sh << 'EOF'
#!/bin/bash
# Quick paper compilation
source venv/bin/activate
make paper
echo ""
echo "✓ Paper compiled: displacement_functional_improved.pdf"
open displacement_functional_improved.pdf 2>/dev/null || echo "Open the PDF manually"
EOF
chmod +x compile_paper.sh
print_status "Created compile_paper.sh"

# Create all script
cat > run_all.sh << 'EOF'
#!/bin/bash
# Generate everything
source venv/bin/activate
echo "Generating figures..."
make figures
echo "Compiling paper..."
make paper
echo ""
echo "✓ All done!"
echo "  - Figures: fig1_entropy.pdf, fig2_lambda.pdf, fig3_ion_trap.pdf"
echo "  - Paper: displacement_functional_improved.pdf"
EOF
chmod +x run_all.sh
print_status "Created run_all.sh"

# Summary
echo ""
echo "=========================================="
echo "Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Activate environment:  source activate.sh"
echo "  2. Generate figures:      make figures"
echo "  3. Compile paper:         make paper"
echo "  4. Or do everything:      ./run_all.sh"
echo ""
echo "Quick commands:"
echo "  ./activate.sh           - Activate Python environment"
echo "  ./compile_paper.sh      - Compile paper and open PDF"
echo "  ./run_all.sh            - Generate everything"
echo "  make help               - Show all make targets"
echo ""
echo "Files created:"
echo "  - venv/                 - Python virtual environment"
echo "  - activate.sh           - Activation script"
echo "  - compile_paper.sh      - Quick compile script"
echo "  - run_all.sh            - Generate all outputs"
echo ""
echo "To deactivate virtual environment: deactivate"
echo ""
