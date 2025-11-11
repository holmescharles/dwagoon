"""
Yodawg package initialization.
Applies monkeypatches to pywal to fix palette handling.
"""


def _monkeypatch_pywal():
    """
    Monkeypatch pywal.colors to handle backends that return fewer than 16 colors.
    This prevents IndexError in shade_16 and generic_adjust functions.
    """
    try:
        import pywal.colors
    except ImportError:
        # pywal not installed, skip patching
        return

    original_get = pywal.colors.get

    def patched_get(img, *args, **kwargs):
        """Wrap pywal.colors.get to extend short palettes."""
        colors = original_get(img, *args, **kwargs)

        # Ensure colors["colors"] has at least 16 entries
        if "colors" in colors and isinstance(colors["colors"], dict):
            color_keys = sorted(
                [k for k in colors["colors"].keys() if k.startswith("color")],
                key=lambda x: int(x.replace("color", "")),
            )
            num_colors = len(color_keys)

            if num_colors < 16:
                # Extend palette by repeating last color or using black
                last_color = (
                    colors["colors"][color_keys[-1]] if color_keys else "#000000"
                )
                for i in range(num_colors, 16):
                    colors["colors"][f"color{i}"] = last_color

        return colors

    pywal.colors.get = patched_get


# Apply monkeypatch on import
_monkeypatch_pywal()
