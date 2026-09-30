const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { execFileSync } = require('node:child_process');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');

const dir = path.resolve(process.env.RELEASE_RESULTS_DIR || 'release-results');
const targetURL = process.env.RELEASE_URL || pathToFileURL(path.resolve('index.html')).href;
if(process.env.RELEASE_URL && !targetURL.startsWith('https://')) throw new Error('Live acceptance URL must use HTTPS');
fs.mkdirSync(dir, {recursive:true});
const report = {timestamp:new Date().toISOString(), commit:execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim(),
  source_sha256:crypto.createHash('sha256').update(fs.readFileSync('index.html')).digest('hex'),
  working_tree_dirty:!!execFileSync('git',['status','--porcelain'],{encoding:'utf8'}).trim(),
  scope:process.env.RELEASE_URL ? 'live URL acceptance; Chromium synthetic keyboard/touch; not physical-device certification' : 'local source acceptance; Chromium synthetic keyboard/touch; not physical-device certification',
  url:targetURL, networking_disabled:!process.env.RELEASE_URL, checks:[]};
const idea = 'Build a mobile meal finder for first-time visitors.';
const success = 'A visitor finds one meal and receives a clear next action.';
async function check(name, action) {
  try { await action(); report.checks.push({name,pass:true}); }
  catch(e) { report.checks.push({name,pass:false,error:e.message}); }
}
async function overflow(frame) {
  const metrics = await frame.locator('html').evaluate(() => ({width:innerWidth, scroll:document.documentElement.scrollWidth}));
  assert.ok(metrics.scroll <= metrics.width+1, JSON.stringify(metrics));
}
async function activate(page, frame, selector, mode) {
  const target=frame.locator(selector);
  if(mode==='touch') return target.tap();
  // Let the application's scheduled heading-focus update complete before focusing the next control.
  await frame.locator('html').evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
  await target.focus();
  await page.keyboard.press('Enter');
}
async function workflow(page, frame, mode, format) {
  await frame.locator('#idea').fill(idea);
  await activate(page,frame,'#panel-1 [data-next]',mode);
  assert.ok(await frame.locator('#gap-audit .gap-card').count()>0);
  await overflow(frame);
  for(const [id,value] of Object.entries({audience:'First-time visitors',constraints:'Zero budget; mobile', 'must-keep':'Preserve accessibility',unknowns:'none'})) await frame.locator('#'+id).fill(value);
  await activate(page,frame,'#panel-2 [data-next]',mode);
  await frame.locator('#success').fill(success);
  await frame.locator('#evidence').fill('Observe a complete path and record pass/fail.');
  await overflow(frame);
  await activate(page,frame,'#panel-3 [data-next]',mode);
  if(mode==='touch') await frame.locator('label[for="format-'+format+'"]').tap();
  else {await frame.locator('#format-'+format).focus();await page.keyboard.press('Space');}
  await overflow(frame);
  await activate(page,frame,'#generate',mode);
  await frame.locator('#panel-5').waitFor({state:'visible'});
  const output=await frame.locator('#output').innerText();
  assert.ok(output.includes(idea), `Missing idea in ${format}: ${output}`); assert.ok(output.includes(success));
  assert.ok(output.includes('Observe a complete path'));
  assert.ok((await frame.locator('#next-action').innerText()).length>10);
  await overflow(frame);
  const download=page.waitForEvent('download');
  await activate(page,frame,'#download',mode);
  const file=await download;
  assert.ok(fs.readFileSync(await file.path(),'utf8').includes(success));
  await activate(page,frame,'#copy',mode);
  assert.ok((await frame.locator('#status').innerText()).length>0);
  await activate(page,frame,'#panel-5 [data-back]',mode);
  assert.ok(await frame.locator('#panel-4').isVisible());
}
(async()=>{
  let browser;
  await check('source checksum',async()=>{
    const expected=fs.readFileSync('SHA256SUMS.txt','utf8').trim().split(/\s+/)[0];
    assert.equal(crypto.createHash('sha256').update(fs.readFileSync('index.html')).digest('hex'),expected);
  });
  try {
    browser=await chromium.launch({headless:true,...(process.env.RELEASE_BROWSER ? {executablePath:process.env.RELEASE_BROWSER}: {})});
    report.browser=browser.version();
    for(const mode of ['keyboard','touch']) for(const layout of ['watch','phone','desktop']) {
      await check(`${mode}: ${layout}: full Layout Lab workflow and four formats`,async()=>{
        const context=await browser.newContext({viewport:{width:1440,height:1000},hasTouch:true,offline:!process.env.RELEASE_URL,acceptDownloads:true});
        try {
          const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
          await page.goto(targetURL);
          await activate(page,page,`[data-open-layout="${layout}"]`,mode);
          const frame=page.frameLocator('#preview-frame');
          if(layout==='watch') {
            const rail=await frame.locator('.step-rail').boundingBox();
            const scroll=await frame.locator('.panel-wrap').boundingBox();
            assert.ok(scroll.y >= rail.y + rail.height, 'Watch scrolling content overlaps fixed progress rail');
          }
          for(const format of ['prompt','brief','spec','line']) {
            if(format!=='prompt') {
              // Reopen a clean child app while retaining the selected Layout Lab size.
              const child=await (await page.locator('#preview-frame').elementHandle()).contentFrame();
              await child.goto(child.url());
            }
            await workflow(page,frame,mode,format);
          }
          await page.screenshot({path:path.join(dir,`${mode}-${layout}.png`)});
          await activate(page,page,'#preview-close',mode);
          assert.ok(await page.locator('#preview-stage').isHidden());
          assert.deepEqual(errors,[]);
        } finally {await context.close();}
      });
    }
    await check('natural phone layout: validation, tab navigation, persistence, reduced motion',async()=>{
      const context=await browser.newContext({viewport:{width:390,height:844},offline:!process.env.RELEASE_URL,reducedMotion:'reduce'});
      try {
        const page=await context.newPage();await page.goto(targetURL);
        await overflow(page);
        await page.locator('#panel-1 [data-next]').click();
        assert.ok((await page.locator('#error-1').innerText()).length>0);
        await page.locator('#idea').fill(idea);await page.reload();
        assert.equal(await page.locator('#idea').inputValue(),idea);
        await page.keyboard.press('Tab');
        assert.notEqual(await page.evaluate(()=>document.activeElement.tagName),'BODY');
        const animations=await page.evaluate(()=>document.getAnimations().filter(a=>a.playState==='running').length);
        assert.equal(animations,0);
        await page.locator('#sound-toggle').click();assert.equal(await page.locator('#sound-toggle').getAttribute('aria-pressed'),'false');
        await page.locator('.qoin').first().click();assert.notEqual(await page.locator('#wallet').innerText(),'Q 000');
      } finally {await context.close();}
    });
  } catch(e) {report.checks.push({name:'browser runtime',pass:false,error:e.message});}
  finally {if(browser)await browser.close();}
  report.pass=report.checks.every(c=>c.pass);
  fs.writeFileSync(path.join(dir,'acceptance.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report,null,2));process.exitCode=report.pass?0:1;
})();
