import sys


def message(*args):
  print(*args, file=sys.stderr)
