import sys

# Lee el archivo
with open('displacement_functional.py', 'r') as f:
    content = f.read()

# Encuentra y reemplaza la función relative_entropy problemática
old_code = '''    @staticmethod
    def relative_entropy(rho, sigma):
        """
        Compute relative entropy S(rho||sigma) = Tr[rho(log rho - log sigma)]
        
        Args:
            rho: Density matrix
            sigma: Reference density matrix
            
        Returns:
            Relative entropy (non-negative)
        """
        # Eigendecomposition
        eigvals_rho, eigvecs_rho = np.linalg.eigh(rho)
        eigvals_sigma, eigvecs_sigma = np.linalg.eigh(sigma)
        
        # Filter out zero/negative eigenvalues
        mask_rho = eigvals_rho > 1e-15
        mask_sigma = eigvals_sigma > 1e-15
        
        # Reconstruct with positive eigenvalues only
        log_rho = eigvecs_rho @ np.diag(np.log(eigvals_rho)) @ eigvecs_rho.conj().T'''

new_code = '''    @staticmethod
    def relative_entropy(rho, sigma):
        """
        Compute relative entropy S(rho||sigma) = Tr[rho(log rho - log sigma)]
        
        Args:
            rho: Density matrix
            sigma: Reference density matrix
            
        Returns:
            Relative entropy (non-negative)
        """
        # Eigendecomposition
        eigvals_rho, eigvecs_rho = np.linalg.eigh(rho)
        eigvals_sigma, eigvecs_sigma = np.linalg.eigh(sigma)
        
        # Filter out zero/negative eigenvalues
        mask_rho = eigvals_rho > 1e-15
        mask_sigma = eigvals_sigma > 1e-15
        
        # Reconstruct with positive eigenvalues only
        if eigvals_rho.size == 1:
            log_rho = eigvecs_rho * np.log(eigvals_rho) * eigvecs_rho.conj().T
        else:
            log_rho = eigvecs_rho @ np.diag(np.log(eigvals_rho)) @ eigvecs_rho.conj().T'''

content = content.replace(old_code, new_code)

# Guarda el archivo corregido
with open('displacement_functional.py', 'w') as f:
    f.write(content)

print("✓ Fixed displacement_functional.py")
