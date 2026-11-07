from html import escape
from pathlib import Path
import json
import random

root = Path(__file__).resolve().parent
e = escape


def itv_art():
    # Stylised tile map of the 1994 ITV regions. Central is left dark: BT's control region.
    tile, gap = 64, 7
    regions = [
        ('Grampian', 3, 0), ('Scottish', 3, 1), ('Ulster', 1, 2), ('Border', 3, 2), ('Tyne Tees', 4, 2),
        ('Granada', 3, 3), ('Yorkshire', 4, 3), ('HTV', 2, 4), ('Central', 3, 4), ('Anglia', 4, 4),
        ('Westcountry', 2, 5), ('Meridian', 3, 5), ('London', 4, 5),
    ]
    ox, oy = 260, 26  # columns 1 to 4 span x 331 to 608, rows 0 to 5 span y 26 to 445, clear of the caption
    warm = ['#e9c46a', '#f1d58a', '#d9f55d', '#c7e36a', '#f4a259', '#efc56f']
    tiles = []
    random.seed(1994)
    for i, (name, col, row) in enumerate(regions):
        x = ox + col * (tile + gap)
        y = oy + row * (tile + gap)
        label_size = 11.5 if len(name) <= 8 else (10.5 if len(name) <= 10 else 8.6)
        if name == 'Central':
            tiles.append(
                f'<g><rect x="{x:.1f}" y="{y:.1f}" width="{tile}" height="{tile}" rx="6" fill="#14171f" stroke="#d9f55d" stroke-width="2" stroke-dasharray="5 4"/>'
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{tile}" height="{tile}" rx="6" fill="url(#hatch)"/>'
                f'<text x="{x + tile / 2:.1f}" y="{y + tile / 2 - 2:.1f}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="11.5" font-weight="bold" fill="#fffdf7">Central</text>'
                f'<text x="{x + tile / 2:.1f}" y="{y + tile / 2 + 12:.1f}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="8.5" letter-spacing="1.1" fill="#d9f55d">NO ADS</text></g>')
        else:
            fill = warm[i % len(warm)]
            arcs = ''.join(
                f'<path d="M{x + tile - 16:.1f} {y + 12 + k * 0:.1f} a{6 + k * 5} {6 + k * 5} 0 0 1 {6 + k * 5} {6 + k * 5}" fill="none" stroke="#171914" stroke-width="1.6" opacity="{.55 - k * .15:.2f}"/>'
                for k in range(3))
            tiles.append(
                f'<g><rect x="{x:.1f}" y="{y:.1f}" width="{tile}" height="{tile}" rx="6" fill="{fill}"/>{arcs}'
                f'<text x="{x + 6:.1f}" y="{y + tile - 8:.1f}" font-family="Arial, Helvetica, sans-serif" font-size="{label_size}" font-weight="bold" fill="#171914">{e(name)}</text></g>')
    static = '\n'.join(
        f'<rect x="{random.uniform(0, 920):.0f}" y="{random.uniform(0, 560):.0f}" width="{random.choice((1, 2, 3))}" height="1" fill="#fffdf7" opacity="{random.uniform(.05, .22):.2f}"/>'
        for _ in range(260))
    return f'''<svg viewBox="0 0 920 560" preserveAspectRatio="xMidYMid slice" role="img" aria-labelledby="art-title">
<title id="art-title">Stylised map of the 1994 ITV regions. Every region is lit except Central, which BT left without its advertising as a control.</title>
<defs>
  <linearGradient id="night" x2="0" y2="1" gradientUnits="objectBoundingBox"><stop stop-color="#1d2533"/><stop offset="1" stop-color="#2b2f3d"/></linearGradient>
  <pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0v8" stroke="#d9f55d" stroke-width="1.2" opacity=".28"/></pattern>
  <pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse"><path d="M0 3.5h4" stroke="#000" stroke-width="1" opacity=".22"/></pattern>
</defs>
<path d="M0 0h920v560H0z" fill="url(#night)"/>
{static}
{''.join(tiles)}
<g font-family="Arial, Helvetica, sans-serif" font-size="12" fill="#fffdf7">
<rect x="78" y="34" width="16" height="16" rx="3" fill="#e9c46a"/><text x="102" y="47">Campaign on air</text>
<rect x="78" y="60" width="16" height="16" rx="3" fill="#14171f" stroke="#d9f55d" stroke-width="1.5" stroke-dasharray="3 2"/><text x="102" y="73">Control region, no ads</text>
</g>
<path d="M0 0h920v560H0z" fill="url(#lines)"/>
</svg>'''



def receipt_art():
    # Editorial illustration: a till receipt of data trails whose barcode rises into a bar chart.
    mono = "'Courier New', Courier, monospace"
    lines = [
        ('BRAND TURNING POINTS', True), ('EDITION 03 / DATA FIRST', False), ('-' * 30, False),
        ("SEARCHES  'CHILD COUGH'     x3", False), ('ONLINE MOOD  HANGRY      -12%', False),
        ('2 WARM DAYS IN A ROW     ADS ON', False), ('SONGS PLAYED THIS YEAR   2,914', False),
        ('1 JAR MAYONNAISE  + RECIPE', False), ('LOYALTY PRICE   SAVED   1.20', False),
        ('-' * 30, False), ('TOTAL     ONE TURNING POINT', True),
    ]
    text = ''.join(f'<text x="252" y="{116 + i * 24}" font-family="{mono}" font-size="15" font-weight="{"bold" if bold else "normal"}" fill="#1d211b">{e(t)}</text>'
                   for i, (t, bold) in enumerate(lines))
    random.seed(3)
    bars, x = [], 252
    for i in range(30):
        w = random.choice((2, 3, 4, 6))
        h = 26 + (i / 29) ** 2.2 * 72
        colour = '#1d211b' if i < 18 else ('#557400' if i < 27 else '#d9f55d')
        bars.append(f'<rect x="{x}" y="{498 - h:.1f}" width="{w}" height="{h:.1f}" fill="{colour}"/>')
        x += w + 3.2
    teeth = ''.join(f'l-14 12-14-12' for _ in range(14))
    return f'''<svg viewBox="0 0 920 560" preserveAspectRatio="xMidYMid slice" role="img" aria-labelledby="art-title">
<title id="art-title">Illustration of a till receipt listing data trails, such as searches, online mood and songs played, whose barcode rises into a bar chart.</title>
<defs><linearGradient id="bg" x2="0" y2="1"><stop stop-color="#20302a"/><stop offset="1" stop-color="#12201b"/></linearGradient>
<filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="#000" flood-opacity=".45"/></filter></defs>
<path d="M0 0h920v560H0z" fill="url(#bg)"/>
<g transform="translate(46 4) scale(.9)"><g transform="rotate(-4 460 300)" filter="url(#sh)">
<path d="M222 40h400v470{teeth}z" fill="#fbf9f1"/>
{text}{''.join(bars)}
</g></g>
</svg>'''


def machine_art():
    # Editorial illustration: a prompt window whose answer is drawn half by a machine and half by hand.
    mono = "'Courier New', Courier, monospace"
    random.seed(4)
    dots = []
    for row in range(14):
        for col in range(18):
            x, y = 486 + col * 17, 150 + row * 17
            d = ((x - 640) ** 2 / 1.3 + (y - 262) ** 2) ** .5
            if d < 118 and random.random() > .08:
                size = 4 + (1 - d / 118) * 7
                colour = '#d9f55d' if d < 46 else ('#a5c31c' if d < 84 else '#557400')
                dots.append(f'<rect x="{x - size / 2:.1f}" y="{y - size / 2:.1f}" width="{size:.1f}" height="{size:.1f}" fill="{colour}"/>')
    return f'''<svg viewBox="0 0 920 560" preserveAspectRatio="xMidYMid slice" role="img" aria-labelledby="art-title">
<title id="art-title">Illustration of a prompt window. The prompt asks for a brand turning point, and the answer is drawn half in machine pixels and half in a hand-drawn line.</title>
<defs><linearGradient id="bg" x2="0" y2="1"><stop stop-color="#1d2420"/><stop offset="1" stop-color="#101512"/></linearGradient>
<filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="#000" flood-opacity=".45"/></filter></defs>
<path d="M0 0h920v560H0z" fill="url(#bg)"/>
<g transform="translate(46 22) scale(.9)"><g transform="rotate(-2 460 280)" filter="url(#sh)">
<rect x="150" y="50" width="620" height="440" rx="10" fill="#fbf9f1"/>
<path d="M150 60a10 10 0 0 1 10-10h600a10 10 0 0 1 10 10v26H150z" fill="#1d211b"/>
<circle cx="174" cy="68" r="5" fill="#d9f55d"/><circle cx="192" cy="68" r="5" fill="#fbf9f1" opacity=".5"/><circle cx="210" cy="68" r="5" fill="#fbf9f1" opacity=".3"/>
<text x="240" y="73" font-family="{mono}" font-size="13" fill="#fbf9f1">EDITION 04 / MACHINE FIRST</text>
<text x="178" y="126" font-family="{mono}" font-size="15" fill="#1d211b">&gt; draw a brand turning point</text>
<rect x="452" y="114" width="9" height="16" fill="#557400"/>
<line x1="178" y1="146" x2="742" y2="146" stroke="#d3d1c5" stroke-width="1.5"/>
{''.join(dots)}
<path d="M640 142c-70 4-122 56-120 122s54 116 120 118" fill="none" stroke="#1d211b" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="1 0"/>
<path d="M600 236c8-10 22-10 28 0M652 236c8-10 22-10 28 0M604 296c22 22 56 22 76 0" fill="none" stroke="#1d211b" stroke-width="3.5" stroke-linecap="round"/>
<text x="178" y="200" font-family="{mono}" font-size="12" fill="#6d6f66">MACHINE</text>
<text x="178" y="220" font-family="{mono}" font-size="12" fill="#6d6f66">OR HAND?</text>
<text x="178" y="458" font-family="{mono}" font-size="13" fill="#1d211b">ANSWER: PEOPLE NOTICE THE DIFFERENCE</text>
</g></g>
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
    ('Owning a moment', 'Tie the brand to an occasion people already keep.'),
]
ROLES = ['Data as aim', 'Data as the show', 'Data as the claim', 'Data as the product']
# Editions that sort cases by a role (03 by data, 04 by machine) set these labels; the defaults are Edition 03's.
ROLE_DEFAULTS = {'roles': ROLES, 'role_label': 'Data use', 'role_aria': 'How data was used', 'source_label': 'The data'}
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


def slug(text):
    return text.lower().replace(' ', '-')


def campaign_image(c, placement, prefix=''):
    image = c.get('image')
    if not image:
        return ''
    fit = ' image-contain' if image.get('contain') else ''
    return (f'<span class="{placement}{fit}"><img src="{e(prefix + image["src"])}" '
            f'alt="{e(image["alt"])}" width="{image["width"]}" height="{image["height"]}" '
            'loading="lazy" decoding="async"></span>')


def proof_tile(c):
    # Used where a case has no licensed image: a type tile that names how the effect was proved,
    # or, in a data edition, how the data was used and where it came from.
    if c.get('data_role'):
        cls, label = f'r-{slug(c["data_role"])}', f'{c["data_role"]} / {c["data_source"]}'
    else:
        cls, label = f'm-{slug(c["mechanism"])}', c.get('method') or c['evidence_level']
    return (f'<span class="case-thumbnail proof-tile {cls}" aria-hidden="true">'
            f'<span class="tile-year">{c["year"]}</span><span class="tile-method">{e(label)}</span></span>')


def render_cards(campaigns, notes, test_heading, prefix='', source_label='The data'):
    cards = []
    for i, c in enumerate(campaigns, 1):
        sources = '\n'.join(f'<li><a href="{e(url)}">{e(label)}</a></li>' for label, url in c['links'])
        creative = c['creative']
        image = c.get('image')
        primary_label, primary_url = c['impact_source']
        related_sources = f'<h3>Further sources</h3><ul class="sources">{sources}</ul>' if sources else ''
        legacy = c['stat_type'] == 'legacy'
        stat_tag = '<p class="stat-tag small">Legacy fact, not a result</p>' if legacy else ''
        credit = f'\n<p class="case-credit small">{e(c["credit"])}</p>' if c.get('credit') else ''
        method = f'\n<p class="method-tag"><span class="small">How it was proved</span> {e(c["method"])}</p>' if c.get('method') else ''
        if creative.get('url'):
            creative_link = f'<a href="{e(creative["url"])}">{e(creative["label"])}</a>'
        else:
            creative_link = f'<p class="no-copy">{e(creative["label"])}</p>'
        image_credit = f'\n<p class="image-credit">Image: <a href="{e(image["source"])}">{e(image["credit"])}</a></p>' if image else ''
        thumbnail = campaign_image(c, 'case-thumbnail', prefix) or proof_tile(c)
        role_attr = f' data-role="{e(c["data_role"])}"' if c.get('data_role') else ''
        data_line = ''
        if c.get('data_source'):
            data_line = f'<span class="case-data"><strong>{e(c["data_role"])}</strong> · {e(c["data_source"])}</span>'
            method += f'\n<p class="method-tag"><span class="small">{e(source_label)}</span> {e(c["data_source"])}</p>'
        cards.append(f'''<details id="{e(c['id'])}" class="case" data-mechanism="{e(c['mechanism'])}" data-evidence="{e(c['evidence_level'])}" data-era="{e(era(c['year']))}"{role_attr}>
<summary>
<span class="case-number small">{i:02d}</span>
{thumbnail}
<span class="case-heading"><span class="case-brand small">{e(c['brand'])} / {c['year']} / {e(c['mechanism'])}</span><span class="case-title">{e(c['title'])}</span><span class="case-hook">{e(c['hook'])}</span>{data_line}</span>
<span class="metric-cell{' legacy' if legacy else ''}"><span class="row-metric">{e(c['metric'])}</span><span class="row-label small">{e(c["metric_label"])}{' · legacy fact' if legacy else ''}</span>{meter(c['evidence_level'])}</span>
<span class="toggle" aria-hidden="true"></span>
</summary>
<div class="case-inner">
<div>
<p class="case-meta">{e(c['place'])} / {e(c['medium'])}</p>{credit}
<h3>The idea</h3><p>{e(c['idea'])}</p>
<h3>The lesson</h3><p>{e(c['lesson'])}</p>
<div class="memory take"><h3>My take</h3><p>{e(c['take'])}</p></div>
<div class="creative-record">
<h3>{e(creative.get('heading', 'Original creative'))} <span>{e(creative['medium'])}</span></h3>
{creative_link}{image_credit}
</div>
</div>
<aside class="proof" aria-label="Evidence">
<h3>{'Headline fact' if legacy else 'Impact'} <span>{e(c['kind'])}</span></h3>
<p class="proof-value">{e(c['metric'])}</p>
{stat_tag}
<p class="proof-metric">{e(c['measure'])}</p>{method}
<div class="proof-strength"><span class="small">Evidence strength</span>{meter(c['evidence_level'])}<p>{e(notes[c['evidence_level']])}</p></div>
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
<h3>{e(test_heading)}</h3><p>{e(c['test'])}</p>
{related_sources}
</div>
</div>
</details>
</details>''')
    return cards


def render_ladder(campaigns, notes, compare=None):
    ladder = []
    for level in LEVELS:
        group = [c for c in campaigns if c['evidence_level'] == level]
        links = ', '.join(f'<a href="#{e(c["id"])}">{e(c["brand"])}</a>' for c in group)
        if compare is None:
            ladder.append(f'''<li class="s{strength_of(level)}"><span class="ladder-name">{meter(level)}</span>
<span class="ladder-count"><b>{len(group)}</b><span class="ladder-bar" style="--n:{len(group)}" aria-hidden="true"></span></span>
<span class="ladder-cases"><span class="ladder-note">{e(notes[level])}</span> {links}</span></li>''')
        else:
            before = sum(1 for c in compare['campaigns'] if c['evidence_level'] == level)
            ladder.append(f'''<li class="s{strength_of(level)} compare-row"><span class="ladder-name">{meter(level)}</span>
<span class="ladder-pair"><span class="pair-row now"><b>{len(group)}</b><span class="ladder-bar" style="--n:{len(group)}" aria-hidden="true"></span><span class="sr">in this edition</span></span><span class="pair-row then"><b>{before}</b><span class="ladder-bar" style="--n:{before}" aria-hidden="true"></span><span class="sr">in {e(compare['label'])}</span></span></span>
<span class="ladder-cases"><span class="ladder-note">{e(notes[level])}</span> {links or '<span class="none">None in this edition</span>'}</span></li>''')
    return ladder


def render_role_grid(campaigns, all_roles=ROLES, role_aria='How data was used'):
    roles = [r for r in all_roles if any(c.get('data_role') == r for c in campaigns)]
    if not roles:
        return ''
    levels = [l for l in LEVELS if any(c['evidence_level'] == l for c in campaigns)]
    cells = ['<span class="rg-corner" aria-hidden="true"></span>'] + [f'<span class="rg-head">{e(l)}</span>' for l in levels]
    brands = [c['brand'] for c in campaigns]
    def chip_label(c):
        # Name the year too when a brand appears more than once, so two IBM chips can be told apart.
        return f'{c["brand"]} {c["year"]}' if brands.count(c['brand']) > 1 else c['brand']
    for r in roles:
        cells.append(f'<span class="rg-role">{e(r)}</span>')
        for l in levels:
            group = [c for c in campaigns if c.get('data_role') == r and c['evidence_level'] == l]
            chips_html = ''.join(f'<a class="rg-chip s{strength_of(l)}" href="#{e(c["id"])}">{e(chip_label(c))}</a>' for c in group)
            cells.append(f'<span class="rg-cell{" empty" if not group else ""}" data-level="{e(l)}">{chips_html}</span>')
    return (f'<div class="role-grid" style="--cols:{len(levels)}" role="group" aria-label="Cases by {e(role_aria.lower())} and by evidence strength">'
            + ''.join(cells) + '</div>')


def series_modelled(edition):
    parts = []
    for other in EDITIONS:
        data = root / other['data']
        if not data.exists():
            continue
        n = sum(1 for c in json.loads(data.read_text(encoding='utf-8')) if c['evidence_level'] == 'Modelled effect')
        parts.append(f'{n} here' if other is edition else f'{n} in Edition {other["number"]}')
    return ', '.join(parts[:-1]) + ' and ' + parts[-1] if len(parts) > 1 else (parts[0] if parts else '')


def present_mechanisms(campaigns):
    return [(m, note) for m, note in MECHANISMS if any(c['mechanism'] == m for c in campaigns)]


def render_mechanisms(campaigns):
    cols = []
    for name, note in present_mechanisms(campaigns):
        items = ''.join(f'<li><a href="#{e(c["id"])}">{e(c["brand"])} <span>{c["year"]}</span></a></li>'
                        for c in sorted(campaigns, key=lambda c: c['year']) if c['mechanism'] == name)
        cols.append(f'<div class="mech"><h3><button class="mech-pick" type="button" data-value="{e(name)}">{e(name)}</button></h3><p>{e(note)}</p><ul>{items}</ul></div>')
    return cols


def render_timeline(campaigns):
    first, last = min(c['year'] for c in campaigns), max(c['year'] for c in campaigns)
    span = last - first
    decades = [y for y in range((first // 10 + 1) * 10, last + 1, 10)]
    ticks = ''.join(f'<span class="tick" style="--x:{(y - first) / span * 100:.2f}%">{y}</span>' for y in decades)
    dots, stacks = [], {}
    for c in sorted(campaigns, key=lambda c: c['year']):
        stack = stacks.get(c['year'], 0)
        stacks[c['year']] = stack + 1
        dots.append(f'<a class="dot s{strength_of(c["evidence_level"])}" href="#{e(c["id"])}" data-id="{e(c["id"])}" style="--x:{(c["year"] - first) / span * 100:.2f}%;--y:{stack}" title="{e(c["brand"])}, {c["year"]}. {e(c["evidence_level"])}"><span class="sr">{e(c["brand"])}, {c["year"]}</span></a>')
    return f'<div class="timeline" role="group" aria-label="Campaigns by year, {first} to {last}">{"".join(dots)}<div class="axis" aria-hidden="true">{ticks}</div></div>'


def chips(group, values):
    out = [f'<button class="filter" type="button" data-group="{group}" data-value="All" aria-pressed="true">All</button>']
    out += [f'<button class="filter" type="button" data-group="{group}" data-value="{e(v)}" aria-pressed="false">{e(v)}</button>' for v in values]
    return ''.join(out)


def render_filters(campaigns, all_roles=ROLES, role_label='Data use', role_aria='How data was used'):
    mech_names = [m for m, _ in present_mechanisms(campaigns)]
    levels = [l for l in LEVELS if any(c['evidence_level'] == l for c in campaigns)]
    eras = [x for x in ERAS if any(era(c['year']) == x for c in campaigns)]
    roles = [r for r in all_roles if any(c.get('data_role') == r for c in campaigns)]
    role_row = f'<div class="filter-row" role="group" aria-label="{e(role_aria)}"><span class="small">{e(role_label)}</span>{chips("role", roles)}</div>' if roles else ''
    return role_row + (f'<div class="filter-row" role="group" aria-label="Mechanism"><span class="small">Mechanism</span>{chips("mechanism", mech_names)}</div>'
            f'<div class="filter-row" role="group" aria-label="Evidence strength"><span class="small">Evidence</span>{chips("evidence", levels)}</div>'
            f'<div class="filter-row" role="group" aria-label="Era"><span class="small">Era</span>{chips("era", eras)}</div>')


def render_screenings(campaigns, screening, prefix=''):
    screenings = []
    for case_id, note, drawn in screening:
        c = next(entry for entry in campaigns if entry['id'] == case_id)
        creative = c['creative']
        url = creative.get('screening_url', creative['url'])
        video = url.partition('https://www.youtube.com/watch?v=')[2]
        player = ''
        if video:
            player = f'<button class="play-film small" type="button" data-video="{e(video)}" data-title="{e(c["title"])}" hidden>Play here</button>'
        frame = campaign_image(c, 'film-frame', prefix) or f'<span class="film-frame drawn {drawn}" aria-hidden="true"></span>'
        screenings.append(f'''<article class="screening">
{frame}
<div class="film-body">
<div class="film-heading"><p class="small">{e(c['brand'])} / {c['year']}</p><h3>{e(c['title'])}</h3></div>
<p>{e(note)}</p>
<div class="film-actions">
{player}<a href="{e(url)}">{'Watch on YouTube' if video else 'Watch at HAT'}</a>
<a href="#{case_id}">Read the case</a>
</div>
</div>
</article>''')
    return screenings


def relative_dir(from_output, to_output):
    import posixpath
    here = posixpath.dirname(from_output) or '.'
    there = posixpath.dirname(to_output) or '.'
    rel = posixpath.relpath(there, here)
    return '' if rel == '.' else rel + '/'


def render_edition_nav(edition):
    links = []
    for other in EDITIONS:
        if not (root / other['data']).exists():
            continue
        label = f'<span class="sr">Edition </span>{other["number"]}'
        if other is edition:
            links.append(f'<a href="#top" aria-current="page" title="Edition {other["number"]}{", " + other["name"] if other.get("name") else ""}">{label}</a>')
        else:
            href = relative_dir(edition['output'], other['output']) or './'
            links.append(f'<a href="{href}" title="Edition {other["number"]}{", " + other["name"] if other.get("name") else ""}">{label}</a>')
    return f'<span class="edition-nav"><span class="edition-nav-label" aria-hidden="true">Editions</span>{"".join(links)}</span>'


def write_forwarding_page(edition):
    alias = edition.get('alias')
    if not alias:
        return None
    target = relative_dir(alias, edition['output']) or './'
    page = f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Brand Turning Points | Edition {edition["number"]}{", " + edition["name"] if edition.get("name") else ""}</title>
<link rel="canonical" href="{target}">
<meta http-equiv="refresh" content="0; url={target}">
<meta name="robots" content="noindex">
</head>
<body>
<p><a href="{target}">Open Brand Turning Points, Edition {edition["number"]}</a></p>
<script>location.replace({json.dumps(target)} + location.hash);</script>
</body>
</html>
'''
    out = root.parent / alias
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding='utf-8')
    return out


def build(edition):
    campaigns = json.loads((root / edition['data']).read_text(encoding='utf-8'))
    notes = dict(LEVEL_NOTES, **edition.get('level_notes', {}))
    prefix = edition.get('asset_prefix', '')
    compare = None
    if edition.get('compare'):
        compare = {'label': edition['compare']['label'],
                   'campaigns': json.loads((root / edition['compare']['data']).read_text(encoding='utf-8'))}
    template = (root / edition['template']).read_text(encoding='utf-8')
    css = (root / 'site.css').read_text(encoding='utf-8')
    js = (root / 'site.js').read_text(encoding='utf-8')
    r = dict(ROLE_DEFAULTS, **edition.get('roles', {}))
    modelled = sum(1 for c in campaigns if c['evidence_level'] == 'Modelled effect')
    compare_modelled = sum(1 for c in (compare or {}).get('campaigns', []) if c['evidence_level'] == 'Modelled effect')
    output = (template.replace('@@CSS@@\n', css)
              .replace('@@JS@@\n', js)
              .replace('@@ART@@', edition['art']() if edition.get('art') else '')
              .replace('@@CASES@@', '\n'.join(render_cards(campaigns, notes, edition['test_heading'], prefix, r['source_label'])))
              .replace('@@SCREENINGS@@', '\n'.join(render_screenings(campaigns, edition['screening'], prefix)))
              .replace('@@LADDER@@', '\n'.join(render_ladder(campaigns, notes, compare)))
              .replace('@@MECHANISMS@@', '\n'.join(render_mechanisms(campaigns)))
              .replace('@@TIMELINE@@', render_timeline(campaigns))
              .replace('@@FILTERS@@', render_filters(campaigns, r['roles'], r['role_label'], r['role_aria']))
              .replace('@@MODELLED@@', str(modelled))
              .replace('@@COMPARE_MODELLED@@', str(compare_modelled))
              .replace('@@EDITION_NAV@@', render_edition_nav(edition))
              .replace('@@ROLE_GRID@@', render_role_grid(campaigns, r['roles'], r['role_aria']))
              .replace('@@SERIES_MODELLED@@', series_modelled(edition))
              .replace('@@COUNT@@', str(len(campaigns)))
              .replace('@@FIRST_YEAR@@', str(min(c['year'] for c in campaigns)))
              .replace('@@LAST_YEAR@@', str(max(c['year'] for c in campaigns))))
    out = root.parent / edition['output']
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(output, encoding='utf-8')
    return out


# The series convention: number every edition with two digits and give it three things.
#   src/campaigns-NN.json      the cases
#   src/page-template-NN.html  the page copy
#   edition-NN/index.html      the published page (Edition 01 also sits on the home page)
# Add an entry below and run `python3 src/build.py`. The editions switcher in the menu updates itself.
EDITIONS = [
    {
        # Edition 01 lives on the home page. edition-01/ forwards there, so every edition has an edition-NN/ address.
        'number': '01',
        'name': 'Fame first',
        'data': 'campaigns-01.json',
        'template': 'page-template-01.html',
        'output': 'index.html',
        'alias': 'edition-01/index.html',
        'test_heading': 'How to measure a similar idea',
        'screening': (
            ('sony-bravia', 'The soundtrack lets the colour do the talking.', None),
            ('volvo-epic-split', 'The precision is what makes the stunt possible.', None),
            ('old-spice', 'Watch the eye contact as the sets change.', None),
            ('barbie-movie', 'The film introduces a world the partnerships bring to life.', None),
        ),
    },
    {
        'number': '02',
        'name': 'Proof first',
        'data': 'campaigns-02.json',
        'template': 'page-template-02.html',
        'output': 'edition-02/index.html',
        'asset_prefix': '../',
        'art': itv_art,
        'test_heading': 'How the proof was built',
        'level_notes': {'Modelled effect': 'A model or a control region estimates the effect against a baseline.'},
        'compare': {'label': 'Edition 01', 'data': 'campaigns-01.json'},
        'screening': (
            ('dft-drink-drive', 'Fifty years of films in under two minutes. Watch the target change.', 'road'),
            ('specsavers-shouldve', 'A mistake, a beat, then the line.', 'sheep'),
            ('john-lewis-long-wait', 'Watch where the boy is looking on Christmas morning.', 'wait'),
            ('spies-do-it-for-denmark', 'Notice how long it plays the joke straight.', 'denmark'),
        ),
    },
    {
        'number': '03',
        'name': 'Data first',
        'data': 'campaigns-03.json',
        'template': 'page-template-03.html',
        'output': 'edition-03/index.html',
        'asset_prefix': '../',
        'art': receipt_art,
        'test_heading': 'How the proof was built',
        'level_notes': {
            'Modelled effect': 'A model or a control group estimates the effect against a baseline.',
            'Sales trend': 'Sales or behaviour moved, but other causes are not separated out.',
        },
        'screening': (
            ('spotify-wrapped', 'Spotify goes behind the scenes of its 2020 recap, from the data to the cards people share.', 'cards'),
            ('british-airways-look-up', 'One plane, one billboard and a child pointing at the sky.', 'sky'),
            ('hellmanns-recipe-receipt', 'Watch the till do the cooking.', 'till'),
            ('snickers-hungerithm', 'Notice who is setting the price.', 'mood'),
        ),
    },
    {
        'number': '04',
        'name': 'Machine first',
        'data': 'campaigns-04.json',
        'template': 'page-template-04.html',
        'output': 'edition-04/index.html',
        'asset_prefix': '../',
        'art': machine_art,
        'test_heading': 'How the proof was built',
        'level_notes': {
            'Modelled effect': 'A model estimates what the work added against a baseline.',
            'Survey': 'A pre-test or a panel said people liked it.',
            'Archival': 'The record shows what happened, not what it earned.',
        },
        'roles': {
            'roles': ['Machine as the show', 'Machine as the maker', 'Machine behind the scenes'],
            'role_label': 'Machine',
            'role_aria': 'What the machine did',
            'source_label': 'The machine',
        },
        'screening': (
            ('ibm-watson-jeopardy', 'IBM’s own account of building a machine for a quiz show. Notice how much rides on one night of television.', 'quiz'),
            ('cadbury-not-just-an-ad', 'Listen for the shop names. Every version was different.', 'shop'),
            ('ing-next-rembrandt', 'Watch how long it takes to get to the brushstrokes.', 'canvas'),
            ('dove-the-code', 'The prompts are simple. Watch the faces of the women reading the results.', 'prompt'),
        ),
    },
]

if __name__ == '__main__':
    import sys
    wanted = sys.argv[1:]
    for edition in EDITIONS:
        if wanted and edition['output'] not in wanted:
            continue
        if not (root / edition['data']).exists():
            continue
        print('Built', build(edition).relative_to(root.parent))
        forwarding = write_forwarding_page(edition)
        if forwarding:
            print('Built', forwarding.relative_to(root.parent), '(forwards to', edition['output'] + ')')
