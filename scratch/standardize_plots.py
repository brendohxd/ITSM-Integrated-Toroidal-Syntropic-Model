import os
import re

directories = [
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Scripts")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Analysis"))
]

skip_files = ['itsm_plot_style.py', 'itsm_3d_fluid_dynamics_web.py']

def standardize_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove hardcoded rcParams blocks
    # This regex matches plt.rcParams.update({ ... }) even across multiple lines
    content_new = re.sub(r'plt\.rcParams\.update\(\{.*?\}\)', '', content, flags=re.DOTALL)
    
    # 2. Inject the import and function call if not already there, right after matplotlib import
    if 'from itsm_plot_style import apply_tier1_style' not in content_new and 'import matplotlib.pyplot as plt' in content_new:
        replacement = "import matplotlib.pyplot as plt\nimport sys\nimport os\nsys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Scripts')))\nfrom itsm_plot_style import apply_tier1_style\napply_tier1_style()"
        content_new = content_new.replace('import matplotlib.pyplot as plt', replacement, 1)

    # 3. Strip \textbf{} from titles
    # Example: plt.title(r'\textbf{My Title}', ...) -> plt.title(r'My Title', ...)
    content_new = re.sub(r'\\textbf\{([^}]+)\}', r'\1', content_new)
    
    # Also strip any specific hardcoded fontsize overrides in plt.title or plt.xlabel so the engine handles it
    # We will just leave them alone to be safe, but removing \textbf{} solves the visual issue.
    
    if content != content_new:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content_new)
        print(f"Updated: {filepath}")

for d in directories:
    for root, dirs, files in os.walk(d):
        if 'Archive' in root:
            continue
        for file in files:
            if file.endswith('.py') and file not in skip_files:
                filepath = os.path.join(root, file)
                standardize_file(filepath)

print("Standardization sweep complete.")
