#!/usr/bin/env python3
"""Build web-optimized ITSM site images with correct aspect ratios.

Sources: Assets/Figures/ (scientific originals — never overwritten)
Outputs: docs/assets/web/ (hero 16:9, cards 4:3, split ~14:9)

Composes letterbox/pillarbox on void background + soft vignette so geometry
is not brutal-cropped when aspect ratios mismatch.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "Assets" / "Figures"
OUT = REPO / "docs" / "assets" / "web"

VOID = (5, 6, 12, 255)  # matches site --void
GOLD = (212, 176, 106, 180)


def fit_on_canvas(
    im: Image.Image,
    canvas_w: int,
    canvas_h: int,
    *,
    mode: str = "contain",
    pad_color: tuple[int, int, int, int] = VOID,
    scale_boost: float = 0.92,
) -> Image.Image:
    """Place image on canvas. contain=letterbox; cover=fill crop center."""
    im = im.convert("RGBA")
    cw, ch = canvas_w, canvas_h
    canvas = Image.new("RGBA", (cw, ch), pad_color)

    iw, ih = im.size
    if mode == "cover":
        scale = max(cw / iw, ch / ih)
    else:
        scale = min(cw / iw, ch / ih) * scale_boost

    nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
    x = (cw - nw) // 2
    y = (ch - nh) // 2
    canvas.alpha_composite(resized, (x, y))
    return canvas


def vignette(im: Image.Image, strength: float = 0.45) -> Image.Image:
    w, h = im.size
    # radial mask: white center, dark edges
    mask = Image.new("L", (w, h), 0)
    # approximate with resized ellipse gradient
    cx, cy = w // 2, h // 2
    max_r = (cx**2 + cy**2) ** 0.5
    pixels = mask.load()
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / max_r
            v = int(255 * max(0.0, 1.0 - strength * (d**1.6)))
            pixels[x, y] = v
            if x + 1 < w:
                pixels[x + 1, y] = v
            if y + 1 < h:
                pixels[x, y + 1] = v
                if x + 1 < w:
                    pixels[x + 1, y + 1] = v
    mask = mask.filter(ImageFilter.GaussianBlur(radius=max(w, h) // 40))
    dark = Image.new("RGBA", (w, h), VOID)
    return Image.composite(im, dark, mask)


def gold_frame(im: Image.Image, inset: int = 10) -> Image.Image:
    """Very subtle gold hairline inset."""
    out = im.copy()
    w, h = out.size
    # draw via rectangle paste of edges
    line = Image.new("RGBA", (w - 2 * inset, 1), GOLD)
    out.alpha_composite(line, (inset, inset))
    out.alpha_composite(line, (inset, h - inset - 1))
    vline = Image.new("RGBA", (1, h - 2 * inset), GOLD)
    out.alpha_composite(vline, (inset, inset))
    out.alpha_composite(vline, (w - inset - 1, inset))
    return out


def enhance(im: Image.Image) -> Image.Image:
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(1.04)
    im = ImageEnhance.Brightness(im).enhance(0.98)
    return im


def save_pair(im: Image.Image, stem: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rgb = Image.new("RGB", im.size, VOID[:3])
    rgb.paste(im, mask=im.split()[-1] if im.mode == "RGBA" else None)
    png_path = OUT / f"{stem}.png"
    webp_path = OUT / f"{stem}.webp"
    rgb.save(png_path, "PNG", optimize=True)
    rgb.save(webp_path, "WEBP", quality=82, method=6)
    print(f"  wrote {png_path.name} {rgb.size}  webp={webp_path.stat().st_size//1024}KB")


def build() -> None:
    jobs = [
        {
            "src": "itsm_3d_toroidal_manifold.png",
            "stem": "hero_toroidal",
            "size": (1920, 1080),
            "mode": "contain",
            "frame": False,
            "scale_boost": 0.95,
        },
        {
            "src": "itsm_3d_wake_analogy.png",
            "stem": "card_wake",
            "size": (1200, 900),
            "mode": "contain",
            "frame": True,
            "scale_boost": 0.94,
        },
        {
            "src": "itsm_t3_fundamental_domain.png",
            "stem": "card_t3",
            "size": (1000, 750),
            "mode": "contain",
            "frame": True,
            "scale_boost": 0.9,
        },
        {
            "src": "itsm_phonon_dispersion.png",
            "stem": "card_phonon",
            "size": (1000, 750),
            "mode": "contain",
            "frame": True,
            "scale_boost": 0.88,
        },
        {
            "src": "itsm_3d_fluid_dynamics_publication.png",
            "stem": "split_fluid",
            "size": (1400, 900),
            "mode": "cover",  # wide cinematic — cover is OK after 14:9 canvas
            "frame": False,
            "scale_boost": 1.0,
        },
    ]

    print(f"Source: {SRC}")
    print(f"Output: {OUT}")
    for job in jobs:
        path = SRC / job["src"]
        if not path.exists():
            print(f"  SKIP missing {path}")
            continue
        print(f"Building {job['stem']} from {job['src']}...")
        im = Image.open(path)
        composed = fit_on_canvas(
            im,
            job["size"][0],
            job["size"][1],
            mode=job["mode"],
            scale_boost=job.get("scale_boost", 0.92),
        )
        composed = enhance(composed)
        composed = vignette(composed, strength=0.38 if job["stem"] == "hero_toroidal" else 0.28)
        if job.get("frame"):
            composed = gold_frame(composed, inset=12)
        save_pair(composed, job["stem"])
    print("Done.")


if __name__ == "__main__":
    build()
