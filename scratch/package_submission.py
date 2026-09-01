import os
import zipfile
import glob

def create_submission_zip():
    zip_filename = 'JCAP_Submission.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add Manuscript files
        for file in ['Manuscript/Main.tex', 'Manuscript/Main.bbl', 'Manuscript/references.bib', 'Manuscript/Main.pdf', 'Manuscript/CoverLetter_JCAP.tex', 'Manuscript/CoverLetter_JCAP.pdf']:
            if os.path.exists(file):
                zipf.write(file)
                print(f"Added {file}")
            else:
                print(f"Warning: {file} not found!")

        # Add Figures
        figure_files = glob.glob('Assets/Figures/*.*')
        for file in figure_files:
            zipf.write(file)
            print(f"Added {file}")

    print(f"\nSuccessfully created {zip_filename} with {len(zipf.namelist())} files.")

if __name__ == "__main__":
    create_submission_zip()
