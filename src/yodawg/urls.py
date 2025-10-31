"""Fetch image URLs from Reddit."""
import requests

from .message import message


def fetch_reddit_page(subreddit, after=None):
  """Fetch a single page of posts from a subreddit."""
  message(f"Fetching posts from r/{subreddit} (after={after})")
  try:
    response = requests.get(
      url=f"https://www.reddit.com/r/{subreddit}/.json",
      headers={"User-Agent": "wallpaper-download-cdh"},
      params={"limit": 100, "after": after},
      timeout=10,
    )
    response.raise_for_status()
    return response.json()
  except requests.RequestException as e:
    message(f"Error fetching from Reddit: {e}")
    return None


def extract_urls_from_gallery(post):
  """Extract image URLs from a Reddit gallery post."""
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
  """Extract all image URLs from a Reddit page."""
  if page is None:
    return
  
  for child in page.get("data", {}).get("children", []):
    post = child.get("data", {})
    url = post.get("url", "")
    if url.startswith("https://www.reddit.com/gallery/"):
      yield from extract_urls_from_gallery(post)
    elif url.endswith((".jpg", ".jpeg", ".png")):
      yield url


def fetch_reddit_pages(subreddit):
  """Fetch all available pages from a subreddit."""
  after = None
  while True:
    page = fetch_reddit_page(subreddit, after=after)
    if page is None:
      break
    
    yield page
    after = page.get("data", {}).get("after")
    if after is None:
      break


def fetch_urls(subreddit):
  """Fetch all image URLs from a subreddit."""
  for page in fetch_reddit_pages(subreddit):
    for url in extract_urls_from_page(page):
      yield url
