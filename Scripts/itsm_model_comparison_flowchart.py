"""
itsm_model_comparison_flowchart.py
------------------------------------
Publication figure: ΛCDM vs MOND vs ITSM structured comparison table.
Journal standard: white bg, serif, 600 dpi.
Output: Assets/Figures/itsm_model_comparison_flowchart.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

plt.rcParams.update({
    "font.family": "serif", "mathtext.fontset": "cm",
    "font.size": 9, "figure.facecolor": "white",
    "axes.facecolor": "white", "savefig.facecolor": "white",
    "text.usetex": False,
})

# ── Data ─────────────────────────────────────────────────────────────────────
questions = [
    "What explains\ngalactic rotation\ncurves?",
    "Origin of $a_0$\n($1.2\\times10^{-10}$ m/s$^2$)?",
    "Hubble Tension\n($5\\sigma$ discrepancy)?",
    "Bullet Cluster\nmass offset?",
    "NANOGrav GWB\nspectral structure?",
    "JWST $z>14$\nmassive galaxies?",
]

lcdm = [
    "Collisionless NFW\ndark matter halo\n(3 free params/galaxy)",
    "Unexplained —\nempirical coincidence\nwith $H_0$",
    "Unresolved —\nnew physics or\nsystematics required",
    "Collisionless DM\nhalo passes through\nbaryonic gas",
    "Featureless SMBHB\npower-law\n$h_c \\propto f^{-2/3}$",
    "Over-production\nproblem — tension\nwith $\\Lambda$CDM",
]

mond = [
    "Modified gravity\n$\\mu(g/a_0)$ interpolation\n(1 free param/galaxy)",
    "Free empirical\nconstant — fit\nto SPARC data",
    "Not addressed\n(no cosmological\nextension)",
    "Requires additional\nsterile neutrinos\n(ad hoc)",
    "Not addressed\n(non-relativistic\nframework)",
    "Not addressed\n(no early-universe\nprediction)",
]

itsm = [
    "Superfluid plenum\nphonon coupling\n$g_{\\rm tot}=g_{\\rm bar}+\\frac{2}{3}\\sqrt{g_{\\rm bar}a_0}$",
    "Derived: $a_0=cH_0/2\\pi$\nfrom $T^3$ topology\n(zero free params)",
    "$H_t^{\\rm pred}=72.97$ km/s/Mpc\nfrom Casimir ratio $13/12$\n$0.07\\sigma$ from SH0ES",
    "ICM acoustic drag;\nstall $v_c\\approx600$ km/s\nfrom toroidal geometry",
    "Lorentzian resonance\npredicted in $[1.08,\\pi]$ nHz\n(falsifiable)",
    "Predicted: enhanced\nearly structure from\nsyntropic source $Q^\\nu$",
]

# ── Palette (clean, print-safe) ───────────────────────────────────────────────
# Ratings: 0=poor/absent, 1=partial, 2=addresses
ratings_lcdm = [1, 0, 0, 2, 1, 0]
ratings_mond  = [2, 0, 0, 0, 0, 0]
ratings_itsm  = [2, 2, 2, 2, 2, 2]

GOOD      = "#d4edda"   # soft sage green   — addresses / explains
PARTIAL   = "#dce8f5"   # cool light steel  — partially addresses
POOR      = "#f8dede"   # soft rose         — does not address
ITSM_GOOD = "#c5dff5"   # medium sky blue   — ITSM decisive prediction

col_lcdm = {0: POOR,    1: PARTIAL,   2: GOOD}
col_mond  = {0: POOR,    1: PARTIAL,   2: GOOD}
col_itsm  = {0: POOR,    1: ITSM_GOOD, 2: ITSM_GOOD}

# Header bar colors (professional, print-safe)
hdr_q    = "#2e2e2e"   # near-black
hdr_lcdm = "#484848"   # charcoal grey
hdr_mond = "#5a6e4a"   # muted forest green  (neutral — no advantage)
hdr_itsm = "#1b4e8c"   # rich navy blue

# Cell edge color
EDGE_COLOR = "#cccccc"
EDGE_LW    = 0.6

# ── Figure layout ─────────────────────────────────────────────────────────────
nrows = len(questions)

# 13% top margin for title clearance, 6% bottom for legend
fig = plt.figure(figsize=(13, 9.0))
ax = fig.add_axes([0.0, 0.06, 1.0, 0.86])   # top = 0.92 in figure coords
ax.axis("off")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

col_widths = [0.155, 0.268, 0.268, 0.309]   # question | ΛCDM | MOND | ITSM
col_xs = [0.0]
for w in col_widths[:-1]:
    col_xs.append(col_xs[-1] + w)

row_h    = 1.0 / (nrows + 1.2)
header_y = 1.0 - row_h          # header row sits at very top of axes

def draw_cell(ax, x, y, w, h, text, bg, fg="black", bold=False, fontsize=8.2):
    rect = mpatches.FancyBboxPatch(
        (x + 0.0025, y + 0.005), w - 0.005, h - 0.010,
        boxstyle="round,pad=0.004", linewidth=EDGE_LW,
        edgecolor=EDGE_COLOR, facecolor=bg,
        transform=ax.transAxes, clip_on=False)
    ax.add_patch(rect)
    weight = "bold" if bold else "normal"
    ax.text(x + w / 2, y + h / 2, text,
            transform=ax.transAxes, ha="center", va="center",
            fontsize=fontsize, color=fg, fontweight=weight,
            linespacing=1.38)

# ── Header row ────────────────────────────────────────────────────────────────
draw_cell(ax, col_xs[0], header_y, col_widths[0], row_h,
          "Question", hdr_q, fg="white", bold=True, fontsize=9.5)
for j, (label, color) in enumerate([
        ("$\\Lambda$CDM",   hdr_lcdm),
        ("MOND",            hdr_mond),
        ("ITSM\n(This Work)", hdr_itsm)]):
    draw_cell(ax, col_xs[j + 1], header_y, col_widths[j + 1], row_h,
              label, color, fg="white", bold=True, fontsize=10.5)

# ── Data rows ─────────────────────────────────────────────────────────────────
for i, (q, l, m, t) in enumerate(zip(questions, lcdm, mond, itsm)):
    y = header_y - (i + 1) * row_h

    # Alternate very-light stripe on question column for readability
    q_bg = "#efefef" if i % 2 == 0 else "#f7f7f7"
    draw_cell(ax, col_xs[0], y, col_widths[0], row_h,
              q, q_bg, fg="#222222", fontsize=8.2, bold=False)
    draw_cell(ax, col_xs[1], y, col_widths[1], row_h,
              l, col_lcdm[ratings_lcdm[i]], fg="#2a2a2a", fontsize=7.9)
    draw_cell(ax, col_xs[2], y, col_widths[2], row_h,
              m, col_mond[ratings_mond[i]],  fg="#2a2a2a", fontsize=7.9)
    draw_cell(ax, col_xs[3], y, col_widths[3], row_h,
              t, col_itsm[ratings_itsm[i]],  fg="#0b3c6e", fontsize=7.9)

# ── Legend ─────────────────────────────────────────────────────────────────────
patches = [
    mpatches.Patch(facecolor=GOOD,      edgecolor=EDGE_COLOR, label="Addresses / explains"),
    mpatches.Patch(facecolor=PARTIAL,   edgecolor=EDGE_COLOR, label="Partially addresses"),
    mpatches.Patch(facecolor=POOR,      edgecolor=EDGE_COLOR, label="Does not address"),
    mpatches.Patch(facecolor=ITSM_GOOD, edgecolor=EDGE_COLOR, label="ITSM zero-param prediction"),
]
ax.legend(handles=patches, loc="lower center",
          bbox_to_anchor=(0.5, -0.065),
          ncol=4, fontsize=8.2, frameon=True,
          edgecolor="#888888", framealpha=1.0,
          columnspacing=1.2, handlelength=1.4)

# ── Title — placed in figure space well above the axes ───────────────────────
# axes top = 0.92; title at 0.985 leaves ~6.5% clear gap
fig.text(0.5, 0.985,
         "ITSM vs. $\\Lambda$CDM vs. MOND: Key Cosmological Questions",
         ha="center", va="top",
         fontsize=13.0, fontweight="bold", color="#111111")

out = Path(__file__).parent.parent / "Assets" / "Figures" / "itsm_model_comparison_flowchart.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, bbox_inches="tight")
print(f"Saved: {out}")
