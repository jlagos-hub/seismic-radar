# Add Seismic Radar to Blogger as a new blog

1. blogger.com → **New blog** → give it the title "Seismic Radar" and an address → Create.
2. Left menu → **Theme** → arrow next to **Customize** → **Restore** → **Upload** → choose `seismic-radar-theme.xml`.
   (Or: Theme → **Edit HTML** → select all, delete, paste the whole file, Save.)
3. View the blog. The radar replaces the normal post list (posts are hidden on purpose; Blogger only requires one Blog widget).
4. Settings → Search description: paste the site description if wanted.

## Updating later
After each Seismic Radar update to `index.html`, run `python3 blogger/build.py` and re-upload the new XML.

## Notes
- The theme is generated from `index.html`; do not edit the XML by hand.
- Source links in the feed could not be checked from the build environment (outbound access blocked). Spot-check before announcing.
- Content last updated 2026-09-24; the "Dates to watch" list now shows only Viridien Q3 results (3 Nov). A refresh is due.
