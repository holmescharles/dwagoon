import asyncio
from pathlib import Path

from aiohttp import ClientSession, ClientTimeout

from .blacklist import BlacklistDB
from .config import (
    MAX_CONCURRENT_DOWNLOADS,
    MAX_DOWNLOAD_RETRIES,
    DOWNLOAD_TIMEOUT,
    WALLPAPER_FOLDER,
)
from .message import message


HEADERS = {"User-Agent": "wallpaper-download"}


async def get_image(session, url):
  """Download image with retry logic."""
  for attempt in range(MAX_DOWNLOAD_RETRIES):
    try:
      async with session.get(
        url, headers=HEADERS,
        timeout=ClientTimeout(total=DOWNLOAD_TIMEOUT),
      ) as response:
        response.raise_for_status()
        return await response.read()
    except Exception as e:
      await asyncio.sleep(1 + attempt)
      message(f"Retry {attempt + 1} for {url}: {e}")
  message(f"Failed to download: {url}")
  return None


def get_filename_from_url(url):
  """Extract filename from URL."""
  return url.split("/")[-1].split("?")[0]


def filter_new_urls(urls, folder, blacklist_db=None):
  """
  Filter URLs to only include new images (not already downloaded or blacklisted).
  
  Args:
      urls: List of image URLs
      folder: Path to wallpaper folder
      blacklist_db: BlacklistDB instance (optional)
  
  Returns:
      List of URLs that are new (not cached and not blacklisted)
  """
  if blacklist_db is None:
    blacklist_db = BlacklistDB()
  
  folder = Path(folder)
  new_urls = []
  
  for url in urls:
    filename = get_filename_from_url(url)
    
    # Check if blacklisted
    if blacklist_db.is_blacklisted(filename):
      message(f"Skipping blacklisted: {filename}")
      continue
    
    # Check if already downloaded
    file_path = folder / filename
    if file_path.exists():
      message(f"Already downloaded: {filename}")
      continue
    
    new_urls.append(url)
  
  return new_urls


async def download_images(urls, output, blacklist_db=None, max_new=None):
  """
  Download images concurrently to the specified folder.
  
  Args:
      urls: List of image URLs
      output: Output folder path
      blacklist_db: BlacklistDB instance (optional)
      max_new: Maximum number of new images to download (optional)
  """
  folder = Path(output)
  folder.mkdir(parents=True, exist_ok=True)
  
  if blacklist_db is None:
    blacklist_db = BlacklistDB()
  
  # Filter to only new URLs
  new_urls = filter_new_urls(urls, folder, blacklist_db)
  
  # Limit if max_new is specified
  if max_new is not None and len(new_urls) > max_new:
    message(f"Limiting to {max_new} new downloads from {len(new_urls)} available")
    new_urls = new_urls[:max_new]
  
  if not new_urls:
    message("No new images to download")
    return

  async with ClientSession() as session:
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)

    async def download(url):
      async with semaphore:
        data = await get_image(session, url)
        if data is None:
          return

        file = folder / get_filename_from_url(url)
        
        try:
          with open(file, "wb") as f:
            f.write(data)
            message(f"Downloaded: {url}")
        except Exception as e:
          message(f"Failed to save {url}: {e}")

    tasks = [asyncio.create_task(download(url)) for url in new_urls]
    await asyncio.gather(*tasks)

