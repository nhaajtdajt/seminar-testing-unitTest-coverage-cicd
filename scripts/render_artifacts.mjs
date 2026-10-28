// Export the current HTML slides and Markdown report/declaration to printable PDFs.
// Requires Node.js with marked and playwright available through NODE_PATH.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const { marked } = await import(pathToFileURL(require.resolve('marked')).href);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const out = path.join(root, 'output/pdf');
await fs.mkdir(out, { recursive: true });
const browser = await chromium.launch({ executablePath: process.env.CHROME_BIN || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const qa = [];
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  await page.goto(pathToFileURL(path.join(root, 'slides/index.html')).href);
  await page.emulateMedia({ media: 'print' });
  await page.locator('a').evaluateAll(nodes => nodes.forEach(n => { if (!/^https?:/i.test(n.getAttribute('href') || '')) n.removeAttribute('href'); }));
  const overflow = await page.locator('.slide').evaluateAll(nodes => nodes.map((n, i) => ({slide: i+1, height: n.clientHeight, contentHeight: n.scrollHeight})).filter(n => n.contentHeight > n.height+2));
  if (overflow.length) throw new Error('Slide content exceeds print height: '+JSON.stringify(overflow));
  await page.pdf({ path: path.join(out, 'Seminar_Slides.pdf'), preferCSSPageSize: true, printBackground: true });
  qa.push({ file: 'Seminar_Slides.pdf', slides: await page.locator('.slide').count(), printOverflow: overflow });
  const css = `@page{size:A4;margin:18mm 16mm}*{box-sizing:border-box}body{color:#000;background:#fff;font:10.5pt/1.5 Arial,sans-serif}h1{font-size:21pt}h2{font-size:16pt;border-bottom:1px solid #ccc;padding-bottom:4pt;margin-top:20pt}h3{font-size:12pt}h1,h2,h3{break-after:avoid}p,li{orphans:3;widows:3}table{border-collapse:collapse;width:100%;font-size:8.3pt;table-layout:fixed}tr{break-inside:avoid}th,td{border:1px solid #aaa;padding:5pt;overflow-wrap:anywhere;vertical-align:top}thead{display:table-header-group}pre{font:8pt/1.4 monospace;white-space:pre-wrap;border:1px solid #ccc;padding:8pt;break-inside:avoid}code{font-size:.92em;overflow-wrap:anywhere}a{color:#000;overflow-wrap:anywhere}blockquote{margin-left:0;padding-left:10pt;border-left:2px solid #999}`;
  for (const [input, output] of [
    ['docs/thuc-hanh/BaoCao_ChiTiet.md', 'BaoCao_ChiTiet.pdf'],
    ['ai-usage-declaration/01_NgoGiaAn.md', 'AI_Declaration_NgoGiaAn.pdf']
  ]) {
    let html = marked.parse(await fs.readFile(path.join(root,input), 'utf8'));
    // Print portable repo paths for local references, avoiding machine-specific file URIs.
    html = html.replace(/<a href="(?!https?:|#|mailto:)([^"]+)"[^>]*>(.*?)<\/a>/gs, (_, href, label) => label+' <code>('+path.relative(root,path.resolve(path.dirname(path.join(root,input)),href))+')</code>');
    await page.setContent('<!doctype html><html lang="vi"><meta charset="utf-8"><style>'+css+'</style><body>'+html+'</body></html>');
    await page.pdf({ path: path.join(out,output), preferCSSPageSize:true, printBackground:true });
    qa.push({ file:output, source:input });
  }
} finally {
  await browser.close();
}
await fs.writeFile(path.join(out,'render-check.json'),JSON.stringify(qa,null,2)+'\n');
console.log(JSON.stringify(qa,null,2));
