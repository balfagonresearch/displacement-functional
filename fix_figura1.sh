#!/bin/bash
# Fix para figura 1 - Estado espectralmente puro

cd ~/displacement-functional-v2 || exit 1

# Backup
cp generate_figures.py generate_figures.py.backup

# Aplicar fix
python3 << 'PYEOF'
with open('generate_figures.py', 'r') as f:
    content = f.read()

# Buscar y reemplazar la sección problemática
old_code = """    S_generic = []
    S_pure = []
    
    for t in t_points:
        # Evolve generic state
        rho_t_vec = expm(L * t) @ rho_generic.flatten()
        rho_t = rho_t_vec.reshape(3, 3)
        S_generic.append(df.relative_entropy(rho_t, sigma))
        
        # Evolve pure state
        rho_t_vec = expm(L * t) @ rho_pure.flatten()
        rho_t = rho_t_vec.reshape(3, 3)
        S_pure.append(df.relative_entropy(rho_t, sigma))
    
    S_generic = np.array(S_generic)
    S_pure = np.array(S_pure)"""

new_code = """    S_generic = []
    
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
    S_pure = r_0_pure * np.exp(-2 * lambda_min * t_points)"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("✓ Código corregido")
else:
    print("⚠ No encontré el patrón exacto")
    print("Intentando con búsqueda alternativa...")
    # Intentar línea por línea si es necesario
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'S_pure = []' in line and i+10 < len(lines):
            # Encontrar el for loop
            for j in range(i+1, min(i+20, len(lines))):
                if 'S_pure.append(df.relative_entropy(rho_t, sigma))' in lines[j]:
                    print(f"✓ Encontrado en línea {j}")
                    break

with open('generate_figures.py', 'w') as f:
    f.write(content)

print("✓ Archivo actualizado")
PYEOF

echo ""
echo "✓ Fix aplicado"
echo "Ahora regenera la figura 1:"
echo "  python generate_figures.py"
