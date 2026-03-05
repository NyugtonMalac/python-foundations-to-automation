# DM Image Converter

A lightweight Python automation tool for converting PNG/JPG images to WEBP with resizing, watermarking and folder watching.

Designed for small automation workflows such as:

- blog image preparation
- flashcard image datasets
- automatic image pipelines

---

# Features

✔ PNG / JPG / JPEG support  
✔ Resize while keeping aspect ratio  
✔ Convert to WEBP  
✔ Optional watermark (PNG with transparency)  
✔ Archive or delete original images  
✔ Folder watch mode (automatic conversion)

---

# Installation

Clone the repository:
git clone https://github.com/yourname/DM_image_converter.git

cd DM_image_converter

Create virtual environment:
python -m venv .venv

Activate environment:

Windows
.venv\Scripts\activate


Install dependencies
pip install -r requirements.txt


---

# Basic usage

Convert images in a folder:
python tools/dm_image_converter.py
--in dm_png_to_convert
--out dm_webp_pics
--width 450


---

# Watch mode (automatic conversion)
python tools/dm_image_converter.py
--in dm_png_to_convert
--out dm_webp_pics
--width 450
--quality 85
--watch


The script will automatically convert new images appearing in the folder.

Stop watching with:
Ctrl + C


---

# Watermark example
python tools/dm_image_converter.py
--in dm_png_to_convert
--out dm_webp_pics
--width 450
--watermark assets/watermark_dm.png


Options:
--wm-size
--wm-opacity
--wm-margin


---

# Archive original files

Instead of deleting original images:
--archive dm_done


---

# Example workflow
dm_png_to_convert
↓
resize
↓
watermark
↓
webp
↓
dm_webp_pics
↓
archive original



---

# Requirements

Python 3.9+

Libraries:

- Pillow
- watchdog

Install with:
pip install -r requirements.txt


---

# License

MIT

---

# Author

DataMagic  
Automation tools for learning, data and productivity.