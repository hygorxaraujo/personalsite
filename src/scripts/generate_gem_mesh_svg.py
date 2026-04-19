#!/usr/bin/env python3
"""
Julia Set Fractal Generator

This script generates a Julia set fractal image in PPM format. The specific
shape of the fractal is determined by a complex seed derived from the
SHA256 hash of an input string or file content. This ensures that the
same input text always produces the same unique fractal pattern.

Usage:
    python generate_fractal_header_img.py --text "my seed" --width 800 --height 600
"""

import argparse
import colorsys
import hashlib
import logging
import random
from pathlib import Path

DEFAULT_OUTPUT_PATH = Path("header.svg")
from typing import Generator

import numpy as np
from scipy.spatial import Delaunay

DEFAULT_HEIGHT = 400
DEFAULT_WIDTH = 1200

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


def scale_to_range(
        value: float, max_possible_value: float, rng_max: float, rng_min: float
) -> float:
    """Scales a value from its original range to a new target range.

    Args:
        value: The value to be scaled.
        max_possible_value: The upper bound of the original value's range.
        rng_max: The upper bound of the target range.
        rng_min: The lower bound of the target range.

    Returns:
        The value scaled linearly to the range [rng_min, rng_max].
    """
    logger.debug(
        f"Scaling {value} (max {max_possible_value}) to range [{rng_min}, {rng_max}]"
    )
    if max_possible_value == 0:
        return rng_min
    ratio = value / max_possible_value
    rang_size = rng_max - rng_min
    value_norm = ratio * (rang_size) + rng_min
    return value_norm


def save_julia_set_as_ppm(julia_set: list[list[int]], output_path: Path):
    """Writes the Julia set iteration data to a Portable Pixmap (P3) file.

    Args:
        julia_set: A 2D list of iteration counts.
        output_path: The Path object where the .ppm file will be saved.
    """
    height = len(julia_set)
    width = len(julia_set[0])
    max_val = max(max(row) for row in julia_set)

    logger.info(f"Saving Julia set to {output_path} ({width}x{height})")

    header = f"P3\n{width} {height}\n255\n"

    def get_color(julia_set: list[list[int]]) -> Generator[str, None, None]:
        for row in julia_set:
            for val in row:
                hue = min(1.0, val / max_val)
                saturation = 1.0
                value = 0.0 if val == max_val else 1.0
                red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
                red = int(scale_to_range(red, 1.0, 255, 0))
                green = int(scale_to_range(green, 1.0, 255, 0))
                blue = int(scale_to_range(blue, 1.0, 255, 0))

                yield f"{red} {green} {blue}"
            yield "\n"

    with output_path.open("w") as f:
        f.writelines(header)
        for color in get_color(julia_set):
            f.write(color + " ")


def generate_header(input_text: str, width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT,
                    output_path: Path = DEFAULT_OUTPUT_PATH):
    digest = hashlib.sha256(input_text.encode('utf-8')).digest()
    random.seed(digest)

    density_factor = 2000
    num_points = (width * height) // density_factor

    points = []
    for _ in range(num_points):
        x_coord = random.uniform(0, width)
        y_coord = random.uniform(0, height)
        points.append([x_coord, y_coord])

    # Inject bounding box corners to ensure full canvas coverage
    bounding_vertices = [
        [0.0, 0.0], [width, 0.0],
        [0.0, height], [width, height]
    ]
    points.extend(bounding_vertices)

    # Convert to numpy array for Scipy
    points_array = np.array(points)

    # 3. Compute Delaunay Triangulation
    tri = Delaunay(points_array)
    logger.info(f"Computed Delaunay mesh with {len(tri.simplices)} triangles.")

    # 4. SVG Rendering
    svg_elements = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
    ]

    for i, simplex in enumerate(tri.simplices):
        # simplex contains the indices of the 3 vertices forming the triangle
        v1, v2, v3 = points_array[simplex]

        # Calculate the centroid (x, y) of the triangle to deterministically assign color
        cx = (v1[0] + v2[0] + v3[0]) / 3.0

        # Map the X centroid coordinate to a continuous Hue [0.0, 1.0]
        hue = cx / width
        # Keep saturation high and vary value slightly based on the index for a faceted look
        saturation = 0.8
        value = 0.7 + (i % 3) * 0.1

        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        hex_color = f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

        points_str = f"{v1[0]},{v1[1]} {v2[0]},{v2[1]} {v3[0]},{v3[1]}"
        svg_elements.append(
            f'  <polygon points="{points_str}" fill="{hex_color}" stroke="#ffffff" stroke-width="0.5"/>'
        )

    svg_elements.append("</svg>\n")

    # Write to disk
    with output_path.open("w", encoding="utf-8") as f:
        f.writelines(svg_elements)

    logger.info(f"Successfully wrote SVG to {output_path}")


def main():
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
            output_path = Path(f'{path.stem}.svg')
    else:
        input_text = args.text

    generate_header(input_text, width, height, output_path)


if __name__ == "__main__":
    main()
