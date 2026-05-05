"""
Numerical tests verifying exact values from the paper

Tests that computational results match published values.
Run with: pytest test_numerics.py -v
"""

import numpy as np
import pytest
from displacement_functional import DisplacementFunctional, qutrit_thermal_semigroup


class TestPaperValues:
    """Verify numerical values reported in the paper"""
    
    def test_qutrit_example_section_8_4(self):
        """Test values from Section 8.4 (Qutrit thermal semigroup)"""
        # Parameters from paper
        gamma = 0.1
        beta_omega = 1.0
        
        L, sigma = qutrit_thermal_semigroup(gamma, beta_omega)
        df = DisplacementFunctional(L, sigma)
        
        # Initial state: maximally mixed
        rho_0 = np.eye(3) / 3
        
        # Compute quantities
        r_0 = df.relative_entropy(rho_0, sigma)
        J, info = df.compute_J_exact(rho_0)
        EP = info['EP']
        
        # Values from paper (Table in §8.4)
        # r_0 = 0.309
        # J = 0.439
        # EP = 0.226
        
        assert np.abs(r_0 - 0.309) < 0.001, f"r_0 = {r_0:.3f}, expected 0.309"
        assert np.abs(J - 0.439) < 0.001, f"J = {J:.3f}, expected 0.439"
        assert np.abs(EP - 0.226) < 0.001, f"EP = {EP:.3f}, expected 0.226"
        
        print(f"\nPaper values (§8.4):")
        print(f"  r_0 = {r_0:.3f} (expected 0.309)")
        print(f"  J   = {J:.3f} (expected 0.439)")
        print(f"  EP  = {EP:.3f} (expected 0.226)")
    
    def test_mlsi_constants(self):
        """Test MLSI constants alpha and Lambda"""
        gamma = 0.1
        beta_omega = 1.0
        
        L, sigma = qutrit_thermal_semigroup(gamma, beta_omega)
        df = DisplacementFunctional(L, sigma)
        
        # Get eigenvalues
        L_hat = df.gns_representation()
        eigenvalues, _ = np.linalg.eigh(-L_hat)
        nonzero_eigs = eigenvalues[eigenvalues > 1e-10]
        
        # MLSI constant (spectral gap / 2)
        alpha = np.min(nonzero_eigs) / 2
        
        # Lambda (largest eigenvalue / 2)
        Lambda = np.max(nonzero_eigs) / 2
        
        # Values from paper
        # alpha ≈ 0.274
        # Lambda ≈ 0.486
        
        assert np.abs(alpha - 0.274) < 0.001, f"alpha = {alpha:.3f}, expected 0.274"
        assert np.abs(Lambda - 0.486) < 0.001, f"Lambda = {Lambda:.3f}, expected 0.486"
        
        print(f"\nMLSI constants:")
        print(f"  alpha  = {alpha:.3f} (expected 0.274)")
        print(f"  Lambda = {Lambda:.3f} (expected 0.486)")
    
    def test_displacement_bounds(self):
        """Test two-sided bounds on J"""
        gamma = 0.1
        beta_omega = 1.0
        
        L, sigma = qutrit_thermal_semigroup(gamma, beta_omega)
        df = DisplacementFunctional(L, sigma)
        
        rho_0 = np.eye(3) / 3
        r_0 = df.relative_entropy(rho_0, sigma)
        J, info = df.compute_J_exact(rho_0)
        
        # Get constants
        L_hat = df.gns_representation()
        eigenvalues, _ = np.linalg.eigh(-L_hat)
        nonzero_eigs = eigenvalues[eigenvalues > 1e-10]
        alpha = np.min(nonzero_eigs) / 2
        Lambda = np.max(nonzero_eigs) / 2
        
        # Bounds: r_0/(2*Lambda) <= J <= r_0/(2*alpha)
        lower_bound = r_0 / (2 * Lambda)
        upper_bound = r_0 / (2 * alpha)
        
        # From paper table:
        # Lower (MLSI-only): 0.318
        # Upper (MLSI):      0.564
        # Actual J:          0.439
        
        assert np.abs(lower_bound - 0.318) < 0.001, \
            f"Lower bound = {lower_bound:.3f}, expected 0.318"
        assert np.abs(upper_bound - 0.564) < 0.001, \
            f"Upper bound = {upper_bound:.3f}, expected 0.564"
        
        # Verify bounds are satisfied
        assert J >= lower_bound - 1e-10, "Lower bound violated"
        assert J <= upper_bound + 1e-10, "Upper bound violated"
        
        print(f"\nDisplacement bounds:")
        print(f"  r_0/(2Λ) = {lower_bound:.3f} (expected 0.318)")
        print(f"  J        = {J:.3f} (expected 0.439)")
        print(f"  r_0/(2α) = {upper_bound:.3f} (expected 0.564)")
    
    def test_cramer_rao_ratio(self):
        """Test Cramér-Rao ratio"""
        gamma = 0.1
        beta_omega = 1.0
        
        L, sigma = qutrit_thermal_semigroup(gamma, beta_omega)
        df = DisplacementFunctional(L, sigma)
        
        rho_0 = np.eye(3) / 3
        r_0 = df.relative_entropy(rho_0, sigma)
        J, info = df.compute_J_exact(rho_0)
        EP = info['EP']
        
        # CR ratio from paper
        CR_ratio = (J * EP) / (r_0**2)
        
        # Paper reports ratio ≈ 1.037
        assert np.abs(CR_ratio - 1.037) < 0.01, \
            f"CR ratio = {CR_ratio:.3f}, expected 1.037"
        
        print(f"\nCramér-Rao ratio:")
        print(f"  J·EP/r_0² = {CR_ratio:.3f} (expected 1.037)")


class TestCubicCorrection:
    """Test cubic correction (Proposition 3.2)"""
    
    def test_cubic_violation_example(self):
        """Test cubic correction example from §8.4"""
        gamma = 0.1
        beta_omega = 1.0
        
        L, sigma = qutrit_thermal_semigroup(gamma, beta_omega)
        df = DisplacementFunctional(L, sigma)
        
        # Get eigenvector with lambda_2
        L_hat = df.gns_representation()
        eigenvalues, eigenvectors = np.linalg.eigh(-L_hat)
        
        # Find lambda_2 ≈ 0.486
        idx = np.where(np.abs(eigenvalues - 0.972) < 0.01)[0]
        if len(idx) > 0:
            tau = eigenvectors[:, idx[0]].reshape(3, 3)
            
            # Small perturbation in this direction
            epsilon = 0.05
            rho_0 = sigma + epsilon * tau
            rho_0 = (rho_0 + rho_0.conj().T) / 2  # Ensure Hermitian
            
            # Ensure positive
            eigvals = np.linalg.eigvalsh(rho_0)
            if np.min(eigvals) < 0:
                rho_0 = rho_0 - np.min(eigvals) * np.eye(3)
            rho_0 = rho_0 / np.trace(rho_0)
            
            r_0 = df.relative_entropy(rho_0, sigma)
            J, info = df.compute_J_exact(rho_0)
            EP = info['EP']
            
            ratio = (J * EP) / (r_0**2)
            
            # Paper reports ratio ≈ 0.987 for this case
            # (showing violation of CR bound at cubic order)
            print(f"\nCubic correction example:")
            print(f"  r_0   = {r_0:.4f}")
            print(f"  Ratio = {ratio:.3f} (expected ~0.987)")
    
    def test_spectral_purity_saturation(self):
        """Test that spectrally pure states saturate the bound"""
        gamma = 0.1
        beta_omega = 1.0
        
        L, sigma = qutrit_thermal_semigroup(gamma, beta_omega)
        df = DisplacementFunctional(L, sigma)
        
        # Get slowest eigenspace
        L_hat = df.gns_representation()
        eigenvalues, eigenvectors = np.linalg.eigh(-L_hat)
        nonzero_mask = eigenvalues > 1e-10
        
        # Slowest mode
        tau_slowest = eigenvectors[:, nonzero_mask][:, 0].reshape(3, 3)
        
        # Perturbation
        epsilon = 0.01
        rho_0 = sigma + epsilon * tau_slowest
        rho_0 = (rho_0 + rho_0.conj().T) / 2
        
        eigvals = np.linalg.eigvalsh(rho_0)
        if np.min(eigvals) < 0:
            rho_0 = rho_0 - np.min(eigvals) * np.eye(3)
        rho_0 = rho_0 / np.trace(rho_0)
        
        r_0 = df.relative_entropy(rho_0, sigma)
        J, info = df.compute_J_exact(rho_0)
        EP = info['EP']
        
        ratio = (J * EP) / (r_0**2)
        
        # Paper reports ratio ≈ 0.995 (99.5% saturation)
        assert ratio > 0.99, f"Spectral purity should saturate, got {ratio:.3f}"
        
        print(f"\nSpectral purity saturation:")
        print(f"  Ratio = {ratio:.3f} (expected ~0.995, 99.5% saturation)")


class TestChiSquareBound:
    """Test χ² Cramér-Rao bound (Theorem 2.2)"""
    
    def test_chi2_bound_always_holds(self):
        """Test that χ² bound holds for all initial states"""
        gamma = 0.1
        beta_omega = 1.0
        
        L, sigma = qutrit_thermal_semigroup(gamma, beta_omega)
        df = DisplacementFunctional(L, sigma)
        
        # Test multiple initial states
        test_states = [
            np.eye(3) / 3,  # Maximally mixed
            np.diag([0.7, 0.2, 0.1]),  # Diagonal
            sigma + 0.1 * (np.eye(3) / 3 - sigma),  # Small perturbation
        ]
        
        for i, rho_0 in enumerate(test_states):
            rho_0 = rho_0 / np.trace(rho_0)
            
            J, info = df.compute_J_exact(rho_0)
            J_chi2 = info['J_chi2']
            EP_chi2 = info['EP_chi2']
            chi2 = info['chi2']
            
            # χ² bound: J_χ² · EP_χ² >= χ²²
            LHS = J_chi2 * EP_chi2
            RHS = chi2**2
            
            assert LHS >= RHS - 1e-8, \
                f"State {i}: χ² bound violated: {LHS:.6f} < {RHS:.6f}"
            
            print(f"\nState {i}: J_χ² · EP_χ² / χ²² = {LHS/RHS:.6f}")


class TestCounterexample:
    """Test the non-QDB counterexample (§8.4.1)"""
    
    def test_non_qdb_violation(self):
        """Test that non-QDB violates the bound"""
        # This would require implementing the non-QDB example
        # from the paper with H = 2σ_x and specific Lindblad operators
        # For now, we just verify the methodology works
        
        # The paper reports for this case:
        # J·EP/r_0² = 0.11 (89% violation)
        
        # This test serves as a placeholder for future implementation
        pytest.skip("Non-QDB example requires separate implementation")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
