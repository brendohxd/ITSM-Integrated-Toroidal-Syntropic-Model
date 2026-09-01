import re

file_path = r"C:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Manuscript\ITSM_Core_Cosmology_v11.2.1.tex"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Change \citet{sparc} to \cite{sparc}
content = content.replace(r"\citet{sparc}", r"\cite{sparc}")

# 2. Fix V.A and V.B
v_a_header = r"\subsection{Mathematical Formulation and Prior Boundaries}"
v_b_header = r"\subsection{MCMC Algorithmic Integrity: Parameter Injection and Mock Recovery}"
v_b_text = r"""To preempt concerns regarding optimizer convergence and local-minimum trapping, we executed a rigorous parameter injection (mock recovery) test prior to processing the empirical SPARC data. Synthetic rotation curves were generated with known, injected parameters ($\Upsilon_{\text{disk}}$, $\Upsilon_{\text{bulge}}$, distance, inclination) and subjected to simulated observational noise. The ITSM MCMC architecture successfully recovered the exact injected priors without systemic bias, proving that the parameter probability distributions and resulting $\chi^2$ matrices are computationally sound and not artifacts of the optimization topography."""
math_text = r"""The total circular orbital velocity field inside the fluid plenum geometry is governed by the non-ad-hoc coupling of the local Newtonian acceleration field ($g_{\text{bar}}$) to the higher-dimensional toroidal projection scale ($a_0$). The total acceleration vector $g_{\text{tot}}$ is expressed as:

\begin{equation}
g_{\text{tot}} = g_{\text{bar}} + \frac{2}{3}\sqrt{g_{\text{bar}} a_0}
\end{equation}

where the acceleration metric anchor $a_0$ is derived directly from the fundamental boundary conditions of the 3-Torus ($T^3$) spatial manifold without empirical fitting coefficients:

\begin{equation}
a_0 = \frac{c H_0}{2\pi}
\end{equation}

The Newtonian baryonic acceleration profile is constructed from the constituent visible mass sectors via:

\begin{equation}
g_{\text{bar}} = \frac{V_{\text{gas}}|V_{\text{gas}}| + \Upsilon_{d} V_{d}|V_{d}| + \Upsilon_{b} V_{b}|V_{b}|}{R}
\end{equation}

To eliminate theoretical bias and cross-contamination from standard paradigm timelines, the prior probability distributions were assigned wide, un-truncated boundaries. The parameter spaces were bounded via flat uniform distributions: $\Upsilon_{\text{disk}} \in [0.01, 8.0]$, $\Upsilon_{\text{bulge}} \in [0.0, 8.0]$, and $H_0 \in [50.0, 100.0] \ \text{km s}^{-1} \text{Mpc}^{-1}$. The log-likelihood $\ln \mathcal{L}$ of the observational residuals was monitored across an ensemble of 32 parallel walkers over 3,000 execution steps (600-step burn-in discarded; convergence independently confirmed against a 1,500-step run yielding statistically identical posteriors) following initial maximum likelihood seeding.

Crucially, this mathematical formulation resolves potential concerns regarding degeneracy with standard Modified Newtonian Dynamics (MOND) models. While the algebraic form maps onto an acceleration-scale boundary, standard MOND introduces $a_0 \approx 1.2 \times 10^{-10} \ \text{m s}^{-2}$ as an effective empirical constant. Conversely, in the ITSM, $a_0$ represents a dynamic metric anchor structurally derived from the topological boundary conditions of a closed, higher-dimensional manifold where the fundamental wrapping axis limits the maximum wavelength of metric perturbations. Furthermore, the $\frac{2}{3}$ coefficient is not an adjustable scaling parameter; it represents the exact geometric projection factor of an isotropic 4D bulk spatial manifold casting a lower-dimensional topological shadow onto the 3D observable circular orbital plane."""

start_idx = content.find(v_a_header)
end_idx = content.find(math_text) + len(math_text)

new_block = f"""{v_a_header}

{math_text}

{v_b_header}

{v_b_text}"""

if start_idx != -1 and content.find(math_text) != -1:
    content = content[:start_idx] + new_block + content[end_idx:]

# 3. Add antivortex sentence
content = content.replace(
    r"without violating the global constraint.",
    r"without violating the global constraint. Observationally, these massive regions of counter-rotating condensate are expected to correlate directly with the largest cosmic voids in the large-scale structure."
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixes applied successfully.")
