#!/usr/bin/env python3
"""Shared Zenodo metadata for ITSM recovery-era deposits.

Inclusive descriptions: open to cosmologists, quantum-field / topology
readers, independent researchers, and reproducibility-minded users.
Claim boundaries stay honest; language stays welcoming.
"""

from __future__ import annotations

# Identity (keep in sync across deposits)
ORCID = "0009-0007-4177-2612"
ORCID_URL = f"https://orcid.org/{ORCID}"
WEBSITE = "https://www.itsm-cosmology.org"
GITHUB = (
    "https://github.com/brendohxd/ITSM-Integrated-Toroidal-Syntropic-Model"
)
CONTACT_EMAIL = "brendon.boyd@itsm-cosmology.org"
AFFILIATION = "Independent Researcher, Burswood, Western Australia, Australia"

CREATOR = {
    "name": "Boyd, Brendon",
    "affiliation": AFFILIATION,
    "orcid": ORCID,
}


def _links_footer_html() -> str:
    return f"""
<p><strong>Author &amp; links</strong></p>
<ul>
<li>Brendon Boyd — ORCID:
<a href="{ORCID_URL}">{ORCID}</a></li>
<li>Project site:
<a href="{WEBSITE}">{WEBSITE}</a>
(model explorer and public materials)</li>
<li>Source code &amp; gates:
<a href="{GITHUB}">GitHub — ITSM Integrated Toroidal-Syntropic Model</a>
(branch <code>recovery/v12-core-architecture</code>)</li>
<li>Contact:
<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></li>
</ul>
<p><em>Open science:</em> anyone may inspect, reproduce, critique, or build on
these materials under the stated license. Feedback from students, independent
researchers, and specialists is welcome. Claim boundaries below are written to
protect readers—not to exclude interest.</p>
""".strip()


def _related_identifiers() -> list[dict]:
    # ORCID lives on creators[].orcid (not as a related_identifier).
    return [
        {
            "identifier": GITHUB,
            "relation": "isSupplementTo",
            "resource_type": "software",
            "scheme": "url",
        },
        {
            "identifier": WEBSITE,
            "relation": "isDocumentedBy",
            "resource_type": "other",
            "scheme": "url",
        },
        {
            "identifier": "10.5281/zenodo.18808348",
            "relation": "isPartOf",
            "resource_type": "publication-article",
            "scheme": "doi",
        },
    ]


def _base_metadata(
    *,
    title: str,
    description: str,
    upload_type: str,
    version: str,
    keywords: list[str],
    notes: str | None = None,
) -> dict:
    meta: dict = {
        "title": title,
        "upload_type": upload_type,
        "description": description.strip(),
        "creators": [CREATOR],
        "keywords": keywords,
        "license": "cc-by-4.0",
        "access_right": "open",
        "version": version,
        "language": "eng",
        "related_identifiers": _related_identifiers(),
    }
    if notes:
        meta["notes"] = notes
    return meta


# ---------------------------------------------------------------------------
# Deposit specs (keys match upload_recovery_deposits.py / draft IDs)
# ---------------------------------------------------------------------------

DEPOSITS: dict[str, dict] = {
    "cbr001": {
        "zip_glob": "ITSM_CBR-001_Casimir_T3_*.zip",
        "deposition_id": 21753798,  # new-version draft (v1 was 21745260 published)
        "metadata": _base_metadata(
            title=(
                "ITSM CBR-001: Casimir stress on a rectangular flat 3-torus "
                "and free-field biaxial backreaction (open research package)"
            ),
            upload_type="software",
            version="1.0.0",
            keywords=[
                "Casimir effect",
                "cosmic topology",
                "three-torus",
                "T3",
                "Bianchi cosmology",
                "anisotropic expansion",
                "open science",
                "reproducible research",
                "ITSM",
                "Integrated Toroidal-Syntropic Model",
            ],
            notes=(
                "Part of the ITSM recovery programme. Suitable for readers in "
                "cosmology, quantum fields on compact spaces, numerical GR, and "
                "open scientific computing. Does not require prior commitment to "
                "the full ITSM framework."
            ),
            description=f"""
<p>This open research package documents a <strong>validated numerical study</strong>
of vacuum (Casimir) stress for a free massless scalar field on a
<strong>rectangular flat three-torus</strong> (<em>T</em><sup>3</sup>), and of
how that stress backreacts on simple biaxial expansion.</p>

<p><strong>Who it is for.</strong> Cosmologists and relativists interested in
topology and anisotropic stress; quantum-field and Casimir practitioners;
students and independent researchers learning reproducible gate-style
workflows; anyone auditing historical “13/12” or free-field Hubble packaging.
No assumption that the full Integrated Toroidal-Syntropic Model (ITSM) is
correct—only that the calculations here are clear and checkable.</p>

<p><strong>What is included.</strong></p>
<ul>
<li>Lattice Casimir energy density and directional pressures (Stage&nbsp;1)</li>
<li>Biaxial shape scan of anisotropic stress (Stage&nbsp;2)</li>
<li>Free-field biaxial backreaction on a positive de&nbsp;Sitter testbed
(Stage&nbsp;3A)</li>
<li>Systematic search for the historically discussed ratio
<em>H<sub>t</sub>/H<sub>p</sub> = 13/12</em> (Stage&nbsp;3B)</li>
<li>Scripts, outputs, and a short deposit README for reproduction under
<code>conda</code> env <code>itsm_env</code></li>
</ul>

<p><strong>What the results support (honest boundary).</strong>
Shape-dependent anisotropic free-field Casimir stress is a concrete mechanism.
Under the free-field search reported here, passages near 13/12 are at most
<strong>transient</strong>—not a quasi-plateau or late-time attractor. Persistent
anisotropy, if it exists in a fuller theory, would need additional derived
stress (open programme), not free-field packaging alone.</p>

<p><strong>What this deposit does <em>not</em> claim.</strong>
A parameter-free resolution of the Hubble tension; a derivation of the galactic
acceleration scale from topology alone; or a completed cubic cosmology
compatible with all CMB topology bounds. Those topics are discussed elsewhere
with separate claim hygiene.</p>

<p><strong>Related paper draft (not required to use this package).</strong>
Working manuscript directory
<code>papers/P2-Rectangular-T3-Casimir/</code> on GitHub; arXiv submission is
deferred pending endorsement. The numerical science stands on this gate package.</p>

{_links_footer_html()}
""",
        ),
    },
    "uvir003": {
        "zip_glob": "ITSM_UVIR-003_LocalFourLeg_*.zip",
        "deposition_id": 21753799,  # new-version draft (v1 was 21745270 published)
        "metadata": _base_metadata(
            title=(
                "ITSM UVIR-003: local four-leg kernel, kinematic deformation, "
                "and adiabatic packet proxy (open intermediate research slice)"
            ),
            upload_type="software",
            version="0.10.0-pre",
            keywords=[
                "effective field theory",
                "cosmological perturbations",
                "preferred frame",
                "infrared-ultraviolet matching",
                "open science",
                "reproducible research",
                "ITSM",
                "UVIR-003",
                "Integrated Toroidal-Syntropic Model",
            ],
            notes=(
                "Intermediate recovery-era gate slice after manuscript freeze "
                "12.0-alpha.9. Intended for EFT / cosmology readers and for "
                "anyone tracking how local kernels are (and are not) turned into "
                "observables. Not a finished unitarity proof."
            ),
            description=f"""
<p>This open package is an <strong>intermediate research slice</strong> of the
ITSM <strong>UVIR-003</strong> programme: building a local exchange-plus-contact
four-leg kernel in a preferred-frame effective description, then stress-testing
it under kinematic deformation and defining a careful
<strong>local adiabatic packet average</strong> (a transparency step—not a
cosmological S-matrix).</p>

<p><strong>Who it is for.</strong> Researchers in cosmological effective field
theory, perturbations, and multi-field systems; numerical-methods readers;
independent investigators following the recovery branch; critics who want
machine-checkable gate statuses rather than prose claims alone.</p>

<p><strong>What is included (subgate record).</strong></p>
<ul>
<li><code>PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL</code>
— local frozen-time four-leg assembly on the regular-tetrahedral slice
(aligned with CoreRecovery freeze 12.0-alpha.9)</li>
<li><code>PASS_FOUR_LEG_KINEMATIC_DEFORMATION_AUDIT</code>
— off-tetrahedron isosceles-disphenoid family, including a denser approach
toward the homogeneous edge</li>
<li><code>PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION</code>
— Gaussian packet proxy of the local kernel in log-momentum; narrow packets
recover the on-shell value</li>
<li>Supporting scripts, JSON/CSV summaries, and gate notes</li>
</ul>

<p><strong>What this supports.</strong>
A documented, reproducible local kernel pipeline with explicit scientific
boundaries. Deformation and packet steps reduce the risk of silently treating a
frozen kernel as a finished scattering amplitude.</p>

<p><strong>What is deliberately not claimed yet.</strong>
Cosmological asymptotic states or an S-matrix; optical-theorem / partial-wave
unitarity bounds; a strong-coupling scale or physical cutoff; unlock of the
downstream matter-matching gate (MAT-001). Those remain open research steps.</p>

<p><strong>How to engage.</strong> Reproduce under <code>itsm_env</code>, open
issues or critiques via the project contact or GitHub, and treat status lines
in the JSON summaries as the machine-readable source of truth for this slice.</p>

{_links_footer_html()}
""",
        ),
    },
    "recovery_docs": {
        "zip_glob": "ITSM_Recovery_ClaimHygiene_*.zip",
        "deposition_id": 21745276,
        "metadata": _base_metadata(
            title=(
                "ITSM recovery-era open research archive: master plan, "
                "publishing firewall, and P1 scale-matching reconstruction note"
            ),
            upload_type="other",
            version="1.3.0",
            keywords=[
                "open science",
                "research data management",
                "claim hygiene",
                "scientific integrity",
                "cosmology",
                "modified gravity",
                "MOND",
                "ITSM",
                "Integrated Toroidal-Syntropic Model",
                "preprint hygiene",
            ],
            notes=(
                "Workflow and claim-hygiene documentation for the recovery "
                "programme. Written for collaborators, reviewers, and curious "
                "readers—not only for specialists already inside the project."
            ),
            description=f"""
<p>This archive collects the <strong>open workflow and claim-hygiene
documents</strong> for the recovery-era Integrated Toroidal-Syntropic Model
(ITSM) programme on branch
<code>recovery/v12-core-architecture</code>.</p>

<p><strong>Who it is for.</strong> Collaborators and reviewers who need a single
entry point; researchers in modified gravity, MOND-adjacent phenomenology, and
cosmic topology who want to see how claims are classified; independent
researchers and students learning how to separate identity, mechanisms, and
predictions; anyone comparing historical overclaims with the present recovery
discipline.</p>

<p><strong>What is included.</strong></p>
<ul>
<li><strong>Master research plan</strong> — ideal identity pillars, three-bucket
claim disposition (hard ban vs packaging-open vs reassess), open-options rule
(untested ≠ banned), session checklist</li>
<li><strong>Selective publishing firewall</strong> — abstract packaging bans
and paper sequence (P1–P4 roles)</li>
<li><strong>P1 scale-matching reconstruction note</strong>
(<code>P1-Scale-Matching-Reconstruction</code>) — no-go results for common
geometric shortcuts to the MOND scale and for treating a projector ratio as
<em>C</em><sub>obs</sub>, plus the field-rescaling invariant
<em>C</em><sub>obs</sub>; versioned share PDF
<code>Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v*.pdf</code></li>
<li>Pointers to core architecture / recovery plan documents</li>
</ul>

<p><strong>Spirit of the archive.</strong>
Preserve the original intuitive building blocks of the programme (open
thermodynamics / syntropy–entropy dual, toroidal geometry, fluid wake,
winding–resonance ideas) as research identity, while refusing false packaging.
Routes that have not been tested stay <strong>open</strong> for careful work;
only proven-false packaging is hard-banned. SWNT-style principles are not forced
if mathematics shows otherwise—they are places to look when a core route stalls.</p>

<p><strong>Related deposits (separate records).</strong>
Numerical CBR-001 Casimir package and UVIR-003 intermediate kernel package are
archived as independent software deposits so documentation and code can evolve
on different schedules. P2 (Casimir manuscript) arXiv is deferred pending
endorsement; the CBR-001 package carries the validated numerics today.</p>

{_links_footer_html()}
""",
        ),
    },
}
