const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720},deviceScaleFactor:2});
await p.goto('file:///home/user/6month/nedp_deck/NEDP_Deck_Ref4_Streamline.html');await p.addStyleTag({content:'*{font-family:Arial,"Liberation Sans",sans-serif!important}'});await p.waitForTimeout(1500);
const n=await p.evaluate(()=>document.querySelectorAll('.frame').length);const out=[];
for(let i=0;i<n;i++){
 await p.evaluate(i=>{const S=[...document.querySelectorAll('.frame')];S.forEach((s,k)=>s.classList.toggle('on',k===i));document.querySelectorAll('#nav,#bar').forEach(e=>e.style.display='none');document.querySelectorAll('[data-hid]').forEach(e=>{e.style.cssText=e.dataset.hid;e.removeAttribute('data-hid')})},i);
 await p.waitForTimeout(300);
 const items=await p.evaluate(()=>{const f=document.querySelector('.frame.on');const fr=f.getBoundingClientRect();const INL=new Set(['B','I','EM','SPAN','SMALL','BR','STRONG','A']);const res=[];
  const all=[...f.querySelectorAll('*')].filter(e=>{if(e.closest('.pin,.sn,.map,.legend,.vbars,.big,.num,.ck i,.chip,.evimg,.evbig'))return false;if(INL.has(e.tagName)&&e.parentElement&&[...e.parentElement.childNodes].some(c=>c.nodeType==3&&c.textContent.trim()))return false;
   const t=(e.innerText||'').trim();if(!t)return false;const d=getComputedStyle(e).display;if((d.includes('flex')||d.includes('grid'))&&e.children.length>1)return false;return [...e.children].every(c=>INL.has(c.tagName))&&!['svg','IMG','STYLE','SCRIPT'].includes(e.tagName)});
  const sel=new Set();for(const e of all){let a=e.parentElement,skip=false;while(a&&a!==f){if(sel.has(a)){skip=true;break}a=a.parentElement}if(skip)continue;const r=e.getBoundingClientRect();if(r.width<2||r.height<2)continue;const cs=getComputedStyle(e);if(parseFloat(cs.fontSize)>150)continue;sel.add(e);
   if(cs.visibility=='hidden'||+cs.opacity===0)continue;
   let col=cs.webkitTextFillColor&&!cs.webkitTextFillColor.includes('0, 0, 0, 0')?cs.webkitTextFillColor:cs.color;if(col.includes(', 0)'))col='rgb(240,236,232)';
   const runs=[];const rgbOf=c=>{let v=c.webkitTextFillColor&&!c.webkitTextFillColor.includes('0, 0, 0, 0')?c.webkitTextFillColor:c.color;return v.includes(', 0)')?'rgb(240,236,232)':v};
   const walk=(node,pcs)=>{for(const c of node.childNodes){if(c.nodeType==3){const t=c.textContent.replace(/\s+/g,' ');if(t.trim()||t==' ')runs.push({t,fs:parseFloat(pcs.fontSize),b:+pcs.fontWeight>=600,c:rgbOf(pcs),up:pcs.textTransform=='uppercase'})}else if(c.tagName=='BR')runs.push({t:'\n'});else if(c.nodeType==1){const cs2=getComputedStyle(c);if(cs2.display=='block'&&runs.length)runs.push({t:'\n'});walk(c,cs2);if(cs2.display=='block')runs.push({t:'\n'})}}};walk(e,cs);
   const pl=parseFloat(cs.paddingLeft)||0,pt=parseFloat(cs.paddingTop)||0;res.push({runs,x:r.left-fr.left+pl,y:r.top-fr.top+pt,w:r.width-pl-(parseFloat(cs.paddingRight)||0),h:r.height-pt,t:e.innerText,fs:parseFloat(cs.fontSize),fw:+cs.fontWeight>=600,col,al:cs.textAlign,ls:parseFloat(cs.letterSpacing)||0});
   e.dataset.hid=e.style.cssText;if(cs.webkitBackgroundClip=='text'||cs.backgroundClip=='text')e.style.setProperty('background','none','important');e.style.setProperty('color','transparent','important');e.style.setProperty('-webkit-text-fill-color','transparent','important');e.querySelectorAll('*').forEach(c=>{c.style.setProperty('color','transparent','important');c.style.setProperty('-webkit-text-fill-color','transparent','important')})}
  return res});
 const el=await p.$('.frame.on');await el.screenshot({path:`/tmp/claude-0/pp/bg${i}.png`});out.push(items);}
fs.writeFileSync('/tmp/claude-0/pp/items.json',JSON.stringify(out));await b.close();})();
