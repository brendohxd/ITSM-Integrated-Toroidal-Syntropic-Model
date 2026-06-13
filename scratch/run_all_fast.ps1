conda activate itsm_env
$scripts = @(
    "Scripts/itsm_3d_fluid_dynamics.py",
    "Scripts/itsm_bootstrapped_rar.py",
    "Scripts/itsm_btfr_validation.py",
    "Scripts/itsm_bullet_cluster.py",
    "Scripts/itsm_bullet_phasespace.py",
    "Scripts/itsm_camb_cmb_spectrum.py",
    "Scripts/itsm_camb_matter_power.py",
    "Scripts/itsm_causality_cones.py",
    "Scripts/itsm_desi_bao.py",
    "Scripts/itsm_desi_bao_empirical_validator.py",
    "Scripts/itsm_drag_saturation.py",
    "Scripts/itsm_global_rar.py",
    "Scripts/itsm_hubble_resolver.py",
    "Scripts/itsm_n_redshift_evolution_diagnostic.py",
    "Scripts/itsm_nanograv_resonance.py",
    "Scripts/itsm_ngc4217_dust_model.py",
    "Scripts/itsm_pantheon_sn1a.py",
    "Scripts/itsm_thermodynamic_decoupling.py",
    "Scripts/itsm_z14_assembly.py"
)

foreach ($s in $scripts) {
    Write-Host "Running $s..."
    python $s
}
Write-Host "All fast plotting scripts finished."
