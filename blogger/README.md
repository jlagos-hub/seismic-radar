# Seismic Radar for Blogger

Files
- `seismic-radar-blogger.html`: the whole site as one self-contained fragment (scoped CSS, 36 pre-rendered stories, small filter script). No external files except Google Fonts.
- `linkedin-post.txt`: short LinkedIn text.
- Rebuild after editing the data in `index.html`: `python3 -I tools/build_blogger.py`

Add it to Blogger
1. blogger.com > **New blog** (name: Seismic Radar). Pick any theme; Contempo/Simple look cleanest.
2. **New post** (or **Pages > New page**), click the pencil icon > **HTML view**.
3. Paste the full contents of `seismic-radar-blogger.html`, give it a title, **Publish**.
4. Optional: Settings > Basic > set the post as the front page, or use a Page and make it your home link. For a full-width look, Theme > Customize > Layout, set the content width to the maximum.
5. Optional: Layout > Add a gadget > HTML/JavaScript and paste the same code to show it on every page.

Note: Blogger may restyle fonts and margins inside posts; all styles are scoped under `#sr` so the rest of the theme is unaffected.

## Review notes (offline)
- 36 stories, no duplicate URLs, all with date, type, region, source and URL.
- Links could not be checked live (sandbox blocks outbound access to the news sites). Open each once before announcing.
- `tgs.com/press-releases` (19 Aug, Mediterranean contract) points to the press-release index, not the article; replace with the direct link.
- `viridiengroup.com/fr/node/12506` (4 Aug) is a French internal node link; prefer the English newsroom URL.
- Data was last updated 24 Sep. "Dates to watch" hides past dates automatically; run the weekly update soon (African Energy Week starts 12 Oct, Viridien Q3 results 3 Nov).
