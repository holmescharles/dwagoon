"""Download wallpapers from Reddit."""
from argparse import ArgumentParser
import asyncio
from itertools import islice
from pathlib import Path
import shutil

from .blacklist import BlacklistDB, BlacklistReason
from .config import WALLPAPER_FOLDER_SFW, WALLPAPER_FOLDER_NSFW
from .imageanalysis import is_boring_background
from .message import message
from .urls import fetch_urls
from .download import download_images
from .toosmall import purge_small_images


PARSER = ArgumentParser()
PARSER.add_argument("subreddit", nargs="?", default="wallpaper")
PARSER.add_argument("--count", "-n", type=int, default=200, 
                    help="Number of posts to fetch from Reddit")
PARSER.add_argument("--new", type=int, 
                    help="Download only this many new wallpapers")
PARSER.add_argument("--clear", action="store_true",
                    help="Clear existing wallpapers before downloading")
PARSER.add_argument("--nsfw", action="store_true",
                    help="Use NSFW channel (separate folder)")
PARSER.add_argument("--filter-boring", action="store_true",
                    help="Filter out images with boring (white/black) backgrounds")


def main():
  """Download wallpapers from a Reddit subreddit."""
  params = PARSER.parse_args()

  # Choose folder based on NSFW flag
  wallpaper_folder = WALLPAPER_FOLDER_NSFW if params.nsfw else WALLPAPER_FOLDER_SFW
  channel_name = "NSFW" if params.nsfw else "SFW"
  
  message(f"Using {channel_name} channel: {wallpaper_folder}")
  
  wallpaper_folder.mkdir(parents=True, exist_ok=True)
  
  # Initialize blacklist database
  blacklist_db = BlacklistDB(wallpaper_folder / ".blacklist.db")
  
  if params.clear:
    message(f"Clearing: {wallpaper_folder}")
    shutil.rmtree(wallpaper_folder)
    wallpaper_folder.mkdir()
    # Reinitialize blacklist after clearing
    blacklist_db = BlacklistDB(wallpaper_folder / ".blacklist.db")

  urls = list(islice(fetch_urls(params.subreddit), params.count))
  if not urls:
    message("No image URLs found")
    return 1
  
  message(f"Found {len(urls)} image URLs from r/{params.subreddit}")

  n0 = len(list(wallpaper_folder.iterdir()))

  # Download with max_new limit if specified
  asyncio.run(download_images(urls, wallpaper_folder, blacklist_db, params.new))
  
  # Filter small images
  purge_small_images(wallpaper_folder, blacklist_db)
  
  # Filter boring backgrounds if requested
  if params.filter_boring:
    message("Filtering images with boring backgrounds...")
    for image_file in wallpaper_folder.iterdir():
      if not image_file.is_file() or image_file.name.startswith('.'):
        continue
      
      if is_boring_background(image_file):
        blacklist_db.add(image_file.name, BlacklistReason.BORING_BACKGROUND)
        image_file.unlink()

  n1 = len(list(wallpaper_folder.iterdir()))
  message(f"<< There are {n1 - n0} new files in {channel_name} channel >>")
  return 0
