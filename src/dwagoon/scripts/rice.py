import os
from pathlib import Path
import platform
from subprocess import run
import sys

from ..message import message

WALLPAPER_FOLDER = Path.home() / "Downloads" / "reddit"


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


def main():
  if is_ssh():
    message(f"{sys.argv[0]} will not run in SSH")
    return

  command = ["wal", "-i", WALLPAPER_FOLDER, "--backend", "colorz", "--cols16"] + sys.argv[1:]
  if is_wsl():
    message("Delegating to powershell")
    command = ["powershell.exe"] + command
  run(command)
