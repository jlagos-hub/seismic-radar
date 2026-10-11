#!/usr/bin/env python3
"""Build blogger/seismic-radar-blogger.html from the JSON data embedded in index.html.
Usage: python3 -I tools/build_blogger.py
Output is a self-contained fragment (scoped CSS + pre-rendered stories + small JS filter)
to paste into Blogger: New post > HTML view (or a Page, or a Layout HTML/JavaScript gadget)."""
import re, json, html, datetime, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
src = (root/'index.html').read_text(encoding='utf-8')
D = json.loads(re.search(r'<script id="radar-data" type="application/json">(.*?)</script>', src, re.S).group(1))
css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
TYPES = {'contract':'Contracts','market':'Results &amp; market','conference':'Conferences','technology':'Technology','policy':'Licensing &amp; policy'}
REGIONS = ['North Sea','Latin America','Africa & Middle East','Asia-Pacific','Global']
e = lambda s: html.escape(str(s), quote=True)
dt = lambda s: datetime.date.fromisoformat(s)

# scope the stylesheet under #sr so it cannot fight the Blogger theme
css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
css = re.sub(r'@media \(prefers-color-scheme: dark\)\{.*?\n\}\n', '', css, flags=re.S)
css = re.sub(r':root\[data-theme="dark"\]\{.*?\}', '', css, flags=re.S)
css = re.sub(r'\n:root\{', '\n#sr{', css, count=1)
css = css.replace('box-sizing:border-box;\n  padding-top:env(safe-area-inset-top,0px); padding-bottom:env(safe-area-inset-bottom,0px);', 'box-sizing:border-box; background:var(--bg); color:var(--ink); font-family:"Barlow",system-ui,sans-serif; font-size:16px; line-height:1.5;')
out=[]
for rule in re.findall(r'([^{}]+)\{([^{}]*)\}|(@keyframes[^{]+\{(?:[^{}]*\{[^{}]*\})+\})|(@media[^{]+\{(?:[^{}]*\{[^{}]*\})+\})', css):
    pass
def scope(m):
    sel, body = m.group(1), m.group(2)
    if sel.strip().startswith('#sr{') or sel.strip()=='#sr': return m.group(0)
    sels=[]
    for s in sel.split(','):
        s=s.strip()
        if not s: continue
        if s in ('html','body',':root'): s='#sr'
        elif s.startswith('*'): s='#sr '+s if s!='*,*::before,*::after' else '#sr,#sr *,#sr *::before,#sr *::after'
        elif s.startswith('@') or s.startswith('from') or s.startswith('to'): return m.group(0)
        else: s='#sr '+s
        sels.append(s)
    return ','.join(sels)+'{'+body+'}'
# handle simple top-level rules; keep @keyframes/@media blocks scoped by hand
blocks = re.split(r'(?<=\})\s*(?=[^\s])', css.strip())
res=[]
for b in blocks:
    b=b.strip()
    if not b: continue
    if b.startswith('@keyframes'): res.append(b); continue
    if b.startswith('@media'):
        head, inner = b.split('{',1); inner=inner.rsplit('}',1)[0]
        inner=re.sub(r'([^{}]+)\{([^{}]*)\}', scope, inner)
        res.append(head+'{'+inner+'}'); continue
    res.append(re.sub(r'([^{}]+)\{([^{}]*)\}', scope, b, count=1))
css='\n'.join(res)
css = css.replace('{.pulse-grid{','{#sr .pulse-grid{').replace('{.section-svg .draw{','{#sr .section-svg .draw{')
css += """
#sr{max-width:1120px;margin:0 auto;border-radius:6px;overflow:hidden}
#sr .title{font-size:clamp(44px,9vw,104px)}
#sr h1,#sr h2,#sr h3{font-family:inherit}
#sr .upcoming li[hidden]{display:none}
#sr a{color:inherit}
@media (prefers-color-scheme: dark){#sr{--bg:#0F1A23;--surface:#15232E;--ink:#E4EBEC;--muted:#9AAAB3;--rule:#2A3B47;--buoy:#F07A45;--buoy-soft:#3A2419;--sea:#7DB9BF;--sea-soft:#1B3238;--trace:#C9D6DA}}
"""

import math
def section_svg():
    W,H,n=1400,170,70; step=W/n; seed=[7]
    def rnd():
        seed[0]=(seed[0]*9301+49297)%233280; return seed[0]/233280
    out=''; hz=[]
    for i in range(n):
        x0=i*step+step/2; pts=[]; fills=[]
        hy=96+22*math.sin(i/9)+8*math.sin(i/3.3); hz.append((x0,hy))
        for y in range(0,H+1,3):
            a=math.sin(y/7+i*.35)*2.2+(rnd()-.5)*1.4
            a+=9*math.exp(-(y-hy)**2/40); a+=5*math.exp(-(y-(hy-38))**2/30)*math.sin(i/5)
            pts.append((x0+a,y)); fills.append((x0+a,y) if a>0 else (x0,y))
        j=lambda L:'L'.join(f'{x:.1f} {y}' for x,y in L)
        out+=f'<path class="wig" d="M{j(pts)}"/><path class="fill" d="M{x0:.1f} 0L{j(fills)}L{x0:.1f} {H}Z"/>'
    out+='<path class="horizon draw" d="M'+'L'.join(f'{x:.1f} {y:.1f}' for x,y in hz)+'"/>'
    return f'<svg class="section-svg" viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true">{out}</svg>'
P = D['pulse']
items = sorted(D['items'], key=lambda i: i['date'], reverse=True)
pts = ''.join(f'<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>' for a,b in P['points'])
up = ''.join(f'<li data-date="{e(a)}"><div class="when">{dt(a).day} {dt(a):%b}</div><div class="what">{e(b)}</div><div class="where">{e(c)}</div></li>' for a,b,c in P['upcoming'])
rows=[]; month=''
for i in items:
    d=dt(i['date']); m=f'{d:%B %Y}'
    if m!=month: month=m; rows.append(f'<h3 class="month">{m}</h3>')
    label = i['event'] if i['type']=='conference' and i.get('event') else TYPES[i['type']]
    hay = e((i['title']+' '+i['summary']+' '+' '.join(i['companies'])+' '+i['region']+' '+i['source']+' '+(i.get('event') or '')).lower())
    rows.append(f'<article class="item" data-region="{e(i["region"])}" data-type="{i["type"]}" data-hay="{hay}"><div class="day">{d.day}<small>{d:%b %Y}</small></div><div><div class="tags"><span class="tag t-{i["type"]}">{label if i["type"]!="conference" or not i.get("event") else e(label)}</span><span class="tag">{e(i["region"])}</span><span class="tag plain">{e(", ".join(i["companies"]))}</span></div><h3><a href="{e(i["url"])}" target="_blank" rel="noopener">{e(i["title"])}</a></h3><p>{e(i["summary"])}</p><div class="src">Source: <a href="{e(i["url"])}" target="_blank" rel="noopener">{e(i["source"])}</a></div></div></article>')
chips = lambda key,vals,lab: ''.join(f'<button class="chip" type="button" data-{key}="{e(v)}" aria-pressed="false">{lab(v)}</button>' for v in vals)
upd = dt(P['updated'])
page = f'''<!-- Seismic Radar for Blogger. Paste in: New post > HTML view. Source: https://jlagos-hub.github.io/seismic-radar/ -->
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&amp;family=Barlow:wght@400;500;600&amp;family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&amp;display=swap" rel="stylesheet">
<style>
{css}
</style>
<div id="sr">
<header class="hero"><div class="wrap">
<h1 class="title">Seismic Radar</h1>
<p class="lede">Marine seismic contracts, results and conference takeaways in one place, with a short read on where exploration is heading.</p>
<div class="meta"><span>Updated <strong>{upd.day} {upd:%B %Y}</strong></span><span>{len(items)} stories tracked since {dt(items[-1]["date"]):%B}</span></div>
</div>{section_svg()}</header>
<section class="pulse"><div class="wrap pulse-grid">
<div><h2 class="h2">Market pulse</h2><p class="read">{e(P["headline"])}</p><p class="read-sub">{e(P["summary"])}</p><dl class="points">{pts}</dl></div>
<div class="upcoming"><h2 class="h2">Dates to watch</h2><p class="small">Conferences and reporting dates that move the market read.</p><ol id="sr-up">{up}</ol></div>
</div></section>
<main class="feed wrap">
<div class="feed-head"><div><h2 class="h2">News feed</h2><p class="small">Newest first. Each summary links to the original article.</p></div><span class="count" id="sr-count" aria-live="polite">{len(items)} stories</span></div>
<div class="tools"><input class="search" id="sr-q" type="search" placeholder="Search company, basin or vessel" aria-label="Search the news feed">
<div class="chips" id="sr-reg"><span class="chip-label">Region</span>{chips("region",REGIONS,e)}</div>
<div class="chips" id="sr-typ"><span class="chip-label">Type</span>{chips("type",TYPES,lambda k: TYPES[k])}</div></div>
<div id="sr-list">{"".join(rows)}</div>
<p class="empty" id="sr-empty" hidden>No stories match these filters.</p>
</main>
<footer><div class="wrap"><p>Curated by <strong>Juan Manuel Lagos</strong>, Master Mariner and offshore QC/HSE client representative on marine seismic campaigns.</p><p>Summaries are written from public company releases and trade press; follow each link for the full story. The market pulse is an editorial reading of those sources, not investment advice.</p></div></footer>
</div>
<script>
(function(){{
var s={{q:'',region:null,type:null}},root=document.getElementById('sr'),items=[].slice.call(root.querySelectorAll('.item'));
var t=new Date();t.setHours(0,0,0,0);
[].forEach.call(root.querySelectorAll('#sr-up li'),function(li){{if(new Date(li.getAttribute('data-date')+'T00:00:00')<t)li.hidden=true;}});
function render(){{var n=0,m=null;
items.forEach(function(a){{var ok=(!s.region||a.getAttribute('data-region')===s.region)&&(!s.type||a.getAttribute('data-type')===s.type)&&(!s.q||a.getAttribute('data-hay').indexOf(s.q)>-1);a.hidden=!ok;if(ok)n++;}});
[].forEach.call(root.querySelectorAll('.month'),function(h){{var x=h.nextElementSibling,any=false;while(x&&x.classList.contains('item')){{if(!x.hidden)any=true;x=x.nextElementSibling;}}h.hidden=!any;}});
document.getElementById('sr-count').textContent=n+(n===1?' story':' stories');document.getElementById('sr-empty').hidden=n>0;}}
function wire(id,key){{var box=document.getElementById(id);box.addEventListener('click',function(ev){{var b=ev.target.closest('.chip');if(!b)return;var v=b.getAttribute('data-'+key);s[key]=s[key]===v?null:v;[].forEach.call(box.querySelectorAll('.chip'),function(x){{x.setAttribute('aria-pressed',String(s[key]===x.getAttribute('data-'+key)));}});render();}});}}
wire('sr-reg','region');wire('sr-typ','type');
document.getElementById('sr-q').addEventListener('input',function(ev){{s.q=ev.target.value.trim().toLowerCase();render();}});
}})();
</script>
'''
(root/'blogger').mkdir(exist_ok=True)
(root/'blogger'/'seismic-radar-blogger.html').write_text(page, encoding='utf-8')
print(len(page), 'bytes')
