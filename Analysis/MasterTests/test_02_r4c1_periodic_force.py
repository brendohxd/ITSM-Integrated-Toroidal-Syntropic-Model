"""R4C1-T2P1: periodic force/zero-mode audit in a frozen-frame control.

The nonlinear torus solve is a conditional static density-contrast snapshot,
not a physical ITSM galaxy solution or canonical Master Test-2 pass.
"""
from __future__ import annotations

import argparse
import ast
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import scipy
from scipy.sparse.linalg import LinearOperator, cg
import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
PINS = {
    "Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md":
        "81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3",
    "Theory/Gates/RES-001/RES001_R4C1_FIRST_VARIATION_REPORT_2026-09-25.md":
        "4834ea7517fd0393015e1d94fa1c130d84e2796b0ae1667712c2b5cf4653692c",
    "Theory/Gates/RES-001/RES001_R4C1_COEFFICIENT_IDENTIFIABILITY_REPORT_2026-09-25.md":
        "c4af4084ae83f7ed70d63f44700a0ebfc2c394ed7d79cd0061e3efe279b7dc0a",
    "Analysis/MasterTests/test_01_r4c1_interacting_background.py":
        "1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f",
    "Theory/Gates/ITSM_TEST_02_T3_TOPOLOGY_ADDENDUM_2026-09-25.md":
        "a4f251ff3d751a60ff4130d61a060f199c825604f877e1aeb5dd5515db8f317c",
    "Theory/Gates/ITSM_TESTS_01_03_DERIVATION_DISPOSITION_2026-09-25.md":
        "b999dff43b81f1dc73a9f584bd1c6a1856c559fe15b896719aa82300c8327883",
    "Theory/Core/ITSM_MASTER_TEST_PROGRAMME_2026-09-24.md":
        "81c7138568d44fd3197b88cb21efe67b17c406ada941f7ff778c2f8821ae074b",
    "Theory/Gates/RES-001/RES001_R4C1_PERIODIC_FORCE_CONTRACT_2026-09-29.md":
        "2f660751bd0155833643b3388672bb0462dbe5af703385875eda370b021d3645",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_pins() -> None:
    for rel, expected in PINS.items():
        path = ROOT / rel
        if sha256(path) != expected:
            raise RuntimeError(f"FROZEN_INPUT_HASH_MISMATCH: {rel}")
        sidecar = path.with_name(path.name + ".sha256")
        if sidecar.exists() and sidecar.read_text(encoding="ascii").strip() != f"{expected}  {path.name}":
            raise RuntimeError(f"SOURCE_SIDECAR_MISMATCH: {rel}")


def literal(node: ast.AST) -> Fraction:
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return Fraction(str(node.value))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = literal(node.operand)
        return value if isinstance(node.op, ast.UAdd) else -value
    if isinstance(node, ast.BinOp):
        left, right = literal(node.left), literal(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
    raise ValueError("Nonliteral B1 parameter expression")


def b1_params() -> dict[str, Fraction]:
    rel = "Analysis/MasterTests/test_01_r4c1_interacting_background.py"
    tree = ast.parse((ROOT / rel).read_text(encoding="utf-8"))
    calls = [node.value for node in tree.body if isinstance(node, ast.Assign)
             and any(isinstance(target, ast.Name) and target.id == "PARAMS"
                     for target in node.targets)]
    if len(calls) != 1 or not isinstance(calls[0], ast.Call):
        raise ValueError("B1 PARAMS declaration not uniquely found")
    call = calls[0]
    if not isinstance(call.func, ast.Name) or call.func.id != "dict" or call.args:
        raise ValueError("B1 PARAMS is not a literal dict call")
    return {item.arg: literal(item.value) for item in call.keywords if item.arg is not None}


def symbolic_checks(checks: list[dict]) -> None:
    t, x = sp.symbols("t x", real=True)
    a = sp.Function("a", positive=True)(t)
    psi = sp.Function("psi")(t, x)
    rho = sp.Function("rho")(t, x)
    K, A, b, beta = sp.symbols("K A b beta", positive=True)
    p_t, p_x, p_xx = sp.diff(psi, t), sp.diff(psi, x), sp.diff(psi, x, 2)
    # Positive-gradient local chart; the separate vector check restores |grad|.
    lag = a**3 * (K * p_t**2 / 2 - A * (p_x / a)**3
                  - b * p_xx**2 / (2 * a**4) - beta * rho * psi)
    euler = (sp.diff(lag, psi) - sp.diff(sp.diff(lag, p_t), t)
             - sp.diff(sp.diff(lag, p_x), x)
             + sp.diff(sp.diff(lag, p_xx), x, 2)) / a**3
    expected = (-K * sp.diff(a**3 * p_t, t) / a**3
                + 3 * A * sp.diff(p_x**2, x) / a**3
                - b * sp.diff(psi, x, 4) / a**4 - beta * rho)
    checks.append({"name": "one_dimensional_FRW_action_variation",
                   "passed": sp.simplify(euler - expected) == 0,
                   "residual": str(sp.simplify(euler - expected))})
    wrong_b = expected + 2 * b * sp.diff(psi, x, 4) / a**4
    checks.append({"name": "regulator_sign_mutant_rejected",
                   "passed": sp.simplify(euler - wrong_b) != 0,
                   "residual": str(sp.simplify(euler - wrong_b))})
    qx, qy, qz = sp.symbols("qx qy qz", real=True)
    norm2 = qx**2 + qy**2 + qz**2
    vector_derivative = sp.diff(A * norm2**sp.Rational(3, 2), qx)
    checks.append({"name": "three_dimensional_cubic_flux_variation",
                   "passed": sp.simplify(vector_derivative - 3 * A * sp.sqrt(norm2) * qx) == 0,
                   "residual": str(sp.simplify(vector_derivative - 3 * A * sp.sqrt(norm2) * qx))})
    mean_psi = sp.Function("mean_psi")(t)
    H = sp.diff(a, t) / a
    homogeneous = -K * (sp.diff(mean_psi, t, 2) + 3 * H * sp.diff(mean_psi, t)) - beta * rho
    checks.append({"name": "homogeneous_B1_force_sign",
                   "passed": sp.simplify(sp.solve(homogeneous, sp.diff(mean_psi, t, 2))[0]
                                         + 3 * H * sp.diff(mean_psi, t) + beta * rho / K) == 0,
                   "residual": "psi_ddot=-3H*psi_dot-beta*rho/K_Q"})


class TorusGrid:
    def __init__(self, n: int, A: float, b: float, beta: float):
        self.n, self.A, self.b, self.beta = n, A, b, beta
        axis = 2 * np.pi * np.arange(n) / n
        self.X, self.Y, self.Z = np.meshgrid(axis, axis, axis, indexing="ij")
        self.delta = (np.cos(self.X) + 2 * np.cos(self.Y) + 3 * np.cos(self.Z)) / 50
        self.delta -= self.delta.mean()
        wave = np.fft.fftfreq(n, d=1 / n)
        self.k = np.meshgrid(wave, wave, wave, indexing="ij")
        self.k2 = sum(ki**2 for ki in self.k)
        self.k4 = self.k2**2
        self.source_scale = beta * float(np.sqrt(np.mean(self.delta**2)))

    def fft(self, field: np.ndarray) -> np.ndarray:
        return np.fft.fftn(field)

    def inverse(self, field: np.ndarray) -> np.ndarray:
        return np.fft.ifftn(field).real

    def fields(self, psi: np.ndarray) -> tuple[list[np.ndarray], np.ndarray, np.ndarray]:
        f = self.fft(psi)
        grad = [self.inverse(1j * ki * f) for ki in self.k]
        lap = self.inverse(-self.k2 * f)
        bilap = self.inverse(self.k4 * f)
        return grad, lap, bilap

    def energy_gradient(self, flat: np.ndarray) -> tuple[float, np.ndarray]:
        psi = flat.reshape((self.n,) * 3)
        psi = psi - psi.mean()
        grad, lap, bilap = self.fields(psi)
        norm = np.sqrt(sum(part**2 for part in grad))
        flux = [norm * part for part in grad]
        div = sum(self.inverse(1j * ki * self.fft(fi)) for ki, fi in zip(self.k, flux))
        euler = -3 * self.A * div + self.b * bilap + self.beta * self.delta
        energy = np.sum(self.A * norm**3 + self.b * lap**2 / 2 + self.beta * self.delta * psi)
        return float(energy), (euler - euler.mean()).ravel()

    def linear_solution(self) -> np.ndarray:
        f = self.fft(self.delta)
        result = np.zeros_like(f, dtype=complex)
        mask = self.k2 > 0
        result[mask] = -self.beta * f[mask] / (self.b * self.k4[mask])
        return self.inverse(result)

    def diagnostics(self, solution: np.ndarray, optimize_result) -> dict:
        psi = solution.reshape((self.n,) * 3)
        psi = psi - psi.mean()
        grad, lap, bilap = self.fields(psi)
        norm = np.sqrt(sum(part**2 for part in grad))
        div = sum(self.inverse(1j * ki * self.fft(norm * part))
                  for ki, part in zip(self.k, grad))
        euler = -3 * self.A * div + self.b * bilap + self.beta * self.delta
        scale = self.source_scale
        strong = float(np.sqrt(np.mean(euler**2)) / scale)
        omit_b = float(np.sqrt(np.mean((-3 * self.A * div + self.beta * self.delta)**2)) / scale)
        weak = {}
        coefficients = {}
        for label, angle, dim in (("x", self.X, 0), ("y", self.Y, 1), ("z", self.Z, 2)):
            for kind in ("cos", "sin"):
                test = np.cos(angle) if kind == "cos" else np.sin(angle)
                test_grad = -np.sin(angle) if kind == "cos" else np.cos(angle)
                test_lap = -test
                integrand = (3 * self.A * norm * grad[dim] * test_grad
                             + self.b * lap * test_lap + self.beta * self.delta * test)
                denominator = scale * float(np.sqrt(np.mean(test**2))) + 1e-12
                weak[kind + "_" + label] = float(abs(np.mean(integrand)) / denominator)
            coefficients[label] = float(2 * np.mean(psi * np.cos(angle)))
        return {
            "n": self.n,
            "optimizer_success": bool(optimize_result.success),
            "optimizer_message": str(optimize_result.message),
            "optimizer_iterations": int(optimize_result.nit),
            "energy": float(optimize_result.fun),
            "psi_mean": float(psi.mean()),
            "source_mean": float(self.delta.mean()),
            "total_density_min": float((0.2 + self.delta).min()),
            "strong_residual_normalized": strong,
            "omit_b_residual_normalized": omit_b,
            "weak_residuals_normalized": weak,
            "fundamental_cosine_coefficients": coefficients,
            "psi_rms": float(np.sqrt(np.mean(psi**2))),
        }


def directional_control(grid: TorusGrid) -> dict:
    probe = 0.03 * (np.cos(grid.X) + np.sin(2 * grid.Y) + np.cos(3 * grid.Z))
    probe = probe - probe.mean()
    rng = np.random.default_rng(311)
    direction = rng.standard_normal(probe.size)
    direction -= direction.mean()
    direction /= np.linalg.norm(direction)
    step = 1e-6
    energy, gradient = grid.energy_gradient(probe.ravel())
    plus = grid.energy_gradient(probe.ravel() + step * direction)[0]
    minus = grid.energy_gradient(probe.ravel() - step * direction)[0]
    finite_difference = (plus - minus) / (2 * step)
    analytic = float(np.dot(gradient, direction))
    discrepancy = abs(finite_difference - analytic) / max(1.0, abs(finite_difference), abs(analytic))
    return {"off_shell_energy": energy, "analytic": analytic,
            "central_difference": finite_difference, "relative_discrepancy": discrepancy}


def minimize_convex(grid: TorusGrid, initial: np.ndarray) -> SimpleNamespace:
    """Damped Newton minimization with a positive Fourier preconditioner.

    The Hessian is the exact discrete derivative of the nonanalytic but C2
    spatial energy. Its zero-mode null direction is removed throughout.
    """
    shape = (grid.n,) * 3
    size = grid.n**3
    x = initial.ravel().copy()
    x -= x.mean()
    for iteration in range(41):
        energy, gradient = grid.energy_gradient(x)
        residual = np.sqrt(np.mean(gradient**2)) / grid.source_scale
        if residual < 1e-7:
            return SimpleNamespace(x=x, success=True,
                                   message=f"damped Newton residual {residual:.3e}",
                                   nit=iteration, fun=energy)
        if iteration == 40:
            break
        psi = x.reshape(shape)
        base_grad, _, _ = grid.fields(psi)
        norm = np.sqrt(sum(part**2 for part in base_grad))
        average_norm = max(float(norm.mean()), 1e-8)

        def hessian_product(flat: np.ndarray) -> np.ndarray:
            variation = flat.reshape(shape) - flat.mean()
            grad_v, _, bilap_v = grid.fields(variation)
            inner = sum(g * v for g, v in zip(base_grad, grad_v))
            quotient = np.zeros_like(inner)
            np.divide(inner, norm, out=quotient, where=norm > 1e-14)
            flux_v = [norm * v + g * quotient
                      for g, v in zip(base_grad, grad_v)]
            div_v = sum(grid.inverse(1j * ki * grid.fft(fi))
                        for ki, fi in zip(grid.k, flux_v))
            result = -3 * grid.A * div_v + grid.b * bilap_v
            result -= result.mean()
            return result.ravel()

        denominator = grid.b * grid.k4 + 3 * grid.A * average_norm * grid.k2
        nonzero = grid.k2 > 0

        def precondition(flat: np.ndarray) -> np.ndarray:
            f = grid.fft(flat.reshape(shape) - flat.mean())
            result = np.zeros_like(f)
            result[nonzero] = f[nonzero] / denominator[nonzero]
            return grid.inverse(result).ravel()

        hessian = LinearOperator((size, size), matvec=hessian_product, dtype=float)
        inverse = LinearOperator((size, size), matvec=precondition, dtype=float)
        direction, info = cg(hessian, -gradient, M=inverse,
                             rtol=1e-10, atol=0.0, maxiter=300)
        if info != 0 or not np.all(np.isfinite(direction)):
            return SimpleNamespace(x=x, success=False,
                                   message=f"Newton CG failed: info={info}",
                                   nit=iteration, fun=energy)
        direction -= direction.mean()
        slope = float(np.dot(gradient, direction))
        if slope >= 0:
            return SimpleNamespace(x=x, success=False,
                                   message=f"Newton direction non-descent: {slope}",
                                   nit=iteration, fun=energy)
        step = 1.0
        accepted = False
        for _ in range(30):
            candidate = x + step * direction
            trial_energy = grid.energy_gradient(candidate)[0]
            if trial_energy <= energy + 1e-4 * step * slope:
                x = candidate
                accepted = True
                break
            step /= 2
        if not accepted:
            return SimpleNamespace(x=x, success=False,
                                   message="Newton Armijo line search failed",
                                   nit=iteration, fun=energy)
    final_energy = grid.energy_gradient(x)[0]
    return SimpleNamespace(x=x, success=False,
                           message="Newton maximum iterations reached",
                           nit=40, fun=final_energy)


def run() -> dict:
    verify_pins()
    checks = []
    symbolic_checks(checks)
    params = b1_params()
    expected = {"A": Fraction(2, 7), "b": Fraction(5, 11),
                "beta": Fraction(2, 5), "K": Fraction(3, 1)}
    for key, value in expected.items():
        checks.append({"name": f"B1_{key}_frozen", "passed": params[key] == value,
                       "value": str(params[key]), "expected": str(value)})
    A, b, beta = [float(params[key]) for key in ("A", "b", "beta")]
    checks.append({"name": "static_full_density_zero_mode_rejected",
                   "passed": params["beta"] * Fraction(1, 5) == Fraction(2, 25),
                   "mean_source": str(beta * float(Fraction(1, 5)))})
    grids = []
    direction = None
    for n in (17, 25, 33):
        grid = TorusGrid(n, A, b, beta)
        initial = grid.linear_solution()
        # Remove the nonlinear term for the independent exact A=0 control.
        linear_control = TorusGrid(n, 0.0, b, beta)
        _, linear_euler = linear_control.energy_gradient(initial.ravel())
        linear_norm = float(np.sqrt(np.mean(linear_euler**2)) / grid.source_scale)
        checks.append({"name": f"grid_{n}_analytic_A_zero_control",
                       "passed": linear_norm < 1e-10, "value": linear_norm})
        optimum = minimize_convex(grid, initial)
        row = grid.diagnostics(optimum.x, optimum)
        grids.append(row)
        checks.append({"name": f"grid_{n}_finite_and_converged",
                       "passed": bool(np.all(np.isfinite(optimum.x))
                                      and np.isfinite(optimum.fun) and optimum.success),
                       "optimizer_message": str(optimum.message)})
        checks.append({"name": f"grid_{n}_zero_mean_and_positive_density",
                       "passed": abs(row["psi_mean"]) < 1e-12
                                 and abs(row["source_mean"]) < 1e-12
                                 and row["total_density_min"] >= 2 / 25 - 1e-12,
                       "values": [row["psi_mean"], row["source_mean"],
                                  row["total_density_min"]]})
        checks.append({"name": f"grid_{n}_strong_collocation_residual",
                       "passed": row["strong_residual_normalized"] < 1e-5,
                       "value": row["strong_residual_normalized"]})
        checks.append({"name": f"grid_{n}_regulator_omission_rejected",
                       "passed": row["omit_b_residual_normalized"] > 1e-2,
                       "value": row["omit_b_residual_normalized"]})
        for mode, residual in row["weak_residuals_normalized"].items():
            checks.append({"name": f"grid_{n}_weak_{mode}",
                           "passed": residual < 1e-5, "value": residual})
        if n == 17:
            direction = directional_control(grid)
            checks.append({"name": "off_shell_directional_variation",
                           "passed": direction["relative_discrepancy"] < 1e-5,
                           "value": direction["relative_discrepancy"]})
    fundamental = {}
    for axis in ("x", "y", "z"):
        low = grids[1]["fundamental_cosine_coefficients"][axis]
        high = grids[2]["fundamental_cosine_coefficients"][axis]
        relative = abs(low - high) / max(abs(high), 1e-12)
        fundamental[axis] = relative
        checks.append({"name": f"grid_25_33_fundamental_{axis}",
                       "passed": relative < 5e-3, "value": relative})
    passed = sum(item["passed"] for item in checks)
    return {
        "candidate": "R4C1-v1", "control": "R4C1-T2P1",
        "validation": "PASS" if passed == len(checks) else "FAIL",
        "passed": passed, "total": len(checks), "checks": checks,
        "grids": grids, "directional_control": direction,
        "grid_25_33_fundamental_relative_changes": fundamental,
        "source_sha256": PINS, "script_sha256": sha256(Path(__file__)),
        "runtime": {"numpy": np.__version__, "scipy": scipy.__version__,
                    "sympy": sp.__version__},
        "status": "ACTION_DERIVED_MEAN_OBSTRUCTION_CONDITIONAL_PERIODIC_SNAPSHOT_ONLY",
        "scope": "aligned fixed FRW and static contrast pseudospectral control; no coupled physical T3 solution",
        "quasistatic_error_bounded": False,
        "full_metric_frame_dust_constraints_solved": False,
        "physical_periodic_solution_verified": False,
        "canonical_Test2_pass": False, "physics_pass": False,
        "gate_effect": "NONE", "Rule9_cleared": False,
        "review_status": "DEFERRED",
        "MAT-001": "BLOCKED", "UVIR-003": "IN_PROGRESS",
        "K_Q": "NOT_DERIVED", "V": "NOT_COMPUTED",
        "Stage4A": "CLOSED",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--attempt", default="01", choices=("01", "02", "03"))
    args = parser.parse_args()
    record = run()
    out = ROOT / "Analysis/MasterTests/outputs" / f"r4c1_t2p1_attempt_{args.attempt}" / "summary.json"
    payload = (json.dumps(record, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        if out.read_bytes() != payload:
            raise RuntimeError(f"EXISTING_RECEIPT_DIFFERS: {out}")
    else:
        with out.open("xb") as stream:
            stream.write(payload)
    sidecar = out.with_name(out.name + ".sha256")
    line = f"{sha256(out)}  {out.name}\n"
    if sidecar.exists():
        if sidecar.read_text(encoding="ascii") != line:
            raise RuntimeError(f"EXISTING_RECEIPT_SIDECAR_DIFFERS: {sidecar}")
    else:
        with sidecar.open("x", encoding="ascii", newline="\n") as stream:
            stream.write(line)
    print(json.dumps({"validation": record["validation"], "passed": record["passed"],
                      "total": record["total"], "status": record["status"],
                      "physics_pass": False, "receipt_sha256": sha256(out)}))
    for item in record["checks"]:
        if not item["passed"]:
            print(json.dumps(item))
    return 0 if record["validation"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
