# Add Seismic Radar to Blogger as a new blog

1. Go to blogger.com > **Create blog** (title: Seismic Radar, pick an address), then open the new blog.
2. Open **Theme**, click the arrow next to **Customize**, then **Edit HTML**.
3. Select all the existing code (Ctrl+A), delete it, paste the full content of `seismic-radar-blogger-theme.xml`, click **Save** (the disk icon).
4. Open **View blog**. The page replaces the default blog layout.

Alternatively: **Theme > Backup / Restore > Upload** and choose `seismic-radar-blogger-theme.xml`.

## Updating the content
All news lives in one place: the line starting `var RADAR_DATA = {...};` near the bottom of the file (Theme > Edit HTML, Ctrl+F "RADAR_DATA"). Edit the `pulse` and `items` entries, then Save. The "Dates to watch" list hides dates that have already passed.

## Notes
- The Blogger theme is a standalone page; Blogger posts are not shown (the required Blog widget is hidden).
- Fonts load from Google Fonts. The source of truth stays `index.html` in this repo (GitHub Pages).
