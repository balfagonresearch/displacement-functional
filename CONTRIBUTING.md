# Contributing to Displacement Functional

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

---

## 🎯 Ways to Contribute

### 1. Report Issues
- **Bugs:** Numerical errors, installation problems, documentation typos
- **Enhancements:** Feature requests, optimization ideas
- **Questions:** Usage help (use FAQ first)

**How to report:**
- Check existing issues first
- Provide minimal reproducible example
- Include Python/LaTeX versions, OS
- Email: cb@balfagonresearch.org

### 2. Add Examples
Help expand the examples section!

**Good examples:**
- Physical systems (spin chains, cavities, circuits)
- Experimental setups (trapped ions, superconducting qubits)
- Theoretical models (Lindblad operators with specific symmetries)

**Template:**
```python
def my_system_example():
    """
    Example: [System name]
    
    Physical setup:
    - [Parameter 1]: [value]
    - [Parameter 2]: [value]
    
    References:
    - [Citation]
    """
    # Setup
    L, sigma = create_my_system()
    df = DisplacementFunctional(L, sigma)
    
    # Compute
    rho_0 = initial_state()
    J, info = df.compute_J_exact(rho_0)
    
    # Print results
    print_results(J, info)
    
    return results
```

### 3. Improve Documentation
- Fix typos or unclear explanations
- Add missing examples to FAQ
- Translate documentation (Spanish welcome!)
- Create tutorials or guides

### 4. Optimize Code
Performance improvements welcome!

**Focus areas:**
- Eigendecomposition for large d
- Memory efficiency
- Vectorization
- Caching strategies

**Requirements:**
- Must pass all existing tests
- Add benchmark comparison
- Document complexity improvement

### 5. Extend Functionality

**High priority:**
- Lanczos implementation (for d > 20)
- Non-QDB bound checker
- Continuous-variable systems
- Time-dependent generators

**Medium priority:**
- GPU acceleration
- Parallel computation
- Interactive visualizations
- Jupyter notebooks

---

## 📝 Contribution Process

### For Code Changes

1. **Fork the repository** (if on GitHub)

2. **Create a branch:**
   ```bash
   git checkout -b feature/my-feature
   ```

3. **Make your changes:**
   - Write code
   - Add tests
   - Update documentation

4. **Test thoroughly:**
   ```bash
   make test           # Full test suite
   make quick-test     # Quick verification
   pytest -v           # Verbose output
   ```

5. **Format code:**
   ```bash
   make format         # Black formatting
   make lint           # Flake8 linting
   ```

6. **Commit with clear message:**
   ```bash
   git commit -m "Add Lanczos implementation for large systems"
   ```

7. **Submit:**
   - Email patch: cb@balfagonresearch.org
   - Or create pull request (if on GitHub)

### For Paper Changes

1. **Identify the change:**
   - New theorem/proof
   - Additional example
   - Clarification
   - Reference addition

2. **Draft the modification:**
   - Use LaTeX comments for notes
   - Maintain consistent style
   - Update cross-references

3. **Verify compilation:**
   ```bash
   make clean
   make paper
   ```

4. **Check impact:**
   - Does it change numbering?
   - Are references updated?
   - Is bibliography complete?

5. **Submit proposal:**
   - Email: cb@balfagonresearch.org
   - Include: motivation, changes, impact

---

## 🧪 Testing Requirements

### For New Features

**Minimum testing:**
```python
def test_my_feature():
    """Test that my feature works correctly"""
    # Setup
    setup_code()
    
    # Execute
    result = my_feature()
    
    # Verify
    assert result > 0, "Feature should be positive"
    assert np.isfinite(result), "Result should be finite"
```

**Good test coverage includes:**
- ✓ Normal operation
- ✓ Edge cases (d=2, equilibrium, pure states)
- ✓ Error handling
- ✓ Performance (if performance-critical)
- ✓ Numerical accuracy

### Test Organization

```
test_my_feature.py
├── class TestBasicFunctionality
│   ├── test_normal_case()
│   └── test_different_parameters()
├── class TestEdgeCases
│   ├── test_near_equilibrium()
│   └── test_pure_states()
└── class TestPerformance
    └── test_execution_time()
```

---

## 📋 Code Style

### Python

**Follow PEP 8 with these specifics:**

```python
# Good: Clear, documented, type hints
def compute_displacement(
    L: np.ndarray,
    sigma: np.ndarray,
    rho_0: np.ndarray
) -> Tuple[float, Dict[str, Any]]:
    """
    Compute displacement functional.
    
    Args:
        L: Lindbladian (d^2 × d^2)
        sigma: Fixed point (d × d)
        rho_0: Initial state (d × d)
        
    Returns:
        J: Displacement functional value
        info: Dictionary with EP, eigenvalues, etc.
    """
    # Implementation
    ...
    return J, info
```

**Naming conventions:**
- Variables: `snake_case` (e.g., `rho_0`, `chi_squared`)
- Functions: `snake_case` (e.g., `compute_J_exact`)
- Classes: `PascalCase` (e.g., `DisplacementFunctional`)
- Constants: `UPPER_CASE` (e.g., `DEFAULT_TOLERANCE`)

**Use NumPy properly:**
```python
# Good: Vectorized
eigenvalues = np.linalg.eigvalsh(L_hat)
nonzero = eigenvalues[eigenvalues > 1e-10]

# Bad: Python loops
nonzero = []
for eig in eigenvalues:
    if eig > 1e-10:
        nonzero.append(eig)
```

### LaTeX

**Follow journal style:**
- Use `\[ \]` for display equations, not `$$ $$`
- Number all referenced equations
- Consistent notation (see paper §1.3)
- References before punctuation: "...inequality~\cite{paper}."

---

## 🔍 Review Criteria

### Code Reviews Check:

- [ ] **Functionality:** Does it work as intended?
- [ ] **Tests:** Are there adequate tests?
- [ ] **Documentation:** Is it well-documented?
- [ ] **Performance:** Is it reasonably efficient?
- [ ] **Style:** Does it follow conventions?
- [ ] **Backward compatibility:** Does it break existing code?

### Paper Reviews Check:

- [ ] **Correctness:** Is the mathematics sound?
- [ ] **Clarity:** Is it clearly written?
- [ ] **Completeness:** Are proofs complete?
- [ ] **Formatting:** Does it follow style?
- [ ] **References:** Are citations appropriate?
- [ ] **Novelty:** Is it genuinely new content?

---

## 🎓 Authorship & Credit

### Code Contributions

All contributors will be:
- Acknowledged in README.md
- Listed in code comments for major features
- Cited in any publications using the code

### Paper Contributions

Significant contributions may warrant co-authorship. Discuss with Christian beforehand.

**Criteria for co-authorship:**
- Novel theoretical results
- Major proof contributions
- Significant new examples or applications

**Acknowledgments for:**
- Bug reports
- Minor corrections
- Suggestions
- Code improvements

---

## 📞 Getting Help

### Before Contributing:

1. **Read existing docs:**
   - README.md (overview)
   - FAQ.md (common questions)
   - This file (contribution process)

2. **Check existing issues/examples:**
   - Maybe it's already done
   - Maybe someone's working on it

3. **Ask questions:**
   - Email: cb@balfagonresearch.org
   - Include: What you want to do, why, how

---

## 🎯 Priority Areas

### High Impact Contributions

1. **Examples:** New physical systems
2. **Performance:** Speed improvements
3. **Testing:** Edge case coverage
4. **Documentation:** Tutorials, guides

### Advanced Contributions

1. **Theory:** New bounds or proofs
2. **Extensions:** Continuous-variable, non-Markovian
3. **Numerical:** Better algorithms

---

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License (see LICENSE file).

---

## 🙏 Thank You!

Your contributions help make this project better for everyone. Whether it's:
- A typo fix
- A new example
- A performance improvement
- A theoretical extension

Every contribution is valuable. Thank you for taking the time to contribute!

---

**Questions?** Email: cb@balfagonresearch.org

**Last updated:** 2025-01-XX
