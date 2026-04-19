#!/usr/bin/env python3
"""
This module generates a geometric "gem-like" mesh SVG image based on a text seed.
It uses Delaunay triangulation to create a faceted aesthetic.

The color palette is derived from the horizontal position of the triangles,
creating a gradient effect, while the geometry is pseudo-randomly generated
using the provided text as a seed.

Usage Example:
    $ python generate_gem_mesh_svg.py --text "my-unique-seed" --width 1920 --height 1080 --output header.svg
    $ python generate_gem_mesh_svg.py --file README.md

"""

import argparse
import hashlib
import logging
import math
import random
from pathlib import Path

import numpy as np
from scipy.spatial import Delaunay

DEFAULT_OUTPUT_PATH = Path("header.svg")
DEFAULT_HEIGHT = 400
DEFAULT_WIDTH = 1200

DIRECTION = random.choice(["horizontal", "vertical", "diagonal", "radial"])

COLOR_START = (105, 171, 141)
COLOR_MIDDLE = (245, 240, 235)
COLOR_END = (212, 206, 70)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(Path(__file__).stem)

parser = argparse.ArgumentParser(
    description="Generate a Julia set fractal image based on input text."
)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--text", type=str, help="Raw text to use as the seed.")
group.add_argument("--file", type=Path, help="Path to a text file to use as the seed.")

parser.add_argument(
    "--width",
    type=int,
    default=DEFAULT_WIDTH,
    help="Width of the generated image (default: 1200)",
)
parser.add_argument(
    "--height",
    type=int,
    default=DEFAULT_HEIGHT,
    help="Height of the generated image (default: 400)",
)
parser.add_argument(
    "--output",
    type=Path,
    default=DEFAULT_OUTPUT_PATH,
    help="Output path for the image",
)


def lerp_color(
    c1: tuple[int, int, int], c2: tuple[int, int, int], t: float
) -> tuple[int, int, int]:
    """Blends between c1 and c2 based on parameter t [0.0, 1.0]."""
    # Ensure t is strictly bounded
    t = max(0.0, min(1.0, t))

    r = int(c1[0] + (c2[0] - c1[0]) * t)
    g = int(c1[1] + (c2[1] - c1[1]) * t)
    b = int(c1[2] + (c2[2] - c1[2]) * t)

    return r, g, b


def generate_gem_mesh_svg(
    input_text: str,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    output_path: Path = DEFAULT_OUTPUT_PATH,
):
    """
    Generates a Delaunay triangulation mesh and saves it as an SVG file.

    :param input_text: The seed text used to initialize the random number generator.
    :param width: The width of the SVG canvas.
    :param height: The height of the SVG canvas.
    :param output_path: The file path where the SVG will be saved.
    """
    # Seeding
    digest = hashlib.sha256(input_text.encode("utf-8")).digest()
    random.seed(digest)

    # Vertices creation
    density_factor = 2000
    num_points = (width * height) // density_factor

    points = []
    for _ in range(num_points):
        x_coord = random.uniform(0, width)
        y_coord = random.uniform(0, height)
        points.append([x_coord, y_coord])

    # Inject bounding box corners to ensure full canvas coverage
    bounding_vertices = [[0.0, 0.0], [width, 0.0], [0.0, height], [width, height]]
    points.extend(bounding_vertices)

    # Convert to numpy array for Scipy
    points_array = np.array(points)

    # Compute Delaunay Triangulation
    tri = Delaunay(points_array)
    logger.info(f"Computed Delaunay mesh with {len(tri.simplices)} triangles.")

    # SVG Rendering
    svg_elements = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
    ]

    for i, simplex in enumerate(tri.simplices):
        # simplex contains the indices of the 3 vertices forming the triangle
        v1, v2, v3 = points_array[simplex]

        # Calculate the centroid (x, y) of the triangle to deterministically assign color
        # Centroid calculation
        cx = (v1[0] + v2[0] + v3[0]) / 3.0
        cy = (v1[1] + v2[1] + v3[1]) / 3.0

        # User-defined diagonal gradient mapping
        cx_norm = cx / width
        cy_norm = cy / height

        # Scalar field mapping based on direction
        if DIRECTION == "horizontal":
            t = cx_norm
        elif DIRECTION == "vertical":
            t = cy_norm
        elif DIRECTION == "diagonal":
            t = (cx_norm + cy_norm) / 2.0
        elif DIRECTION == "radial":
            # Euclidean distance from normalized center (0.5, 0.5)
            dist = math.hypot(cx_norm - 0.5, cy_norm - 0.5)
            # Normalize by max possible distance to corner (~0.707)
            t = min(1.0, dist / 0.707)
        else:
            t = 0.0  # Fallback

        # Blend the colors using our helper function
        # r, g, b = lerp_color(COLOR_START, COLOR_END, t)

        # 3-Color Piecewise Interpolation
        if t <= 0.5:
            # Remap global t from [0.0, 0.5] to local t [0.0, 1.0]
            local_t = t * 2.0
            r, g, b = lerp_color(COLOR_START, COLOR_MIDDLE, local_t)
        else:
            # Remap global t from [0.5, 1.0] to local t [0.0, 1.0]
            local_t = (t - 0.5) * 2.0
            r, g, b = lerp_color(COLOR_MIDDLE, COLOR_END, local_t)

        # Format to hex string for the SVG
        hex_color = f"#{r:02x}{g:02x}{b:02x}"

        # hue = (cx_norm + cy_norm) / 2
        # # Jitter applied to saturation/value for faceted gem effect
        # saturation = 0.6 + random.uniform(-0.1, 0.1)
        # value = 0.8 + random.uniform(-0.1, 0.1)
        # r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        # hex_color = f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

        # Format to 1 decimal place to reduce payload size
        points_str = f"{v1[0]},{v1[1]} {v2[0]},{v2[1]} {v3[0]},{v3[1]}"

        # Stroke matches fill for seamless topology
        svg_elements.append(
            f'  <polygon points="{points_str}" fill="{hex_color}" stroke="{hex_color}" stroke-width="0.5"/>'
        )

    svg_elements.append("</svg>\n")

    # Write to disk
    with output_path.open("w", encoding="utf-8") as f:
        f.writelines(svg_elements)

    logger.info(f"Successfully wrote SVG to {output_path}")


def main():
    """
    Parses command line arguments and executes the SVG generation.
    """
    args = parser.parse_args()

    # read args
    output_path = args.output
    width = args.width
    height = args.height

    if args.file:
        if not args.file.exists():
            logger.error(f"File not found: {args.file}")
            exit(1)

        path: Path = args.file
        input_text = path.read_text()

        if output_path == DEFAULT_OUTPUT_PATH:
            output_path = Path(f"{path.stem}.svg")
    else:
        input_text = args.text

    generate_gem_mesh_svg(input_text, width, height, output_path)


if __name__ == "__main__":
    main()
