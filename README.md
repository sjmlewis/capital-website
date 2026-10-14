# Capital Industrial Participation — website

The public website of Capital Offset Services Limited, trading as Capital Industrial Participation.

- The pages in this folder (`index.html`, `platform.html`, …) are the live site, served by GitHub Pages.
- `tools/build.py` holds the wording and layout of every page and writes the pages out. To rebuild after a change:

```
python3 tools/build.py
```

Offset alerts (the Home page strip and panel, and `offset-alerts.html`) come from `tools/alerts.json`. They are a weekly round-up of new defence sales over each country's offset threshold. To add the week's alerts, add items at the top with `added` set to today's date, change `updated` to today's date and rebuild. Each item is a headline and one or two plain factual lines, with a short note on offset only where it is clear (for example, no offset because a purchase is SAFE-funded). Sources are not shown on the site and are not kept in this file: record them in the private "Website alerts: sources (private)" table at the end of the Offset Opportunity Monitor's Programme Register (a Claude Doc). From 19 October 2026 the Monday task "Offset Monitor – Monday email and website" adds each week's alerts and updates the private preview. Scheduled tasks cannot push to GitHub, so the master copy of `tools/alerts.json` is kept in the Claude project (`claude/website-src/tools-alerts.json`); before working on the site, copy that file over `tools/alerts.json` on `draft` if it is newer, rebuild and push to `draft` only. Internal monitor scores, suggested services and verdicts never go in this file.

`alerts.json` is the permanent record: never delete an item. The site shows only items added in the last three weeks (at least eight are always shown), so older alerts fall off the pages but stay in the file. The Home page shows the newest nine as cards and cycles the newest ten in the "Offset wire" strip under the header; the alerts page groups the items by the week they were added.

Styles live in `styles.css`; the small amount of script (menu, copy buttons, the drawing behind the navy bands) is in `site.js`.
