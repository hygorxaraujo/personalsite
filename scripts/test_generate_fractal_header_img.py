import subprocess
import sys
from pathlib import Path
from scripts.generate_fractal_header_img import (
    scale_to_range,
    get_complex_seed_from_text,
    get_julia_iteration_count,
    generate_julia_set,
    save_julia_set_as_ppm,
)

def test_scale_to_range():
    # Test midpoint
    assert scale_to_range(50, 100, 10, 0) == 5.0
    # Test min
    assert scale_to_range(0, 100, 10, 0) == 0.0
    # Test max
    assert scale_to_range(100, 100, 10, 0) == 10.0
    # Test negative range
    assert scale_to_range(50, 100, 1, -1) == 0.0
    # Test max_possible_value is 0 (should return rng_min)
    assert scale_to_range(0, 0, 10, 0) == 0.0
    assert scale_to_range(0, 0, 10, 5) == 5.0

def test_get_complex_seed_from_text():
    seed1 = get_complex_seed_from_text("test")
    seed2 = get_complex_seed_from_text("test")
    seed3 = get_complex_seed_from_text("different")
    
    assert isinstance(seed1, complex)
    assert seed1 == seed2
    assert seed1 != seed3

def test_get_julia_iteration_count():
    seed = complex(-0.8, 0.156)
    # Test a point that should escape quickly or stay
    # Just verify it returns an int within expected range
    count = get_julia_iteration_count(0, 0, seed, 100, 100, max_iters=10)
    assert isinstance(count, int)
    assert 1 <= count <= 10

def test_generate_julia_set():
    width, height = 10, 5
    seed = complex(-0.8, 0.156)
    julia_set = generate_julia_set(seed, width, height)
    
    assert len(julia_set) == height
    assert len(julia_set[0]) == width
    assert all(isinstance(val, int) for row in julia_set for val in row)

def test_save_julia_set_as_ppm_body_format(tmp_path):
    # Create a small 2x2 julia set with known values
    # Values: 0 (min) and 10 (max)
    julia_set = [[0, 5], [10, 0]]
    output_path = tmp_path / "format_test.ppm"
    save_julia_set_as_ppm(julia_set, output_path)
    
    content = output_path.read_text()
    lines = content.strip().split("\n")
    
    # Check header
    assert lines[0] == "P3"
    assert lines[1] == "2 2"
    assert lines[2] == "255"
    
    # The body starts from line 3. Our implementation joins with spaces.
    # Let's extract all numbers from the body part
    body_text = " ".join(lines[3:])
    pixel_values = [int(v) for v in body_text.split() if v.isdigit()]
    
    # 2x2 image should have 4 pixels, each with 3 components (R, G, B) = 12 values
    assert len(pixel_values) == 12
    
    # Check scaling:
    # 0 should map to 0
    # 5 should map to 127 (midpoint of 0-255)
    # 10 should map to 255
    # Pixel 1: [0, 0, 0]
    assert pixel_values[0:3] == [0, 0, 0]
    # Pixel 2: [127, 127, 127]
    assert pixel_values[3:6] == [127, 127, 127]
    # Pixel 3: [255, 255, 255]
    assert pixel_values[6:9] == [255, 255, 255]
    # Pixel 4: [0, 0, 0]
    assert pixel_values[9:12] == [0, 0, 0]

def test_cli_text_input(tmp_path):
    output_path = tmp_path / "cli_test.ppm"
    # Use sys.executable to ensure we use the same python environment
    result = subprocess.run(
        [sys.executable, "scripts/generate_fractal_header_img.py", "--text", "hello", "--output", str(output_path), "--width", "10", "--height", "10"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert output_path.exists()
    assert output_path.read_text().startswith("P3")

def test_cli_file_input(tmp_path):
    seed_file = tmp_path / "seed.txt"
    seed_file.write_text("file seed content")
    output_path = tmp_path / "cli_file_test.ppm"
    
    result = subprocess.run(
        [sys.executable, "scripts/generate_fractal_header_img.py", "--file", str(seed_file), "--output", str(output_path), "--width", "10", "--height", "10"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert output_path.exists()
    assert output_path.read_text().startswith("P3")
