"""
Performance tests for displacement functional

Tests computational performance and scaling.
Run with: pytest test_performance.py -v
"""

import numpy as np
import pytest
import time
from displacement_functional import DisplacementFunctional, qutrit_thermal_semigroup


class TestComputationalPerformance:
    """Test computational efficiency"""
    
    def test_qutrit_performance(self):
        """Test that qutrit computation is reasonably fast"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        rho_0 = np.eye(3) / 3
        
        # Warm-up
        J, info = df.compute_J_exact(rho_0)
        
        # Benchmark
        times = []
        for _ in range(10):
            start = time.perf_counter()
            J, info = df.compute_J_exact(rho_0)
            end = time.perf_counter()
            times.append(end - start)
        
        mean_time = np.mean(times)
        
        # Should complete in reasonable time (< 100ms on modern hardware)
        assert mean_time < 0.1, f"Computation too slow: {mean_time*1000:.2f} ms"
        
        print(f"\nQutrit computation: {mean_time*1000:.2f} ms (mean of 10 runs)")
    
    def test_gns_representation_performance(self):
        """Test GNS representation computation speed"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        
        # Warm-up
        L_hat = df.gns_representation()
        
        # Benchmark
        times = []
        for _ in range(20):
            start = time.perf_counter()
            L_hat = df.gns_representation()
            end = time.perf_counter()
            times.append(end - start)
        
        mean_time = np.mean(times)
        
        # GNS should be fast (< 10ms)
        assert mean_time < 0.01, f"GNS computation too slow: {mean_time*1000:.2f} ms"
        
        print(f"\nGNS representation: {mean_time*1000:.2f} ms (mean of 20 runs)")
    
    def test_relative_entropy_performance(self):
        """Test relative entropy computation speed"""
        rho = np.diag([0.5, 0.3, 0.2])
        sigma = np.diag([0.4, 0.3, 0.3])
        
        # Warm-up
        S = DisplacementFunctional.relative_entropy(rho, sigma)
        
        # Benchmark
        times = []
        for _ in range(100):
            start = time.perf_counter()
            S = DisplacementFunctional.relative_entropy(rho, sigma)
            end = time.perf_counter()
            times.append(end - start)
        
        mean_time = np.mean(times)
        
        # Should be very fast (< 1ms)
        assert mean_time < 0.001, f"Relative entropy too slow: {mean_time*1000:.2f} ms"
        
        print(f"\nRelative entropy: {mean_time*1000:.2f} ms (mean of 100 runs)")


class TestScaling:
    """Test how performance scales with dimension"""
    
    def test_dimension_scaling(self):
        """Test scaling with Hilbert space dimension"""
        dimensions = [2, 3, 5]
        times = []
        
        for d in dimensions:
            # Create simple depolarizing channel
            L = -np.eye(d**2)
            for i in range(d**2):
                L[i, i] = 1 - 1/d**2
            
            sigma = np.eye(d) / d
            df = DisplacementFunctional(L, sigma)
            
            rho_0 = np.eye(d) / d + 0.1 * (np.ones((d, d)) / d**2)
            rho_0 = rho_0 / np.trace(rho_0)
            
            # Benchmark
            run_times = []
            for _ in range(5):
                start = time.perf_counter()
                J, info = df.compute_J_exact(rho_0)
                end = time.perf_counter()
                run_times.append(end - start)
            
            mean_time = np.mean(run_times)
            times.append(mean_time)
            
            print(f"\nd={d}: {mean_time*1000:.2f} ms")
        
        # Should scale roughly as O(d^6) but still be reasonable
        # d=2->3 should be slower but not by huge factor
        assert times[1] < times[0] * 50, "Scaling d=2->3 unreasonable"
        assert times[2] < times[1] * 50, "Scaling d=3->5 unreasonable"
    
    def test_memory_efficiency(self):
        """Test that memory usage is reasonable"""
        import sys
        
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        
        # Size of Lindbladian
        L_size = sys.getsizeof(L)
        
        # Should be reasonable (< 10 KB for 3x3 system)
        assert L_size < 10000, f"Lindbladian too large: {L_size} bytes"
        
        print(f"\nLindbladian size: {L_size} bytes")


class TestCaching:
    """Test that repeated computations are efficient"""
    
    def test_repeated_computation(self):
        """Test that repeated calls don't slow down"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        rho_0 = np.eye(3) / 3
        
        times = []
        for i in range(20):
            start = time.perf_counter()
            J, info = df.compute_J_exact(rho_0)
            end = time.perf_counter()
            times.append(end - start)
        
        # First call might be slower (Python JIT, etc.)
        # But should stabilize
        first_half = np.mean(times[:10])
        second_half = np.mean(times[10:])
        
        # Second half shouldn't be significantly slower
        assert second_half < first_half * 1.5, "Performance degradation detected"
        
        print(f"\nFirst 10 calls: {first_half*1000:.2f} ms")
        print(f"Last 10 calls:  {second_half*1000:.2f} ms")


class TestNumericalPrecision:
    """Test numerical precision and stability"""
    
    def test_precision_consistency(self):
        """Test that results are consistent across runs"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        rho_0 = np.eye(3) / 3
        
        # Run multiple times
        results = []
        for _ in range(10):
            J, info = df.compute_J_exact(rho_0)
            results.append(J)
        
        # Should get exactly the same answer every time
        assert np.std(results) < 1e-12, "Results not consistent"
        
        print(f"\nJ = {np.mean(results):.15f} ± {np.std(results):.2e}")
    
    def test_numerical_stability_extreme_values(self):
        """Test stability with extreme parameter values"""
        # Very small gamma
        L, sigma = qutrit_thermal_semigroup(gamma=1e-6, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        rho_0 = np.eye(3) / 3
        J, info = df.compute_J_exact(rho_0)
        
        assert np.isfinite(J), "J not finite for small gamma"
        assert J > 0, "J not positive for small gamma"
        
        # Very large gamma
        L, sigma = qutrit_thermal_semigroup(gamma=100.0, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        J, info = df.compute_J_exact(rho_0)
        
        assert np.isfinite(J), "J not finite for large gamma"
        assert J > 0, "J not positive for large gamma"
        
        print(f"\nSmall gamma (1e-6): J = {J:.6e}")
        
        L, sigma = qutrit_thermal_semigroup(gamma=100.0, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        J, info = df.compute_J_exact(rho_0)
        
        print(f"Large gamma (100):  J = {J:.6e}")


@pytest.mark.slow
class TestLongRunning:
    """Tests that take longer to run"""
    
    def test_extended_benchmark(self):
        """Extended benchmark with more iterations"""
        L, sigma = qutrit_thermal_semigroup(gamma=0.1, beta_omega=1.0)
        df = DisplacementFunctional(L, sigma)
        rho_0 = np.eye(3) / 3
        
        # Warm-up
        for _ in range(10):
            J, info = df.compute_J_exact(rho_0)
        
        # Extended benchmark
        times = []
        for _ in range(100):
            start = time.perf_counter()
            J, info = df.compute_J_exact(rho_0)
            end = time.perf_counter()
            times.append(end - start)
        
        mean_time = np.mean(times)
        std_time = np.std(times)
        min_time = np.min(times)
        max_time = np.max(times)
        
        print(f"\nExtended benchmark (100 runs):")
        print(f"  Mean: {mean_time*1000:.2f} ms")
        print(f"  Std:  {std_time*1000:.2f} ms")
        print(f"  Min:  {min_time*1000:.2f} ms")
        print(f"  Max:  {max_time*1000:.2f} ms")
        
        # Variance should be reasonable
        assert std_time < mean_time * 0.5, "High variance in computation time"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
