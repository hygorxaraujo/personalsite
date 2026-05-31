#!/usr/bin/env python3
"""
Generate a deterministic "knowledge graph" banner SVG from a text seed.

A field of pseudo-random nodes is connected via Delaunay triangulation and
rendered as a node-link diagram (thin edges + circular nodes) drawn in light
mint over a deep-emerald gradient. This mirrors the site's homepage hero
(a light graph on paper) as its inverse, so post banners stay on-brand and
keep light title text legible in both light and dark mode.

Usage Example:
    $ python generate_gem_mesh_svg.py --text "my-unique-seed" --width 1200 --height 400 --output header.svg
    $ python generate_gem_mesh_svg.py --file README.md
"""

import argparse
import hashlib
import logging
import math
import random
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.spatial import Delaunay

DEFAULT_OUTPUT_PATH = Path("header.svg")
DEFAULT_HEIGHT = 400
DEFAULT_WIDTH = 1200

# Monograph brand palette (matches custom.scss tokens)
BG_TOP = "#0B7A52"      # $emerald
BG_BOTTOM = "#064027"   # deeper than $emerald-deep, for gradient depth
EDGE_COLOR = "233, 243, 238"   # $emerald-tint as rgb (drawn with per-edge alpha)
NODE_COLOR = "#EAF4EE"          # light mint nodes
NODE_HOT = "#FFFFFF"            # brightest hub nodes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(Path(__file__).stem)

parser = argparse.ArgumentParser(
    description="Generate a knowledge-graph banner SVG based on input text."
)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--text", type=str, help="Raw text to use as the seed.")
group.add_argument("--file", type=Path, help="Path to a text file to use as the seed.")
parser.add_argument(
    "--width", type=int, default=DEFAULT_WIDTH, help="Width of the image (default: 1200)"
)
parser.add_argument(
    "--height", type=int, default=DEFAULT_HEIGHT, help="Height of the image (default: 400)"
)
parser.add_argument(
    "--output", type=Path, default=DEFAULT_OUTPUT_PATH, help="Output path for the image"
)


def generate_graph_header(
    input_text: str,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> None:
    """
    Generate a knowledge-graph banner and save it as an SVG file.

    :param input_text: Seed text used to initialise the random number generator.
    :param width: Width of the SVG canvas.
    :param height: Height of the SVG canvas.
    :param output_path: Destination path for the SVG.
    """
    # Deterministic seeding from the text
    digest = hashlib.sha256(input_text.encode("utf-8")).digest()
    random.seed(digest)

    # Scatter nodes; keep a margin so circles are not clipped at the edges
    margin = 40
    density_factor = 14000  # larger => fewer nodes (a graph reads best when sparse)
    num_points = max(18, (width * height) // density_factor)

    points = [
        [random.uniform(margin, width - margin), random.uniform(margin, height - margin)]
        for _ in range(num_points)
    ]
    points_array = np.array(points)

    # Delaunay triangulation gives a planar, well-distributed edge set
    tri = Delaunay(points_array)

    edges: set[tuple[int, int]] = set()
    for simplex in tri.simplices:
        for a, b in ((simplex[0], simplex[1]), (simplex[1], simplex[2]), (simplex[2], simplex[0])):
            edges.add((min(a, b), max(a, b)))

    # Node degree drives radius/brightness so hubs stand out
    degree: dict[int, int] = defaultdict(int)
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    max_degree = max(degree.values()) if degree else 1

    diag = math.hypot(width, height)

    svg = [
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'xmlns="http://www.w3.org/2000/svg">',
        "  <defs>",
        f'    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{BG_TOP}"/>'
        f'<stop offset="1" stop-color="{BG_BOTTOM}"/></linearGradient>',
        '    <radialGradient id="vignette" cx="0.5" cy="0.35" r="0.9">'
        '<stop offset="0.55" stop-color="#000000" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#000000" stop-opacity="0.28"/></radialGradient>',
        "  </defs>",
        f'  <rect width="{width}" height="{height}" fill="url(#bg)"/>',
        '  <g stroke-linecap="round">',
    ]

    # Edges: shorter links are brighter, giving a sense of local clustering
    for a, b in edges:
        x1, y1 = points_array[a]
        x2, y2 = points_array[b]
        length = math.hypot(x2 - x1, y2 - y1)
        alpha = round(max(0.06, 0.40 * (1.0 - length / (diag * 0.55))), 3)
        svg.append(
            f'    <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="rgba({EDGE_COLOR}, {alpha})" stroke-width="1"/>'
        )
    svg.append("  </g>")

    # Nodes: radius and colour scale with degree; top hubs get a soft halo
    svg.append("  <g>")
    for i, (x, y) in enumerate(points_array):
        d = degree.get(i, 1)
        t = d / max_degree
        radius = 2.2 + t * 5.0
        if t > 0.7:
            svg.append(
                f'    <circle cx="{x:.1f}" cy="{y:.1f}" r="{radius + 6:.1f}" '
                f'fill="rgba({EDGE_COLOR}, 0.12)"/>'
            )
        color = NODE_HOT if t > 0.7 else NODE_COLOR
        opacity = round(0.55 + 0.45 * t, 2)
        svg.append(
            f'    <circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" '
            f'fill="{color}" fill-opacity="{opacity}"/>'
        )
    svg.append("  </g>")

    # Subtle vignette to anchor overlaid title text
    svg.append(f'  <rect width="{width}" height="{height}" fill="url(#vignette)"/>')
    svg.append("</svg>\n")

    output_path.write_text("\n".join(svg), encoding="utf-8")
    logger.info(
        f"Wrote knowledge-graph banner ({num_points} nodes, {len(edges)} edges) to {output_path}"
    )


def main() -> None:
    """Parse command line arguments and run the SVG generation."""
    args = parser.parse_args()
    output_path = args.output

    if args.file:
        if not args.file.exists():
            logger.error(f"File not found: {args.file}")
            raise SystemExit(1)
        input_text = args.file.read_text()
        if output_path == DEFAULT_OUTPUT_PATH:
            output_path = Path(f"{args.file.stem}.svg")
    else:
        input_text = args.text

    generate_graph_header(input_text, args.width, args.height, output_path)


if __name__ == "__main__":
    main()
