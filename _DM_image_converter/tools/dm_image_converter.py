"""
DM Image Converter
==================

A lightweight Python tool for converting PNG/JPG images to WEBP with optional:

• resizing
• watermarking
• archive or deletion of original files
• automatic folder watching (real-time processing)

Typical workflow
----------------

input folder
    ↓
image detected
    ↓
resize (optional)
    ↓
apply watermark (optional)
    ↓
convert to WEBP
    ↓
archive original

Features
--------

- Supports PNG, JPG, JPEG
- Keeps aspect ratio when resizing
- Optional watermark (PNG with transparency)
- Automatic folder watcher using watchdog
- Archive or delete original files after conversion
- Designed for automation pipelines

Example use cases
-----------------

Flashcard images
    Resize to fixed width (e.g. 450px) and convert to WEBP.

Blog images
    Resize smaller (e.g. 250px) and watermark automatically.

Automation
    Run in watch mode to automatically process new images
    arriving in a folder.

Example commands
----------------

Basic conversion

    python tools/dm_image_converter.py \
        --in dm_png_to_convert \
        --out dm_webp_pics \
        --width 450

Watch mode with watermark and archive

    python tools/dm_image_converter.py \
        --in dm_png_to_convert \
        --out dm_webp_pics \
        --width 450 \
        --quality 85 \
        --archive dm_done \
        --watch \
        --watermark assets/watermark_dm.png

Author
------

DataMagic – Automation tools for learning and data workflows
"""



from __future__ import annotations

import argparse
import time
from pathlib import Path
import shutil

from PIL import Image, ImageOps

# Optional watcher (only if you use --watch)
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except Exception:
    WATCHDOG_AVAILABLE = False


SUPPORTED_EXTS = {".png", ".jpg", ".jpeg"}


def is_image(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in SUPPORTED_EXTS


def compute_resize(
    img: Image.Image,
    width: int | None,
    height: int | None,
    max_side: int | None
) -> tuple[int, int]:
    """Return target (w, h) keeping aspect ratio.

    Priority:
      - If width provided -> scale by width
      - Else if height provided -> scale by height
      - Else if max_side provided -> scale so max(w,h) == max_side
      - Else -> keep original
    """
    w, h = img.size

    if width and width > 0:
        new_w = width
        new_h = int(round(h * (new_w / w)))
        return new_w, max(1, new_h)

    if height and height > 0:
        new_h = height
        new_w = int(round(w * (new_h / h)))
        return max(1, new_w), new_h

    if max_side and max_side > 0:
        scale = max_side / max(w, h)
        if scale >= 1:
            return w, h  # don't upscale by default
        return max(1, int(round(w * scale))), max(1, int(round(h * scale)))

    return w, h


def apply_watermark(
    base_img: Image.Image,
    watermark_path: Path,
    wm_size: int,
    wm_opacity: float,
    wm_margin: int,
) -> Image.Image:
    """Apply a bottom-right watermark to base_img and return a new image."""
    if not watermark_path or not watermark_path.exists():
        return base_img

    # Work in RGBA for alpha compositing
    if base_img.mode != "RGBA":
        base = base_img.convert("RGBA")
    else:
        base = base_img.copy()

    with Image.open(watermark_path) as wm:
        wm = wm.convert("RGBA")

        # Resize watermark to square wm_size x wm_size (keeps sharpness)
        wm = wm.resize((wm_size, wm_size), Image.Resampling.LANCZOS)

        # Apply opacity (0..1)
        wm_opacity = max(0.0, min(1.0, wm_opacity))
        if wm_opacity < 1.0:
            alpha = wm.getchannel("A")
            alpha = alpha.point(lambda a: int(a * wm_opacity))
            wm.putalpha(alpha)

        # Position: bottom-right with margin
        bw, bh = base.size
        ww, wh = wm.size
        x = max(0, bw - ww - wm_margin)
        y = max(0, bh - wh - wm_margin)

        base.alpha_composite(wm, (x, y))

    return base


def convert_one(
    in_path: Path,
    out_dir: Path,
    width: int | None,
    height: int | None,
    max_side: int | None,
    quality: int,
    overwrite: bool,
    delete_source: bool,
    archive_dir: Path | None,
    watermark_path: Path | None,
    wm_size: int,
    wm_opacity: float,
    wm_margin: int,
) -> Path | None:
    """Convert one image to WEBP with optional resize + optional watermark."""
    if not is_image(in_path):
        return None

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / (in_path.stem + ".webp")

    if out_path.exists() and not overwrite:
        print(f"⏭️  Skip (exists): {out_path.name}")
        return out_path

    try:
        with Image.open(in_path) as img:
            # iPhone JPEG-eknél fontos: EXIF orientation helyesre forgatás
            img = ImageOps.exif_transpose(img)

            # Resize
            target_w, target_h = compute_resize(img, width, height, max_side)
            if (target_w, target_h) != img.size:
                img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)

            # Watermark (optional)
            if watermark_path:
                img = apply_watermark(img, watermark_path, wm_size, wm_opacity, wm_margin)

            # WEBP-hez RGB/RGBA jó
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")

            # Save WEBP
            quality = int(quality)
            quality = max(1, min(100, quality))
            img.save(out_path, "WEBP", quality=quality, method=6)

        # After successful save:
        if archive_dir:
            archive_dir.mkdir(parents=True, exist_ok=True)
            target = archive_dir / in_path.name
            shutil.move(str(in_path), str(target))
        elif delete_source:
            in_path.unlink(missing_ok=True)

        print(f"✅ {in_path.name}  →  {out_path.name}  ({target_w}x{target_h}, q={quality})")
        return out_path

    except Exception as e:
        print(f"❌ Error converting {in_path.name}: {e}")
        return None


def convert_folder(
    in_dir: Path,
    out_dir: Path,
    width: int | None,
    height: int | None,
    max_side: int | None,
    quality: int,
    overwrite: bool,
    delete_source: bool,
    archive_dir: Path | None,
    watermark_path: Path | None,
    wm_size: int,
    wm_opacity: float,
    wm_margin: int,
) -> None:
    in_dir = in_dir.resolve()
    out_dir = out_dir.resolve()

    if not in_dir.exists():
        raise FileNotFoundError(f"Input folder not found: {in_dir}")

    files = [p for p in in_dir.iterdir() if is_image(p)]
    if not files:
        print("ℹ️  No PNG/JPG images found.")
        return

    print(f"📦 Found {len(files)} image(s) in: {in_dir}")
    for p in files:
        convert_one(
            p, out_dir,
            width, height, max_side,
            quality, overwrite,
            delete_source, archive_dir,
            watermark_path, wm_size, wm_opacity, wm_margin
        )


# ------------------ WATCH MODE ------------------

class NewFileHandler(FileSystemEventHandler):
    def __init__(
        self,
        out_dir: Path,
        width: int | None,
        height: int | None,
        max_side: int | None,
        quality: int,
        overwrite: bool,
        delete_source: bool,
        archive_dir: Path | None,
        watermark_path: Path | None,
        wm_size: int,
        wm_opacity: float,
        wm_margin: int,
    ):
        self.out_dir = out_dir
        self.width = width
        self.height = height
        self.max_side = max_side
        self.quality = quality
        self.overwrite = overwrite
        self.delete_source = delete_source
        self.archive_dir = archive_dir
        self.watermark_path = watermark_path
        self.wm_size = wm_size
        self.wm_opacity = wm_opacity
        self.wm_margin = wm_margin

    def on_created(self, event):
        if event.is_directory:
            return

        path = Path(event.src_path)

        # várunk kicsit, hogy az email/letöltés “befejezze” az írást
        time.sleep(0.8)

        if is_image(path):
            convert_one(
                path, self.out_dir,
                self.width, self.height, self.max_side,
                self.quality, self.overwrite,
                self.delete_source, self.archive_dir,
                self.watermark_path, self.wm_size, self.wm_opacity, self.wm_margin
            )


def watch_folder(
    in_dir: Path,
    out_dir: Path,
    width: int | None,
    height: int | None,
    max_side: int | None,
    quality: int,
    overwrite: bool,
    delete_source: bool,
    archive_dir: Path | None,
    watermark_path: Path | None,
    wm_size: int,
    wm_opacity: float,
    wm_margin: int,
) -> None:
    if not WATCHDOG_AVAILABLE:
        raise RuntimeError("watchdog is not installed. Run: pip install watchdog")

    in_dir = in_dir.resolve()
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    handler = NewFileHandler(
        out_dir,
        width, height, max_side,
        quality, overwrite,
        delete_source, archive_dir,
        watermark_path, wm_size, wm_opacity, wm_margin
    )
    observer = Observer()
    observer.schedule(handler, str(in_dir), recursive=False)

    print(f"👀 Watching: {in_dir}")
    print(f"➡️  Output:   {out_dir}")
    if archive_dir:
        print(f"🗄️  Archive:  {archive_dir.resolve()}")
    elif delete_source:
        print("🧹 Delete source: ON")
    if watermark_path:
        print(f"💧 Watermark: {watermark_path.resolve()} (size={wm_size}, opacity={wm_opacity}, margin={wm_margin})")
    print("Press Ctrl+C to stop.")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    parser = argparse.ArgumentParser(
        description="DM image converter: PNG/JPG -> WEBP with optional resize + watch mode + watermark."
    )
    parser.add_argument("--in", dest="in_dir", required=True, help="Input folder (png/jpg/jpeg)")
    parser.add_argument("--out", dest="out_dir", required=True, help="Output folder (webp)")
    parser.add_argument("--width", type=int, default=None, help="Resize by width (keeps aspect)")
    parser.add_argument("--height", type=int, default=None, help="Resize by height (keeps aspect)")
    parser.add_argument("--max-side", type=int, default=None, help="Resize so max(w,h)=max-side (no upscale)")
    parser.add_argument("--quality", type=int, default=82, help="WEBP quality 1-100 (default 82)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing .webp files")
    parser.add_argument("--watch", action="store_true", help="Watch input folder and auto-convert new files")

    parser.add_argument("--delete-source", action="store_true", help="Delete source file after successful convert")
    parser.add_argument("--archive", type=str, default=None, help="Move source files to this folder after convert (safer than delete)")

    # Watermark options
    parser.add_argument("--watermark", type=str, default=None, help="Path to watermark PNG (with transparency)")
    parser.add_argument("--wm-size", type=int, default=48, help="Watermark size (square px). Default 48")
    parser.add_argument("--wm-opacity", type=float, default=0.28, help="Watermark opacity 0..1. Default 0.28")
    parser.add_argument("--wm-margin", type=int, default=12, help="Watermark margin from edge (px). Default 12")

    args = parser.parse_args()

    in_dir = Path(args.in_dir)
    out_dir = Path(args.out_dir)

    archive_dir = Path(args.archive) if args.archive else None
    watermark_path = Path(args.watermark) if args.watermark else None

    # Safety: if archive is set, we ignore delete_source (archive is safer)
    delete_source = bool(args.delete_source) and (archive_dir is None)

    if args.watch:
        watch_folder(
            in_dir, out_dir,
            args.width, args.height, args.max_side,
            args.quality, args.overwrite,
            delete_source, archive_dir,
            watermark_path, args.wm_size, args.wm_opacity, args.wm_margin
        )
    else:
        convert_folder(
            in_dir, out_dir,
            args.width, args.height, args.max_side,
            args.quality, args.overwrite,
            delete_source, archive_dir,
            watermark_path, args.wm_size, args.wm_opacity, args.wm_margin
        )


if __name__ == "__main__":
    main()