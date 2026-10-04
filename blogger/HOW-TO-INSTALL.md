# Add Seismic Radar to Blogger as a new blog

1. Go to https://www.blogger.com and click **New Blog**. Pick a title (e.g. "Seismic Radar") and an address (e.g. `seismic-radar.blogspot.com`), and choose any starter theme.
2. Open **Theme**. Click the arrow next to **Customize** and choose **Edit HTML**.
3. Click inside the editor, press Ctrl+A to select everything, and delete it.
4. Open `seismic-radar-blogger-theme.xml`, copy the whole file and paste it into the editor.
5. Click **Save** (the disk icon), then **View blog**.

Alternative: **Theme > Backup/Restore > Upload** accepts this same `.xml` file.

## Updating the content later
All content (market pulse, dates to watch, news items) is the `RADAR_DATA` object inside the `<script>` block. Edit that JSON and save the theme; no posts are needed.

## Notes
- The site is a single static page, so Blogger posts are not displayed. The Blog widget is kept hidden because Blogger requires one.
- The "Dates to watch" list hides past dates automatically.
- Fonts load from Google Fonts. Dark mode follows the visitor's system setting.
