const filters = document.querySelector('#filters');
const search = document.querySelector('#search');
const result = document.querySelector('#result');
const empty = document.querySelector('#empty');
const buttons = Array.from(document.querySelectorAll('.filter'));
const cases = Array.from(document.querySelectorAll('.case'));
const dots = Array.from(document.querySelectorAll('.dot'));
const selected = {mechanism: 'All', evidence: 'All', era: 'All'};

function normalise(text) {
  return text.toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g, '')
    .replace(/['’]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
}

function updateArchive() {
  const terms = normalise(search.value).split(' ').filter(Boolean);
  let count = 0;
  for (const entry of cases) {
    const matchesFilter = Object.keys(selected).every(group => selected[group] === 'All' || entry.dataset[group] === selected[group]);
    const text = normalise(entry.textContent);
    entry.hidden = !(matchesFilter && terms.every(term => text.includes(term)));
    if (!entry.hidden) count += 1;
  }
  for (const dot of dots) {
    const entry = document.getElementById(dot.dataset.id);
    dot.classList.toggle('out', entry.hidden);
  }
  for (const button of buttons) {
    button.setAttribute('aria-pressed', String(selected[button.dataset.group] === button.dataset.value));
  }
  result.textContent = count === 1 ? '1 campaign' : count + ' campaigns';
  empty.hidden = count !== 0;
}

function resetFilters() {
  for (const group of Object.keys(selected)) selected[group] = 'All';
  search.value = '';
  updateArchive();
}

function openLinkedCase(hash) {
  const entry = cases.find(item => '#' + item.id === hash);
  if (!entry) return;
  if (entry.hidden) resetFilters();
  entry.open = true;
  entry.scrollIntoView({block:'start'});
}

filters.hidden = false;
for (const button of buttons) {
  button.addEventListener('click', () => {
    selected[button.dataset.group] = button.dataset.value;
    updateArchive();
  });
}
for (const pick of document.querySelectorAll('.mech-pick')) {
  pick.addEventListener('click', () => {
    resetFilters();
    selected.mechanism = pick.dataset.value;
    updateArchive();
    document.querySelector('#archive').scrollIntoView({block:'start'});
  });
}
search.addEventListener('input', updateArchive);
window.addEventListener('hashchange', () => openLinkedCase(location.hash));
for (const link of document.querySelectorAll('main a[href^="#"]:not(.skip)')) {
  link.addEventListener('click', event => {
    if (location.hash === event.currentTarget.hash) openLinkedCase(location.hash);
  });
}
openLinkedCase(location.hash);

const player = document.querySelector('.film-player');
const filmScreen = document.querySelector('#film-screen');
const filmTitle = document.querySelector('#film-title');
const filmOriginal = document.querySelector('#film-original');
let filmTrigger;
if (/^https?:$/.test(location.protocol) && typeof player.showModal === 'function') {
  for (const trigger of document.querySelectorAll('.play-film')) {
    trigger.hidden = false;
    trigger.addEventListener('click', () => {
      filmTrigger = trigger;
      const {video, title} = trigger.dataset;
      const iframe = document.createElement('iframe');
      iframe.title = title + ' on YouTube';
      iframe.src = 'https://www.youtube-nocookie.com/embed/' + video;
      iframe.allow = 'encrypted-media; picture-in-picture; fullscreen';
      iframe.referrerPolicy = 'strict-origin-when-cross-origin';
      iframe.allowFullscreen = true;
      filmTitle.textContent = title;
      filmOriginal.href = 'https://www.youtube.com/watch?v=' + video;
      filmScreen.replaceChildren(iframe);
      player.showModal();
    });
  }
  player.addEventListener('close', () => {
    filmScreen.replaceChildren();
    filmTrigger?.focus();
  });
}
