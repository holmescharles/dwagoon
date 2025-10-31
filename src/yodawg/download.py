import asyncio
from pathlib import Path

from aiohttp import ClientSession, ClientTimeout

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


async def download_images(urls, output):
  """Download images concurrently to the specified folder."""
  folder = Path(output)
  folder.mkdir(parents=True, exist_ok=True)

  async with ClientSession() as session:
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)

    async def download(url):
      async with semaphore:
        data = await get_image(session, url)
        if data is None:
          return

        file = folder / url.split("/")[-1].split("?")[0]
        if file.exists():
          message(f"Cached: {url}")
          return

        try:
          with open(file, "wb") as f:
            f.write(data)
            message(f"Downloaded: {url}")
        except Exception as e:
          message(f"Failed to save {url}: {e}")

    tasks = [asyncio.create_task(download(url)) for url in urls]
    await asyncio.gather(*tasks)

