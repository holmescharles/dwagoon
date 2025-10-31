from argparse import ArgumentParser
from pathlib import Path
import platform
from subprocess import run

from .blacklist import BlacklistDB, BlacklistReason
from .config import WALLPAPER_FOLDER_SFW, WALLPAPER_FOLDER_NSFW
from .message import message

PARSER = ArgumentParser()
PARSER.add_argument("-l", "--light", action="store_true", 
                    help="use light color scheme (default is dark)")
PARSER.add_argument("-x", "--nsfw", action="store_true",
                    help="use NSFW wallpaper channel")
PARSER.add_argument("-d", "--delete", action="store_true",
                    help="blacklist current wallpaper and remove it")
PARSER.add_argument(
  "image",
  nargs="?",
  default=None,
  help="path to wallpaper image or folder of images",
)


def is_windows():
  """Check if running on Windows."""
  return platform.system() == "Windows"


def get_current_wallpaper():
  """Get the path to the currently set wallpaper from wal cache."""
  try:
    wal_file = Path.home() / ".cache" / "wal" / "wal"
    if wal_file.exists():
      with wal_file.open() as f:
        return Path(f.readline().strip())
  except Exception as e:
    message(f"Error reading current wallpaper: {e}")
  return None


def main():
  """Apply wallpaper and generate color scheme using pywal16."""
  params = PARSER.parse_args()

  # Handle --delete flag
  if params.delete:
    current_wallpaper = get_current_wallpaper()
    if current_wallpaper is None or not current_wallpaper.exists():
      message("Error: No current wallpaper found to delete")
      return 1
    
    # Use default blacklist (shared across all channels)
    blacklist_db = BlacklistDB()
    
    # Add to blacklist and delete
    blacklist_db.add(current_wallpaper.name, BlacklistReason.DELETED)
    current_wallpaper.unlink()
    message(f"Deleted and blacklisted: {current_wallpaper.name}")
    return 0

  # Determine image source
  if params.image is None:
    # Use NSFW or SFW folder based on flag
    image_source = WALLPAPER_FOLDER_NSFW if params.nsfw else WALLPAPER_FOLDER_SFW
    channel_name = "NSFW" if params.nsfw else "SFW"
    message(f"Using {channel_name} channel: {image_source}")
  else:
    image_source = params.image

  command = ["wal", "-i", str(image_source), "--cols16"]
  if params.light:
    command += ["-l"]
  
  message(f"Running: {' '.join(map(str, command))}")
  
  try:
    run(command, check=True)
  except FileNotFoundError:
    message("Error: 'wal' command not found. Is pywal16 installed?")
    return 1
  except Exception as e:
    message(f"Error running wal: {e}")
    return 1

  if is_windows():
    message("Updating terminal")
    try:
      ps_script = Path(__file__).parent / "UpdateTerminal.ps1"
      run(["powershell.exe", "-File", str(ps_script)], check=True)
    except Exception as e:
      message(f"Warning: Failed to update Windows Terminal: {e}")
  
  return 0
