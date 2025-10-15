from pathlib import Path

from ..message import message


def main():
  wal_file = Path.home() / ".cache" / "wal" / "wal"
  with wal_file.open() as f:
    image_file = Path(f.readline())

  saved_file = Path.home() / "Pictures" / "saved_wallpapers" / image_file.name
  saved_file.parent.mkdir(parents=True, exist_ok=True)

  with image_file.open("rb") as fin, saved_file.open("wb") as fout:
    fout.write(fin.read())

  message(f"Saved: {saved_file}")
