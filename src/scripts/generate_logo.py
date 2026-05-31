#!/usr/bin/env python3
"""
Generate the "Node-H" personal-brand logo for the Monograph site.

The mark casts the serif letter **H** as the emphasized "hot center node" of a
small knowledge graph: an emerald node-chip carrying the H, surrounded by an
asymmetric constellation of satellite nodes and edges. This echoes the homepage
hero SVG and the post-header banners, keeping the personal mark on-brand.

A single geometry definition drives two emitters so the vector and raster
assets cannot drift apart:
  * SVG  -- hand-shaped vector source for the web (uses the Newsreader webfont).
  * PNG / ICO -- rendered with Pillow (shapes + a real serif H), because this
    host has no SVG rasterizer (no librsvg / inkscape). Rendering rasters
    directly avoids that gap and gives pixel-perfect control of the favicon.

Usage:
    $ python generate_logo.py                 # write the full asset set
    $ python generate_logo.py --outdir assets # explicit output directory
"""

from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass, field
from pathlib import Path
from urllib.request import urlretrieve

from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(Path(__file__).stem)

# ---------------------------------------------------------------------------
# Monograph brand palette (matches custom.scss / custom-dark.scss tokens)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Palette:
    """Colours for one logo variant. RGB hex; ``edge_alpha`` in [0, 1]."""

    chip: str
    letter: str
    node: str
    edge: str
    edge_alpha: float
    paper: str  # solid background used only by the apple-touch icon


LIGHT = Palette(
    chip="#0B7A52",     # $emerald
    letter="#FAFAF7",   # $paper
    node="#0B7A52",     # $emerald
    edge="#0B7A52",
    edge_alpha=0.42,
    paper="#FAFAF7",
)
DARK = Palette(
    chip="#2BA572",     # brighter emerald to stand off charcoal
    letter="#FAFAF7",   # $paper letter stays consistent across variants
    node="#34C088",     # dark-mode $emerald
    edge="#6FE0AD",     # dark-mode highlight
    edge_alpha=0.45,
    paper="#14161A",    # dark $paper
)

# ---------------------------------------------------------------------------
# Geometry -- authored in a 0..100 square coordinate space
# ---------------------------------------------------------------------------

CENTER = (50.0, 50.0)
CHIP = (27.0, 27.0, 73.0, 73.0)  # x0, y0, x1, y1
CHIP_RADIUS = 11.0
LETTER = "H"

# Satellite nodes: (x, y, radius). Asymmetric placement -- a scattered graph,
# not a symmetric ring.
SATELLITES: list[tuple[float, float, float]] = [
    (15.0, 21.0, 5.0),   # top-left
    (85.0, 27.0, 6.0),   # top-right (largest hub)
    (90.0, 59.0, 3.5),   # right
    (75.0, 86.0, 5.0),   # bottom-right
    (16.0, 80.0, 4.0),   # bottom-left
]
# Edges as index pairs into a node list where -1 denotes the centre chip.
EDGES: list[tuple[int, int]] = [
    (-1, 0), (-1, 1), (-1, 2), (-1, 3), (-1, 4),  # hub spokes
    (0, 1), (3, 4), (1, 2),                        # rim links
]
# Reduced mark for the favicon: chip + three dots, minimal spokes.
SIMPLE_SATELLITES = [SATELLITES[0], SATELLITES[1], SATELLITES[3]]
SIMPLE_EDGES = [(-1, 0), (-1, 1), (-1, 2)]

EDGE_WIDTH = 1.7  # in 100-space units

# ---------------------------------------------------------------------------
# Font resolution -- prefer the real brand serif, fall back to a system serif
# ---------------------------------------------------------------------------

FONT_DIR = Path(".cache/fonts")
SERIF_CACHE = FONT_DIR / "Newsreader.ttf"
MONO_CACHE = FONT_DIR / "SpaceMono.ttf"
NEWSREADER_URL = (
    "https://raw.githubusercontent.com/google/fonts/main/ofl/newsreader/"
    "Newsreader%5Bopsz%2Cwght%5D.ttf"
)
SPACEMONO_URL = (
    "https://raw.githubusercontent.com/google/fonts/main/ofl/spacemono/"
    "SpaceMono-Regular.ttf"
)
SERIF_FALLBACKS = [
    "/usr/share/fonts/google-noto-vf/NotoSerif[wght].ttf",
    "/usr/share/fonts/liberation-serif-fonts/LiberationSerif-Regular.ttf",
]
MONO_FALLBACKS = [
    "/usr/share/fonts/google-noto-vf/NotoSansMono[wght].ttf",
]


def _resolve(cache: Path, url: str, fallbacks: list[str], label: str) -> Path:
    """Return a usable TTF: cached, else downloaded (OFL), else a system font."""
    if cache.exists() and cache.stat().st_size > 5000:
        return cache
    cache.parent.mkdir(parents=True, exist_ok=True)
    try:
        logger.info("Fetching %s font -> %s", label, cache)
        urlretrieve(url, cache)  # noqa: S310 (trusted OFL source)
        if cache.stat().st_size > 5000:
            return cache
    except Exception as exc:  # pragma: no cover - network optional
        logger.warning("%s download failed (%s); using system font", label, exc)
    for candidate in fallbacks:
        if Path(candidate).exists():
            logger.info("Falling back to %s", candidate)
            return Path(candidate)
    raise RuntimeError(f"No {label} font available.")


def resolve_font_path() -> Path:
    """Return the brand serif (Newsreader), downloading it if absent."""
    return _resolve(SERIF_CACHE, NEWSREADER_URL, SERIF_FALLBACKS, "Newsreader")


def resolve_mono_path() -> Path:
    """Return the brand mono (Space Mono), downloading it if absent."""
    return _resolve(MONO_CACHE, SPACEMONO_URL, MONO_FALLBACKS, "Space Mono")


def load_letter_font(path: Path, px: int, weight: int = 600) -> ImageFont.FreeTypeFont:
    """Load the serif font at ``px`` and bias the variable axes for display."""
    font = ImageFont.truetype(str(path), px)
    try:
        axes = [a.decode() if isinstance(a, bytes) else a
                for a in font.get_variation_axis_names() or []]
        if axes:  # Newsreader exposes opsz + wght; set a display-weight cut
            values = []
            for name in axes:
                lname = name.lower()
                if "opsz" in lname or "optical" in lname:
                    values.append(72)
                elif "wght" in lname or "weight" in lname:
                    values.append(weight)
                else:
                    values.append(0)
            font.set_variation_by_axes(values)
    except (OSError, AttributeError):
        pass  # static font -- nothing to tune
    return font


# ---------------------------------------------------------------------------
# Raster rendering (Pillow)
# ---------------------------------------------------------------------------

SS = 8  # supersampling factor for anti-aliasing


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _map(coord: float, size: int, pad: float) -> float:
    inner = size * (1.0 - 2.0 * pad)
    return size * pad + coord / 100.0 * inner


def render_mark(
    size: int,
    pal: Palette,
    *,
    simplified: bool = False,
    background: str | None = None,
    pad: float = 0.05,
    font_path: Path | None = None,
    letter_scale: float = 0.72,
    letter_weight: int = 600,
) -> Image.Image:
    """Render the mark to an RGBA image of ``size`` x ``size`` pixels."""
    font_path = font_path or resolve_font_path()
    s = size * SS
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if background is not None:
        draw.rectangle([0, 0, s, s], fill=(*_hex_to_rgb(background), 255))

    sats = SIMPLE_SATELLITES if simplified else SATELLITES
    edges = SIMPLE_EDGES if simplified else EDGES

    def px(coord: float) -> float:
        return _map(coord, s, pad)

    def node_xy(idx: int) -> tuple[float, float]:
        if idx == -1:
            return CENTER
        return sats[idx][0], sats[idx][1]

    # 1) Edges first (the chip is drawn over the hub ends so spokes appear to
    #    emanate from the chip border).
    edge_rgba = (*_hex_to_rgb(pal.edge), int(round(pal.edge_alpha * 255)))
    for a, b in edges:
        ax, ay = node_xy(a)
        bx, by = node_xy(b)
        draw.line([px(ax), px(ay), px(bx), px(by)],
                  fill=edge_rgba, width=max(1, int(round(EDGE_WIDTH / 100.0 * s))))

    # 2) Central chip.
    x0, y0, x1, y1 = (px(CHIP[0]), px(CHIP[1]), px(CHIP[2]), px(CHIP[3]))
    draw.rounded_rectangle(
        [x0, y0, x1, y1],
        radius=CHIP_RADIUS / 100.0 * s,
        fill=(*_hex_to_rgb(pal.chip), 255),
    )

    # 3) Satellite nodes on top.
    node_rgb = (*_hex_to_rgb(pal.node), 255)
    for sx, sy, sr in sats:
        r = sr / 100.0 * s
        draw.ellipse([px(sx) - r, px(sy) - r, px(sx) + r, px(sy) + r], fill=node_rgb)

    # 4) The serif H, optically centred in the chip.
    chip_inner = (CHIP[3] - CHIP[1]) / 100.0 * s
    font = load_letter_font(font_path, int(chip_inner * letter_scale), letter_weight)
    cx, cy = px(CENTER[0]), px(CENTER[1])
    bbox = draw.textbbox((0, 0), LETTER, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = cx - tw / 2 - bbox[0]
    ty = cy - th / 2 - bbox[1]
    draw.text((tx, ty), LETTER, font=font, fill=(*_hex_to_rgb(pal.letter), 255))

    return img.resize((size, size), Image.LANCZOS)


def render_wordmark(pal: Palette, font_path: Path) -> Image.Image:
    """Mark + 'Hygor X. Araújo' lockup, plus a mono role line."""
    h = 160
    mark_box = h
    width = 760
    s = SS
    img = Image.new("RGBA", (width * s, h * s), (0, 0, 0, 0))

    mark = render_mark(mark_box, pal, pad=0.10, font_path=font_path)
    mark = mark.resize((mark_box * s, mark_box * s), Image.LANCZOS)
    img.alpha_composite(mark, (0, 0))

    draw = ImageDraw.Draw(img)
    name_font = load_letter_font(font_path, int(46 * s))
    name = "Hygor X. Araújo"
    nx = int((mark_box + 18) * s)
    bbox = draw.textbbox((0, 0), name, font=name_font)
    nh = bbox[3] - bbox[1]
    ny = int(h * s * 0.40) - nh // 2 - bbox[1]
    draw.text((nx, ny), name, font=name_font, fill=(*_hex_to_rgb("#13171A"
              if pal is LIGHT else "#FAFAF7"), 255))

    # Role line in the brand mono (Space Mono), letter-spaced for an editorial label.
    role_font = ImageFont.truetype(str(resolve_mono_path()), int(18 * s))
    role = "INTELLIGENT SYSTEMS ENGINEER · RESEARCHER"
    rx = nx + 3
    ry = int(h * s * 0.60)
    for ch in role:  # manual tracking -- Pillow has no letter-spacing argument
        draw.text((rx, ry), ch, font=role_font, fill=(*_hex_to_rgb(pal.node), 255))
        rx += draw.textlength(ch, font=role_font) + 1.5 * s

    return img.resize((width, h), Image.LANCZOS)


# ---------------------------------------------------------------------------
# SVG emission (shares the geometry above)
# ---------------------------------------------------------------------------


def emit_svg(pal: Palette, *, simplified: bool = False) -> str:
    sats = SIMPLE_SATELLITES if simplified else SATELLITES
    edges = SIMPLE_EDGES if simplified else EDGES

    def node_xy(idx: int) -> tuple[float, float]:
        return CENTER if idx == -1 else (sats[idx][0], sats[idx][1])

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
        'width="100" height="100" role="img" aria-label="Hygor X. Araújo logo">'
    ]
    # Edges
    for a, b in edges:
        ax, ay = node_xy(a)
        bx, by = node_xy(b)
        parts.append(
            f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{pal.edge}" '
            f'stroke-opacity="{pal.edge_alpha}" stroke-width="{EDGE_WIDTH}" '
            'stroke-linecap="round"/>'
        )
    # Chip
    parts.append(
        f'<rect x="{CHIP[0]}" y="{CHIP[1]}" width="{CHIP[2] - CHIP[0]}" '
        f'height="{CHIP[3] - CHIP[1]}" rx="{CHIP_RADIUS}" fill="{pal.chip}"/>'
    )
    # Satellites
    for sx, sy, sr in sats:
        parts.append(f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="{pal.node}"/>')
    # Letter
    parts.append(
        f'<text x="50" y="50.5" text-anchor="middle" dominant-baseline="central" '
        f'font-family="Newsreader, Georgia, serif" font-weight="600" '
        f'font-size="33" fill="{pal.letter}">{LETTER}</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


def emit_wordmark_svg(pal: Palette) -> str:
    ink = "#13171A" if pal is LIGHT else "#FAFAF7"
    mark = emit_svg(pal)
    # Inline the 100x100 mark into a wider canvas via <svg> nesting.
    inner = mark.replace(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
        'width="100" height="100" role="img" '
        'aria-label="Hygor X. Araújo logo">',
        '<svg x="6" y="14" width="132" height="132" viewBox="0 0 100 100">',
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 160" '
        'width="760" height="160" role="img" '
        'aria-label="Hygor X. Araújo">'
        f'{inner}'
        f'<text x="160" y="70" font-family="Newsreader, Georgia, serif" '
        f'font-weight="600" font-size="46" fill="{ink}">Hygor X. Araújo</text>'
        f'<text x="162" y="104" font-family="\'Space Mono\', monospace" '
        f'font-size="18" letter-spacing="1.5" fill="{pal.node}">'
        'INTELLIGENT SYSTEMS ENGINEER · RESEARCHER</text>'
        '</svg>'
    )


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


@dataclass
class Outputs:
    outdir: Path
    font_path: Path = field(default_factory=resolve_font_path)

    def write(self) -> None:
        self.outdir.mkdir(parents=True, exist_ok=True)
        fp = self.font_path

        # SVG vector sources
        (self.outdir / "logo.svg").write_text(emit_svg(LIGHT), encoding="utf-8")
        (self.outdir / "logo-dark.svg").write_text(emit_svg(DARK), encoding="utf-8")
        (self.outdir / "logo-wordmark.svg").write_text(
            emit_wordmark_svg(LIGHT), encoding="utf-8"
        )
        logger.info("Wrote SVG sources (logo, logo-dark, logo-wordmark)")

        # Raster marks
        render_mark(512, LIGHT, font_path=fp).save(self.outdir / "logo-512.png")
        render_mark(256, LIGHT, font_path=fp).save(self.outdir / "logo-256.png")
        render_mark(512, DARK, font_path=fp).save(self.outdir / "logo-512-dark.png")
        render_mark(180, LIGHT, background=LIGHT.paper, pad=0.12,
                    font_path=fp).save(self.outdir / "apple-touch-icon-180.png")
        render_wordmark(LIGHT, fp).save(self.outdir / "logo-wordmark.png")
        logger.info("Wrote PNG set (512/256/dark/apple-touch/wordmark)")

        # Favicon: simplified mark at three sizes packed into one .ico
        # Heavier, larger H so the serif survives at 16 px.
        ico_sizes = [48, 32, 16]
        base = render_mark(256, LIGHT, simplified=True, pad=0.06, font_path=fp,
                           letter_scale=0.82, letter_weight=700)
        base.save(
            self.outdir / "favicon.ico",
            format="ICO",
            sizes=[(n, n) for n in ico_sizes],
        )
        logger.info("Wrote favicon.ico (%s)", ico_sizes)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the Node-H brand logo set.")
    parser.add_argument(
        "--outdir", type=Path, default=Path("assets"),
        help="Output directory for the logo assets (default: assets).",
    )
    args = parser.parse_args()
    Outputs(outdir=args.outdir).write()
    logger.info("Logo assets generated in %s", args.outdir.resolve())


if __name__ == "__main__":
    main()
