# DOCX Layout, Image Masking, and Export

Use this reference when producing an illustrated Word article or a print-like PDF proof.

## Versioning and source assets

- Do not overwrite a validated master when the user asks for a new title, narrative, image set, or layout.
- Create a new output version and a parallel asset/build-script version when the change is substantial.
- Keep the previous DOCX/PDF as a fallback.
- Name files with the final article title plus a version qualifier such as `【数据与来源复核版】`.
- Keep generated images in a versioned folder. Reuse unchanged images by copying them, but re-render anything whose mask or text changes.

A practical pattern is:

```text
project/
  article-v5.docx
  article-v6.docx
  _overlay_assets_v5/
  _overlay_assets_v6/
  _build_article_v5.py
  _build_article_v6.py
  _layout_check/
    article-v6.pdf
    contact_article_v6.jpg
```

## Page and typography

- Set page size, margins, header distance, and footer distance explicitly.
- Use a restrained background color and sufficient contrast; do not place dark text over a visually busy photograph without a mask or scrim.
- Keep body text at a readable size. Do not solve crowding by shrinking captions or source notes into illegibility.
- Use a clear type hierarchy: cover title, standfirst, section title, body, caption, chart, source note.
- Long captions should add meaning, not duplicate the body sentence.
- Use first-page-different header/footer settings when the cover should remain clean.

## Image-text integration

For a cover or section opener:

- identify the visual anchor, such as an eye, face, hand, artifact, ridgeline, or habitat detail;
- place the text mask over low-information space;
- preserve the anchor with a feathered or bounded scrim;
- use a subtitle that explains the article's movement, not a generic slogan;
- check the final PDF at full resolution for text clipping and mask harshness.

For in-flow images:

- pair an establishing image with context, a close-up with mechanism, and a chart with change;
- use captions for source, date, and interpretation;
- avoid repeating the same image at different crops unless the repetition is deliberate;
- do not hide a subject's key feature under a panel.

## Internal bookmarks and external links

To make source markers clickable inside DOCX:

1. Create a bookmark around each source entry, for example `_Ref1` through `_Ref8`.
2. Create a hyperlink in the body with `w:anchor="ref1"` or the exact bookmark name.
3. Create the external URL as a normal external relationship on the source-list entry.
4. Verify both directions: no missing anchor and no body marker that points to a non-existent bookmark.

If the source list uses a URL host that is only an aggregator, include the original publisher in the entry. Do not put Chinese footnotes or descriptive text inside the URL itself.

## Export and visual proof

Preferred Windows path:

- use Word COM through PowerShell or a compatible automation layer to export a DOCX to PDF with `ExportAsFixedFormat(..., 17)`;
- keep Word hidden;
- close the document without saving and quit the application;
- if COM dependencies are unavailable, use an installed LibreOffice/PDF converter rather than treating a failed library import as a document failure.

Then render the PDF:

- create a page contact sheet for pagination and rhythm;
- inspect the cover, every overlay, every chart, and the source page at full size;
- check for blank pages, clipped captions, orphaned headings, duplicated images, and old title strings.

Run the skill's validator before and after the visual proof. The validator is mechanical; it does not replace reading the article against the sources.
