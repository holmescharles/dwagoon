"""Configuration settings for YoDawg."""
from pathlib import Path

# Wallpaper download folder
WALLPAPER_FOLDER = Path.home() / "Downloads" / "Wallpapers"

# Saved wallpapers folder
SAVED_WALLPAPER_FOLDER = Path.home() / "Pictures" / "saved_wallpapers"

# Minimum image width (images smaller than this are filtered out)
MIN_IMAGE_WIDTH = 1920

# Maximum concurrent downloads
MAX_CONCURRENT_DOWNLOADS = 10

# Download retry attempts
MAX_DOWNLOAD_RETRIES = 5

# Download timeout in seconds
DOWNLOAD_TIMEOUT = 30
