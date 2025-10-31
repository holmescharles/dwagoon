from argparse import ArgumentParser
from pathlib import Path
import platform
from subprocess import run

from .config import WALLPAPER_FOLDER
from .message import message

PARSER = ArgumentParser()
PARSER.add_argument("-l", "--light", action="store_true", help="use light color scheme (default is dark)")
PARSER.add_argument(
  "image",
  nargs="?",
  default=WALLPAPER_FOLDER,
  help="path to wallpaper image or folder of images",
)


def is_windows():
  """Check if running on Windows."""
  return platform.system() == "Windows"


def main():
  """Apply wallpaper and generate color scheme using pywal16."""
  params = PARSER.parse_args()

  command = ["wal", "-i", params.image, "--cols16"]
  if params.light:
    command += ["-l"]
  
  message(f"Running: {' '.join(map(str, command))}")
  
  try:
    result = run(command, check=True)
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
