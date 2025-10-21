from argparse import ArgumentParser
import os
from pathlib import Path
import platform
from subprocess import run
import sys

from .message import message

WALLPAPER_FOLDER = Path.home() / "Downloads" / "Wallpapers"


PARSER = ArgumentParser()
PARSER.add_argument("--dark", action="store_true", help="dark color scheme?")
PARSER.add_argument(
  "image",
  nargs="?",
  default=WALLPAPER_FOLDER,
  help="path to wallpaper image or folder of images",
)


def is_ssh():
  return bool(os.environ.get("SSH_CONNECTION"))


def is_wsl():
  if platform.system() != "Linux":
    return False
  try:
    with open("/proc/version") as f:
      info = f.read()
    return "Microsoft" in info or "WSL" in info
  except FileNotFoundError:
    return False


def is_windows():
  return platform.system() == "Windows"


def parse_args():
  parser = ArgumentParser(description="Apply a wallpaper and color scheme using pywal.")


def main():
  params = PARSER.parse_args()

  if is_ssh():
    message(f"{sys.argv[0]} will not run in SSH")
    return

  command = ["wal", "-i", params.image, "--cols16"]
  if not params.dark:
    command += ["-l"]

  message(f"Running: {' '.join(map(str, command))}")
  if is_wsl():
    message("Delegating to powershell")
    command = ["powershell.exe"] + command
  run(command)

  if is_windows() and not is_wsl():
    message("Updating terminal")
    run(["powershell.exe", "-File", str(Path(__file__).parent / "UpdateTerminal.ps1")])
