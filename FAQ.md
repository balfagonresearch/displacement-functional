# Frequently Asked Questions (FAQ)

## General Questions

### What is the displacement functional?

The displacement functional $\mathcal{J}(\rho_0)$ measures the **total cumulative irreversibility** of a quantum relaxation process. It's defined as:

$$\mathcal{J}(\rho_0) = \int_0^\infty S(\Phi_t(\rho_0)\|\sigma)\,dt$$

where $S(\cdot\|\sigma)$ is the relative entropy and $\Phi_t$ is the quantum Markov semigroup.

Think of it as the "area under the curve" of the entropy relaxation.

### How is this different from the MLSI?

| Quantity | What it controls | Reference |
|----------|-----------------|-----------|
| **Spectral gap Δ** | Trace distance $\|\rho(t)-\sigma\|_1$ | Spohn 1977 |
| **MLSI (α)** | Entropy $S(t)$ *pointwise* | Kastoryano-Temme 2013 |
| **This paper (J)** | Entropy *integral* | This work |

The MLSI tells you **how fast** equilibration happens. The displacement functional tells you **how much total dissipation** occurs.

### What's new in this paper?

1. **The $\chi^2$ bound** (Theorem 2.2): $\mathcal{J}_{\chi^2} \cdot \mathrm{EP}_{\chi^2} \ge \chi^2(\rho_0\|\sigma)^2$
   - Exact, non-perturbative
   - Universal within QDB
   - No curvature hypothesis needed

2. **Complete classification** (Theorem 3.7): The KL bound holds universally ⟺ $d=2$ AND $\sigma=I/2$

3. **Physical interpretation**: $\mathcal{J}$ bounds total extractable work lost during thermalization

---

## Installation Questions

### Do I need LaTeX installed?

**No, but it helps.** You can:
- Use the code without LaTeX (for numerical work)
- Compile the paper online (Overleaf)
- Install LaTeX later if needed

For macOS: `brew install --cask basictex` (quick, ~100MB)

### Which Python version do I need?

Python 3.8 or newer. Check with:
```bash
python3 --version
```

### Can I use this on Windows?

Yes! See `INSTALLATION.md` for Windows-specific instructions. You'll need:
- Python 3.8+ from python.org
- MiKTeX for LaTeX
- Git Bash (optional, for convenience)

### The setup script fails. What do I do?

1. Check you're on macOS: `uname`
2. Make it executable: `chmod +x setup.sh`
3. Try manual installation (see `INSTALLATION.md`)
4. Check error message and see `TROUBLESHOOTING.md`

---

## Usage Questions

### How do I compute J for my own system?

```python
from displacement_functional import DisplacementFunctional
import numpy as np

# 1. Create your Lindbladian (d^2 × d^2 matrix)
L = ...  # Your generator

# 2. Define fixed point (d × d density matrix)
sigma = ...  # Your equilibrium state

# 3. Create displacement functional
df = DisplacementFunctional(L, sigma)

# 4. Compute for initial state
rho_0 = ...  # Your initial state
J, info = df.compute_J_exact(rho_0)

print(f"J = {J}")
print(f"EP = {info['EP']}")
print(f"CR ratio = {J * info['EP'] / r_0**2}")
```

### What if my generator doesn't satisfy QDB?

The $\chi^2$ bound (Theorem 2.2) **requires QDB**.

The KL bound (Theorem 2.1) **also requires QDB** plus log-convex decay.

If your generator doesn't satisfy QDB:
- The bound may be violated (see Theorem 3.10)
- You can still compute $\mathcal{J}$ numerically
- But the Cramér-Rao inequality won't hold

### How do I check if my generator satisfies QDB?

```python
df = DisplacementFunctional(L, sigma)
L_hat = df.gns_representation()

# Check self-adjointness
is_qdb = np.allclose(L_hat, L_hat.conj().T, atol=1e-8)
print(f"Satisfies QDB: {is_qdb}")
```

If `L_hat` is self-adjoint, you have QDB.

### Can I use this for continuous-variable systems?

The current implementation is for **finite-dimensional** systems only.

For bosonic/continuous-variable systems, see the "Open Problems" section (§9) of the paper. An extension is possible but not yet implemented.

---

## Numerical Questions

### Why doesn't the KL bound hold for my system?

Check:
1. **Does it satisfy QDB?** (See above)
2. **Is d > 2 or σ ≠ I/d?** Then log-convex decay may fail (Theorem 3.7)
3. **Is the initial state far from equilibrium?** Cubic corrections matter (Prop 3.2)

The **$\chi^2$ bound always holds** for QDB systems.

### How accurate are the numerical results?

The eigendecomposition method (Algorithm 1) gives **machine precision** accuracy (~10⁻¹⁵).

For comparison:
- Direct quadrature: Limited by number of points
- Lanczos: Controlled truncation error

### What dimensions can I handle?

| Dimension | Method | Time |
|-----------|--------|------|
| d ≤ 10 | Eigendecomposition | Fast (< 1s) |
| d ≤ 20 | Eigendecomposition | Moderate (~10s) |
| d > 20 | Lanczos (k~50) | Depends on k |

Complexity is $O(d^6)$ for exact eigendecomposition.

### The computation is slow. How can I speed it up?

1. **Use smaller systems**: d=3 instead of d=10
2. **Use Lanczos**: For d > 20
3. **Vectorize**: Don't use loops in Python
4. **Use NumPy properly**: Ensure contiguous arrays
5. **Consider QuTiP**: For specialized quantum systems

---

## Paper Questions

### Which journal should I target?

Based on the improvements:

**Tier 1 (top choice):**
- Communications in Mathematical Physics
- Journal of Functional Analysis

**Tier 2 (excellent fit):**
- Journal of Mathematical Physics
- Annales Henri Poincaré

See `README.md` for detailed reasoning.

### How do I cite this work?

```bibtex
@article{Balfagon2025Displacement,
  title={The Displacement Functional for Quantum Markov Semigroups: 
         A Cram\'er--Rao Bound for Cumulative Dissipation},
  author={Balfag\'on, Christian},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2025}
}
```

### What's the main result?

**The $\chi^2$ Cramér-Rao bound** (Theorem 2.2):

$$\mathcal{J}_{\chi^2}(\rho_0) \cdot \mathrm{EP}_{\chi^2}(\rho_0) \ge \chi^2(\rho_0\|\sigma)^2$$

- **Exact** (no approximations)
- **Universal** (all QDB generators)
- **Sharp** (saturated by eigenstates)
- **No extra hypotheses** (no curvature, no gradient estimates)

This is stronger than the KL bound because it works universally.

---

## Development Questions

### How do I add a new example?

1. Create a new function in `displacement_functional.py`:
```python
def my_example():
    """My custom example"""
    L, sigma = ...  # Set up your system
    df = DisplacementFunctional(L, sigma)
    rho_0 = ...
    J, info = df.compute_J_exact(rho_0)
    # Print results
    return results
```

2. Add to main block:
```python
if __name__ == "__main__":
    # ... existing examples ...
    my_example()
```

3. Test it:
```bash
python displacement_functional.py
```

### How do I add a new test?

1. Create test in `test_displacement_functional.py`:
```python
def test_my_feature():
    """Test my new feature"""
    # Setup
    L, sigma = qutrit_thermal_semigroup()
    df = DisplacementFunctional(L, sigma)
    
    # Test
    result = df.my_feature()
    
    # Assert
    assert result > 0, "Feature should be positive"
```

2. Run tests:
```bash
pytest test_displacement_functional.py::test_my_feature -v
```

### Can I contribute to this project?

Yes! See `CONTRIBUTING.md` for guidelines.

Areas where contributions are welcome:
- New examples (physical systems)
- Performance optimizations
- Extended functionality (continuous-variable, non-QDB)
- Documentation improvements
- Bug fixes

---

## Troubleshooting

### Import errors

**Problem:** `ModuleNotFoundError: No module named 'numpy'`

**Solution:**
```bash
source venv/bin/activate  # or activate.sh
pip install -r requirements.txt
```

### LaTeX errors

**Problem:** `! LaTeX Error: File 'amsmath.sty' not found`

**Solution:**
```bash
# macOS
sudo tlmgr install amsmath

# Linux
sudo apt-get install texlive-latex-extra
```

### Numerical issues

**Problem:** "Lindbladian eigendecomposition failed"

**Check:**
1. Is sigma positive definite?
2. Does L actually preserve sigma?
3. Are there numerical precision issues? (Try smaller system)

### More help

See `TROUBLESHOOTING.md` for detailed debugging steps.

---

## Advanced Questions

### What's the connection to thermodynamic uncertainty relations?

The Cramér-Rao bound $\mathcal{J} \cdot \mathrm{EP} \ge r_0^2$ has the same structure as TURs:

**cost** × **current** ≥ **signal²**

Here:
- Cost = $\mathcal{J}$ (cumulative dissipation)
- Current = EP (entropy production rate)
- Signal = $r_0$ (distance from equilibrium)

### How does this relate to optimal transport?

The displacement functional is the **Green potential** of the relative entropy:

$$\mathcal{J} = (-\mathcal{L})^{-1} S(\cdot\|\sigma)$$

This connects to Wasserstein geometry via gradient flows (Erbar-Maas 2012).

### What about continuous measurements?

The current formulation assumes **unmonitored** quantum dynamics. For continuous measurement, the trajectory average needs to be taken over quantum jumps. This is an open problem (see §9 of the paper).

---

## Quick Command Reference

```bash
# Installation
./setup.sh                    # One-command install

# Usage
./run_all.sh                  # Generate everything
./compile_paper.sh            # Just compile paper
source activate.sh            # Activate environment

# Testing
make test                     # Full test suite
make quick-test               # Quick verification
pytest -v                     # Verbose tests

# Cleaning
make clean                    # Clean temp files
./clean_all.sh                # Deep clean

# Help
make help                     # Show all make targets
```

---

**Still have questions?**

Check:
1. `QUICK_START_SEBASTIAN.md` - Quick reference
2. `INSTALLATION.md` - Installation details
3. `TROUBLESHOOTING.md` - Detailed debugging
4. Email: cb@balfagonresearch.org
