"""
Displacement Functional Computation for Quantum Markov Semigroups

This module implements exact computation of the displacement functional
J(rho_0) = int_0^infty S(Phi_t(rho_0) || sigma) dt
for finite-dimensional quantum Markov semigroups with quantum detailed balance.

Author: Christian Balfagón
Date: 2025
License: MIT
"""

import numpy as np
from scipy.linalg import eigh, sqrtm, inv
from scipy.integrate import quad
from typing import Tuple, Optional
import matplotlib.pyplot as plt


class DisplacementFunctional:
    """
    Computes the displacement functional for quantum Markov semigroups.
    
    Attributes:
        lindbladian: Liouvillian superoperator (d^2 x d^2 matrix)
        sigma: Fixed point (d x d density matrix)
        d: Hilbert space dimension
    """
    
    def __init__(self, lindbladian: np.ndarray, sigma: np.ndarray):
        """
        Initialize with Lindbladian and fixed point.
        
        Args:
            lindbladian: Liouvillian in vectorized form (d^2 x d^2)
            sigma: Fixed point density matrix (d x d)
        """
        self.sigma = sigma
        self.d = sigma.shape[0]
        
        # Verify fixed point
        sigma_vec = sigma.flatten()
        result = lindbladian @ sigma_vec
        assert np.allclose(result, 0, atol=1e-10), "sigma is not a fixed point"
        
        self.lindbladian = lindbladian
        
    def gns_representation(self) -> np.ndarray:
        """
        Compute GNS representation: L_hat = J_sigma^{-1/2} L J_sigma^{1/2}
        
        Returns:
            GNS Lindbladian (self-adjoint for QDB)
        """
        # J_sigma(X) = sigma^{1/2} X sigma^{1/2}
        # In vectorized form, this is a similarity transform
        
        sqrt_sigma = sqrtm(self.sigma)
        inv_sqrt_sigma = inv(sqrt_sigma)
        
        # Build J_sigma as superoperator
        J_sigma = np.zeros((self.d**2, self.d**2), dtype=complex)
        for i in range(self.d):
            for j in range(self.d):
                for k in range(self.d):
                    for l in range(self.d):
                        ij = i * self.d + j
                        kl = k * self.d + l
                        J_sigma[ij, kl] = sqrt_sigma[i,k] * sqrt_sigma[j,l]
        
        J_sigma_inv = np.linalg.inv(J_sigma)
        sqrt_J_sigma = sqrtm(J_sigma)
        inv_sqrt_J_sigma = inv(sqrt_J_sigma)
        
        # L_hat = J_sigma^{-1/2} L J_sigma^{1/2}
        L_hat = inv_sqrt_J_sigma @ self.lindbladian @ sqrt_J_sigma
        
        # Verify self-adjointness (QDB condition)
        if not np.allclose(L_hat, L_hat.conj().T, atol=1e-8):
            print("Warning: Generator does not satisfy QDB (L_hat not self-adjoint)")
        
        return L_hat
    
    def compute_J_exact(self, rho_0: np.ndarray) -> Tuple[float, dict]:
        """
        Compute displacement functional exactly via eigendecomposition.
        
        This is Algorithm 1 from the paper.
        
        Args:
            rho_0: Initial density matrix (d x d)
            
        Returns:
            J: Displacement functional value
            info: Dictionary with spectral data
        """
        # Step 1: GNS representation
        L_hat = self.gns_representation()
        
        # Step 2: Eigendecomposition of -L_hat
        eigenvalues, eigenvectors = eigh(-L_hat)
        
        # Filter out the zero eigenvalue (fixed point)
        nonzero_mask = eigenvalues > 1e-10
        lambdas = eigenvalues[nonzero_mask]
        taus = eigenvectors[:, nonzero_mask]
        
        # Step 3: Project rho_0 - sigma onto eigenbasis
        delta = rho_0 - self.sigma
        delta_vec = delta.flatten()
        
        # Compute coefficients c_j = Tr[tau_j sigma^{-1} delta]
        inv_sigma = inv(self.sigma)
        coeffs = []
        
        for j in range(len(lambdas)):
            tau_j_vec = taus[:, j]
            tau_j = tau_j_vec.reshape(self.d, self.d)
            
            # c_j = Tr[tau_j sigma^{-1} delta]
            c_j = np.trace(tau_j @ inv_sigma @ delta)
            coeffs.append(c_j)
        
        coeffs = np.array(coeffs)
        
        # Step 4: Compute spectral weights w_j = |c_j|^2 <tau_j, J_sigma(tau_j)>_sigma
        weights = []
        
        for j in range(len(lambdas)):
            tau_j_vec = taus[:, j]
            tau_j = tau_j_vec.reshape(self.d, self.d)
            
            # J_sigma(tau_j) = sigma^{1/2} tau_j sigma^{1/2}
            sqrt_sigma = sqrtm(self.sigma)
            J_tau_j = sqrt_sigma @ tau_j @ sqrt_sigma
            
            # <tau_j, J_sigma(tau_j)>_sigma = Tr[tau_j sigma^{-1} J_tau_j]
            inner_product = np.trace(tau_j @ inv_sigma @ J_tau_j)
            
            w_j = np.abs(coeffs[j])**2 * inner_product.real
            weights.append(w_j)
        
        weights = np.array(weights)
        
        # Step 5: Compute J = sum_{j} w_j / (2 lambda_j)
        J = np.sum(weights / (2 * lambdas))
        
        # Also compute EP and chi^2 for verification
        EP = np.sum(2 * lambdas * weights)
        chi2 = np.sum(weights)
        
        info = {
            'eigenvalues': lambdas,
            'weights': weights,
            'EP': EP,
            'chi2': chi2,
            'J_chi2': np.sum(weights / (2 * lambdas)),
            'EP_chi2': EP,
            'CR_ratio': J * EP / (self.relative_entropy(rho_0, self.sigma)**2)
        }
        
        return J, info
    
    @staticmethod
    def relative_entropy(rho: np.ndarray, sigma: np.ndarray) -> float:
        """
        Compute Umegaki relative entropy S(rho || sigma) = Tr[rho (log rho - log sigma)]
        
        Args:
            rho: Density matrix
            sigma: Reference density matrix
            
        Returns:
            S(rho || sigma)
        """
        # Eigendecompose
        eigvals_rho, eigvecs_rho = eigh(rho)
        eigvals_sigma, eigvecs_sigma = eigh(sigma)
        
        # Set small eigenvalues to machine epsilon for numerical stability
        eigvals_rho = np.where(eigvals_rho > 1e-12, eigvals_rho, 1e-12)
        eigvals_sigma = np.where(eigvals_sigma > 1e-12, eigvals_sigma, 1e-12)
        
        # Reconstruct logarithms
        log_rho = eigvecs_rho @ np.diag(np.log(eigvals_rho)) @ eigvecs_rho.conj().T
        log_sigma = eigvecs_sigma @ np.diag(np.log(eigvals_sigma)) @ eigvecs_sigma.conj().T
        
        S = np.trace(rho @ (log_rho - log_sigma)).real
        
        return S
    
    def compute_J_quadrature(self, rho_0: np.ndarray, T_max: float = 20) -> float:
        """
        Compute J via numerical integration (for comparison).
        
        Args:
            rho_0: Initial density matrix
            T_max: Integration cutoff time
            
        Returns:
            J: Displacement functional (approximate)
        """
        def S_t(t):
            # Evolve rho_0 -> rho(t) via matrix exponential
            rho_t_vec = expm(self.lindbladian * t) @ rho_0.flatten()
            rho_t = rho_t_vec.reshape(self.d, self.d)
            return self.relative_entropy(rho_t, self.sigma)
        
        J, error = quad(S_t, 0, T_max, limit=100)
        
        return J


def qutrit_thermal_semigroup(gamma: float = 0.1, 
                              beta_omega: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Construct the qutrit thermal semigroup from the paper.
    
    Args:
        gamma: Overall decay rate
        beta_omega: Inverse temperature times transition frequency
        
    Returns:
        lindbladian: Liouvillian superoperator
        sigma: Thermal fixed point
    """
    d = 3
    
    # Thermal populations
    Z = 1 + np.exp(-beta_omega) + np.exp(-2*beta_omega)
    p = np.array([1, np.exp(-beta_omega), np.exp(-2*beta_omega)]) / Z
    sigma = np.diag(p)
    
    # Transition rates gamma_{ij} = gamma exp(-(j-i)/2)
    def rate(i, j):
        if i == j:
            return 0
        return gamma * np.exp(-(j - i) / 2)
    
    # Build Lindbladian in Pauli basis
    # For simplicity, use the master equation form
    L = np.zeros((d**2, d**2), dtype=complex)
    
    # Diagonal part (population relaxation)
    for i in range(d):
        for j in range(d):
            if i != j:
                ij_idx = i * d + j
                # Dephasing from transitions
                for k in range(d):
                    if k != i:
                        L[ij_idx, ij_idx] -= rate(i, k) / 2
                    if k != j:
                        L[ij_idx, ij_idx] -= rate(j, k) / 2
    
    # Off-diagonal (coherence decay via QDB)
    # Detailed balance: gamma_{ij} sigma_j = gamma_{ji} sigma_i
    for i in range(d):
        for j in range(d):
            if i != j:
                ii_idx = i * d + i
                jj_idx = j * d + j
                
                # Population transfer i -> j
                L[jj_idx, ii_idx] = rate(i, j)
                L[ii_idx, ii_idx] -= rate(i, j)
    
    return L, sigma


def ion_trap_example():
    """
    Demonstrate the ion trap cooling time bound from Section 8.5.
    """
    # Physical parameters for Ca-40 ion
    omega_0 = 2 * np.pi * 411e12  # Hz (optical transition)
    gamma = 2 * np.pi * 20.7e6    # Hz (spontaneous emission rate)
    T = 300                        # K
    k_B = 1.380649e-23            # J/K
    hbar = 1.054572e-34           # J·s
    
    beta = hbar * omega_0 / (k_B * T)
    
    # Thermal occupation
    n_bar = 1 / (np.exp(beta) - 1)
    
    # Fixed point (thermal state)
    p_e = n_bar / (n_bar + 1)
    sigma = np.diag([1 - p_e, p_e])
    
    # Lindbladian (spontaneous emission + absorption)
    d = 2
    L = np.zeros((d**2, d**2))
    
    # Simplified model: pure dephasing + thermalization
    alpha = gamma * (1 + 2*n_bar)  # MLSI constant
    
    # Define two initial states
    # 1. Equal superposition |+><+|
    rho_plus = 0.5 * np.array([[1, 1], [1, 1]])
    
    # 2. Optimal eigenstate (ground state)
    rho_optimal = np.array([[1, 0], [0, 0]])
    
    # Build simple depolarizing Lindbladian
    I = np.eye(d)
    L = -alpha * np.kron(I, I)
    for i in range(d):
        for j in range(d):
            ij = i*d + j
            L[ij, ij] += alpha
    
    # Set diagonal to preserve sigma
    L = L - np.outer(sigma.flatten(), sigma.flatten()) * np.trace(L)
    
    df = DisplacementFunctional(L, sigma)
    
    # Compute for both states
    results = {}
    for name, rho_0 in [("plus", rho_plus), ("optimal", rho_optimal)]:
        r_0 = df.relative_entropy(rho_0, sigma)
        J, info = df.compute_J_exact(rho_0)
        EP = info['EP']
        
        # Target entropy
        S_targ = 0.01
        
        # Spectral bound: T >= (1/2alpha) log(r_0 / S_targ)
        T_spectral = (1 / (2*alpha)) * np.log(r_0 / S_targ)
        
        # CR bound: T >= r_0^2 / (EP * S_targ)
        T_CR = r_0**2 / (EP * S_targ)
        
        results[name] = {
            'r_0': r_0,
            'J': J,
            'EP': EP,
            'T_spectral': T_spectral,
            'T_CR': T_CR,
            'ratio': T_CR / T_spectral
        }
    
    print("Ion Trap Cooling Time Bounds")
    print("="*60)
    print(f"Physical parameters:")
    print(f"  omega_0 = {omega_0/1e12:.1f} THz")
    print(f"  gamma   = {gamma/1e6:.1f} MHz")
    print(f"  T       = {T} K")
    print(f"  beta    = {beta:.2f}")
    print(f"  n_bar   = {n_bar:.2e}")
    print(f"  alpha   = {alpha/1e6:.1f} MHz")
    print()
    
    for name, res in results.items():
        print(f"Initial state: |{name}>")
        print(f"  r_0 = {res['r_0']:.3f}")
        print(f"  T_spectral = {res['T_spectral']*1e9:.1f} ns")
        print(f"  T_CR       = {res['T_CR']*1e9:.1f} ns")
        print(f"  Ratio      = {res['ratio']:.2f}")
        print()
    
    return results


if __name__ == "__main__":
    print("Displacement Functional Computation")
    print("="*60)
    print()
    
    # Example 1: Qutrit thermal semigroup
    print("Example 1: Qutrit thermal semigroup")
    print("-"*60)
    
    L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
    df = DisplacementFunctional(L, sigma)
    
    # Initial state: maximally mixed
    rho_0 = np.eye(3) / 3
    
    r_0 = df.relative_entropy(rho_0, sigma)
    J, info = df.compute_J_exact(rho_0)
    
    print(f"Initial entropy: r_0 = {r_0:.3f}")
    print(f"Displacement functional: J = {J:.3f}")
    print(f"Entropy production: EP = {info['EP']:.3f}")
    print(f"Chi^2 displacement: J_chi2 = {info['J_chi2']:.3f}")
    print(f"Cramér-Rao ratio: J·EP/r_0^2 = {info['CR_ratio']:.3f}")
    print()
    
    # Spectral data
    print(f"Eigenvalues: {info['eigenvalues']}")
    print(f"Weights: {info['weights']}")
    print()
    
    # Example 2: Ion trap application
    print("Example 2: Ion trap cooling bounds")
    print("-"*60)
    
    ion_trap_example()
