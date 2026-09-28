# science-popularization-push

A Codex skill for producing evidence-based, image-rich science-popularization articles and WeChat-style long-form posts.

It covers:

- turning a brief and reference materials into a clear narrative structure;
- maintaining a claim ledger with place, year, scope, unit, and source;
- preventing fabricated people, dialogue, incidents, and unsupported local claims;
- planning image-text relationships, masks, captions, and source credits;
- assembling editable DOCX files and PDF proofs;
- validating bookmarks, clickable source links, media uniqueness, page count, and title propagation.

## Install in Codex

Install directly from this repository path:

```text
https://github.com/Aleravincence/science-popularization-push/tree/main/skills/science-popularization-push
```

In Codex, ask:

> Install the skill from this GitHub path: https://github.com/Aleravincence/science-popularization-push/tree/main/skills/science-popularization-push

## Manual install

Copy `skills/science-popularization-push` into:

- Windows: `C:\Users\<username>\.codex\skills\`
- macOS/Linux: `~/.codex/skills/`

The final structure must be:

```text
.codex/skills/science-popularization-push/
  SKILL.md
  agents/
  references/
  scripts/
```

Start a new Codex turn after installing so the skill is discovered.

## Use

Ask Codex:

> Use `science-popularization-push` to create a sourced, image-rich popular-science article from these materials.

The skill is intended for:

- science, ecology, nature, heritage, and technology communication;
- image-rich Word/PDF deliverables;
- WeChat-style long-form posts;
- revisions where factual traceability and visual consistency matter.

It is not intended for unsourced marketing copy or fictional storytelling.

## Script dependencies

The two helper scripts require:

```bash
pip install python-docx pypdfium2 Pillow
```

- `scripts/validate_docx_article.py` checks DOCX package integrity, source bookmarks, external links, media uniqueness, required/forbidden phrases, and optional PDF page count.
- `scripts/render_pdf_contact_sheet.py` renders PDF pages and creates a visual contact sheet.

## Repository layout

```text
.
|-- README.md
|-- .gitignore
`-- skills/
    `-- science-popularization-push/
        |-- SKILL.md
        |-- agents/
        |-- references/
        `-- scripts/
```
