import os
import glob

# Paths to process
scripts_dir = r"C:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Scripts"
py_files = glob.glob(os.path.join(scripts_dir, "**", "*.py"), recursive=True)

data_folders = ["SPARC_data", "DESI_data", "NANOGrav_data", "Planck_data"]

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # Common pattern 1: "..", "SPARC_data" -> "..", "Data", "SPARC_data"
    for folder in data_folders:
        content = content.replace(f'\"..\", \"{folder}\"', f'\"..\", \"Data\", \"{folder}\"')
        content = content.replace(f'\'..\', \'{folder}\'', f'\'..\', \'Data\', \'{folder}\'')
        
        # Common pattern 2: "SPARC_data" without ".." but in join
        # For example, os.path.join(repo_root, "SPARC_data")
        content = content.replace(f'repo_root, \"{folder}\"', f'repo_root, \"Data\", \"{folder}\"')
        content = content.replace(f'repo_root, \'{folder}\'', f'repo_root, \'Data\', \'{folder}\'')
        
        # Pattern 3: direct string "Planck_data" as first arg in os.path.join
        # os.path.join("Planck_data", ...) -> os.path.join("Data", "Planck_data", ...)
        content = content.replace(f'os.path.join(\"{folder}\"', f'os.path.join(\"Data\", \"{folder}\"')
        content = content.replace(f'os.path.join(\'{folder}\'', f'os.path.join(\'Data\', \'{folder}\'')
        
        # Pattern 4: in Archive\itsm_zenodo_release.py
        # ["Scripts", "SPARC_data", "DESI_data", "NANOGrav_data"] -> need to handle specially or just let it be if we want it to grab from Data/
        if "dirs_to_zip" in content and folder in content:
            content = content.replace(f'\"{folder}\"', f'\"Data/{folder}\"')

    if content != original_content:
        print(f"Updating: {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

for py_file in py_files:
    process_file(py_file)
