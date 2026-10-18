# Add Seismic Radar to Blogger as a new blog

1. Go to blogger.com > **New Blog**. Title: `Seismic Radar`. Pick an address (e.g. `seismic-radar.blogspot.com`). Create it.
2. In the new blog: **Theme** > the arrow next to **Customize** > **Edit HTML**.
3. Select all the existing code (Ctrl+A), delete it, and paste the full contents of `seismic-radar-blogger-template.xml`.
4. Click **Save** (floppy icon), then **View blog**.

Notes
- The page is a single-page template: all stories live in the JSON block (`<script id="radar-data">`). To update, edit that block in Theme > Edit HTML: change `pulse.updated`, `pulse.headline`, `points`, `upcoming` and add new objects at the top of `items`.
- Blogger shows no posts on this page (a hidden Blog widget is kept because Blogger requires one). Don't remove it.
- The navbar is hidden by CSS. The preview image used for LinkedIn is the one already hosted on GitHub Pages.
- Set **Settings > Search description** with the text from the page description for better SEO.
- Paste the blog URL into the LinkedIn text before posting.
