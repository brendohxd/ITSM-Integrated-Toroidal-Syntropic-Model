import os
import zipfile

VERSION = "v11.4.1"
ZIP_NAME = f"ITSM_Computational_Framework_{VERSION}.zip"

def create_framework_zip():
    print(f"[*] Packaging computational framework into {ZIP_NAME}...")
    dirs_to_zip = ["Scripts", "Data"]
    files_to_zip = ["environment.yml", "README.md", "CHANGELOG.md"]
    
    with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in files_to_zip:
            if os.path.exists(f):
                print(f"    - Adding {f}")
                zipf.write(f)
        for d in dirs_to_zip:
            if os.path.exists(d):
                for root, _, files in os.walk(d):
                    if "__pycache__" in root or "results" in root or "Archive" in root:
                        continue
                    for file in files:
                        file_path = os.path.join(root, file)
                        print(f"    - Adding {file_path}")
                        zipf.write(file_path)
    print(f"    [+] {ZIP_NAME} created successfully.")

if __name__ == "__main__":
    create_framework_zip()
