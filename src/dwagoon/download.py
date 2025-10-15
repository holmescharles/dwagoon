import asyncio
from pathlib import Path

from aiohttp import ClientSession, ClientTimeout

from .message import message


MAX_CONCURRENT = 10
HEADERS = {"User-Agent": "wallpaper-download"}


async def get_image(session, url):
  for attempt in range(5):
    try:
      async with session.get(
        url, headers=HEADERS,
        timeout=ClientTimeout(total=30),
      ) as response:
        response.raise_for_status()
        return await response.read()
    except Exception as e:
      await asyncio.sleep(1 + attempt)
      message(f"Retry {attempt + 1} for {url}: {e}")
  message(f"Failed to download: {url}")   



async def download_images(urls, output):
  folder = Path(output)
  folder.mkdir(parents=True, exist_ok=True)

  async with ClientSession() as session:
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

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
          message(f"Failed: {url}")

    tasks = [asyncio.create_task(download(url)) for url in urls]
    await asyncio.gather(*tasks)
