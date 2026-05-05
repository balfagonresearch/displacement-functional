# Installation Guide
## Displacement Functional for Quantum Markov Semigroups

Complete installation instructions for macOS, Linux, and Windows.

---

## macOS (Sebastián's Setup)

### Automated Installation (Recommended)

**One-command setup:**
```bash
chmod +x setup.sh
./setup.sh
```

The script will:
1. Install Homebrew (if needed)
2. Install Python 3 (if needed)
3. Offer LaTeX installation options
4. Create virtual environment
5. Install Python dependencies
6. Run verification tests
7. Create convenience scripts

**Estimated time:** 5-15 minutes (depending on what's already installed)

### Manual Installation

If you prefer manual control:

**Step 1: Install Homebrew (if not installed)**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Step 2: Install Python 3**
```bash
brew install python3
```

**Step 3: Install LaTeX**

*Option A: Full MacTeX (~4GB)*
```bash
brew install --cask mactex
```

*Option B: BasicTeX (~100MB, recommended)*
```bash
brew install --cask basictex
sudo tlmgr update --self
sudo tlmgr install collection-fontsrecommended
sudo tlmgr install collection-latexrecommended
```

**Step 4: Set up Python environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Step 5: Verify installation**
```bash
python displacement_functional.py
make quick-test
```

---

## Linux (Ubuntu/Debian)

### Automated Installation

```bash
chmod +x setup.sh
./setup.sh
```

### Manual Installation

**Step 1: Install system dependencies**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
sudo apt-get install texlive-full  # Or texlive-latex-extra for minimal
```

**Step 2: Set up Python environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Step 3: Verify**
```bash
make quick-test
```

---

## Windows

### Prerequisites

1. Install Python 3.8+: https://www.python.org/downloads/
   - ✓ Check "Add Python to PATH" during installation

2. Install MiKTeX: https://miktex.org/download
   - Choose complete installation

3. Install Git Bash (optional, for convenience): https://git-scm.com/downloads

### Installation

**Option 1: Using PowerShell**
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Option 2: Using Git Bash (if installed)**
```bash
python -m venv venv
source venv/Scripts/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Compilation

**Compile paper:**
```bash
pdflatex displacement_functional_improved.tex
bibtex displacement_functional_improved
pdflatex displacement_functional_improved.tex
pdflatex displacement_functional_improved.tex
```

**Generate figures:**
```bash
python generate_figures.py
```

---

## Verification

After installation, verify everything works:

### Test 1: Python Environment
```bash
source venv/bin/activate  # Or .\venv\Scripts\activate on Windows
python -c "import numpy, scipy, matplotlib; print('✓ Packages OK')"
```

Expected output:
```
✓ Packages OK
```

### Test 2: Code Execution
```bash
python displacement_functional.py
```

Expected output:
```
Displacement Functional Computation
============================================================

Example 1: Qutrit thermal semigroup
------------------------------------------------------------
Initial entropy: r_0 = 0.309
Displacement functional: J = 0.439
...
```

### Test 3: Figure Generation
```bash
python generate_figures.py
```

Expected output:
```
Generating figures for Displacement Functional paper
============================================================

Generated fig1_entropy.pdf
✓ Figure 1 complete
...
```

### Test 4: LaTeX Compilation
```bash
make paper  # or use pdflatex commands on Windows
```

Expected output:
```
✓ Paper compiled successfully: displacement_functional_improved.pdf
```

---

## Dependencies

### Python Packages

**Required:**
- numpy >= 1.20.0
- scipy >= 1.7.0
- matplotlib >= 3.4.0

**Optional:**
- qutip >= 4.6.0 (extended quantum features)
- jupyter >= 1.0.0 (interactive notebooks)
- pytest >= 6.0.0 (running tests)

**Development:**
- black >= 21.0 (code formatting)
- flake8 >= 3.9.0 (linting)
- sphinx >= 4.0.0 (documentation)

### System Requirements

**Minimum:**
- Python 3.8+
- 500 MB free disk space
- 2 GB RAM

**Recommended:**
- Python 3.10+
- 2 GB free disk space
- 4 GB RAM
- LaTeX installation (BasicTeX or equivalent)

---

## Troubleshooting

### macOS Issues

**"xcrun: error: invalid active developer path"**
```bash
xcode-select --install
```

**"LaTeX not found after installation"**
```bash
export PATH="/Library/TeX/texbin:$PATH"
echo 'export PATH="/Library/TeX/texbin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**"Permission denied" errors**
```bash
chmod +x setup.sh
chmod +x *.sh
```

### Linux Issues

**"pip: command not found"**
```bash
sudo apt-get install python3-pip
```

**"venv: command not found"**
```bash
sudo apt-get install python3-venv
```

**LaTeX missing packages**
```bash
sudo tlmgr install collection-fontsrecommended
sudo tlmgr install collection-latexrecommended
```

### Windows Issues

**"python is not recognized"**
- Reinstall Python and check "Add Python to PATH"
- Or add manually: System Properties → Environment Variables

**"pdflatex is not recognized"**
- Add MiKTeX bin directory to PATH
- Usually: `C:\Program Files\MiKTeX\miktex\bin\x64\`

**Virtual environment activation fails**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### General Issues

**"ModuleNotFoundError"**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**LaTeX compilation errors**
```bash
# Clean and retry
make clean
make paper

# Or manually
rm -f *.aux *.bbl *.blg *.log
pdflatex displacement_functional_improved.tex
bibtex displacement_functional_improved
pdflatex displacement_functional_improved.tex
pdflatex displacement_functional_improved.tex
```

**Tests failing**
```bash
# Update pytest
pip install --upgrade pytest

# Run with verbose output
pytest test_displacement_functional.py -v
```

---

## Getting Help

1. **Check documentation:**
   - README.md - Overview and usage
   - QUICK_START_SEBASTIAN.md - Quick reference
   - This file - Installation details

2. **Run diagnostics:**
   ```bash
   python --version
   pip --version
   pdflatex --version
   ```

3. **Contact:**
   - Email: cb@balfagonresearch.org
   - Include: OS, Python version, error message

---

## Next Steps

After successful installation:

1. **Quick test:** `./run_all.sh` (macOS/Linux)
2. **Read:** QUICK_START_SEBASTIAN.md for daily workflow
3. **Explore:** `make help` for all available commands

**Ready to go!** 🚀
