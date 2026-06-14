"""
Master orchestration script to execute the entire ITSM analysis pipeline sequentially.
Runs all necessary scripts to reproduce the repository's results from scratch.
"""
import os
import subprocess
import glob
import time

def run_all_scripts():
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    # All analysis scripts start with itsm_
    # We will exclude itsm_plot_style.py and run_all.py
    scripts = sorted(glob.glob(os.path.join(scripts_dir, "itsm_*.py")))
    
    # Filter out non-execution scripts
    scripts = [s for s in scripts if not s.endswith("itsm_plot_style.py") and not s.endswith("run_all.py")]
    
    print("="*60)
    print(" ITSM Master Execution Pipeline")
    print("="*60)
    print(f" Found {len(scripts)} production scripts to execute.")
    
    success_count = 0
    fail_count = 0
    
    start_time = time.time()
    
    for script in scripts:
        basename = os.path.basename(script)
        print(f"\n[RUNNING] {basename} ...")
        # Run using the same python interpreter
        result = subprocess.run(["python", script], cwd=scripts_dir, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[SUCCESS] {basename}")
            success_count += 1
        else:
            print(f"[FAILED] {basename} with exit code {result.returncode}")
            print(result.stderr)
            fail_count += 1
            
    total_time = time.time() - start_time
    print("="*60)
    print(f" Pipeline completed in {total_time:.1f} seconds.")
    print(f" Success: {success_count} | Failed: {fail_count}")
    print("="*60)

if __name__ == "__main__":
    run_all_scripts()
