from argparse import ArgumentParser
import sys


def print_version():
    """Print yodawg and pywal versions."""
    # Get yodawg version
    try:
        from importlib.metadata import version
        yodawg_version = version("yodawg")
    except Exception:
        yodawg_version = "unknown"
    
    # Get pywal version
    try:
        from importlib.metadata import version
        pywal_version = version("pywal16")
    except Exception:
        pywal_version = "unknown"
    
    print(f"yodawg {yodawg_version} (pywal16 {pywal_version})")


def main():
    parser = ArgumentParser(prog="yodawg", description="Download wallpapers and manage rice")
    parser.add_argument("-V", "--version", action="store_true", help="Show version information")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # reddit subcommand
    reddit_parser = subparsers.add_parser("reddit", help="Download wallpapers from Reddit")
    reddit_parser.add_argument("subreddit", nargs="?", default="wallpaper")
    reddit_parser.add_argument("--count", "-n", type=int, default=200)
    reddit_parser.add_argument("--clear", action="store_true")

    # rice subcommand
    rice_parser = subparsers.add_parser("rice", help="Apply color scheme from wallpaper")
    rice_parser.add_argument("-l", "--light", action="store_true", help="use light color scheme (default is dark)")
    rice_parser.add_argument(
        "image",
        nargs="?",
        help="path to wallpaper image or folder of images",
    )

    # save subcommand
    save_parser = subparsers.add_parser("save", help="Save current wallpaper to Pictures folder")

    args = parser.parse_args()

    if args.version:
        print_version()
        sys.exit(0)

    if args.command == "reddit":
        from .reddit import main as reddit_main
        reddit_main(args)
    elif args.command == "rice":
        from .rice import main as rice_main
        rice_main(args)
    elif args.command == "save":
        from .savewall import main as savewall_main
        savewall_main(args)
    else:
        parser.print_help()
        sys.exit(1)
