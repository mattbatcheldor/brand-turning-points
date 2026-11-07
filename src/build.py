from html import escape
from pathlib import Path
import json

root = Path(__file__).resolve().parent
campaigns = json.loads((root / 'campaigns.json').read_text(encoding='utf-8'))
e = escape

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
output = (template.replace('@@CASES@@', '\n'.join(cards))
          .replace('@@SCREENINGS@@', '\n'.join(screenings))
          .replace('@@LADDER@@', '\n'.join(ladder))
          .replace('@@MECHANISMS@@', '\n'.join(mech_cols))
          .replace('@@TIMELINE@@', timeline)
          .replace('@@FILTERS@@', filters)
          .replace('@@COUNT@@', str(len(campaigns)))
          .replace('@@FIRST_YEAR@@', str(min(c['year'] for c in campaigns)))
          .replace('@@LAST_YEAR@@', str(max(c['year'] for c in campaigns))))
(root.parent / 'index.html').write_text(output, encoding='utf-8')
