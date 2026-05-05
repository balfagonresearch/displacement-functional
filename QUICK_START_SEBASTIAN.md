# Quick Start Guide for Sebastián
## Displacement Functional Repository

**Your Mac:** MacBook Pro  
**Setup time:** ~15 minutes  
**Prerequisites:** None (script handles everything)

---

## 🚀 Installation (One Command)

Open Terminal and run:

```bash
cd ~/Desktop  # Or wherever you want the repo
# (Christian will send you the folder)
cd displacement-functional
chmod +x setup.sh
./setup.sh
```

The script will:
1. ✓ Check/install Homebrew
2. ✓ Check/install Python 3
3. ✓ Ask about LaTeX (choose option 2: BasicTeX for speed)
4. ✓ Create virtual environment
5. ✓ Install all Python packages
6. ✓ Run verification tests
7. ✓ Create convenience scripts

**Total install:** ~5-10 minutes (depending on LaTeX choice)

---

## 📦 What You'll Have After Setup

```
displacement-functional/
├── activate.sh              ← Run this first!
├── compile_paper.sh         ← Compile & open PDF
├── run_all.sh               ← Generate everything
├── venv/                    ← Python environment
└── [all the code files]
```

---

## 🎯 Daily Workflow

### Option 1: Generate Everything (Recommended First Time)
```bash
./run_all.sh
```
**Output:**
- `fig1_entropy.pdf` - Entropy trajectories
- `fig2_lambda.pdf` - Dissipation rate
- `fig3_ion_trap.pdf` - Ion trap bounds  
- `displacement_functional_improved.pdf` - Complete paper

### Option 2: Just Compile the Paper
```bash
./compile_paper.sh
```
Opens the PDF automatically when done.

### Option 3: Manual Control
```bash
source activate.sh          # Activate environment
make figures                # Generate figures
make paper                  # Compile paper
make clean                  # Clean temp files
```

---

## 🔧 Common Tasks

### Run Examples
```bash
source activate.sh
python displacement_functional.py
```
**Output:** Qutrit example + ion trap bounds

### Generate Just One Figure
```bash
source activate.sh
python generate_figures.py
```

### Run Tests
```bash
source activate.sh
make test                   # Full test suite
make quick-test             # Just run the examples
```

### Check What's Available
```bash
make help
```

---

## 📝 Editing Workflow

If Christian asks you to modify parameters:

1. **Edit the Python file:**
   ```bash
   nano displacement_functional.py  # or use VS Code, etc.
   ```

2. **Test your changes:**
   ```bash
   source activate.sh
   python displacement_functional.py
   ```

3. **Regenerate everything:**
   ```bash
   ./run_all.sh
   ```

---

## 🐛 Troubleshooting

### "Command not found: pdflatex"
```bash
# LaTeX not in PATH. Add this to ~/.zshrc:
export PATH="/Library/TeX/texbin:$PATH"
source ~/.zshrc
```

### "ModuleNotFoundError: No module named 'numpy'"
```bash
# Virtual environment not activated
source activate.sh
# Or
source venv/bin/activate
```

### "Permission denied: ./setup.sh"
```bash
chmod +x setup.sh
chmod +x *.sh
```

### Paper won't compile - LaTeX error
```bash
# Clean and retry
make clean
make paper
```

### Can't open PDF automatically
```bash
# Manual open
open displacement_functional_improved.pdf
# Or just double-click it in Finder
```

---

## 📊 Expected Output Examples

### Running `python displacement_functional.py`
```
Displacement Functional Computation
============================================================

Example 1: Qutrit thermal semigroup
------------------------------------------------------------
Initial entropy: r_0 = 0.309
Displacement functional: J = 0.439
Entropy production: EP = 0.226
Chi^2 displacement: J_chi2 = 0.439
Cramér-Rao ratio: J·EP/r_0^2 = 1.037
```

### Running `make test`
```
Running tests...
test_displacement_functional.py::TestDisplacementFunctional::test_qutrit_semigroup_creation PASSED
test_displacement_functional.py::TestDisplacementFunctional::test_relative_entropy PASSED
...
✓ Tests passed
```

---

## 🔄 Updating the Paper

If Christian sends updates:

1. Replace the `.tex` file
2. Run: `make clean && make paper`
3. Done!

---

## 💾 Saving Your Work

The virtual environment (`venv/`) is local - no need to back it up.
Just back up:
- Any code changes you make
- Generated PDFs you want to keep

---

## 🆘 Need Help?

**First:** Try `make help` to see all options

**Second:** Check this file for common issues

**Third:** Send Christian:
- What you tried to run
- The exact error message
- Output of `python3 --version` and `pdflatex --version`

---

## ✅ Quick Verification

After setup, test everything works:

```bash
source activate.sh
make quick-test
```

Should see:
```
✓ Quick test passed
```

If you see that, you're all set! 🎉

---

## 📚 Useful Commands Reference

| Command | What it does |
|---------|--------------|
| `source activate.sh` | Activate Python environment |
| `./run_all.sh` | Generate everything |
| `./compile_paper.sh` | Compile paper only |
| `make help` | Show all options |
| `make clean` | Remove temp files |
| `make test` | Run tests |
| `deactivate` | Exit virtual environment |

---

**Last updated:** 2025-01-XX  
**Questions?** Ask Christian
