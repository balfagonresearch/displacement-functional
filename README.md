# Displacement Functional for Quantum Markov Semigroups: Improved Version

This repository contains the improved version of the paper "The Displacement Functional for Quantum Markov Semigroups: A Cramér-Rao Bound for Cumulative Dissipation" with four major enhancements.

**Author:** Christian Balfagón  
**Affiliation:** Departamento de Física, Universidad de Buenos Aires  
**Contact:** cb@balfagonresearch.org  
**ORCID:** 0009-0003-0835-5519

## What's New

This improved version adds approximately 4 pages of content addressing key reviewer concerns:

### 1. Historical Motivation (§1.4, ~1.5 pages)
**Why the displacement functional J hasn't been studied before**

Identifies three technical barriers:
- **Integrability**: Required MLSI theory (mature only in 2010s)
- **Rate vs. integral**: Previous focus on mixing times, not cumulative cost
- **Classical analogues are vacuous**: Non-trivial structure emerges only for non-uniform σ or quantum coherences

**Key insight:** J interpolates between spectral theory (MLSI bounds) and thermodynamic uncertainty relations (CR product), filling a conceptual gap.

### 2. Ion Trap Application (§8.5, ~1 page)
**Protocol-independent thermalization time bounds**

Concrete example: Ca⁺⁴⁰ ion at 300K
- Spectral bound: T ≥ (1/2α) log(r₀/S_targ)
- **New CR bound:** T ≥ r₀²/(EP·S_targ)

**Result:** For generic states, CR bound is 33% stronger than spectral bound!

**Experimental testability:** Cumulative dissipation ∫S(t)dt measurable via:
- Continuous weak monitoring of fluorescence
- Quantum state tomography at multiple time points

### 3. Computational Methods (§8.6, ~1 page)
**Algorithm 1:** Exact computation via eigendecomposition (O(d⁶) complexity)

**Complexity comparison:**
| Method | Time | Accuracy |
|--------|------|----------|
| Direct quadrature | O(Nd³) | ε_quad |
| **Eigendecomposition** | **O(d⁶)** | **Machine precision** |
| Lanczos | O(kd⁴) | ε_Lanczos |

**Practical guidance:**
- d ≤ 10: Use exact eigendecomposition
- d ≥ 20: Use Lanczos with k ≈ 50

**Infinite dimension:** Closed-form formula for Fock states in quantum optical semigroup

**Open-source implementation:** Python code using QuTiP

### 4. Open Problems (§9, ~0.5 pages)
Five concrete future directions:

1. **Non-unique fixed points:** Generalized J_Θ with infimum over manifold
2. **Infinite-dimensional algebras:** Extension to von Neumann algebras (QFT on curved spacetime)
3. **Weaker-than-QDB scenarios:** Partial detailed balance
4. **Non-Markovian corrections:** Memory-corrected J_mem as quantitative measure
5. **Continuous-variable systems:** Explicit formula for bosonic Gaussian channels

## Files in This Repository

```
.
├── displacement_functional_improved.tex    # Main LaTeX document with all improvements
├── displacement_functional.py              # Python implementation of Algorithm 1
├── generate_figures.py                     # Script to generate all figures
└── README.md                               # This file
```

## Installation

### Requirements

**For LaTeX compilation:**
```bash
# Ubuntu/Debian
sudo apt-get install texlive-full

# macOS
brew install --cask mactex

# Windows
# Download and install MiKTeX from https://miktex.org/
```

**For Python code:**
```bash
pip install numpy scipy matplotlib qutip
```

**Minimum versions:**
- Python ≥ 3.8
- NumPy ≥ 1.20
- SciPy ≥ 1.7
- Matplotlib ≥ 3.4
- QuTiP ≥ 4.6 (optional, for extended features)

## Usage

### Compile the Paper

```bash
pdflatex displacement_functional_improved.tex
bibtex displacement_functional_improved
pdflatex displacement_functional_improved.tex
pdflatex displacement_functional_improved.tex
```

Or with latexmk:
```bash
latexmk -pdf displacement_functional_improved.tex
```

### Run Computational Examples

**Basic usage:**
```bash
python displacement_functional.py
```

**Output:**
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

Eigenvalues: [0.274 0.486 0.486]
Weights: [0.0849 0.1124 0.1124]

Example 2: Ion trap cooling bounds
------------------------------------------------------------
Physical parameters:
  omega_0 = 411.0 THz
  gamma   = 20.7 MHz
  T       = 300 K
  beta    = 159.87
  n_bar   = 1.14e-69
  alpha   = 20.7 MHz

Initial state: |plus>
  r_0 = 0.693
  T_spectral = 16.8 ns
  T_CR       = 22.4 ns
  Ratio      = 1.33

Initial state: |optimal>
  r_0 = 0.347
  T_spectral = 8.4 ns
  T_CR       = 5.6 ns
  Ratio      = 0.67
```

### Generate Figures

```bash
python generate_figures.py
```

**Generates:**
- `fig1_entropy.pdf`: Entropy trajectories (generic vs spectrally pure)
- `fig2_lambda.pdf`: Dissipation rate λ(t) evolution
- `fig3_ion_trap.pdf`: Cooling time bounds comparison

**Example output:**
```
Generating figures for Displacement Functional paper
============================================================

Generated fig1_entropy.pdf
✓ Figure 1 complete

Generated fig2_lambda.pdf
✓ Figure 2 complete

Generated fig3_ion_trap.pdf
✓ Figure 3 complete

All figures generated successfully!
```

## Key Results Summary

### Main Theorems

**Theorem 2.2 (χ² Cramér-Rao, exact):**
```
J_χ²(ρ₀) · EP_χ²(ρ₀) ≥ χ²(ρ₀‖σ)²
```
- **Universal** within QDB
- **No curvature hypothesis** needed
- **Saturated** by single eigenspace states

**Theorem 2.1 (Relative-entropy CR):**
```
J(ρ₀) · EP(ρ₀) ≥ S(ρ₀‖σ)²
```
- Requires **log-convex entropy decay**
- Perturbative otherwise: J·EP/r₀² = 1 + O(r₀^(1/2))

**Theorem 3.7 (Classification):**
```
Universal CR bound ⟺ d = 2 AND σ = I/2
```
- **Necessity:** Cubic skewness M₃ must vanish
- **Sufficiency:** Power series positivity (Equation 91)

### Bounds Hierarchy

```
r₀/(2Λ)  ≤  J(ρ₀)  ≤  r₀/(2α)
   ↑                      ↑
 MLSI-only          MLSI upper
  lower
  
Under log-convex decay:
J(ρ₀) ≥ r₀²/EP(ρ₀)  (Cramér-Rao lower, tight)
```



## Differences from Original Version

| Section | Original | Improved | Change |
|---------|----------|----------|--------|
| §1.4 | — | Historical motivation | +1.5 pages |
| §8.5 | — | Ion trap application | +1 page |
| §8.6 | — | Computational methods | +1 page |
| §9 | Basic conclusion | + Open problems | +0.5 pages |
| Total | 40 pages | 44 pages | +10% |

**New content highlights:**
- 3 technical barriers explaining historical gap
- Ca⁺⁴⁰ numerical example with 33% improvement
- Algorithm 1 with complexity analysis
- 5 concrete open problems with preliminary results

## License

This work is licensed under a Creative Commons Attribution 4.0 International License (CC BY 4.0).

**Code:** MIT License

## Acknowledgments

Special thanks to Claude (Anthropic) for assistance with:
- Identifying improvement areas
- Drafting new sections
- Code implementation
- Figure generation

## Contact

For questions, suggestions, or collaboration:
- **Email:** cb@balfagonresearch.org
- **ORCID:** [0009-0003-0835-5519](https://orcid.org/0009-0003-0835-5519)

