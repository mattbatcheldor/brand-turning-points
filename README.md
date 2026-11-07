# Brand Turning Points

An editorial archive of campaigns that changed how people saw a brand, a product or themselves. The first edition opens with Sony BRAVIA’s *Balls* and covers 15 campaigns from 1959 to 2023.

[Read the brand and editorial guidelines](Brand_Turning_Points_Guidelines.html) for the visual identity, case structure, citation standards and film policy.

## Preview and publish

Open `index.html` in a browser. The archive and direct watch links work from a local file. To preview the in-page YouTube player, serve the folder over HTTP, for example with `python3 -m http.server 8000`.

For GitHub Pages, upload the package contents to the root of your repository and commit to `main`. In **Settings → Pages**, select **Deploy from a branch**, choose **main** and **/ (root)**, then save. GitHub Pages serves the committed `index.html` with no build step.

## Maintain an edition

- Edit `src/campaigns.json` to add or revise a case. Keep the original creative, the primary impact source and any further reading in their separate fields. Include a specific reason the work is memorable.
- Edit `src/page-template.html` for changes to the layout, typography or site copy. The screening selection lives in `src/build.py`. Use direct links for archival films and eligible official YouTube uploads for in-page viewing.
- Run `python3 src/build.py` to regenerate `index.html`. Preview the updated site and commit the source and output together. Recheck each new source link and any film playback.

The cover is an editorial illustration. Original advertisements and external video belong to their respective rights holders.
