from pathlib import Path

from PIL import Image

from .blacklist import BlacklistDB, BlacklistReason
from .config import MIN_IMAGE_WIDTH
from .message import message


def purge_small_images(folder, blacklist_db=None):
  """Remove images smaller than the minimum width threshold and blacklist them."""
  if blacklist_db is None:
    blacklist_db = BlacklistDB()
  
  for child in Path(folder).iterdir():
    if not child.is_file():
      continue
    
    try:
      with Image.open(child) as image:
        image.load()
        width, _ = image.size
        if width < MIN_IMAGE_WIDTH:
          image.close()
          # Add to blacklist before removing
          blacklist_db.add(child.name, BlacklistReason.TOO_SMALL)
          child.unlink()
          message(f"Removed {child.name}: Too small ({width}px < {MIN_IMAGE_WIDTH}px)")
    except Exception as e:
      message(f"Error processing {child}: {e}")
