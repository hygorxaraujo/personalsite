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

from typing import Generator

import hashlib
import logging
from pathlib import Path
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(Path(__file__).stem)

NUM_BITS_IN_EACH_BYTE = 8
SELECTED_INT_NUM_BYTES = 8
MAX_INT_SIZE = 2 ** (SELECTED_INT_NUM_BYTES * NUM_BITS_IN_EACH_BYTE) - 1

X_MAX_VAL = 2.0
X_MIN_VAL = -X_MAX_VAL

Y_MAX_VAL = 1.5
Y_MIN_VAL = -Y_MAX_VAL

parser = argparse.ArgumentParser(
    description="Generate a Julia set fractal image based on input text."
)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--text", type=str, help="Raw text to use as the seed.")
group.add_argument("--file", type=Path, help="Path to a text file to use as the seed.")

parser.add_argument(
    "--width",
    type=int,
    default=1200,
    help="Width of the generated image (default: 1200)",
)
parser.add_argument(
    "--height",
    type=int,
    default=400,
    help="Height of the generated image (default: 400)",
)
parser.add_argument(
    "--output",
    type=Path,
    default=Path("julia_set.ppm"),
    help="Output path for the PPM image (default: julia_set.ppm)",
)


def get_complex_seed_from_text(input_text: str) -> complex:
    """Generates a complex number seed based on the SHA256 hash of the input text.

    Args:
        input_text: The string to be hashed to generate the seed.

    Returns:
        A complex number where the real and imaginary parts are derived from
        the hash and normalized within the defined X and Y ranges.
    """
    logger.debug(f"Received text of size: {len(input_text)}")

    sha256_obj = hashlib.sha256(input_text.encode())
    logger.debug("Hashed input text")

    sha256_digest = sha256_obj.digest()
    x_bytes = sha256_digest[:SELECTED_INT_NUM_BYTES]
    y_bytes = sha256_digest[-SELECTED_INT_NUM_BYTES:]

    x = int.from_bytes(x_bytes, byteorder="big", signed=False)
    y = int.from_bytes(y_bytes, byteorder="big", signed=False)
    logger.debug(f"Got {x=} and {y=}")

    x_norm = scale_to_range(x, MAX_INT_SIZE, X_MAX_VAL, X_MIN_VAL)
    y_norm = scale_to_range(y, MAX_INT_SIZE, Y_MAX_VAL, Y_MIN_VAL)
    logger.debug(f"Normalized {x_norm=} {y_norm=}")

    c = complex(x_norm, y_norm)
    logger.debug(f"Got {c=}")

    return c


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


def get_julia_iteration_count(
    coord_x: float,
    coord_y: float,
    complex_seed: complex,
    width: float,
    height: float,
    max_iters: int = 10,
) -> int:
    """Calculates the escape time for a point in a Julia set.

    Args:
        coord_x: The horizontal pixel coordinate.
        coord_y: The vertical pixel coordinate.
        complex_seed: The constant 'c' in the Julia set formula z = z^2 + c.
        width: The total width of the coordinate system.
        height: The total height of the coordinate system.
        max_iters: The maximum number of iterations before stopping.

    Returns:
        The number of iterations performed before the magnitude exceeded 2.0
        or max_iters was reached.
    """
    logger.debug(
        f"Calculating Julia iterations for ({coord_x}, {coord_y}) with seed {complex_seed}"
    )

    x_norm = scale_to_range(coord_x, width, X_MAX_VAL, X_MIN_VAL)
    y_norm = scale_to_range(coord_y, height, Y_MAX_VAL, Y_MIN_VAL)
    z = complex(x_norm, y_norm)

    iter_num = 0
    while True:
        iter_num += 1
        z = z**2 + complex_seed
        if z.real**2 + z.imag**2 >= 4.0 or iter_num >= max_iters:
            break

    logger.debug(f"Finished after {iter_num} iterations")
    return iter_num


def generate_julia_set(
    complex_seed: complex, width: int, height: int
) -> list[list[int]]:
    """Generates a 2D grid representing the Julia set.

    Args:
        complex_seed: The constant 'c' used in the iteration formula.
        width: The width of the output image in pixels.
        height: The height of the output image in pixels.

    Returns:
        A 2D list (list of lists) where each element is the iteration
        count for that specific pixel coordinate.
    """
    julia_set = [
        [
            get_julia_iteration_count(x, y, complex_seed, width, height)
            for x in range(width)
        ]
        for y in range(height)
    ]
    return julia_set


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
                # Simple grayscale mapping: scale iteration count to 0-255
                color = int(scale_to_range(val, max_val, 255, 0))
                yield f"{color} {color} {color}"
            yield "\n"

    with output_path.open("w") as f:
        f.writelines(header)
        for color in get_color(julia_set):
            f.write(color + " ")


if __name__ == "__main__":
    args = parser.parse_args()

    # read args
    if args.file:
        if not args.file.exists():
            logger.error(f"File not found: {args.file}")
            exit(1)
        input_text = args.file.read_text()
    else:
        input_text = args.text

    width = args.width
    height = args.height

    # generate fractal
    complex_seed = get_complex_seed_from_text(input_text)
    julia_set = generate_julia_set(complex_seed, width, height)
    save_julia_set_as_ppm(julia_set, args.output)
