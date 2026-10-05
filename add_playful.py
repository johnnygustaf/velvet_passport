from pathlib import Path
p=Path('/mnt/data/velvet_passport/build_site.py')
s=p.read_text()
insert = r'''
# A playful intimacy prompt for every night. These are deliberately flirty rather than explicit,
# and assume enthusiastic consent; either person can skip or change a prompt at any time.
playful_prompts = {
'paris': "Dessert first, figuratively: steal 15 private minutes together before getting dressed for dinner. Later, make the first course a blindfolded taste test; the person being fed chooses when the blindfold comes off.",
'milan': "Make the vodka sauce in an apron-and-nice-underwear dress code if you both feel like it. The 'director' gets one kitchen make-out timeout to call whenever the sauce is simmering and nothing can burn.",
'tokyo': "Turn plating into a teasing little omakase: feed each other the first bite of every course, and use one small silk scarf as a brief blindfold for a mystery bite. Keep the reveal playful, never gross or surprising in a bad way.",
'barcelona': "Every shared plate earns a tiny dare card: slow dance for one song, kiss in the kitchen, whisper what you want later, or trade one piece of clothing. Pick only the dares you both actually want.",
'mexico': "Call a two-minute 'tortilla break' while the dough rests: music up, hands off the food, attention on each other. Whoever wins the tortilla contest gets to choose the post-dinner location and the other person's final drink.",
'greek': "Start the evening with a shower together or a swimsuit-style getting-ready hour, then cook in linen and bare feet. After dinner, take dessert somewhere away from the table and make the rule that nobody checks a phone until morning.",
'seoul': "Use the grill as the excuse for a playful 'chef and guest' dynamic: one cooks the first round while the other sits close, feeds them bites, and handles the drinks. Swap roles halfway through dinner.",
'bangkok': "Make this the silk-and-spice night: one of you chooses the other's outfit, then taste the curry together as the heat builds. Between cooking steps, draw one card from a bowl of affectionate dares you wrote for each other beforehand.",
'buenos': "Give yourselves a pre-dinner rule: twenty private minutes before the steak ever hits the pan. Later, put on one tango song and let the person leading the dance also lead the pacing of dessert - with an easy, immediate veto always available.",
'marrakech': "Build a pillow-and-candle corner before you cook. Halfway through the tagine simmer, take a ten-minute no-talking break together; use touch, eye contact, and music instead, then come back and finish dinner.",
'neworleans': "Dress like you're sneaking out to a hotel bar. Before dinner, each person writes one flirty request on a folded note; exchange them over the first cocktail and decide together which one becomes tonight's encore.",
'copenhagen': "Make the cozy night intentionally unhurried: cook in oversized knits or robes, share the first mulled wine under one blanket, and put a sealed 'open after dessert' note at each place setting with one affectionate invitation for later."
}
for _night in nights:
    _night['playful'] = playful_prompts[_night['id']]
'''
marker="]\n\nsite_data = json.dumps(nights, ensure_ascii=False)"
if marker not in s:
    raise SystemExit('marker not found')
s=s.replace(marker, "]\n"+insert+"\nsite_data = json.dumps(nights, ensure_ascii=False)")
# Add CSS for playful card
s=s.replace(".ritual{", ".playful{margin:0 7% 18px;padding:20px 22px;border:1px solid #e2bac5;border-radius:18px;background:linear-gradient(135deg,#fff8f6,#f7e9ed);position:relative}.playful strong{display:block;font:700 10px Arial,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#7b2f46;margin-bottom:8px}.playful:before{content:'♥';position:absolute;right:18px;top:12px;color:#b9657d;font-size:20px}.ritual{")
# Add playful render before ritual
needle="  <div class=\"ritual ${n.after&&!afterToggle.checked?'blurred':''}\"><strong>${n.after?'After Dark ritual':'Date-night ritual'}</strong><div class=\"ritual-text\">${n.ritual}</div></div>"
rep="  <div class=\"playful\"><strong>Playful interlude</strong><div>${n.playful}</div></div>\n  <div class=\"ritual ${n.after&&!afterToggle.checked?'blurred':''}\"><strong>${n.after?'After Dark ritual':'Date-night ritual'}</strong><div class=\"ritual-text\">${n.ritual}</div></div>"
if needle not in s:
    raise SystemExit('render needle missing')
s=s.replace(needle,rep)
# Print rules
s=s.replace(".ritual{margin:0 32px 18px;break-inside:avoid}", ".playful,.ritual{margin:0 32px 18px;break-inside:avoid}")
# README feature
s=s.replace("- 12 complete date nights\\n", "- 12 complete date nights\\n- a playful intimacy interlude for every night\\n")
p.write_text(s)

# Patch print builder to include playful card
q=Path('/mnt/data/velvet_passport/build_print.py')
t=q.read_text()
needle="<div class=\"ritual\"><strong>{'After Dark ritual' if n['after'] else 'Date-night ritual'}</strong><div class=\"ritual-text\">{esc(n['ritual'])}</div></div>"
rep="<div class=\"playful\"><strong>Playful interlude</strong><div>{esc(n['playful'])}</div></div>\n<div class=\"ritual\"><strong>{'After Dark ritual' if n['after'] else 'Date-night ritual'}</strong><div class=\"ritual-text\">{esc(n['ritual'])}</div></div>"
if needle not in t:
    raise SystemExit('print needle missing')
t=t.replace(needle,rep)
q.write_text(t)
print('patched')
