#!/usr/bin/env python3
"""Fix the relative_entropy function in displacement_functional.py"""

import re

# Lee el archivo
with open('displacement_functional.py', 'r') as f:
    content = f.read()

# Patrón para encontrar la función problemática
old_pattern = r'''        # Reconstruct with positive eigenvalues only
        log_rho = eigvecs_rho @ np\.diag\(np\.log\(eigvals_rho\)\) @ eigvecs_rho\.conj\(\)\.T
        log_sigma = eigvecs_sigma @ np\.diag\(np\.log\(eigvals_sigma\)\) @ eigvecs_sigma\.conj\(\)\.T'''

# Código nuevo que maneja el caso escalar
new_code = '''        # Reconstruct with positive eigenvalues only
        # Handle potential scalar/1D cases
        d = rho.shape[0]
        if d == 1:
            log_rho = np.log(rho)
            log_sigma = np.log(sigma)
        else:
            log_rho = eigvecs_rho @ np.diag(np.log(eigvals_rho)) @ eigvecs_rho.conj().T
            log_sigma = eigvecs_sigma @ np.diag(np.log(eigvals_sigma)) @ eigvecs_sigma.conj().T'''

# Reemplaza
if re.search(old_pattern, content):
    content = re.sub(old_pattern, new_code, content)
    print("✓ Encontrado y corregido el patrón")
else:
    print("⚠ No encontré el patrón exacto, intentando búsqueda alternativa...")
    # Buscar de forma más simple
    if "log_rho = eigvecs_rho @ np.diag(np.log(eigvals_rho)) @ eigvecs_rho.conj().T" in content:
        content = content.replace(
            "        # Reconstruct with positive eigenvalues only\n        log_rho = eigvecs_rho @ np.diag(np.log(eigvals_rho)) @ eigvecs_rho.conj().T\n        log_sigma = eigvecs_sigma @ np.diag(np.log(eigvals_sigma)) @ eigvecs_sigma.conj().T",
            new_code
        )
        print("✓ Corregido con método alternativo")

# Guarda el archivo
with open('displacement_functional.py', 'w') as f:
    f.write(content)

print("✓ Archivo displacement_functional.py actualizado")
print("\nAhora ejecuta: python generate_figures.py")
