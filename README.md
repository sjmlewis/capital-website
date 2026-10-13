# Capital Industrial Participation — website

The public website of Capital Offset Services Limited, trading as Capital Industrial Participation.

- The pages in this folder (`index.html`, `platform.html`, …) are the live site, served by GitHub Pages.
- `tools/build.py` holds the wording and layout of every page and writes the pages out. To rebuild after a change:

```
python3 tools/build.py
```

Offset alerts (the Home page panel and `offset-alerts.html`) come from `tools/alerts.json`. To add the week's alerts, add items there, change `updated` to today's date and rebuild. Each item needs a source link; internal monitor scores and verdicts never go in this file.

Styles live in `styles.css`; the small amount of script (menu, copy buttons, the drawing behind the navy bands) is in `site.js`.
