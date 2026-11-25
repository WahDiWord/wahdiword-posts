// renders every .html in a folder to a 1080x1080 .png next to it
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const dir=path.resolve(process.argv[2]);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1080,height:1080}});
for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.html'))){
 await p.goto('file://'+path.join(dir,f));await p.waitForTimeout(300);
 await p.screenshot({path:path.join(dir,f.replace('.html','.png'))});}
await b.close();})();
