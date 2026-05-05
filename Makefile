# Makefile for Displacement Functional Paper
# Usage: make [target]

# Variables
TEX = displacement_functional_improved
LATEX = pdflatex
BIBTEX = bibtex
PYTHON = python3

# Main targets
.PHONY: all clean paper figures test install help

all: paper figures

# Compile the paper
paper: $(TEX).pdf

$(TEX).pdf: $(TEX).tex
	@echo "Compiling LaTeX document..."
	$(LATEX) $(TEX).tex
	$(BIBTEX) $(TEX)
	$(LATEX) $(TEX).tex
	$(LATEX) $(TEX).tex
	@echo "✓ Paper compiled successfully: $(TEX).pdf"

# Generate all figures
figures:
	@echo "Generating figures..."
	$(PYTHON) generate_figures.py
	@echo "✓ Figures generated"

# Run tests
test:
	@echo "Running tests..."
	$(PYTHON) -m pytest tests/ -v
	@echo "✓ Tests passed"

# Quick test of core functionality
quick-test:
	@echo "Running quick functionality test..."
	$(PYTHON) displacement_functional.py
	@echo "✓ Quick test passed"

# Install Python dependencies
install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "✓ Dependencies installed"

# Install for development (includes dev tools)
install-dev:
	@echo "Installing development dependencies..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✓ Development environment ready"

# Clean auxiliary files
clean:
	@echo "Cleaning auxiliary files..."
	rm -f $(TEX).aux $(TEX).bbl $(TEX).blg $(TEX).log $(TEX).out $(TEX).toc
	rm -f *.aux *.bbl *.blg *.log *.out *.toc
	rm -f *~
	@echo "✓ Cleaned"

# Clean everything including PDF
clean-all: clean
	@echo "Cleaning all generated files..."
	rm -f $(TEX).pdf
	rm -f fig*.pdf
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf *.egg-info
	@echo "✓ All cleaned"

# Format Python code
format:
	@echo "Formatting Python code..."
	black *.py
	@echo "✓ Code formatted"

# Lint Python code
lint:
	@echo "Linting Python code..."
	flake8 *.py --max-line-length=100
	@echo "✓ Linting complete"

# Check LaTeX for common issues
check-tex:
	@echo "Checking LaTeX..."
	@grep -n "TODO\|FIXME\|XXX" $(TEX).tex || echo "No TODOs found"
	@echo "✓ LaTeX checked"

# Help
help:
	@echo "Displacement Functional - Makefile Help"
	@echo "========================================"
	@echo ""
	@echo "Available targets:"
	@echo "  make all          - Build paper and generate figures"
	@echo "  make paper        - Compile LaTeX document"
	@echo "  make figures      - Generate all figures"
	@echo "  make test         - Run full test suite"
	@echo "  make quick-test   - Quick functionality test"
	@echo "  make install      - Install Python dependencies"
	@echo "  make install-dev  - Install dev environment"
	@echo "  make clean        - Remove auxiliary files"
	@echo "  make clean-all    - Remove all generated files"
	@echo "  make format       - Format Python code with black"
	@echo "  make lint         - Lint Python code with flake8"
	@echo "  make check-tex    - Check LaTeX for TODOs"
	@echo "  make help         - Show this help message"
	@echo ""
	@echo "Quick start:"
	@echo "  1. make install   # Install dependencies"
	@echo "  2. make all       # Build everything"
	@echo ""
