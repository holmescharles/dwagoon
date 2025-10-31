from pathlib import Path

from PIL import Image

from .config import MIN_IMAGE_WIDTH
from .message import message


def purge_small_images(folder):
  """Remove images smaller than the minimum width threshold."""
  for child in Path(folder).iterdir():
    if not child.is_file():
      continue
    
    try:
      with Image.open(child) as image:
        image.load()
        width, _ = image.size
        if width < MIN_IMAGE_WIDTH:
          image.close()
          child.unlink()
          message(f"Removed {child}: Too small ({width}px < {MIN_IMAGE_WIDTH}px)")
    except Exception as e:
      message(f"Error processing {child}: {e}")
