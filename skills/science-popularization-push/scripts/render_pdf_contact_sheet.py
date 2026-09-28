#!/usr/bin/env python3
"""Render a PDF into page PNGs plus a contact sheet for visual review."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import pypdfium2 as pdfium
    from PIL import Image, ImageDraw
except ImportError as exc:  # pragma: no cover - environment guidance
    raise SystemExit("pypdfium2 and Pillow are required in the active Python environment") from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--out", type=Path, help="contact-sheet JPEG path")
    parser.add_argument("--pages-dir", type=Path, help="directory for full-page PNG renders")
    parser.add_argument("--cols", type=int, default=5)
    parser.add_argument("--scale", type=float, default=2.0)
    parser.add_argument("--thumb-width", type=int, default=520)
    parser.add_argument("--thumb-height", type=int, default=740)
    parser.add_argument("--quality", type=int, default=92)
    args = parser.parse_args()

    if not args.pdf.exists():
        raise SystemExit(f"PDF not found: {args.pdf}")
    if args.cols < 1:
        raise SystemExit("--cols must be at least 1")

    stem = args.pdf.stem
    out = args.out or args.pdf.with_name(f"contact_{stem}.jpg")
    pages_dir = args.pages_dir or args.pdf.with_name(f"{stem}_pages")
    pages_dir.mkdir(parents=True, exist_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)

    pdf = pdfium.PdfDocument(str(args.pdf))
    thumbs = []
    for index in range(len(pdf)):
        page = pdf[index]
        image = page.render(scale=args.scale).to_pil().convert("RGB")
        page_path = pages_dir / f"page{index + 1:02d}.png"
        image.save(page_path)
        thumb = image.copy()
        thumb.thumbnail((args.thumb_width, args.thumb_height))
        thumbs.append((index + 1, thumb))

    cols = args.cols
    cell_width = args.thumb_width + 20
    cell_height = args.thumb_height + 60
    rows = (len(thumbs) + cols - 1) // cols
    contact = Image.new("RGB", (cols * cell_width, rows * cell_height), "white")
    draw = ImageDraw.Draw(contact)
    for idx, (number, image) in enumerate(thumbs):
        x = (idx % cols) * cell_width
        y = (idx // cols) * cell_height
        contact.paste(image, (x + (cell_width - image.width) // 2, y + 35))
        draw.text((x + 8, y + 8), f"page{number:02d}", fill="black")

    contact.save(out, quality=args.quality)
    print(f"PAGES {len(pdf)}")
    print(f"PAGE_RENDERS {pages_dir.resolve()}")
    print(f"CONTACT {out.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
