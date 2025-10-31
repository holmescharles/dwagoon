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

Downloads image posts from Reddit subreddits.

**Usage:**
```bash
reddit [subreddit] [options]
```

**Arguments:**
- `subreddit` - Name of the subreddit to download from (default: `wallpaper`)

**Options:**
- `-n, --count COUNT` - Number of posts to fetch (default: 200)
- `--clear` - Clear existing wallpapers before downloading new ones

**Examples:**
```bash
# Download 200 wallpapers from r/wallpaper
reddit

# Download from a specific subreddit
reddit EarthPorn

# Download more wallpapers
reddit wallpaper -n 500

# Clear old wallpapers and download fresh ones
reddit --clear
```

**Details:**
- Downloads to `~/Downloads/Wallpapers/` by default
- Automatically filters out images smaller than 1920px width
- Skips already downloaded images
- Supports Reddit galleries
- Handles retries for failed downloads

### `rice` - Apply Wallpaper and Color Scheme

Applies a wallpaper and generates a matching color scheme using pywal16.

**Usage:**
```bash
rice [image] [options]
```

**Arguments:**
- `image` - Path to a specific image file or folder (default: `~/Downloads/Wallpapers/`)

**Options:**
- `-l, --light` - Use light color scheme instead of dark

**Examples:**
```bash
# Apply random wallpaper from default folder
rice

# Apply specific wallpaper
rice ~/Pictures/myimage.jpg

# Use light theme
rice -l

# Apply wallpaper from specific folder
rice ~/Pictures/Wallpapers/
```

**Details:**
- Runs `wal -i <image> --cols16` under the hood
- On Windows: Automatically updates Windows Terminal color scheme
- Generates 16 colors from the wallpaper
- Sets wallpaper and updates terminal colors in one command

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

### Wallpaper Download Location

By default, wallpapers are downloaded to `~/Downloads/Wallpapers/`. This is defined in `src/yodawg/download.py`:

```python
WALLPAPER_FOLDER = Path.home() / "Downloads" / "Wallpapers"
```

### Image Size Filtering

Images smaller than 1920px width are automatically removed. This is defined in `src/yodawg/toosmall.py`:

```python
if width < 1920:
```

### Concurrent Downloads

Maximum concurrent downloads is set to 10 in `src/yodawg/download.py`:

```python
MAX_CONCURRENT = 10
```

## Workflow

A typical YoDawg workflow:

1. **Initial Setup:**
   ```bash
   # Download a collection of wallpapers
   reddit wallpaper -n 300
   reddit EarthPorn -n 200
   ```

2. **Daily Use:**
   ```bash
   # Apply a random wallpaper from your collection
   rice
   
   # If you like it, save it
   save-wallpaper
   
   # If you don't like it, just run rice again
   rice
   ```

3. **Refresh Collection:**
   ```bash
   # Download more wallpapers periodically
   reddit
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
