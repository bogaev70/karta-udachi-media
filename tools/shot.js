const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch({executablePath:process.env.CHROME||'/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'}).catch(async()=>await chromium.launch());
const p=await b.newPage({viewport:{width:1080,height:1350}});
await p.goto('file://'+process.cwd()+'/'+process.argv[2]);await p.waitForTimeout(800);
await p.screenshot({path:process.argv[3]});await b.close();})();
