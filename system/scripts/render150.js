// Renders 150 pin images (1000x1500) from /home/claude/pins150.json
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const src = fs.readFileSync(path.join(__dirname, 'render.js'), 'utf8');
const C = eval('(' + src.match(/const C = (\{[^;]*\});/)[1] + ')');
const ICON = eval('(' + src.match(/const ICON = (\{[\s\S]*?\n\});/)[1] + ')');
const FONTS = path.join(__dirname, 'node_modules/@fontsource');
const OUT = process.argv[2];
const pins = JSON.parse(fs.readFileSync('/home/claude/pins150.json', 'utf8'));
const css = `
@font-face{font-family:Fredoka;font-weight:700;src:url(file://${FONTS}/fredoka/files/fredoka-latin-700-normal.woff2)}
@font-face{font-family:Nunito;font-weight:800;src:url(file://${FONTS}/nunito/files/nunito-latin-800-normal.woff2)}
@font-face{font-family:Nunito;font-weight:700;src:url(file://${FONTS}/nunito/files/nunito-latin-700-normal.woff2)}
*{margin:0;padding:0;box-sizing:border-box} body{width:1000px;height:1500px;overflow:hidden}
.h{font-family:Fredoka;font-weight:700;line-height:1.02;letter-spacing:-1px}
.fit{display:flex;align-items:center;justify-content:center;text-align:center}
.pill{display:inline-block;border-radius:60px;font-family:Nunito;font-weight:800}
`;
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
const badge = (bg, fg) => `<span class="pill" style="background:${bg};color:${fg};font-size:30px;padding:12px 30px;letter-spacing:2px">PH.D. SCHOOL PSYCHOLOGIST PICK</span>`;
const cta = (bg, fg) => `<span class="pill" style="background:${bg};color:${fg};font-size:40px;padding:22px 52px">Tap to shop on Amazon &rarr;</span>`;
const brand = (fg) => `<div style="position:absolute;left:0;right:0;bottom:46px;text-align:center;font-family:Fredoka;font-weight:700;font-size:32px;color:${fg};opacity:.85">Dr. Q Kids</div>`;

function html(p) {
  const H = esc(p.headline), N = esc(p.name), P = esc(p.promise.charAt(0).toUpperCase() + p.promise.slice(1)), I = ICON[p.icon](p.accent);
  switch (p.variant) {
    case 0: return `<div style="position:absolute;inset:0;background:${C.cream}">
      <div style="position:absolute;left:0;right:0;top:0;height:520px;background:${p.bg}"></div>
      <div class="fit h" data-fit style="position:absolute;left:60px;right:60px;top:60px;height:300px;color:${C.navy};font-size:110px">${H}</div>
      <div style="position:absolute;left:0;right:0;top:390px;text-align:center">${badge(C.navy, '#fff')}</div>
      <div style="position:absolute;left:330px;top:540px;width:340px;height:340px">${I}</div>
      <div class="fit" style="position:absolute;left:80px;right:80px;top:900px;height:250px;background:#fff;border:8px solid ${C.navy};border-radius:44px;flex-direction:column;padding:20px 30px">
        <div style="font-family:Nunito;font-weight:800;font-size:28px;color:${C.coral};letter-spacing:2px">DR. Q'S PICK</div>
        <div class="h" data-fit2 style="font-size:52px;color:${C.navy};margin-top:8px">${N}</div></div>
      <div style="position:absolute;left:0;right:0;top:1200px;text-align:center">${cta(C.coral, '#fff')}</div>${brand(C.navy)}</div>`;
    case 1: return `<div style="position:absolute;inset:0;background:${p.bg}">
      <div style="position:absolute;left:60px;right:60px;top:60px;bottom:60px;background:#fff;border-radius:60px;border:10px solid ${C.navy};box-shadow:0 16px 0 ${C.navy}"></div>
      <div style="position:absolute;left:0;right:0;top:120px;text-align:center">${badge(p.accent, C.navy)}</div>
      <div class="fit h" data-fit style="position:absolute;left:110px;right:110px;top:200px;height:330px;color:${C.navy};font-size:112px">${H}</div>
      <div style="position:absolute;left:350px;top:560px;width:300px;height:300px">${I}</div>
      <div class="fit" style="position:absolute;left:120px;right:120px;top:880px;height:150px;font-family:Nunito;font-weight:800;font-size:40px;color:${C.ink}">${P}</div>
      <div class="fit h" data-fit2 style="position:absolute;left:120px;right:120px;top:1040px;height:130px;font-size:50px;color:${C.coral}">${N}</div>
      <div style="position:absolute;left:0;right:0;top:1210px;text-align:center">${cta(C.navy, '#fff')}</div></div>`;
    case 2: return `<div style="position:absolute;inset:0;background:${C.navy}">
      <svg style="position:absolute;inset:0;opacity:.18" width="1000" height="1500"><circle cx="900" cy="120" r="180" fill="${p.accent}"/><circle cx="80" cy="1380" r="220" fill="${C.coral}"/></svg>
      <div style="position:absolute;left:0;right:0;top:90px;text-align:center">${badge(C.sun, C.navy)}</div>
      <div class="fit h" data-fit style="position:absolute;left:70px;right:70px;top:170px;height:420px;color:#fff;font-size:124px">${H}</div>
      <div style="position:absolute;left:300px;top:600px;width:400px;height:400px;background:${C.cream};border-radius:50%;padding:40px">${I}</div>
      <div class="fit h" data-fit2 style="position:absolute;left:90px;right:90px;top:1030px;height:150px;font-size:54px;color:${C.sun}">${N}</div>
      <div style="position:absolute;left:0;right:0;top:1220px;text-align:center">${cta(C.coral, '#fff')}</div>${brand('#fff')}</div>`;
    case 3: return `<div style="position:absolute;inset:0;background:#fff">
      <div style="position:absolute;left:0;right:0;top:0;height:640px;background:${p.bg}"></div>
      <div style="position:absolute;left:280px;top:90px;width:440px;height:440px">${I}</div>
      <div style="position:absolute;left:0;right:0;top:560px;text-align:center">${badge(C.navy, '#fff')}</div>
      <div class="fit h" data-fit style="position:absolute;left:70px;right:70px;top:670px;height:330px;color:${C.navy};font-size:112px">${H}</div>
      <div class="fit" style="position:absolute;left:100px;right:100px;top:1010px;height:170px;border-top:6px dashed ${p.accent};flex-direction:column">
        <div style="font-family:Nunito;font-weight:800;font-size:28px;color:${C.ink};letter-spacing:2px">MY PICK</div>
        <div class="h" data-fit2 style="font-size:50px;color:${C.coral};margin-top:6px">${N}</div></div>
      <div style="position:absolute;left:0;right:0;top:1220px;text-align:center">${cta(C.navy, '#fff')}</div>${brand(C.navy)}</div>`;
    default: return `<div style="position:absolute;inset:0;background:${C.cream}">
      <div style="position:absolute;right:50px;top:50px;width:230px;height:230px">${I}</div>
      <div style="position:absolute;left:60px;top:90px;font-family:Nunito;font-weight:800;font-size:34px;color:${C.coral};letter-spacing:3px">PARENTS ASK ME:</div>
      <div class="h" data-fit style="position:absolute;left:60px;right:60px;top:300px;height:520px;display:flex;align-items:center;color:${C.navy};font-size:140px">${H}</div>
      <div style="position:absolute;left:60px;right:60px;top:850px;height:8px;background:${p.accent};border-radius:4px"></div>
      <div style="position:absolute;left:60px;right:60px;top:900px;font-family:Nunito;font-weight:800;font-size:36px;color:${C.ink}">The one I recommend as a school psychologist:</div>
      <div class="h" data-fit2 style="position:absolute;left:60px;right:60px;top:970px;height:200px;display:flex;align-items:center;font-size:66px;color:${C.coral}">${N}</div>
      <div style="position:absolute;left:60px;top:1220px">${cta(C.navy, '#fff')}</div>${brand(C.navy)}</div>`;
  }
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1000, height: 1500 } });
  const tmp = path.join(__dirname, 'tmp150.html');
  for (const p of pins) {
    fs.writeFileSync(tmp, `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${html(p)}</body></html>`);
    await page.goto('file://' + tmp);
    await page.evaluate(async () => {
      await document.fonts.ready;
      const shrink = (el, min) => { let s = parseFloat(getComputedStyle(el).fontSize);
        const box = el.hasAttribute('data-fit') || el.hasAttribute('data-fit2') ? el : el.parentElement;
        while ((el.scrollHeight > box.clientHeight + 2 || el.scrollWidth > el.clientWidth + 2) && s > min) { s -= 2; el.style.fontSize = s + 'px'; } };
      document.querySelectorAll('[data-fit]').forEach(e => shrink(e, 48));
      document.querySelectorAll('[data-fit2]').forEach(e => {
        let s = parseFloat(getComputedStyle(e).fontSize);
        const limit = e.parentElement.hasAttribute('data-fit2') ? e.parentElement : (e.style.height ? e : e.parentElement);
        const tooBig = () => e.style.height ? e.scrollHeight > e.clientHeight + 2 : e.parentElement.scrollHeight > e.parentElement.clientHeight + 2;
        while (tooBig() && s > 28) { s -= 2; e.style.fontSize = s + 'px'; }
      });
    });
    await page.screenshot({ path: path.join(OUT, p.file) });
  }
  await browser.close();
  console.log('rendered', pins.length);
})();
