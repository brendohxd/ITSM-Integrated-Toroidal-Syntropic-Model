import os, glob

header_camb = """\"\"\"
Software Dependencies & Attributions:
This script utilizes a modified version of the CAMB Boltzmann solver.
Original Source: Lewis, A., Challinor, A., & Lasenby, A. (2000). Efficient computation of CMB anisotropies in closed FRW models. The Astrophysical Journal, 538(2), 473.
\"\"\"
"""

header_emcee = """\"\"\"
Software Dependencies & Attributions:
This script utilizes the emcee (The MCMC Hammer) and corner.py packages for Bayesian inference and visualization.
- emcee: Foreman-Mackey, D., Hogg, D. W., Lang, D., & Goodman, J. (2013). Publications of the Astronomical Society of the Pacific, 125(925), 306.
- corner.py: Foreman-Mackey, D. (2016). The Journal of Open Source Software, 1(2), 24.
\"\"\"
"""

for file in glob.glob('Scripts/**/*.py', recursive=True):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already attributed to avoid duplication
    if 'Software Dependencies & Attributions' in content:
        continue

    needs_camb = 'import camb' in content
    needs_emcee = 'import emcee' in content

    if needs_camb and needs_emcee:
        header = header_camb.strip() + '\n' + header_emcee.replace('\"\"\"\nSoftware Dependencies & Attributions:\n', '') + '\n\n'
    elif needs_camb:
        header = header_camb + '\n'
    elif needs_emcee:
        header = header_emcee + '\n'
    else:
        continue

    # Insert header after the shebang or at the top
    if content.startswith('#!'):
        lines = content.split('\n')
        new_content = lines[0] + '\n' + header + '\n'.join(lines[1:])
    else:
        new_content = header + content
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'Added attributions to {file}')
