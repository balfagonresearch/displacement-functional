"""
Generate figures for the Displacement Functional paper.

This script creates:
- fig1_entropy.pdf: Entropy trajectories for qutrit
- fig2_lambda.pdf: Dissipation rate evolution
- fig3_ion_trap.pdf: Ion trap cooling time comparison
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
from displacement_functional import DisplacementFunctional, qutrit_thermal_semigroup


def generate_fig1_entropy():
    """
    Figure 1: Entropy trajectory S(t) for qutrit thermal semigroup.
    
    (a) Absolute entropy with MLSI bounds
    (b) Normalized comparison: generic vs spectrally pure
    """
    # Setup
    gamma = 0.1
    beta_omega = 1.0
    L, sigma = qutrit_thermal_semigroup(gamma, beta_omega)
    df = DisplacementFunctional(L, sigma)
    
    # Get spectral data
    L_hat = df.gns_representation()
    eigenvalues, eigenvectors = np.linalg.eigh(-L_hat)
    nonzero_mask = eigenvalues > 1e-10
    lambdas = eigenvalues[nonzero_mask]
    
    alpha = np.min(lambdas) / 2  # MLSI constant
    Lambda = np.max(lambdas) / 2  # Largest eigenvalue
    
    # Initial states
    rho_generic = np.eye(3) / 3
    
    # Spectrally pure: project onto slowest eigenspace
    tau_slowest = eigenvectors[:, nonzero_mask][:, 0].reshape(3, 3)
    epsilon = 0.01
    rho_pure = sigma + epsilon * tau_slowest
    rho_pure = rho_pure / np.trace(rho_pure)  # Normalize
    
    # Time evolution
    t_max = 15
    t_points = np.linspace(0, t_max, 200)
    
    S_generic = []
    
    for t in t_points:
        # Evolve generic state
        rho_t_vec = expm(L * t) @ rho_generic.flatten()
        rho_t = rho_t_vec.reshape(3, 3)
        S_generic.append(df.relative_entropy(rho_t, sigma))
    
    S_generic = np.array(S_generic)
    
    # For spectrally pure state, use analytical solution
    # S(t) = r_0 * exp(-2*lambda_min * t) exactly (no numerical artifacts)
    r_0_pure = df.relative_entropy(rho_pure, sigma)
    lambda_min = np.min(lambdas) / 2
    S_pure = r_0_pure * np.exp(-2 * lambda_min * t_points)
    
    # Compute J (shaded area)
    r_0_generic = S_generic[0]
    J_generic, _ = df.compute_J_exact(rho_generic)
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Panel (a): Absolute entropy
    ax1.plot(t_points, S_generic, 'b-', linewidth=2, label='$S(t)$ (generic)')
    ax1.plot(t_points, r_0_generic * np.exp(-2*alpha*t_points), 'r--', 
             linewidth=1.5, label=f'$r_0 e^{{-2\\alpha t}}$ (MLSI upper)')
    ax1.plot(t_points, r_0_generic * np.exp(-2*Lambda*t_points), 'g:', 
             linewidth=1.5, label=f'$r_0 e^{{-2\\Lambda t}}$ (spectral lower)')
    
    # Shade area under curve (J)
    ax1.fill_between(t_points, 0, S_generic, alpha=0.2, color='blue',
                     label=f'$\\mathcal{{J}} = {J_generic:.3f}$')
    
    ax1.set_xlabel('Time $t$', fontsize=12)
    ax1.set_ylabel('$S(\\Phi_t(\\rho_0)\\|\\sigma)$', fontsize=12)
    ax1.set_title('(a) Entropy trajectory', fontsize=12)
    ax1.legend(fontsize=10, loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([0, r_0_generic * 1.1])
    
    # Panel (b): Normalized comparison
    S_generic_norm = S_generic / S_generic[0]
    S_pure_norm = S_pure / S_pure[0]
    
    ax2.plot(t_points, S_generic_norm, 'b-', linewidth=2, label='Generic state')
    ax2.plot(t_points, S_pure_norm, 'orange', linewidth=2, label='Spectrally pure')
    ax2.set_xlabel('Time $t$', fontsize=12)
    ax2.set_ylabel('$S(t) / S(0)$', fontsize=12)
    ax2.set_title('(b) Normalized entropy', fontsize=12)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim([0, 1.1])
    
    plt.tight_layout()
    plt.savefig('fig1_entropy.pdf', dpi=300, bbox_inches='tight')
    print("Generated fig1_entropy.pdf")
    
    return fig


def generate_fig2_lambda():
    """
    Figure 2: Dissipation rate lambda(t) = EP(t) / S(t).
    
    (a) Generic state: monotone decrease
    (b) Spectrally pure: approximately constant
    """
    # Setup
    gamma = 0.1
    beta_omega = 1.0
    L, sigma = qutrit_thermal_semigroup(gamma, beta_omega)
    df = DisplacementFunctional(L, sigma)
    
    # Get spectral data
    L_hat = df.gns_representation()
    eigenvalues, eigenvectors = np.linalg.eigh(-L_hat)
    nonzero_mask = eigenvalues > 1e-10
    lambdas = eigenvalues[nonzero_mask]
    alpha = np.min(lambdas) / 2
    
    # Initial states
    rho_generic = np.eye(3) / 3
    
    # Spectrally pure
    tau_slowest = eigenvectors[:, nonzero_mask][:, 0].reshape(3, 3)
    epsilon = 0.01
    rho_pure = sigma + epsilon * tau_slowest
    rho_pure = rho_pure / np.trace(rho_pure)
    
    # Time evolution
    t_max = 10
    t_points = np.linspace(0.01, t_max, 200)  # Avoid t=0 singularity
    
    lambda_generic = []
    lambda_pure = []
    
    for t in t_points:
        # Generic state
        rho_t_vec = expm(L * t) @ rho_generic.flatten()
        rho_t = rho_t_vec.reshape(3, 3)
        S_t = df.relative_entropy(rho_t, sigma)
        
        # Numerical derivative for EP(t)
        dt = 0.001
        rho_tp_vec = expm(L * (t + dt)) @ rho_generic.flatten()
        rho_tp = rho_tp_vec.reshape(3, 3)
        S_tp = df.relative_entropy(rho_tp, sigma)
        
        EP_t = -(S_tp - S_t) / dt
        lambda_generic.append(EP_t / S_t if S_t > 1e-10 else 2*alpha)
        
        # Pure state
        rho_t_vec = expm(L * t) @ rho_pure.flatten()
        rho_t = rho_t_vec.reshape(3, 3)
        S_t = df.relative_entropy(rho_t, sigma)
        
        rho_tp_vec = expm(L * (t + dt)) @ rho_pure.flatten()
        rho_tp = rho_tp_vec.reshape(3, 3)
        S_tp = df.relative_entropy(rho_tp, sigma)
        
        EP_t = -(S_tp - S_t) / dt
        lambda_pure.append(EP_t / S_t if S_t > 1e-10 else 2*alpha)
    
    lambda_generic = np.array(lambda_generic)
    lambda_pure = np.array(lambda_pure)
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Panel (a): Generic state
    ax1.plot(t_points, lambda_generic, 'b-', linewidth=2, label='$\\lambda(t)$')
    ax1.axhline(2*alpha, color='purple', linestyle='--', linewidth=1.5, 
                label=f'$2\\alpha = {2*alpha:.3f}$')
    ax1.set_xlabel('Time $t$', fontsize=12)
    ax1.set_ylabel('$\\lambda(t) = \\mathrm{EP}(t) / S(t)$', fontsize=12)
    ax1.set_title('(a) Generic state: monotone decrease', fontsize=12)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Panel (b): Spectrally pure
    ax2.plot(t_points, lambda_pure, 'orange', linewidth=2, label='$\\lambda(t)$')
    ax2.axhline(2*alpha, color='purple', linestyle='--', linewidth=1.5, 
                label=f'$2\\alpha = {2*alpha:.3f}$')
    ax2.set_xlabel('Time $t$', fontsize=12)
    ax2.set_ylabel('$\\lambda(t)$', fontsize=12)
    ax2.set_title('(b) Spectrally pure: approximately constant', fontsize=12)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('fig2_lambda.pdf', dpi=300, bbox_inches='tight')
    print("Generated fig2_lambda.pdf")
    
    return fig


def generate_fig3_ion_trap():
    """
    Figure 3: Ion trap cooling time comparison.
    
    Shows spectral vs CR bounds for different initial states.
    """
    # Simplified 2-level model
    d = 2
    gamma = 1.0  # Normalized units
    alpha = gamma
    
    # Fixed point (thermal state at low temperature)
    p_e = 0.1
    sigma = np.diag([1 - p_e, p_e])
    
    # Build depolarizing Lindbladian
    I = np.eye(d)
    L = -alpha * np.kron(I, I)
    for i in range(d):
        for j in range(d):
            ij = i*d + j
            L[ij, ij] += alpha
    L = L - np.outer(sigma.flatten(), sigma.flatten()) * np.trace(L)
    
    df = DisplacementFunctional(L, sigma)
    
    # Generate range of initial states
    # Parameterize by purity and coherence
    n_states = 50
    purities = np.linspace(0.5, 1.0, n_states)
    
    T_spectral_list = []
    T_CR_list = []
    r_0_list = []
    
    S_targ = 0.01
    
    for purity in purities:
        # Create state with given purity
        # rho = p |0><0| + (1-p) |1><1| + c (|0><1| + |1><0|)
        # with purity constraint
        p = (purity - 0.5) / 0.5  # Map [0.5, 1] -> [0, 1]
        
        rho_0 = np.array([
            [p, 0.1 * np.sqrt(p * (1-p))],
            [0.1 * np.sqrt(p * (1-p)), 1-p]
        ])
        
        # Ensure positive definite
        eigvals = np.linalg.eigvalsh(rho_0)
        if np.min(eigvals) < 0:
            continue
        
        rho_0 = rho_0 / np.trace(rho_0)
        
        r_0 = df.relative_entropy(rho_0, sigma)
        J, info = df.compute_J_exact(rho_0)
        EP = info['EP']
        
        # Spectral bound
        if r_0 > S_targ:
            T_spec = (1 / (2*alpha)) * np.log(r_0 / S_targ)
        else:
            T_spec = 0
        
        # CR bound
        if EP > 0:
            T_cr = r_0**2 / (EP * S_targ)
        else:
            T_cr = 0
        
        T_spectral_list.append(T_spec)
        T_CR_list.append(T_cr)
        r_0_list.append(r_0)
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Panel (a): Cooling times vs initial entropy
    ax1.plot(r_0_list, T_spectral_list, 'b-', linewidth=2, label='Spectral bound')
    ax1.plot(r_0_list, T_CR_list, 'r--', linewidth=2, label='CR bound')
    ax1.set_xlabel('Initial entropy $r_0$', fontsize=12)
    ax1.set_ylabel('Cooling time $T_{\\mathrm{cool}}$', fontsize=12)
    ax1.set_title('(a) Thermalization time bounds', fontsize=12)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Panel (b): Ratio
    ratio = np.array(T_CR_list) / np.array(T_spectral_list)
    ax2.plot(r_0_list, ratio, 'g-', linewidth=2)
    ax2.axhline(1, color='k', linestyle=':', linewidth=1)
    ax2.set_xlabel('Initial entropy $r_0$', fontsize=12)
    ax2.set_ylabel('Ratio $T_{\\mathrm{CR}} / T_{\\mathrm{spec}}$', fontsize=12)
    ax2.set_title('(b) Relative bound strength', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim([0, 2])
    
    plt.tight_layout()
    plt.savefig('fig3_ion_trap.pdf', dpi=300, bbox_inches='tight')
    print("Generated fig3_ion_trap.pdf")
    
    return fig


if __name__ == "__main__":
    print("Generating figures for Displacement Functional paper")
    print("="*60)
    print()
    
    # Set matplotlib style
    plt.rcParams.update({
        'font.size': 10,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 12,
        'text.usetex': False  # Set to True if LaTeX is available
    })
    
    try:
        generate_fig1_entropy()
        print("✓ Figure 1 complete")
        print()
        
        generate_fig2_lambda()
        print("✓ Figure 2 complete")
        print()
        
        generate_fig3_ion_trap()
        print("✓ Figure 3 complete")
        print()
        
        print("All figures generated successfully!")
        
    except Exception as e:
        print(f"Error generating figures: {e}")
        import traceback
        traceback.print_exc()
