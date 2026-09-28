# Source and Image Audit

Use this reference when the article contains statistics, policy claims, ecological outcomes, community transitions, historical dates, maps, or third-party images.

## Source hierarchy

Prefer sources in this order, while matching the source to the claim:

1. original law, policy, dataset, survey, or scientific report;
2. government, university, museum, protected-area, or institutional publication;
3. original reporting by an established newsroom or the original long-form source;
4. a republication or aggregator that reproduces the original;
5. social posts or unattributed summaries.

If only an aggregator is available, identify the original publisher and the host separately. Do not cite a search-result snippet as if it were the underlying document.

## Claim ledger

Use one row per claim or chart value:

```text
claim | exact value | unit | place/scope | year/period | source | page/URL | use | confidence | notes
```

Examples of scope traps:

- a figure for a proposed national park is not automatically a figure for one township;
- a provincial program's job count is not proof that every local community received those jobs;
- a media estimate and a report estimate may use different years or definitions;
- “candidate area,” “pilot,” and “formally established” are different statuses;
- a species count from an artificial breeding facility is not the same as a wild population count.

## Numbers, dates, and status

Before retaining a number, confirm:

- the exact number and unit;
- whether it is a count, percentage, value, rate, or ratio;
- the year and reporting period;
- the geographic or institutional boundary;
- the denominator or baseline;
- whether it is actual, planned, estimated, or forecast;
- whether the source says “about,” “more than,” or an exact value;
- whether another authoritative source conflicts.

If two sources conflict, choose one for the article only with a stated rationale, or present both with their definitions. Do not average them or silently substitute the more dramatic one.

## Local-transfer test

When a source describes a different protected area, town, school, or project, do not apply its conclusion locally unless there is local corroboration. Rephrase the reference as context if needed:

- “A provincial program proposed …”
- “The same model has been reported in another protected area …”
- “This is a direction for future replication, not a documented local outcome.”

## Source-marker design

A robust article has two link layers:

1. **in-text marker -> internal bookmark**. “来源③” or a bracketed marker jumps to the source list inside the document.
2. **source-list entry -> external URL**. The original report, policy, dataset, or article opens in the browser.

If the user cannot click an internal marker, verify that the DOCX contains a `w:bookmarkStart`/`w:bookmarkEnd` pair and that the body hyperlink uses `w:anchor` matching the bookmark name. A visual number alone is not a link.

## Image audit

For every photograph, illustration, map, screenshot, or manipulated visual, record:

| field | requirement |
|---|---|
| content | what is actually visible |
| creator | photographer, illustrator, agency, or institution |
| publisher | government site, journal, news outlet, museum, etc. |
| date | publication or capture date if available |
| URL | original or authoritative host |
| permission | confirmed, public-interest use assumed, or unresolved |
| match | paragraph, chart, or claim it supports |
| uniqueness | whether near-duplicate crops are reused |

Avoid:

- an image that shows one species, place, or period while the text claims another;
- a personal name with no publisher or source trail;
- repeated near-identical crops that make the layout feel padded;
- a mask that covers the image's informational highlight;
- an AI-generated image presented as documentary evidence.

When images come from media or third-party libraries, state the credit and warn that external publication may require a separate license. If the image is supplied by the user, do not invent its source; mark the credit as unverified until confirmed.

## Final source audit

- Read the article from start to finish with the claim ledger beside it.
- Follow every marker to the matching source entry.
- Open every external URL and confirm that the host, title, date, and scope match the sentence it supports.
- Recheck the title, standfirst, chart labels, captions, and footer for old versions.
- Separate direct evidence, contextual comparison, and author outlook.
