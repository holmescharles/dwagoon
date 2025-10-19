from pathlib import Path

from PIL import Image

from .message import message


def purge_small_images(folder):
  for child in Path(folder).iterdir():
    with Image.open(child) as image:
      image.load()
      width, _ = image.size
      if width < 1920:
        image.close()
        child.unlink()
        message(f"Removed {child}: Too small")
