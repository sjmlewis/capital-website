# Capital Industrial Participation — website

The public website of Capital Offset Services Limited, trading as Capital Industrial Participation.

- The pages in this folder (`index.html`, `platform.html`, …) are the live site, served by GitHub Pages.
- `tools/build.py` holds the wording and layout of every page and writes the pages out. To rebuild after a change:

```
python3 tools/build.py
```

Offset alerts (the Home page strip and panel, and `offset-alerts.html`) come from `tools/alerts.json`. To add the week's alerts, add items at the top with `added` set to today's date, change `updated` to today's date and rebuild. Each item needs a source link; internal monitor scores, suggested services and verdicts never go in this file.

`alerts.json` is the permanent record: never delete an item. The site shows only items added in the last three weeks (at least eight are always shown), so older alerts fall off the pages but stay in the file. The Home page shows the newest nine as cards and cycles the newest ten in the "Offset wire" strip under the header; the alerts page groups the items by the week they were added.

Styles live in `styles.css`; the small amount of script (menu, copy buttons, the drawing behind the navy bands) is in `site.js`.
