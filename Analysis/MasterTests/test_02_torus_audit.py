"""Exact flat-T3 counterexamples; not a physical periodic galaxy solution."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import sympy as s

from tests_01_03_symbolic_audit import Audit, digest

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "Theory/Gates/ITSM_TEST_02_T3_TOPOLOGY_ADDENDUM_2026-09-25.md"


def main():
    audit = Audit()
    x, y, z = coords = s.symbols("x y z", real=True)
    epsilon, k = s.symbols("epsilon k", positive=True)
    potential = epsilon * (s.cos(x) + 2*s.cos(y))
    gradient = s.Matrix([s.diff(potential, q) for q in coords])
    laplacian = sum(s.diff(potential, q, 2) for q in coords)
    for q in coords:
        audit.check(f"potential_periodic_{q}", potential.subs(q, q+2*s.pi)-potential)
    audit.check("periodic_source_zero_mean", s.integrate(laplacian, (x,0,2*s.pi), (y,0,2*s.pi)))
    # R>0 on the patch under examination. No differentiability at R=0 is assumed.
    R = s.sin(x)**2 + 4*s.sin(y)**2
    proposed = k*s.sqrt(epsilon)*s.Matrix([-s.sin(x), -2*s.sin(y), 0])/R**s.Rational(1,4)
    norm = k*s.sqrt(epsilon)*R**s.Rational(1,4)
    audit.check("proposed_norm_squared", proposed.dot(proposed)-norm**2)
    flux = norm*proposed
    for i in range(3):
        audit.check(f"flux_relation_{i}", flux[i]-k**2*gradient[i])
    audit.check("sourced_flux_equation", sum(s.diff(flux[i], coords[i]) for i in range(3))-k**2*laplacian)
    curl = s.diff(proposed[1],x)-s.diff(proposed[0],y)
    expected = k*s.sqrt(epsilon)*s.sin(x)*s.sin(y)*(s.cos(x)-2*s.cos(y))/R**s.Rational(5,4)
    audit.check("periodic_curl_formula", curl-expected)
    point = {x:s.pi/4, y:s.pi/4, epsilon:1, k:1}
    curl_point = s.simplify(curl.subs(point))
    audit.check("universal_algebraic_gradient_rejected_on_T3", curl_point, True)
    # Smooth periodic scalar with zero-mean gradient, but nonlinear mean flux
    # not identically zero as a function of the deformation b.
    b = s.symbols("b", real=True)
    phi = s.sin(x) + b*s.sin(2*x)/2
    q = s.diff(phi,x)
    audit.check("periodic_gradient_zero_mean", s.integrate(q,(x,0,2*s.pi)))
    # d/db (|q|q) at b=0 = 2|cos x|cos(2x), including the zeros by continuity.
    integrand = 2*s.cos(x)*s.cos(2*x)
    mean_flux_derivative = (s.integrate(integrand,(x,0,s.pi/2))
        -s.integrate(integrand,(x,s.pi/2,3*s.pi/2))
        +s.integrate(integrand,(x,3*s.pi/2,2*s.pi)))/(2*s.pi)
    audit.check("nonlinear_mean_flux_derivative", mean_flux_derivative-4/(3*s.pi))
    audit.check("zero_harmonic_flux_not_automatic", mean_flux_derivative, True)
    # All nonzero transverse Fourier modes are curls; their zero mode is not.
    kx,ky,kz = s.symbols("kx ky kz", real=True)
    ax,ay,az = s.symbols("ax ay az", real=True)
    wave = s.Matrix([kx,ky,kz])
    transverse = wave.cross(s.Matrix([ax,ay,az]))
    vector_potential = s.I*wave.cross(transverse)/wave.dot(wave)
    residual = s.I*wave.cross(vector_potential)-transverse
    for i in range(3):
        audit.check(f"nonzero_mode_hodge_reconstruction_{i}", residual[i])
    # A constant unit field is divergence-free and has nonzero mean. The mean
    # of any periodic curl is zero (integral of each derivative is an endpoint
    # difference), so a global periodic curl alone cannot represent this field.
    constant = s.Matrix([1,0,0])
    audit.check("constant_mode_divergence", sum(s.diff(constant[i],coords[i]) for i in range(3)))
    audit.check("constant_mode_nonzero_mean", s.integrate(constant[0],(x,0,2*s.pi))/(2*s.pi), True)
    audit.record(
        status="PERIODIC_ALGEBRAIC_COUNTEREXAMPLE_HARMONIC_FLUX_REQUIRED_PARENT_HOLD",
        geometry="flat cubic T3 snapshot; 2*pi-periodic dimensionless coordinates; no cosmological solve",
        potential=potential, source_laplacian=laplacian,
        physical_density="delta_rho=laplacian/(4*pi*G*L^2); rho_bar >= 3*epsilon/(4*pi*G*L^2) ensures rho>=0",
        source_scaling="physical position r=L*(x,y,z); epsilon has potential units; counterexample k>0",
        curl=curl, curl_at_registered_point=curl_point,
        harmonic_flux_derivative=mean_flux_derivative,
        hodge="F=curl(H)+h0; h0=spatial_mean(F); F=|grad(phi)|grad(phi)/a0-(Cm/CIR)*grad(Phi_N)",
        hodge_assumptions="flat periodic metric; S_Q=0; source equations satisfied; no prescribed nonperiodic potential winding",
        harmonic_boundary="h0 is fixed by the periodic solution, not a freely fitted uniform acceleration",
        global_solution="NOT_COMPUTED", local_spherical_error="NOT_BOUNDED")
    passed = all(row["passed"] for row in audit.checks)
    sources = {"contract": CONTRACT, "executable": Path(__file__),
               "shared_helper": Path(__file__).with_name("tests_01_03_symbolic_audit.py")}
    payload = {"test":2, "addendum":"T3", "local_symbolic_validation":"PASS" if passed else "FAIL",
               "checks":audit.checks, "results":audit.results,
               "source_sha256":{key:digest(path) for key,path in sources.items()},
               "runtime":{"python":sys.version.split()[0], "sympy":s.__version__},
               "physics_pass":False, "canonical_test_complete":False, "gate_effect":"NONE", "Rule9":"NOT_COMPLETED"}
    target = Path(__file__).parent / "outputs/test_02_torus_audit.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    for path in (target,CONTRACT,Path(__file__)):
        path.with_suffix(path.suffix+".sha256").write_text(f"{digest(path)}  {path.name}\n",encoding="ascii")
    print(json.dumps({"validation":payload["local_symbolic_validation"],
                      "passed":sum(row["passed"] for row in audit.checks), "total":len(audit.checks),
                      "status":audit.results["status"], "curl_at_point":str(curl_point),
                      "mean_flux_derivative":str(mean_flux_derivative), "sha256":digest(target)}))
    if not passed:
        print(json.dumps([row for row in audit.checks if not row["passed"]],indent=2))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
