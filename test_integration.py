"""
Integration tests for displacement functional

Tests end-to-end workflows combining multiple components.
Run with: pytest test_integration.py -v
"""

import numpy as np
import pytest
import os
import subprocess
from displacement_functional import (
    DisplacementFunctional, 
    qutrit_thermal_semigroup,
    ion_trap_example
)


class TestEndToEndWorkflows:
    """Test complete workflows from start to finish"""
    
    def test_qutrit_full_workflow(self):
        """Test complete qutrit analysis workflow"""
        # Step 1: Create semigroup
        gamma = 0.1
        beta_omega = 1.0
        L, sigma = qutrit_thermal_semigroup(gamma, beta_omega)
        
        # Step 2: Initialize displacement functional
        df = DisplacementFunctional(L, sigma)
        
        # Step 3: Set initial state
        rho_0 = np.eye(3) / 3
        
        # Step 4: Compute all quantities
        r_0 = df.relative_entropy(rho_0, sigma)
        J, info = df.compute_J_exact(rho_0)
        EP = info['EP']
        chi2 = info['chi2']
        J_chi2 = info['J_chi2']
        EP_chi2 = info['EP_chi2']
        
        # Step 5: Verify relationships
        # MLSI bound
        L_hat = df.gns_representation()
        eigenvalues, _ = np.linalg.eigh(-L_hat)
        alpha = np.min(eigenvalues[eigenvalues > 1e-10]) / 2
        
        assert J <= r_0 / (2 * alpha) + 1e-8, "MLSI upper bound violated"
        
        # Chi^2 CR bound
        assert J_chi2 * EP_chi2 >= chi2**2 - 1e-8, "Chi^2 CR bound violated"
        
        # Consistency
        assert J >= 0, "J should be non-negative"
        assert EP >= 0, "EP should be non-negative"
        assert r_0 >= 0, "r_0 should be non-negative"
    
    def test_ion_trap_workflow(self):
        """Test ion trap example workflow"""
        # Should run without errors
        results = ion_trap_example()
        
        # Check structure
        assert 'plus' in results
        assert 'optimal' in results
        
        # Check values
        for state, res in results.items():
            assert 'r_0' in res
            assert 'J' in res
            assert 'EP' in res
            assert 'T_spectral' in res
            assert 'T_CR' in res
            assert 'ratio' in res
            
            # Physical constraints
            assert res['r_0'] >= 0
            assert res['J'] >= 0
            assert res['EP'] >= 0
            assert res['T_spectral'] >= 0
            assert res['T_CR'] >= 0
    
    def test_multiple_initial_states(self):
        """Test workflow with various initial states"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        
        # Test different types of initial states
        initial_states = [
            np.eye(3) / 3,  # Maximally mixed
            sigma + 0.1 * np.diag([1, -0.5, -0.5]),  # Diagonal perturbation
            sigma + 0.05 * np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]]),  # With coherences
        ]
        
        for i, rho_0 in enumerate(initial_states):
            # Ensure valid density matrix
            rho_0 = (rho_0 + rho_0.conj().T) / 2  # Make Hermitian
            eigvals = np.linalg.eigvalsh(rho_0)
            if np.min(eigvals) < 0:
                rho_0 = rho_0 - np.min(eigvals) * np.eye(3)
            rho_0 = rho_0 / np.trace(rho_0)  # Normalize
            
            # Compute J
            J, info = df.compute_J_exact(rho_0)
            
            # Basic checks
            assert J >= 0, f"State {i}: J should be non-negative"
            assert info['EP'] >= 0, f"State {i}: EP should be non-negative"
            assert info['chi2'] >= 0, f"State {i}: chi2 should be non-negative"


class TestConsistency:
    """Test consistency between different methods"""
    
    def test_J_vs_Jchi_relationship(self):
        """Test that J <= J_chi2"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        
        # Multiple initial states
        for epsilon in [0.01, 0.05, 0.1, 0.2]:
            rho_0 = sigma + epsilon * (np.eye(3) / 3 - sigma)
            rho_0 = rho_0 / np.trace(rho_0)
            
            J, info = df.compute_J_exact(rho_0)
            J_chi2 = info['J_chi2']
            
            # S <= chi^2, so J <= J_chi2
            assert J <= J_chi2 + 1e-8, f"J should be <= J_chi2 (epsilon={epsilon})"
    
    def test_eigenvalue_consistency(self):
        """Test that eigenvalues are consistent across methods"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        
        # Get eigenvalues via GNS
        L_hat = df.gns_representation()
        eigs_gns = np.linalg.eigvalsh(-L_hat)
        eigs_gns = eigs_gns[eigs_gns > 1e-10]
        
        # Get eigenvalues via direct computation
        rho_0 = np.eye(3) / 3
        _, info = df.compute_J_exact(rho_0)
        eigs_direct = info['eigenvalues']
        
        # Should match (up to ordering)
        eigs_gns_sorted = np.sort(eigs_gns)
        eigs_direct_sorted = np.sort(eigs_direct)
        
        assert np.allclose(eigs_gns_sorted, eigs_direct_sorted, atol=1e-10), \
            "Eigenvalues should match between methods"


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_near_equilibrium(self):
        """Test behavior very close to equilibrium"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        
        # Very small perturbation
        epsilon = 1e-8
        rho_0 = sigma + epsilon * (np.eye(3) / 3 - sigma)
        rho_0 = rho_0 / np.trace(rho_0)
        
        J, info = df.compute_J_exact(rho_0)
        r_0 = df.relative_entropy(rho_0, sigma)
        
        # Should scale quadratically
        assert J < 1e-6, "J should be very small near equilibrium"
        assert r_0 < 1e-6, "r_0 should be very small near equilibrium"
    
    def test_maximally_mixed(self):
        """Test with maximally mixed initial state"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        
        rho_0 = np.eye(3) / 3
        J, info = df.compute_J_exact(rho_0)
        
        # Should be well-defined
        assert np.isfinite(J), "J should be finite"
        assert J > 0, "J should be positive (non-equilibrium state)"
    
    def test_pure_state(self):
        """Test with pure initial state"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        
        # Pure state |0><0|
        rho_0 = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
        
        J, info = df.compute_J_exact(rho_0)
        
        # Should be well-defined
        assert np.isfinite(J), "J should be finite for pure state"
        assert J > 0, "J should be positive"


class TestNumericalStability:
    """Test numerical stability and robustness"""
    
    def test_different_gammas(self):
        """Test with various values of gamma"""
        gammas = [0.01, 0.1, 1.0, 10.0]
        
        for gamma in gammas:
            L, sigma = qutrit_thermal_semigroup(gamma=gamma, beta_omega=1.0)
            df = DisplacementFunctional(L, sigma)
            
            rho_0 = np.eye(3) / 3
            J, info = df.compute_J_exact(rho_0)
            
            assert np.isfinite(J), f"J should be finite for gamma={gamma}"
            assert J > 0, f"J should be positive for gamma={gamma}"
    
    def test_different_temperatures(self):
        """Test with various temperatures (beta_omega)"""
        beta_omegas = [0.1, 1.0, 10.0, 100.0]
        
        for beta_omega in beta_omegas:
            L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=beta_omega)
            df = DisplacementFunctional(L, sigma)
            
            rho_0 = np.eye(3) / 3
            J, info = df.compute_J_exact(rho_0)
            
            assert np.isfinite(J), f"J should be finite for beta_omega={beta_omega}"
            assert J > 0, f"J should be positive for beta_omega={beta_omega}"


class TestFileGeneration:
    """Test that scripts generate expected outputs"""
    
    def test_figure_generation(self, tmp_path):
        """Test that generate_figures.py creates files"""
        # Change to temporary directory
        import os
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            # Run figure generation
            result = subprocess.run(
                ['python', os.path.join(original_dir, 'generate_figures.py')],
                capture_output=True,
                timeout=60
            )
            
            # Check it ran successfully
            assert result.returncode == 0, "Figure generation failed"
            
            # Check files were created
            assert os.path.exists('fig1_entropy.pdf'), "fig1 not created"
            assert os.path.exists('fig2_lambda.pdf'), "fig2 not created"
            assert os.path.exists('fig3_ion_trap.pdf'), "fig3 not created"
            
        finally:
            os.chdir(original_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
