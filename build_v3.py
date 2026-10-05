from pathlib import Path
import runpy, json, re, html
root=Path('/mnt/data/velvet_passport')
ns=runpy.run_path(str(root/'build_site.py'))
nights=ns['nights']
byid={n['id']:n for n in nights}

# Remove calendar framing and diversify floral language.
flowers={
'paris':'Burgundy garden roses + black calla lilies',
'milan':'Blush peonies + ivory sweet peas',
'tokyo':'White orchids + plum anemones',
'barcelona':'Coral dahlias + bougainvillea',
'mexico':'Marigolds + scarlet celosia',
'greek':'White delphinium + olive branches',
'seoul':'Deep-red spider mums + black calla lilies',
'bangkok':'Fuchsia orchids + jasmine',
'buenos':'Burgundy dahlias + trailing amaranthus',
'marrakech':'Rust chrysanthemums + dried palms',
'neworleans':'Purple lisianthus + magnolia leaves',
'copenhagen':'Winter hellebore + eucalyptus + pine',
}
for n in nights:
    n.pop('month',None)
    n['flowers']=flowers[n['id']]

# Replace Seoul with a dedicated ramen night.
r=byid['seoul']
r.update({
    'city':'Sapporo, Japan',
    'title':'Ramen After Rain',
    'tagline':'Steaming miso ramen, crispy gyoza, cold drinks, and nowhere to rush off to.',
    'mood':'Cozy + slurpable',
    'dress':'Soft layers, socks, hair up, sleeves rolled. Tiny ramen bar energy.',
    'music':'Japanese jazz, city pop, rainy-night instrumentals',
    'after':False,
    'ritual':'Before dinner, each write three folded cards: one sweet dare, one flirty dare, and one “dealer’s choice.” Put all six in a bowl. Draw one while the broth simmers, one between ramen and dessert, and save one unopened for later.',
    'menu':['Crispy pork gyoza','Sapporo-style miso ramen','Soy-butter corn & mushrooms','Black sesame ice cream'],
    'recipes':[
        ('Crispy Pork Gyoza',['24 gyoza wrappers','8 oz ground pork','1 cup finely chopped napa cabbage','2 scallions, minced','1 tbsp soy sauce','1 tsp sesame oil','1 tsp grated ginger','1 tbsp neutral oil'],['Mix pork, cabbage, scallions, soy sauce, sesame oil, and ginger.','Fill wrappers with about 1 teaspoon filling; wet edges and pleat closed.','Pan-fry in oil until bottoms are golden. Add 1/3 cup water, cover, and steam 4-5 minutes.','Uncover and cook until bottoms crisp again.']),
        ('Sapporo-Style Miso Ramen',['8 oz fresh ramen noodles','4 cups chicken stock','2 tbsp white or yellow miso','1 tbsp soy sauce','1 tbsp butter','8 oz ground pork','2 garlic cloves, minced','1 tsp grated ginger','1 cup corn','2 soft-boiled eggs, halved','2 scallions, sliced'],['Brown pork in a pot. Add garlic and ginger and cook 30 seconds.','Add stock and soy sauce; simmer 10 minutes. Whisk miso with a little hot broth, then return it to the pot. Do not boil hard after adding miso.','Cook noodles separately and divide between two large bowls.','Ladle over broth and pork; top with butter, corn, egg, and scallions.']),
        ('Soy-Butter Corn & Mushrooms',['8 oz cremini mushrooms, sliced','1 1/2 cups corn','2 tbsp butter','1 tbsp soy sauce','1 tsp sesame oil','2 scallions, sliced'],['Brown mushrooms in 1 tablespoon butter over medium-high heat.','Add corn and remaining butter; cook until lightly charred.','Add soy sauce and sesame oil and toss for 30 seconds.','Finish with scallions.']),
        ('Black Sesame Ice Cream Sundaes',['1 pint vanilla ice cream','2 tbsp black sesame paste','1 tbsp honey','2 tbsp toasted sesame seeds','4 crisp wafer cookies'],['Stir black sesame paste and honey together until glossy.','Scoop ice cream into bowls and ribbon the sesame mixture over top.','Sprinkle with toasted sesame seeds.','Serve with a crisp wafer cookie.'])
    ]
})

# Stronger playful / write-it-down dare system for every night.
playful={
'paris':'Before getting dressed, each write one thing you want more of tonight and seal it in an envelope. Take 15 private pre-dinner minutes together, then open the notes over the first drink. If both notes point the same direction, consider that the theme of the evening.',
'milan':'Each write three tiny dare cards before cooking: one kitchen dare, one compliment dare, and one after-dinner dare. Cook the vodka sauce in an apron-only-or-nearly-so dress code if you both want. Draw the kitchen card only while the sauce is safely simmering.',
'tokyo':'Create a four-card mini omakase before dinner: feed me, blindfold bite, secret compliment, and dealer’s choice. Shuffle them and draw one before each course. Either person can redraw once, no questions asked.',
'barcelona':'Each write four tapas dares and mix them in a bowl. Every second shared plate earns a draw: slow dance, kitchen kiss, whisper what you want later, trade one item of clothing, or invent your own. A dare only counts if both people like it.',
'mexico':'Write three “winner chooses” cards before you start: next song, next kiss location, and post-dinner destination. Make tortillas like a ridiculous competition. Best tortilla gets the first card; best taco build gets the second.',
'greek':'Each write a postcard-sized “wish for tonight” before cooking, then hide it under the other person’s plate. Start with a shower together or an unhurried getting-ready hour, cook barefoot, and reveal the wishes with dessert away from the table.',
'seoul':'While the broth simmers, each write one sweet dare, one flirty dare, and one wildcard. Put all six in a bowl. Draw one before ramen, one after the bowls are empty, and leave one sealed for later. A skip is always free.',
'bangkok':'Build a six-card silk-and-spice deck before dinner: outfit choice, feed me a bite, kitchen kiss, slow dance, whisper a request, dealer’s choice. Draw one every time you finish a cooking step. If the card does not fit the moment, put it back and redraw.',
'buenos':'Before the steak hits the pan, each write one “lead me” card and one “surprise me” card. Take 20 private pre-dinner minutes together, then draw a card after the steaks rest. The person leading the tango later also chooses when dessert begins.',
'marrakech':'Each write three cards before cooking: touch, tell, and tease. During the tagine simmer, draw one and take a ten-minute no-phone, low-light break together. Save the other two for the pillow-and-candle corner after dinner.',
'neworleans':'Dress like you are meeting secretly at a hotel bar. Each write two flirty requests and one “absolutely ridiculous” dare. Exchange one over the first cocktail, one with dessert, and keep the last as the encore card.',
'copenhagen':'Make six folded notes before dinner: three invitations and three dares. Cook in robes or oversized knits, draw one under a shared blanket with the first drink, and place one sealed note at each setting marked “open after dessert.”'
}
for n in nights: n['playful']=playful[n['id']]

# Interactive themed dare deck. Kept playful and non-graphic.
dares={
'paris':['Choose the other person’s next song.','Give a one-minute shoulder massage before the next course.','Whisper one thing you have wanted to hear from them lately.','Slow dance through one entire song.','Trade one item of clothing for the next course.','Call a five-minute private intermission before dessert.'],
'milan':['The other person picks your apron or cooking outfit.','Kiss until the song changes, then get back to the sauce.','Feed each other the next three bites.','Give one very specific compliment you have not said before.','The “director” chooses dessert location.','Write one after-dinner request and hand it over folded.'],
'tokyo':['Feed the first bite of the next course.','Blindfold one mystery bite.','Choose a song that reminds you of the other person.','Give a whispered compliment in ten words or fewer.','Sit on the same side of the table for the next course.','Dealer’s choice: invent a gentle dare together.'],
'barcelona':['Slow dance for one song.','Kiss in the kitchen before plating the next dish.','Trade one accessory or item of clothing.','Say what you want more of tonight.','Feed each other the next bite.','Move dessert somewhere other than the table.'],
'mexico':['Winner chooses where the next kiss happens.','Loser makes the winner’s next taco.','Pick the next three songs.','Do a 60-second dance break while the tortillas rest.','Write a one-line request for later.','Winner chooses where dessert is eaten.'],
'greek':['Take dessert outside or onto the floor with pillows.','Give the other person a five-minute hand or shoulder massage.','Share one travel fantasy you would actually book.','Put phones away until tomorrow morning.','Choose the other person’s final drink.','Write one wish for the rest of the night.'],
'seoul':['Feed the other person the first perfect ramen bite.','Choose the next song and pull them in for a kitchen dance.','Write one post-ramen request and fold it shut.','Swap seats and sit shoulder-to-shoulder.','Take a five-minute no-talking cuddle break while the broth simmers.','Dealer’s choice: invent one dare together.'],
'bangkok':['Choose the other person’s outfit detail.','Feed them one bite with eyes closed.','Whisper one request before the next cooking step.','Dance until the current song ends.','Trade one clothing item or accessory.','Call a two-minute kitchen make-out timeout.'],
'buenos':['Lead one full tango song.','Choose the other person’s final drink.','Give a slow one-minute neck or shoulder massage.','Write one “surprise me” note for later.','The leader chooses dessert timing.','Take a ten-minute private intermission before dessert.'],
'marrakech':['Take a ten-minute no-talking candlelit break together.','Choose one scent, song, or texture for the room.','Whisper a request, not a question.','Feed each other dessert from the same plate.','Write one tease card and seal it for later.','Move to the pillow corner for the next course.'],
'neworleans':['Read one folded request over the first cocktail.','Slow dance to one jazz song.','Choose a ridiculous secret alias for each other tonight.','Give one hotel-bar-worthy compliment.','Write one encore request for later.','Move the final drink somewhere more private.'],
'copenhagen':['Open one invitation note under a shared blanket.','Give a five-minute foot or shoulder massage.','Choose one memory from the year and tell the full story.','Write one affectionate dare for after dessert.','Share dessert from one bowl.','Put every screen away for the rest of the night.']
}
for n in nights: n['dares']=dares[n['id']]

# Search/filter tags.
def tags(n):
    s=(' '.join([n['title'],n['mood'],*n['menu'],*[x[0] for x in n['recipes']]])).lower()
    out=['dare']
    if n['after']: out.append('after')
    if any(k in s for k in ['steak','ribeye','filet']): out.append('steak')
    if 'truffle' in s: out.append('truffle')
    if any(k in s for k in ['pasta','rigatoni','noodle','ramen','pad see ew']): out.append('noodles')
    if 'ramen' in s: out.append('ramen')
    if any(k in n['mood'].lower() for k in ['cozy','intimate','breezy']): out.append('cozy')
    if any(k in n['mood'].lower() for k in ['glamour','luxe','classic','slow-burn']): out.append('fancy')
    if any(k in s for k in ['share','tapas','tacos','mezze']): out.append('shareable')
    return out
for n in nights: n['tags']=tags(n)

# Keep source quantities as the base for four, but browser defaults to dinner-for-two and scales dynamically.
data=json.dumps(nights,ensure_ascii=False)

index='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Velvet Passport - Choose Your Night</title><link rel="stylesheet" href="styles.css"></head><body>
<header class="hero" id="top"><div class="eyebrow">CHOOSE A CRAVING. DRAW A DARE. GO SOMEWHERE ELSE FOR A NIGHT.</div><h1>Velvet Passport</h1><p class="dek">Date nights selected by appetite, not by calendar.</p><p class="sub">For Johnny &amp; Frances - steak, truffle, vodka sauce, ramen, flowers, tiny rituals, and a deck of folded trouble.</p><div class="hero-actions"><button id="surprise">Surprise us tonight</button><button class="ghost" onclick="window.print()">Print / Save PDF</button></div><div class="stamp">DINNER FOR 2<br>SCALABLE<br>DARE DECKS</div></header>
<nav class="selection-nav" id="selectionNav"><button class="navchip active" data-filter="all">Everything</button><button class="navchip" data-filter="steak">Steak</button><button class="navchip" data-filter="truffle">Truffle</button><button class="navchip" data-filter="ramen">Ramen</button><button class="navchip" data-filter="noodles">Pasta + noodles</button><button class="navchip" data-filter="dare">Dares</button><button class="navchip" data-filter="after">After Dark</button><button class="navchip" data-filter="cozy">Cozy</button><button class="navchip" data-filter="fancy">Fancy</button><button class="navchip" data-filter="shareable">Shareable</button></nav>
<section class="controls"><div class="serve-control"><span>Dinner for</span><button class="serve" data-servings="2">2</button><button class="serve" data-servings="4">4</button><button class="serve" data-servings="6">6</button><button class="serve" data-servings="8">8</button></div><label class="toggle"><input type="checkbox" id="afterToggle"><span></span> Reveal After Dark rituals</label></section>
<main id="app"></main><footer><div class="flower-mark">✿</div><h2>Pick by appetite.</h2><p>No months. No order. Tonight only needs a craving and a little nerve.</p><a href="#top">Back to the top ↑</a></footer>
<script>window.NIGHTS='''+data+''';</script><script src="app.js"></script></body></html>'''

js=r'''const nights=window.NIGHTS;
let currentFilter='all'; let servings=2;
const app=document.querySelector('#app'); const afterToggle=document.querySelector('#afterToggle');
const FRACTIONS={'1/2':.5,'1/3':1/3,'2/3':2/3,'1/4':.25,'3/4':.75,'1/8':.125,'3/8':.375,'5/8':.625,'7/8':.875};
function fmt(x){if(Math.abs(x-Math.round(x))<.001)return String(Math.round(x)); const fr=[[.125,'1/8'],[.25,'1/4'],[1/3,'1/3'],[.375,'3/8'],[.5,'1/2'],[.625,'5/8'],[2/3,'2/3'],[.75,'3/4'],[.875,'7/8']];let w=Math.floor(x),d=x-w,b=fr.reduce((a,z)=>Math.abs(z[0]-d)<Math.abs(a[0]-d)?z:a,fr[0]);return (w?w+' ':'')+b[1]}
function nval(s){s=s.trim(); if(FRACTIONS[s]!=null)return FRACTIONS[s]; if(/^\d+(\.\d+)?$/.test(s))return +s; const m=s.match(/^(\d+)\s+(\d\/\d)$/); if(m)return +m[1]+(FRACTIONS[m[2]]||0); return null}
function scaleIngredient(s){const factor=servings/4; let m=s.match(/^(\d+\s+\d\/\d|\d+\/\d|\d+(?:\.\d+)?)(?:-(\d+\s+\d\/\d|\d+\/\d|\d+(?:\.\d+)?))?(.*)$/); if(!m)return s; let a=nval(m[1]); if(a==null)return s; let out=fmt(a*factor); if(m[2]){let b=nval(m[2]); if(b!=null)out+='-'+fmt(b*factor)} return out+m[3]}
function uniqIngredients(n){let a=[]; n.recipes.forEach(r=>r[1].forEach(x=>a.push(scaleIngredient(x)))); return [...new Set(a)]}
function render(){app.innerHTML=''; const filtered=currentFilter==='all'?nights:nights.filter(n=>n.tags.includes(currentFilter)); filtered.forEach((n,i)=>{const sec=document.createElement('section');sec.className='night';sec.id=n.id; const dark=n.after&&!afterToggle.checked;
sec.innerHTML=`<div class="night-head"><div class="passport">Passport No. ${String(nights.indexOf(n)+1).padStart(2,'0')}</div><h2>${n.title}</h2><div class="city">${n.city}</div><p class="tagline">${n.tagline}</p><div class="badges"><span class="badge">${n.mood}</span><span class="badge flower-badge">${n.flowers}</span>${n.tags.map(t=>`<span class="badge tag">${t}</span>`).join('')}</div></div>
<div class="details"><div class="detail"><small>Flowers</small><div>${n.flowers}</div></div><div class="detail"><small>Dress</small><div>${n.dress}</div></div><div class="detail"><small>Sound</small><div>${n.music}</div></div><div class="detail"><small>Serves tonight</small><div>${servings} ${servings===2?'lovers':'people'}</div></div></div>
<div class="menu-wrap"><h3>Tonight’s menu</h3><div class="menu">${n.menu.map(x=>`<div class="menu-item">${x}</div>`).join('')}</div></div>
<div class="playful"><strong>Before dinner: write it down</strong><div>${n.playful}</div></div>
<div class="dare-box"><div><strong>Dare Deck</strong><p>Write your own cards first, or let Velvet Passport deal one.</p></div><button class="draw-dare" data-id="${n.id}">Draw a dare</button><div class="dare-result" id="dare-${n.id}">Folded cards > algorithms. But both are fun.</div></div>
<div class="ritual ${dark?'blurred':''}"><strong>${n.after?'After Dark ritual':'Date-night ritual'}</strong><div class="ritual-text">${n.ritual}</div></div>
<div class="recipes"><div class="recipes-title"><h3>Recipes</h3><span>scaled from 4 → <b>${servings}</b></span></div><div class="recipe-grid">${n.recipes.map(r=>`<article class="recipe"><div class="serves">Serves ${servings}</div><h4>${r[0]}</h4><div class="recipe-columns"><ul>${r[1].map(x=>`<li>${scaleIngredient(x)}</li>`).join('')}</ul><ol>${r[2].map(x=>`<li>${x}</li>`).join('')}</ol></div></article>`).join('')}</div></div>
<details class="grocery"><summary>Grocery checklist · scaled for ${servings}</summary><div class="grocery-list">${uniqIngredients(n).map((x,j)=>`<label><input type="checkbox" data-key="${n.id}-${servings}-${j}"> ${x}</label>`).join('')}</div></details>`; app.appendChild(sec);});restoreChecks(); bindDares();}
function restoreChecks(){document.querySelectorAll('.grocery input').forEach(c=>{c.checked=localStorage.getItem('vp-'+c.dataset.key)==='1';c.addEventListener('change',()=>localStorage.setItem('vp-'+c.dataset.key,c.checked?'1':'0'))})}
function bindDares(){document.querySelectorAll('.draw-dare').forEach(b=>b.addEventListener('click',()=>{let n=nights.find(x=>x.id===b.dataset.id);let result=n.dares[Math.floor(Math.random()*n.dares.length)];document.querySelector('#dare-'+n.id).textContent=result}))}
afterToggle.addEventListener('change',render);
document.querySelectorAll('.navchip').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('.navchip').forEach(x=>x.classList.remove('active'));b.classList.add('active');currentFilter=b.dataset.filter;render()}));
document.querySelectorAll('.serve').forEach(b=>b.addEventListener('click',()=>{servings=+b.dataset.servings;document.querySelectorAll('.serve').forEach(x=>x.classList.toggle('active',+x.dataset.servings===servings));render()}));document.querySelector('.serve[data-servings="2"]').classList.add('active');
document.querySelector('#surprise').addEventListener('click',()=>{const pool=currentFilter==='all'?nights:nights.filter(n=>n.tags.includes(currentFilter));const n=pool[Math.floor(Math.random()*pool.length)];location.hash=n.id;setTimeout(()=>document.querySelector('#'+n.id)?.scrollIntoView({behavior:'smooth'}),40)});render();'''

css=r''':root{--ink:#1d1115;--wine:#5b1f31;--deep:#2a111b;--rose:#b56c7e;--cream:#f8f0e6;--paper:#fffaf5;--gold:#b78c57}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font-family:Georgia,'Times New Roman',serif;line-height:1.5}.hero{min-height:82vh;background:radial-gradient(circle at 18% 8%,#793047 0 10%,transparent 29%),linear-gradient(135deg,#180c12,#461828 58%,#1f0e15);color:#fff6ee;padding:9vw 8vw;position:relative;overflow:hidden}.hero:after{content:"✦  ❀  ✦";position:absolute;right:6vw;bottom:5vw;font-size:clamp(50px,9vw,130px);letter-spacing:.18em;color:#dca9b7;opacity:.18;transform:rotate(-8deg)}.eyebrow{font:600 12px Arial,sans-serif;letter-spacing:.24em;color:#e7c7cf;max-width:800px}.hero h1{font-size:clamp(60px,10vw,150px);font-weight:400;letter-spacing:-.055em;margin:.05em 0}.dek{font-size:clamp(23px,3vw,42px);margin:0;color:#f3d9df}.sub{max-width:760px;font-size:18px;color:#eadcdf}.hero-actions{display:flex;gap:12px;margin-top:34px;flex-wrap:wrap}button{font:700 11px Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;border:0;border-radius:999px;padding:13px 18px;background:var(--cream);color:var(--deep);cursor:pointer}.ghost{background:transparent;color:white;border:1px solid #ffffff55}.stamp{position:absolute;right:8vw;top:7vw;border:1px solid #e6bdc7;border-radius:50%;width:122px;height:122px;display:grid;place-items:center;text-align:center;font:700 10px/1.5 Arial,sans-serif;letter-spacing:.12em;transform:rotate(8deg);color:#efced6}.selection-nav{position:sticky;top:0;z-index:20;display:flex;gap:8px;overflow:auto;padding:12px 5vw;background:#fffaf5ee;backdrop-filter:blur(14px);border-bottom:1px solid #eadbd7}.navchip{white-space:nowrap;background:#f1e4df;color:#5c2736}.navchip.active{background:var(--wine);color:#fff}.controls{padding:20px 6vw;display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;border-bottom:1px solid #eadbd7}.controls span,.serve-control>span{font:700 10px Arial,sans-serif;text-transform:uppercase;letter-spacing:.13em;margin-right:8px}.serve{background:#f0e3df;padding:10px 14px}.serve.active{background:var(--deep);color:white}.toggle{font:700 10px Arial,sans-serif;text-transform:uppercase;letter-spacing:.08em;display:flex;align-items:center;gap:8px}.toggle input{accent-color:var(--wine)}main{max-width:1220px;margin:auto;padding:30px 5vw 90px}.night{margin:50px 0 90px;border:1px solid #e5d4cf;background:#fff;box-shadow:0 18px 50px #37111f12;border-radius:28px;overflow:hidden}.night-head{padding:54px 7%;background:linear-gradient(125deg,#fffaf6 0 66%,#f0dadd 66%);position:relative}.night-head:after{content:"❀";position:absolute;right:5%;bottom:-34px;font-size:150px;color:#7c3044;opacity:.10;transform:rotate(-14deg)}.passport{font:700 10px Arial,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:var(--rose)}.night h2{font-size:clamp(40px,6vw,78px);font-weight:400;letter-spacing:-.045em;margin:3px 0;color:var(--deep)}.city{font-style:italic;color:var(--wine)}.tagline{font-size:20px;max-width:700px}.badges{display:flex;gap:7px;flex-wrap:wrap;margin-top:18px}.badge{font:700 9px Arial,sans-serif;letter-spacing:.07em;text-transform:uppercase;border-radius:999px;padding:7px 10px;background:#f2e3df;color:#693346}.flower-badge{background:#efe7dd;color:#55453e}.badge.tag{background:#fff;border:1px solid #e3cfca}.details{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid #eddeda;border-bottom:1px solid #eddeda}.detail{padding:22px;border-right:1px solid #eddeda}.detail:last-child{border-right:0}.detail small{font:700 9px Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#9a7180}.menu-wrap{padding:34px 7%}.menu-wrap h3,.recipes h3{font-size:28px;font-weight:400;margin:0 0 15px}.menu{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.menu-item{border-radius:16px;background:#f8efeb;padding:18px;font-style:italic;min-height:80px;display:flex;align-items:flex-end}.playful{margin:0 7% 16px;padding:21px 23px;border:1px solid #e2bac5;border-radius:18px;background:linear-gradient(135deg,#fff8f6,#f7e9ed);position:relative}.playful:before{content:'✎';position:absolute;right:20px;top:13px;color:#a84e68;font-size:23px}.playful strong,.dare-box strong,.ritual strong{display:block;font:700 10px Arial,sans-serif;letter-spacing:.15em;text-transform:uppercase;margin-bottom:7px}.playful strong{color:#7b2f46}.dare-box{margin:0 7% 18px;padding:21px 23px;background:#f4eadc;border-radius:18px;display:grid;grid-template-columns:1fr auto;gap:12px;align-items:center}.dare-box strong{color:#71502d}.dare-box p{margin:0}.draw-dare{background:#76532f;color:white}.dare-result{grid-column:1/-1;padding-top:11px;border-top:1px solid #dccab3;font-style:italic;font-size:17px}.ritual{margin:0 7% 30px;padding:22px 24px;border-left:4px solid var(--wine);background:#2d141f;color:#f7e8e7;border-radius:0 16px 16px 0}.ritual strong{color:#dda8b5}.ritual.blurred .ritual-text{filter:blur(7px);user-select:none}.ritual.blurred:after{content:'Reveal After Dark above to open this card.';display:block;font:700 10px Arial,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#f0c8d1;margin-top:-18px;position:relative}.recipes{padding:0 7% 40px}.recipes-title{display:flex;align-items:baseline;justify-content:space-between;gap:16px}.recipes-title span{font:700 10px Arial,sans-serif;text-transform:uppercase;letter-spacing:.1em;color:#9a7180}.recipe-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}.recipe{border:1px solid #e9d8d3;border-radius:18px;padding:22px;background:#fffdfb}.recipe h4{font-size:22px;margin:0 0 8px}.serves{font:700 9px Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#a36c7b}.recipe-columns{display:grid;grid-template-columns:1fr 1.15fr;gap:18px;margin-top:15px}.recipe ul,.recipe ol{margin:0;padding-left:18px;font-size:14px}.recipe li{margin:5px 0}.grocery{margin:0 7% 45px;border:1px dashed #cdaeb5;border-radius:18px;padding:18px;background:#fbf5f1}.grocery summary{cursor:pointer;font-size:20px}.grocery-list{columns:2;margin-top:12px}.grocery label{display:block;break-inside:avoid;font-size:14px;margin:6px 0}.grocery input{accent-color:var(--wine)}footer{text-align:center;padding:75px 20px;background:var(--deep);color:#f5e6e3}.flower-mark{font-size:75px;color:#b9657d}footer h2{font-size:46px;font-weight:400;margin:0}footer a{color:#ecc9d0}@media(max-width:800px){.stamp{display:none}.details,.menu,.recipe-grid{grid-template-columns:1fr 1fr}.recipe-columns{grid-template-columns:1fr}.grocery-list{columns:1}}@media(max-width:540px){.hero{padding:17vh 7vw 10vh}.details,.menu,.recipe-grid{grid-template-columns:1fr}.detail{border-right:0;border-bottom:1px solid #eddeda}.night-head{padding:40px 8%}.dare-box{grid-template-columns:1fr}.draw-dare{justify-self:start}.controls{align-items:flex-start}.recipes-title{align-items:flex-start;flex-direction:column}.stamp{display:none}}@media print{.hero{min-height:auto;padding:45px 40px}.hero-actions,.controls,.selection-nav,.draw-dare,.grocery,footer a{display:none!important}.night{break-before:page;margin:0;border:0;box-shadow:none;border-radius:0}.night-head{padding:28px}.details{grid-template-columns:repeat(4,1fr)}.detail{padding:10px}.menu-wrap{padding:17px 30px}.playful,.dare-box,.ritual{margin:0 30px 13px;break-inside:avoid;padding:14px 16px}.recipes{padding:0 30px 16px}.recipe{break-inside:avoid;padding:15px}.recipe-grid{gap:8px}.recipe h4{font-size:16px}.recipe-columns{gap:7px}.recipe ul,.recipe ol{font-size:9px}.night h2{font-size:38px}.tagline{font-size:14px}.dare-result{font-size:12px}@page{size:Letter;margin:.32in}}'''

root.joinpath('index.html').write_text(index)
root.joinpath('app.js').write_text(js)
root.joinpath('styles.css').write_text(css)
root.joinpath('README.txt').write_text('''VELVET PASSPORT - CHOOSE YOUR NIGHT\n\nOpen index.html in a browser.\n\nFeatures:\n- 12 date nights selected by craving/mood, not month\n- filters for Steak, Truffle, Ramen, Pasta + Noodles, Dares, After Dark, Cozy, Fancy, Shareable\n- dedicated Sapporo ramen night\n- varied floral styling across every night\n- interactive Dare Deck on every night\n- serving selector for 2 / 4 / 6 / 8 (defaults to 2)\n- dynamically scaled recipe ingredients and grocery checklists\n- persistent grocery checkboxes\n- surprise picker respects the currently selected filter\n- mobile responsive + print/PDF styling\n\nDeploy to Vercel as a static site; no build command required.\n''')

# Standalone version.
stand=index.replace('<link rel="stylesheet" href="styles.css">','<style>'+css+'</style>').replace('<script src="app.js"></script>','<script>'+js+'</script>')
root.joinpath('Velvet_Passport_Standalone.html').write_text(stand)

# Print edition: fixed at 2 servings, no months.
def esc(s): return html.escape(str(s))
def scale_simple(s,f=.5):
    fr={'1/2':.5,'1/3':1/3,'2/3':2/3,'1/4':.25,'3/4':.75,'1/8':.125,'3/8':.375,'5/8':.625,'7/8':.875}
    def nv(x):
        x=x.strip()
        if x in fr:return fr[x]
        if re.match(r'^\d+(\.\d+)?$',x):return float(x)
        m=re.match(r'^(\d+)\s+(\d/\d)$',x)
        return float(m.group(1))+fr.get(m.group(2),0) if m else None
    def fm(x):
        if abs(x-round(x))<.001:return str(int(round(x)))
        whole=int(x); d=x-whole; opts=[(.125,'1/8'),(.25,'1/4'),(1/3,'1/3'),(.375,'3/8'),(.5,'1/2'),(.625,'5/8'),(2/3,'2/3'),(.75,'3/4'),(.875,'7/8')]; q=min(opts,key=lambda z:abs(z[0]-d))[1]
        return (str(whole)+' ' if whole else '')+q
    m=re.match(r'^(\d+\s+\d/\d|\d+/\d|\d+(?:\.\d+)?)(?:-(\d+\s+\d/\d|\d+/\d|\d+(?:\.\d+)?))?(.*)$',s)
    if not m:return s
    a=nv(m.group(1)); out=fm(a*f)
    if m.group(2):out+='-'+fm(nv(m.group(2))*f)
    return out+m.group(3)
secs=[]
for i,n in enumerate(nights,1):
    rec=[]
    for rr in n['recipes']:
        rec.append('<article class="recipe"><div class="serves">Serves 2</div><h4>'+esc(rr[0])+'</h4><div class="recipe-columns"><ul>'+''.join('<li>'+esc(scale_simple(x))+'</li>' for x in rr[1])+'</ul><ol>'+''.join('<li>'+esc(x)+'</li>' for x in rr[2])+'</ol></div></article>')
    secs.append(f'''<section class="night" id="{n['id']}"><div class="night-head"><div class="passport">Passport No. {i:02d}</div><h2>{esc(n['title'])}</h2><div class="city">{esc(n['city'])}</div><p class="tagline">{esc(n['tagline'])}</p><div class="badges"><span class="badge">{esc(n['mood'])}</span><span class="badge flower-badge">{esc(n['flowers'])}</span></div></div><div class="details"><div class="detail"><small>Flowers</small><div>{esc(n['flowers'])}</div></div><div class="detail"><small>Dress</small><div>{esc(n['dress'])}</div></div><div class="detail"><small>Sound</small><div>{esc(n['music'])}</div></div><div class="detail"><small>Serves</small><div>Dinner for two</div></div></div><div class="menu-wrap"><h3>Tonight's menu</h3><div class="menu">{''.join('<div class="menu-item">'+esc(x)+'</div>' for x in n['menu'])}</div></div><div class="playful"><strong>Before dinner: write it down</strong><div>{esc(n['playful'])}</div></div><div class="dare-box"><div><strong>Six-card Dare Deck</strong><p>{esc(' • '.join(n['dares'][:3]))}</p></div><div class="dare-result">Plus three blank cards for whatever you two write yourselves.</div></div><div class="ritual"><strong>{'After Dark ritual' if n['after'] else 'Date-night ritual'}</strong><div class="ritual-text">{esc(n['ritual'])}</div></div><div class="recipes"><div class="recipes-title"><h3>Recipes</h3><span>DINNER FOR 2</span></div><div class="recipe-grid">{''.join(rec)}</div></div></section>''')
print_html=f'''<!doctype html><html><head><meta charset="utf-8"><title>Velvet Passport</title><link rel="stylesheet" href="styles.css"></head><body><header class="hero"><div class="eyebrow">CHOOSE A CRAVING. DRAW A DARE. GO SOMEWHERE ELSE FOR A NIGHT.</div><h1>Velvet Passport</h1><p class="dek">Date nights selected by appetite, not by calendar.</p><p class="sub">For Johnny &amp; Frances - dinner for two, scalable online, with flowers and folded trouble.</p><div class="stamp">DINNER FOR 2<br>DARE DECKS<br>NO CALENDAR</div></header><main>{''.join(secs)}</main><footer><div class="flower-mark">✿</div><h2>Pick by appetite.</h2><p>No months. No order. Just choose what sounds good tonight.</p></footer></body></html>'''
root.joinpath('print.html').write_text(print_html)
print('built v3')
