from pathlib import Path

from .config import SAVED_WALLPAPER_FOLDER
from .message import message


def main():
  """Save the currently active wallpaper to the saved wallpapers folder."""
  try:
    wal_file = Path.home() / ".cache" / "wal" / "wal"
    
    if not wal_file.exists():
      message("Error: No wallpaper set. Run 'rice' first to set a wallpaper.")
      return 1
    
    with wal_file.open() as f:
      image_path = Path(f.readline().strip())
    
    if not image_path.exists():
      message(f"Error: Wallpaper file not found: {image_path}")
      return 1

    saved_file = SAVED_WALLPAPER_FOLDER / image_path.name
    saved_file.parent.mkdir(parents=True, exist_ok=True)

    with image_path.open("rb") as fin, saved_file.open("wb") as fout:
      fout.write(fin.read())

    message(f"Saved: {saved_file}")
    return 0
  except Exception as e:
    message(f"Error saving wallpaper: {e}")
    return 1
