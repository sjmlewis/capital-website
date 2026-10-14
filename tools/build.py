#!/usr/bin/env python3
"""Builds the Capital website: writes complete pages into site/ (for hosting)
and an artifact/ copy whose index.html has no outer document tags (for the Claude artifact viewer)."""
import os, re, html, datetime, json

ROOT = os.path.dirname(os.path.abspath(__file__))
# When this script lives in tools/, the finished pages go into the folder above it (the repository root).
IN_TOOLS = os.path.basename(ROOT) == "tools"
SITE = os.path.dirname(ROOT) if IN_TOOLS else os.path.join(ROOT, "site")
ART = os.path.join(os.path.dirname(ROOT), ".artifact") if IN_TOOLS else os.path.join(ROOT, "artifact")
DOMAIN = "https://www.capitaloffsetservices.com"
YEAR = datetime.date.today().year
EMAIL = "stephen.lewis@capitaloffsetservices.com"
PHONE = "+44 (0)7776 226656"
EMAIL_WBR = EMAIL.replace("@", "@<wbr>")  # lets the long address break after @ on small phones

FAVICON = ("data:image/svg+xml," + "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' rx='4' fill='%230B1F3A'/%3E"
           "%3Crect x='10' y='10' width='12' height='12' transform='rotate(45 16 16)' fill='%23A4834B'/%3E%3C/svg%3E")

CSS = r"""
/* Capital Industrial Participation — site styles.
   Layout: left-aligned editorial grid (max 1280px). Navy page heads carrying a generated engineering-drawing
   texture; alternating white / stone sections; navy call-to-action band; deep-navy footer. One committed light look. */
:root{
  --navy:#0B1F3A; --navy-deep:#071527; --navy-mid:#13305A;
  --brass:#A4834B; --brass-light:#C9A96A; --brass-pale:#EADFC8;
  --paper:#FFFFFF; --stone:#EEF1F5; --ink:#15202E; --ink-soft:#364152; --rule:#D5DBE3;
  --on-navy:#F3F5F8; --on-navy-soft:#B9C3D1;
  --display:"Libre Caslon Text","Iowan Old Style","Palatino Linotype",Georgia,serif;
  --body:"IBM Plex Sans","Segoe UI",Helvetica,Arial,sans-serif;
  --max:1280px; --gutter:clamp(16px,4vw,40px);
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
[id]{scroll-margin-top:96px}
.nowrap{white-space:nowrap}
[hidden]{display:none!important}
.skip{position:absolute;left:-999px;top:8px;background:var(--brass);color:var(--navy);padding:8px 12px;border-radius:2px;z-index:50}
.skip:focus{left:8px}

/* ---------- Navigation ---------- */
.nav{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:var(--paper);border-bottom:1px solid var(--rule)}
.nav .wrap{display:flex;align-items:center;justify-content:space-between;gap:24px;min-height:76px;position:relative}
.brand{display:flex;align-items:center;gap:14px;text-decoration:none;color:var(--navy)}
.brand .mark{width:13px;height:13px;background:var(--brass);transform:rotate(45deg);flex:none}
.brand .word{font-family:var(--display);font-size:33px;line-height:1;letter-spacing:.005em;font-weight:700}
.brand .desc{font-size:13.5px;line-height:1.2;color:var(--ink-soft);padding-left:14px;border-left:1px solid var(--rule);max-width:120px}
.menu{display:flex;align-items:center;gap:22px;list-style:none;margin:0;padding:0}
.menu a{text-decoration:none;font-size:15px;font-weight:500;color:var(--ink);padding-block:6px;border-bottom:2px solid transparent;white-space:nowrap}
.menu a:hover,.menu a[aria-current="page"]{border-bottom-color:var(--brass)}
.menu .cta a{border:1.5px solid var(--brass);color:var(--navy);padding:9px 16px;border-radius:2px}
.menu .cta a:hover,.menu .cta a[aria-current="page"]{background:var(--brass);border-color:var(--brass);color:var(--navy)}
.navtoggle{display:none;background:none;border:1.5px solid var(--rule);border-radius:2px;padding:8px 10px;font:inherit;font-size:14px;color:var(--ink);cursor:pointer}
/* the header descriptor needs 1280px or more alongside the eight menu items */
@media (max-width:1279px){.nav .brand .desc{display:none}}
@media (max-width:1160px){
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
.cands li{display:grid;grid-template-columns:16px 1fr auto;grid-template-areas:"mark name status" "mark why why" "mark checks checks";column-gap:12px;row-gap:3px;padding:13px 18px;border-bottom:1px solid var(--rule);align-items:start}
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
.c-checks{grid-area:checks;display:flex;flex-wrap:wrap;gap:5px;margin-top:5px}
.c-checks span{font-size:11.5px;line-height:1.5;font-weight:500;color:var(--navy);background:var(--stone);border:1px solid var(--rule);padding:1px 7px;border-radius:2px;white-space:nowrap}
.c-checks .ok::before{content:"\2713";color:var(--brass);font-weight:700;margin-right:4px}
.c-checks .gap{background:transparent;border-style:dashed;border-color:var(--ink-soft);color:var(--ink-soft)}
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
  .cands li{grid-template-columns:16px 1fr;grid-template-areas:"mark name" "mark status" "mark why" "mark checks"}
  .c-status{white-space:normal}
}

/* ---------- Sections ---------- */
.section{padding-block:clamp(56px,7vw,96px)}
.section.stone{background:var(--stone)}
.section.tight{padding-block:clamp(40px,5vw,64px)}
.two{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,7fr);gap:clamp(28px,5vw,80px);align-items:start}
.two h2,.h2{font-size:clamp(28px,3vw,38px);line-height:1.15;color:var(--navy)}
.h3{font-family:var(--display);font-size:24px;line-height:1.25;color:var(--navy)}
.prose{display:grid;gap:18px;max-width:64ch;font-size:17.5px;overflow-wrap:anywhere}
.prose ul,.prose ol{margin:0;padding-left:22px;display:grid;gap:10px}
.prose li::marker{color:var(--brass)}
.prose strong{font-weight:600;color:var(--navy)}
.prose .h3{margin-top:10px}
.kicker{display:block;width:44px;height:3px;background:var(--brass);margin-bottom:20px}
.sub{margin-top:14px;max-width:62ch;color:var(--ink-soft);font-size:18px}
.cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(24px,4vw,56px);margin-top:clamp(32px,4vw,48px)}
.cols.two-up{grid-template-columns:repeat(2,minmax(0,1fr))}
.cols.four-up{grid-template-columns:repeat(4,minmax(0,1fr))}
.col{border-top:1px solid var(--rule);padding-top:22px;min-width:0}
.col h3{font-size:23px;line-height:1.25;color:var(--navy)}
.col p{margin-top:12px;color:var(--ink-soft);font-size:17px}
.col p+p{margin-top:10px}
.steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(22px,3vw,40px) clamp(24px,4vw,56px);margin-top:clamp(32px,4vw,48px);counter-reset:step;list-style:none;padding:0;margin-inline:0}
.steps.two-up{grid-template-columns:repeat(2,minmax(0,1fr))}
.steps li{counter-increment:step;display:grid;grid-template-columns:auto 1fr;gap:16px;align-items:start;min-width:0}
.steps li::before{content:counter(step,decimal-leading-zero);font-family:var(--display);font-size:30px;line-height:1;color:var(--brass);padding-top:2px;min-width:2ch;font-variant-numeric:tabular-nums}
.steps b{display:block;font-weight:600;color:var(--navy);font-size:18px}
.steps p{margin-top:6px;color:var(--ink-soft);font-size:17px}
.scale{list-style:none;margin:0;padding:0;border-top:1px solid var(--rule)}
.scale li{display:grid;grid-template-columns:16px 1fr;gap:14px;padding:16px 0;border-bottom:1px solid var(--rule);align-items:start}
.scale .mark{margin-top:6px}
.scale b{display:block;font-weight:600;color:var(--navy)}
.scale span{display:block;color:var(--ink-soft);font-size:16.5px;margin-top:2px}
.note{border-left:3px solid var(--brass);background:var(--stone);padding:18px 22px;max-width:64ch;font-size:16px;color:var(--ink)}
.note b{color:var(--navy);font-weight:600}
.section.stone .note{background:var(--paper)}
.facts{list-style:none;margin:0;padding:0;border-top:1px solid var(--rule)}
.prose .facts{padding-left:0;display:block}
.facts li{display:grid;grid-template-columns:minmax(120px,180px) 1fr;gap:16px;padding:16px 0;border-bottom:1px solid var(--rule)}
.facts b{font:600 13px/1.4 var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--brass);padding-top:3px}
.exp{list-style:none;margin:clamp(28px,4vw,40px) 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px clamp(24px,3vw,44px)}
.exp li{border-top:1px solid var(--rule);padding-top:18px;min-width:0}
.exp b{display:block;font:600 13px/1.4 var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--brass);margin-bottom:8px}
.exp span{display:block;color:var(--ink);font-size:16.5px;line-height:1.6}
@media (max-width:1100px){.exp{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:700px){.exp{grid-template-columns:1fr}}
.facts span{color:var(--ink);font-size:16.5px}
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
/* Offset alerts: a calm dated list of new defence sales (sources are not shown) */
.vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.sechead{display:flex;justify-content:space-between;align-items:flex-end;gap:16px 32px;flex-wrap:wrap}
.sechead .more{font-size:15px;font-weight:600;color:var(--navy);text-decoration:none;border-bottom:1.5px solid var(--brass);padding-bottom:2px;white-space:nowrap}
.sechead .more:hover{color:var(--brass)}
.updated{margin-top:10px;font-size:13.5px;color:var(--ink-soft)}
.alerts{list-style:none;margin:clamp(28px,4vw,40px) 0 0;padding:0;border-top:1px solid var(--rule)}
.alerts li{display:grid;grid-template-columns:minmax(140px,180px) minmax(0,1fr);gap:6px 36px;padding:22px 0;border-bottom:1px solid var(--rule)}
.a-meta{display:flex;flex-direction:column;gap:3px;padding-top:4px}
.a-meta b{font-size:12.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--brass)}
.a-meta time{font-size:13.5px;color:var(--ink-soft);font-variant-numeric:tabular-nums}
.a-title{font-family:var(--display);font-size:clamp(19px,1.6vw,21px);line-height:1.32;color:var(--navy)}
.a-title a{text-decoration:none;background-image:linear-gradient(var(--brass),var(--brass));background-repeat:no-repeat;background-position:0 100%;background-size:0 1px;transition:background-size .2s}
.a-title a:hover,.a-title a:focus-visible{background-size:100% 1px}
.a-sum{margin-top:8px;color:var(--ink-soft);font-size:16.5px;max-width:72ch}
.a-src{margin-top:10px;font-size:13.5px;color:var(--ink-soft)}
.a-src a{color:var(--navy);font-weight:500;text-decoration:none;border-bottom:1px solid var(--brass)}
.a-src a:hover{color:var(--brass)}
.arrow{display:inline-block;margin-left:3px;font-family:var(--body);font-size:.85em;color:var(--brass)}
@media (max-width:700px){
  .alerts li{grid-template-columns:1fr}
  .a-meta{flex-direction:row;gap:10px;align-items:baseline;padding-top:0}
  .a-meta time::before{content:"·";margin-right:10px;color:var(--rule)}
}
@media (max-width:900px){
  .two{grid-template-columns:1fr}
  .cols,.cols.two-up,.cols.four-up,.steps,.steps.two-up{grid-template-columns:1fr}
  .facts li{grid-template-columns:1fr;gap:4px}
}
@media (min-width:901px) and (max-width:1100px){
  .cols,.cols.four-up,.steps{grid-template-columns:repeat(2,minmax(0,1fr))}
}
.col .meta{display:block;font:600 12.5px/1.3 var(--body);letter-spacing:.09em;text-transform:uppercase;color:var(--brass);margin-bottom:10px}
.panel .actions{margin-top:22px;gap:12px}
.panel .actions .btn{margin-top:0}
.pagehead .actions{margin-top:30px}

/* ---------- Training page ---------- */
.figs{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:24px clamp(16px,2.4vw,32px)}
.figs li{border-top:1px solid var(--rule);padding-top:16px;min-width:0}
.figs b{display:block;font-family:var(--display);font-weight:400;font-size:clamp(38px,3.6vw,50px);line-height:1;color:var(--navy);font-variant-numeric:lining-nums}
.figs span{display:block;margin-top:10px;font-size:15.5px;line-height:1.45;color:var(--ink-soft)}
@media (max-width:1100px){.figs{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:560px){.figs{grid-template-columns:repeat(2,minmax(0,1fr))}}
.steps.four-up{grid-template-columns:repeat(4,minmax(0,1fr))}
@media (min-width:901px) and (max-width:1100px){.steps.four-up{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:900px){.steps.four-up{grid-template-columns:1fr}}
.dlist{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.dlist li{position:relative;padding-left:22px;font-size:16.5px;line-height:1.55;color:var(--ink)}
.dlist li::before{content:"";position:absolute;left:2px;top:.62em;width:7px;height:7px;background:var(--brass);transform:rotate(45deg)}
.col .dlist{margin-top:16px}
/* the offset life cycle, module by module */
.path{list-style:none;margin:clamp(32px,4vw,44px) 0 0;padding:0;display:grid;grid-template-columns:repeat(7,minmax(0,1fr))}
.path li{position:relative;padding:30px 14px 0 0;min-width:0}
.path li::before{content:"";position:absolute;left:1px;top:3px;width:12px;height:12px;background:var(--brass);transform:rotate(45deg)}
.path li::after{content:"";position:absolute;left:26px;right:10px;top:9px;height:1px;background:var(--brass-light)}
.path li:last-child::after{display:none}
.path .pm{display:block;font:600 12px/1.3 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--brass)}
.path b{display:block;margin-top:6px;font-family:var(--display);font-weight:400;font-size:19px;line-height:1.25;color:var(--navy)}
@media (max-width:1000px){
  .path{grid-template-columns:1fr}
  .path li{padding:0 0 18px 34px}
  .path li::before{top:5px}
  .path li::after{left:7px;right:auto;top:24px;bottom:2px;width:1px;height:auto}
  .path b{margin-top:2px}
}
/* modules: one card each, opened for detail */
.modhead{display:flex;justify-content:space-between;align-items:baseline;gap:12px 24px;flex-wrap:wrap;margin-top:clamp(36px,4.5vw,52px)}
.modnote{font-size:15.5px;color:var(--ink-soft)}
.linkbtn{font:600 15px var(--body);color:var(--navy);background:none;border:0;border-bottom:1.5px solid var(--brass);padding:0 0 2px;cursor:pointer}
.linkbtn:hover{color:var(--brass)}
.mods{display:grid;gap:10px;margin-top:16px}
.mod{background:var(--paper);border:1px solid var(--rule);border-radius:2px}
.mod[open]{box-shadow:inset 3px 0 0 var(--brass)}
.mod summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:150px minmax(0,1fr) 22px;gap:4px 24px;align-items:start;padding:22px clamp(18px,2.6vw,30px)}
.mod summary::-webkit-details-marker{display:none}
.mod summary:hover .mtitle{color:var(--navy-mid)}
.mnum{font:600 12.5px/1.3 var(--body);letter-spacing:.09em;text-transform:uppercase;color:var(--brass);padding-top:7px}
.mhead{min-width:0}
.mtitle{font-size:clamp(21px,2vw,25px);line-height:1.25;color:var(--navy)}
.mq{display:block;margin-top:6px;font-size:16.5px;color:var(--ink-soft)}
.mtog{position:relative;width:22px;height:22px;margin-top:5px}
.mtog::before,.mtog::after{content:"";position:absolute;left:4px;right:4px;top:10px;height:2px;background:var(--brass);transition:transform .2s}
.mtog::after{transform:rotate(90deg)}
.mod[open] .mtog::after{transform:rotate(0deg)}
.mbody{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:22px clamp(24px,4vw,56px);padding:0 clamp(18px,2.6vw,30px) 26px calc(174px + clamp(18px,2.6vw,30px))}
.mbody h4{margin:0 0 12px;font:600 12.5px/1.3 var(--body);letter-spacing:.09em;text-transform:uppercase;color:var(--ink-soft)}
.mfacts{margin:0;display:grid;gap:12px}
.mfacts div{border-top:1px solid var(--rule);padding-top:10px}
.mfacts dt{font:600 12.5px/1.3 var(--body);letter-spacing:.09em;text-transform:uppercase;color:var(--brass)}
.mfacts dd{margin:4px 0 0;font-size:16.5px;line-height:1.5;color:var(--navy)}
@media (max-width:900px){
  .mod summary{grid-template-columns:minmax(0,1fr) 22px;row-gap:8px}
  .mnum{grid-column:1;grid-row:1;padding-top:2px}
  .mtog{grid-column:2;grid-row:1;margin-top:0}
  .mhead{grid-column:1 / -1;grid-row:2}
  .mbody{grid-template-columns:1fr;padding-left:clamp(18px,2.6vw,30px)}
}
/* the capstone: a navy feature section */
.section.navy{background:linear-gradient(118deg,var(--navy-mid) 0%,var(--navy) 50%,var(--navy-deep) 100%);color:var(--on-navy)}
.section.navy h2{color:#fff}
.section.navy .sub{color:var(--on-navy-soft)}
.section.navy .prose{color:var(--on-navy)}
.section.navy .facts{border-top-color:rgba(255,255,255,.18);margin-top:8px}
.section.navy .facts li{border-bottom-color:rgba(255,255,255,.18)}
.section.navy .facts b{color:var(--brass-light)}
.section.navy .facts span{color:var(--on-navy)}
/* the two formats */
.sched{list-style:none;margin:18px 0 0;padding:0;border-top:1px solid var(--rule)}
.sched li{display:grid;grid-template-columns:minmax(92px,120px) minmax(0,1fr);gap:12px;padding:10px 0;border-bottom:1px solid var(--rule);font-size:16px}
.sched b{font-weight:600;color:var(--navy)}
.sched span{color:var(--ink-soft)}
/* the self-test: one question at a time once the script runs; all questions with answers if it does not */
.quiz{background:var(--paper);border:1px solid var(--rule);border-top:3px solid var(--brass);border-radius:2px;padding:clamp(20px,3vw,32px);min-width:0}
.qtop{display:flex;justify-content:space-between;gap:12px;font:600 12.5px/1.3 var(--body);letter-spacing:.09em;text-transform:uppercase;color:var(--brass);margin-bottom:16px}
.qtally{color:var(--ink-soft)}
.qlist{list-style:none;margin:0;padding:0}
.q+.q{margin-top:28px;padding-top:24px;border-top:1px solid var(--rule)}
.quiz.js .q{display:none}
.quiz.js .q.current{display:block;margin-top:0;padding-top:0;border-top:0}
.qtext{font-family:var(--display);font-size:clamp(19px,1.7vw,22px);line-height:1.38;color:var(--navy)}
.qtext:focus{outline:none}
.opts{list-style:none;margin:18px 0 0;padding:0;display:grid;gap:10px}
.opt{display:grid;grid-template-columns:28px minmax(0,1fr);gap:12px;align-items:center;width:100%;text-align:left;font:inherit;font-size:16.5px;line-height:1.45;color:var(--ink);background:var(--paper);border:1.5px solid var(--rule);border-radius:2px;padding:11px 14px;cursor:pointer;transition:border-color .15s,background-color .15s}
.opt:hover:not(:disabled){border-color:var(--navy)}
.opt:disabled{cursor:default;color:var(--ink)}
.opt .ol{display:flex;align-items:center;justify-content:center;width:28px;height:28px;border:1.5px solid var(--rule);border-radius:50%;font:600 13px/1 var(--body);color:var(--navy);background:var(--paper)}
.opt.right{border-color:#2E6B4F;background:#EEF5F1}
.opt.right .ol{background:#2E6B4F;border-color:#2E6B4F;color:#fff}
.opt.wrong{border-color:#A33D2F;background:#FBEFEC}
.opt.wrong .ol{background:#A33D2F;border-color:#A33D2F;color:#fff}
.why{margin-top:16px;padding:14px 16px;background:var(--stone);border-left:3px solid var(--brass);font-size:16px;line-height:1.55;color:var(--ink)}
.why b{color:var(--navy);font-weight:600}
.quiz.js .why{display:none}
.quiz.js .q.answered .why{display:block}
.qnav{margin-top:20px;display:flex;justify-content:flex-end}
.qbig{font-family:var(--display);font-size:clamp(26px,2.6vw,32px);line-height:1.2;color:var(--navy)}
.qmsg{margin-top:10px;font-size:17px;color:var(--ink-soft)}
.qresult .actions{margin-top:22px}
.qresult:focus{outline:none}
/* Offset wire: a thin strip under the header on the home page. One item at a time, fading to the next; pauses on hover; still with reduced motion */
.wire{background:var(--stone);border-bottom:1px solid var(--rule)}
.wire .wrap{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;gap:18px;min-height:46px;padding-block:7px}
.wire .label{font:600 12px/1.3 var(--body);letter-spacing:.1em;text-transform:uppercase;color:var(--brass);white-space:nowrap;display:flex;align-items:center;gap:9px}
.wire .label::before{content:"";width:7px;height:7px;background:var(--brass);transform:rotate(45deg)}
.wire .item{min-width:0;font-size:15px;line-height:1.4;color:var(--ink);transition:opacity .45s ease}
.wire .item.out{opacity:0}
.wire .item a{display:block;text-decoration:none;color:inherit;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wire .item a:hover .w-title{border-bottom-color:var(--brass)}
.wire .w-country{font-weight:600;letter-spacing:.06em;text-transform:uppercase;font-size:12.5px;color:var(--navy)}
.wire .w-date{color:var(--ink-soft);font-size:13.5px;font-variant-numeric:tabular-nums;margin:0 10px}
.wire .w-date::before{content:"·";margin-right:10px;color:var(--brass)}
.wire .w-title{border-bottom:1px solid transparent;transition:border-color .15s}
.wire .ctl{display:flex;align-items:center;gap:4px;white-space:nowrap}
.wire .ctl button{font:inherit;font-size:15px;line-height:1;color:var(--navy);background:transparent;border:1px solid var(--rule);border-radius:2px;width:30px;height:30px;cursor:pointer}
.wire .ctl button:hover{border-color:var(--brass);color:var(--brass)}
.wire .ctl .count{font-size:12.5px;color:var(--ink-soft);font-variant-numeric:tabular-nums;margin:0 8px}
.wire .ctl .all{font-size:13.5px;font-weight:600;color:var(--navy);text-decoration:none;border-bottom:1.5px solid var(--brass);margin-left:10px;padding-bottom:1px}
.wire .ctl .all:hover{color:var(--brass)}
@media (max-width:700px){
  .wire .wrap{grid-template-columns:minmax(0,1fr) auto;row-gap:4px}
  .wire .label{display:none}
  .wire .item a{white-space:normal;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
  .wire .ctl .all,.wire .ctl .count{display:none}
}
/* Home panel: the newest alerts as cards, three across */
.agrid{list-style:none;margin:clamp(28px,4vw,40px) 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0 clamp(24px,3vw,44px)}
.agrid li{border-top:1px solid var(--rule);padding:20px 0 26px;min-width:0;display:flex;flex-direction:column}
.agrid .a-eyebrow{display:flex;align-items:baseline;flex-wrap:wrap;gap:4px 10px;font-size:12.5px}
.agrid .a-eyebrow b{font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--brass)}
.agrid .a-eyebrow time{color:var(--ink-soft);font-size:13.5px;font-variant-numeric:tabular-nums}
.agrid .a-title{margin-top:10px;font-size:clamp(18px,1.5vw,20px);line-height:1.32}
.agrid .a-sum{margin-top:8px;font-size:15.5px;line-height:1.55;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
.agrid .a-src{margin-top:auto;padding-top:12px;font-size:13px}
.tag{display:inline-block;font:600 11px/1.5 var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--navy);background:var(--brass-pale);padding:0 7px;border-radius:2px;vertical-align:1px}
@media (max-width:1100px){.agrid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:700px){.agrid{grid-template-columns:1fr}}
/* Alerts page: items grouped by the week they were added */
.week{margin-top:clamp(32px,4vw,48px)}
.week:first-of-type{margin-top:clamp(24px,3vw,32px)}
.week>h3{font:600 13px/1.4 var(--body);letter-spacing:.09em;text-transform:uppercase;color:var(--brass);padding-bottom:12px;border-bottom:2px solid var(--brass);display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
.week>h3 span{font-weight:500;letter-spacing:0;text-transform:none;color:var(--ink-soft)}
.week .alerts{margin-top:0;border-top:0}
.retain{margin-top:28px;max-width:72ch;font-size:15px;color:var(--ink-soft)}

/* ---------- Course modules (training page) ---------- */
.modules{list-style:none;margin:clamp(32px,4vw,48px) 0 0;padding:0;border-top:1px solid var(--rule)}
.modules>li{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:16px clamp(24px,5vw,80px);padding:clamp(26px,3vw,36px) 0;border-bottom:1px solid var(--rule)}
.modules .num{display:block;font:600 12.5px/1.3 var(--body);letter-spacing:.09em;text-transform:uppercase;color:var(--brass);margin-bottom:12px}
.modules h3{font-size:clamp(22px,2.1vw,26px);line-height:1.25;color:var(--navy)}
.modules .focus{margin-top:10px;color:var(--ink-soft);font-size:16px;max-width:44ch}
.modules ul{list-style:none;margin:0;padding:0;display:grid;gap:14px}
.modules ul li{position:relative;padding-left:22px;font-size:16px;color:var(--ink-soft)}
.modules ul li::before{content:"";position:absolute;left:2px;top:.62em;width:7px;height:7px;background:var(--brass);transform:rotate(45deg)}
.modules ul b{font-weight:600;color:var(--navy)}
@media (max-width:900px){.modules>li{grid-template-columns:1fr}}

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

  // Training page: open or close every module at once, and open a module named in the address
  var ea=document.getElementById('expandall'),mods=document.querySelectorAll('details.mod');
  if(ea&&mods.length){
    ea.hidden=false;
    ea.addEventListener('click',function(){
      var o=ea.getAttribute('aria-expanded')!=='true';
      Array.prototype.forEach.call(mods,function(d){d.open=o;});
      ea.setAttribute('aria-expanded',o?'true':'false');
      ea.textContent=o?'Close all modules':'Open all modules';
    });
  }
  if(/^#module-\d$/.test(location.hash)){var md=document.querySelector(location.hash);if(md)md.open=true;}

  // Training page: the self-test, one question at a time (in its own scope, so its names cannot clash with other page scripts)
  (function(){
    var qz=document.getElementById('quiz');
    if(!qz)return;
    var each=Array.prototype.forEach,qs=qz.querySelectorAll('.q'),total=qs.length,cur=0,score=0,
        list=qz.querySelector('.qlist'),nav=qz.querySelector('.qnav'),next=qz.querySelector('.qnext'),
        res=qz.querySelector('.qresult'),cnt=qz.querySelector('.qcount'),tally=qz.querySelector('.qtally'),
        live=qz.querySelector('.qlive');
    qz.classList.add('js');
    // Bring the top of the quiz into view below the sticky header, then move focus without a second jump
    var nb=document.querySelector('.nav');
    var bring=function(el){
      var off=(nb?nb.getBoundingClientRect().bottom:0)+16,top=qz.getBoundingClientRect().top;
      if(top<off||top>window.innerHeight/3)window.scrollBy(0,top-off);
      try{el.focus({preventScroll:true});}catch(e){el.focus();}
    };
    var show=function(i){
      each.call(qs,function(q,k){q.classList.toggle('current',k===i);});
      cnt.textContent='Question '+(i+1)+' of '+total;nav.hidden=true;
    };
    var reset=function(){
      cur=0;score=0;tally.textContent='';res.hidden=true;list.hidden=false;
      each.call(qs,function(q){
        q.classList.remove('answered');
        var v=q.querySelector('.verdict');v.textContent=v.getAttribute('data-label');
        each.call(q.querySelectorAll('.opt'),function(b){b.disabled=false;b.classList.remove('right','wrong');});
      });
      show(0);
    };
    each.call(qs,function(q){
      var ans=+q.getAttribute('data-answer'),v=q.querySelector('.verdict'),ex=q.querySelector('.expl');
      v.setAttribute('data-label',v.textContent);
      q.addEventListener('click',function(e){
        var b=e.target.closest?e.target.closest('.opt'):null;
        if(!b||q.classList.contains('answered'))return;
        var ok=(+b.getAttribute('data-i'))===ans;
        q.classList.add('answered');
        each.call(q.querySelectorAll('.opt'),function(x,k){x.disabled=true;if(k===ans)x.classList.add('right');});
        if(ok){score++;}else{b.classList.add('wrong');}
        v.textContent=ok?'Correct.':'Not quite. '+v.getAttribute('data-label');
        tally.textContent=score+' correct';
        live.textContent=v.textContent+' '+ex.textContent;
        next.textContent=cur===total-1?'See your score':'Next question';
        nav.hidden=false;next.focus();
      });
    });
    next.addEventListener('click',function(){
      if(cur<total-1){cur++;show(cur);bring(qs[cur].querySelector('.qtext'));return;}
      list.hidden=true;nav.hidden=true;cnt.textContent='Your result';
      var band=score===total?'top':(score>=total-2?'mid':'low');
      res.querySelector('.qbig').textContent='You scored '+score+' out of '+total+'.';
      each.call(res.querySelectorAll('.qmsg'),function(p){p.hidden=p.getAttribute('data-band')!==band;});
      res.hidden=false;bring(res);
    });
    qz.querySelector('.qagain').addEventListener('click',function(){reset();bring(qs[0].querySelector('.qtext'));});
    reset();
  })();
  // Offset wire: one headline at a time. Fades to the next every 7 seconds; pauses while hovered or focused;
  // with reduced motion it stays on the newest item and the arrows still work.
  var wire=document.getElementById('wire');
  if(wire){
    var data=[];try{data=JSON.parse(wire.getAttribute('data-items')||'[]');}catch(e){}
    var slot=wire.querySelector('.item'),cnt=wire.querySelector('.count'),i=0,timer=null,paused=false;
    var still=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function render(){var d=data[i];if(!d)return;
      slot.innerHTML='<a href="'+d.href+'"><span class="w-country">'+d.country+'</span><span class="w-date">'+d.date+'</span><span class="w-title">'+d.title+'</span></a>';
      if(cnt)cnt.textContent=(i+1)+' / '+data.length;}
    function show(n){i=(n+data.length)%data.length;
      if(still){render();return;}
      slot.classList.add('out');setTimeout(function(){render();slot.classList.remove('out');},450);}
    function start(){if(still||data.length<2)return;stop();timer=setInterval(function(){if(!paused)show(i+1);},7000);}
    function stop(){if(timer){clearInterval(timer);timer=null;}}
    if(data.length){render();start();}
    var prev=wire.querySelector('[data-prev]'),next=wire.querySelector('[data-next]');
    if(prev)prev.addEventListener('click',function(){show(i-1);start();});
    if(next)next.addEventListener('click',function(){show(i+1);start();});
    wire.addEventListener('mouseenter',function(){paused=true;});wire.addEventListener('mouseleave',function(){paused=false;});
    wire.addEventListener('focusin',function(){paused=true;});wire.addEventListener('focusout',function(){paused=false;});
    document.addEventListener('visibilitychange',function(){if(document.hidden)stop();else start();});
  }

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
    g.fillText('SHEET 1 OF 1',tbx+8,tby+14);g.fillText('SCALE 1:2',tbx+96,tby+14);g.fillText('GIMBAL ASSY',tbx+8,tby+34);g.fillText('REV B',tbx+96,tby+34);
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
    ("advisory.html", "Advisory"),
    ("training.html", "Training"),
    ("uk-icr.html", "Roundtable"),
    ("offset-alerts.html", "Offset alerts"),
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
    <div><h4>Services</h4><ul><li><a href="advisory.html">Advisory</a></li><li><a href="training.html">Offset practitioner course</a></li><li><a href="uk-icr.html">UK-ICR Roundtable</a></li><li><a href="offset-alerts.html">Offset alerts</a></li><li><a href="industrial-participation.html">Industrial participation</a></li><li><a href="uk-companies.html">For UK companies</a></li></ul></div>
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

def pagehead(title, lede, crumb=None, extra=""):
    crumb_html = ""
    if crumb:
        crumb_html = '<div class="crumb"><a href="index.html">Home</a>' + "".join(
            f'<span>{html.escape(c) if isinstance(c,str) else f"<a href=\"{c[0]}\">{c[1]}</a>"}</span>' for c in crumb) + "</div>"
    return f"""
<section class="pagehead"><canvas id="drawing" aria-hidden="true"></canvas><div class="wrap">
  {crumb_html}<h1>{title}</h1><p class="lede">{lede}</p>{extra}
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

_TAG = re.compile(r"(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)", re.S)
def _cap_text(t):
    t = re.sub(r"\bindustrial participation\b", "Industrial Participation", t, flags=re.I)
    t = re.sub(r"\boffset(s?)\b", lambda m: "Offset" + m.group(1), t)
    return t
def cap_terms(doc):
    """Capitalise the key terms Industrial Participation and Offset in visible text and page descriptions."""
    out = []
    for part in _TAG.split(doc):
        if not part:
            continue
        if part.startswith("<script") or part.startswith("<style"):
            out.append(part)
        elif part.startswith("<"):
            if part.startswith("<meta") and ('name="description"' in part or 'property="og:' in part):
                part = re.sub(r'content="([^"]*)"', lambda m: 'content="' + _cap_text(m.group(1)) + '"', part)
            out.append(part)
        else:
            out.append(_cap_text(part))
    return "".join(out)

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
    return cap_terms(doc)

# ---------------------------------------------------------------- offset alerts (data in tools/alerts.json)
# alerts.json is the permanent record: items are never deleted there. The site shows the items added in the last
# three weeks (WINDOW_DAYS before "updated"); if that leaves fewer than MIN_SHOWN, the newest older items make up the number.
_alerts_file = os.path.join(ROOT, "alerts.json")
with open(_alerts_file) as f:
    _AL = json.load(f)
_upd = datetime.date.fromisoformat(_AL["updated"])
ALERTS_UPDATED = f"{_upd.day} {_upd.strftime('%B %Y')}"
WINDOW_DAYS, MIN_SHOWN, MAX_SHOWN, HOME_CARDS, WIRE_ITEMS = 21, 8, 30, 9, 10

def _d(ym):
    """A full date for sorting: 'YYYY-MM-DD' as is, 'YYYY-MM' as the first of that month."""
    return datetime.date.fromisoformat(ym if len(ym) == 10 else ym + "-01")

def when(ym):
    """Shown date: '5 October 2026' for a full date, 'October 2026' when only the month is known."""
    d = _d(ym)
    return f"{d.day} {d.strftime('%B %Y')}" if len(ym) == 10 else d.strftime("%B %Y")

def when_short(ym):
    d = _d(ym)
    return f"{d.day} {d.strftime('%b')}" if len(ym) == 10 else d.strftime("%b %Y")

for _n, _a in enumerate(_AL["items"]):
    _a.setdefault("added", _AL["updated"])
    _a["id"] = "a" + _d(_a["added"]).strftime("%Y%m%d") + "-" + str(_n)
# newest first: by the week added, then by event date; items with the same dates keep the order they have in the file
_all = sorted(_AL["items"], key=lambda a: (_d(a["added"]), _d(a["date"])), reverse=True)
_cutoff = _upd - datetime.timedelta(days=WINDOW_DAYS)
ALERTS = [a for a in _all if _d(a["added"]) >= _cutoff]
if len(ALERTS) < MIN_SHOWN:
    ALERTS = _all[:MIN_SHOWN]
ALERTS = ALERTS[:MAX_SHOWN]

def _esc(a):
    return {k: html.escape(str(v)) for k, v in a.items()}

def _tag(a):
    return f' <span class="tag">{html.escape(a["tag"])}</span>' if a.get("tag") else ""

def alert_list(items):
    rows = []
    for a in items:
        e = _esc(a)
        rows.append(f"""<li id="{e['id']}">
      <div class="a-meta"><b>{e['country']}{_tag(a)}</b><time datetime="{e['date']}">{when(a['date'])}</time></div>
      <div>
        <h3 class="a-title">{e['title']}</h3>
        <p class="a-sum">{e['summary']}</p>
      </div>
    </li>""")
    return '<ul class="alerts">' + "\n    ".join(rows) + "</ul>"

def alert_cards(items):
    rows = []
    for a in items:
        e = _esc(a)
        rows.append(f"""<li>
      <div class="a-eyebrow"><b>{e['country']}</b>{_tag(a)}<time datetime="{e['date']}">{when(a['date'])}</time></div>
      <h3 class="a-title"><a href="offset-alerts.html#{e['id']}">{e['title']}</a></h3>
      <p class="a-sum">{e['summary']}</p>
    </li>""")
    return '<ul class="agrid">' + "\n    ".join(rows) + "</ul>"

def alert_weeks(items):
    """The alerts page: items grouped under the Monday of the week they were added."""
    groups, order = {}, []
    for a in items:
        d = _d(a["added"]); monday = d - datetime.timedelta(days=d.weekday())
        if monday not in groups:
            groups[monday] = []; order.append(monday)
        groups[monday].append(a)
    out = []
    for monday in order:
        n = len(groups[monday])
        out.append(f'<div class="week"><h3>Week of {monday.day} {monday.strftime("%B %Y")}<span>{n} alert{"s" if n != 1 else ""}</span></h3>{alert_list(groups[monday])}</div>')
    return "\n".join(out)

def wire(items):
    data = [dict(country=a["country"], date=when_short(a["date"]), title=_cap_text(a["title"]), href="offset-alerts.html#" + a["id"]) for a in items]
    first = data[0]
    return f"""
<div class="wire" id="wire" data-items="{html.escape(json.dumps(data), quote=True)}" aria-label="Offset wire: latest alerts">
  <div class="wrap">
    <span class="label">Offset wire</span>
    <div class="item"><a href="{first['href']}"><span class="w-country">{html.escape(first['country'])}</span><span class="w-date">{first['date']}</span><span class="w-title">{html.escape(first['title'])}</span></a></div>
    <div class="ctl"><button type="button" data-prev aria-label="Previous alert">&#8249;</button><span class="count" aria-hidden="true">1 / {len(data)}</span><button type="button" data-next aria-label="Next alert">&#8250;</button><a class="all" href="offset-alerts.html">All alerts</a></div>
  </div>
</div>"""

HOME_WIRE = wire(ALERTS[:WIRE_ITEMS])

HOME_ALERTS = f"""
<section class="section" aria-labelledby="alerts-title"><div class="wrap">
  <div class="sechead">
    <div><span class="kicker" aria-hidden="true"></span><h2 class="h2" id="alerts-title">Latest offset alerts</h2>
      <p class="sub">A weekly round-up of new defence sales around the world above the offset thresholds, and changes to the offset rules.</p>
      <p class="updated">Checked weekly. Last updated {ALERTS_UPDATED}.</p></div>
    <a class="more" href="offset-alerts.html">See all offset alerts</a>
  </div>
  {alert_cards(ALERTS[:HOME_CARDS])}
</div></section>"""

# ---------------------------------------------------------------- pages
PAGES = {}

PAGES["index.html"] = dict(title="Home", desc="Capital helps overseas defence companies meet UK industrial participation commitments, with an evidence-based platform for finding credible UK industrial partners and more than 25 years of offset experience.", body=f"""{HOME_WIRE}
<section class="hero" aria-labelledby="hero-title">
  <canvas id="drawing" aria-hidden="true"></canvas>
  <div class="wrap">
    <div>
      <h1 id="hero-title">Find credible UK industrial partners for your defence programme</h1>
      <p class="lede">Capital helps overseas defence companies meet UK industrial participation commitments, with an evidence-based search platform and more than 25 years of offset experience.</p>
      <div class="actions">
        <a class="btn btn-brass" href="request-access.html">Request platform access</a>
        <a class="btn btn-ghost" href="platform.html">How the platform works</a>
      </div>
      <p class="audience">For overseas primes and their UK subsidiaries preparing bids and participation plans</p>
    </div>
    <aside class="card" aria-label="Example of a platform shortlist">
      <div class="card-top"><b>Shortlist</b><span>Line 14 of 38</span></div>
      <div class="part"><div class="part-name">Stabilised EO/IR camera gimbal, two-axis</div><div class="part-meta">Airborne surveillance pod · AS9100 required · 60 units a year · unclassified description</div></div>
      <ol class="cands">
        <li><span class="mark" aria-hidden="true"></span><div class="c-name">Calder Vale Optronics Ltd <em>SME</em><br><span>Edinburgh</span></div><div class="c-status">Can make this now</div><div class="c-why">Stabilised airborne camera gimbals shown on its own website</div><div class="c-checks"><span class="ok">AS9100D</span><span class="ok">Cyber Essentials Plus</span><span class="ok">Finances: strong</span><span class="ok">UK-owned</span><span class="info">3 MOD contracts since 2023</span></div></li>
        <li><span class="mark" aria-hidden="true"></span><div class="c-name">Severnbank Motion Systems Ltd<br><span>Gloucester</span></div><div class="c-status">Can make this now</div><div class="c-why">Precision pointing and stabilisation assemblies for aircraft</div><div class="c-checks"><span class="ok">AS9100D</span><span class="ok">Cyber Essentials Plus</span><span class="ok">Finances: strong</span><span class="info">Owned by a US group</span><span class="info">Tier 2 to UK primes</span></div></li>
        <li><span class="mark support" aria-hidden="true"></span><div class="c-name">Fenwick Gear &amp; Motion Ltd <em>SME</em><br><span>Coventry</span></div><div class="c-status">Could make this with support</div><div class="c-why">Precision gearboxes and motor housings for industrial robots</div><div class="c-checks"><span class="ok">ISO 9001</span><span class="gap">AS9100 not recorded</span><span class="ok">Finances: adequate</span><span class="ok">UK-owned</span><span class="info">Growth candidate for defence</span></div></li>
      </ol>
      <div class="card-foot"><span>Illustrative example</span><a href="platform.html#labels">What each label means</a></div>
    </aside>
  </div>
</section>

<section class="section" aria-labelledby="challenge-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="challenge-title">The challenge</h2></div>
  <div class="prose">
    <p>The UK expects overseas suppliers to invest in its defence industry. Meeting that expectation means finding UK companies that can genuinely make your parts, develop your technology or support your programme, and finding them early.</p>
    <p>A web search turns up distributors, sales offices and advertisers alongside real manufacturers. Reviewing their capabilities, financial health, compliance and certifications takes a significant investment of time.</p>
    <p><a href="industrial-participation.html">About UK industrial participation</a></p>
  </div>
</div></section>

<section class="section stone" aria-labelledby="offers-title"><div class="wrap">
  <span class="kicker" aria-hidden="true"></span><h2 class="h2" id="offers-title">What Capital offers</h2>
  <div class="cols">
    <div class="col"><h3>The UK Defence Localisation Platform</h3><p>Upload a parts list and receive a reasoned shortlist of UK manufacturers, SMEs, universities and research centres for each line, with the evidence behind every match.</p><p><a href="platform.html">How the platform works</a></p></div>
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
    <li><div><b>Exclude competitors</b><p>Remove competitor groups from your results. Anything excluded stays listed, so you can bring it back.</p></div></li>
    <li><div><b>Review the shortlist</b><p>Results for each line are grouped by readiness, each with a reason and links to the company's own published information.</p></div></li>
    <li><div><b>Check the companies you pick</b><p>Financial health, ownership and security information for the firms you shortlist.</p></div></li>
    <li><div><b>Make first contact in your own name</b><p>A sanitised first-stage capability enquiry for each company, with a tracker for replies.</p></div></li>
  </ol>
</div></section>

<section class="section stone" aria-labelledby="eng-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="eng-title">Built for engineers, not marketing</h2>
    <p class="sub">Every match comes with a reason that is simple to understand, and a link to the company's own published information. Companies that only sell or distribute are kept out of the manufacturer results.</p></div>
  <ul class="scale" aria-label="What each readiness label means">
    <li><span class="mark" aria-hidden="true"></span><div><b>Can make this now</b><span>Evidence that the company already makes this type of item in the UK.</span></div></li>
    <li><span class="mark support" aria-hidden="true"></span><div><b>Could make this with support</b><span>Related capability. A candidate for technology transfer, new capability or SME development.</span></div></li>
    <li><span class="mark partial" aria-hidden="true"></span><div><b>Partial</b><span>The company covers part of the requirement.</span></div></li>
    <li><span class="mark none" aria-hidden="true"></span><div><b>No confirmed UK maker found</b><span>Stated plainly, with any support options still shown. The platform gives you a well-evidenced starting point; your engineers confirm capability directly with each company.</span></div></li>
  </ul>
</div></section>
{HOME_ALERTS}

<section class="section stone" aria-labelledby="more-title"><div class="wrap">
  <span class="kicker" aria-hidden="true"></span><h2 class="h2" id="more-title">The roundtable and training</h2>
  <p class="sub">Two ways Capital brings people together around industrial participation, alongside the platform.</p>
  <div class="cols two-up">
    <div class="col"><h3>UK Industrial <span class="nowrap">Co-operation</span> Roundtable</h3><p>An informal quarterly meeting in London for UK and international defence companies with UK industrial participation commitments, with government officials invited to take part. The first meeting takes place in Q4 2026.</p><p><a href="uk-icr.html">About UK-ICR</a></p></div>
    <div class="col"><h3>Offset practitioner course</h3><p>A practitioner's masterclass for people new to offset and industrial participation: eight modules, a UK elective and a live negotiation simulation, online over nine weeks or in-house over three days.</p><p><a href="training.html">See the course outline</a></p></div>
  </div>
</div></section>
{band()}""")

PAGES["platform.html"] = dict(title="The UK Defence Localisation Platform", desc="A secure, self-service platform that turns a bill of materials into a shortlist of credible UK industrial partners, with the evidence behind every match.", body=pagehead(
    "The UK Defence Localisation Platform",
    "A secure, self-service tool that turns your bill of materials into a shortlist of credible UK industrial partners: companies that can make your parts now, and companies that could make them with your support.",
    ["Platform"]) + f"""
<section class="section" aria-labelledby="how-title"><div class="wrap">
  <span class="kicker" aria-hidden="true"></span><h2 class="h2" id="how-title">How it works</h2>
  <ol class="steps">
    <li><div><b>Upload your parts list</b><p>Use plain, unclassified descriptions. No drawings, part numbers or controlled data are needed.</p></div></li>
    <li><div><b>Choose your priorities</b><p>Put ready-now manufacturers first, or give more weight to the UK value a partnership creates, such as SME growth, new capability and certification.</p></div></li>
    <li><div><b>Exclude competitors</b><p>Remove competitor groups from your results. Anything excluded stays listed, so you can bring it back.</p></div></li>
    <li><div><b>Review the shortlist</b><p>Results for each line are grouped by readiness, each with a reason and links to the company's own published information.</p></div></li>
    <li><div><b>Check the companies you pick</b><p>See financial health, ownership and security information for the firms you shortlist.</p></div></li>
    <li><div><b>Make first contact in your own name</b><p>Generate a sanitised first-stage capability enquiry for each company, with a tracker for replies.</p></div></li>
  </ol>
</div></section>

<section class="section stone" id="labels" aria-labelledby="labels-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="labels-title">What you get for each line</h2>
    <p class="sub">Every candidate carries one of four labels, a reason that is simple to understand, and links to the company's own published information.</p></div>
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
    <p>UK companies can read <a href="uk-companies.html">how they are included, and how to correct or remove a listing</a>.</p>
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

PAGES["industrial-participation.html"] = dict(title="UK industrial participation", desc="What UK industrial participation (offset) means for overseas defence suppliers, and how Capital helps them create genuine UK value.", body=pagehead(
    "UK industrial participation (offset)",
    "Under the UK Government's offset regime, when it buys defence equipment from abroad, the overseas supplier must create British jobs and benefits.",
    ["Industrial participation"]) + f"""
<section class="section" aria-labelledby="means-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="means-title">What this means for overseas suppliers</h2></div>
  <div class="prose">
    <ul>
      <li>UK partners are needed early, often before a bid is submitted.</li>
      <li>Commitments are usually met over many years, so partners must be stable and capable.</li>
      <li>Credit favours real, lasting value: new UK suppliers, new capability, certifications and skilled jobs, especially in smaller companies.</li>
    </ul>
    <div class="note"><b>Know the rules that apply to you.</b> Thresholds, percentages and timescales are set by the Ministry of Defence. Capital can explain how they apply to your contract.</div>
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
    <p>Capital's founder has worked on offset and industrial participation programmes for more than 25 years, across Europe, the Middle East, Asia, Africa and the Americas. <a href="about.html">About Capital</a></p>
    <p>Capital also convenes the <a href="uk-icr.html">UK Industrial Co-operation Roundtable</a>, an informal quarterly meeting in London for companies working through UK commitments, and runs a <a href="training.html">practitioner course</a> for people new to offset.</p>
  </div>
</div></section>
{band()}""")

PAGES["uk-companies.html"] = dict(title="For UK companies", desc="How UK manufacturers, SMEs and research centres are included on Capital's UK Defence Localisation Platform, how they may be contacted, and how to correct or remove a listing.", body=pagehead(
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

PAGES["security.html"] = dict(title="Security and privacy", desc="How Capital's UK Defence Localisation Platform keeps programme information private to the client organisation.", body=pagehead(
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

PAGES["advisory.html"] = dict(title="Advisory services", desc="Direct advisory support on offset and industrial participation for companies and governments, contracted separately from Capital's UK Defence Localisation Platform.", body=pagehead(
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

<section class="section stone" aria-labelledby="also-title"><div class="wrap">
  <span class="kicker" aria-hidden="true"></span><h2 class="h2" id="also-title">Training and the roundtable</h2>
  <div class="cols two-up">
    <div class="col"><h3>Offset practitioner course</h3><p>A practitioner's masterclass for people new to offset and industrial participation: eight modules, a UK elective and a live negotiation simulation, online over nine weeks or in-house over three days.</p><p><a href="training.html">See the course outline</a></p></div>
    <div class="col"><h3>UK Industrial <span class="nowrap">Co-operation</span> Roundtable</h3><p>An informal quarterly meeting in London for UK and international defence companies with UK industrial participation commitments, with government officials invited to take part. The first meeting takes place in Q4 2026.</p><p><a href="uk-icr.html">About UK-ICR</a></p></div>
  </div>
</div></section>
{band("Discuss a project", "Tell us about your programme and target market, and we will come back to you within two working days.", "Contact Capital", "contact.html")}""")

# ---------------------------------------------------------------- practitioner course
# The public course outline shows structure, topics and formats only. Teaching notes, model answers,
# the Project Halcyon scenario and the course quiz questions stay in the paid materials.
COURSE_SUBJECT = "Offset course: register interest"

COURSE_FIGS = [
    ("8", "core modules, plus a UK elective"),
    ("6", "public-record case studies"),
    ("13", "national offset regimes compared"),
    ("72", "knowledge-check questions"),
    ("85", "terms in the course glossary"),
    ("1", "live negotiation to finish"),
]

COURSE_OUTCOMES = [
    ("Explain the deal", "What offset, industrial participation and localisation are, why governments use them and how they differ by country."),
    ("Read a policy", "Pick out the clauses in a national offset policy that drive cost, risk and strategy."),
    ("Build a strategy", "Shape an offset strategy for a bid, and judge how it changes the chance of winning."),
    ("Place work locally", "Design direct offset and localisation projects that protect quality and schedule."),
    ("Transfer technology safely", "Design technology, research, investment and training projects that earn credit, protect core intellectual property and stay within export controls."),
    ("Do the numbers", "Calculate credit, multipliers, banked credit, penalty exposure and the true cost of an offset programme."),
    ("Negotiate", "Prepare for and conduct a negotiation with an offset authority."),
    ("Deliver cleanly", "Run a programme to close-out: governance, evidence, audits, reporting and recovery, within anti-bribery law."),
]

COURSE_PATH = [
    ("Module 1", "Before you start"),
    ("Module 2", "Read the market"),
    ("Module 3", "Plan and propose"),
    ("Modules 4 and 5", "Design the projects"),
    ("Module 6", "Value and cost"),
    ("Module 7", "Agree the terms"),
    ("Module 8", "Deliver, prove and close"),
]

COURSE_MODULES = [
    dict(num="Module 1", title="Foundations", q="What is offset, and why do governments want it?",
         topics=["What offset is, and the names countries use for it",
                 "Direct offset, indirect offset and countertrade",
                 "Why governments demand offset, and the case against it",
                 "The players, and what each of them wants"],
         facts=[("Case study", "The F-16 ‘deal of the century’, 1975"),
                ("Exercise", "Offset or not? Classifying ten proposed activities")]),
    dict(num="Module 2", title="The rules of the game", q="What do the rules allow, demand and forbid?",
         topics=["Trade law and the security exception: the myth of the open market",
                 "Anatomy of an offset regime: a twelve-point checklist",
                 "Three families of regime, compared country by country",
                 "The hard limits: bribery, export control, sanctions and competition law"],
         facts=[("Case study", "Europe’s U-turn on offsets"),
                ("Exercise", "Decode a national offset policy")]),
    dict(num="Module 3", title="Strategy and the bid", q="How do we win with an offset package we can afford?",
         topics=["Starting early: offset in the capture plan",
                 "Reading your leverage",
                 "Building the strategy and the proposal",
                 "Getting the bid approved: cost, risk and governance"],
         facts=[("Case study", "Switzerland’s F-35 offset and its regional key"),
                ("Exercise", "Strategy on a page")]),
    dict(num="Module 4", title="Direct offsets and localisation", q="How do we place work locally without hurting quality or schedule?",
         topics=["From burden to asset: localisation that wins bids",
                 "The forms of direct offset, from build-to-print to licensed production",
                 "Supply chain reality checks: qualifying a new local supplier",
                 "Structuring the deal: workshare, quality and risk"],
         facts=[("Case study", "Poland’s K2 tank localisation"),
                ("Exercise", "A supplier development plan")]),
    dict(num="Module 5", title="Technology transfer and indirect offsets", q="How do we earn credit beyond the platform without giving away the crown jewels?",
         topics=["What governments ask for, and what is commercially viable",
                 "Protecting intellectual property inside export controls",
                 "Valuing technology transfer: the cost, market and income approaches",
                 "Investment, joint ventures, research, training and export support"],
         facts=[("Case study", "Korea, from F-16 kits to aircraft exports"),
                ("Exercise", "The technology package: transfer, license or decline")]),
    dict(num="Module 6", title="The mathematics of offsets", q="What is each project worth, what will it cost, and what if we fall short?",
         topics=["How credit is valued",
                 "Multipliers, caps and discount factors",
                 "Banking, pre-crediting and transfers",
                 "Penalty exposure and the true cost of offset"],
         facts=[("Worked example", "A supplier’s credit and cost model"),
                ("Exercise", "Rebalance the plan, using the course spreadsheet")]),
    dict(num="Module 7", title="Negotiation across cultures", q="How do we agree terms we can live with?",
         topics=["The practitioner’s edge: why standard tactics fail",
                 "The offset agreement, clause by clause",
                 "Regional approaches: the Gulf, Asia, Europe and North America",
                 "Redirecting the impossible ask"],
         facts=[("Case study", "The radar that could not move, drawn from practice"),
                ("Exercise", "The negotiation plan")]),
    dict(num="Module 8", title="Delivery, audit and recovery", q="How do we deliver, prove it and recover when things slip?",
         topics=["Running an offset programme",
                 "The audit trail: causality, additionality and evidence",
                 "When delivery falls short",
                 "Penalties, disputes and close-out",
                 "Integrity in delivery"],
         facts=[("Case study", "South Africa’s arms deal offsets"),
                ("Exercise", "Year 4: recovering a programme under pressure")]),
    dict(num="Module 9 · Elective", title="The UK lens", q="What could the UK ask for, and how should companies prepare?",
         topics=["The UK’s past experience of industrial participation",
                 "What the UK has said since 2025",
                 "How a UK regime could work: a worked model",
                 "How foreign suppliers and UK companies should prepare"],
         facts=[("Case study", "Two designs compared"),
                ("Format", "One 90-minute session for UK-focused groups")]),
]

# A short public self-test. These questions are deliberately separate from the course's own knowledge checks.
COURSE_QUIZ = [
    dict(q="A sales agent you hired bribes an official to speed up approval of your offset project. Nobody at your company knew. Under the UK Bribery Act, your company:",
         opts=["Is safe, because nobody at the company knew",
               "Is liable only if the bribe was paid in the UK",
               "Can be guilty of failing to prevent bribery, unless it had adequate procedures",
               "Is liable only if a director approved the payment"],
         a=2, why="Section 7 makes a company liable when someone performing services for it pays a bribe to win or keep business for it, anywhere in the world. Its only defence is adequate procedures to prevent bribery."),
    dict(q="A local supplier invoices you £10m for new work. 40% of its value is imported material, and £2m of the order is business you already place with that supplier every year. Under a typical value-added rule, how much is eligible for credit before any multiplier?",
         opts=["£10m", "£8m", "£6m", "£4.8m"],
         a=3, why="Many regimes credit only new business, and only the share of value added locally: (£10m − £2m) × 60% = £4.8m."),
    dict(q="Under Poland’s Offset Act, what penalty applies to an obligation left unperformed?",
         opts=["100% of the unperformed value", "5% of the shortfall", "10% of the shortfall", "50% of the shortfall"],
         a=0, why="Poland’s penalty equals the unperformed obligation, and the supplier’s security must be at least the offset value. Many other regimes charge between 5% and 15%."),
    dict(q="Since 2026, which activity earns the highest multiplier under Canada’s Industrial and Technological Benefits policy?",
         opts=["Buying Canadian-made components",
               "Indigenous workforce development",
               "Investment in Canadian-owned intellectual property",
               "Direct work with small and medium-sized firms"],
         a=1, why="Canada raised Indigenous workforce development to ten times its value in 2026, its largest multiplier. Investment in Canadian-owned intellectual property earns five times, and direct work with small firms twice."),
    dict(q="Switzerland set the offset on its F-35A purchase at 60% of the contract value. Which rule also decides where the work goes?",
         opts=["At least half must go to small firms",
               "Civil exports earn double credit",
               "All of it must be direct work on the aircraft",
               "It must be shared out across the language regions"],
         a=3, why="Swiss offsets follow a regional key: 65% to German-speaking, 30% to French-speaking and 5% to Italian-speaking Switzerland."),
    dict(q="Your offset project would share US-origin technical data for a defence item with a foreign partner. Which approval do you normally need before sharing it?",
         opts=["A technical assistance agreement approved by the US State Department",
               "Your partner’s signature on a non-disclosure agreement",
               "None, once the data is more than ten years old",
               "An export licence from the buyer’s government"],
         a=0, why="Under the US International Traffic in Arms Regulations, defence services and technical data need State Department approval, usually through a technical assistance agreement, before they are shared."),
]

def course_figs_html():
    return "".join(f'<li><b>{n}</b><span>{html.escape(t)}</span></li>' for n, t in COURSE_FIGS)

def course_outcomes_html():
    return "".join(f'<li><div><b>{html.escape(b)}</b><p>{html.escape(p)}</p></div></li>' for b, p in COURSE_OUTCOMES)

def course_path_html():
    return "".join(f'<li><span class="pm">{html.escape(m)}</span><b>{html.escape(s)}</b></li>' for m, s in COURSE_PATH)

def course_modules_html():
    out = []
    for i, m in enumerate(COURSE_MODULES, 1):
        topics = "".join(f"<li>{html.escape(t)}</li>" for t in m["topics"])
        facts = "".join(f"<div><dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd></div>" for k, v in m["facts"])
        is_open = " open" if i == 1 else ""
        out.append(f"""<details class="mod" id="module-{i}"{is_open}>
      <summary><span class="mnum">{html.escape(m['num'])}</span><span class="mhead"><h3 class="mtitle">{html.escape(m['title'])}</h3><span class="mq">{html.escape(m['q'])}</span></span><span class="mtog" aria-hidden="true"></span></summary>
      <div class="mbody"><div><h4>What it covers</h4><ul class="dlist">{topics}</ul></div><div><h4>How it is taught</h4><dl class="mfacts">{facts}</dl></div></div>
    </details>""")
    return "\n    ".join(out)

def course_quiz_html():
    letters = "ABCD"
    qs = []
    for q in COURSE_QUIZ:
        opts = "".join(f'<li><button type="button" class="opt" data-i="{j}"><span class="ol" aria-hidden="true">{letters[j]}</span><span>{html.escape(o)}</span></button></li>'
                       for j, o in enumerate(q["opts"]))
        qs.append(f'<li class="q" data-answer="{q["a"]}"><p class="qtext" tabindex="-1">{html.escape(q["q"])}</p>'
                  f'<ul class="opts">{opts}</ul>'
                  f'<p class="why"><b class="verdict">Answer: {letters[q["a"]]}.</b> <span class="expl">{html.escape(q["why"])}</span></p></li>')
    n = len(COURSE_QUIZ)
    return f"""<div class="quiz" id="quiz">
      <div class="qtop"><span class="qcount">{n} questions</span><span class="qtally"></span></div>
      <ol class="qlist">{"".join(qs)}</ol>
      <p class="vh qlive" aria-live="polite"></p>
      <div class="qnav" hidden><button type="button" class="btn btn-navy qnext">Next question</button></div>
      <div class="qresult" hidden tabindex="-1">
        <p class="qbig"></p>
        <p class="qmsg" data-band="top" hidden>You clearly know the field. The in-house course can bring the rest of your team up to the same standard.</p>
        <p class="qmsg" data-band="mid" hidden>A solid base, with a gap or two. The course fills them, and adds the negotiating and delivery judgement that comes from practice.</p>
        <p class="qmsg" data-band="low" hidden>Many people new to offset score here. The course was written for exactly that starting point.</p>
        <div class="actions"><a class="btn btn-brass" href="#register">Register your interest</a><button type="button" class="btn btn-outline qagain">Try again</button></div>
      </div>
    </div>"""

PAGES["training.html"] = dict(title="Offset practitioner course", desc="Strategic Industrial Participation and Offsets: a practitioner's masterclass for people new to offset and industrial participation. Eight modules, a UK elective and a live negotiation simulation, online over nine weeks or in-house over three days.", body=pagehead(
    "Strategic Industrial Participation &amp; Offsets",
    "A practitioner's masterclass for people new to offset and industrial participation. It sets academic theory aside and concentrates on the commercial realities: winning bids, protecting margins and delivering what was promised.",
    ["Training"],
    '<div class="actions"><a class="btn btn-brass" href="#register">Register your interest</a><a class="btn btn-ghost" href="#modules">See the course structure</a></div>'
    '<p class="audience">Online over nine weeks, or in-house over three days for your team</p>') + f"""
<section class="section tight" aria-label="The course at a glance"><div class="wrap">
  <ul class="figs">{course_figs_html()}</ul>
</div></section>

<section class="section stone" aria-labelledby="for-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="for-title">Who the course is for</h2></div>
  <div class="prose">
    <p>People taking on offset or industrial participation responsibilities for the first time: bid and capture managers, newly appointed offset managers, commercial, contracts and procurement staff, programme managers, finance staff who cost and report offset, and executives who approve bids.</p>
    <p>It suits defence and aerospace companies bidding into markets with offset requirements, their suppliers, and UK companies and government staff who work with foreign suppliers. No prior knowledge of offset is needed.</p>
    <div class="note"><b>Course aim.</b> To turn offset obligations from a compliance cost into a competitive advantage that wins bids and protects margins.</div>
  </div>
</div></section>

<section class="section" id="test" aria-labelledby="test-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="test-title">How much do you already know?</h2>
    <p class="sub">Six questions that experienced offset managers should get right. It takes about two minutes, and nothing you choose is recorded.</p></div>
  {course_quiz_html()}
</div></section>

<section class="section stone" aria-labelledby="out-title"><div class="wrap">
  <span class="kicker" aria-hidden="true"></span><h2 class="h2" id="out-title">What participants will be able to do</h2>
  <ol class="steps four-up">{course_outcomes_html()}</ol>
</div></section>

<section class="section" id="modules" aria-labelledby="mod-title"><div class="wrap">
  <span class="kicker" aria-hidden="true"></span><h2 class="h2" id="mod-title">Course structure</h2>
  <p class="sub">Eight core modules follow the life of an offset obligation, from the first sight of a requirement to the completion letter. Every exercise builds the same fictional bid, so the closing negotiation draws on all of it.</p>
  <ol class="path" aria-label="The offset life cycle, module by module">{course_path_html()}</ol>
  <div class="modhead"><p class="modnote">Open a module to see what it covers and how it is taught.</p><button type="button" class="linkbtn" id="expandall" aria-expanded="false" hidden>Open all modules</button></div>
  <div class="mods">
    {course_modules_html()}
  </div>
</div></section>

<section class="section navy" id="capstone" aria-labelledby="cap-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="cap-title">The capstone: Project Halcyon</h2>
    <p class="sub">A live negotiation that draws on every module.</p></div>
  <div class="prose">
    <p>Every exercise in the course builds towards one fictional procurement: a £500m helicopter programme with a demanding offset authority. In the capstone, teams play the foreign supplier's capture and offset team and negotiate the industrial participation agreement against the clock.</p>
    <p>Developments during the negotiation test judgement as well as technique. Afterwards, each participant turns the result into a strategy paper for the board.</p>
    <ul class="facts">
      <li><b>Teams</b><span>Four or five people, each in a defined role</span></li>
      <li><b>Time</b><span>2.5 hours online, or up to a full day in-house</span></li>
      <li><b>Across the table</b><span>The offset authority, played by the course leader</span></li>
      <li><b>Scored on</b><span>The agreement reached, what the plan costs and covers, and how the team conducts itself</span></li>
    </ul>
  </div>
</div></section>

<section class="section" id="formats" aria-labelledby="formats-title"><div class="wrap">
  <span class="kicker" aria-hidden="true"></span><h2 class="h2" id="formats-title">Two ways to take the course</h2>
  <div class="cols two-up">
    <div class="col"><span class="meta">Online · nine weeks</span><h3>Online cohort</h3>
      <p>Work through each module at your own pace during the week: a recorded lecture of 60 to 90 minutes in short segments, about an hour of reading from official government guidelines, and an online knowledge check. Each week ends with a 60-minute live session.</p>
      <ul class="sched"><li><b>Weeks 1 to 8</b><span>One module a week</span></li><li><b>Week 9</b><span>The capstone negotiation</span></li><li><b>Week 11</b><span>Strategy paper due</span></li></ul></div>
    <div class="col"><span class="meta">In-house · three days, plus an optional fourth</span><h3>In-house intensive</h3>
      <p>Delivered to your team, two or three modules a day, each with a short exercise. The optional fourth day is the full capstone negotiation; without it, a shorter negotiation closes the third day.</p>
      <ul class="sched"><li><b>Day 1</b><span>Modules 1 to 3</span></li><li><b>Day 2</b><span>Modules 4 to 6</span></li><li><b>Day 3</b><span>Modules 7 and 8, and capstone preparation</span></li><li><b>Day 4</b><span>The capstone negotiation (optional)</span></li></ul></div>
  </div>
  <div class="note" style="margin-top:clamp(28px,4vw,40px);max-width:none"><b>UK elective.</b> For UK-focused groups, Module 9 adds one 90-minute session: online after the course, or as a half-day add-on in-house.</div>
</div></section>

<section class="section stone" aria-labelledby="cert-title"><div class="wrap">
  <span class="kicker" aria-hidden="true"></span><h2 class="h2" id="cert-title">Assessment, certificate and materials</h2>
  <div class="cols two-up">
    <div class="col"><span class="meta">Assessment</span><h3>Three steps to the certificate</h3>
      <ul class="dlist"><li>A knowledge check after each module: eight questions, with a pass mark of six.</li><li>A full role in the capstone negotiation.</li><li>A strategy paper of up to 2,500 words, marked against set criteria: pass at 60%, distinction at 75%.</li></ul>
      <p>In-house groups can take a certificate of attendance instead, without the paper.</p></div>
    <div class="col"><span class="meta">Included</span><h3>What participants receive</h3>
      <ul class="dlist"><li>A participant workbook with every exercise and the full Project Halcyon scenario</li><li>The course spreadsheet: a credit, milestone and cost model</li><li>A glossary of 85 terms</li><li>A reading pack of official guidelines and expert summaries for 15 countries</li><li>A certificate on completion</li></ul></div>
  </div>
</div></section>

<section class="section" aria-labelledby="lead-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="lead-title">Course leader</h2></div>
  <div class="prose">
    <p>The course is led by Stephen Lewis, who founded Capital in 2013. He has more than 25 years' experience in offset, industrial participation and cross-border trade finance, on programmes in nearly 30 countries across Europe, the Middle East, Asia, Africa and the Americas.</p>
    <p>The teaching draws on that front-line experience rather than academic theory. Every module includes examples from his own programmes, from technology transfer in Taiwan to steel exports credited under offset contracts in South Korea. <a href="about.html">About Capital</a></p>
  </div>
</div></section>

<section class="section stone" id="register" aria-labelledby="reg-title"><div class="wrap two">
  <div>
    <span class="kicker" aria-hidden="true"></span><h2 id="reg-title">Register your interest</h2>
    <div class="prose" style="margin-top:18px">
      <p>Email Capital with your name, job title and organisation, and say which format interests you: the online cohort, or an in-house course for your team.</p>
      <p>Dates and fees for the first online cohort will be sent to everyone who registers interest. For an in-house course, let us know your preferred dates and roughly how many people will take part.</p>
      <p>Your details are used only to respond to your enquiry.</p>
    </div>
  </div>
  <div class="panel">
    <h3>Email Capital</h3>
    <div class="big">{EMAIL_WBR}</div>
    <div class="copyrow"><button class="copybtn" type="button" data-copy="{EMAIL}">Copy email address</button></div>
    <p style="margin-top:20px"><strong>Subject line</strong>, so your enquiry is picked up straight away:</p>
    <div class="copyrow" style="margin-top:8px"><code>{COURSE_SUBJECT}</code><button class="copybtn" type="button" data-copy="{COURSE_SUBJECT}">Copy subject</button></div>
    <div class="actions"><a class="btn btn-brass" href="mailto:{EMAIL}?subject=Offset%20course%3A%20register%20interest">Open in your email app</a></div>
    <p>Prefer to talk first? {PHONE}, UK office hours.</p>
  </div>
</div></section>
{band('Working on a UK commitment?', 'Meet others doing the same at the UK Industrial Co-operation Roundtable, an informal quarterly meeting in London. The first takes place in Q4 2026.', 'About the roundtable', 'uk-icr.html')}""")


PAGES["uk-icr.html"] = dict(title='UK Industrial Co-operation Roundtable (UK-ICR)', desc='UK-ICR is an informal, quarterly one-day roundtable in London for UK and international defence companies with UK industrial participation (offset) commitments, with government officials invited to take part.', body=pagehead(
    'UK Industrial <span class="nowrap">Co-operation</span> Roundtable',
    'UK-ICR is an informal forum for companies with UK industrial participation (offset) commitments. It meets for one day each quarter in London, with the aim of bringing industry and government together on how those commitments work in practice.',
    ['Roundtable'],
    '<div class="actions"><a class="btn btn-brass" href="#join">Join the mailing list</a><a class="btn btn-ghost" href="#host">Offer to host a meeting</a></div><p class="audience">Inaugural meeting: Q4 2026, central London</p>') + f"""
<section class="section" aria-labelledby="why-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="why-title">Why a roundtable, and why now</h2></div>
  <div class="prose">
    <p>The UK Government now applies an offset regime to defence equipment bought from abroad. Overseas suppliers, their UK partners and government all gain from a shared, practical understanding of how commitments are set, met and credited.</p>
    <p>Many overseas companies already manage offset obligations in other countries, and many UK companies already supply them. The roundtable gives both a regular place to compare experience, raise practical problems early and understand the thinking behind the rules.</p>
    <p>It is deliberately informal: a day of open discussion, not a conference or a sales event.</p>
  </div>
</div></section>

<section class="section stone" aria-labelledby="who-title"><div class="wrap">
  <span class="kicker" aria-hidden="true"></span><h2 class="h2" id="who-title">Who it is for</h2>
  <div class="cols">
    <div class="col"><h3>International defence companies</h3><p>Overseas suppliers with UK industrial participation commitments, or expecting them on future UK contracts, and their UK subsidiaries.</p></div>
    <div class="col"><h3>UK defence companies</h3><p>UK companies of every size, from primes to SMEs, that partner with overseas suppliers or want to.</p></div>
    <div class="col"><h3>Government</h3><p>Officials responsible for UK industrial participation policy and defence procurement, invited to set out policy and hear industry's experience.</p></div>
  </div>
</div></section>

<section class="section" aria-labelledby="topics-title"><div class="wrap">
  <span class="kicker" aria-hidden="true"></span><h2 class="h2" id="topics-title">What the roundtable discusses</h2>
  <p class="sub">Three themes run through every meeting.</p>
  <div class="cols">
    <div class="col"><h3>Macroeconomic rules</h3><p>How commitments are set and valued, what counts towards them, how they are reported, and the economic goals behind them.</p></div>
    <div class="col"><h3>National security requirements</h3><p>Sovereign capability, security of supply, ownership, protection of intellectual property and export control.</p></div>
    <div class="col"><h3>Supply contract obligations</h3><p>How commitments are written into contracts, flow down to UK suppliers, and are delivered and evidenced over the life of a programme.</p></div>
  </div>
</div></section>

<section class="section stone" aria-labelledby="format-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="format-title">How it works</h2></div>
  <div>
    <ul class="facts">
      <li><b>When</b><span>Quarterly, for one day.</span></li>
      <li><b>Where</b><span>Central London, at the offices of a participating organisation that offers to host.</span></li>
      <li><b>Format</b><span>Informal and discussion-led.</span></li>
      <li><b>Ground rules</b><span>Policy and general practice only. Live competitions, individual bids and prices are not discussed.</span></li><li><b>Chatham House Rule</b><span>All meetings are held under the Chatham House Rule. You may use what you hear, but you may not reveal who said it or which organisation they represent. This allows everyone to speak freely.</span></li>
      <li><b>Convened by</b><span>Capital, as an independent forum. UK-ICR is not a government body and does not speak for the Ministry of Defence.</span></li>
    </ul>
    <div class="note" style="margin-top:28px;max-width:none"><b>Inaugural meeting: Q4 2026.</b> The first meeting will take place in central London in the final quarter of 2026. The date and venue will be sent to everyone on the mailing list.</div>
  </div>
</div></section>

<section class="section" id="join" aria-labelledby="join-title"><div class="wrap two">
  <div>
    <span class="kicker" aria-hidden="true"></span><h2 id="join-title">Join the mailing list</h2>
    <div class="prose" style="margin-top:18px">
      <p>To receive invitations and meeting dates, email Capital with your name, job title and organisation.</p>
      <p id="host"><strong>Hosting a meeting.</strong> Each meeting is hosted by a participating organisation at its central London offices. If your organisation could provide a meeting room for the day, please let us know.</p>
      <p>Your details are used only to send UK-ICR invitations and updates, and are not shared with anyone else. You can ask to be removed at any time.</p>
    </div>
  </div>
  <div class="panel">
    <h3>Email Capital</h3>
    <div class="big">{EMAIL_WBR}</div>
    <div class="copyrow"><button class="copybtn" type="button" data-copy="{EMAIL}">Copy email address</button></div>
    <p style="margin-top:20px">Please use one of these <strong>subject lines</strong>, so your email reaches the right list:</p>
    <div class="copyrow" style="margin-top:8px"><code>UK-ICR mailing list</code><button class="copybtn" type="button" data-copy="UK-ICR mailing list">Copy subject</button></div>
    <div class="copyrow" style="margin-top:8px"><code>UK-ICR hosting offer</code><button class="copybtn" type="button" data-copy="UK-ICR hosting offer">Copy subject</button></div>
    <div class="actions"><a class="btn btn-brass" href="mailto:{EMAIL}?subject=UK-ICR%20mailing%20list">Join the mailing list</a><a class="btn btn-outline" href="mailto:{EMAIL}?subject=UK-ICR%20hosting%20offer">Offer to host</a></div>
  </div>
</div></section>
{band()}""")

ALERT_SUBJECT = "Offset alerts"
PAGES["offset-alerts.html"] = dict(title="Offset alerts", desc="A weekly round-up of new defence sales around the world above the offset thresholds.", body=pagehead(
    "Offset alerts",
    "A weekly round-up of new defence sales around the world above the offset thresholds, and changes to the offset rules. Each summary is written by Capital from public reports.",
    ["Offset alerts"]) + f"""
<section class="section" aria-labelledby="all-title"><div class="wrap">
  <div class="sechead">
    <div><span class="kicker" aria-hidden="true"></span><h2 class="h2" id="all-title">Recent alerts</h2>
      <p class="updated">Newest first. Checked weekly. Last updated {ALERTS_UPDATED}.</p></div>
  </div>
  {alert_weeks(ALERTS)}
  <p class="retain">Alerts stay on this page for three weeks. Earlier alerts are kept in Capital's records; please ask if you need one.</p>
</div></section>

<section class="section stone" aria-labelledby="sub-title"><div class="wrap two">
  <div>
    <span class="kicker" aria-hidden="true"></span><h2 id="sub-title">Receive the alerts by email</h2>
    <div class="prose" style="margin-top:18px">
      <p>A short weekly email of new alerts, free of charge.</p>
      <p>To join, send us an email with the subject line shown. You can leave at any time by replying "unsubscribe".</p>
      <p>We use your email address only to send the alerts.</p>
    </div>
  </div>
  <div class="panel">
    <h3>Join the weekly email</h3>
    <div class="big">{EMAIL_WBR}</div>
    <div class="copyrow"><button class="copybtn" type="button" data-copy="{EMAIL}">Copy email address</button></div>
    <p style="margin-top:20px"><strong>Subject line</strong></p>
    <div class="copyrow" style="margin-top:8px"><code>{ALERT_SUBJECT}</code><button class="copybtn" type="button" data-copy="{ALERT_SUBJECT}">Copy subject</button></div>
    <a class="btn btn-brass" href="mailto:{EMAIL}?subject={ALERT_SUBJECT.replace(' ', '%20')}">Open in your email app</a>
  </div>
</div></section>

<section class="section tight" aria-labelledby="about-alerts-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="about-alerts-title">About these alerts</h2></div>
  <div class="prose">
    <p>Alerts are drawn from public reports, including government announcements, official notices and the defence press. Programme details can change, so please check them before acting on an alert.</p>
    <p>Capital is independent of the governments and companies named. An alert does not mean that Capital is involved in the programme.</p>
  </div>
</div></section>
{band("Bidding into one of these programmes?", "Capital supports offset strategy, proposal writing and the delivery of offset obligations. We reply within two working days.", "Discuss a project", "contact.html")}""")

COUNTRIES = ["Belgium","Brazil","Bulgaria","Canada","Denmark","Egypt","Estonia","Finland","India","Italy","Kuwait","Lithuania","Malaysia","Netherlands","Norway","Oman","Poland","Portugal","Romania","Saudi Arabia","Slovenia","South Africa","South Korea","Spain","Switzerland","Taiwan","Thailand","Turkey","United Arab Emirates"]

PAGES["about.html"] = dict(title="About Capital", desc="Capital was founded in 2013 by Stephen Lewis. More than 25 years of offset and industrial participation experience across Europe, the Middle East, Asia, Africa and the Americas.", body=pagehead(
    "About Capital",
    "Capital was founded in 2013 by Stephen Lewis to help companies create lasting value through offset and industrial participation. It now combines that experience with Capital's UK Defence Localisation Platform.",
    ["About"]) + f"""
<section class="section" aria-labelledby="founder-title"><div class="wrap two">
  <div><span class="kicker" aria-hidden="true"></span><h2 id="founder-title">Founder</h2></div>
  <div class="prose">
    <p>Stephen Lewis has more than 25 years' experience in offset, industrial participation and cross-border trade finance, first with a leading international consulting and financing organisation and, since 2013, through Capital.</p>
    <p>His work has covered structured export finance, technology transfer and training programmes, and advisory work for governments developing their own industrial policies.</p>
    <div class="countries" aria-label="Countries worked in">{"".join(f"<span>{c}</span>" for c in COUNTRIES)}</div>
  </div>
</div></section>

<section class="section stone" aria-labelledby="exp-title"><div class="wrap">
  <span class="kicker" aria-hidden="true"></span><h2 class="h2" id="exp-title">Selected experience</h2>
  <p class="sub">Projects Stephen has led or contributed to.</p>
  <ul class="exp">
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
PAGES["request-access.html"] = dict(title="Request platform access", desc="Request a demonstration of Capital's UK Defence Localisation Platform and discuss subscription options.", body=pagehead(
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
    <div class="big">{EMAIL_WBR}</div>
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
    <div class="big">{EMAIL_WBR}</div>
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
