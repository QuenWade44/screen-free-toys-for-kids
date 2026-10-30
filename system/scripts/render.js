// Renders Pinterest brand assets to PNG with Playwright.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT = process.argv[2] || path.join(__dirname, 'out');
const FONTS = path.join(__dirname, 'node_modules/@fontsource');
const fontFace = `
@font-face{font-family:Fredoka;font-weight:600;src:url(file://${FONTS}/fredoka/files/fredoka-latin-600-normal.woff2)}
@font-face{font-family:Fredoka;font-weight:700;src:url(file://${FONTS}/fredoka/files/fredoka-latin-700-normal.woff2)}
@font-face{font-family:Nunito;font-weight:400;src:url(file://${FONTS}/nunito/files/nunito-latin-400-normal.woff2)}
@font-face{font-family:Nunito;font-weight:700;src:url(file://${FONTS}/nunito/files/nunito-latin-700-normal.woff2)}
@font-face{font-family:Nunito;font-weight:800;src:url(file://${FONTS}/nunito/files/nunito-latin-800-normal.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:transparent}
`;

const C = { cream: '#FFF6EA', navy: '#1E3A5F', coral: '#FF7A59', sun: '#FFC24B', teal: '#2BB3A3', sage: '#8CC7A1', sky: '#7DB9E8', plum: '#9B7BD4', ink: '#22303F' };

// ---------- simple original icons (SVG) ----------
const ICON = {
  routine: (c) => `<svg viewBox="0 0 200 200"><rect x="40" y="30" width="120" height="150" rx="18" fill="#fff" stroke="${C.navy}" stroke-width="8"/><rect x="72" y="18" width="56" height="26" rx="10" fill="${c}" stroke="${C.navy}" stroke-width="6"/>${[70,105,140].map((y,i)=>`<rect x="58" y="${y-10}" width="22" height="22" rx="6" fill="${i<2?c:'#fff'}" stroke="${C.navy}" stroke-width="5"/>${i<2?`<path d="M62 ${y+1} l6 6 l11 -13" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`:''}<rect x="90" y="${y-4}" width="${i==1?48:56}" height="10" rx="5" fill="${C.navy}" opacity=".85"/>`).join('')}</svg>`,
  timer: (c) => `<svg viewBox="0 0 200 200"><circle cx="100" cy="108" r="72" fill="#fff" stroke="${C.navy}" stroke-width="8"/><path d="M100 108 L100 44 A64 64 0 0 1 160 128 Z" fill="${c}"/><circle cx="100" cy="108" r="9" fill="${C.navy}"/><rect x="88" y="18" width="24" height="18" rx="6" fill="${C.navy}"/>${Array.from({length:12},(_,i)=>{const a=i*Math.PI/6;return `<line x1="${100+60*Math.sin(a)}" y1="${108-60*Math.cos(a)}" x2="${100+52*Math.sin(a)}" y2="${108-52*Math.cos(a)}" stroke="${C.navy}" stroke-width="4" stroke-linecap="round"/>`}).join('')}</svg>`,
  sensory: (c) => `<svg viewBox="0 0 200 200"><path d="M30 90 h140 l-14 80 a12 12 0 0 1 -12 10 h-88 a12 12 0 0 1 -12 -10 z" fill="${c}" stroke="${C.navy}" stroke-width="8" stroke-linejoin="round"/>${[[60,80,C.sun],[90,72,C.coral],[120,80,C.sky],[145,74,C.sage],[75,64,C.plum],[110,58,C.sun]].map(([x,y,f])=>`<circle cx="${x}" cy="${y}" r="13" fill="${f}" stroke="${C.navy}" stroke-width="5"/>`).join('')}<path d="M150 40 q22 -6 26 14 l-34 30" stroke="${C.navy}" stroke-width="8" fill="none" stroke-linecap="round"/></svg>`,
  screenfree: (c) => `<svg viewBox="0 0 200 200"><rect x="48" y="40" width="104" height="132" rx="16" fill="#fff" stroke="${C.navy}" stroke-width="8"/><circle cx="100" cy="106" r="40" fill="none" stroke="${c}" stroke-width="12"/><line x1="72" y1="78" x2="128" y2="134" stroke="${c}" stroke-width="12" stroke-linecap="round"/><rect x="20" y="140" width="40" height="40" rx="8" fill="${C.sun}" stroke="${C.navy}" stroke-width="6"/><rect x="146" y="132" width="40" height="40" rx="8" fill="${C.sky}" stroke="${C.navy}" stroke-width="6" transform="rotate(10 166 152)"/></svg>`,
  calm: (c) => `<svg viewBox="0 0 200 200"><circle cx="100" cy="104" r="78" fill="${c}" opacity=".25"/><circle cx="100" cy="104" r="56" fill="${c}" opacity=".45"/><path d="M100 150 C40 112 52 62 84 62 C94 62 100 70 100 78 C100 70 106 62 116 62 C148 62 160 112 100 150 Z" fill="#fff" stroke="${C.navy}" stroke-width="8" stroke-linejoin="round"/></svg>`,
  active: (c) => `<svg viewBox="0 0 200 200"><rect x="22" y="128" width="156" height="42" rx="14" fill="${c}" stroke="${C.navy}" stroke-width="7"/><path d="M40 128 L80 84 L120 128 Z" fill="${C.sun}" stroke="${C.navy}" stroke-width="7" stroke-linejoin="round"/><rect x="112" y="92" width="58" height="36" rx="12" fill="${C.sky}" stroke="${C.navy}" stroke-width="7"/><circle cx="150" cy="48" r="20" fill="${C.coral}" stroke="${C.navy}" stroke-width="6"/><path d="M118 60 q-14 -22 -34 -12" stroke="${C.navy}" stroke-width="5" fill="none" stroke-dasharray="6 8" stroke-linecap="round"/></svg>`,
  gifts: (c) => `<svg viewBox="0 0 200 200"><rect x="36" y="84" width="128" height="90" rx="12" fill="${c}" stroke="${C.navy}" stroke-width="8"/><rect x="28" y="62" width="144" height="34" rx="10" fill="${c}" stroke="${C.navy}" stroke-width="8"/><rect x="90" y="62" width="20" height="112" fill="${C.sun}" stroke="${C.navy}" stroke-width="6"/><path d="M100 62 C70 30 50 50 70 62 Z M100 62 C130 30 150 50 130 62 Z" fill="${C.sun}" stroke="${C.navy}" stroke-width="6" stroke-linejoin="round"/></svg>`,
  travel: (c) => `<svg viewBox="0 0 200 200"><path d="M24 128 v-22 a14 14 0 0 1 14 -14 h18 l22 -30 a14 14 0 0 1 11 -6 h40 a14 14 0 0 1 12 7 l18 29 h7 a14 14 0 0 1 14 14 v22 z" fill="${c}" stroke="${C.navy}" stroke-width="8" stroke-linejoin="round"/><path d="M86 92 l14 -20 h26 l12 20 z" fill="#fff" stroke="${C.navy}" stroke-width="5"/><circle cx="62" cy="134" r="20" fill="${C.navy}"/><circle cx="62" cy="134" r="8" fill="#fff"/><circle cx="146" cy="134" r="20" fill="${C.navy}"/><circle cx="146" cy="134" r="8" fill="#fff"/><path d="M30 170 h140" stroke="${C.navy}" stroke-width="6" stroke-dasharray="16 12" stroke-linecap="round"/></svg>`,
  montessori: (c) => `<svg viewBox="0 0 200 200">${[[72,C.coral],[56,C.sun],[40,c],[24,C.sky]].map(([r,f])=>`<path d="M${100-r-14} 160 A${r+14} ${r+14} 0 0 1 ${100+r+14} 160 L${100+r} 160 A${r} ${r} 0 0 0 ${100-r} 160 Z" fill="${f}" stroke="${C.navy}" stroke-width="5" stroke-linejoin="round"/>`).join('')}<rect x="20" y="160" width="160" height="14" rx="7" fill="${C.navy}"/></svg>`,
  outdoor: (c) => `<svg viewBox="0 0 200 200"><circle cx="148" cy="52" r="26" fill="${C.sun}" stroke="${C.navy}" stroke-width="6"/><path d="M20 170 q80 -40 160 0 z" fill="${c}" stroke="${C.navy}" stroke-width="7" stroke-linejoin="round"/><path d="M90 150 v-56" stroke="${C.navy}" stroke-width="7" stroke-linecap="round"/><path d="M90 108 c-30 -2 -40 -22 -36 -36 c22 0 36 14 36 36 z" fill="${C.sage}" stroke="${C.navy}" stroke-width="6" stroke-linejoin="round"/><path d="M90 96 c24 -6 40 -26 34 -40 c-22 2 -34 18 -34 40 z" fill="${C.sage}" stroke="${C.navy}" stroke-width="6" stroke-linejoin="round"/></svg>`,
};

const BOARDS = JSON.parse(fs.readFileSync(path.join(__dirname, 'boards.json'), 'utf8'));

function confetti(w, h, n, seed) {
  let s = seed; const rnd = () => (s = (s * 9301 + 49297) % 233280) / 233280;
  const cols = [C.coral, C.sun, C.teal, C.sky, C.plum, C.sage];
  let out = '';
  for (let i = 0; i < n; i++) {
    const x = rnd() * w, y = rnd() * h, r = 8 + rnd() * 18, col = cols[i % cols.length], t = i % 3;
    out += t === 0 ? `<circle cx="${x}" cy="${y}" r="${r}" fill="${col}" opacity=".5"/>`
      : t === 1 ? `<rect x="${x}" y="${y}" width="${r * 1.6}" height="${r * 1.6}" rx="${r / 3}" fill="${col}" opacity=".45" transform="rotate(${rnd() * 60} ${x} ${y})"/>`
      : `<path d="M${x} ${y} l${r} ${r * 1.7} l${-r * 2} 0 z" fill="${col}" opacity=".45"/>`;
  }
  return out;
}

const pages = [];

// ---------- LOGO 1000x1000 ----------
pages.push({ file: '01_profile/logo-profile-picture-1000x1000.png', w: 1000, h: 1000, html: `
<div style="width:1000px;height:1000px;background:${C.navy};position:relative;overflow:hidden;font-family:Fredoka">
  <div style="position:absolute;inset:110px;border-radius:50%;background:${C.cream}"></div>
  <svg style="position:absolute;left:0;top:0" width="1000" height="1000" viewBox="0 0 1000 1000">
    <circle cx="500" cy="500" r="360" fill="none" stroke="${C.coral}" stroke-width="34" stroke-dasharray="560 1700" stroke-linecap="round" transform="rotate(-90 500 500)"/>
    <rect x="300" y="650" width="110" height="110" rx="22" fill="${C.sun}"/>
    <rect x="445" y="650" width="110" height="110" rx="22" fill="${C.teal}"/>
    <rect x="590" y="650" width="110" height="110" rx="22" fill="${C.coral}"/>
  </svg>
  <div style="position:absolute;left:0;right:0;top:300px;text-align:center;color:${C.navy};font-weight:700;font-size:260px;letter-spacing:-6px;line-height:1">Dr.&nbsp;Q</div>
  <div style="position:absolute;left:0;right:0;top:575px;text-align:center;color:${C.navy};font-family:Nunito;font-weight:800;font-size:44px;letter-spacing:10px">KIDS</div>
</div>` });

// ---------- PROFILE COVER 1920x1080 ----------
pages.push({ file: '01_profile/profile-cover-1920x1080.png', w: 1920, h: 1080, html: `
<div style="width:1920px;height:1080px;background:${C.cream};position:relative;overflow:hidden">
  <svg style="position:absolute;inset:0" width="1920" height="1080">${confetti(1920, 1080, 70, 7)}</svg>
  <div style="position:absolute;left:60px;top:240px;width:380px;height:380px">${ICON.timer(C.coral)}</div>
  <div style="position:absolute;left:180px;top:620px;width:300px;height:300px">${ICON.sensory(C.teal)}</div>
  <div style="position:absolute;right:70px;top:200px;width:360px;height:360px">${ICON.montessori(C.teal)}</div>
  <div style="position:absolute;right:170px;top:600px;width:320px;height:320px">${ICON.routine(C.sun)}</div>
  <div style="position:absolute;left:420px;right:420px;top:250px;text-align:center;font-family:Fredoka;color:${C.navy}">
    <div style="display:inline-block;background:${C.navy};color:#fff;font-family:Nunito;font-weight:800;font-size:30px;letter-spacing:4px;padding:14px 30px;border-radius:40px">PICKED BY A PH.D. SCHOOL PSYCHOLOGIST</div>
    <div style="font-weight:700;font-size:112px;line-height:1.02;margin-top:36px;white-space:nowrap">Screen-Free Kid Toys<br><span style="color:${C.coral}">Parents Love</span></div>
    <div style="font-family:Nunito;font-weight:700;font-size:38px;margin-top:34px;color:${C.ink}">Routine charts &bull; Visual timers &bull; Calm-down tools<br>Sensory play &bull; Gifts for kids 2-10</div>
  </div>
</div>` });

// ---------- BOARD COVERS 1000x1500 ----------
BOARDS.forEach((b, i) => {
  pages.push({ file: `02_board-covers/${String(i + 1).padStart(2, '0')}-${b.slug}-1000x1500.png`, w: 1000, h: 1500, html: `
<div style="width:1000px;height:1500px;background:${b.bg};position:relative;overflow:hidden;font-family:Fredoka">
  <svg style="position:absolute;inset:0" width="1000" height="1500">${confetti(1000, 1500, 26, i * 13 + 3)}</svg>
  <div style="position:absolute;left:90px;right:90px;top:250px;bottom:250px;background:#fff;border-radius:60px;border:10px solid ${C.navy};box-shadow:0 18px 0 ${C.navy}"></div>
  <div style="position:absolute;left:300px;top:330px;width:400px;height:400px">${ICON[b.icon](b.accent)}</div>
  <div style="position:absolute;left:130px;right:130px;top:760px;text-align:center;color:${C.navy};font-weight:700;font-size:${b.cover.length > 22 ? 84 : 96}px;line-height:1.05">${b.cover}</div>
  <div style="position:absolute;left:130px;right:130px;top:1060px;text-align:center;color:${C.ink};font-family:Nunito;font-weight:700;font-size:36px">${b.sub}</div>
  <div style="position:absolute;left:0;right:0;bottom:120px;text-align:center"><span style="background:${C.navy};color:#fff;font-weight:700;font-size:36px;padding:12px 34px;border-radius:40px">Dr.&nbsp;Q Kids</span></div>
</div>` });
});

// ---------- VIDEO PIN OVERLAY TEMPLATES 1080x1920 (transparent) ----------
pages.push({ file: '03_pin-templates/video-pin-overlay-title-band-1080x1920.png', w: 1080, h: 1920, transparent: true, html: `
<div style="width:1080px;height:1920px;position:relative;font-family:Fredoka">
  <div style="position:absolute;left:60px;right:60px;top:150px;height:330px;background:rgba(255,246,234,.94);border-radius:44px;border:8px solid ${C.navy}"></div>
  <div style="position:absolute;left:110px;right:110px;top:190px;color:#bbb;font-weight:700;font-size:64px;line-height:1.1;text-align:center">YOUR HOOK TEXT HERE<br><span style="font-size:42px">(delete this and type in your editor)</span></div>
  <div style="position:absolute;left:0;right:0;bottom:420px;text-align:center"><span style="background:${C.navy};color:#fff;font-weight:700;font-size:40px;padding:14px 38px;border-radius:44px">Dr.&nbsp;Q Kids &bull; school psychologist picks</span></div>
</div>` });
pages.push({ file: '03_pin-templates/video-pin-overlay-clean-1080x1920.png', w: 1080, h: 1920, transparent: true, html: `
<div style="width:1080px;height:1920px;position:relative;font-family:Fredoka">
  <div style="position:absolute;right:60px;top:150px"><span style="display:inline-block;background:${C.coral};color:#fff;font-weight:700;font-size:40px;padding:14px 32px;border-radius:44px">Dr.&nbsp;Q Kids</span></div>
  <div style="position:absolute;left:0;right:0;bottom:420px;text-align:center"><span style="background:rgba(30,58,95,.92);color:#fff;font-family:Nunito;font-weight:800;font-size:38px;padding:14px 36px;border-radius:44px">Tap to shop &rarr;</span></div>
</div>` });
pages.push({ file: '03_pin-templates/cover-image-template-1000x1500.png', w: 1000, h: 1500, html: `
<div style="width:1000px;height:1500px;background:${C.cream};position:relative;overflow:hidden;font-family:Fredoka">
  <svg style="position:absolute;inset:0" width="1000" height="1500">${confetti(1000, 1500, 18, 99)}</svg>
  <div style="position:absolute;left:70px;right:70px;top:120px;text-align:center;color:${C.navy};font-weight:700;font-size:92px;line-height:1.05">Morning Routine Chart for Kids</div>
  <div style="position:absolute;left:110px;right:110px;top:420px;height:760px;border-radius:50px;border:8px dashed ${C.navy};display:flex;align-items:center;justify-content:center;color:#9aa;font-family:Nunito;font-weight:800;font-size:44px;text-align:center;background:rgba(255,255,255,.6)">PUT YOUR PRODUCT<br>PHOTO HERE</div>
  <div style="position:absolute;left:0;right:0;top:1240px;text-align:center;color:${C.ink};font-family:Nunito;font-weight:800;font-size:44px">School psychologist's pick</div>
  <div style="position:absolute;left:0;right:0;bottom:90px;text-align:center"><span style="background:${C.navy};color:#fff;font-weight:700;font-size:36px;padding:12px 34px;border-radius:40px">Dr.&nbsp;Q Kids</span></div>
</div>` });

// ---------- CONTACT SHEET (preview) ----------
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const p of pages) {
    const f = path.join(OUT, p.file);
    fs.mkdirSync(path.dirname(f), { recursive: true });
    const tmp = path.join(__dirname, 'tmp.html');
    fs.writeFileSync(tmp, `<!doctype html><html><head><meta charset="utf-8"><style>${fontFace}</style></head><body>${p.html}</body></html>`);
    await page.setViewportSize({ width: p.w, height: p.h });
    await page.goto('file://' + tmp);
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: f, omitBackground: !!p.transparent, clip: { x: 0, y: 0, width: p.w, height: p.h } });
    console.log('wrote', p.file);
  }
  await browser.close();
})();
