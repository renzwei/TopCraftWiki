/* Coordinate atlas: actual region polygons and points, never inferred roads. */
(() => {
  'use strict';
  let atlasPromise;
  const observers = new Map();
  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const kinds = {npc:'NPC', arrival:'抵达点', elite:'精英', boss:'领主', event:'区域事件'};
  const symbols = {npc:'●', arrival:'◆', elite:'▲', boss:'✦', event:'✦'};
  const fmt = n => Number(n.toFixed(1));
  function mountMap(root, data) {
    if (!root.isConnected || root.dataset.ready) return;
    root.dataset.ready = 'true';
    const all = [...data.regions, ...data.markers];
    let selected = all.find(p => p.id === root.dataset.selected);
    let box = [...data.bounds], dragging, moved = false;
    const options = all.map(p => `<option value="${esc(p.id)}">${esc(p.name)}</option>`).join('');
    root.innerHTML = `<div class="world-map-head"><div><strong>${esc(data.name)} · 区域示意图</strong><small>北 ↑ · X 向东 / Z 向南</small></div><div class="world-map-tools"><button type="button" data-action="in" aria-label="放大地图">＋</button><button type="button" data-action="out" aria-label="缩小地图">−</button><button type="button" data-action="reset">全图</button><button type="button" data-action="fullscreen">全屏</button></div></div><div class="world-map-layout"><div class="world-map-canvas"><svg xmlns="http://www.w3.org/2000/svg" role="group" aria-label="${esc(data.name)}可交互坐标地图" tabindex="0"></svg><span class="world-map-hint">拖动平移 · ＋ / − 缩放 · 方向键平移</span></div><aside class="world-map-panel"><label>查找地点<select data-map-select><option value="">选择地区或地点</option>${options}</select></label><div class="world-map-detail" aria-live="polite"></div><div class="world-map-legend"><span>区域边界</span><span class="underground">地下区域</span>${Object.entries(kinds).filter(([k])=>data.markers.some(p=>p.kind===k)).map(([k,v])=>`<span class="${k}">${symbols[k]} ${v}</span>`).join('')}</div><p class="world-map-caption">按服务器坐标绘制。边界不表示道路或地形；传送入口尚未开放。</p></aside></div>`;
    const svg = root.querySelector('svg'), select = root.querySelector('select'), detail = root.querySelector('.world-map-detail');
    function choose(id, focus = false) {
      selected = all.find(p=>p.id===id); select.value = selected?.id || '';
      if (focus && selected) {
        if (selected.points) {
          const xs=selected.points.map(p=>p[0]), zs=selected.points.map(p=>p[1]);
          const width=Math.max(Math.max(...xs)-Math.min(...xs)+45, data.bounds[2]/6);
          const height=Math.max(...zs)-Math.min(...zs)+45;
          const w=Math.max(width,height*data.bounds[2]/data.bounds[3]),h=w*data.bounds[3]/data.bounds[2];
          box=[(Math.min(...xs)+Math.max(...xs)-w)/2,(Math.min(...zs)+Math.max(...zs)-h)/2,w,h];
        } else {
          const w=data.bounds[2]/4,h=data.bounds[3]/4;
          box=[selected.x-w/2,selected.z-h/2,w,h];
        }
      }
      detail.innerHTML = selected ? `<h3>${esc(selected.name)}</h3>${selected.points ? `<p class="world-coordinate">怪物等级：${esc(selected.level || '—')}</p>` : `<p class="world-coordinate">X / Y / Z<br><b>${fmt(selected.x)} / ${fmt(selected.y)} / ${fmt(selected.z)}</b></p>`}<p>${esc(selected.description)}</p><a class="world-map-link" href="#/${esc(selected.route)}">查看${selected.points?'地区':'详细'}介绍 →</a>` : '<h3>选择一个地点</h3><p>点击区域或地点标记，查看等级、坐标与相关攻略。</p><p>营地人物较集中，可打开冒险者营地的局部地图，或在上方列表中查找。</p>';
      draw();
    }
    function draw() {
      svg.setAttribute('viewBox',box.join(' '));
      const rect=svg.getBoundingClientRect();
      const unit = Math.max(box[2]/(rect.width||700),box[3]/(rect.height||520)), labelSize=13*unit;
      const grid = data.bounds[2] > 200 ? 100 : 20;
      let markup='';
      for(let x=Math.ceil(box[0]/grid)*grid;x<box[0]+box[2];x+=grid) markup+=`<path class="world-grid" d="M${x} ${box[1]}v${box[3]}"/><text class="world-axis" x="${x+3*unit}" y="${box[1]+15*unit}" font-size="${10*unit}">${x}</text>`;
      for(let z=Math.ceil(box[1]/grid)*grid;z<box[1]+box[3];z+=grid) markup+=`<path class="world-grid" d="M${box[0]} ${z}h${box[2]}"/><text class="world-axis" x="${box[0]+3*unit}" y="${z-3*unit}" font-size="${10*unit}">${z}</text>`;
      for(const p of data.regions) {
        const x=p.points.reduce((a,b)=>a+b[0],0)/p.points.length,z=p.points.reduce((a,b)=>a+b[1],0)/p.points.length;
        const offset=['df_hyjt','df_djt'].includes(p.id)?-16*unit:0;
        markup+=`<g role="button" tabindex="0" aria-label="${esc(p.name)}，怪物等级 ${esc(p.level || '—')}" aria-pressed="${selected?.id===p.id}" data-place="${esc(p.id)}" class="world-region ${p.underground?'underground':''} ${selected?.id===p.id?'selected':''}"><polygon points="${p.points.map(v=>v.join(',')).join(' ')}"/><text x="${x}" y="${z+offset}" font-size="${labelSize}" text-anchor="middle">${esc(p.name)}</text><text class="world-region-level" x="${x}" y="${z+(offset?24:17)*unit}" font-size="${11*unit}" text-anchor="middle">${p.level==='—'?'营地':esc(p.level)+' 级'}</text></g>`;
      }
      const labelRects=data.markers.map(p=>[p.x-9*unit,p.z-9*unit,p.x+9*unit,p.z+9*unit]);
      for(const p of data.markers) {
        // On the whole forest map, avoid a pile of NPC names over the camp.
        if(data.regions.length && p.kind==='npc' && data.bounds[2]/box[2]<2.2 && p.id!==selected?.id) continue;
        const active=p.id===selected?.id;
        let name='';
        if(!data.regions.length || active) {
          const width=p.name.length*labelSize,height=labelSize*1.2;
          const candidates=[[12,4,'start'],[-12,4,'end'],[0,-16,'middle'],[0,27,'middle'],[12,-17,'start'],[-12,-17,'end'],[12,29,'start'],[-12,29,'end']];
          let best;
          for(const [dx,dy,anchor] of candidates) {
            const x=p.x+dx*unit,y=p.z+dy*unit,left=x-(anchor==='end'?width:anchor==='middle'?width/2:0);
            const area=[left,y-height,left+width,y+3*unit];
            const overlap=labelRects.filter(a=>area[0]<a[2] && area[2]>a[0] && area[1]<a[3] && area[3]>a[1]).length;
            if(!best || overlap<best.overlap)best={x,y,anchor,area,overlap};
            if(!overlap)break;
          }
          labelRects.push(best.area);
          name=`<text class="world-point-name" x="${best.x}" y="${best.y}" text-anchor="${best.anchor}" font-size="${labelSize}">${esc(p.name)}</text>`;
        }
        markup+=`<g role="button" tabindex="0" aria-label="${esc(p.name)}，坐标 ${p.x}, ${p.y}, ${p.z}" aria-pressed="${active}" data-place="${esc(p.id)}" class="world-point ${p.kind} ${active?'selected':''}"><circle cx="${p.x}" cy="${p.z}" r="${8*unit}"/><text class="world-point-symbol" x="${p.x}" y="${p.z+4*unit}" text-anchor="middle" font-size="${12*unit}">${symbols[p.kind]}</text>${name}<title>${esc(p.name)}</title></g>`;
      }
      svg.innerHTML=markup;
      root.querySelector('[data-action="in"]').disabled=box[2]<=data.bounds[2]/8;
      root.querySelector('[data-action="out"]').disabled=box[2]>=data.bounds[2]*1.5;
    }
    function zoom(factor) {
      const w=Math.max(data.bounds[2]/8,Math.min(data.bounds[2]*1.5,box[2]*factor)),h=w*data.bounds[3]/data.bounds[2];
      box=[box[0]+(box[2]-w)/2,box[1]+(box[3]-h)/2,w,h]; draw();
    }
    root.querySelector('.world-map-tools').addEventListener('click',async e=>{
      const action=e.target.closest('button')?.dataset.action;
      if(action==='in') zoom(.75);
      if(action==='out') zoom(1.3333333);
      if(action==='reset') {box=[...data.bounds];draw();}
      if(action==='fullscreen') {
        try {
          if(document.fullscreenElement===root) await document.exitFullscreen();
          else await root.requestFullscreen();
        } catch {root.classList.toggle('world-map-expanded');}
        root.querySelector('[data-action="fullscreen"]').textContent=(document.fullscreenElement===root || root.classList.contains('world-map-expanded'))?'退出全屏':'全屏';
      }
    });
    root.addEventListener('fullscreenchange',()=>{root.querySelector('[data-action="fullscreen"]').textContent=document.fullscreenElement===root?'退出全屏':'全屏';});
    select.addEventListener('change',()=>choose(select.value,true));
    svg.addEventListener('keydown',e=>{
      const place=e.target.closest('[data-place]');
      if(place && (e.key==='Enter'||e.key===' ')) {e.preventDefault(); const id=place.dataset.place;choose(id);svg.querySelector(`[data-place="${id}"]`)?.focus();return;}
      if(e.key==='Escape' && root.classList.contains('world-map-expanded')) {root.classList.remove('world-map-expanded');root.querySelector('[data-action="fullscreen"]').textContent='全屏';}
      if(['+','=','-','ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Home'].includes(e.key)) {
        e.preventDefault();
        if(e.key==='+'||e.key==='=')zoom(.75);else if(e.key==='-')zoom(1.3333333);
        else if(e.key==='Home'){box=[...data.bounds];draw();}
        else {const delta=box[2]*.1;box[0]+=(e.key==='ArrowRight'?delta:e.key==='ArrowLeft'?-delta:0);box[1]+=(e.key==='ArrowDown'?delta:e.key==='ArrowUp'?-delta:0);draw();}
        svg.focus();
      }
    });
    svg.addEventListener('pointerdown',e=>{
      if(e.button!==0)return;
      dragging={x:e.clientX,y:e.clientY,box:[...box],place:e.target.closest('[data-place]')?.dataset.place};moved=false;
      svg.setPointerCapture(e.pointerId);
    });
    svg.addEventListener('pointermove',e=>{
      if(!dragging)return;
      const dx=e.clientX-dragging.x,dy=e.clientY-dragging.y;
      if(Math.abs(dx)+Math.abs(dy)<5)return;
      moved=true;const rect=svg.getBoundingClientRect();
      const scale=Math.min(rect.width/dragging.box[2],rect.height/dragging.box[3]);
      box=[dragging.box[0]-dx/scale,dragging.box[1]-dy/scale,dragging.box[2],dragging.box[3]];draw();
    });
    svg.addEventListener('pointerup',()=>{const place=dragging?.place;dragging=null;if(!moved && place)choose(place);});
    svg.addEventListener('pointercancel',()=>{dragging=null;});
    choose(selected?.id);
    const observer=new ResizeObserver(draw);observer.observe(svg);observers.set(root,observer);
  }
  function mountFilters() {
    const search=document.querySelector('[data-monster-search]'),region=document.querySelector('[data-monster-region]');
    if(!search || search.dataset.ready)return;search.dataset.ready='true';
    const cards=[...document.querySelectorAll('.world-monster')];
    function filter() {
      let count=0;
      for(const card of cards) {card.hidden=!(card.dataset.name.includes(search.value.trim()) && (!region.value || card.dataset.regions.split(' ').includes(region.value)));if(!card.hidden)count++;}
      document.querySelector('[data-monster-count]').textContent=`${count} / ${cards.length} 种怪物`;
      document.querySelector('.world-empty').hidden=count>0;
    }
    search.addEventListener('input',filter);region.addEventListener('change',filter);filter();
  }
  window.TopCraftWorld={mount() {
    for(const [root,observer] of observers)if(!root.isConnected){observer.disconnect();observers.delete(root);}
    mountFilters();
    const roots=[...document.querySelectorAll('.world-map:not([data-ready])')];
    if(!roots.length)return;
    atlasPromise ||= fetch('assets/data/world.json').then(r=>{if(!r.ok)throw new Error('地图数据加载失败');return r.json();}).catch(e=>{atlasPromise=null;throw e;});
    atlasPromise.then(data=>roots.forEach(root=>mountMap(root,data[root.dataset.map]))).catch(()=>roots.forEach(root=>{if(root.isConnected)root.innerHTML='<p>地图暂时未能加载，请刷新重试。下方地区目录与坐标表仍可查询。</p>';}));
  }};
})();
