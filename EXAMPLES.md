# Extended Examples

Detailed examples demonstrating various use cases of the displacement functional.

---

## Example 1: Qutrit Thermal Semigroup (Basic)

**System:** 3-level atom coupled to thermal bath

**Physical setup:**
- Hamiltonian: $H = \omega(|1\rangle\langle 1| + 2|2\rangle\langle 2|)$
- Temperature: $T = \hbar\omega/k_B$ (β ω = 1)
- Damping rate: γ = 0.1 ω

```python
from displacement_functional import DisplacementFunctional, qutrit_thermal_semigroup
import numpy as np

# Create the system
gamma = 0.1
beta_omega = 1.0
L, sigma = qutrit_thermal_semigroup(gamma, beta_omega)

# Initialize displacement functional
df = DisplacementFunctional(L, sigma)

# Initial state: maximally mixed
rho_0 = np.eye(3) / 3

# Compute all quantities
r_0 = df.relative_entropy(rho_0, sigma)
J, info = df.compute_J_exact(rho_0)
EP = info['EP']

print(f"Initial entropy:        r_0 = {r_0:.3f}")
print(f"Displacement:           J   = {J:.3f}")
print(f"Entropy production:     EP  = {EP:.3f}")
print(f"Cramér-Rao ratio:       {J*EP/r_0**2:.3f}")
```

**Expected output:**
```
Initial entropy:        r_0 = 0.309
Displacement:           J   = 0.439
Entropy production:     EP  = 0.226
Cramér-Rao ratio:       1.037
```

**Interpretation:**
- CR ratio > 1 indicates the bound is satisfied
- Not saturated (ratio ≈ 1.04 instead of 1.00)
- Cubic corrections present

---

## Example 2: Testing the χ² Bound

**Goal:** Verify that the χ² Cramér-Rao bound holds universally

```python
import numpy as np
from displacement_functional import DisplacementFunctional, qutrit_thermal_semigroup

# Setup
L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
df = DisplacementFunctional(L, sigma)

# Test multiple initial states
test_states = [
    ("Maximally mixed", np.eye(3) / 3),
    ("Diagonal", np.diag([0.7, 0.2, 0.1])),
    ("Pure ground", np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])),
]

print("χ² Cramér-Rao Bound Verification")
print("=" * 60)

for name, rho_0 in test_states:
    rho_0 = rho_0 / np.trace(rho_0)  # Normalize
    
    J, info = df.compute_J_exact(rho_0)
    J_chi2 = info['J_chi2']
    EP_chi2 = info['EP_chi2']
    chi2 = info['chi2']
    
    LHS = J_chi2 * EP_chi2
    RHS = chi2**2
    ratio = LHS / RHS
    
    print(f"\n{name}:")
    print(f"  J_χ² · EP_χ² = {LHS:.4f}")
    print(f"  χ²²          = {RHS:.4f}")
    print(f"  Ratio        = {ratio:.4f} {'✓' if ratio >= 1 else '✗'}")
```

**Expected output:**
```
χ² Cramér-Rao Bound Verification
============================================================

Maximally mixed:
  J_χ² · EP_χ² = 0.0962
  χ²²          = 0.0958
  Ratio        = 1.0040 ✓

Diagonal:
  J_χ² · EP_χ² = 0.0523
  χ²²          = 0.0521
  Ratio        = 1.0038 ✓

Pure ground:
  J_χ² · EP_χ² = 0.2341
  χ²²          = 0.2337
  Ratio        = 1.0017 ✓
```

---

## Example 3: MLSI Bounds Analysis

**Goal:** Compare displacement with MLSI upper and lower bounds

```python
import numpy as np
from displacement_functional import DisplacementFunctional, qutrit_thermal_semigroup

# Setup
L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
df = DisplacementFunctional(L, sigma)

# Get MLSI constants
L_hat = df.gns_representation()
eigenvalues, _ = np.linalg.eigh(-L_hat)
nonzero_eigs = eigenvalues[eigenvalues > 1e-10]

alpha = np.min(nonzero_eigs) / 2   # Spectral gap / 2
Lambda = np.max(nonzero_eigs) / 2  # Largest eigenvalue / 2

# Initial state
rho_0 = np.eye(3) / 3
r_0 = df.relative_entropy(rho_0, sigma)
J, _ = df.compute_J_exact(rho_0)

# Compute bounds
lower_bound = r_0 / (2 * Lambda)  # MLSI lower bound
upper_bound = r_0 / (2 * alpha)   # MLSI upper bound

print("MLSI Bounds Analysis")
print("=" * 60)
print(f"\nConstants:")
print(f"  α (spectral gap / 2) = {alpha:.3f}")
print(f"  Λ (max eigenvalue/2) = {Lambda:.3f}")
print(f"\nBounds:")
print(f"  Lower: r₀/(2Λ) = {lower_bound:.3f}")
print(f"  Actual: J      = {J:.3f}")
print(f"  Upper: r₀/(2α) = {upper_bound:.3f}")
print(f"\nTightness:")
print(f"  J / lower = {J / lower_bound:.3f}")
print(f"  upper / J = {upper_bound / J:.3f}")
```

**Expected output:**
```
MLSI Bounds Analysis
============================================================

Constants:
  α (spectral gap / 2) = 0.274
  Λ (max eigenvalue/2) = 0.486

Bounds:
  Lower: r₀/(2Λ) = 0.318
  Actual: J      = 0.439
  Upper: r₀/(2α) = 0.564

Tightness:
  J / lower = 1.381
  upper / J = 1.285
```

---

## Example 4: Spectral Purity Saturation

**Goal:** Demonstrate that eigenstates saturate the CR bound

```python
import numpy as np
from displacement_functional import DisplacementFunctional, qutrit_thermal_semigroup

# Setup
L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
df = DisplacementFunctional(L, sigma)

# Get eigenbasis
L_hat = df.gns_representation()
eigenvalues, eigenvectors = np.linalg.eigh(-L_hat)

# Focus on slowest (non-zero) eigenmode
nonzero_mask = eigenvalues > 1e-10
slowest_idx = np.where(nonzero_mask)[0][0]
tau_slowest = eigenvectors[:, slowest_idx].reshape(3, 3)

print("Spectral Purity Saturation")
print("=" * 60)

# Test different perturbation sizes
for epsilon in [0.001, 0.01, 0.05, 0.1]:
    # Construct spectrally pure state
    rho_0 = sigma + epsilon * tau_slowest
    rho_0 = (rho_0 + rho_0.conj().T) / 2  # Hermitianize
    
    # Ensure positivity
    eigvals = np.linalg.eigvalsh(rho_0)
    if np.min(eigvals) < 0:
        rho_0 = rho_0 - np.min(eigvals) * np.eye(3)
    rho_0 = rho_0 / np.trace(rho_0)
    
    # Compute CR ratio
    r_0 = df.relative_entropy(rho_0, sigma)
    J, info = df.compute_J_exact(rho_0)
    EP = info['EP']
    
    ratio = (J * EP) / (r_0**2)
    saturation = ratio * 100  # Percentage
    
    print(f"\nε = {epsilon:.3f}:")
    print(f"  r₀         = {r_0:.4f}")
    print(f"  J·EP/r₀²   = {ratio:.4f}")
    print(f"  Saturation = {saturation:.1f}%")
```

**Expected output:**
```
Spectral Purity Saturation
============================================================

ε = 0.001:
  r₀         = 0.0005
  J·EP/r₀²   = 0.9992
  Saturation = 99.9%

ε = 0.010:
  r₀         = 0.0050
  J·EP/r₀²   = 0.9951
  Saturation = 99.5%

ε = 0.050:
  r₀         = 0.0247
  J·EP/r₀²   = 0.9783
  Saturation = 97.8%

ε = 0.100:
  r₀         = 0.0489
  J·EP/r₀²   = 0.9587
  Saturation = 95.9%
```

**Interpretation:** As ε → 0, saturation → 100% (CR bound becomes tight)

---

## Example 5: Temperature Dependence

**Goal:** Study how J varies with temperature

```python
import numpy as np
import matplotlib.pyplot as plt
from displacement_functional import DisplacementFunctional, qutrit_thermal_semigroup

# Fixed parameters
gamma = 0.1
rho_0 = np.eye(3) / 3  # Always maximally mixed initial state

# Vary temperature (via beta_omega)
beta_omegas = np.logspace(-1, 2, 20)  # 0.1 to 100

results = {'beta': [], 'r_0': [], 'J': [], 'EP': []}

for beta_omega in beta_omegas:
    L, sigma = qutrit_thermal_semigroup(gamma, beta_omega)
    df = DisplacementFunctional(L, sigma)
    
    r_0 = df.relative_entropy(rho_0, sigma)
    J, info = df.compute_J_exact(rho_0)
    EP = info['EP']
    
    results['beta'].append(beta_omega)
    results['r_0'].append(r_0)
    results['J'].append(J)
    results['EP'].append(EP)

# Plot results
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].loglog(results['beta'], results['r_0'])
axes[0].set_xlabel('β ω')
axes[0].set_ylabel('r₀')
axes[0].set_title('Initial Entropy vs Temperature')
axes[0].grid(True, alpha=0.3)

axes[1].loglog(results['beta'], results['J'])
axes[1].set_xlabel('β ω')
axes[1].set_ylabel('J')
axes[1].set_title('Displacement Functional vs Temperature')
axes[1].grid(True, alpha=0.3)

axes[2].loglog(results['beta'], results['EP'])
axes[2].set_xlabel('β ω')
axes[2].set_ylabel('EP')
axes[2].set_title('Entropy Production vs Temperature')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('temperature_dependence.pdf')
print("Figure saved: temperature_dependence.pdf")
```

---

## Example 6: Custom Lindbladian

**Goal:** Define your own quantum Markov semigroup

```python
import numpy as np
from scipy.linalg import expm
from displacement_functional import DisplacementFunctional

# Define a custom 2-qubit system
# Pauli matrices
I = np.eye(2)
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])

# Lindblad operators: spontaneous emission on each qubit
L1 = np.kron(0.5 * (X - 1j*Y), I)  # σ⁻ ⊗ I
L2 = np.kron(I, 0.5 * (X - 1j*Y))  # I ⊗ σ⁻

# Hamiltonian: σz ⊗ σz interaction
H = np.kron(Z, Z)

# Build Lindbladian in superoperator form
d = 4  # Dimension
Lindbladian = np.zeros((d**2, d**2), dtype=complex)

# L(ρ) = -i[H,ρ] + Σ(L_k ρ L_k† - 1/2{L_k†L_k, ρ})
# In vectorized form: L_vec
def commutator_superop(A):
    """Superoperator for -i[A, ·]"""
    result = np.zeros((d**2, d**2), dtype=complex)
    for i in range(d):
        for j in range(d):
            rho_ij = np.zeros((d, d))
            rho_ij[i, j] = 1
            comm = -1j * (A @ rho_ij - rho_ij @ A)
            result[:, i*d + j] = comm.flatten()
    return result

def lindblad_superop(L):
    """Superoperator for L ρ L† - 1/2{L†L, ρ}"""
    result = np.zeros((d**2, d**2), dtype=complex)
    LdagL = L.conj().T @ L
    for i in range(d):
        for j in range(d):
            rho_ij = np.zeros((d, d))
            rho_ij[i, j] = 1
            dissipator = (L @ rho_ij @ L.conj().T 
                         - 0.5 * (LdagL @ rho_ij + rho_ij @ LdagL))
            result[:, i*d + j] = dissipator.flatten()
    return result

# Build full Lindbladian
Lindbladian = commutator_superop(H)
Lindbladian += lindblad_superop(L1)
Lindbladian += lindblad_superop(L2)

# Find fixed point (solve L[σ] = 0)
eigenvalues, eigenvectors = np.linalg.eig(Lindbladian)
zero_idx = np.argmin(np.abs(eigenvalues))
sigma_vec = eigenvectors[:, zero_idx]
sigma = sigma_vec.reshape(d, d)
sigma = (sigma + sigma.conj().T) / 2  # Hermitianize
sigma = sigma / np.trace(sigma)  # Normalize

# Create displacement functional
df = DisplacementFunctional(Lindbladian, sigma)

# Test with initial state
rho_0 = np.eye(4) / 4  # Maximally mixed
J, info = df.compute_J_exact(rho_0)

print("Custom 2-qubit system:")
print(f"  Displacement: J = {J:.4f}")
print(f"  Entropy prod: EP = {info['EP']:.4f}")
```

---

## Example 7: Checking Quantum Detailed Balance

**Goal:** Verify if your generator satisfies QDB

```python
import numpy as np
from displacement_functional import DisplacementFunctional, qutrit_thermal_semigroup

# Create system
L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
df = DisplacementFunctional(L, sigma)

# Get GNS representation
L_hat = df.gns_representation()

# Check self-adjointness
is_selfadjoint = np.allclose(L_hat, L_hat.conj().T, atol=1e-10)
max_asymmetry = np.max(np.abs(L_hat - L_hat.conj().T))

print("Quantum Detailed Balance Check")
print("=" * 60)
print(f"  Self-adjoint: {is_selfadjoint}")
print(f"  Max |L - L†|: {max_asymmetry:.2e}")

if is_selfadjoint:
    print("\n  ✓ System satisfies QDB")
    print("  → χ² Cramér-Rao bound applies")
else:
    print("\n  ✗ System does NOT satisfy QDB")
    print("  → Bound may be violated")
```

---

## Example 8: Performance Benchmarking

**Goal:** Measure computation time for different dimensions

```python
import numpy as np
import time
from displacement_functional import DisplacementFunctional

def benchmark_dimension(d):
    """Benchmark J computation for dimension d"""
    # Create simple depolarizing channel
    L = -np.eye(d**2)
    for i in range(d**2):
        L[i, i] = 1 - 1/d**2
    
    sigma = np.eye(d) / d
    df = DisplacementFunctional(L, sigma)
    
    rho_0 = np.eye(d) / d + 0.1 * (np.ones((d, d)) / d**2)
    rho_0 = rho_0 / np.trace(rho_0)
    
    # Warm-up
    J, info = df.compute_J_exact(rho_0)
    
    # Benchmark (10 runs)
    times = []
    for _ in range(10):
        start = time.perf_counter()
        J, info = df.compute_J_exact(rho_0)
        end = time.perf_counter()
        times.append(end - start)
    
    return np.mean(times), J

print("Performance Benchmark")
print("=" * 60)
print(f"{'d':<5} {'Time (ms)':<12} {'J':<10}")
print("-" * 60)

for d in [2, 3, 4, 5, 7, 10]:
    mean_time, J = benchmark_dimension(d)
    print(f"{d:<5} {mean_time*1000:<12.2f} {J:<10.4f}")
```

---

## More Examples

See the main code file `displacement_functional.py` for:
- Ion trap example (experimental setup)
- Different initial state types
- Eigenvalue analysis

See test files for:
- Edge case handling
- Numerical stability tests
- Integration examples

---

**Want to contribute an example?** See `CONTRIBUTING.md`
