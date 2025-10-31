"""Configuration settings for YoDawg."""
from pathlib import Path

# Wallpaper download base folder
WALLPAPER_BASE_FOLDER = Path.home() / "Downloads" / "Wallpapers"

# SFW and NSFW subfolders
WALLPAPER_FOLDER_SFW = WALLPAPER_BASE_FOLDER / "sfw"
WALLPAPER_FOLDER_NSFW = WALLPAPER_BASE_FOLDER / "nsfw"

# Default wallpaper folder (SFW)
WALLPAPER_FOLDER = WALLPAPER_FOLDER_SFW

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

# Boring background detection threshold (0.0-1.0)
# Fraction of border pixels that must be white/black to be considered boring
BORING_BACKGROUND_THRESHOLD = 0.7
