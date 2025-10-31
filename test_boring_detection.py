#!/usr/bin/env python3
"""
Test script for boring image detection.

Since network access to Reddit is blocked in this environment, this creates
synthetic test images to validate the boring background detection algorithm.
Creates images with white, black, and colorful backgrounds to test the detector.
"""
from pathlib import Path
import sys
from PIL import Image, ImageDraw
import random

# Add src to path so we can import yodawg modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from yodawg.imageanalysis import is_boring_background
from yodawg.config import BORING_BACKGROUND_THRESHOLD


def create_test_image(path, background_type):
    """Create a test image with specified background type."""
    img = Image.new('RGB', (1920, 1080))
    draw = ImageDraw.Draw(img)
    
    if background_type == 'white':
        # Solid white background
        draw.rectangle([(0, 0), (1920, 1080)], fill=(255, 255, 255))
    elif background_type == 'black':
        # Solid black background
        draw.rectangle([(0, 0), (1920, 1080)], fill=(0, 0, 0))
    elif background_type == 'white_border':
        # White border with some content in middle
        draw.rectangle([(0, 0), (1920, 1080)], fill=(255, 255, 255))
        draw.rectangle([(400, 300), (1520, 780)], fill=(100, 150, 200))
    elif background_type == 'black_border':
        # Black border with some content in middle
        draw.rectangle([(0, 0), (1920, 1080)], fill=(0, 0, 0))
        draw.rectangle([(400, 300), (1520, 780)], fill=(200, 100, 150))
    elif background_type == 'colorful':
        # Colorful image (no boring background)
        for _ in range(100):
            x1, y1 = random.randint(0, 1820), random.randint(0, 980)
            x2, y2 = x1 + random.randint(50, 300), y1 + random.randint(50, 300)
            color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
            draw.rectangle([(x1, y1), (x2, y2)], fill=color)
    elif background_type == 'gradient':
        # Gradient background (should not be boring)
        for y in range(1080):
            gray = int(255 * y / 1080)
            draw.rectangle([(0, y), (1920, y+1)], fill=(gray, gray, gray))
    elif background_type == 'mostly_white':
        # 80% white border
        draw.rectangle([(0, 0), (1920, 1080)], fill=(255, 255, 255))
        draw.ellipse([(700, 400), (1220, 680)], fill=(100, 150, 200))
    elif background_type == 'mostly_black':
        # 80% black border
        draw.rectangle([(0, 0), (1920, 1080)], fill=(0, 0, 0))
        draw.ellipse([(700, 400), (1220, 680)], fill=(200, 100, 150))
    
    img.save(path)


def main():
    """Create test images and test boring detection."""
    test_dir = Path("test_images")
    test_dir.mkdir(exist_ok=True)
    
    # Define test cases
    test_cases = [
        # (filename, background_type, expected_boring)
        ('white_solid.jpg', 'white', True),
        ('black_solid.jpg', 'black', True),
        ('white_border.jpg', 'white_border', True),
        ('black_border.jpg', 'black_border', True),
        ('colorful.jpg', 'colorful', False),
        ('gradient.jpg', 'gradient', False),
        ('mostly_white.jpg', 'mostly_white', True),
        ('mostly_black.jpg', 'mostly_black', True),
    ]
    
    print(f"Creating {len(test_cases)} test images...")
    print(f"Boring threshold: {BORING_BACKGROUND_THRESHOLD:.1%} of border must be white/black\n")
    
    results = []
    correct = 0
    
    for filename, bg_type, expected_boring in test_cases:
        path = test_dir / filename
        create_test_image(path, bg_type)
        
        # Test detection
        is_boring = is_boring_background(path)
        is_correct = is_boring == expected_boring
        
        if is_correct:
            correct += 1
            status = "✓"
        else:
            status = "✗"
        
        result = f"{status} {filename:20s} -> {'BORING' if is_boring else 'NOT BORING':12s} (expected: {'BORING' if expected_boring else 'NOT BORING'})"
        print(result)
        results.append((filename, is_boring))
    
    print(f"\nAccuracy: {correct}/{len(test_cases)} ({100*correct/len(test_cases):.1f}%)")
    
    # Write output files
    boring_files = [f for f, is_boring in results if is_boring]
    not_boring_files = [f for f, is_boring in results if not is_boring]
    
    with open("BORING.txt", "w") as f:
        f.write("# Test images classified as BORING\n")
        f.write(f"# Total: {len(boring_files)}\n\n")
        for filename in boring_files:
            f.write(f"test_images/{filename}\n")
    
    with open("NOT_BORING.txt", "w") as f:
        f.write("# Test images classified as NOT BORING\n")
        f.write(f"# Total: {len(not_boring_files)}\n\n")
        for filename in not_boring_files:
            f.write(f"test_images/{filename}\n")
    
    print(f"\nResults written to BORING.txt ({len(boring_files)} images) and NOT_BORING.txt ({len(not_boring_files)} images)")
    print(f"Test images saved to test_images/")
    
    # Clean up
    print("\nNote: Due to network restrictions, this test uses synthetic images.")
    print("The boring detection algorithm analyzes image borders for white/black pixels.")
    print("Images with >70% white or black borders are classified as boring.")


if __name__ == "__main__":
    main()

