# Brand Turning Points

An editorial archive of campaigns that changed how people saw a brand, a product or themselves.

- **Edition 01, Fame first** (the home page, also at `edition-01/`) opens with Sony BRAVIA’s *Balls* and covers 15 of the most famous campaigns, from 1959 to 2023. It finds that the most famous campaigns rarely prove they worked.
- **Edition 02, Proof first** (`edition-02/`) opens with BT’s *It’s Good to Talk* and covers 15 campaigns that can show they worked, from 1958 to 2019. Every case is an IPA Effectiveness Awards paper.
- **Edition 03, Data first** (`edition-03/`) opens with Spotify Wrapped and covers 15 campaigns where data was the idea, from 1975 to 2020. It finds that data used to aim the work proves itself, while data used as the show mostly proves attention.
- **Edition 04, Machine first** (`edition-04/`) opens with Cadbury’s *Shah Rukh Khan-My-Ad* and covers 15 campaigns made with machines or about them, from 1997 to 2025. It finds that machines working behind the scenes prove the most, while machines on screen mostly prove attention, and sometimes backlash.

## Series plan

The editions run in this fixed order. Keep the numbers and names exactly as listed.

| Edition | Name | Status |
| --- | --- | --- |
| 01 | Fame first | Published |
| 02 | Proof first | Published |
| 03 | Data first | Published |
| 04 | Machine first | Published |
| 05 | Failure first | Planned |
| 06 | Product first | Planned |

[Read the brand and editorial guidelines](Brand_Turning_Points_Guidelines.html) for the visual identity, case structure, citation standards and film policy.

## Preview and publish

Open `index.html` in a browser. The archive and direct watch links work from a local file. To preview the in-page YouTube player, serve the folder over HTTP, for example with `python3 -m http.server 8000`.

For GitHub Pages, upload the package contents to the root of your repository and commit to `main`. In **Settings → Pages**, select **Deploy from a branch**, choose **main** and **/ (root)**, then save. GitHub Pages serves the committed `index.html` with no build step.

## Maintain an edition

- Each edition has its own case file, numbered to match: `src/campaigns-01.json` for Edition 01 and `src/campaigns-02.json` for Edition 02. Keep the original creative, the primary impact source and any further reading in their separate fields, and include a specific reason the work is memorable.
- Give every case a `mechanism` (Demonstration, Reframed weakness, Participation, Exposing an assumption, Representation or Owning a moment), an `evidence_level` (Modelled effect, Sales trend, Survey, Reach only or Archival), a `stat_type` (`result`, or `legacy` for a date, award or production fact that is not an outcome) and a one-line `take` in the curator’s own voice. The finding ladder, mechanism map, timeline and filters are generated from these fields.
- Keep campaign thumbnails in `assets/` and record the original source and credit in the corresponding case’s `image` metadata. A case without an `image` shows a method tile in the list and a drawn frame in the screening room, so nothing is reused without a source.
- Edition 02 cases also carry a `method` (how the effect was measured) and a `credit` (the IPA record: year, award, agency and client). If no official copy of the work is online, leave `creative.url` empty and say so in `creative.label`.
- Shared layout, typography and behaviour live in `src/site.css` and `src/site.js`. Each edition’s copy lives in its own numbered template: `src/page-template-01.html` and `src/page-template-02.html`. Edition settings, including the screening-room films, are in `EDITIONS` in `src/build.py`. An edition that sorts cases by role (03 by data, 04 by machine) sets `data_role` and `data_source` on each case and names its roles and labels in the entry's `roles` setting. Use direct links for archival films and eligible official YouTube uploads for in-page viewing.
- Run `python3 src/build.py` to regenerate both editions, or `python3 src/build.py edition-02/index.html` for one. Preview the site and commit the source and output together. Recheck each new source link and any film playback.

## Add an edition

The series follows one naming pattern, so each new edition is a copy-and-number job.

1. Pick the next two-digit number, for example `03`, and a short edition name.
2. Add `src/campaigns-03.json` for the cases and `src/page-template-03.html` for the page copy. Copy the previous edition’s template as a starting point. Keep the masthead as “Brand Turning Points.” with “The campaign archive / Edition 03 / Name” in the line above it.
3. Add an entry to `EDITIONS` in `src/build.py` with `'number': '03'`, the name, the two file names and `'output': 'edition-03/index.html'`.
4. Run `python3 src/build.py`. The editions switcher in every edition’s menu picks up the new number.
5. Work on a branch called `edition-03-short-name` and commit it as “Add Edition 03: Name”.

Edition 01’s cover uses a still from the Sony BRAVIA *Balls* campaign. Edition 02’s and Edition 03’s covers are editorial illustrations. Original advertisements and external video belong to their respective rights holders.
