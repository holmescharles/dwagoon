# YoDawg Usage Guide

YoDawg is a wallpaper management tool that downloads wallpapers from Reddit and automatically generates color schemes for your terminal using pywal16.

## Table of Contents
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Commands](#commands)
  - [reddit](#reddit---download-wallpapers)
  - [rice](#rice---apply-wallpaper-and-color-scheme)
  - [save-wallpaper](#save-wallpaper---save-current-wallpaper)
  - [wal](#wal---pywal16-wrapper)
- [Configuration](#configuration)
- [Workflow](#workflow)
- [Platform-Specific Notes](#platform-specific-notes)

## Installation

### Standard Installation

```bash
pip install yodawg
```

### Development Installation

```bash
git clone https://github.com/holmescharles/yodawg.git
cd yodawg
pip install -e .
```

## Getting Started

1. **Download wallpapers** from a subreddit (default: r/wallpaper):
   ```bash
   reddit
   ```

2. **Apply a wallpaper** and generate color scheme:
   ```bash
   rice
   ```

That's it! YoDawg will randomly select a wallpaper from your downloaded collection and apply it along with a matching color scheme.

## Commands

### `reddit` - Download Wallpapers

Downloads image posts from Reddit subreddits with intelligent filtering and tracking.

**Usage:**
```bash
reddit [subreddit] [options]
```

**Arguments:**
- `subreddit` - Name of the subreddit to download from (default: `wallpaper`)

**Options:**
- `-n, --count COUNT` - Number of posts to fetch from Reddit (default: 200)
- `--new NEW` - Download only this many new wallpapers (filters out already downloaded)
- `--clear` - Clear existing wallpapers before downloading new ones
- `--nsfw` - Use NSFW channel (separate folder)
- `--filter-boring` - Filter out images with boring (white/black) backgrounds

**Examples:**
```bash
# Download 200 wallpapers from r/wallpaper
reddit

# Download from a specific subreddit
reddit EarthPorn

# Download more wallpapers
reddit wallpaper -n 500

# Download only 50 new wallpapers (skips already downloaded)
reddit --new 50

# Clear old wallpapers and download fresh ones
reddit --clear

# Download NSFW wallpapers to separate folder
reddit wallpapers_nsfw --nsfw

# Filter out boring white/black background images
reddit --filter-boring
```

**Details:**
- Downloads to `~/Downloads/Wallpapers/sfw/` by default (or `nsfw/` with --nsfw)
- Automatically filters out images smaller than 1920px width
- Tracks all downloaded and filtered files in a blacklist database
- Skips already downloaded images and blacklisted files
- Supports Reddit galleries
- Handles retries for failed downloads
- Can filter boring white/black background images

### `rice` - Apply Wallpaper and Color Scheme

Applies a wallpaper and generates a matching color scheme using pywal16.

**Usage:**
```bash
rice [image] [options]
```

**Arguments:**
- `image` - Path to a specific image file or folder (optional)

**Options:**
- `-l, --light` - Use light color scheme instead of dark
- `--nsfw` - Use NSFW wallpaper channel
- `--delete` - Blacklist current wallpaper and remove it

**Examples:**
```bash
# Apply random wallpaper from SFW folder
rice

# Apply random wallpaper from NSFW folder
rice --nsfw

# Apply specific wallpaper
rice ~/Pictures/myimage.jpg

# Use light theme
rice -l

# Delete current wallpaper and blacklist it
rice --delete

# Apply wallpaper from specific folder
rice ~/Pictures/Wallpapers/
```

**Details:**
- Runs `wal -i <image> --cols16` under the hood
- On Windows: Automatically updates Windows Terminal color scheme
- Generates 16 colors from the wallpaper
- Sets wallpaper and updates terminal colors in one command
- Can blacklist and remove wallpapers you don't like

### `save-wallpaper` - Save Current Wallpaper

Saves the currently applied wallpaper to a permanent collection.

**Usage:**
```bash
save-wallpaper
```

**Details:**
- Reads the current wallpaper from `~/.cache/wal/wal`
- Copies it to `~/Pictures/saved_wallpapers/`
- Useful for preserving wallpapers you want to keep

**Example workflow:**
```bash
rice                    # Try random wallpapers until you find one you like
save-wallpaper         # Save the one you like
```

### `wal` - pywal16 Wrapper

Direct access to pywal16 commands. YoDawg includes pywal16 as a dependency and provides the `wal` command for advanced usage.

**Usage:**
```bash
wal [pywal16-options]
```

See [pywal16 documentation](https://github.com/eylles/pywal16) for full options.

## Configuration

YoDawg stores all configuration settings in `src/yodawg/config.py`, making it easy to customize behavior.

### Configurable Settings

**Wallpaper Locations:**
```python
# SFW wallpaper folder (default)
WALLPAPER_FOLDER_SFW = Path.home() / "Downloads" / "Wallpapers" / "sfw"

# NSFW wallpaper folder
WALLPAPER_FOLDER_NSFW = Path.home() / "Downloads" / "Wallpapers" / "nsfw"

# Saved wallpapers location (default: ~/Pictures/saved_wallpapers)  
SAVED_WALLPAPER_FOLDER = Path.home() / "Pictures" / "saved_wallpapers"
```

**Image Filtering:**
```python
# Minimum image width in pixels (default: 1920)
MIN_IMAGE_WIDTH = 1920

# Boring background detection threshold (default: 0.7)
# Fraction of border pixels that must be white/black
BORING_BACKGROUND_THRESHOLD = 0.7
```

**Download Settings:**
```python
# Maximum concurrent downloads (default: 10)
MAX_CONCURRENT_DOWNLOADS = 10

# Number of retry attempts for failed downloads (default: 5)
MAX_DOWNLOAD_RETRIES = 5

# Download timeout in seconds (default: 30)
DOWNLOAD_TIMEOUT = 30
```

To customize these settings, edit `/path/to/yodawg/src/yodawg/config.py` with your preferred values.

## Blacklist Management

YoDawg tracks all processed files in a blacklist database to avoid re-downloading or re-processing files.

**Blacklist Reasons:**
- `TOO_SMALL` - Image was smaller than minimum width
- `DELETED` - User manually deleted the wallpaper
- `BORING_BACKGROUND` - Image had a boring white/black background

**Location:** The blacklist database is stored as `.blacklist.db` in each wallpaper folder (SFW and NSFW have separate databases).

**Workflow:**
1. When you download wallpapers, small images are automatically blacklisted
2. When you use `rice --delete`, the current wallpaper is blacklisted
3. Future downloads skip blacklisted files automatically
4. The `--new` flag only downloads files not in the blacklist

## Workflow

A typical YoDawg workflow:

1. **Initial Setup:**
   ```bash
   # Download a collection of SFW wallpapers
   reddit wallpaper -n 300
   reddit EarthPorn -n 200
   
   # Optionally download NSFW wallpapers
   reddit wallpapers_nsfw --nsfw -n 100
   ```

2. **Daily Use:**
   ```bash
   # Apply a random wallpaper from SFW collection
   rice
   
   # If you like it, save it
   save-wallpaper
   
   # If you don't like it, delete and blacklist it
   rice --delete
   
   # Then get a new one
   rice
   
   # Use NSFW wallpapers occasionally
   rice --nsfw
   ```

3. **Refresh Collection:**
   ```bash
   # Download only 50 new wallpapers (skips already downloaded)
   reddit --new 50
   
   # Download more wallpapers, filtering boring backgrounds
   reddit --filter-boring --new 100
   ```

4. **Clean Slate:**
   ```bash
   # Start fresh with new wallpapers
   reddit --clear
   ```

## Platform-Specific Notes

### Windows

On Windows, YoDawg automatically integrates with Windows Terminal:
- Runs `UpdateTerminal.ps1` after applying wallpaper
- Creates/updates a "cols16" color scheme in Windows Terminal settings
- Sets it as the default color scheme
- Works with both stable and preview versions of Windows Terminal

### Linux/macOS

On Unix systems:
- Uses standard pywal16 functionality
- Color scheme files are stored in `~/.cache/wal/`
- You may need to configure your terminal to use pywal colors
- See [pywal wiki](https://github.com/dylanaraps/pywal/wiki) for terminal integration

## SFW/NSFW Channel Management

YoDawg supports separate channels for SFW and NSFW content:

### How It Works
- **SFW Channel** (default): `~/Downloads/Wallpapers/sfw/`
- **NSFW Channel**: `~/Downloads/Wallpapers/nsfw/`
- Each channel has its own blacklist database
- Wallpapers never mix between channels

### Usage Examples
```bash
# Download SFW wallpapers (default)
reddit wallpaper -n 200

# Download NSFW wallpapers to separate folder
reddit wallpapers_nsfw --nsfw -n 100

# Apply SFW wallpaper (default)
rice

# Apply NSFW wallpaper
rice --nsfw

# Delete and blacklist from current channel
rice --delete
```

### Benefits
- Keep work-appropriate and personal wallpapers separate
- Each channel maintains its own download history
- Easy to switch between channels with `--nsfw` flag

## Troubleshooting

### No wallpapers downloaded
- Check your internet connection
- Verify the subreddit name is correct
- Some subreddits may have rate limiting

### Colors not applying
- Ensure pywal16 is working: `wal --version`
- On Windows, check Windows Terminal is installed
- On Linux/macOS, verify terminal supports color schemes

### Images too small
- YoDawg filters images smaller than 1920px
- Use subreddits with high-resolution images like r/wallpaper or r/WidescreenWallpaper

### Too many boring backgrounds
- Use `--filter-boring` flag when downloading
- Adjusts `BORING_BACKGROUND_THRESHOLD` in config.py (default: 0.7)

## Advanced Usage

### Custom Pywal Options

You can use the `wal` command directly for more control:

```bash
# Generate colors without setting wallpaper
wal -i image.jpg -n

# Use specific backend
wal -i image.jpg --backend colorz

# Generate light theme
wal -l -i image.jpg
```

### Scripting

Combine commands in scripts:

```bash
#!/bin/bash
# Download and apply new wallpaper daily
reddit wallpaper -n 50
rice
```

## Dependencies

YoDawg requires:
- Python 3.7+
- requests - HTTP library
- aiohttp - Async HTTP for fast downloads
- pillow - Image processing
- pywal16 - Color scheme generation
- colorz - Color extraction

All dependencies are automatically installed with YoDawg.
