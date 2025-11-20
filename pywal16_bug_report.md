# pywal16 --cols16 Bug Report

## Issue: `--cols16` crashes when image has 8-15 unique colors (wal backend)

The `wal` backend crashes with `--cols16` on images that generate 8-15 unique colors. The code requires 16+ colors but only validates for 8+, causing an index error.

### Command Run
```bash
wal -i /path/to/image.jpg --cols16
```

### Expected Behavior
Generate a 16-color scheme from the image.

### Actual Behavior
Crashes with:
```
Traceback (most recent call last):
  File "pywal/colors.py", line 141, in shade_16
    colors[k_v[15]] = util.darken_color(colors[k_v[0]], 0.75)
```

### Root Cause
Found the bug in `wal.py:107`:

```python
raw_colors = cols[:1] + cols[8:16] + cols[8:-1]
```

This slicing requires 16+ colors to work, but line 57 only validates for 8+ colors:

```python
if len(raw_colors) > 7:  # Only checks for 8+
    break
```

When ImageMagick returns 8-15 colors, the slicing produces only 1 color (`cols[:1]`), since `cols[8:16]` and `cols[8:-1]` are empty. Then `shade_16()` tries to access colors that don't exist.

### Suggested Fix
Two-part fix needed:

1. **Change validation** in `wal.py` line 57:
```python
if len(raw_colors) > 15:  # Require 16+ colors for --cols16 support
```

2. **Add fallback logic** in `adjust()` function:
```python
def adjust(cols, light, **kwargs):
    if "c16" in kwargs:
        cols16 = kwargs["c16"]
    else:
        cols16 = False

    if cols16 and len(cols) < 16:
        # Not enough colors for 16-color mode, fall back to 8-color mode
        import logging
        logging.warning("--cols16 requested but only %d colors available, falling back to 8 colors", len(cols))
        cols16 = False

    raw_colors = cols[:1] + cols[8:16] + cols[8:-1]
    return colors.generic_adjust(raw_colors, light, c16=cols16)
```

### System Info
- macOS 15.7.2
- pywal16 3.8.11
- Python 3.13

### Workaround
Remove `--cols16` or use a different backend like `colorz`.

### Status
- Issue identified and root cause found
- Partial fix implemented in fork at https://github.com/holmescharles/pywal16
- Needs testing and PR creation