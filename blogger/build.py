#!/usr/bin/env python3
"""Build a Blogger theme (blogger/seismic-radar-theme.xml) from ../index.html.
Re-run after every Seismic Radar update:  python3 blogger/build.py"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "index.html").read_text(encoding="utf-8")

css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
data = re.search(r'<script id="radar-data" type="application/json">(.*?)</script>', src, re.S).group(1).strip()
body = re.search(r"<body>(.*?)<script id=\"radar-data\"", src, re.S).group(1)
js = re.search(r"</script>\s*<script>(.*?)</script>\s*</body>", src, re.S).group(1)

# Data becomes a plain JS variable (no JSON.parse of a DOM node, safe inside CDATA)
js = js.replace("JSON.parse(document.getElementById('radar-data').textContent)", "window.RADAR_DATA")
assert "RADAR_DATA" in js
# XHTML-style void tags for Blogger's XML parser
body = re.sub(r"<input([^>]*?)\s*/?>", r"<input\1/>", body)
assert "]]>" not in css + data + js

theme = f"""<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE html>
<html b:version='2' class='v2' expr:dir='data:blog.languageDirection' xmlns='http://www.w3.org/1999/xhtml' xmlns:b='http://www.google.com/2005/gml/b' xmlns:data='http://www.google.com/2005/gml/data' xmlns:expr='http://www.google.com/2005/gml/expr'>
<head>
<meta content='width=device-width, initial-scale=1, viewport-fit=cover' name='viewport'/>
<meta content='A curated feed of marine seismic contracts, results and conference takeaways, with a short market read.' name='description'/>
<b:include data='blog' name='all-head-content'/>
<title><data:blog.pageTitle/></title>
<link href='https://fonts.googleapis.com' rel='preconnect'/>
<link crossorigin='anonymous' href='https://fonts.gstatic.com' rel='preconnect'/>
<link href='https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&amp;family=Barlow:wght@400;500;600&amp;family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&amp;display=swap' rel='stylesheet'/>
<b:skin><![CDATA[/* Seismic Radar - Blogger theme (generated from index.html by blogger/build.py) */
{css}
]]></b:skin>
</head>
<body>
{body}
<!-- Blogger needs one Blog widget in the template; posts are kept out of view because the page is the radar itself. -->
<div style='display:none'>
<b:section class='main' id='main' showaddelement='no'>
<b:widget id='Blog1' locked='true' title='Blog Posts' type='Blog' version='2'/>
</b:section>
</div>
<script>
//<![CDATA[
window.RADAR_DATA = {data};
{js}
//]]>
</script>
</body>
</html>
"""
out = root / "blogger" / "seismic-radar-theme.xml"
out.write_text(theme, encoding="utf-8")
print("wrote", out, len(theme), "bytes")
