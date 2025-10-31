"""Download wallpapers from Reddit."""
from argparse import ArgumentParser
import asyncio
from itertools import islice
from pathlib import Path
import shutil

from .config import WALLPAPER_FOLDER
from .message import message
from .urls import fetch_urls
from .download import download_images
from .toosmall import purge_small_images


PARSER = ArgumentParser()
PARSER.add_argument("subreddit", nargs="?", default="wallpaper")
PARSER.add_argument("--count", "-n", type=int, default=200)
PARSER.add_argument("--clear", action="store_true")


def main():
  """Download wallpapers from a Reddit subreddit."""
  params = PARSER.parse_args()

  WALLPAPER_FOLDER.mkdir(parents=True, exist_ok=True)
  if params.clear:
    message(f"Clearing: {WALLPAPER_FOLDER}")
    shutil.rmtree(WALLPAPER_FOLDER)
    WALLPAPER_FOLDER.mkdir()

  urls = list(islice(fetch_urls(params.subreddit), params.count))
  if not urls:
    message("No image URLs found")
    return 1
  
  message(f"Found {len(urls)} image URLs")

  n0 = len(list(WALLPAPER_FOLDER.iterdir()))

  asyncio.run(download_images(urls, WALLPAPER_FOLDER))
  purge_small_images(WALLPAPER_FOLDER)

  n1 = len(list(WALLPAPER_FOLDER.iterdir()))
  message(f"<< There are {n1 - n0} new files >>")
  return 0
