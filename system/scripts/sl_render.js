// Sideline Ready: brand assets + 150 pins
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const F = path.join(__dirname, 'node_modules/@fontsource');
const OUT = process.argv[2];
const C = { navy: '#14213D', turf: '#1F7A4C', orange: '#FF7F3F', yellow: '#FFC93C', chalk: '#F6F3EA', sky: '#4EA5D9', red: '#E63946', ink: '#1B2433' };
const css = `
@font-face{font-family:Oswald;font-weight:700;src:url(file://${F}/oswald/files/oswald-latin-700-normal.woff2)}
@font-face{font-family:Oswald;font-weight:600;src:url(file://${F}/oswald/files/oswald-latin-600-normal.woff2)}
@font-face{font-family:Inter;font-weight:800;src:url(file://${F}/inter/files/inter-latin-800-normal.woff2)}
@font-face{font-family:Inter;font-weight:700;src:url(file://${F}/inter/files/inter-latin-700-normal.woff2)}
*{margin:0;padding:0;box-sizing:border-box} html,body{background:transparent}
.h{font-family:Oswald;font-weight:700;line-height:1.02;text-transform:uppercase;letter-spacing:.5px}
.b{font-family:Inter;font-weight:800}
.fit{display:flex;align-items:center;justify-content:center;text-align:center}
.pill{display:inline-block;border-radius:14px;font-family:Inter;font-weight:800}`;
const S = (w, i) => `stroke="${C.navy}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
const ICON = {
  seat: c => `<svg viewBox="0 0 200 200"><rect x="40" y="36" width="120" height="78" rx="16" fill="${c}" ${S(8)}/><rect x="30" y="112" width="140" height="34" rx="12" fill="${c}" ${S(8)}/><path d="M48 146 v30 M152 146 v30" ${S(9)}/><path d="M60 60 h80 M60 84 h80" stroke="#fff" stroke-width="6" opacity=".6" stroke-linecap="round"/></svg>`,
  cold: c => `<svg viewBox="0 0 200 200"><path d="M60 92 h80 l-10 86 h-60 z" fill="${c}" ${S(8)}/><path d="M140 108 h12 a14 14 0 0 1 0 28 h-16" fill="none" ${S(8)}/><path d="M84 70 q-8 -14 0 -26 M108 70 q-8 -14 0 -26" fill="none" ${S(6)}/><g ${S(6)}><path d="M160 20 v44 M141 31 l38 22 M141 53 l38 -22"/></g></svg>`,
  wagon: c => `<svg viewBox="0 0 200 200"><path d="M26 80 h134 l-12 56 h-110 z" fill="${c}" ${S(8)}/><path d="M160 92 l26 -26" ${S(8)}/><circle cx="58" cy="152" r="20" fill="${C.navy}"/><circle cx="58" cy="152" r="7" fill="#fff"/><circle cx="130" cy="152" r="20" fill="${C.navy}"/><circle cx="130" cy="152" r="7" fill="#fff"/><rect x="44" y="44" width="40" height="36" rx="6" fill="${C.yellow}" ${S(6)}/><circle cx="114" cy="62" r="18" fill="#fff" ${S(6)}/></svg>`,
  travel: c => `<svg viewBox="0 0 200 200"><rect x="30" y="70" width="140" height="100" rx="16" fill="${c}" ${S(8)}/><rect x="30" y="70" width="140" height="30" rx="12" fill="#fff" ${S(8)}/><path d="M80 70 v-18 h40 v18" fill="none" ${S(8)}/><circle cx="150" cy="38" r="22" fill="#fff" ${S(6)}/><path d="M134 30 q16 10 32 0 M134 46 q16 -10 32 0" fill="none" stroke="${C.red}" stroke-width="4"/></svg>`,
  gifts: c => `<svg viewBox="0 0 200 200"><rect x="36" y="84" width="128" height="90" rx="10" fill="${c}" ${S(8)}/><rect x="28" y="62" width="144" height="34" rx="8" fill="${c}" ${S(8)}/><rect x="90" y="62" width="20" height="112" fill="${C.yellow}" ${S(6)}/><path d="M100 62 C70 30 50 50 70 62 Z M100 62 C130 30 150 50 130 62 Z" fill="${C.yellow}" ${S(6)}/></svg>`,
  coach: c => `<svg viewBox="0 0 200 200"><path d="M40 100 a46 46 0 1 0 92 0 v-26 h44 v-30 h-90 a46 46 0 0 0 -46 56 z" fill="${c}" ${S(8)}/><circle cx="86" cy="100" r="16" fill="#fff" ${S(6)}/><path d="M60 60 q-30 -30 -40 10" fill="none" ${S(6)}/></svg>`,
  dad: c => `<svg viewBox="0 0 200 200"><path d="M50 40 h100 v80 h-100 z" fill="${c}" ${S(8)}/><path d="M36 120 h128" ${S(9)}/><path d="M56 120 l-20 56 M144 120 l20 56 M56 176 l88 -56 M144 176 l-88 -56" ${S(7)}/><path d="M62 62 h76 M62 84 h76" stroke="#fff" stroke-width="6" opacity=".6"/></svg>`,
  hot: c => `<svg viewBox="0 0 200 200"><circle cx="70" cy="70" r="30" fill="${C.yellow}" ${S(6)}/>${Array.from({length:8},(_,i)=>{const a=i*Math.PI/4;return `<path d="M${70+42*Math.cos(a)} ${70+42*Math.sin(a)} L${70+54*Math.cos(a)} ${70+54*Math.sin(a)}" ${S(6)}/>`}).join('')}<circle cx="138" cy="122" r="38" fill="${c}" ${S(7)}/><path d="M138 122 l0 -30 M138 122 l26 15 M138 122 l-26 15" ${S(7)}/><path d="M138 160 v26" ${S(8)}/></svg>`,
  gameday: c => `<svg viewBox="0 0 200 200"><rect x="40" y="70" width="120" height="104" rx="12" fill="${c}" opacity=".35" ${S(8)}/><path d="M70 70 v-14 a30 30 0 0 1 60 0 v14" fill="none" ${S(8)}/><ellipse cx="100" cy="124" rx="34" ry="22" fill="#A0522D" ${S(6)}/><path d="M80 124 h40 M92 116 v16 M100 116 v16 M108 116 v16" stroke="#fff" stroke-width="4"/></svg>`,
  bag: c => `<svg viewBox="0 0 200 200"><path d="M34 74 h132 l-12 100 h-108 z" fill="${c}" ${S(8)}/><path d="M70 74 q0 -40 30 -40 q30 0 30 40" fill="none" ${S(8)}/><rect x="60" y="104" width="30" height="40" rx="6" fill="#fff" ${S(5)}/><circle cx="128" cy="124" r="16" fill="${C.yellow}" ${S(5)}/></svg>`,
};
const BCOL = { bag: C.orange, seat: C.sky, cold: C.sky, wagon: C.red, travel: C.turf, gifts: C.red, coach: C.yellow, dad: C.turf, hot: C.orange, gameday: C.sky };
const BBG = { bag: '#FFE3D3', seat: '#DCEEFA', cold: '#E3ECF7', wagon: '#FADBDD', travel: '#D7EFE2', gifts: '#FCE1E3', coach: '#FFF1C9', dad: '#DCEFE4', hot: '#FFE8C9', gameday: '#DDECF6' };
const stripes = (w, h, op) => `<svg style="position:absolute;inset:0" width="${w}" height="${h}">${Array.from({ length: 12 }, (_, i) => `<rect x="0" y="${i * h / 12}" width="${w}" height="${h / 24}" fill="#fff" opacity="${op}"/>`).join('')}</svg>`;
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
const brand = (fg) => `<div style="position:absolute;left:0;right:0;bottom:44px;text-align:center" class="h"><span style="font-size:34px;color:${fg};letter-spacing:4px">SIDELINE READY</span></div>`;
const cta = (bg, fg) => `<span class="pill" style="background:${bg};color:${fg};font-size:40px;padding:22px 50px">SHOP IT ON AMAZON &rarr;</span>`;
const tag = (bg, fg, t) => `<span class="pill" style="background:${bg};color:${fg};font-size:28px;padding:12px 26px;letter-spacing:2px">${t}</span>`;

function pinHTML(p) {
  const H = esc(p.headline), N = esc(p.name), PR = esc(p.promise), col = BCOL[p.bkey], bg = BBG[p.bkey], I = ICON[p.bkey](col);
  switch (p.variant) {
    case 0: return `<div style="position:absolute;inset:0;background:${C.turf}">${stripes(1000, 1500, .07)}
      <div style="position:absolute;left:0;right:0;top:80px;text-align:center">${tag(C.yellow, C.navy, 'SPORTS PARENT MUST HAVE')}</div>
      <div class="fit h" data-fit style="position:absolute;left:60px;right:60px;top:160px;height:400px;color:#fff;font-size:130px">${H}</div>
      <div style="position:absolute;left:310px;top:590px;width:380px;height:380px;background:${C.chalk};border-radius:50%;padding:46px;border:10px solid ${C.navy}">${I}</div>
      <div class="fit h" data-fit style="position:absolute;left:80px;right:80px;top:1010px;height:170px;color:${C.yellow};font-size:68px">${N}</div>
      <div style="position:absolute;left:0;right:0;top:1220px;text-align:center">${cta(C.orange, '#fff')}</div>${brand('#fff')}</div>`;
    case 1: return `<div style="position:absolute;inset:0;background:${C.chalk}">
      <div style="position:absolute;left:0;right:0;top:0;height:560px;background:${C.navy}"></div>
      <div style="position:absolute;left:0;right:0;top:70px;text-align:center">${tag(C.orange, '#fff', 'GAME DAY CHECKLIST')}</div>
      <div class="fit h" data-fit style="position:absolute;left:60px;right:60px;top:150px;height:370px;color:#fff;font-size:124px">${H}</div>
      <div style="position:absolute;left:330px;top:600px;width:340px;height:340px">${I}</div>
      <div class="fit" style="position:absolute;left:80px;right:80px;top:960px;height:220px;background:#fff;border:8px solid ${C.navy};border-radius:24px;flex-direction:column;padding:16px 26px">
        <div class="b" style="font-size:28px;color:${C.orange};letter-spacing:3px">ADD THIS TO YOUR BAG</div>
        <div class="h" data-fit2 style="font-size:58px;color:${C.navy};margin-top:8px">${N}</div></div>
      <div style="position:absolute;left:0;right:0;top:1220px;text-align:center">${cta(C.navy, '#fff')}</div>${brand(C.navy)}</div>`;
    case 2: return `<div style="position:absolute;inset:0;background:${bg}">
      <div style="position:absolute;left:50px;right:50px;top:50px;bottom:50px;background:#fff;border-radius:30px;border:10px solid ${C.navy}"></div>
      <div style="position:absolute;left:50px;right:50px;top:50px;height:120px;background:${C.navy};border-radius:20px 20px 0 0" class="fit h"><span style="color:${C.yellow};font-size:54px;letter-spacing:6px">SCOREBOARD PICK</span></div>
      <div class="fit h" data-fit style="position:absolute;left:100px;right:100px;top:200px;height:340px;color:${C.navy};font-size:118px">${H}</div>
      <div style="position:absolute;left:350px;top:560px;width:300px;height:300px">${I}</div>
      <div class="fit b" style="position:absolute;left:110px;right:110px;top:880px;height:120px;font-size:38px;color:${C.ink}">For ${PR.toLowerCase()}</div>
      <div class="fit h" data-fit style="position:absolute;left:110px;right:110px;top:1010px;height:150px;font-size:60px;color:${C.orange}">${N}</div>
      <div style="position:absolute;left:0;right:0;top:1200px;text-align:center">${cta(C.orange, '#fff')}</div></div>`;
    case 3: return `<div style="position:absolute;inset:0;background:${C.navy}">
      <svg style="position:absolute;inset:0" width="1000" height="1500"><path d="M0 1500 L0 1100 Q500 950 1000 1100 L1000 1500 Z" fill="${C.turf}"/><path d="M0 1130 Q500 980 1000 1130" stroke="#fff" stroke-width="6" fill="none" opacity=".5"/></svg>
      <div style="position:absolute;left:70px;top:80px">${tag(C.yellow, C.navy, 'SIDELINE READY PICK')}</div>
      <div class="h" data-fit style="position:absolute;left:70px;right:70px;top:170px;height:470px;display:flex;align-items:center;color:#fff;font-size:150px">${H}</div>
      <div style="position:absolute;right:70px;top:640px;width:300px;height:300px;background:${C.chalk};border-radius:30px;padding:30px">${I}</div>
      <div class="h" data-fit style="position:absolute;left:70px;width:520px;top:660px;height:260px;display:flex;align-items:center;color:${C.yellow};font-size:64px">${N}</div>
      <div style="position:absolute;left:70px;top:1210px">${cta(C.orange, '#fff')}</div>${brand('#fff')}</div>`;
    default: return `<div style="position:absolute;inset:0;background:${C.chalk}">
      <div style="position:absolute;left:0;top:0;bottom:0;width:40px;background:${col}"></div>
      <div style="position:absolute;left:90px;top:90px" class="b"><span style="font-size:34px;color:${C.orange};letter-spacing:3px">PARENTS SEARCH:</span></div>
      <div class="h" data-fit style="position:absolute;left:90px;right:70px;top:150px;height:520px;display:flex;align-items:center;color:${C.navy};font-size:150px">${H}</div>
      <div style="position:absolute;left:90px;right:70px;top:700px;height:10px;background:${C.navy}"></div>
      <div style="position:absolute;left:90px;top:750px" class="b"><span style="font-size:36px;color:${C.ink}">The one sports parents keep buying:</span></div>
      <div class="h" data-fit style="position:absolute;left:90px;width:560px;top:820px;height:330px;display:flex;align-items:center;color:${C.turf};font-size:72px">${N}</div>
      <div style="position:absolute;right:70px;top:860px;width:260px;height:260px">${I}</div>
      <div style="position:absolute;left:90px;top:1220px">${cta(C.navy, '#fff')}</div>${brand(C.navy)}</div>`;
  }
}

const boards = JSON.parse(fs.readFileSync('/home/claude/sl_boards.json', 'utf8'));
const pages = [];
pages.push({ file: '01_profile/logo-profile-picture-1000x1000.png', w: 1000, h: 1000, html: `<div style="width:1000px;height:1000px;background:${C.turf};position:relative;overflow:hidden">${stripes(1000, 1000, .08)}
  <div style="position:absolute;inset:120px;border-radius:50%;background:${C.navy};border:16px solid #fff"></div>
  <div style="position:absolute;left:350px;top:220px;width:300px;height:300px">${ICON.seat(C.orange)}</div>
  <div class="h" style="position:absolute;left:0;right:0;top:530px;text-align:center;color:#fff;font-size:118px;letter-spacing:4px">SIDELINE</div>
  <div class="h" style="position:absolute;left:0;right:0;top:660px;text-align:center;color:${C.yellow};font-size:84px;letter-spacing:14px">READY</div></div>` });
pages.push({ file: '01_profile/profile-cover-1920x1080.png', w: 1920, h: 1080, html: `<div style="width:1920px;height:1080px;background:${C.turf};position:relative;overflow:hidden">${stripes(1920, 1080, .07)}
  <div style="position:absolute;left:80px;top:300px;width:360px;height:360px;background:${C.chalk};border-radius:50%;padding:50px">${ICON.seat(C.orange)}</div>
  <div style="position:absolute;right:80px;top:300px;width:360px;height:360px;background:${C.chalk};border-radius:50%;padding:50px">${ICON.wagon(C.red)}</div>
  <div style="position:absolute;left:480px;right:480px;top:230px;text-align:center">
    ${tag(C.yellow, C.navy, 'THE SPORTS PARENT GEAR GUIDE')}
    <div class="h" style="color:#fff;font-size:150px;margin-top:40px;line-height:1">SIDELINE READY</div>
    <div class="b" style="color:#fff;font-size:40px;margin-top:40px;line-height:1.4">Stadium seats &bull; Sports wagons &bull; Cold game gear<br>Sports mom bag essentials &bull; Coach gifts</div></div></div>` });
boards.forEach((b, i) => pages.push({ file: `02_board-covers/${String(i + 1).padStart(2, '0')}-${b.key}.png`, w: 1000, h: 1500, html: `<div style="width:1000px;height:1500px;background:${C.navy};position:relative;overflow:hidden">
  <svg style="position:absolute;inset:0" width="1000" height="1500"><path d="M0 1500 L0 1150 Q500 1000 1000 1150 L1000 1500 Z" fill="${C.turf}"/></svg>
  <div style="position:absolute;left:290px;top:230px;width:420px;height:420px;background:${C.chalk};border-radius:50%;padding:60px;border:12px solid #fff">${ICON[b.key](BCOL[b.key])}</div>
  <div class="fit h" style="position:absolute;left:80px;right:80px;top:720px;height:330px;color:#fff;font-size:${b.cover.length > 26 ? 92 : 108}px">${b.cover}</div>
  <div style="position:absolute;left:0;right:0;bottom:120px;text-align:center" class="h"><span style="font-size:40px;color:${C.yellow};letter-spacing:6px">SIDELINE READY</span></div></div>` }));
const pins = JSON.parse(fs.readFileSync('/home/claude/sl_pins.json', 'utf8'));
pins.forEach(p => pages.push({ file: `pins/${p.file}`, w: 1000, h: 1500, html: `<div style="width:1000px;height:1500px;position:relative;overflow:hidden">${pinHTML(p)}</div>` }));

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const tmp = path.join(__dirname, 'sltmp.html');
  for (const p of pages) {
    const f = path.join(OUT, p.file); fs.mkdirSync(path.dirname(f), { recursive: true });
    fs.writeFileSync(tmp, `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${p.html}</body></html>`);
    await page.setViewportSize({ width: p.w, height: p.h });
    await page.goto('file://' + tmp);
    await page.evaluate(async () => {
      await document.fonts.ready;
      document.querySelectorAll('[data-fit],[data-fit2]').forEach(e => {
        let s = parseFloat(getComputedStyle(e).fontSize);
        const box = e.hasAttribute('data-fit2') ? e.parentElement : e;
        const over = () => box.scrollHeight > box.clientHeight + 2 || e.scrollWidth > e.clientWidth + 2;
        while (over() && s > 26) { s -= 2; e.style.fontSize = s + 'px'; }
      });
    });
    await page.screenshot({ path: f, clip: { x: 0, y: 0, width: p.w, height: p.h } });
  }
  await browser.close(); console.log('rendered', pages.length);
})();
