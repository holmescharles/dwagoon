#!/usr/bin/env python3
"""
Real-world test script for boring image detection.

This script downloads actual images from Reddit (e.g., r/animewallpapernsfw)
and tests the boring background detection algorithm on them.

Usage:
    python test_boring_detection_real.py [subreddit] [--count COUNT] [--sample SAMPLE]

Examples:
    # Download 1000 images from animewallpapernsfw, test 400 random ones
    python test_boring_detection_real.py animewallpapernsfw --count 1000 --sample 400
    
    # Download 500 images from wallpaper, test all of them
    python test_boring_detection_real.py wallpaper --count 500

This will create:
    - test_images/ directory with downloaded images
    - BORING.txt with URLs of boring images
    - NOT_BORING.txt with URLs of not boring images
"""
import asyncio
import argparse
from itertools import islice
from pathlib import Path
import random
import sys

# Add src to path so we can import yodawg modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from yodawg.urls import fetch_urls
from yodawg.download import download_images
from yodawg.imageanalysis import is_boring_background
from yodawg.message import message


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Test boring image detection on real Reddit images'
    )
    parser.add_argument(
        'subreddit',
        nargs='?',
        default='animewallpapernsfw',
        help='Subreddit to download from (default: animewallpapernsfw)'
    )
    parser.add_argument(
        '--count', '-n',
        type=int,
        default=1000,
        help='Number of posts to fetch from Reddit (default: 1000)'
    )
    parser.add_argument(
        '--sample', '-s',
        type=int,
        default=400,
        help='Number of random images to test (default: 400, use 0 for all)'
    )
    parser.add_argument(
        '--keep-images',
        action='store_true',
        help='Keep downloaded images in test_images/ (default: delete after testing)'
    )
    return parser.parse_args()


async def main():
    """Download images from Reddit and test boring detection."""
    args = parse_args()
    
    print(f"=== Boring Image Detection Test ===")
    print(f"Subreddit: r/{args.subreddit}")
    print(f"Fetching up to {args.count} posts")
    print(f"Sample size: {args.sample if args.sample > 0 else 'all'}")
    print()
    
    # Fetch URLs from Reddit
    print(f"Fetching URLs from r/{args.subreddit}...")
    urls = list(islice(fetch_urls(args.subreddit), args.count))
    
    if not urls:
        print("Error: No image URLs found")
        return 1
    
    print(f"Found {len(urls)} image URLs")
    
    # Determine sample size
    if args.sample > 0 and args.sample < len(urls):
        sampled_urls = random.sample(urls, args.sample)
        print(f"Randomly selected {len(sampled_urls)} URLs for testing")
    else:
        sampled_urls = urls
        print(f"Testing all {len(sampled_urls)} images")
    
    # Create test directory
    test_dir = Path("test_images")
    test_dir.mkdir(exist_ok=True)
    
    # Download images
    print(f"\nDownloading {len(sampled_urls)} images to {test_dir}/...")
    await download_images(sampled_urls, test_dir)
    
    # Get list of downloaded images
    downloaded = list(test_dir.glob("*"))
    downloaded = [f for f in downloaded if f.is_file() and not f.name.startswith('.')]
    print(f"Successfully downloaded {len(downloaded)} images")
    
    if not downloaded:
        print("Error: No images were downloaded")
        return 1
    
    # Create URL mapping (filename -> URL)
    url_map = {}
    for url in sampled_urls:
        filename = url.split("/")[-1].split("?")[0]
        url_map[filename] = url
    
    # Test boring detection on each image
    boring_urls = []
    not_boring_urls = []
    errors = []
    
    print(f"\nTesting boring image detection on {len(downloaded)} images...")
    for i, image_file in enumerate(downloaded, 1):
        if i % 50 == 0 or i == len(downloaded):
            print(f"  Progress: {i}/{len(downloaded)} images processed...")
        
        try:
            is_boring = is_boring_background(image_file)
            url = url_map.get(image_file.name, f"unknown/{image_file.name}")
            
            if is_boring:
                boring_urls.append(url)
            else:
                not_boring_urls.append(url)
        except Exception as e:
            errors.append((image_file.name, str(e)))
            print(f"  Warning: Error processing {image_file.name}: {e}")
    
    # Write results
    print(f"\n=== Results ===")
    print(f"Boring images: {len(boring_urls)} ({100*len(boring_urls)/len(downloaded):.1f}%)")
    print(f"Not boring images: {len(not_boring_urls)} ({100*len(not_boring_urls)/len(downloaded):.1f}%)")
    if errors:
        print(f"Errors: {len(errors)}")
    
    # Write URLs to files
    with open("BORING.txt", "w") as f:
        f.write(f"# Boring images from r/{args.subreddit}\n")
        f.write(f"# Total: {len(boring_urls)} images\n")
        f.write(f"# Detection threshold: >70% of border must be white or black\n")
        f.write(f"#\n")
        for url in sorted(boring_urls):
            f.write(f"{url}\n")
    
    with open("NOT_BORING.txt", "w") as f:
        f.write(f"# Not boring images from r/{args.subreddit}\n")
        f.write(f"# Total: {len(not_boring_urls)} images\n")
        f.write(f"# Detection threshold: >70% of border must be white or black\n")
        f.write(f"#\n")
        for url in sorted(not_boring_urls):
            f.write(f"{url}\n")
    
    print(f"\nResults written to:")
    print(f"  BORING.txt ({len(boring_urls)} URLs)")
    print(f"  NOT_BORING.txt ({len(not_boring_urls)} URLs)")
    
    # Clean up images unless --keep-images flag is set
    if not args.keep_images:
        print(f"\nCleaning up test images...")
        for image_file in downloaded:
            image_file.unlink()
        # Try to remove directory if empty
        try:
            test_dir.rmdir()
        except:
            pass
        print(f"Test images deleted (use --keep-images to preserve)")
    else:
        print(f"\nTest images kept in {test_dir}/")
    
    print(f"\n=== Test Complete ===")
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
