"""
Test suite for displacement_functional.py

Run with: pytest test_displacement_functional.py -v
"""

import numpy as np
import pytest
from displacement_functional import DisplacementFunctional, qutrit_thermal_semigroup


class TestDisplacementFunctional:
    """Test the DisplacementFunctional class"""
    
    def test_qutrit_semigroup_creation(self):
        """Test that qutrit semigroup is created correctly"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        
        # Check dimensions
        assert L.shape == (9, 9), "Lindbladian should be 9x9"
        assert sigma.shape == (3, 3), "Fixed point should be 3x3"
        
        # Check sigma is a valid density matrix
        assert np.allclose(np.trace(sigma), 1.0), "Trace should be 1"
        assert np.all(np.linalg.eigvalsh(sigma) >= -1e-10), "Should be positive"
        
        # Check that sigma is a fixed point
        sigma_vec = sigma.flatten()
        result = L @ sigma_vec
        assert np.allclose(result, 0, atol=1e-10), "sigma should be fixed point"
    
    def test_relative_entropy(self):
        """Test relative entropy computation"""
        # Simple test case: relative entropy of pure state to maximally mixed
        rho = np.array([[1, 0], [0, 0]])  # |0><0|
        sigma = np.array([[0.5, 0], [0, 0.5]])  # I/2
        
        S = DisplacementFunctional.relative_entropy(rho, sigma)
        
        # S(|0><0| || I/2) = -log(1/2) = log(2)
        expected = np.log(2)
        assert np.abs(S - expected) < 1e-10, f"Expected {expected}, got {S}"
    
    def test_displacement_functional_positivity(self):
        """Test that J is always non-negative"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        
        # Test with several initial states
        test_states = [
            np.eye(3) / 3,  # Maximally mixed
            np.diag([0.7, 0.2, 0.1]),  # Diagonal
            sigma + 0.01 * np.array([[1, 0, 0], [0, -0.5, 0], [0, 0, -0.5]])  # Small perturbation
        ]
        
        for rho_0 in test_states:
            # Normalize
            rho_0 = rho_0 / np.trace(rho_0)
            
            J, info = df.compute_J_exact(rho_0)
            assert J >= 0, f"J should be non-negative, got {J}"
    
    def test_cramér_rao_bound(self):
        """Test that the Cramér-Rao inequality holds"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        
        rho_0 = np.eye(3) / 3
        J, info = df.compute_J_exact(rho_0)
        EP = info['EP']
        chi2 = info['chi2']
        
        # Chi^2 CR bound: J_chi2 * EP_chi2 >= chi^2^2
        J_chi2 = info['J_chi2']
        EP_chi2 = info['EP_chi2']
        
        LHS = J_chi2 * EP_chi2
        RHS = chi2**2
        
        assert LHS >= RHS - 1e-8, f"CR bound violated: {LHS} < {RHS}"
    
    def test_mlsi_bounds(self):
        """Test that J satisfies MLSI upper bound"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        
        # Get eigenvalues to find alpha
        L_hat = df.gns_representation()
        eigenvalues, _ = np.linalg.eigh(-L_hat)
        nonzero_mask = eigenvalues > 1e-10
        lambdas = eigenvalues[nonzero_mask]
        alpha = np.min(lambdas) / 2  # MLSI constant
        
        rho_0 = np.eye(3) / 3
        r_0 = df.relative_entropy(rho_0, sigma)
        J, _ = df.compute_J_exact(rho_0)
        
        # Upper bound: J <= r_0 / (2*alpha)
        upper_bound = r_0 / (2 * alpha)
        
        assert J <= upper_bound + 1e-8, f"MLSI upper bound violated: {J} > {upper_bound}"
    
    def test_fixed_point_zero_J(self):
        """Test that J(sigma) = 0"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        
        # Small numerical perturbation to avoid division by zero
        rho_0 = sigma + 1e-10 * np.eye(3)
        rho_0 = rho_0 / np.trace(rho_0)
        
        J, _ = df.compute_J_exact(rho_0)
        
        # Should be very close to zero
        assert J < 1e-6, f"J(sigma) should be ~0, got {J}"
    
    def test_spectral_purity_saturation(self):
        """Test that spectrally pure states saturate the bound"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        
        # Get eigenspace
        L_hat = df.gns_representation()
        eigenvalues, eigenvectors = np.linalg.eigh(-L_hat)
        nonzero_mask = eigenvalues > 1e-10
        
        # Project onto slowest eigenspace
        tau_slowest = eigenvectors[:, nonzero_mask][:, 0].reshape(3, 3)
        epsilon = 0.01
        rho_0 = sigma + epsilon * tau_slowest
        rho_0 = rho_0 / np.trace(rho_0)
        
        J, info = df.compute_J_exact(rho_0)
        r_0 = df.relative_entropy(rho_0, sigma)
        EP = info['EP']
        
        # Check saturation: J * EP / r_0^2 should be very close to 1
        ratio = (J * EP) / (r_0**2)
        
        # Allow some tolerance due to numerical errors
        assert np.abs(ratio - 1.0) < 0.05, f"Spectral purity should saturate, got ratio {ratio}"


class TestNumericalExamples:
    """Test the numerical examples from the paper"""
    
    def test_qutrit_example_values(self):
        """Test that qutrit example produces expected values"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        
        rho_0 = np.eye(3) / 3
        r_0 = df.relative_entropy(rho_0, sigma)
        J, info = df.compute_J_exact(rho_0)
        EP = info['EP']
        
        # Check approximate values from paper
        assert 0.30 < r_0 < 0.32, f"r_0 should be ~0.309, got {r_0}"
        assert 0.43 < J < 0.45, f"J should be ~0.439, got {J}"
        assert 0.22 < EP < 0.24, f"EP should be ~0.226, got {EP}"
    
    def test_eigenvalue_structure(self):
        """Test that eigenvalue structure is correct"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        
        L_hat = df.gns_representation()
        eigenvalues, _ = np.linalg.eigh(-L_hat)
        
        # Filter out zero eigenvalue
        nonzero_eigs = eigenvalues[eigenvalues > 1e-10]
        
        # Should have d^2 - 1 = 8 nonzero eigenvalues
        assert len(nonzero_eigs) == 8, f"Expected 8 nonzero eigenvalues, got {len(nonzero_eigs)}"
        
        # Smallest should be approximately alpha from paper
        alpha = np.min(nonzero_eigs) / 2
        assert 0.27 < alpha < 0.28, f"alpha should be ~0.274, got {alpha}"


def test_imports():
    """Test that all required packages can be imported"""
    try:
        import numpy
        import scipy
        import matplotlib
    except ImportError as e:
        pytest.fail(f"Required package not found: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
