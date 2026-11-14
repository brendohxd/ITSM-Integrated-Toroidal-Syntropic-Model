"""Reproduce and diagnose SPARC's remaining 18 conditional sampling failures."""

import argparse
import json
from pathlib import Path

import sparc_real_mcmc_v3 as base
from sparc_continue_54_v1 import PARENT
import emcee
import numpy as np
from scipy.stats import spearmanr


CONTINUED = PARENT.parent / "sparc_54_continue_v1_20261101"
CONTRACT = (base.ROOT / "Theory/Gates/STAT-001"
            / "SPARC_18_CHAIN_DIAGNOSTIC_V1_CONTRACT_2026-11-09.md")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verified_file(folder, manifest, name):
    path = folder / name
    require(base.digest(path) == manifest[name], f"Artifact mismatch: {path}")
    return path


def open_archive(folder):
    path = folder / "artifact_manifest.json"
    digest = base.digest(path)
    require(digest == path.with_suffix(".json.sha256").read_text().split()[0],
            f"Manifest sidecar mismatch: {path}")
    return json.loads(path.read_text()), digest


def load_ensemble(name, ensemble, archives, ndim):
    fixed, descriptive = [], [[], []]
    best_lp, best = -np.inf, None
    for segment, (folder, manifest) in enumerate(archives):
        for end in range(1000 + segment * 10000, 11000 + segment * 10000, 1000):
            rel = f"{name}/{ensemble}/block_{end:06d}.npz"
            with np.load(verified_file(folder, manifest, rel), allow_pickle=False) as block:
                chain, lp = block["chain"], block["log_probability"]
                require(chain.shape == (1000, 64, ndim) and lp.shape == (1000, 64)
                        and int(block["end"]) == end, f"Block mismatch: {rel}")
                require(np.isfinite(chain).all() and np.isfinite(lp).all(),
                        f"Nonfinite block: {rel}")
                if end <= 2000:
                    continue
                fixed.append(chain[:, 0].copy())
                # Steps 2,001–11,000 and 11,001–20,000 are equal windows.
                window = int(end > 11000)
                descriptive[window].append(chain[::20].reshape(-1, ndim).copy())
                location = np.unravel_index(lp.argmax(), lp.shape)
                if lp[location] > best_lp:
                    best_lp, best = float(lp[location]), chain[location].copy()
    return np.concatenate(fixed), [np.concatenate(w) for w in descriptive], best, best_lp


def inspect_galaxy(name, row, archives, recorded):
    data = base.load(row)
    names = ["log10_Udisk", "D_over_D0", "inclination_deg"]
    if np.any(data["bulge"] != 0):
        names.append("log10_Ubulge")
    ndim = len(names)
    ensembles = [load_ensemble(name, e, archives, ndim) for e in range(4)]
    fixed = np.stack([e[0] for e in ensembles])
    require(fixed.shape == (4, 18000, ndim), f"Unexpected retained length: {name}")
    rhat = base.rhat(fixed)
    taus = np.array([emcee.autocorr.integrated_time(c[:, None, :], tol=0, quiet=True)
                     for c in fixed])
    ess = np.sum(18000 / taus, axis=0)
    length_ok = bool(np.all(18000 >= 50 * taus))
    require(np.allclose(rhat, recorded["rank_folded_split_rhat"], atol=1e-12, rtol=0)
            and np.allclose(ess, recorded["fixed_walker_ess"], atol=1e-6, rtol=1e-9)
            and length_ok == recorded["length_check"]
            and not recorded["criteria_met"] and np.any(rhat >= 1.01),
            f"Original convergence diagnostics did not reproduce: {name}")
    pooled = np.concatenate([w for e in ensembles for w in e[1]])
    q25, q75 = np.quantile(pooled, [0.25, 0.75], axis=0)
    iqr = q75 - q25
    require(np.all(iqr > 0), f"Degenerate descriptive IQR: {name}")
    centers = np.array([np.median(np.concatenate(e[1]), axis=0) for e in ensembles])
    span = np.ptp(centers, axis=0) / iqr
    details = []
    for _, windows, best, best_lp in ensembles:
        require(abs(float(base.logpost(best, data)[0]) - best_lp) <= 1e-10,
                f"Saved target mismatch: {name}")
        samples = np.concatenate(windows)
        correlations = spearmanr(samples, axis=0).statistic
        ub = 10**samples[:, 3] if ndim == 4 else np.zeros(len(samples))
        disk = data["disk"] * np.abs(data["disk"])
        gas = data["gas"] * np.abs(data["gas"])
        bulge = data["bulge"] * np.abs(data["bulge"])
        require(np.all(disk > 0), f"Unsupported support chart: {name}")
        floor = np.max((-gas - ub[:, None] * bulge) / disk, axis=1)
        positive = floor > 0
        close_to_floor = np.zeros(len(samples), dtype=bool)
        close_to_floor[positive] = samples[positive, 0] - np.log10(floor[positive]) <= 0.05
        v, valid = base.prediction(best, data)
        require(valid[0], f"Unsupported best saved state: {name}")
        prior_z = [(best[0] - np.log10(.5)) / .1,
                   (best[1] - 1) / data["d_sigma"],
                   (best[2] - data["i0"]) / data["i_sigma"]]
        if ndim == 4:
            prior_z.append((best[3] - np.log10(.7)) / .1)
        details.append(dict(
            window_medians=[np.median(w, axis=0).tolist() for w in windows],
            window_shift_iqr=(np.abs(np.median(windows[1], axis=0)
                                     - np.median(windows[0], axis=0)) / iqr).tolist(),
            spearman=correlations.tolist(),
            fraction_within_1deg_of_inclination_limit=float(
                np.mean((samples[:, 2] <= 1) | (samples[:, 2] >= 89))),
            fraction_near_positive_inward_floor=float(np.mean(close_to_floor)),
            best_sample=best.tolist(), best_log_density=best_lp,
            raw_chi2_at_best_sample=float(np.sum(((v[0]-data["v"])/data["error"])**2)),
            best_sample_prior_z=prior_z))
    return dict(name=name, parameters=names, radial_points=len(data["v"]),
                rank_folded_split_rhat=rhat.tolist(), fixed_walker_ess=ess.tolist(),
                length_check=length_ok, ensemble_median_span_iqr=span.tolist(),
                pooled_descriptive_iqr=iqr.tolist(), ensembles=details)


def calculate():
    parent, parent_hash = open_archive(PARENT)
    continued, continued_hash = open_archive(CONTINUED)
    parent_contract = json.loads(verified_file(PARENT, parent, "run_contract.json").read_text())
    link = json.loads(verified_file(CONTINUED, continued, "continuation_contract.json").read_text())
    require(link["parent_manifest_sha256"] == parent_hash and link["unchanged_target"],
            "Continuation provenance mismatch")
    for rel, digest in parent_contract["pins"].items():
        require(base.digest(base.ROOT / rel) == digest, f"Source input mismatch: {rel}")
    old = json.loads(verified_file(CONTINUED, continued, "diagnostics.json").read_text())
    names = old["still_not_accepted"]
    require(len(names) == len(set(names)) == 18 and set(names) <= set(link["names"]),
            "Unexpected failure population")
    rows = {r["Name"]: r for r in parent_contract["rows"]}
    archived = {d["name"]: d for d in old["diagnostics"]}
    archives = [(PARENT, parent), (CONTINUED, continued)]
    results = [inspect_galaxy(name, rows[name], archives, archived[name]) for name in names]
    return dict(physics_pass=False, gate_effect="NONE", review_status="DEFERRED",
                parent_manifest_sha256=parent_hash, continued_manifest_sha256=continued_hash,
                source_sha256=base.digest(Path(__file__)), contract_sha256=base.digest(CONTRACT),
                archives_preserved=True, reproduced_cases=len(results), results=results)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--output", type=Path)
    mode.add_argument("--replay", type=Path)
    args = parser.parse_args()
    result = calculate()
    payload = (json.dumps(result, indent=2, allow_nan=False) + "\n").encode("utf-8")
    if args.replay:
        require(args.replay.read_bytes() == payload, "Replay differs from receipt")
        print("Byte-identical read-only replay for all 18 cases")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=False)
        with args.output.open("xb") as stream:
            stream.write(payload)
        print("Verified and diagnosed all 18 cases")


if __name__ == "__main__":
    main()
