# ITSM CBR-001 — Rectangular \(T^3\) Casimir and free-field backreaction

**Version:** 1.0.0  
**Date:** 2026-08-02  
**Git:** `a57ed29` on `recovery/v12-core-architecture`  
**License:** CC-BY-4.0 (data/docs); code under repository LICENSE  

## Claim boundary

Validated: lattice Casimir energy density and directional pressures; biaxial
shape scan; free-field biaxial backreaction; Stage-3B search finds **no**
free-field \(H_t/H_p=13/12\) attractor (transient only).

**Not claimed:** parameter-free \(H_0=72.97\), geometric \(a_0\), completed
cosmology, or driven anisotropy (CBR-002 open).

## Reproduce

```powershell
conda activate itsm_env
cd Analysis/Casimir/CBR-001
python casimir_t3_lattice.py
python cbr001_stage2_standalone.py
python cbr001_stage3_backreaction.py
python cbr001_stage3b_ratio_test.py
```

## Repository

https://github.com/brendohxd/ITSM-Integrated-Toroidal-Syntropic-Model
