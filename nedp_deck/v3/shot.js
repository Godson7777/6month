const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});
await p.goto('file://'+__dirname+'/Deck_v3.html');await p.waitForTimeout(1500);
const f=await p.$$('svg.frame');for(let i=0;i<f.length;i++)await f[i].screenshot({path:__dirname+`/png/s${String(i+1).padStart(2,'0')}.png`});await b.close()})();
