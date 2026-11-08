# Add Seismic Radar to Blogger as a new blog

1. blogger.com → **New blog** → enter title "Seismic Radar" and an address → Create.
2. Open the new blog → **Theme** → click the arrow next to **Customize** → **Edit HTML**.
3. Select all existing code (Ctrl+A), delete it, and paste the full contents of
   `seismic-radar-blogger-theme.xml`. Click **Save**.
4. Open the blog URL. The Seismic Radar page replaces the default layout.
5. Optional: Settings → Basic → set a custom domain; Settings → Search preferences → add a meta description.

## Updating content later
All news lives in the JSON block `<script id="radar-data">` near the bottom of the template.
Edit `index.html` in the repo, then run `python3 blogger/build_blogger.py` to regenerate the XML
and paste it again (Theme → Edit HTML).

## Notes
- The page is a single "home" layout; Blogger posts are hidden. Add a post-based layout if you want normal blogging later.
- The "Dates to watch" list hides past dates automatically. The last content update is 24 Sep 2026, so
  only 2026-11-03 or later items would show; refresh the data before launch.
- og:image points at the GitHub Pages copy of preview.jpg; keep that repo public or upload the image to Blogger and swap the URL.
