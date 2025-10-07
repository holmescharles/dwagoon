from argparse import ArgumentParser
from pathlib import Path
import sys

from PIL import Image
from joblib import Parallel, delayed
import requests


def fetch_reddit_page(subreddit):
  message(f"Fetching posts from r/{subreddit}")
  response = requests.get(
    url=f"https://www.reddit.com/r/{subreddit}/.json",
    headers={"User-Agent": "wallpaper-download-cdh"},
    params={"limit": 100},
  )
  response.raise_for_status()
  return response.json()


def extract_urls(page):
  for child in page["data"]["children"]:
    post = child["data"]
    url = post.get("url", "")

    if url.startswith("https://www.reddit.com/gallery/"):
      gallery_data = post.get("gallery_data", {})
      media_metadata = post.get("media_metadata", {})

      for item in gallery_data.get("items", []):
        media_id = item.get("media_id")
        if media_id and media_id in media_metadata:
          mime_type = media_metadata[media_id].get("m", "")
          if "/" in mime_type:
            ext = mime_type.split("/")[-1]
            yield f"https://i.redd.it/{media_id}.{ext}"

    else:
      if url.endswith((".jpg", ".jpeg", ".png")):
        yield url


def message(*args):
  print(*args, file=sys.stderr)


def download_image(url, folder):
  folder = Path(folder)
  file = folder / url.split("/")[-1]
  try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    file.write_bytes(response.content)
    return file
  except Exception as e:
    message(f"Failed to download {url}: {e}")
    return None

def download_all_images(urls, folder, n_jobs=None):
  folder = Path(folder)

  folder.mkdir(parents=True, exist_ok=True)
  message(f"Downloading images to {folder}")

  results = Parallel(n_jobs=n_jobs, verbose=10)(
    delayed(download_image)(url, folder) for url in urls
  )
  downloads = [f for f in results if f is not None]
  message(f"Downloaded {len(downloads)} of {len(urls)} images")

  return downloads


def get_image_width(filepath):
  try:
    with Image.open(filepath) as img:
      return img.width
  except Exception as e:
    __import__('pdb').set_trace()
    message(f"Failed to read {filepath}: {e}")


def remove_small_images(filepaths, min_width=1920):
  count = 0;
  smalls = [f for f in filepaths if get_image_width(f) < 1920]
  for f in smalls:
    Path(f).unlink()
  message(f"Removed {len(smalls)} of {len(filepaths)} files <{min_width} pixels wide")



def main():

  parser = ArgumentParser()
  parser.add_argument("subreddit", nargs="?", default="wallpaper")
  parser.add_argument("-o", "--output", default="WALLPAPERS", type=Path)
  params = parser.parse_args()

  if params.output.exists():
    import shutil
    shutil.rmtree(params.output)

  page = fetch_reddit_page(params.subreddit)
  urls = list(extract_urls(page))
  downloads = download_all_images(urls, params.output, n_jobs=-1)
  removed = remove_small_images(downloads)


main()
