"""Bounded raw-table replay of arXiv:2608.08945v1 anchors.

This is an empirical RAR methods control, not an ITSM prediction or MCMC.
No archived Python is executed and no pickled numpy arrays are loaded.
Inputs stay under the ignored local evidence directory. Outputs are new files.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import scipy
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / ".local/itsm-context/sparc-identifiability-20261007"
SOURCE = BASE / "inspection"
OUT = BASE / "parent_anchor_replay_v2"
PINNED = {
    "data/SPARC_Lelli2016c.mrt": "5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243",
    "data/MassModels_Lelli2016c.mrt": "9108994b12cc401b94a1768beca61c53ec354779385c9c9cc571049f3043244c",
    "results/bh_family_table.csv": "e07c43a0e155011fd725bd90f23eaa53b73aefc913ce2779efeaafc02ef3bf07",
}
KPC_M = 3.0856775814913673e19
G_PC_KMS2_MSUN = 4.30091e-3
C_KMS = 299792.458
A0_EMPIRICAL = 1.2e-10


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def data_lines(path):
    lines = path.read_text(encoding="ascii").splitlines()
    last_separator = max(i for i, line in enumerate(lines) if line.strip() and set(line.strip()) == {"-"})
    return [line for line in lines[last_separator + 1:] if line.strip()]


def parse_sources():
    """Use the documented column order; archived whitespace is not byte-aligned."""
    galaxies = {}
    for line in data_lines(SOURCE / "data/SPARC_Lelli2016c.mrt"):
        columns = line.split()
        if len(columns) != 19:
            raise ValueError(f"Unexpected galaxy column count: {len(columns)}")
        name = columns[0]
        if name in galaxies:
            raise ValueError(f"Duplicate galaxy: {name}")
        galaxies[name] = {
            "D": float(columns[2]), "eD": float(columns[3]),
            "inc": float(columns[5]), "einc": float(columns[6]),
            "L36": float(columns[7]), "Reff": float(columns[9]),
            "MHI": float(columns[13]), "Q": int(columns[17]),
        }
    points = {}
    for line in data_lines(SOURCE / "data/MassModels_Lelli2016c.mrt"):
        columns = line.split()
        if len(columns) != 10:
            raise ValueError(f"Unexpected point column count: {len(columns)}")
        name = columns[0]
        points.setdefault(name, []).append([
            *map(float, columns[2:8]),
        ])
    return galaxies, points


def reconstruct(galaxies, points, sigma_kms=0.0):
    sample = {}
    for name, g in galaxies.items():
        if g["Q"] > 3 or not 30 < g["inc"] < 80 or name not in points:
            continue
        arr = np.asarray(points[name], dtype=float)
        radius, velocity, _, gas, disk, bulge = arr.T
        # Gas already contains helium; do not multiply its velocity term by 1.33.
        baryon_v2 = gas * np.abs(gas) + 0.5 * disk * np.abs(disk) + 0.7 * bulge * np.abs(bulge)
        keep = (radius > 0) & (velocity > 0) & (baryon_v2 > 0)
        if np.count_nonzero(keep) < 5:
            continue
        radius, velocity, baryon_v2 = radius[keep], velocity[keep], baryon_v2[keep]
        gbar = baryon_v2 * 1e6 / (radius * KPC_M)
        # Uniform dispersion is a sensitivity device, not a measured correction.
        gobs = (velocity**2 + 2 * sigma_kms**2) * 1e6 / (radius * KPC_M)
        grar = gbar / (-np.expm1(-np.sqrt(gbar / A0_EMPIRICAL)))
        residual = np.log10(gobs / grar)
        mass = (0.5 * g["L36"] + 1.33 * g["MHI"]) * 1e9
        compactness = G_PC_KMS2_MSUN * mass / (1000 * g["Reff"] * C_KMS**2)
        sample[name] = {
            **g, "logM": float(np.log10(mass)), "loglam": float(np.log10(compactness)),
            "gmed": float(np.median(np.log10(gbar))), "dmed": float(np.median(residual)),
            "dmean": float(np.mean(residual)), "npts": int(len(radius)),
            "logSigma": float(np.log10(mass / (np.pi * g["Reff"]**2))),
        }
    return sample


def vector(sample, names, key):
    return np.asarray([sample[name][key] for name in names], dtype=float)


def partial(x, y, controls):
    design = np.column_stack([np.ones(len(x)), *controls])
    rx = x - design @ np.linalg.lstsq(design, x, rcond=None)[0]
    ry = y - design @ np.linalg.lstsq(design, y, rcond=None)[0]
    r = float(stats.pearsonr(rx, ry).statistic)
    df = len(x) - design.shape[1] - 1
    p = float(2 * stats.t.sf(abs(r * np.sqrt(df / (1 - r*r))), df))
    return {"r": r, "p": p, "df": df}


def linear_proxy_cv(sample, names):
    x, y, mass, quality = [vector(sample, names, key) for key in ("loglam", "dmean", "logM", "Q")]
    pred_structure, pred_mass, pred_quality = np.zeros((3, len(names)))
    for i in range(len(names)):
        train = np.arange(len(names)) != i
        pred_structure[i] = np.polyval(np.polyfit(x[train], y[train], 1), x[i])
        pred_mass[i] = np.polyval(np.polyfit(mass[train], y[train], 1), mass[i])
        same = train & (quality == quality[i])
        pred_quality[i] = np.mean(y[same]) if np.count_nonzero(same) > 2 else np.mean(y[train])
    errors = [float(np.mean((y - prediction)**2)) for prediction in (np.zeros(len(y)), pred_structure, pred_mass, pred_quality)]
    return {"structure_vs_zero": errors[1]/errors[0], "structure_vs_mass": errors[1]/errors[2], "structure_vs_quality": errors[1]/errors[3]}


def write_hashed(path, text):
    path.write_text(text, encoding="utf-8", newline="\n")
    path.with_name(path.name + ".sha256").write_text(digest(path) + "  " + path.name + "\n", encoding="ascii")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "summary.json").exists():
        raise FileExistsError("Preserve previous evidence: output already exists.")
    for relative, expected in PINNED.items():
        if digest(SOURCE / relative) != expected:
            raise ValueError(f"Input hash mismatch: {relative}")
    galaxies, points = parse_sources()
    sample = reconstruct(galaxies, points)
    adjusted = reconstruct(galaxies, points, sigma_kms=8.0)
    names = sorted(sample)
    threshold = float(np.median(vector(sample, names, "gmed")))
    groups = {"full": names, "lowg": [n for n in names if sample[n]["gmed"] <= threshold], "highg": [n for n in names if sample[n]["gmed"] > threshold]}
    results = {}
    for label, group in groups.items():
        x, y = vector(sample, group, "loglam"), vector(sample, group, "dmed")
        corr = stats.pearsonr(x, y)
        results[label] = {"N": len(group), "r": float(corr.statistic), "p": float(corr.pvalue), "linear_proxy_cv": linear_proxy_cv(sample, group)}
    controls = [vector(sample, groups["lowg"], k) for k in ("Q", "npts", "logM", "einc")]
    results["canonical_lowg_adc8"] = partial(vector(sample, groups["lowg"], "loglam"), vector(adjusted, groups["lowg"], "dmed"), controls)
    # This equality follows from logSigma = 2 loglam - logM + constant.
    by_mass = [vector(sample, groups["lowg"], "logM")]
    y = vector(sample, groups["lowg"], "dmean")
    compact = partial(vector(sample, groups["lowg"], "loglam"), y, by_mass)
    surface = partial(vector(sample, groups["lowg"], "logSigma"), y, by_mass)
    results["mass_control_identity"] = {"compactness": compact, "surface_density": surface, "difference_r": surface["r"]-compact["r"]}
    with (SOURCE / "results/bh_family_table.csv").open(newline="", encoding="ascii") as f:
        family = list(csv.DictReader(f))
    raw = np.array([float(row["raw_p"]) for row in family])
    order = np.argsort(raw)
    corrected = np.minimum(1, np.minimum.accumulate((raw[order] * len(raw) / np.arange(1, len(raw)+1))[::-1])[::-1])
    canonical_index = next(i for i, row in enumerate(family) if row["test"] == "canonical_joint_partial")
    results["bh_table_arithmetic_only"] = {"tests": len(raw), "survivors": int(np.count_nonzero(corrected <= .05)), "canonical_adjusted_p": float(corrected[np.where(order == canonical_index)[0][0]]), "max_difference_from_archived_rounded_adjusted_p": float(max(abs(corrected[j] - float(family[i]["BH_adjusted_p"])) for j, i in enumerate(order)))}
    checks = {
        "catalogue_175": len(galaxies) == 175,
        "sample_126": len(sample) == 126,
        "sample_points_2709": sum(g["npts"] for g in sample.values()) == 2709,
        "lowg_63": len(groups["lowg"]) == 63,
        "lowg_r_rounds_0464": round(results["lowg"]["r"], 3) == .464,
        "canonical_r_rounds_0299": round(results["canonical_lowg_adc8"]["r"], 3) == .299,
        "canonical_p_rounds_00213": round(results["canonical_lowg_adc8"]["p"], 4) == .0213,
        "full_linear_cv_mass_rounds_0986": round(results["full"]["linear_proxy_cv"]["structure_vs_mass"], 3) == .986,
        "full_linear_cv_quality_rounds_1220": round(results["full"]["linear_proxy_cv"]["structure_vs_quality"], 3) == 1.220,
        "structural_partial_identity": abs(results["mass_control_identity"]["difference_r"]) < 1e-12,
        "bh_survivors_17": results["bh_table_arithmetic_only"]["survivors"] == 17,
    }
    receipt = {
        "result_id": "R9-SPARC-LIT-20261007", "scope": "PARTIAL_RAW_MRT_ANCHOR_REPLAY_AND_METHODS_PLAN",
        "method": "fixed empirical RAR; correlations and linear-proxy LOOCV; no MCMC",
        "physics_pass": False, "gate_effect": "NONE", "Rule9_cleared": False,
        "review_status": "DEFERRED", "research_execution": "PROCEED_PROVISIONALLY",
        "claim_status": "Conditional", "ITSM_prediction_test": "NOT_RUN",
        "input_sha256": PINNED, "script_sha256": digest(Path(__file__)),
        "versions": {"numpy": np.__version__, "scipy": scipy.__version__},
        "checks": [{"name": key, "passed": bool(value)} for key,value in checks.items()],
        "results": results, "lowg_threshold_log10_gbar_SI": threshold,
        "limitations": ["Raw MRT bytes came from the author's archive; origin-site identity not independently verified.", "No full nonlinear M2 replay, hierarchical model, external dataset fit, or dynamical solution.", "BH p-values are author inputs; only adjustment arithmetic is replayed.", "Low/high split uses the full source sample median; it is descriptive and not prospective external validation.", "Shared stellar mass assumptions and pressure-support approximations are retained for anchor reconstruction."],
    }
    write_hashed(OUT / "summary.json", json.dumps(receipt, indent=2, allow_nan=False) + "\n")
    rows = [{"name": name, **sample[name]} for name in names]
    import io
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
    writer.writeheader(); writer.writerows(rows)
    write_hashed(OUT / "galaxy_reconstruction.csv", buffer.getvalue())
    print(json.dumps({"checks": checks, "results": results, "receipt": str(OUT / "summary.json")}, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
