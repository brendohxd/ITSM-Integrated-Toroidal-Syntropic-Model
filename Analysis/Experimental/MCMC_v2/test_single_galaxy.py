"""
ITSM — Single Galaxy Multicore Test
Runs the MCMC pipeline on ONE galaxy (NGC7814) to verify multicore pattern works.
Staging: Analysis/Experimental/MCMC_v2/
"""
import os
import sys

# Add the MCMC_v2 directory to path so we can import the main module
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from itsm_mcmc_multicore import run_single_galaxy
from multiprocessing import cpu_count

if __name__ == "__main__":

    repo_root  = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
    data_dir   = os.path.join(repo_root, "SPARC_data")
    output_dir = os.path.join(script_dir, "results")
    os.makedirs(output_dir, exist_ok=True)

    # Use NGC7814 — well-sampled bulge-dominated galaxy, good test case
    test_galaxy = os.path.join(data_dir, "NGC7814_rotmod.dat")

    # Fallback: use first available file if NGC7814 not found
    if not os.path.exists(test_galaxy):
        import glob
        all_files = sorted(glob.glob(os.path.join(data_dir, "*_rotmod.dat")))
        if not all_files:
            raise FileNotFoundError(f"No SPARC files found in {data_dir}")
        test_galaxy = all_files[0]

    galaxy_name = os.path.basename(test_galaxy).replace("_rotmod.dat", "")

    print("=" * 60)
    print(f" ITSM MULTICORE TEST — Single Galaxy: {galaxy_name}")
    print(f" CPU cores available: {cpu_count()}")
    print(f" ITSM: g_eff = g_bar + (2/3)*sqrt(g_bar * a0)")
    print(f"       a0 = c*H0/(2*pi)  [geometrically derived]")
    print("=" * 60)
    print()

    # Reduced steps for quick test — same physics, fewer iterations
    N_WALKERS = 32
    N_STEPS   = 500   # reduced for speed test
    N_DISCARD = 100

    args = (test_galaxy, output_dir, N_WALKERS, N_STEPS, N_DISCARD)

    print(f"Running {N_WALKERS} walkers x {N_STEPS} steps on {galaxy_name}...")
    result = run_single_galaxy(args)
    print()
    print(result)
    print()
    print("Output files:")
    for f in os.listdir(output_dir):
        if galaxy_name in f:
            fpath = os.path.join(output_dir, f)
            print(f"  {f}  ({os.path.getsize(fpath):,} bytes)")
    print()
    if result.startswith("OK"):
        print("TEST PASSED — multicore pattern confirmed working.")
        print("Ready to run full 175-galaxy batch via itsm_mcmc_multicore.py")
    else:
        print("TEST FAILED — check error above.")
