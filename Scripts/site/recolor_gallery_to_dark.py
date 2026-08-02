#!/usr/bin/env python3
"""Recolor gallery figures: paper white + slate grey faces -> true void dark.

Sources (scientific originals):
  Assets/Figures/itsm_3d_wake_analogy.png
  Assets/Figures/itsm_t3_fundamental_domain.png
  Assets/Figures/itsm_phonon_dispersion.png

Outputs:
  docs/assets/web/card_*.{png,webp}   — 4:3 full-bleed web cards
  docs/assets/web/full_*.{png,webp} — high-res lightbox versions
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "Assets" / "Figures"
WEB = REPO / "docs" / "assets" / "web"

VOID = np.array([5, 6, 12], dtype=np.float32)
CARD = (1400, 1050)  # 4:3, larger than before for retina cards
FULL_MAX = 2000


def white_and_grey_to_void(im: Image.Image) -> Image.Image:
    """Map paper white AND mid-grey figure faces to void; keep saturated plot colors."""
    rgba = im.convert("RGBA")
    arr = np.asarray(rgba).astype(np.float32)
    rgb = arr[..., :3]
    alpha = arr[..., 3:4]

    mx = rgb.max(axis=2)
    mn = rgb.min(axis=2)
    sat = (mx - mn) / np.maximum(mx, 1.0)
    lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]

    # Near-white paper
    paper_w = (mx >= 200) & (sat < 0.14)
    # Mid / light greys (matplotlib face, axes background, light grid wash)
    paper_g = (sat < 0.12) & (lum >= 45) & (lum < 200)
    # Soft blend near white threshold for anti-aliased edges
    soft_w = np.clip((mx - 175) / 45.0, 0, 1) * (sat < 0.16)
    soft_g = np.clip((lum - 40) / 35.0, 0, 1) * (sat < 0.14) * (lum < 200)

    blend = np.maximum.reduce(
        [
            paper_w.astype(np.float32),
            paper_g.astype(np.float32) * 0.95,
            soft_w * 0.9,
            soft_g * 0.85,
        ]
    )[..., None]

    out_rgb = rgb * (1.0 - blend) + VOID * blend

    # Dim residual light greys that survived (axis chrome, soft fills)
    residual = (sat < 0.10) & (lum > 35) & (lum < 160)
    rblend = ((lum - 35) / 125.0).clip(0, 1)[..., None] * residual[..., None].astype(
        np.float32
    )
    out_rgb = out_rgb * (1 - 0.75 * rblend) + VOID * (0.75 * rblend)

    out = np.concatenate([out_rgb.clip(0, 255), alpha], axis=2).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def invert_mono_ink(im: Image.Image) -> Image.Image:
    """Flip dark monochrome ink (axes, labels, ticks) to light ice-grey on dark bg.

    Conservative thresholds: only near-black low-sat pixels so anti-aliased
    glyph edges and colored science content are not mangled.
    """
    arr = np.asarray(im.convert("RGBA")).astype(np.float32)
    rgb = arr[..., :3]
    lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    mx = rgb.max(axis=2)
    mn = rgb.min(axis=2)
    sat = (mx - mn) / np.maximum(mx, 1.0)

    # Near-black mono ink only (axes spines, tick labels, grid on paper plots)
    mono_ink = (lum < 70) & (sat < 0.12)
    strength = ((70 - lum) / 70.0).clip(0, 1) ** 1.2 * mono_ink.astype(np.float32)
    strength = strength[..., None]

    light = np.array([200.0, 208.0, 222.0], dtype=np.float32)
    rgb2 = rgb * (1 - strength) + light * strength

    out = np.concatenate([rgb2.clip(0, 255), arr[..., 3:4]], axis=2).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def content_bbox(im: Image.Image, dark_thresh: float = 22.0, pad: int = 8) -> tuple[int, int, int, int]:
    """Tight bbox around non-void content so we don't double-letterbox."""
    arr = np.asarray(im.convert("RGB")).astype(np.float32)
    lum = arr.mean(axis=2)
    # Content = not nearly void
    mask = lum > dark_thresh
    # Also treat highly saturated pixels as content even if dark
    mx = arr.max(axis=2)
    mn = arr.min(axis=2)
    sat = (mx - mn) / np.maximum(mx, 1.0)
    mask |= sat > 0.12
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return (0, 0, im.width, im.height)
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(im.width, x1 + pad)
    y1 = min(im.height, y1 + pad)
    return (x0, y0, x1, y1)


def fit_cover(im: Image.Image, size=CARD, void_rgb=None) -> Image.Image:
    """Scale to cover size (center-crop), then paste on void — full-bleed card."""
    if void_rgb is None:
        void_rgb = tuple(int(v) for v in VOID)
    cw, ch = size
    im = im.convert("RGBA")
    # Scale so image covers target
    scale = max(cw / im.width, ch / im.height)
    nw, nh = max(1, int(round(im.width * scale))), max(1, int(round(im.height * scale)))
    scaled = im.resize((nw, nh), Image.Resampling.LANCZOS)
    # Center crop
    x0 = (nw - cw) // 2
    y0 = (nh - ch) // 2
    cropped = scaled.crop((x0, y0, x0 + cw, y0 + ch))
    canvas = Image.new("RGBA", (cw, ch), (*void_rgb, 255))
    canvas.alpha_composite(cropped, (0, 0))
    return canvas


def fit_contain_tight(im: Image.Image, size=CARD, pad_frac: float = 0.02) -> Image.Image:
    """Letterbox with minimal pad — used when cover would crop science content badly."""
    void_rgb = tuple(int(v) for v in VOID)
    cw, ch = size
    canvas = Image.new("RGBA", (cw, ch), (*void_rgb, 255))
    im = im.convert("RGBA")
    pw, ph = int(cw * (1 - 2 * pad_frac)), int(ch * (1 - 2 * pad_frac))
    fitted = im.copy()
    fitted.thumbnail((pw, ph), Image.Resampling.LANCZOS)
    x = (cw - fitted.width) // 2
    y = (ch - fitted.height) // 2
    canvas.alpha_composite(fitted, (x, y))
    return canvas


def enhance(im: Image.Image) -> Image.Image:
    im = ImageEnhance.Contrast(im).enhance(1.12)
    im = ImageEnhance.Color(im).enhance(1.08)
    im = ImageEnhance.Brightness(im).enhance(1.03)
    return im


def process(src_name: str, stem: str, *, mode: str = "cover") -> None:
    path = SRC / src_name
    if not path.exists():
        raise FileNotFoundError(path)
    print(f"Processing {src_name} -> {stem} ({mode})")
    im = Image.open(path)
    im = white_and_grey_to_void(im)
    im = invert_mono_ink(im)
    im = enhance(im)

    # Crop empty void margins before framing
    box = content_bbox(im)
    im = im.crop(box)
    print(f"  content crop {box} -> {im.size}")

    WEB.mkdir(parents=True, exist_ok=True)

    # Full lightbox: tight contain, max edge FULL_MAX
    full = im.convert("RGBA")
    fw, fh = full.size
    scale = min(FULL_MAX / fw, FULL_MAX / fh, 1.0) if max(fw, fh) > FULL_MAX else 1.0
    if scale < 1.0:
        full = full.resize(
            (max(1, int(fw * scale)), max(1, int(fh * scale))), Image.Resampling.LANCZOS
        )
    # Pad slight void border for clean lightbox edge
    pad = 24
    full_bg = Image.new(
        "RGB",
        (full.width + 2 * pad, full.height + 2 * pad),
        tuple(int(v) for v in VOID),
    )
    full_rgb = Image.new("RGB", full.size, tuple(int(v) for v in VOID))
    full_rgb.paste(full.convert("RGB"), mask=full.split()[-1] if full.mode == "RGBA" else None)
    full_bg.paste(full_rgb, (pad, pad))
    full_bg.save(WEB / f"full_{stem}.png", "PNG", optimize=True)
    full_bg.save(WEB / f"full_{stem}.webp", "WEBP", quality=90, method=6)

    # Card: cover for landscape-ish, contain for tall plots that need full content
    if mode == "cover":
        card = fit_cover(im, CARD)
    else:
        card = fit_contain_tight(im, CARD, pad_frac=0.03)
    rgb = Image.new("RGB", card.size, tuple(int(v) for v in VOID))
    rgb.paste(card, mask=card.split()[-1])
    rgb.save(WEB / f"{stem}.png", "PNG", optimize=True)
    rgb.save(WEB / f"{stem}.webp", "WEBP", quality=88, method=6)
    print(f"  card {rgb.size}  full {full_bg.size}")


def main() -> None:
    # All three: tight contain so labels/axes never clip; letterbox is pure void
    # (matches site bg — invisible gutters). Cover mode was over-cropping wake.
    jobs = [
        ("itsm_3d_wake_analogy.png", "card_wake", "contain"),
        ("itsm_t3_fundamental_domain.png", "card_t3", "contain"),
        ("itsm_phonon_dispersion.png", "card_phonon", "contain"),
    ]
    for src, stem, mode in jobs:
        process(src, stem, mode=mode)
    print(f"Done -> {WEB}")


if __name__ == "__main__":
    main()
