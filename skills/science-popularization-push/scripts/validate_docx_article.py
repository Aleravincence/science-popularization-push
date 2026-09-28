#!/usr/bin/env python3
"""Mechanical checks for an illustrated science-communication DOCX.

This verifies package integrity, source-anchor wiring, clickable external links,
media uniqueness, optional page count, and explicitly requested/forbidden phrases.
It does not verify whether a sentence is scientifically true; pair it with the
source-and-image audit reference and a manual read-through.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

try:
    from docx import Document
    from docx.oxml.ns import qn
except ImportError as exc:  # pragma: no cover - environment guidance
    raise SystemExit("python-docx is required: install python-docx in the active Python environment") from exc


def collect_text(doc):
    chunks = []
    for paragraph in doc.paragraphs:
        chunks.append(paragraph.text)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    chunks.append(paragraph.text)
    for section in doc.sections:
        for part in (section.header, section.footer):
            for paragraph in part.paragraphs:
                chunks.append(paragraph.text)
            for table in part.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            chunks.append(paragraph.text)
    return "\n".join(chunks)


def inspect_media(path):
    groups = defaultdict(list)
    with zipfile.ZipFile(path) as archive:
        bad_member = archive.testzip()
        for name in archive.namelist():
            if name.startswith("word/media/") and not name.endswith("/"):
                groups[hashlib.sha256(archive.read(name)).hexdigest()].append(name)
    return bad_member, groups


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--required-phrase", action="append", default=[])
    parser.add_argument("--forbidden-phrase", action="append", default=[])
    parser.add_argument("--bookmark-prefix", default="_Ref")
    parser.add_argument("--expect-images", type=int)
    parser.add_argument("--expect-pages", type=int)
    parser.add_argument("--json", action="store_true", help="print a machine-readable report")
    args = parser.parse_args()

    if not args.docx.exists():
        raise SystemExit(f"DOCX not found: {args.docx}")

    errors = []
    warnings = []
    report = {"docx": str(args.docx.resolve())}

    try:
        doc = Document(str(args.docx))
    except Exception as exc:
        raise SystemExit(f"cannot open DOCX: {exc}") from exc

    blob = collect_text(doc)
    report["text_characters"] = len(blob)
    report["inline_images"] = len(doc.inline_shapes)

    bookmarks = {
        node.get(qn("w:name"))
        for node in doc._element.xpath(".//w:bookmarkStart")
        if node.get(qn("w:name"))
    }
    anchors = [
        node.get(qn("w:anchor"))
        for node in doc._element.xpath(".//w:hyperlink")
        if node.get(qn("w:anchor"))
    ]
    missing_anchors = sorted(set(anchors) - bookmarks)
    if missing_anchors:
        errors.append(f"missing bookmark anchors: {missing_anchors}")

    external_targets = []
    bad_external_targets = []
    unicode_urls = []
    for rel in doc.part.rels.values():
        if not rel.is_external:
            continue
        target = rel.target_ref
        external_targets.append(target)
        if not target.startswith(("http://", "https://")):
            bad_external_targets.append(target)
        if any(ord(char) > 127 for char in target):
            unicode_urls.append(target)

    if bad_external_targets:
        errors.append(f"non-http external targets: {bad_external_targets}")
    if unicode_urls:
        warnings.append(f"external URLs contain non-ASCII characters: {unicode_urls}")

    try:
        bad_member, media_groups = inspect_media(args.docx)
    except zipfile.BadZipFile as exc:
        raise SystemExit(f"invalid DOCX ZIP package: {exc}") from exc

    if bad_member:
        errors.append(f"ZIP contains a corrupt member: {bad_member}")

    report.update(
        {
            "bookmarks": sorted(bookmarks),
            "source_bookmarks": sorted(x for x in bookmarks if x.startswith(args.bookmark_prefix)),
            "anchors": sorted(set(anchors)),
            "missing_anchors": missing_anchors,
            "external_link_count": len(external_targets),
            "bad_external_targets": bad_external_targets,
            "media_total": sum(len(v) for v in media_groups.values()),
            "media_unique": len(media_groups),
            "zip_bad_member": bad_member,
        }
    )

    if args.expect_images is not None:
        if report["inline_images"] != args.expect_images or report["media_total"] != args.expect_images:
            errors.append(
                f"expected {args.expect_images} images, found inline={report['inline_images']}, media={report['media_total']}"
            )

    for phrase in args.required_phrase:
        if phrase not in blob:
            errors.append(f"required phrase missing: {phrase!r}")

    for phrase in args.forbidden_phrase:
        if phrase in blob:
            errors.append(f"forbidden phrase present: {phrase!r}")

    if args.pdf:
        if not args.pdf.exists():
            errors.append(f"PDF not found: {args.pdf}")
        else:
            try:
                import pypdfium2 as pdfium
            except ImportError:
                warnings.append("pypdfium2 unavailable; PDF page count not checked")
            else:
                pdf = pdfium.PdfDocument(str(args.pdf))
                report["pdf_pages"] = len(pdf)
                if args.expect_pages is not None and len(pdf) != args.expect_pages:
                    errors.append(f"expected {args.expect_pages} PDF pages, found {len(pdf)}")

    report["errors"] = errors
    report["warnings"] = warnings
    report["status"] = "PASS" if not errors else "FAIL"

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"STATUS {report['status']}")
        print(f"DOCX {args.docx}")
        print(f"SOURCE_BOOKMARKS {report['source_bookmarks']}")
        print(f"MISSING_ANCHORS {report['missing_anchors']}")
        print(f"EXTERNAL_LINKS {report['external_link_count']}")
        print(f"BAD_EXTERNAL_TARGETS {report['bad_external_targets']}")
        print(f"IMAGES inline={report['inline_images']} media={report['media_total']} unique={report['media_unique']}")
        if "pdf_pages" in report:
            print(f"PDF_PAGES {report['pdf_pages']}")
        for warning in warnings:
            print(f"WARNING {warning}")
        for error in errors:
            print(f"ERROR {error}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
