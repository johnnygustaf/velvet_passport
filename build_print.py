from pathlib import Path
import runpy
root=Path('/mnt/data/velvet_passport')
ns=runpy.run_path(str(root/'build_site.py'))
nights=ns['nights']

def tokens(n):
    s=(' '.join([n['title'],*n['menu'],*[r[0] for r in n['recipes']]])).lower()
    return {'steak': any(k in s for k in ['steak','ribeye','filet']), 'pasta': any(k in s for k in ['rigatoni','noodles','pasta','pad see ew']), 'truffle':'truffle' in s}

def esc(s):
    return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
sections=[]
for i,n in enumerate(nights,1):
    t=tokens(n)
    recipes=[]
    for r in n['recipes']:
        recipes.append(f'''<article class="recipe"><div class="serves">Serves 4</div><h4>{esc(r[0])}</h4><div class="recipe-columns"><ul>{''.join('<li>'+esc(x)+'</li>' for x in r[1])}</ul><ol>{''.join('<li>'+esc(x)+'</li>' for x in r[2])}</ol></div></article>''')
    sections.append(f'''<section class="night" id="{n['id']}"><div class="night-head"><div class="month">{n['month']} · Passport No. {i:02d}</div><h2>{esc(n['title'])}</h2><div class="city">{esc(n['city'])}</div><p class="tagline">{esc(n['tagline'])}</p><div class="badges"><span class="badge">{esc(n['mood'])}</span><span class="badge">{esc(n['flowers'])}</span>{'<span class="badge dark">After Dark</span>' if n['after'] else ''}</div></div>
<div class="details"><div class="detail"><small>Flowers</small><div>{esc(n['flowers'])}</div></div><div class="detail"><small>Dress</small><div>{esc(n['dress'])}</div></div><div class="detail"><small>Sound</small><div>{esc(n['music'])}</div></div><div class="detail"><small>Food bias</small><div>{'Truffle-forward' if t['truffle'] else 'Steak-night energy' if t['steak'] else 'Noodles / pasta' if t['pasta'] else 'Shareable comfort'}</div></div></div>
<div class="menu-wrap"><h3>Tonight’s menu</h3><div class="menu">{''.join('<div class="menu-item">'+esc(x)+'</div>' for x in n['menu'])}</div></div>
<div class="playful"><strong>Playful interlude</strong><div>{esc(n['playful'])}</div></div>
<div class="ritual"><strong>{'After Dark ritual' if n['after'] else 'Date-night ritual'}</strong><div class="ritual-text">{esc(n['ritual'])}</div></div>
<div class="recipes"><h3>Recipes · serves 4</h3><div class="recipe-grid">{''.join(recipes)}</div></div></section>''')

toc=''.join(f'<a href="#{n["id"]}">{n["month"]}</a>' for n in nights)
html=f'''<!doctype html><html><head><meta charset="utf-8"><title>Velvet Passport</title><link rel="stylesheet" href="styles.css"></head><body><header class="hero" id="top"><div class="eyebrow">A PRIVATE LITTLE WORLD TOUR</div><h1>Velvet Passport</h1><p class="dek">12 Date Nights Around the World</p><p class="sub">For Johnny &amp; Frances — food, flowers, music, rituals, and three nights that go a little darker.</p><div class="stamp">RANUNCULUS<br>AFTER DARK<br>RECIPES FOR 4</div></header><nav class="month-nav">{toc}</nav><main>{''.join(sections)}</main><footer><div class="flower-mark">✿</div><h2>Keep the passport.</h2><p>One photograph per night. Twelve little worlds by the end of the year.</p></footer></body></html>'''
(root/'print.html').write_text(html)
print('wrote print.html')
