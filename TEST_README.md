# Boring Image Detection Tests

This directory contains two test scripts for the boring background detection algorithm.

## Test Scripts

### 1. `test_boring_detection.py` - Synthetic Test

This script generates synthetic test images with known properties to validate the algorithm.

**Usage:**
```bash
python test_boring_detection.py
```

**What it does:**
- Creates 8 synthetic test images (white/black backgrounds, gradients, etc.)
- Tests the boring detection algorithm on each
- Outputs BORING.txt and NOT_BORING.txt with local file paths
- Shows accuracy percentage

**Good for:**
- Quick validation that the algorithm works
- Testing changes to the detection logic
- No network connection required

---

### 2. `test_boring_detection_real.py` - Real Reddit Images Test

This script downloads actual images from Reddit and tests them.

**Usage:**
```bash
# Basic usage (downloads 1000 posts from r/animewallpapernsfw, tests 400 random ones)
python test_boring_detection_real.py

# Specify subreddit
python test_boring_detection_real.py wallpaper

# Custom count and sample size
python test_boring_detection_real.py animewallpapernsfw --count 5000 --sample 400

# Test all downloaded images (no sampling)
python test_boring_detection_real.py wallpaper --count 500 --sample 0

# Keep downloaded images for manual inspection
python test_boring_detection_real.py wallpaper --keep-images
```

**Options:**
- `subreddit` - Which subreddit to download from (default: animewallpapernsfw)
- `--count`, `-n` - Number of Reddit posts to fetch (default: 1000)
- `--sample`, `-s` - Number of random images to test (default: 400, use 0 for all)
- `--keep-images` - Keep downloaded images in test_images/ folder

**What it does:**
1. Fetches image URLs from specified subreddit
2. Downloads images to `test_images/` directory
3. Runs boring detection on each image
4. Outputs BORING.txt and NOT_BORING.txt with Reddit URLs
5. Cleans up images (unless --keep-images flag is used)

**Output:**
- `BORING.txt` - List of Reddit URLs for images classified as boring
- `NOT_BORING.txt` - List of Reddit URLs for images classified as not boring
- Shows percentage breakdown

**Good for:**
- Testing on real-world images
- Validating detection accuracy
- Building a dataset of boring vs not-boring images

---

## Running from WSL (Windows Subsystem for Linux)

1. **Install YoDawg:**
   ```bash
   cd /path/to/yodawg
   pip install -e .
   ```

2. **Run the real image test:**
   ```bash
   # Download 1000 images, test 400 random ones
   python test_boring_detection_real.py animewallpapernsfw --count 1000 --sample 400
   ```

3. **Check the results:**
   ```bash
   # See how many were classified as boring
   wc -l BORING.txt NOT_BORING.txt
   
   # View some boring image URLs
   head BORING.txt
   
   # View some not-boring image URLs
   head NOT_BORING.txt
   ```

4. **Keep images for manual inspection:**
   ```bash
   python test_boring_detection_real.py wallpaper --count 200 --keep-images
   
   # Images will be in test_images/
   ls test_images/
   ```

## Understanding the Algorithm

The boring background detection algorithm:

1. **Samples border pixels** (top, bottom, left, right edges)
2. **Calculates brightness** for each pixel (RGB average)
3. **Counts white pixels** (brightness > 240)
4. **Counts black pixels** (brightness < 15)
5. **Classifies as boring** if >70% of border is white OR black

**Adjustable in config.py:**
```python
BORING_BACKGROUND_THRESHOLD = 0.7  # 70% threshold
```

## Example Output

```
=== Boring Image Detection Test ===
Subreddit: r/animewallpapernsfw
Fetching up to 1000 posts
Sample size: 400

Fetching URLs from r/animewallpapernsfw...
Found 982 image URLs
Randomly selected 400 URLs for testing

Downloading 400 images to test_images/...
Successfully downloaded 387 images

Testing boring image detection on 387 images...
  Progress: 50/387 images processed...
  Progress: 100/387 images processed...
  Progress: 150/387 images processed...
  Progress: 200/387 images processed...
  Progress: 250/387 images processed...
  Progress: 300/387 images processed...
  Progress: 350/387 images processed...
  Progress: 387/387 images processed...

=== Results ===
Boring images: 45 (11.6%)
Not boring images: 342 (88.4%)

Results written to:
  BORING.txt (45 URLs)
  NOT_BORING.txt (342 URLs)

Cleaning up test images...
Test images deleted (use --keep-images to preserve)

=== Test Complete ===
```

## Interpreting Results

- **High boring %** (>30%) - Algorithm might be too sensitive, consider lowering threshold
- **Low boring %** (<5%) - Algorithm might be too lenient, consider raising threshold
- **Moderate boring %** (5-20%) - Algorithm is working as expected

You can manually inspect some URLs from BORING.txt and NOT_BORING.txt to verify if the classification makes sense.
