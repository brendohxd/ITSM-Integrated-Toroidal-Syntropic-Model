#!/usr/bin/env python3
"""Build web-optimized ITSM site images with correct aspect ratios.

Sources (never overwritten): Assets/Figures/ (fallback: docs/assets/)
Outputs: docs/assets/web/

Targets (plan):
  hero_toroidal     1920×1080  16:9   (prefer render_itsm_identity_figures.py)
  card_wake         1200×900   4:3
  card_t3           1000×750   4:3
  card_phonon       1000×750   4:3
  split_fluid       1400×900  ~14:9
  full_card_*       2× card for lightbox

Composition: letterbox/pillarbox on void (#05060c), soft vignette, optional
gold hairline. Prefer contain over brutal crop for schematics.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

REPO = Path(__file__).resolve().parents[2]
SRC_PRIMARY = REPO / "Assets" / "Figures"
SRC_FALLBACK = REPO / "docs" / "assets"
OUT = REPO / "docs" / "assets" / "web"

VOID = (5, 6, 12, 255)
GOLD = (212, 176, 106, 160)


def resolve_src(name: str) -> Path | None:
    for root in (SRC_PRIMARY, SRC_FALLBACK):
        p = root / name
        if p.exists():
            return p
    return None


def fit_on_canvas(
    im: Image.Image,
    canvas_w: int,
    canvas_h: int,
    *,
    mode: str = "contain",
    pad_color: tuple[int, int, int, int] = VOID,
    scale_boost: float = 0.92,
) -> Image.Image:
    im = im.convert("RGBA")
    canvas = Image.new("RGBA", (canvas_w, canvas_h), pad_color)
    iw, ih = im.size
    if mode == "cover":
        scale = max(canvas_w / iw, canvas_h / ih)
    else:
        scale = min(canvas_w / iw, canvas_h / ih) * scale_boost
    nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
    x = (canvas_w - nw) // 2
    y = (canvas_h - nh) // 2
    canvas.alpha_composite(resized, (x, y))
    return canvas


def vignette(im: Image.Image, strength: float = 0.32) -> Image.Image:
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    cx, cy = w // 2, h // 2
    max_r = (cx**2 + cy**2) ** 0.5
    px = mask.load()
    step = 2
    for y in range(0, h, step):
        for x in range(0, w, step):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / max_r
            v = int(255 * max(0.0, 1.0 - strength * (d**1.55)))
            for dy in range(step):
                for dx in range(step):
                    xx, yy = x + dx, y + dy
                    if xx < w and yy < h:
                        px[xx, yy] = v
    mask = mask.filter(ImageFilter.GaussianBlur(radius=max(w, h) // 36))
    dark = Image.new("RGBA", (w, h), VOID)
    return Image.composite(im, dark, mask)


def gold_frame(im: Image.Image, inset: int = 12) -> Image.Image:
    out = im.copy()
    w, h = out.size
    line = Image.new("RGBA", (w - 2 * inset, 1), GOLD)
    out.alpha_composite(line, (inset, inset))
    out.alpha_composite(line, (inset, h - inset - 1))
    vline = Image.new("RGBA", (1, h - 2 * inset), GOLD)
    out.alpha_composite(vline, (inset, inset))
    out.alpha_composite(vline, (w - inset - 1, inset))
    return out


def enhance(im: Image.Image) -> Image.Image:
    im = ImageEnhance.Contrast(im).enhance(1.07)
    im = ImageEnhance.Color(im).enhance(1.05)
    im = ImageEnhance.Brightness(im).enhance(0.99)
    return im


def save_pair(im: Image.Image, stem: str, *, webp_quality: int = 82) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rgb = Image.new("RGB", im.size, VOID[:3])
    if im.mode == "RGBA":
        rgb.paste(im, mask=im.split()[-1])
    else:
        rgb.paste(im.convert("RGB"))
    png_path = OUT / f"{stem}.png"
    webp_path = OUT / f"{stem}.webp"
    rgb.save(png_path, "PNG", optimize=True)
    rgb.save(webp_path, "WEBP", quality=webp_quality, method=6)
    kb = webp_path.stat().st_size // 1024
    print(f"  wrote {stem}: {rgb.size[0]}x{rgb.size[1]}  webp={kb}KB")


def compose(
    src: Path,
    size: tuple[int, int],
    *,
    mode: str = "contain",
    frame: bool = False,
    scale_boost: float = 0.92,
    vignette_s: float = 0.28,
) -> Image.Image:
    im = Image.open(src)
    composed = fit_on_canvas(
        im, size[0], size[1], mode=mode, scale_boost=scale_boost
    )
    composed = enhance(composed)
    composed = vignette(composed, strength=vignette_s)
    if frame:
        composed = gold_frame(composed, inset=max(10, min(size) // 80))
    return composed


def build() -> None:
    print(f"Primary source: {SRC_PRIMARY}")
    print(f"Fallback:       {SRC_FALLBACK}")
    print(f"Output:         {OUT}")

    # Cards + split from scientific archives (hero from identity renderer preferred)
    jobs = [
        {
            "src": "itsm_3d_wake_analogy.png",
            "stem": "card_wake",
            "full_stem": "full_card_wake",
            "size": (1200, 900),
            "full_size": (2000, 1500),
            "mode": "contain",
            "frame": True,
            "scale_boost": 0.94,
            "q": 80,
        },
        {
            "src": "itsm_t3_fundamental_domain.png",
            "stem": "card_t3",
            "full_stem": "full_card_t3",
            "size": (1000, 750),
            "full_size": (2000, 1500),
            "mode": "contain",
            "frame": True,
            "scale_boost": 0.90,
            "q": 82,
        },
        {
            "src": "itsm_phonon_dispersion.png",
            "stem": "card_phonon",
            "full_stem": "full_card_phonon",
            "size": (1000, 750),
            "full_size": (2000, 1500),
            "mode": "contain",
            "frame": True,
            "scale_boost": 0.88,
            "q": 82,
        },
        {
            "src": "itsm_3d_fluid_dynamics_publication.png",
            "stem": "split_fluid",
            "full_stem": None,
            "size": (1400, 900),
            "full_size": None,
            "mode": "cover",
            "frame": False,
            "scale_boost": 1.0,
            "q": 78,
            "vignette": 0.34,
        },
    ]

    for job in jobs:
        path = resolve_src(job["src"])
        if path is None:
            print(f"  SKIP missing {job['src']}")
            continue
        print(f"Building {job['stem']} from {path.name}...")
        card = compose(
            path,
            job["size"],
            mode=job["mode"],
            frame=job.get("frame", False),
            scale_boost=job.get("scale_boost", 0.92),
            vignette_s=job.get("vignette", 0.28),
        )
        save_pair(card, job["stem"], webp_quality=job.get("q", 82))
        if job.get("full_stem") and job.get("full_size"):
            full = compose(
                path,
                job["full_size"],
                mode=job["mode"],
                frame=job.get("frame", False),
                scale_boost=job.get("scale_boost", 0.92),
                vignette_s=job.get("vignette", 0.28),
            )
            save_pair(full, job["full_stem"], webp_quality=job.get("q", 82))

    # Optional legacy reframe (only if identity hero missing — do not clobber)
    hero = OUT / "hero_toroidal.png"
    if not hero.exists():
        path = resolve_src("itsm_3d_toroidal_manifold.png")
        if path:
            print("Building fallback hero_toroidal from manifold archive...")
            h = compose(
                path,
                (1920, 1080),
                mode="contain",
                frame=False,
                scale_boost=0.95,
                vignette_s=0.38,
            )
            save_pair(h, "hero_toroidal", webp_quality=80)
    else:
        print("  keep existing hero_toroidal (identity renderer)")

    print("Done.")


if __name__ == "__main__":
    build()
