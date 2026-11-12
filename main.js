/* TTC Imperial Hotel Huế — khám phá: tòa nhà → mặt bằng → ảnh phòng. Không dùng thư viện ngoài. */

/* ------------------------------------------------------------------ */
/* Nội dung — sửa ở đây khi có số liệu chính thức                       */
/* ------------------------------------------------------------------ */
const COMMON = ['Sàn gỗ cao cấp', 'Đồ gỗ chạm trổ hoa văn truyền thống, cảm hứng triều Nguyễn',
  'TV truyền hình cáp, tủ lạnh, két an toàn', 'Bàn làm việc, bình đun nước, dụng cụ pha trà/cà phê, áo choàng tắm'];

// spots: id → [nhãn, ảnh, loại ảnh]. Loại 'real' = ảnh thật của khách sạn, 'ai' = ảnh minh họa tạo bằng AI.
// still: ảnh mặt bằng chân thật (một góc). at: vị trí điểm bấm trên ảnh đó (tỉ lệ 0–1) khi ảnh không cùng góc với khung Blender.
const ROOMS = {
  deluxe: {
    name: 'Deluxe', still: 'assets/plans/deluxe.jpg', sub: 'Double / Twin', area: '36 m²', count: '168 phòng',
    desc: 'Không gian phòng ngủ mở với 1 giường đôi lớn hoặc 2 giường đơn, bàn làm việc, khu vực ghế ngồi thư giãn và phòng tắm riêng biệt có buồng tắm đứng. Một số phòng có hướng nhìn ra phố hoặc sông Hương.',
    spots: { bedroom: ['Phòng ngủ', 'assets/photos/deluxe.jpg', 'real'], window: ['Góc trà bên cửa sổ'], bath: ['Phòng tắm · buồng tắm đứng'] },
  },
  junior: {
    name: 'Junior Suite', still: 'assets/plans/junior.jpg', sub: '', area: '46 m²', count: '20 phòng',
    desc: 'Không gian rộng hơn gồm phòng ngủ 01 giường đôi, khu vực phòng khách nhỏ bên trong phòng và phòng tắm cao cấp được trang bị thêm bồn tắm nằm.',
    spots: { bedroom: ['Phòng ngủ', 'assets/photos/junior-bedroom.jpg', 'ai'], lounge: ['Góc tiếp khách'], bath: ['Phòng tắm · bồn tắm nằm'] },
  },
  imperial: {
    name: 'Imperial Suite', still: 'assets/plans/imperial.jpg', sub: '', area: '80 m²', count: '',
    desc: 'Phòng khách riêng biệt bài trí theo lối cổ điển hoàng gia, phòng ngủ lớn và phòng tắm rộng có bồn tắm nằm, cùng tầm nhìn bao quát hướng sông Hương.',
    spots: { living: ['Phòng khách', 'assets/photos/suite-living.jpg', 'real'], window: ['Góc ngồi bên cửa sổ', 'assets/photos/suite-lounge.jpg', 'real'], dining: ['Bàn ăn'], bedroom: ['Phòng ngủ lớn'], bath: ['Phòng tắm · bồn tắm nằm'] },
  },
  presidential: {
    name: 'Grand Presidential Suite', still: 'assets/plans/presidential.jpg', sub: '', area: '160 m²', count: '1 phòng',
    desc: 'Quy mô lớn gồm 1 phòng khách sang trọng, phòng ngủ chính và phòng tắm lớn có bồn tắm. Hướng nhìn toàn cảnh ra sông Hương, cầu Trường Tiền và núi Ngự Bình.',
    at: { living: [0.36, 0.5], dining: [0.44, 0.66], bedroom: [0.62, 0.33], bath: [0.74, 0.47] },
    spots: { living: ['Phòng khách', 'assets/photos/suite-sunset.jpg', 'real'], dining: ['Phòng ăn'], bedroom: ['Phòng ngủ chính'], bath: ['Phòng tắm lớn'] },
  },
};
const KIND = { real: 'ảnh thật', ai: 'ảnh minh họa' };

// Phân bổ tầng là GIẢ ĐỊNH để trình diễn — thay bằng sơ đồ thật của khách sạn.
const FLOOR_ROOM = f => (f <= 12 ? 'deluxe' : f <= 14 ? 'junior' : f === 15 ? 'imperial' : 'presidential');
const LOBBY = { title: 'Sảnh đón', eyebrow: 'Khối đế · ảnh thật', photo: 'assets/photos/lobby.jpg' };

/* Vùng từng tầng trên ảnh tòa nhà (assets/hero/tower.jpg, 1792×2400), đo trên khối tháp chính.
   y là mép trên/dưới của tầng ở mặt trước; mặt bên trái nghiêng theo phối cảnh. */
const HERO = { w: 1792, h: 2400, base: 1590 };
const FLOOR_Y = { 5: [1505, 1590], 6: [1418, 1505], 7: [1331, 1418], 8: [1244, 1331], 9: [1157, 1244], 10: [1070, 1157],
  11: [983, 1070], 12: [896, 983], 13: [809, 896], 14: [720, 809], 15: [575, 720], 16: [460, 575] };
const TOWER_FLOORS = Object.keys(FLOOR_Y).map(Number);
function floorPoly(f) {
  const [t, b] = FLOOR_Y[f];
  const crown = f >= 15;
  const xl = crown ? 380 : 350, xc = crown ? 590 : 600, xr = crown ? 870 : 900;
  const lean = y => y + 0.052 * (HERO.base - y);            // mép trái thấp dần theo phối cảnh
  return [[xl, lean(t)], [xc, t], [xr, t], [xr, b], [xc, b], [xl, lean(b)]];
}
const LOBBY_POLY = [[250, 1600], [1560, 1560], [1700, 2060], [1100, 2200], [250, 2130]];

/* ------------------------------------------------------------------ */
const $ = id => document.getElementById(id);
const body = document.body;
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
const wait = ms => new Promise(r => setTimeout(r, reduceMotion ? 1 : ms));
async function veil(on) { $('veil').classList.toggle('on', on); await wait(460); }
let busy = false;

/* ========================= Màn tòa nhà ========================= */
const heroBox = $('heroBox'), heroSvg = $('heroSvg');
const SVGNS = 'http://www.w3.org/2000/svg';
const bands = new Map();

function floorLabel(id) {
  if (id === 'lobby') return ['Khối đế', 'Sảnh đón · ảnh thật'];
  const r = ROOMS[FLOOR_ROOM(id)];
  return [`Tầng ${id}`, `${r.name} · ${r.area}`];
}
function highlight(id) {
  bands.forEach((el, k) => el.classList.toggle('on', k === id));
  document.querySelectorAll('.rail button').forEach(b => b.classList.toggle('on', b.dataset.floor === String(id)));
}
function buildTower() {
  heroSvg.setAttribute('viewBox', `0 0 ${HERO.w} ${HERO.h}`);
  const add = (id, pts) => {
    const p = document.createElementNS(SVGNS, 'polygon');
    p.setAttribute('points', pts.map(q => q.map(v => v.toFixed(1)).join(',')).join(' '));
    p.setAttribute('class', 'band');
    const [a, t] = floorLabel(id);
    p.addEventListener('pointerenter', e => { if (e.pointerType !== 'touch' && !busy) { highlight(id); showTip(e, a, t); } });
    p.addEventListener('pointermove', e => { if (e.pointerType !== 'touch' && !busy) showTip(e, a, t); });
    p.addEventListener('pointerleave', () => { highlight(null); $('tip').hidden = true; });
    p.addEventListener('click', () => enterFloor(id));
    heroSvg.appendChild(p); bands.set(id, p);
  };
  TOWER_FLOORS.forEach(f => add(f, floorPoly(f)));
  add('lobby', LOBBY_POLY);

  [...TOWER_FLOORS].reverse().concat(['lobby']).forEach(id => {
    const b = document.createElement('button');
    b.dataset.floor = id;
    const [a, t] = floorLabel(id);
    b.innerHTML = `<span class="t">${t}</span><span>${id === 'lobby' ? 'Sảnh' : id}</span>`;
    b.setAttribute('aria-label', `${a}: ${t}`);
    b.onmouseenter = b.onfocus = () => highlight(id);
    b.onmouseleave = b.onblur = () => highlight(null);
    b.onclick = () => enterFloor(id);
    $('rail').appendChild(b);
  });
}
function showTip(e, a, t) {
  const tip = $('tip');
  tip.innerHTML = `<b>${a}</b><span>${t}</span>`;
  tip.hidden = false;
  tip.style.left = Math.min(e.clientX, innerWidth - 240) + 'px'; tip.style.top = e.clientY + 'px';
}

function showTower() {
  heroBox.style.transition = 'none'; heroBox.style.transform = '';
  body.dataset.view = 'tower';
  $('photo').setAttribute('aria-hidden', 'true');
  highlight(null);
  setNav(null);
}

async function enterFloor(id) {
  if (busy || body.dataset.view !== 'tower') return; busy = true;
  $('tip').hidden = true;
  highlight(id);
  // Phóng ảnh vào đúng tầng được chọn rồi mới chuyển cảnh
  const pts = id === 'lobby' ? LOBBY_POLY : floorPoly(id);
  const cx = pts.reduce((s, p) => s + p[0], 0) / pts.length / HERO.w, cy = pts.reduce((s, p) => s + p[1], 0) / pts.length / HERO.h;
  heroBox.style.transition = '';
  heroBox.style.transformOrigin = `${cx * 100}% ${cy * 100}%`;
  heroBox.style.transform = 'scale(2.3)';
  await wait(650);
  await veil(true);
  if (id === 'lobby') await openPhoto(LOBBY.photo, LOBBY.eyebrow, LOBBY.title, 'tower');
  else await showPlan(FLOOR_ROOM(id), `Tầng ${id}`);
  await veil(false);
  busy = false;
}

/* ============ Màn mặt bằng: ảnh chân thật, hoặc vòng xoay Blender ============ */
let turnMeta = {};
const frameCache = {};
let current = null;           // { key, frames, idx, spots }
const turn = $('turn'), turnBox = $('turnBox'), turnImg = $('turnImg');

function layoutTurn() {
  const wide = innerWidth > 760;
  const areaW = wide ? innerWidth - 372 : innerWidth;
  const areaH = wide ? innerHeight - 60 : innerHeight * 0.56;
  const top = wide ? 60 : 84;
  const w = Math.min(areaW * 1.12, areaH * 1.12 * 4 / 3), h = w * 3 / 4;
  Object.assign(turnBox.style, { width: w + 'px', height: h + 'px', left: (areaW - w) / 2 + 'px', top: top + (areaH - h) / 2 + 'px' });
}
addEventListener('resize', layoutTurn);

function loadFrames(key) {
  if (!frameCache[key]) {
    const urls = ROOMS[key].still ? [ROOMS[key].still]
      : turnMeta[key].frames.map((_, i) => `assets/turn/${key}/${String(i).padStart(2, '0')}.jpg`);
    frameCache[key] = Promise.all(urls.map(u => new Promise(ok => {
      const im = new Image(); im.onload = im.onerror = () => ok(im); im.src = u;
    })));
  }
  return frameCache[key];
}
// Ảnh chân thật cùng góc máy với khung 00 của Blender nên dùng chung vị trí điểm bấm, trừ khi phòng có `at` riêng.
const spotXY = (key, idx, id) => (ROOMS[key].at && ROOMS[key].at[id]) || turnMeta[key].frames[idx][id];

function setFrame(i) {
  const n = current.frames.length;
  current.idx = ((Math.round(i) % n) + n) % n;
  turnImg.src = current.frames[current.idx].src;
  for (const s of current.spots) {
    const [x, y] = spotXY(current.key, current.idx, s.id);
    s.el.style.left = (x * 100).toFixed(2) + '%'; s.el.style.top = (y * 100).toFixed(2) + '%';
  }
}

async function showPlan(key, floorText) {
  const room = ROOMS[key];
  const frames = await loadFrames(key);
  zoomOut(true);
  $('pFloor').textContent = floorText || 'Hạng phòng';
  $('pName').textContent = room.name;
  $('pFacts').innerHTML = `<div><dt>Diện tích</dt><dd>${room.area}</dd></div>` +
    (room.count ? `<div><dt>Số lượng</dt><dd>${room.count}</dd></div>` : '') +
    (room.sub ? `<div><dt>Giường</dt><dd>${room.sub}</dd></div>` : '');
  $('pDesc').textContent = room.desc;
  $('pFeat').innerHTML = COMMON.map(t => `<li>${t}</li>`).join('');

  const layer = $('hotspots'), list = $('pSpots');
  layer.innerHTML = ''; list.innerHTML = '';
  const spots = Object.entries(room.spots).map(([id, [label, photo, kind]]) => {
    const s = { id, label, photo, kind };
    s.el = document.createElement('button');
    s.el.className = 'hs' + (photo ? ' cam' : ''); s.el.textContent = label;
    if (photo) s.el.dataset.kind = KIND[kind];
    s.el.onclick = () => enterSpot(s);
    layer.appendChild(s.el);
    const li = document.createElement('button');
    li.textContent = label + (photo ? ` · ${KIND[kind]}` : ''); li.onclick = () => enterSpot(s);
    list.appendChild(li);
    return s;
  });
  turn.classList.toggle('still', frames.length === 1);
  $('pNote').textContent = room.still
    ? 'Hình mặt bằng là ảnh minh họa tạo bằng AI theo ảnh thật của khách sạn; bố trí phỏng dựng theo diện tích công bố.'
    : 'Mặt bằng 3D do Blender kết xuất, phỏng dựng theo diện tích công bố.';
  current = { key, frames, idx: 0, spots };
  setFrame(0);
  body.dataset.view = 'plan';
  setNav(key);
}

// Kéo ngang để xoay (chỉ với phòng còn dùng vòng xoay Blender); phím ← → cũng xoay
let drag = null;
turn.addEventListener('pointerdown', e => {
  if (e.target.closest('button') || busy || zoomed || current.frames.length < 2) return;
  drag = { x: e.clientX, i: current.idx }; turn.setPointerCapture(e.pointerId);
});
turn.addEventListener('pointermove', e => {
  if (!drag) return;
  if (Math.abs(e.clientX - drag.x) > 4) turn.classList.add('dragging');
  setFrame(drag.i - (e.clientX - drag.x) / (turnBox.clientWidth / current.frames.length * 0.9));
});
const endDrag = () => { drag = null; turn.classList.remove('dragging'); };
turn.addEventListener('pointerup', endDrag); turn.addEventListener('pointercancel', endDrag);
$('turnPrev').onclick = () => { if (!zoomed) setFrame(current.idx - 1); };
$('turnNext').onclick = () => { if (!zoomed) setFrame(current.idx + 1); };

let zoomed = false;
function zoomOut(instant) {
  zoomed = false;
  turnBox.style.transition = instant ? 'none' : '';
  turnBox.style.transform = '';
  turn.classList.remove('zoomed');
}
async function enterSpot(s) {
  if (busy) return; busy = true;
  const [x, y] = spotXY(current.key, current.idx, s.id);
  turnBox.style.transition = '';
  turnBox.style.transformOrigin = `${x * 100}% ${y * 100}%`;
  turnBox.style.transform = 'scale(2.6)';
  zoomed = true; turn.classList.add('zoomed');
  await wait(1000);
  if (s.photo) await openPhoto(s.photo, `${ROOMS[current.key].name} · ${KIND[s.kind]}`, s.label, 'plan');
  busy = false;
}

/* ========================= Màn ảnh phòng ========================= */
let photoBack = 'plan';
function openPhoto(src, eyebrow, title, back) {
  photoBack = back;
  return new Promise(done => {
    const img = $('photoImg');
    const go = () => {
      $('phEyebrow').textContent = eyebrow; $('phTitle').textContent = title; img.alt = `${title} — ${eyebrow}`;
      $('backPlan').textContent = back === 'plan' ? '← Mặt bằng' : '← Tòa nhà';
      $('photo').setAttribute('aria-hidden', 'false');
      body.dataset.view = 'photo'; done();
    };
    img.onload = go; img.onerror = go; img.src = src;
  });
}

async function toTower() {
  if (busy) return; busy = true;
  await veil(true); showTower(); await veil(false);
  busy = false;
}
function goBack() {
  if (busy) return;
  const v = body.dataset.view;
  if (v === 'photo' && photoBack === 'plan') { $('photo').setAttribute('aria-hidden', 'true'); body.dataset.view = 'plan'; zoomOut(); }
  else if (v === 'plan' && zoomed) zoomOut();
  else if (v === 'photo' || v === 'plan') toTower();
}
$('backPlan').onclick = goBack;
$('backTower').onclick = toTower;
turn.addEventListener('click', e => { if (zoomed && !busy && !e.target.closest('button')) zoomOut(); });
addEventListener('keydown', e => {
  if (e.key === 'Escape') goBack();
  if (body.dataset.view === 'plan' && !zoomed && (e.key === 'ArrowLeft' || e.key === 'ArrowRight')) setFrame(current.idx + (e.key === 'ArrowLeft' ? -1 : 1));
});

function setNav(key) {
  document.querySelectorAll('.nav button').forEach(b => b.setAttribute('aria-current', String(b.dataset.room === key)));
}
document.querySelectorAll('.nav button').forEach(b => b.onclick = async () => {
  if (busy) return; busy = true;
  await veil(true);
  $('photo').setAttribute('aria-hidden', 'true');
  if (b.dataset.room === 'lobby') { showTower(); await openPhoto(LOBBY.photo, LOBBY.eyebrow, LOBBY.title, 'tower'); }
  else await showPlan(b.dataset.room, '');
  await veil(false); busy = false;
});

/* ============================ Khởi động ============================ */
async function boot() {
  turnMeta = await fetch('assets/turn/turn.json').then(r => r.json());
  buildTower(); layoutTurn();
  const img = $('heroImg');
  if (!img.complete) await new Promise(ok => { img.onload = img.onerror = ok; });
  showTower();
  $('loading').classList.add('done');
  window.__ready = true;
  loadFrames('deluxe');
}
boot().catch(err => { $('loadPct').textContent = 'Không tải được dữ liệu: ' + err.message; console.error(err); });
