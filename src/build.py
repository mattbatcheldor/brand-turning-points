from html import escape
from pathlib import Path
import json
import random

root = Path(__file__).resolve().parent
campaigns = json.loads((root / 'campaigns.json').read_text(encoding='utf-8'))
e = escape
random.seed(24)
colours = ['#f4504b', '#f49e41', '#ebde54', '#b2e25b', '#38c9bd', '#5994ec', '#b575ed', '#ee88b5']
balls = []
for i in range(214):
    z = random.random()
    x = 486 + (random.random() - .5) * (270 + 720*z) - 68*z
    y = 206 + 338*z - random.random() * (18 + 130*z)
    r = 1.8 + (1.5 + 8*z)*random.random()
    balls.append((y, f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{random.choice(colours)}" opacity="{.68 + .32*random.random():.2f}"/>'))
dots = '\n'.join(ball for _,ball in sorted(balls))
art = '''<svg viewBox="0 0 920 560" preserveAspectRatio="xMidYMid slice" role="img" aria-labelledby="art-title">
<title id="art-title">Illustration of bright bouncy balls tumbling down a San Francisco hillside</title>
<defs>
  <linearGradient id="sky" x2="0" y2="1" gradientUnits="objectBoundingBox"><stop stop-color="#303951"/><stop offset="1" stop-color="#e7b79b"/></linearGradient>
  <linearGradient id="street" x2="0" y2="1" gradientUnits="objectBoundingBox"><stop stop-color="#82767c"/><stop offset="1" stop-color="#222732"/></linearGradient>
  <linearGradient id="shadow"><stop stop-color="#141b28"/><stop offset="1" stop-color="#3a4050"/></linearGradient>
  <pattern id="windows" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M8 7h13v18H8z" fill="#d3a184" opacity=".36"/><path d="M14 7v18M8 16h13" stroke="#312e38" stroke-width="1"/></pattern>
  <pattern id="grain" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="1" cy="4" r=".45" fill="#ffeed9" opacity=".17"/><circle cx="6" cy="1" r=".5" fill="#120c17" opacity=".29"/></pattern>
</defs>
<path d="M0 0h920v560H0z" fill="url(#sky)"/>
<circle cx="625" cy="133" r="81" fill="#ffd9a7" opacity=".65"/>
<path d="M0 252L364 186l128-35 162 47 266 73v289H0z" fill="#7d717b"/>
<path d="M6 313L457 197l30-42 45 53 374 100v252H6z" fill="#aea09a"/>
<path d="M0 492L480 170l12 6L920 487v73H0z" fill="url(#street)"/>
<path d="M493 198L468 560M504 208L545 560" stroke="#a79682" stroke-dasharray="11 22" stroke-width="2.7" opacity=".52"/>
<path d="M0 380L443 220M534 209l386 179M0 430L430 236M548 229l372 212" fill="none" stroke="#dcc8ad" stroke-width="2" opacity=".56"/>
<path d="M0 39L109 55v29l39-18 75 24v31l49-10 54 19v35l40-11 47 22v58L0 443z" fill="url(#shadow)"/>
<path d="M0 73l105 16v135L0 268zm117 38l99-13v120l-99 50zm109 34l90-13v92l-90 46zm99 39l74-17v67l-74 34z" fill="url(#windows)"/>
<path d="M920 17L809 48v42l-46-13-70 25v35l-43-12-61 22v31l-53 11v44l384 182z" fill="#3a3949"/>
<path d="M920 75l-105 29v143l105 37zm-116 53l-103-19v139l103 50zm-113 31l-94-11v104l94 50z" fill="url(#windows)"/>
<path d="M0 39L109 55l39 11 75 24m586-42l111-31M0 327l411-106m126 2l383 128" stroke="#f5d6b3" stroke-width="2" opacity=".32" fill="none"/>
<path d="M0 0h920v560H0z" fill="url(#grain)"/>
''' + dots + '''
<g><circle cx="159" cy="470" r="35" fill="#f14c5b"/><circle cx="148" cy="459" r="9" fill="#ff9c90" opacity=".73"/>
<circle cx="786" cy="488" r="23" fill="#89dd5b"/><circle cx="778" cy="481" r="6" fill="#d1ff91" opacity=".75"/>
<circle cx="658" cy="530" r="37" fill="#4a91e8"/><circle cx="645" cy="518" r="11" fill="#b8ddff" opacity=".65"/>
<circle cx="285" cy="528" r="21" fill="#ffc44b"/><circle cx="279" cy="521" r="5.5" fill="#fff9ae" opacity=".75"/>
<circle cx="393" cy="432" r="14" fill="#ac75ec"/><circle cx="388" cy="428" r="4" fill="#e5baff" opacity=".65"/></g>
</svg>'''

LEVELS = ['Modelled effect', 'Sales trend', 'Survey', 'Reach only', 'Archival']
LEVEL_NOTES = {
    'Modelled effect': 'A model estimates the effect against a baseline.',
    'Sales trend': 'Sales moved, but other causes are not separated out.',
    'Survey': 'People who saw it said something changed.',
    'Reach only': 'The number counts attention, not outcomes.',
    'Archival': 'The record shows the work existed and endured.',
}
MECHANISMS = [
    ('Demonstration', 'Stage the benefit so people can see it for themselves.'),
    ('Reframed weakness', 'Say the uncomfortable thing first and make it the point.'),
    ('Participation', 'Hand the audience a part to play and let them spread it.'),
    ('Exposing an assumption', 'Show people a judgement they did not know they held.'),
    ('Representation', 'Put people in the picture who were missing from it.'),
]
mech_names = [m for m, _ in MECHANISMS]
ERAS = ['1950s to 1980s', '1990s and 2000s', '2010s', '2020s']


def era(year):
    if year < 1990:
        return ERAS[0]
    if year < 2010:
        return ERAS[1]
    if year < 2020:
        return ERAS[2]
    return ERAS[3]


def strength_of(level):
    return len(LEVELS) - LEVELS.index(level)


def meter(level):
    strength = strength_of(level)
    bars = ''.join(f'<i class="{"on" if n < strength else ""}"></i>' for n in range(len(LEVELS)))
    return (f'<span class="meter s{strength}" role="img" aria-label="Evidence strength {strength} of {len(LEVELS)}: {e(level)}">'
            f'<span class="bars" aria-hidden="true">{bars}</span><span class="meter-label" aria-hidden="true">{e(level)}</span></span>')


cards = []
for i, c in enumerate(campaigns, 1):
    sources = '\n'.join(f'<li><a href="{e(url)}">{e(label)}</a></li>' for label, url in c['links'])
    creative = c['creative']
    primary_label, primary_url = c['impact_source']
    related_sources = f'<h3>Further sources</h3><ul class="sources">{sources}</ul>' if sources else ''
    legacy = c['stat_type'] == 'legacy'
    stat_tag = '<p class="stat-tag small">Legacy fact, not a result</p>' if legacy else ''
    cards.append(f'''<details id="{e(c['id'])}" class="case" data-mechanism="{e(c['mechanism'])}" data-evidence="{e(c['evidence_level'])}" data-era="{e(era(c['year']))}">
<summary>
<span class="case-number small">{i:02d}</span>
<span><span class="case-brand small">{e(c['brand'])} / {c['year']} / {e(c['mechanism'])}</span><span class="case-title">{e(c['title'])}</span><span class="case-hook">{e(c['hook'])}</span></span>
<span class="metric-cell{' legacy' if legacy else ''}"><span class="row-metric">{e(c['metric'])}</span><span class="row-label small">{e(c["metric_label"])}{' · legacy fact' if legacy else ''}</span>{meter(c['evidence_level'])}</span>
<span class="toggle" aria-hidden="true"></span>
</summary>
<div class="case-inner">
<div>
<p class="case-meta">{e(c['place'])} / {e(c['medium'])}</p>
<h3>The idea</h3><p>{e(c['idea'])}</p>
<h3>The lesson</h3><p>{e(c['lesson'])}</p>
<div class="memory take"><h3>My take</h3><p>{e(c['take'])}</p></div>
<div class="creative-record">
<h3>Original creative <span>{e(creative['medium'])}</span></h3>
<a href="{e(creative['url'])}">{e(creative['label'])}</a>
</div>
</div>
<aside class="proof" aria-label="Evidence">
<h3>{'Headline fact' if legacy else 'Impact'} <span>{e(c['kind'])}</span></h3>
<p class="proof-value">{e(c['metric'])}</p>
{stat_tag}
<p class="proof-metric">{e(c['measure'])}</p>
<div class="proof-strength"><span class="small">Evidence strength</span>{meter(c['evidence_level'])}<p>{e(LEVEL_NOTES[c['evidence_level']])}</p></div>
<p class="impact-citation"><span class="small">Source</span> <a href="{e(primary_url)}">{e(primary_label)}</a></p>
</aside>
</div>
<details class="full-case">
<summary><span>Read the full case</span><span class="toggle" aria-hidden="true"></span></summary>
<div class="full-inner">
<div>
<h3>The starting point</h3><p>{e(c['before'])}</p>
<h3>What changed</h3><p>{e(c['shift'])}</p>
<h3>Why it’s memorable</h3><p>{e(c['memorable'])}</p>
</div>
<div>
<h3>What the number can and can’t show</h3><p>{e(c['evidence'])}</p>
<h3>How to measure a similar idea</h3><p>{e(c['test'])}</p>
{related_sources}
</div>
</div>
</details>
</details>''')

ladder = []
for level in LEVELS:
    group = [c for c in campaigns if c['evidence_level'] == level]
    links = ', '.join(f'<a href="#{e(c["id"])}">{e(c["brand"])}</a>' for c in group)
    ladder.append(f'''<li class="s{strength_of(level)}"><span class="ladder-name">{meter(level)}</span>
<span class="ladder-count"><b>{len(group)}</b><span class="ladder-bar" style="--n:{len(group)}" aria-hidden="true"></span></span>
<span class="ladder-cases"><span class="ladder-note">{e(LEVEL_NOTES[level])}</span> {links}</span></li>''')

mech_cols = []
for name, note in MECHANISMS:
    items = ''.join(f'<li><a href="#{e(c["id"])}">{e(c["brand"])} <span>{c["year"]}</span></a></li>'
                    for c in sorted(campaigns, key=lambda c: c['year']) if c['mechanism'] == name)
    mech_cols.append(f'<div class="mech"><h3><button class="mech-pick" type="button" data-value="{e(name)}">{e(name)}</button></h3><p>{e(note)}</p><ul>{items}</ul></div>')

first, last = min(c['year'] for c in campaigns), max(c['year'] for c in campaigns)
span = last - first
ticks = ''.join(f'<span class="tick" style="--x:{(y - first) / span * 100:.2f}%">{y}</span>' for y in (1960, 1970, 1980, 1990, 2000, 2010, 2020))
dots, stacks = [], {}
for c in sorted(campaigns, key=lambda c: c['year']):
    stack = stacks.get(c['year'], 0)
    stacks[c['year']] = stack + 1
    dots.append(f'<a class="dot s{strength_of(c["evidence_level"])}" href="#{e(c["id"])}" data-id="{e(c["id"])}" style="--x:{(c["year"] - first) / span * 100:.2f}%;--y:{stack}" title="{e(c["brand"])}, {c["year"]}. {e(c["evidence_level"])}"><span class="sr">{e(c["brand"])}, {c["year"]}</span></a>')
timeline = f'<div class="timeline" role="group" aria-label="Campaigns by year, {first} to {last}">{"".join(dots)}<div class="axis" aria-hidden="true">{ticks}</div></div>'


def chips(group, values):
    out = [f'<button class="filter" type="button" data-group="{group}" data-value="All" aria-pressed="true">All</button>']
    out += [f'<button class="filter" type="button" data-group="{group}" data-value="{e(v)}" aria-pressed="false">{e(v)}</button>' for v in values]
    return ''.join(out)


filters = (f'<div class="filter-row" role="group" aria-label="Mechanism"><span class="small">Mechanism</span>{chips("mechanism", mech_names)}</div>'
           f'<div class="filter-row" role="group" aria-label="Evidence strength"><span class="small">Evidence</span>{chips("evidence", LEVELS)}</div>'
           f'<div class="filter-row" role="group" aria-label="Era"><span class="small">Era</span>{chips("era", ERAS)}</div>')
template = (root / 'page-template.html').read_text(encoding='utf-8')
screening_ids = ('sony-bravia', 'volvo-epic-split', 'old-spice', 'barbie-movie')
screening_notes = {
    'sony-bravia': ('colour', 'The soundtrack lets the colour do the talking.'),
    'volvo-epic-split': ('split', 'The precision is what makes the stunt possible.'),
    'old-spice': ('spice', 'Watch the eye contact as the sets change.'),
    'barbie-movie': ('pink', 'The film introduces a world the partnerships bring to life.'),
}
screenings = []
for case_id in screening_ids:
    c = next(entry for entry in campaigns if entry['id'] == case_id)
    colour, note = screening_notes[case_id]
    creative = c['creative']
    video = creative['url'].partition('https://www.youtube.com/watch?v=')[2]
    player = ''
    if video:
        player = f'<button class="play-film small" type="button" data-video="{e(video)}" data-title="{e(c["title"])}" hidden>Play here</button>'
    screenings.append(f'''<article class="screening">
<div class="film-frame {colour}">
<span class="small">{e(c['brand'])} / {c['year']}</span>
<h3>{e(c['title'])}</h3>
</div>
<div class="film-body">
<p>{e(note)}</p>
<div class="film-actions">
{player}<a href="{e(creative['url'])}">{'Watch on YouTube' if video else 'Watch at HAT'}</a>
<a href="#{case_id}">Read the case</a>
</div>
</div>
</article>''')
output = (template.replace('@@ART@@', art)
          .replace('@@CASES@@', '\n'.join(cards))
          .replace('@@SCREENINGS@@', '\n'.join(screenings))
          .replace('@@LADDER@@', '\n'.join(ladder))
          .replace('@@MECHANISMS@@', '\n'.join(mech_cols))
          .replace('@@TIMELINE@@', timeline)
          .replace('@@FILTERS@@', filters)
          .replace('@@COUNT@@', str(len(campaigns)))
          .replace('@@FIRST_YEAR@@', str(min(c['year'] for c in campaigns)))
          .replace('@@LAST_YEAR@@', str(max(c['year'] for c in campaigns))))
(root.parent / 'index.html').write_text(output, encoding='utf-8')
