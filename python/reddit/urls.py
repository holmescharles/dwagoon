import requests
from .message import message


def fetch_reddit_page(subreddit, after=None):
  message(f"Fetching posts from r/{subreddit} (after={after})")
  response = requests.get(
    url=f"https://www.reddit.com/r/{subreddit}/.json",
    headers={"User-Agent": "wallpaper-download-cdh"},
    params={"limit": 100, "after": after},
  )
  response.raise_for_status()
  return response.json()


def extract_urls_from_gallery(post):
  gallery_data = post.get("gallery_data")
  if gallery_data is None:
    return
  media_metadata = post.get("media_metadata", {})
  for item in gallery_data.get("items", []):
    media_id = item.get("media_id")
    if media_id and media_id in media_metadata:
      mime_type = media_metadata[media_id].get("m", "")
      if "/" in mime_type:
        ext = mime_type.split("/")[-1]
        yield f"https://i.redd.it/{media_id}.{ext}"


def extract_urls_from_page(page):
  for child in page["data"]["children"]:
    post = child["data"]
    url = post.get("url", "")
    if url.startswith("https://www.reddit.com/gallery/"):
      yield from extract_urls_from_gallery(post)
    elif url.endswith((".jpg", ".jpeg", ".png")):
      yield url


def fetch_reddit_pages(subreddit):
  after = None
  while True:
    page = fetch_reddit_page(subreddit, after=after)
    yield page
    after = page["data"]["after"]
    if after is None:
      break


def fetch_urls(subreddit):
  for page in fetch_reddit_pages(subreddit):
    for url in extract_urls_from_page(page):
      yield url
