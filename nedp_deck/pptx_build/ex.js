const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720},deviceScaleFactor:2});
await p.goto('file:///home/user/6month/nedp_deck/NEDP_Deck_Ref4_Streamline.html');await p.addStyleTag({content:'*{font-family:Arial,"Liberation Sans",sans-serif!important}'});await p.waitForTimeout(1500);
const n=await p.evaluate(()=>document.querySelectorAll('.frame').length);const out=[];
for(let i=0;i<n;i++){
 await p.evaluate(i=>{const S=[...document.querySelectorAll('.frame')];S.forEach((s,k)=>s.classList.toggle('on',k===i));document.querySelectorAll('#nav,#bar').forEach(e=>e.style.display='none');document.querySelectorAll('[data-hid]').forEach(e=>{e.style.cssText=e.dataset.hid;e.removeAttribute('data-hid')})},i);
 await p.waitForTimeout(300);
 const items=await p.evaluate(()=>{const f=document.querySelector('.frame.on');const fr=f.getBoundingClientRect();const INL=new Set(['B','I','EM','SPAN','SMALL','BR','STRONG','A']);const res=[];
  const all=[...f.querySelectorAll('*')].filter(e=>{if(e.closest('.pin,.sn,.map,.legend,.leg,.pill,.badge,.newtag,.vbars,.big,.num,.ck i,.chip,.evimg,.evbig'))return false;if(INL.has(e.tagName)&&e.parentElement&&[...e.parentElement.childNodes].some(c=>c.nodeType==3&&c.textContent.trim()))return false;
   const t=(e.innerText||'').trim();if(!t)return false;const d=getComputedStyle(e).display;if((d.includes('flex')||d.includes('grid'))&&e.children.length>1)return false;return [...e.children].every(c=>INL.has(c.tagName))&&!['svg','IMG','STYLE','SCRIPT'].includes(e.tagName)});
  const sel=new Set();for(const e of all){let a=e.parentElement,skip=false;while(a&&a!==f){if(sel.has(a)){skip=true;break}a=a.parentElement}if(skip)continue;const r=e.getBoundingClientRect();if(r.width<2||r.height<2)continue;const cs=getComputedStyle(e);if(parseFloat(cs.fontSize)>150)continue;sel.add(e);
   if(cs.visibility=='hidden'||+cs.opacity===0)continue;
   let col=cs.webkitTextFillColor&&!cs.webkitTextFillColor.includes('0, 0, 0, 0')?cs.webkitTextFillColor:cs.color;if(col.includes(', 0)'))col='rgb(240,236,232)';
   const words=[];const tw=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);let tn;
   while(tn=tw.nextNode()){const pcs=getComputedStyle(tn.parentElement);const txt=tn.textContent;const re=/\S+\s*/g;let m;
    while(m=re.exec(txt)){const rg=document.createRange();rg.setStart(tn,m.index);rg.setEnd(tn,m.index+m[0].trimEnd().length);const rr=rg.getClientRects()[0];if(!rr)continue;
     let c=pcs.webkitTextFillColor&&!pcs.webkitTextFillColor.includes('0, 0, 0, 0')?pcs.webkitTextFillColor:pcs.color;if(c.includes(', 0)'))c='rgb(240,236,232)';
     words.push({t:m[0],x:rr.left-fr.left,y:rr.top-fr.top,r:rr.right-fr.left,h:rr.height,fs:parseFloat(pcs.fontSize),b:+pcs.fontWeight>=600,c,up:pcs.textTransform=='uppercase'})}}
   const lines=[];for(const w of words){let L=lines.find(l=>Math.abs(l.y-w.y)<w.h*0.5);if(!L){L={y:w.y,x:w.x,r:w.r,h:w.h,ws:[]};lines.push(L)}L.x=Math.min(L.x,w.x);L.r=Math.max(L.r,w.r);L.h=Math.max(L.h,w.h);if(L.ws.length){const pv=L.ws[L.ws.length-1];if(w.x-pv.r>1.5&&!/\s$/.test(pv.t))pv.t+=' '}L.ws.push(w)}
   for(const L of lines)res.push({x:L.x,y:L.y,w:L.r-L.x,h:L.h,al:'left',runs:L.ws.map(w=>({t:w.t,fs:w.fs,b:w.b,c:w.c,up:w.up}))});
   e.dataset.hid=e.style.cssText;if(cs.webkitBackgroundClip=='text'||cs.backgroundClip=='text')e.style.setProperty('background','none','important');e.style.setProperty('color','transparent','important');e.style.setProperty('-webkit-text-fill-color','transparent','important');e.querySelectorAll('*').forEach(c=>{c.style.setProperty('color','transparent','important');c.style.setProperty('-webkit-text-fill-color','transparent','important')})}
  return res});
 const el=await p.$('.frame.on');await el.screenshot({path:`/tmp/claude-0/pp/bg${i}.png`});out.push(items);}
fs.writeFileSync('/tmp/claude-0/pp/items.json',JSON.stringify(out));await b.close();})();
