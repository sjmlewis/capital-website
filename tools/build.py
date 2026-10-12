#!/usr/bin/env python3
"""Builds the Capital website: writes complete pages into site/ (for hosting)
and an artifact/ copy whose index.html has no outer document tags (for the Claude artifact viewer)."""
import os, re, html, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
# When this script lives in tools/, the finished pages go into the folder above it (the repository root).
IN_TOOLS = os.path.basename(ROOT) == "tools"
SITE = os.path.dirname(ROOT) if IN_TOOLS else os.path.join(ROOT, "site")
ART = os.path.join(os.path.dirname(ROOT), ".artifact") if IN_TOOLS else os.path.join(ROOT, "artifact")
DOMAIN = "https://www.capitaloffsetservices.com"
YEAR = datetime.date.today().year
EMAIL = "stephen.lewis@capitaloffsetservices.com"
PHONE = "+44 (0)7776 226656"

FAVICON = ("data:image/svg+xml," + "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' rx='4' fill='%230B1F3A'/%3E"
           "%3Crect x='10' y='10' width='12' height='12' transform='rotate(45 16 16)' fill='%23A4834B'/%3E%3C/svg%3E")

CSS = r"""
/* Capital Industrial Participation — site styles.
   Layout: left-aligned editorial grid (max 1180px). Navy page heads carrying a generated engineering-drawing
   texture; alternating white / stone sections; navy call-to-action band; deep-navy footer. One committed light look. */
:root{
  --navy:#0B1F3A; --navy-deep:#071527; --navy-mid:#13305A;
  --brass:#A4834B; --brass-light:#C9A96A; --brass-pale:#EADFC8;
  --paper:#FFFFFF; --stone:#EEF1F5; --ink:#15202E; --ink-soft:#4A5566; --rule:#D5DBE3;
  --on-navy:#F3F5F8; --on-navy-soft:#B9C3D1;
  --display:"Libre Caslon Text","Iowan Old Style","Palatino Linotype",Georgia,serif;
  --body:"IBM Plex Sans","Segoe UI",Helvetica,Arial,sans-serif;
  --max:1180px; --gutter:clamp(16px,4vw,40px);
  color-scheme:light;
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);font-size:17px;line-height:1.6}
img,svg,canvas{max-width:100%}
a{color:inherit}
h1,h2,h3{font-family:var(--display);font-weight:400;margin:0;text-wrap:balance;letter-spacing:-0.005em}
p{margin:0}
.wrap{max-width:var(--max);margin-inline:auto;padding-inline:var(--gutter)}
:focus-visible{outline:2px solid var(--brass);outline-offset:3px}
.skip{position:absolute;left:-999px;top:8px;background:var(--brass);color:var(--navy);padding:8px 12px;border-radius:2px;z-index:50}
.skip:focus{left:8px}

/* ---------- Navigation ---------- */
.nav{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:var(--paper);border-bottom:1px solid var(--rule)}
.nav .wrap{display:flex;align-items:center;justify-content:space-between;gap:24px;min-height:76px;position:relative}
.brand{display:flex;align-items:center;gap:14px;text-decoration:none;color:var(--navy)}
.brand .mark{width:10px;height:10px;background:var(--brass);transform:rotate(45deg);flex:none}
.brand .word{font-family:var(--display);font-size:25px;line-height:1;letter-spacing:.01em}
.brand .desc{font-size:12.5px;line-height:1.2;color:var(--ink-soft);padding-left:14px;border-left:1px solid var(--rule);max-width:110px}
.menu{display:flex;align-items:center;gap:26px;list-style:none;margin:0;padding:0}
.menu a{text-decoration:none;font-size:15px;font-weight:500;color:var(--ink);padding-block:6px;border-bottom:2px solid transparent;white-space:nowrap}
.menu a:hover,.menu a[aria-current="page"]{border-bottom-color:var(--brass)}
.menu .cta a{border:1.5px solid var(--brass);color:var(--navy);padding:9px 16px;border-radius:2px}
.menu .cta a:hover,.menu .cta a[aria-current="page"]{background:var(--brass);border-color:var(--brass);color:var(--navy)}
.navtoggle{display:none;background:none;border:1.5px solid var(--rule);border-radius:2px;padding:8px 10px;font:inherit;font-size:14px;color:var(--ink);cursor:pointer}
@media (max-width:1000px){
  .brand .desc{display:none}
  .navtoggle{display:inline-block}
  .menu{display:none;position:absolute;left:0;right:0;top:100%;flex-direction:column;align-items:stretch;gap:0;background:var(--paper);border-bottom:1px solid var(--rule);padding:8px var(--gutter) 16px;box-shadow:0 20px 30px -20px rgba(0,0,0,.3)}
  .menu.open{display:flex}
  .menu li a{display:block;padding:12px 0;border-bottom:1px solid var(--rule);white-space:normal}
  .menu .cta{margin-top:12px}
  .menu .cta a{text-align:center;border-bottom:1.5px solid var(--brass)}
}

/* ---------- Buttons ---------- */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;font:inherit;font-size:15.5px;font-weight:600;text-decoration:none;padding:14px 22px;border-radius:2px;border:1.5px solid transparent;cursor:pointer;transition:background-color .15s,color .15s,border-color .15s}
.btn-brass{background:var(--brass);color:var(--navy);border-color:var(--brass)}
.btn-brass:hover{background:var(--brass-light);border-color:var(--brass-light)}
.btn-ghost{background:transparent;color:#fff;border-color:rgba(255,255,255,.55)}
.btn-ghost:hover{border-color:#fff;background:rgba(255,255,255,.06)}
.btn-navy{background:var(--navy);color:#fff;border-color:var(--navy)}
.btn-navy:hover{background:var(--navy-mid);border-color:var(--navy-mid)}
.btn-outline{background:transparent;color:var(--navy);border-color:var(--navy)}
.btn-outline:hover{background:var(--navy);color:#fff}
.actions{display:flex;flex-wrap:wrap;gap:14px;margin-top:34px}

/* ---------- Hero (home) and page heads ---------- */
.hero,.pagehead{position:relative;background:linear-gradient(118deg,var(--navy-mid) 0%,var(--navy) 48%,var(--navy-deep) 100%);color:var(--on-navy);overflow:hidden;isolation:isolate}
.hero canvas,.pagehead canvas{position:absolute;inset:0;width:100%;height:100%;z-index:-1;pointer-events:none}
.hero .wrap{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(32px,5vw,72px);align-items:center;padding-block:clamp(56px,8vw,104px)}
.hero h1{font-size:clamp(34px,4.6vw,58px);line-height:1.12;color:#fff;max-width:15ch}
.hero .lede{margin-top:22px;font-size:clamp(17px,1.4vw,19.5px);line-height:1.6;color:var(--on-navy-soft);max-width:52ch}
.audience{margin-top:26px;font-size:14px;color:var(--on-navy-soft);display:flex;gap:10px;align-items:center}
.audience::before{content:"";width:28px;height:1px;background:var(--brass-light);flex:none}
.pagehead .wrap{padding-block:clamp(44px,6vw,80px)}
.pagehead .crumb{font-size:13.5px;color:var(--on-navy-soft);margin-bottom:18px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.pagehead .crumb a{color:var(--on-navy-soft);text-decoration:none}
.pagehead .crumb a:hover{color:#fff}
.pagehead .crumb span::before{content:"";display:inline-block;width:14px;height:1px;background:var(--brass-light);vertical-align:middle;margin-right:10px}
.pagehead h1{font-size:clamp(32px,4vw,50px);line-height:1.12;color:#fff;max-width:18ch}
.pagehead .lede{margin-top:18px;font-size:clamp(17px,1.35vw,19px);line-height:1.6;color:var(--on-navy-soft);max-width:60ch}

/* Shortlist card (home): the one focal object */
.card{background:var(--paper);color:var(--ink);border-radius:3px;box-shadow:0 30px 60px -24px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.06);overflow:hidden;font-size:14px}
.card-top{display:flex;justify-content:space-between;align-items:center;padding:12px 18px;background:var(--stone);border-bottom:1px solid var(--rule);font-size:12.5px;color:var(--ink-soft);font-variant-numeric:tabular-nums}
.card-top b{font-weight:600;color:var(--navy)}
.part{padding:16px 18px 14px;border-bottom:1px solid var(--rule)}
.part-name{font-family:var(--display);font-size:19px;line-height:1.3;color:var(--navy)}
.part-meta{margin-top:6px;font-size:13px;color:var(--ink-soft)}
.cands{list-style:none;margin:0;padding:0}
.cands li{display:grid;grid-template-columns:16px 1fr auto;grid-template-areas:"mark name status" "mark why why";column-gap:12px;row-gap:3px;padding:13px 18px;border-bottom:1px solid var(--rule);align-items:start}
.cands li:last-child{border-bottom:0}
.mark{display:block;width:12px;height:12px;margin-top:5px;border:1.5px solid var(--brass);background:var(--brass);border-radius:1px;flex:none}
.cands .mark{grid-area:mark}
.mark.support{background:transparent}
.mark.partial{background:linear-gradient(90deg,var(--brass) 50%,transparent 50%)}
.mark.none{background:transparent;border-style:dashed;border-color:var(--ink-soft)}
.c-name{grid-area:name;font-weight:600;color:var(--ink)}
.c-name span{font-weight:500;color:var(--ink-soft)}
.c-name em,.sme{font-style:normal;font-size:11px;font-weight:600;color:var(--navy);background:var(--brass-pale);padding:1px 6px;border-radius:2px;margin-left:6px;vertical-align:1px}
.c-status{grid-area:status;font-size:12.5px;font-weight:500;color:var(--navy);white-space:nowrap}
.c-why{grid-area:why;font-size:13px;color:var(--ink-soft)}
.card-foot{padding:11px 18px;background:var(--stone);border-top:1px solid var(--rule);font-size:12px;color:var(--ink-soft);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.card-foot a{color:var(--navy);text-decoration:none;font-weight:500;border-bottom:1px solid var(--brass)}
@media (prefers-reduced-motion:no-preference){
  .cands li{opacity:0;transform:translateY(6px);animation:rise .5s ease forwards}
  .cands li:nth-child(1){animation-delay:.35s}.cands li:nth-child(2){animation-delay:.6s}.cands li:nth-child(3){animation-delay:.85s}
  @keyframes rise{to{opacity:1;transform:none}}
}
@media (max-width:900px){
  .hero .wrap{grid-template-columns:1fr}
  .hero h1{max-width:none}
  .cands li{grid-template-columns:16px 1fr;grid-template-areas:"mark name" "mark status" "mark why"}
  .c-status{white-space:normal}
}

/* ---------- Sections ---------- */
.section{padding-block:clamp(56px,7vw,96px)}
.section.stone{background:var(--stone)}
.section.tight{padding-block:clamp(40px,5vw,64px)}
.two{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,7fr);gap:clamp(28px,5vw,80px);align-items:start}
.two h2,.h2{font-size:clamp(28px,3vw,38px);line-height:1.15;color:var(--navy)}
.h3{font-family:var(--display);font-size:24px;line-height:1.25;color:var(--navy)}
.prose{display:grid;gap:18px;max-width:64ch;font-size:17.5px}
.prose ul,.prose ol{margin:0;padding-left:22px;display:grid;gap:10px}
.prose li::marker{color:var(--brass)}
.prose strong{font-weight:600;color:var(--navy)}
.prose .h3{margin-top:10px}
.kicker{display:block;width:44px;height:3px;background:var(--brass);margin-bottom:20px}
.sub{margin-top:14px;max-width:62ch;color:var(--ink-soft);font-size:17.5px}
.cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(24px,4vw,56px);margin-top:clamp(32px,4vw,48px)}
.cols.two-up{grid-template-columns:repeat(2,minmax(0,1fr))}
.cols.four-up{grid-template-columns:repeat(4,minmax(0,1fr))}
.col{border-top:1px solid var(--rule);padding-top:22px;min-width:0}
.col h3{font-size:23px;line-height:1.25;color:var(--navy)}
.col p{margin-top:12px;color:var(--ink-soft);font-size:16px}
.col p+p{margin-top:10px}
.steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(22px,3vw,40px) clamp(24px,4vw,56px);margin-top:clamp(32px,4vw,48px);counter-reset:step;list-style:none;padding:0;margin-inline:0}
.steps.two-up{grid-template-columns:repeat(2,minmax(0,1fr))}
.steps li{counter-increment:step;display:grid;grid-template-columns:auto 1fr;gap:16px;align-items:start;min-width:0}
.steps li::before{content:counter(step,decimal-leading-zero);font-family:var(--display);font-size:30px;line-height:1;color:var(--brass);padding-top:2px;min-width:2ch;font-variant-numeric:tabular-nums}
.steps b{display:block;font-weight:600;color:var(--navy);font-size:17px}
.steps p{margin-top:6px;color:var(--ink-soft);font-size:15.5px}
.scale{list-style:none;margin:0;padding:0;border-top:1px solid var(--rule)}
.scale li{display:grid;grid-template-columns:16px 1fr;gap:14px;padding:16px 0;border-bottom:1px solid var(--rule);align-items:start}
.scale .mark{margin-top:6px}
.scale b{display:block;font-weight:600;color:var(--navy)}
.scale span{display:block;color:var(--ink-soft);font-size:15.5px;margin-top:2px}
.note{border-left:3px solid var(--brass);background:var(--stone);padding:18px 22px;max-width:64ch;font-size:16px;color:var(--ink)}
.note b{color:var(--navy);font-weight:600}
.section.stone .note{background:var(--paper)}
.facts{list-style:none;margin:0;padding:0;border-top:1px solid var(--rule)}
.facts li{display:grid;grid-template-columns:minmax(120px,180px) 1fr;gap:16px;padding:16px 0;border-bottom:1px solid var(--rule)}
.facts b{font-family:var(--display);font-weight:400;color:var(--brass);font-size:19px;line-height:1.3}
.facts span{color:var(--ink);font-size:16px}
.panel{background:var(--paper);border:1px solid var(--rule);border-top:3px solid var(--brass);padding:28px;border-radius:2px}
.section.stone .panel{border-color:var(--rule);border-top-color:var(--brass)}
.panel h3{font-size:22px;color:var(--navy)}
.panel p{margin-top:10px;color:var(--ink-soft);font-size:15.5px}
.panel .big{font-family:var(--display);font-size:clamp(18px,1.6vw,21px);color:var(--navy);margin-top:16px;word-break:break-word;user-select:all}
.panel .btn{margin-top:18px}
.copyrow{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:16px}
.copyrow code{font:500 15px/1.4 var(--body);background:var(--stone);border:1px solid var(--rule);padding:8px 12px;border-radius:2px;user-select:all;word-break:break-all}
.copybtn{font:600 13px var(--body);background:var(--navy);color:#fff;border:0;border-radius:2px;padding:9px 12px;cursor:pointer}
.copybtn:hover{background:var(--navy-mid)}
.countries{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.countries span{font-size:13.5px;color:var(--navy);border:1px solid var(--rule);background:var(--paper);padding:5px 10px;border-radius:2px}
.section.stone .countries span{background:var(--paper)}
@media (max-width:900px){
  .two{grid-template-columns:1fr}
  .cols,.cols.two-up,.cols.four-up,.steps,.steps.two-up{grid-template-columns:1fr}
  .facts li{grid-template-columns:1fr;gap:4px}
}
@media (min-width:901px) and (max-width:1100px){
  .cols,.cols.four-up,.steps{grid-template-columns:repeat(2,minmax(0,1fr))}
}

/* ---------- Call to action band ---------- */
.band{background:var(--navy);color:var(--on-navy);border-top:4px solid var(--brass)}
.band .wrap{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:32px;align-items:center;padding-block:clamp(48px,6vw,80px)}
.band h2{font-size:clamp(26px,2.8vw,36px);line-height:1.2;color:#fff}
.band p{margin-top:12px;color:var(--on-navy-soft);max-width:54ch}
.band .actions{margin-top:0;justify-content:flex-end}
@media (max-width:900px){.band .wrap{grid-template-columns:1fr}.band .actions{justify-content:flex-start}}

/* ---------- Footer ---------- */
.foot{background:var(--navy-deep);color:var(--on-navy-soft);font-size:14px}
.foot .wrap{display:grid;grid-template-columns:minmax(0,5fr) repeat(3,minmax(0,2fr));gap:32px;padding-block:48px 28px}
.foot .brand{color:#fff}
.foot .brand .desc{color:var(--on-navy-soft);border-left-color:rgba(255,255,255,.2)}
.foot h4{margin:0 0 12px;font:600 13px/1.4 var(--body);color:#fff;letter-spacing:.02em}
.foot ul{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.foot a{text-decoration:none;color:var(--on-navy-soft)}
.foot a:hover{color:#fff}
.foot .contact{margin-top:18px;max-width:38ch;line-height:1.7}
.foot .contact span{display:block;color:#fff;user-select:all}
.legal{border-top:1px solid rgba(255,255,255,.12)}
.legal .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px 24px;padding-block:18px;font-size:13px}
@media (max-width:900px){.foot .wrap{grid-template-columns:1fr 1fr}.foot .wrap>:first-child{grid-column:1/-1}}
@media (max-width:520px){.foot .wrap{grid-template-columns:1fr}}
"""

JS = r"""
(function(){
  // Menu
  var t=document.getElementById('navtoggle'),m=document.getElementById('menu');
  if(t&&m){t.addEventListener('click',function(){var o=m.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');});
    m.addEventListener('click',function(e){if(e.target.tagName==='A'){m.classList.remove('open');t.setAttribute('aria-expanded','false');}});}

  // Copy buttons
  Array.prototype.forEach.call(document.querySelectorAll('[data-copy]'),function(b){
    b.addEventListener('click',function(){
      var v=b.getAttribute('data-copy'),label=b.textContent;
      function done(ok){b.textContent=ok?'Copied':'Select and copy';setTimeout(function(){b.textContent=label;},1800);}
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(v).then(function(){done(true)},function(){done(false)});}
      else{done(false);}
    });
  });

  // Engineering-drawing texture behind navy heads (generated, deterministic)
  var c=document.getElementById('drawing');if(!c)return;
  var hero=c.parentNode,light=hero.classList.contains('pagehead');
  function draw(){
    var W=hero.clientWidth,H=hero.clientHeight,dpr=Math.min(window.devicePixelRatio||1,2);
    c.width=Math.round(W*dpr);c.height=Math.round(H*dpr);
    var g=c.getContext('2d');g.setTransform(dpr,0,0,dpr,0,0);g.clearRect(0,0,W,H);
    var brass='201,169,106',white='255,255,255',k=light?0.7:1;
    var minor=24,major=120;
    g.lineWidth=1;
    for(var x=0.5;x<W;x+=minor){g.strokeStyle='rgba('+white+','+(((x-0.5)%major)<1?0.075:0.032)+')';g.beginPath();g.moveTo(x,0);g.lineTo(x,H);g.stroke();}
    for(var y=0.5;y<H;y+=minor){g.strokeStyle='rgba('+white+','+(((y-0.5)%major)<1?0.075:0.032)+')';g.beginPath();g.moveTo(0,y);g.lineTo(W,y);g.stroke();}
    var s=Math.max(0.6,Math.min(1,W/1200))*(light?0.75:1);
    var cx=W*(W>900?(light?0.82:0.74):0.5),cy=H*(W>900?0.5:0.3);
    function ring(r,a,w){g.strokeStyle='rgba('+brass+','+(a*k)+')';g.lineWidth=w||1;g.beginPath();g.arc(cx,cy,r*s,0,Math.PI*2);g.stroke();}
    ring(112,0.3,1.2);ring(180,0.2);ring(262,0.16);ring(348,0.13);ring(440,0.08);
    g.strokeStyle='rgba('+brass+','+(0.16*k)+')';g.lineWidth=1;
    for(var i=0;i<36;i++){var ang=i*Math.PI/18,r1=(i%3?338:326)*s,r2=348*s;g.beginPath();g.moveTo(cx+Math.cos(ang)*r1,cy+Math.sin(ang)*r1);g.lineTo(cx+Math.cos(ang)*r2,cy+Math.sin(ang)*r2);g.stroke();}
    for(var j=0;j<12;j++){var a2=j*Math.PI/6,bx=cx+Math.cos(a2)*220*s,by=cy+Math.sin(a2)*220*s;g.strokeStyle='rgba('+brass+','+(0.2*k)+')';g.beginPath();g.arc(bx,by,9*s,0,Math.PI*2);g.stroke();g.beginPath();g.moveTo(bx-13*s,by);g.lineTo(bx+13*s,by);g.moveTo(bx,by-13*s);g.lineTo(bx,by+13*s);g.strokeStyle='rgba('+brass+','+(0.12*k)+')';g.stroke();}
    g.setLineDash([22,6,4,6]);g.strokeStyle='rgba('+brass+','+(0.18*k)+')';g.lineWidth=1;
    g.beginPath();g.moveTo(cx-470*s,cy+0.5);g.lineTo(cx+470*s,cy+0.5);g.stroke();
    g.beginPath();g.moveTo(cx+0.5,Math.max(0,cy-470*s));g.lineTo(cx+0.5,Math.min(H,cy+470*s));g.stroke();
    g.setLineDash([]);
    if(light)return;
    var dy=cy+392*s,x1=cx-262*s,x2=cx+262*s;
    g.strokeStyle='rgba('+brass+',0.3)';g.lineWidth=1;
    g.beginPath();g.moveTo(x1,cy);g.lineTo(x1,dy+10);g.moveTo(x2,cy);g.lineTo(x2,dy+10);g.stroke();
    g.beginPath();g.moveTo(x1,dy+0.5);g.lineTo(x2,dy+0.5);g.stroke();
    function arrow(x,dir){g.fillStyle='rgba('+brass+',0.35)';g.beginPath();g.moveTo(x,dy+0.5);g.lineTo(x+dir*11,dy-3);g.lineTo(x+dir*11,dy+4);g.closePath();g.fill();}
    arrow(x1,1);arrow(x2,-1);
    g.fillStyle='rgba('+brass+',0.42)';g.font='500 11px "IBM Plex Sans", Helvetica, Arial, sans-serif';g.textAlign='center';g.fillText('Ø 524',cx,dy-6);
    g.save();g.beginPath();g.moveTo(cx,cy);g.arc(cx,cy,180*s,Math.PI,Math.PI*1.5);g.closePath();g.clip();
    g.strokeStyle='rgba('+brass+',0.1)';g.lineWidth=1;
    for(var q=-400;q<400;q+=11){g.beginPath();g.moveTo(cx+q*s,cy-200*s);g.lineTo(cx+(q+200)*s,cy);g.stroke();}
    g.restore();
    if(W<900)return;
    var tbx=Math.max(16,W*0.04),tby=H-58;
    g.strokeStyle='rgba('+brass+',0.22)';g.lineWidth=1;g.strokeRect(tbx+0.5,tby+0.5,176,40);
    g.beginPath();g.moveTo(tbx+0.5,tby+20.5);g.lineTo(tbx+176.5,tby+20.5);g.moveTo(tbx+88.5,tby+0.5);g.lineTo(tbx+88.5,tby+40.5);g.stroke();
    g.fillStyle='rgba('+brass+',0.4)';g.font='500 9.5px "IBM Plex Sans", Helvetica, Arial, sans-serif';g.textAlign='left';
    g.fillText('SHEET 1 OF 1',tbx+8,tby+14);g.fillText('SCALE 1:2',tbx+96,tby+14);g.fillText('TITANIUM BRACKET',tbx+8,tby+34);g.fillText('REV B',tbx+96,tby+34);
  }
  var tm;function onresize(){clearTimeout(tm);tm=setTimeout(draw,120);}
  draw();window.addEventListener('resize',onresize);
  if(document.fonts&&document.fonts.ready){document.fonts.ready.then(draw);}
})();
"""

# ---------------------------------------------------------------- navigation
NAV = [
    ("platform.html", "Platform"),
    ("industrial-participation.html", "Industrial participation"),
    ("uk-companies.html", "UK companies"),
    ("advisory.html", "Advisory"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]

def brand(cls=""):
    return (f'<a class="brand{cls}" href="index.html" aria-label="Capital Industrial Participation, home">'
            '<span class="mark" aria-hidden="true"></span><span class="word">Capital</span>'
            '<span class="desc">Industrial Participation</span></a>')

def nav(current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    cur = ' aria-current="page"' if current == "request-access.html" else ""
    items.append(f'<li class="cta"><a href="request-access.html"{cur}>Request access</a></li>')
    return ('<a class="skip" href="#main">Skip to content</a>\n<header class="nav"><div class="wrap">' + brand() +
            '<button class="navtoggle" id="navtoggle" type="button" aria-expanded="false" aria-controls="menu">Menu</button>'
            '<ul class="menu" id="menu">' + "".join(items) + '</ul></div></header>')

FOOTER = f"""
<footer class="foot" id="contact">
  <div class="wrap">
    <div>
      {brand()}
      <p class="contact">Based in London, United Kingdom. Meetings by appointment.<br><span>{EMAIL}</span><span>{PHONE}</span></p>
    </div>
    <div><h4>Platform</h4><ul><li><a href="platform.html">How it works</a></li><li><a href="security.html">Security and privacy</a></li><li><a href="request-access.html">Request access</a></li></ul></div>
    <div><h4>Services</h4><ul><li><a href="advisory.html">Advisory</a></li><li><a href="industrial-participation.html">Industrial participation</a></li><li><a href="uk-companies.html">For UK companies</a></li></ul></div>
    <div><h4>Company</h4><ul><li><a href="about.html">About Capital</a></li><li><a href="compliance.html">Compliance and ethics</a></li><li><a href="contact.html">Contact</a></li></ul></div>
  </div>
  <div class="legal"><div class="wrap">
    <span>Capital Offset Services Limited, trading as Capital Industrial Participation. Registered in England and Wales, company number 08803140.</span>
    <span>© {YEAR} Capital Offset Services Limited</span>
  </div></div>
</footer>"""

def band(title="Preparing a UK bid or an industrial participation plan?",
         text="Request a demonstration of the platform, or contact us to discuss an advisory project. We reply within two working days.",
         label="Request platform access", href="request-access.html"):
    return f"""
<section class="band" aria-labelledby="cta-title"><div class="wrap">
  <div><h2 id="cta-title">{title}</h2><p>{text}</p></div>
  <div class="actions"><a class="btn btn-brass" href="{href}">{label}</a></div>
</div></section>"""

def pagehead(title, lede, crumb=None):
    crumb_html = ""
    if crumb:
        crumb_html = '<div class="crumb"><a href="index.html">Home</a>' + "".join(
            f'<span>{html.escape(c) if isinstance(c,str) else f"<a href=\"{c[0]}\">{c[1]}</a>"}</span>' for c in crumb) + "</div>"
    return f"""
<section class="pagehead"><canvas id="drawing" aria-hidden="true"></canvas><div class="wrap">
  {crumb_html}<h1>{title}</h1><p class="lede">{lede}</p>
</div></section>"""

def head(title, desc, path, extra_css=""):
    full = "Capital Industrial Participation" if path == "index.html" else f"{title} · Capital Industrial Participation"
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(full)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{DOMAIN}/{'' if path=='index.html' else path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Capital Industrial Participation">
<meta property="og:title" content="{html.escape(full)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{DOMAIN}/{'' if path=='index.html' else path}">
<meta name="theme-color" content="#0B1F3A">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="styles.css">{extra_css}"""

def page(path, title, desc, body, current=None):
    doc = f"""<!doctype html>
<html lang="en-GB">
<head>
{head(title, desc, path)}
</head>
<body>
{nav(current or path)}
<main id="main">
{body}
</main>
{FOOTER}
<script src="site.js"></script>
</body>
</html>
"""
    return doc

# ---------------------------------------------------------------- pages
PAGES = {}

PAGES["index.html"] = dict(title="Home", desc="Capital helps overseas defence companies meet UK industrial participation commitments, with an evidence-based platform for finding credible UK industrial partners and more than 20 years of offset experience.", body=f"""
<section class="hero" aria-labelledby="hero-title">
  <canvas id="drawing" aria-hidden="true"></canvas>
  <div class="wrap">
    <div>
      <h1 id="hero-title">Find credible UK industrial partners for your defence programme</h1>
      <p class="lede">Capital helps overseas defence companies meet UK industrial participation commitments, with an evidence-based search platform and more than 20 years of offset experience.</p>
      <div class="actions">
        <a class="btn btn-brass" href="request-access.html">Request platform access</a>
        <a class="btn btn-ghost" href="platform.html">How the platform works</a>
      </div>
      <p class="audience">For overseas primes and their UK subsidiaries preparing bids and participation plans</p>
    </div>
    <aside class="card" aria-label="Example of a platform shortlist">
      <div class="card-top"><b>Shortlist</b><span>Line 14 of 38</span></div>
      <div class="part"><div class="part-name">Titanium bracket, 5-axis machined</div><div class="part-meta">AS9100 required · 400 units a year · unclassified description</div></div>
      <ol class="cands">
        <li><span class="mark" aria-hidden="true"></span><div class="c-name">Northgate Precision Ltd <em>SME</em><br><span>Sheffield</span></div><div class="c-status">Can make this now</div><div class="c-why">AS9100D · 5-axis titanium work shown on its own website</div></li>
        <li><span class="mark" aria-hidden="true"></span><div class="c-name">Avonside Aero Components Ltd<br><span>Bristol</span></div><div class="c-status">Can make this now</div><div class="c-why">AS9100D · existing aerospace structures customer base</div></li>
        <li><span class="mark support" aria-hidden="true"></span><div class="c-name">Pennine Tool &amp; Machining Ltd <em>SME</em><br><span>Derby</span></div><div class="c-status">Could make this with support</div><div class="c-why">5-axis steel and aluminium · AS9100 not recorded, confirm with the supplier</div></li>
      </ol>
      <div class="card-foot"><span>Illustrative example</span><a href="platform.html#labels">What each label means</a></div>
    </aside>
  </div>
</section>

<section class="section" aria-labelledby="challenge-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="challenge-title">The challenge</h2></div>
  <div class="prose">
    <p>The UK expects overseas suppliers to invest in its defence industry. Meeting that expectation means finding UK companies that can genuinely make your parts, develop your technology or support your programme, and finding them early.</p>
    <p>A web search turns up distributors, sales offices and advertisers alongside real manufacturers. Separating one from the other takes engineering time you may not have.</p>
    <p><a href="industrial-participation.html">About UK industrial participation</a></p>
  </div>
</div></section>

<section class="section stone" aria-labelledby="offers-title"><div class="wrap">
  <span class="kicker" aria-hidden="true"></span><h2 class="h2" id="offers-title">What Capital offers</h2>
  <div class="cols">
    <div class="col"><h3>The Capital Localisation Platform</h3><p>Upload a parts list and receive a reasoned shortlist of UK manufacturers, SMEs, universities and research centres for each line, with the evidence behind every match.</p><p><a href="platform.html">How the platform works</a></p></div>
    <div class="col"><h3>Your data stays yours</h3><p>The platform is designed so that your parts lists and shortlists are visible only to your organisation, not to Capital. You contact UK companies directly, in your own name.</p><p><a href="security.html">Security and privacy</a></p></div>
    <div class="col"><h3>Experience you can call on</h3><p>Separately from the platform, Capital offers advisory support drawn from offset and industrial participation programmes in nearly 30 countries.</p><p><a href="advisory.html">Advisory services</a></p></div>
  </div>
</div></section>

<section class="section" aria-labelledby="how-title"><div class="wrap">
  <span class="kicker" aria-hidden="true"></span><h2 class="h2" id="how-title">How the platform works</h2>
  <p class="sub">Six steps from a parts list to first contact. Your engineers stay in control at every one of them.</p>
  <ol class="steps">
    <li><div><b>Upload your parts list</b><p>Plain, unclassified descriptions. No drawings, part numbers or controlled data are needed.</p></div></li>
    <li><div><b>Choose your priorities</b><p>Put ready-now manufacturers first, or give more weight to the UK value a partnership creates.</p></div></li>
    <li><div><b>Exclude competitors</b><p>Remove rival groups from your results. Anything excluded stays listed, so you can bring it back.</p></div></li>
    <li><div><b>Review the shortlist</b><p>Results for each line are grouped by readiness, each with a reason and links to the company's own published information.</p></div></li>
    <li><div><b>Check the companies you pick</b><p>Financial health, ownership and security information for the firms you shortlist.</p></div></li>
    <li><div><b>Make first contact in your own name</b><p>A sanitised first-stage capability enquiry for each company, with a tracker for replies.</p></div></li>
  </ol>
</div></section>

<section class="section stone" aria-labelledby="eng-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="eng-title">Built for engineers, not marketing</h2>
    <p class="sub">Every match comes with a plain-English reason and a link to the company's own published information. Companies that only sell or distribute are kept out of the manufacturer results.</p></div>
  <ul class="scale" aria-label="What each readiness label means">
    <li><span class="mark" aria-hidden="true"></span><div><b>Can make this now</b><span>Evidence that the company already makes this type of item in the UK.</span></div></li>
    <li><span class="mark support" aria-hidden="true"></span><div><b>Could make this with support</b><span>Related capability. A candidate for technology transfer, new capability or SME development.</span></div></li>
    <li><span class="mark partial" aria-hidden="true"></span><div><b>Partial</b><span>The company covers part of the requirement.</span></div></li>
    <li><span class="mark none" aria-hidden="true"></span><div><b>No confirmed UK maker found</b><span>Stated plainly, with any support options still shown. The platform gives you a well-evidenced starting point; your engineers confirm capability directly with each company.</span></div></li>
  </ul>
</div></section>
{band()}""")

PAGES["platform.html"] = dict(title="The Capital Localisation Platform", desc="A secure, self-service platform that turns a bill of materials into a shortlist of credible UK industrial partners, with the evidence behind every match.", body=pagehead(
    "The Capital Localisation Platform",
    "A secure, self-service tool that turns your bill of materials into a shortlist of credible UK industrial partners: companies that can make your parts now, and companies that could make them with your support.",
    ["Platform"]) + f"""
<section class="section" aria-labelledby="how-title"><div class="wrap">
  <span class="kicker" aria-hidden="true"></span><h2 class="h2" id="how-title">How it works</h2>
  <ol class="steps">
    <li><div><b>Upload your parts list</b><p>Use plain, unclassified descriptions. No drawings, part numbers or controlled data are needed.</p></div></li>
    <li><div><b>Choose your priorities</b><p>Put ready-now manufacturers first, or give more weight to the UK value a partnership creates, such as SME growth, new capability and certification.</p></div></li>
    <li><div><b>Exclude competitors</b><p>Remove rival groups from your results. Anything excluded stays listed, so you can bring it back.</p></div></li>
    <li><div><b>Review the shortlist</b><p>Results for each line are grouped by readiness, each with a reason and links to the company's own published information.</p></div></li>
    <li><div><b>Check the companies you pick</b><p>See financial health, ownership and security information for the firms you shortlist.</p></div></li>
    <li><div><b>Make first contact in your own name</b><p>Generate a sanitised first-stage capability enquiry for each company, with a tracker for replies.</p></div></li>
  </ol>
</div></section>

<section class="section stone" id="labels" aria-labelledby="labels-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="labels-title">What you get for each line</h2>
    <p class="sub">Every candidate carries one of four labels, a plain-English reason, and links to the company's own published information.</p></div>
  <ul class="scale" aria-label="Readiness labels">
    <li><span class="mark" aria-hidden="true"></span><div><b>Can make this now</b><span>Evidence that the company already makes this type of item in the UK.</span></div></li>
    <li><span class="mark support" aria-hidden="true"></span><div><b>Could make this with support</b><span>Related capability, making the company a candidate for technology transfer, new capability or SME development.</span></div></li>
    <li><span class="mark partial" aria-hidden="true"></span><div><b>Partial</b><span>The company covers part of the requirement.</span></div></li>
    <li><span class="mark none" aria-hidden="true"></span><div><b>No confirmed UK maker found</b><span>Stated plainly, with any support options still shown.</span></div></li>
  </ul>
</div></section>

<section class="section" aria-labelledby="info-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="info-title">Company information</h2></div>
  <div class="prose">
    <p>For each organisation, the platform draws together, where available: capabilities and products, facilities, certifications, size, financial health, ownership, location, contacts, public funding and research activity, and past public contract awards.</p>
    <p>Anything not on record is marked <strong>“not recorded, confirm with the supplier”</strong>. It is never treated as a fail. Verdicts come only from adverse evidence.</p>
    <p>Smaller companies are marked <span class="sme">SME</span> throughout, because they are where most new UK capability is created.</p>
  </div>
</div></section>

<section class="section stone" aria-labelledby="isnot-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="isnot-title">What the platform is, and is not</h2></div>
  <div class="prose">
    <p><strong>It is</strong> a well-evidenced shortlist of credible UK candidates for each part, with reasons, ready for your engineers to review and contact.</p>
    <p><strong>It is not</strong> a guarantee of capability, a supplier approval or a substitute for your own qualification process. Final qualification always requires direct contact with the company.</p>
    <div class="note"><b>Who it is for.</b> Overseas defence and aerospace companies, and their UK subsidiaries, preparing bids, industrial participation plans or UK supply-chain development.</div>
  </div>
</div></section>
{band("Available by subscription", "To arrange a demonstration and discuss subscription options, request access. We reply within two working days.")}""")

PAGES["industrial-participation.html"] = dict(title="UK industrial participation", desc="What the UK's move towards industrial participation (offset) means for overseas defence suppliers, and how Capital helps them create genuine UK value.", body=pagehead(
    "UK industrial participation (offset)",
    "The UK Government has said it will introduce a new offsets regime, subject to consultation, so that when it buys defence equipment from abroad, British jobs and benefits are created.",
    ["Industrial participation"]) + f"""
<section class="section" aria-labelledby="means-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="means-title">What this means for overseas suppliers</h2></div>
  <div class="prose">
    <ul>
      <li>UK partners are needed early, often before a bid is submitted.</li>
      <li>Commitments are usually met over many years, so partners must be stable and capable.</li>
      <li>Credit is likely to favour real, lasting value: new UK suppliers, new capability, certifications and skilled jobs, especially in smaller companies.</li>
    </ul>
    <div class="note"><b>Policy detail is still being finalised.</b> Thresholds, percentages and timescales will be set out by the Ministry of Defence. Capital will update this page when they are published.</div>
  </div>
</div></section>

<section class="section stone" aria-labelledby="routes-title"><div class="wrap">
  <span class="kicker" aria-hidden="true"></span><h2 class="h2" id="routes-title">Two ways to create UK value</h2>
  <div class="cols two-up">
    <div class="col"><h3>Buy from capable UK makers now</h3><p>Place work with UK companies that already make what you need, creating UK exports from day one.</p></div>
    <div class="col"><h3>Build new UK capability</h3><p>Transfer technology, support certification or help a smaller company enter defence, creating capability that lasts beyond the contract.</p></div>
  </div>
</div></section>

<section class="section" aria-labelledby="help-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="help-title">How Capital helps</h2></div>
  <div class="prose">
    <p>The platform finds candidates for both routes and highlights the opportunities, such as a smaller company that could gain a certification or a commercial manufacturer ready to enter defence. Your team then decides where to engage.</p>
    <p>Capital's founder has worked on offset and industrial participation programmes for more than 20 years, across Europe, the Middle East, Asia, Africa and the Americas. <a href="about.html">About Capital</a></p>
  </div>
</div></section>
{band()}""")

PAGES["uk-companies.html"] = dict(title="For UK companies", desc="How UK manufacturers, SMEs and research centres are included on the Capital Localisation Platform, how they may be contacted, and how to correct or remove a listing.", body=pagehead(
    "For UK manufacturers, SMEs and research centres",
    "Overseas defence companies need UK partners. The platform helps them find you based on what you actually make.",
    ["UK companies"]) + f"""
<section class="section" aria-labelledby="inc-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="inc-title">How companies are included</h2></div>
  <div class="prose">
    <p>The platform draws on publicly available information about UK organisations, including company websites and public company records. There is no charge to be included.</p>
    <p>It includes companies that design or make things in the UK, and research centres with relevant capability. Distributors and sales-only offices are not shown as manufacturers.</p>
  </div>
</div></section>

<section class="section stone" aria-labelledby="con-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="con-title">How you may be contacted</h2></div>
  <div class="prose">
    <p>If an overseas company shortlists you, it may send you a first-stage capability enquiry in its own name. These enquiries contain no controlled technical data and are not an invitation to tender. You are free to reply or decline.</p>
    <p>Capital does not act as a go-between and does not see these enquiries or your replies.</p>
  </div>
</div></section>

<section class="section" aria-labelledby="acc-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="acc-title">Keeping your information accurate</h2></div>
  <div class="prose">
    <p>To correct your company's details, or to ask for your company to be removed, email <a href="mailto:{EMAIL}">{EMAIL}</a>. A self-service profile update is planned.</p>
  </div>
</div></section>
{band("Are you a UK maker with capability to offer?", "Tell us about your company and we will make sure your listing is accurate.", "Email Capital", "contact.html")}""")

PAGES["security.html"] = dict(title="Security and privacy", desc="How the Capital Localisation Platform keeps programme information private to the client organisation.", body=pagehead(
    "Your programme information stays with you",
    "Defence companies cannot share their parts lists lightly. The platform is designed so that your information is visible only to your organisation.",
    [("platform.html", "Platform"), "Security and privacy"]) + f"""
<section class="section" aria-labelledby="princ-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="princ-title">Our principles</h2></div>
  <div class="prose">
    <ul>
      <li><strong>Private by design.</strong> Uploaded parts lists, saved projects, shortlists, enquiries, trackers and supplier replies are designed to be visible only to your organisation's account, not to Capital.</li>
      <li><strong>No go-between.</strong> You contact UK companies directly, in your own name. Capital is never placed between you and your suppliers.</li>
      <li><strong>Unclassified information only.</strong> The platform needs plain descriptions. Please do not upload classified or export-controlled information, drawings or part numbers.</li>
      <li><strong>Sanitised enquiries.</strong> First-contact enquiries leave out part numbers, programme names and customer names, and you approve every line before anything is produced.</li>
      <li><strong>Nothing sent for you.</strong> The platform never sends emails on your behalf.</li>
    </ul>
  </div>
</div></section>

<section class="section stone" aria-labelledby="sep-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="sep-title">Separate services</h2></div>
  <div class="prose">
    <p>Capital's <a href="advisory.html">advisory services</a> are contracted separately from the platform. Platform data is not used for advisory work.</p>
    <p>Questions about security or data handling: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  </div>
</div></section>
{band()}""")

PAGES["advisory.html"] = dict(title="Advisory services", desc="Direct advisory support on offset and industrial participation for companies and governments, contracted separately from the Capital Localisation Platform.", body=pagehead(
    "Advisory services",
    "Alongside the platform, Capital offers direct advisory support to companies and governments working on offset and industrial participation. Advisory work is contracted separately from any platform subscription.",
    ["Advisory"]) + f"""
<section class="section" aria-labelledby="serv-title"><div class="wrap">
  <span class="kicker" aria-hidden="true"></span><h2 class="h2" id="serv-title">Services</h2>
  <div class="cols four-up">
    <div class="col"><h3>Industrial participation strategy</h3><p>Understanding the obligation, choosing the right mix of activities and shaping a credible plan.</p></div>
    <div class="col"><h3>Partner development</h3><p>Structuring technology transfer, training and co-production arrangements with in-country partners.</p></div>
    <div class="col"><h3>Structured export finance</h3><p>Payment structures and financing arrangements that support capital equipment exports under offset commitments.</p></div>
    <div class="col"><h3>Government advisory</h3><p>Helping governments design industrial and procurement policies that attract foreign technology and investment.</p></div>
  </div>
</div></section>

<section class="section stone" aria-labelledby="sect-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="sect-title">Sectors</h2></div>
  <div class="prose">
    <p>Capital works mainly with companies in aerospace, defence, security and space. Any company with technology or capability of interest to a government customer can benefit from the same approach.</p>
  </div>
</div></section>

<section class="section" aria-labelledby="work-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="work-title">How we work</h2></div>
  <div class="prose">
    <p>Engagements usually begin with a short discussion of your goals and target market, followed by a written proposal. Work is carried out under a services agreement, with fees agreed case by case.</p>
  </div>
</div></section>
{band("Discuss a project", "Tell us about your programme and target market, and we will come back to you within two working days.", "Contact Capital", "contact.html")}""")

COUNTRIES = ["Belgium","Brazil","Bulgaria","Canada","Denmark","Egypt","Estonia","Finland","India","Italy","Kuwait","Lithuania","Malaysia","Netherlands","Norway","Oman","Poland","Portugal","Romania","Saudi Arabia","Slovenia","South Africa","South Korea","Spain","Switzerland","Taiwan","Thailand","Turkey","United Arab Emirates"]

PAGES["about.html"] = dict(title="About Capital", desc="Capital was founded in 2013 by Stephen Lewis. More than 20 years of offset and industrial participation experience across Europe, the Middle East, Asia, Africa and the Americas.", body=pagehead(
    "About Capital",
    "Capital was founded in 2013 by Stephen Lewis to help companies create lasting value through offset and industrial participation. It now combines that experience with the Capital Localisation Platform.",
    ["About"]) + f"""
<section class="section" aria-labelledby="founder-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="founder-title">Founder</h2></div>
  <div class="prose">
    <p>Stephen Lewis has more than 20 years' experience in offset, industrial participation and cross-border trade finance, first with a leading international consulting and financing organisation and, since 2013, through Capital.</p>
    <p>His work has covered structured export finance, technology transfer and training programmes, and advisory work for governments developing their own industrial policies.</p>
    <div class="countries" aria-label="Countries worked in">{"".join(f"<span>{c}</span>" for c in COUNTRIES)}</div>
  </div>
</div></section>

<section class="section stone" aria-labelledby="exp-title"><div class="wrap">
  <span class="kicker" aria-hidden="true"></span><h2 class="h2" id="exp-title">Selected experience</h2>
  <p class="sub">Projects Stephen has led or contributed to.</p>
  <ul class="facts" style="margin-top:28px">
    <li><b>Taiwan</b><span>Linked a client with a UK aerospace company that was outsourcing component manufacture, leading to technology transfer, training, certification and about USD 100m of component exports to the UK over three years.</span></li>
    <li><b>South Korea</b><span>Helped three steel manufacturers export more than USD 200m of commercial steel to European and US defence clients under five offset contracts over six years.</span></li>
    <li><b>India</b><span>Set up technology cooperation with agencies of the Defence Research and Development Organisation, within international sanctions rules, and built partnerships with Indian aerospace and defence companies for a client's bid.</span></li>
    <li><b>Finland</b><span>Established a self-funding national R&amp;D technology centre within the main engineering university, for long-term defence product development with Finnish industry and SMEs.</span></li>
    <li><b>South Africa</b><span>Helped three local companies win new export sales over three years in ship and oil-platform repair, yellow goods and jewellery, worth about USD 80m in total.</span></li>
    <li><b>Romania</b><span>Secured around EUR 30m of technology products for Romanian universities and research centres, supported by an international defence company.</span></li>
    <li><b>Kuwait</b><span>Negotiated technological assistance for the aerospace engineering and quality control capability of the Gulf University of Science and Technology.</span></li>
    <li><b>Egypt</b><span>Structured a counter-purchase and escrow arrangement to fund stage payments for naval vessels.</span></li>
    <li><b>Brazil</b><span>Arranged aircraft finance linked to a US defence client's offset commitment to the Brazilian Air Force.</span></li>
    <li><b>Thailand</b><span>Took on a client's obligation, with a penalty for non-performance, to generate USD 20m of additional agricultural exports, and arranged the sales with an overseas buyer.</span></li>
    <li><b>United Arab Emirates</b><span>Negotiated a steel off-take agreement through an international trading network, improving the mill's financing.</span></li>
  </ul>
</div></section>

<section class="section" aria-labelledby="comp-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="comp-title">How Capital works</h2></div>
  <div class="prose">
    <p>Offset and industrial participation carry commercial and political risk. Capital works on an open, documented basis and complies with the anti-corruption and export-control laws that apply to its work.</p>
    <p><a href="compliance.html">Compliance and ethics</a></p>
  </div>
</div></section>
{band()}""")

PAGES["compliance.html"] = dict(title="Compliance and ethics", desc="Capital's anti-bribery policy and the anti-corruption and export-control laws it works to.", body=pagehead(
    "Compliance and ethics",
    "Offset and industrial participation carry commercial and political risk. Capital works on an open, documented basis.",
    [("about.html", "About"), "Compliance and ethics"]) + f"""
<section class="section" aria-labelledby="laws-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="laws-title">The laws we work to</h2></div>
  <div class="prose">
    <p>Capital complies with the anti-corruption and export-control laws that apply to its work, including:</p>
    <ul>
      <li>the UK Bribery Act 2010;</li>
      <li>the US Foreign Corrupt Practices Act (FCPA);</li>
      <li>UK export controls and the US International Traffic in Arms Regulations (ITAR), where relevant to a client's activity.</li>
    </ul>
  </div>
</div></section>

<section class="section stone" aria-labelledby="ab-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="ab-title">Anti-bribery policy</h2></div>
  <div class="prose">
    <ol>
      <li><strong>Zero tolerance.</strong> Capital does not offer, give, request or accept bribes in any form, anywhere in the world.</li>
      <li><strong>No facilitation payments.</strong> Small payments to speed up routine government actions are not made.</li>
      <li><strong>Gifts and hospitality.</strong> Only modest, occasional and transparent courtesies are given or accepted, and never to influence a decision. Nothing is given to a government official without prior written approval.</li>
      <li><strong>Accurate records.</strong> Every payment is properly documented and recorded.</li>
      <li><strong>Third parties.</strong> Agents, consultants and partners acting for Capital must follow the same standards and are checked before they are engaged.</li>
      <li><strong>Raising concerns.</strong> Concerns can be reported in confidence to <a href="mailto:{EMAIL}">{EMAIL}</a>.</li>
    </ol>
  </div>
</div></section>

<section class="section" aria-labelledby="ec-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="ec-title">Export control and the platform</h2></div>
  <div class="prose">
    <p>Platform users must upload only unclassified, non-controlled descriptions. They remain responsible for the content of their own enquiries and for their own export-control compliance.</p>
    <p>Detailed technical exchanges belong at a later stage, after a non-disclosure agreement and any required export authorisation.</p>
  </div>
</div></section>
{band()}""")

SUBJECT = "Platform access request"
PAGES["request-access.html"] = dict(title="Request platform access", desc="Request a demonstration of the Capital Localisation Platform and discuss subscription options.", body=pagehead(
    "Request platform access",
    "Tell us about your organisation and we will arrange a short demonstration and discuss subscription options.",
    ["Request access"]) + f"""
<section class="section" aria-labelledby="req-title"><div class="wrap two">
  <div>
    <span class="kicker" aria-hidden="true"></span><h2 id="req-title">How to request access</h2>
    <div class="prose" style="margin-top:18px">
      <p>Send a short email with:</p>
      <ul>
        <li>your name and job title;</li>
        <li>your organisation and country;</li>
        <li>what you hope to achieve, for example preparing a UK bid or an industrial participation plan.</li>
      </ul>
      <p>Please do not include any programme, technical or classified information.</p>
      <p>We aim to reply within two working days. Your details are used only to respond to your request.</p>
    </div>
  </div>
  <div class="panel">
    <h3>Email Capital</h3>
    <div class="big">{EMAIL}</div>
    <div class="copyrow"><button class="copybtn" type="button" data-copy="{EMAIL}">Copy email address</button></div>
    <p style="margin-top:20px"><strong>Subject line</strong>, so your request is picked up straight away:</p>
    <div class="copyrow" style="margin-top:8px"><code>{SUBJECT}</code><button class="copybtn" type="button" data-copy="{SUBJECT}">Copy subject</button></div>
    <a class="btn btn-brass" href="mailto:{EMAIL}?subject={SUBJECT.replace(' ', '%20')}">Open in your email app</a>
    <p>Prefer to talk first? {PHONE}, UK office hours.</p>
  </div>
</div></section>
{band("Want to see what the platform does first?", "The platform page explains the six steps from a parts list to first contact, and what each readiness label means.", "How the platform works", "platform.html")}""")

PAGES["contact.html"] = dict(title="Contact", desc="Contact Capital Industrial Participation by email or telephone. Based in London, United Kingdom.", body=pagehead(
    "Contact",
    "For platform enquiries, please use Request access. For everything else, get in touch below.",
    ["Contact"]) + f"""
<section class="section" aria-labelledby="gt-title"><div class="wrap two">
  <div>
    <span class="kicker" aria-hidden="true"></span><h2 id="gt-title">Get in touch</h2>
    <div class="prose" style="margin-top:18px">
      <p>Based in London, United Kingdom. Meetings by appointment.</p>
      <p>Please do not send programme, technical or classified information by email.</p>
    </div>
  </div>
  <div class="panel">
    <h3>Capital Industrial Participation</h3>
    <div class="big">{EMAIL}</div>
    <div class="copyrow"><button class="copybtn" type="button" data-copy="{EMAIL}">Copy email address</button></div>
    <p style="margin-top:18px"><strong>Telephone</strong><br>{PHONE}</p>
    <p style="margin-top:14px"><strong>Company details</strong><br>Capital Offset Services Limited, trading as Capital Industrial Participation.<br>Registered in England and Wales, company number 08803140.</p>
  </div>
</div></section>
{band()}""")

PAGES["404.html"] = dict(title="Page not found", desc="That page could not be found.", body=pagehead(
    "Page not found", "The page you asked for is not here. It may have moved when the site was rebuilt.", None) + """
<section class="section"><div class="wrap"><div class="actions" style="margin-top:0"><a class="btn btn-navy" href="index.html">Go to the home page</a><a class="btn btn-outline" href="platform.html">How the platform works</a></div></div></section>""")

# ---------------------------------------------------------------- write out
os.makedirs(SITE, exist_ok=True); os.makedirs(ART, exist_ok=True)
with open(os.path.join(SITE, "styles.css"), "w") as f: f.write(CSS.strip() + "\n")
with open(os.path.join(SITE, "site.js"), "w") as f: f.write(JS.strip() + "\n")
for p, d in PAGES.items():
    doc = page(p, d["title"], d["desc"], d["body"])
    with open(os.path.join(SITE, p), "w") as f: f.write(doc)

# sitemap + robots
urls = [p for p in PAGES if p != "404.html"]
with open(os.path.join(SITE, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        f.write(f"  <url><loc>{DOMAIN}/{'' if u=='index.html' else u}</loc></url>\n")
    f.write("</urlset>\n")
with open(os.path.join(SITE, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")

# artifact copy: same files, but index.html stripped of outer document tags (the viewer adds its own)
import shutil
for name in os.listdir(SITE):
    if os.path.isfile(os.path.join(SITE, name)) and (name.endswith(('.html','.css','.js','.xml','.txt'))):
        shutil.copy(os.path.join(SITE, name), os.path.join(ART, name))
idx = open(os.path.join(SITE, "index.html")).read()
m = re.search(r"<head>\n(.*?)</head>\s*<body>\n(.*)</body>", idx, re.S)
head_inner, body_inner = m.group(1), m.group(2)
# the viewer wants <title> and <style>/<link> first; drop charset/viewport (it adds its own)
head_inner = re.sub(r'<meta charset="utf-8">\n<meta name="viewport"[^>]*>\n', "", head_inner)
with open(os.path.join(ART, "index.html"), "w") as f: f.write(head_inner + "\n" + body_inner)
print("built", len(PAGES), "pages →", SITE, "and", ART)
