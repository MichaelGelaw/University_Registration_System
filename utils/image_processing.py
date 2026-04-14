import os
from PIL import Image, ImageOps, ImageTk, ImageDraw

AVATARS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "avatars")
os.makedirs(AVATARS_DIR, exist_ok=True)

def _resolve_avatar_path(avatar_path):
    """
    Accepts either:
      - A filename-only string like 'jsmith24_avatar.png'  → resolved to AVATARS_DIR/filename
      - A full absolute path (legacy / during transition)  → used as-is
    Returns the resolved absolute path, or None if empty/missing.
    """
    if not avatar_path:
        return None
    # If it's already absolute and exists, use it directly
    if os.path.isabs(avatar_path):
        return avatar_path if os.path.exists(avatar_path) else None
    # Otherwise treat as a filename relative to AVATARS_DIR
    resolved = os.path.join(AVATARS_DIR, avatar_path)
    return resolved if os.path.exists(resolved) else None

def process_avatar(avatar_path, size=(100, 100)):
    """
    Takes an avatar path (filename-only or absolute), resizes it, applies a
    circular mask, and returns a Tkinter-compatible PhotoImage.
    """
    resolved = _resolve_avatar_path(avatar_path)
    if not resolved:
        return None

    try:
        img = Image.open(resolved).convert("RGBA")

        # Crop to square first
        min_dim = min(img.size)
        left = (img.size[0] - min_dim) / 2
        top  = (img.size[1] - min_dim) / 2
        right  = (img.size[0] + min_dim) / 2
        bottom = (img.size[1] + min_dim) / 2
        img = img.crop((left, top, right, bottom))

        # Resize
        img = img.resize(size, Image.Resampling.LANCZOS)

        # Apply circular mask
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)

        output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)

        return ImageTk.PhotoImage(output)
    except Exception as e:
        print(f"Error processing image '{resolved}': {e}")
        return None

def save_avatar_file(source_path, username):
    """
    Copies the source image into the internal avatars folder.
    Returns the **filename only** (e.g. 'jsmith24_avatar.png') so paths
    stored in JSON are portable across machines.
    """
    if not source_path or not os.path.exists(source_path):
        return ""
    try:
        ext = os.path.splitext(source_path)[1].lower() or ".png"
        dest_filename = f"{username}_avatar{ext}"
        dest_path = os.path.join(AVATARS_DIR, dest_filename)

        img = Image.open(source_path)
        img = img.convert("RGB")  # JPEG-safe (no alpha channel issues)
        img.save(dest_path)

        return dest_filename          # ← relative filename, not full path
    except Exception as e:
        print(f"Error saving avatar: {e}")
        return ""
