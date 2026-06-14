import os
import shutil
import sys

def generate_rotation_curve_expanded():
    """
    The 'ITSM_Rotation_Curve_Expanded.png' figure used in the manuscript is
    the rotation curve for the flagship galaxy NGC 5055.
    
    This figure is automatically generated during the 175-galaxy batch run 
    by `itsm_mcmc_multicore.py` and saved to `Assets/SPARC_Batch_Outputs/NGC5055_rc.png`.
    
    This script simply copies that generated figure into the `Assets/Figures/` 
    directory with the publication-ready filename so that it is explicitly 
    available for the LaTeX compiler without manual renaming.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_file = os.path.join(script_dir, "..", "Assets", "SPARC_Batch_Outputs", "NGC5055_rc.png")
    dest_file = os.path.join(script_dir, "..", "Assets", "Figures", "ITSM_Rotation_Curve_Expanded.png")
    
    if not os.path.exists(source_file):
        print(f"Notice: Source file {source_file} not found.")
        print("This is normal if you haven't run the full `itsm_mcmc_multicore.py` batch yet.")
        print(f"The original publication figure is already located at: {dest_file}")
        return
        
    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
    shutil.copy2(source_file, dest_file)
    print(f"[PLOT] Successfully copied NGC 5055 rotation curve to:")
    print(f"       {dest_file}")

if __name__ == "__main__":
    generate_rotation_curve_expanded()
