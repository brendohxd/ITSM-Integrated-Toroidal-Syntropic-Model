#!/usr/bin/env python3
"""Recolor original gallery figures: white/light paper -> void dark, 4:3 web cards.

Sources (scientific originals):
  Assets/Figures/itsm_3d_wake_analogy.png
  Assets/Figures/itsm_t3_fundamental_domain.png
  Assets/Figures/itsm_phonon_dispersion.png

Outputs:
  docs/assets/web/card_wake.{png,webp}
  docs/assets/web/card_t3.{png,webp}
  docs/assets/web/card_phonon.{png,webp}
  docs/assets/web/full_*.png  (full-resolution dark versions for lightbox)
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "Assets" / "Figures"
WEB = REPO / "docs" / "assets" / "web"

VOID = np.array([5, 6, 12], dtype=np.float32)
CARD = (1200, 900)


def white_to_void(im: Image.Image, threshold: float = 220.0, soft: float = 35.0) -> Image.Image:
    """Map near-white paper background to site void; keep plot colors."""
    rgba = im.convert("RGBA")
    arr = np.asarray(rgba).astype(np.float32)
    rgb = arr[..., :3]
    a = arr[..., 3:4] / 255.0

    # Luminance / "whiteness"
    mx = rgb.max(axis=2)
    mn = rgb.min(axis=2)
    # High max + low saturation => paper
    sat = (mx - mn) / np.maximum(mx, 1.0)
    paper = (mx >= threshold) & (sat < 0.12)
    # Soft falloff near threshold
    t0, t1 = threshold - soft, threshold
    soft_w = np.clip((mx - t0) / max(t1 - t0, 1.0), 0, 1)
    soft_w = soft_w * (sat < 0.18)
    blend = np.maximum(paper.astype(np.float32), soft_w * 0.85)[..., None]

    out_rgb = rgb * (1.0 - blend) + VOID * blend
    # Also darken pure greys that are still light
    grey = (sat < 0.08) & (mx > 160)
    gblend = ((mx - 160) / 95.0).clip(0, 1)[..., None] * grey[..., None].astype(np.float32)
    # Map light grey text axes to muted light so they stay visible on dark
    out_rgb = np.where(
        gblend > 0.01,
        out_rgb * (1 - 0.35 * gblend) + np.array([180, 190, 210])[None, None, :] * (0.35 * gblend),
        out_rgb,
    )

    out = np.concatenate([out_rgb.clip(0, 255), arr[..., 3:4]], axis=2).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def invert_light_ink_on_dark(im: Image.Image) -> Image.Image:
    """For plots: after killing white, boost ink that was dark-on-white to light-on-dark."""
    arr = np.asarray(im.convert("RGBA")).astype(np.float32)
    rgb = arr[..., :3]
    lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    # Dark ink on former white plots
    ink = lum < 90
    # Flip dark ink toward light ice/grey, preserve colored pixels (higher sat)
    mx = rgb.max(axis=2)
    mn = rgb.min(axis=2)
    sat = (mx - mn) / np.maximum(mx, 1.0)
    mono_ink = ink & (sat < 0.15)
    flipped = 255.0 - rgb
    # Keep flipped only for mono ink
    m = mono_ink[..., None].astype(np.float32)
    rgb2 = rgb * (1 - m) + flipped * m
    # Soften pure black remnants
    rgb2 = np.maximum(rgb2, 18.0)
    out = np.concatenate([rgb2.clip(0, 255), arr[..., 3:4]], axis=2).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def fit_card(im: Image.Image, size=CARD, pad_frac: float = 0.04) -> Image.Image:
    """Letterbox into 4:3 on void with margin so nothing is clipped."""
    cw, ch = size
    canvas = Image.new("RGBA", (cw, ch), (*map(int, VOID), 255))
    im = im.convert("RGBA")
    # usable area with padding
    pw, ph = int(cw * (1 - 2 * pad_frac)), int(ch * (1 - 2 * pad_frac))
    fitted = im.copy()
    fitted.thumbnail((pw, ph), Image.Resampling.LANCZOS)
    x = (cw - fitted.width) // 2
    y = (ch - fitted.height) // 2
    canvas.alpha_composite(fitted, (x, y))
    return canvas


def enhance(im: Image.Image) -> Image.Image:
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Color(im).enhance(1.05)
    return im


def process(src_name: str, stem: str, *, flip_ink: bool = True) -> None:
    path = SRC / src_name
    if not path.exists():
        raise FileNotFoundError(path)
    print(f"Processing {src_name} -> {stem}")
    im = Image.open(path)
    im = white_to_void(im)
    if flip_ink:
        im = invert_light_ink_on_dark(im)
    im = enhance(im)

    WEB.mkdir(parents=True, exist_ok=True)
    # Full-size lightbox version (max width 1800, preserve aspect)
    full = im.convert("RGB")
    full.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
    # Pad full to dark for clean edges
    fw, fh = full.size
    full_bg = Image.new("RGB", (fw, fh), tuple(map(int, VOID)))
    full_bg.paste(full, (0, 0))
    full_bg.save(WEB / f"full_{stem}.png", "PNG", optimize=True)
    full_bg.save(WEB / f"full_{stem}.webp", "WEBP", quality=88, method=6)

    card = fit_card(im)
    rgb = Image.new("RGB", card.size, tuple(map(int, VOID)))
    rgb.paste(card, mask=card.split()[-1])
    rgb.save(WEB / f"{stem}.png", "PNG", optimize=True)
    rgb.save(WEB / f"{stem}.webp", "WEBP", quality=86, method=6)
    print(f"  card {rgb.size}  full {full_bg.size}")


def main() -> None:
    jobs = [
        ("itsm_3d_wake_analogy.png", "card_wake", True),
        ("itsm_t3_fundamental_domain.png", "card_t3", True),
        ("itsm_phonon_dispersion.png", "card_phonon", True),
    ]
    for src, stem, flip in jobs:
        process(src, stem, flip_ink=flip)
    print(f"Done -> {WEB}")


if __name__ == "__main__":
    main()
