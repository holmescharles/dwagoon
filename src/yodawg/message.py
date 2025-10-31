"""Utility function for printing messages to stderr."""
import sys


def message(*args):
  """Print message to stderr for better separation from stdout."""
  print(*args, file=sys.stderr)
