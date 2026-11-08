#!/usr/bin/env python3
"""Generate blogger/seismic-radar-blogger-theme.xml from index.html (single source of truth)."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "index.html").read_text(encoding="utf-8")

css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)
body = re.search(r"<body>\n(.*?)<script id=\"radar-data\"", src, re.S).group(1)
data = re.search(r'<script id="radar-data" type="application/json">(.*?)</script>', src, re.S).group(1)
code = re.search(r"</script>\n<script>\n(.*?)</script>\n</body>", src, re.S).group(1)
body = body.replace('aria-label="Search the news feed">', 'aria-label="Search the news feed"/>')
for part in (css, body, data, code):
    assert "]]>" not in part

theme = f'''<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE html>
<html b:version='2' class='v2' expr:dir='data:blog.languageDirection' xmlns='http://www.w3.org/1999/xhtml' xmlns:b='http://www.google.com/2005/gml/b' xmlns:data='http://www.google.com/2005/gml/data' xmlns:expr='http://www.google.com/2005/gml/expr'>
<head>
<meta charset="utf-8"/>
<meta content='width=device-width, initial-scale=1, viewport-fit=cover' name='viewport'/>
<title>Seismic Radar — marine seismic news &amp; market pulse</title>
<meta content="A curated feed of marine seismic contracts, results and conference takeaways, with a short market read." name="description"/>
<link expr:href='data:blog.canonicalHomepageUrl' rel='canonical'/>
<meta content="website" property="og:type"/>
<meta content="Seismic Radar" property="og:site_name"/>
<meta content="Seismic Radar — marine seismic news &amp; market pulse" property="og:title"/>
<meta content="Marine seismic contracts, results and conference takeaways in one place, with a short read on where offshore exploration is heading." property="og:description"/>
<meta expr:content='data:blog.canonicalHomepageUrl' property='og:url'/>
<!-- Keep the preview image hosted on GitHub Pages (or re-upload preview.jpg to Blogger and replace this URL) -->
<meta content="https://jlagos-hub.github.io/seismic-radar/preview.jpg" property="og:image"/>
<meta content="1568" property="og:image:width"/>
<meta content="652" property="og:image:height"/>
<meta content="summary_large_image" name="twitter:card"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&amp;family=Barlow:wght@400;500;600&amp;family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&amp;display=swap" rel="stylesheet"/>
<b:include data='blog' name='all-head-content'/>
<b:skin><![CDATA[/*
-----------------------------------------------
Blogger Template Style
Name:     Seismic Radar
Designer: Juan Manuel Lagos
----------------------------------------------- */
{css}
/* Hide Blogger chrome */
#navbar-iframe, .Navbar, .post-feeds, #hidden-blog-widget{{display:none !important}}
]]></b:skin>
</head>
<body>
{body}
<!-- Required by Blogger: a Blog widget must exist. Hidden; the page is rendered by the script below. -->
<div id='hidden-blog-widget' style='display:none'>
<b:section class='main' id='main' showaddelement='no'>
<b:widget id='Blog1' locked='true' title='Blog Posts' type='Blog' version='2'/>
</b:section>
</div>
<script id="radar-data" type="application/json"><![CDATA[{data}]]></script>
<script>//<![CDATA[
{code}//]]></script>
</body>
</html>
'''
out = root / "blogger" / "seismic-radar-blogger-theme.xml"
out.write_text(theme, encoding="utf-8")
print("wrote", out, len(theme), "bytes")
