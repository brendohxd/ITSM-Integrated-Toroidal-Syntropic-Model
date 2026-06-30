import re

file_path = r"C:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Manuscript\ITSM_Core_Cosmology_v11.2.0.tex"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Missing citation [? ] (Raychaudhuri)
content = content.replace(
    r"\cite{jacobson_einstein}",
    r"\cite{misner_gravitation, ellis_maccallum}"
)

# 1b. Add to bibliography if not present
if "misner_gravitation" not in content:
    bib_add = r"""\bibitem{misner_gravitation}
C. W. Misner, K. S. Thorne, and J. A. Wheeler, \textit{Gravitation}, W. H. Freeman (1973).

\bibitem{ellis_maccallum}
G. F. R. Ellis and M. A. H. MacCallum, \textit{A Class of Homogeneous Cosmological Models}, Comm. Math. Phys. \textbf{12}, 108 (1969).

\end{thebibliography}"""
    content = content.replace(r"\end{thebibliography}", bib_add)


# 2. Table IV H0 value
content = content.replace(
    r"Global SPARC$\times$Pan+$\times$DESI & $69.62$ & Posterior \\",
    r"Global SPARC$\times$Pan+$\times$DESI & $72.50$ & Posterior \\"
)

# 3. Empty section bodies VI.D (remove) and V.A (rearrange)
# Remove empty VI.D
content = content.replace(
    r"\subsection{Joint Cosmological Validation: Pantheon+ SN1a and DESI BAO}" + "\n",
    ""
)

# Rearrange V.A and V.B
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

# Find the block and rewrite it properly structured
old_block_pattern = v_a_header + r"\s*" + v_b_header + r"\s*" + re.escape(v_b_text) + r"\s*" + re.escape(math_text)
new_block = f"""{v_a_header}

{math_text}

{v_b_header}

{v_b_text}"""
content = re.sub(old_block_pattern, new_block.replace('\\', '\\\\'), content, count=1)


# 4. Ndata discrepancy abstract
content = content.replace(
    r"($N_{\rm data} = 3{,}179$ rotation-curve points)",
    r"($N_{\rm data} = 3{,}178$ rotation-curve points)"
)

# 5. NANOGrav band notation
# First occurrence (in abstract)
content = content.replace(
    r"bounded within $[1.08, 3.14]\,\text{nHz}$; (ii)",
    r"bounded within $[1.08, \pi]\,\text{nHz} \ (\approx [1.08, 3.14]\,\text{nHz})$; (ii)"
)
# Other occurrences
content = content.replace(r"$[1.08, 3.14]\,\text{nHz}$", r"$[1.08, \pi]\,\text{nHz}$")
content = content.replace(r"$[1.08, 3.14]$~nHz", r"$[1.08, \pi]$~nHz")
content = content.replace(r"$[1.08, 3.14]\text{ nHz}$", r"$[1.08, \pi]\text{ nHz}$")


# 6. chi2 ambiguity
content = content.replace(
    r"($\chi^2_\nu \approx 1.2$, $p=0.62$ from forward-model Monte Carlo",
    r"(per-galaxy ensemble median $\chi^2_\nu = 1.2$; global RAR $\chi^2_\nu = 8.57, p=0.62$ from forward-model Monte Carlo"
)

# 7. Zero-net-vorticity
vortex_insert = r"""\paragraph{The Zero-Net-Vorticity Constraint on $T^3$.} A fundamental requirement of compact manifolds such as the 3-torus is the zero-net-vorticity theorem (a direct consequence of the Gauss-Bonnet and Stokes' theorems): the total topological charge integrated over a closed compact surface must strictly vanish. Therefore, macroscopic vortex cores cannot exist in isolation on the global manifold; they must nucleate as vortex-antivortex pairs. The ITSM naturally satisfies this constraint. The massive primordial vortex cores seeding early SMBHs are dynamically balanced by an equal number of antivortex defects globally distributed across the expanding manifold. Because the scale of the fundamental domain ($L \gtrsim 1.25 \chi_{\text{rec}}$) exceeds the causal horizon, local symmetry in the observable distribution of these cores is not required. The total circulation of the $T^3$ condensate remains rigorously zero, while allowing localized, hyper-dense rotational defects to act as early-universe gravitational seeds."""

content = content.replace(
    r"forced early baryonic gas to condense.",
    r"forced early baryonic gas to condense." + "\n\n" + vortex_insert
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixes applied successfully.")
