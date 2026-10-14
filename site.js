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
