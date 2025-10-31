"""Image analysis utilities for filtering wallpapers."""
from pathlib import Path
from collections import Counter

from PIL import Image
import numpy as np

from .message import message


def is_boring_background(image_path, threshold=0.7):
    """
    Detect if an image has a boring (mostly white or black) background.
    
    Analyzes the border pixels and checks if they're predominantly one color.
    
    Args:
        image_path: Path to the image file
        threshold: Fraction of border that must be same color (0.0-1.0)
    
    Returns:
        True if the image has a boring background, False otherwise
    """
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Get image dimensions
            width, height = img.size
            
            # Sample border pixels (top, bottom, left, right edges)
            border_width = min(10, width // 20, height // 20)  # 10px or 5% of smallest dimension
            
            border_pixels = []
            
            # Top and bottom borders
            for y in [range(border_width), range(height - border_width, height)]:
                for py in y:
                    for px in range(width):
                        try:
                            border_pixels.append(img.getpixel((px, py)))
                        except:
                            pass
            
            # Left and right borders
            for x in [range(border_width), range(width - border_width, width)]:
                for px in x:
                    for py in range(height):
                        try:
                            border_pixels.append(img.getpixel((px, py)))
                        except:
                            pass
            
            if not border_pixels:
                return False
            
            # Check if pixels are predominantly white or black
            white_count = 0
            black_count = 0
            
            for pixel in border_pixels:
                r, g, b = pixel[:3]  # Handle RGBA
                brightness = (r + g + b) / 3
                
                if brightness > 240:  # Very bright (white-ish)
                    white_count += 1
                elif brightness < 15:  # Very dark (black-ish)
                    black_count += 1
            
            total_border_pixels = len(border_pixels)
            white_ratio = white_count / total_border_pixels
            black_ratio = black_count / total_border_pixels
            
            is_boring = white_ratio > threshold or black_ratio > threshold
            
            if is_boring:
                if white_ratio > black_ratio:
                    message(f"Detected white background ({white_ratio:.1%} white): {image_path.name}")
                else:
                    message(f"Detected black background ({black_ratio:.1%} black): {image_path.name}")
            
            return is_boring
            
    except Exception as e:
        message(f"Error analyzing {image_path}: {e}")
        return False


def get_dominant_color(image_path, num_colors=5):
    """
    Get the dominant color(s) in an image.
    
    Args:
        image_path: Path to the image file
        num_colors: Number of dominant colors to return
    
    Returns:
        List of (color, count) tuples
    """
    try:
        with Image.open(image_path) as img:
            # Resize for faster processing
            img = img.resize((100, 100))
            
            # Convert to RGB
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Get all pixels
            pixels = list(img.getdata())
            
            # Count colors
            color_counts = Counter(pixels)
            
            # Return most common
            return color_counts.most_common(num_colors)
            
    except Exception as e:
        message(f"Error getting dominant color for {image_path}: {e}")
        return []
