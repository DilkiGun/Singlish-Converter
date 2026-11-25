"""Generate application icons and Windows installer graphics using Pillow."""

from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"


def _find_sinhala_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path(r"C:\Windows\Fonts\NirmalaB.ttf"),
        Path(r"C:\Windows\Fonts\Nirmala.ttc"),
        Path(r"C:\Windows\Fonts\iskpotab.ttf"),
        Path(r"C:\Windows\Fonts\iskpota.ttf"),
        Path(r"C:\Windows\Fonts\segoeui.ttf"),
    ]
    for path in candidates:
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def _draw_rounded_gradient(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    grad = Image.new("RGBA", (size, size))
    px = grad.load()
    # Smooth diagonal gradient: deep indigo (#1e1b4b) -> vibrant teal (#0d9488)
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * max(size - 1, 1))
            r = int(28 + (13 - 28) * t)
            g = int(37 + (148 - 37) * t)
            b = int(99 + (136 - 99) * t)
            px[x, y] = (r, g, b, 255)

    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    radius = int(size * 0.22)
    mask_draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)

    img.paste(grad, (0, 0), mask)

    draw = ImageDraw.Draw(img)
    # Subtle inner border highlight
    inset = max(1, size // 64)
    draw.rounded_rectangle(
        (inset, inset, size - 1 - inset, size - 1 - inset),
        radius=max(1, radius - inset),
        outline=(255, 255, 255, 55),
        width=max(1, size // 64),
    )

    # Small glowing accent dot in top-right
    dot_r = int(size * 0.065)
    cx = int(size * 0.80)
    cy = int(size * 0.20)
    draw.ellipse(
        (cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r),
        fill=(45, 212, 191, 230),
    )

    # Center Sinhala glyph "සි" (fallback to "Si" if font lacks Sinhala)
    font = _find_sinhala_font(int(size * 0.48))
    glyph = "සි"
    try:
        bbox = draw.textbbox((0, 0), glyph, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        if tw <= 0:
            glyph = "Si"
            bbox = draw.textbbox((0, 0), glyph, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
    except Exception:
        glyph = "Si"
        bbox = draw.textbbox((0, 0), glyph, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

    tx = (size - tw) / 2 - bbox[0]
    ty = (size - th) / 2 - bbox[1] - size * 0.02
    draw.text((tx, ty + max(1, size // 48)), glyph, font=font, fill=(0, 0, 0, 80))
    draw.text((tx, ty), glyph, font=font, fill=(248, 250, 252, 255))
    return img


def _make_installer_bmp(width: int, height: int, with_icon: Image.Image) -> Image.Image:
    img = Image.new("RGB", (width, height), (15, 23, 42))
    px = img.load()
    for y in range(height):
        for x in range(width):
            t = (x * 0.4 + y * 0.6) / max(width * 0.4 + height * 0.6, 1)
            r = int(15 + (13 - 15) * t)
            g = int(23 + (78 - 23) * t)
            b = int(42 + (88 - 42) * t)
            px[x, y] = (r, g, b)

    icon_size = min(width, height) - 24 if width < 100 else 88
    resized = with_icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    ix = (width - icon_size) // 2
    iy = (height - icon_size) // 2 if width < 100 else 48
    img.paste(resized, (ix, iy), resized)
    return img


def generate_all() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    master = _draw_rounded_gradient(512)
    master.save(ASSETS_DIR / "app_icon.png")

    # Multi-size Windows ICO
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    master.save(ASSETS_DIR / "app_icon.ico", format="ICO", sizes=sizes)

    # Inno Setup wizard images (standard Inno dimensions: 164x314 and 55x58)
    _make_installer_bmp(164, 314, master).save(ASSETS_DIR / "wizard_large.bmp", format="BMP")
    _make_installer_bmp(55, 58, master).save(ASSETS_DIR / "wizard_small.bmp", format="BMP")
    print(f"Generated assets in {ASSETS_DIR}")


if __name__ == "__main__":
    generate_all()
