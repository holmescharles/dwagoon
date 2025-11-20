from argparse import ArgumentParser
import os
from pathlib import Path
import platform
from subprocess import run
import sys

from .download import WALLPAPER_FOLDER
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
  return platform.system() == "Windows"


def main(args=None):
  params = PARSER.parse_args() if args is None else args

  image = params.image if params.image else WALLPAPER_FOLDER
  command = ["wal", "-i", image, "--cols16"]
  if params.light:
    command += ["-l"]
  message(f"Running: {' '.join(map(str, command))}")
  result = run(command)

  # FIXME: Temporary workaround for pywal16 --cols16 bug with 8-15 color images
  # Remove this fallback once upstream pywal16 fixes the wal backend validation
  # See: pywal16_bug_report.md for details
  if result.returncode != 0:
    message("--cols16 failed, retrying with 8 colors")
    command = ["wal", "-i", image]
    if params.light:
      command += ["-l"]
    run(command)

  if is_windows():
    message("Updating terminal")
    run(["powershell.exe", "-File", str(Path(__file__).parent / "UpdateTerminal.ps1")])
