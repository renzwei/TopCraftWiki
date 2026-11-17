/* Local combat reference: arithmetic only; never executes configuration JavaScript. */
(function (global) {
  'use strict';
  const numbers = global.TopCraftNumbers || require('./numbers.js');
  const fmt = numbers.value;
  const escape = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function arithmetic(source) {
    const tokens = source.match(/\d*\.?\d+(?:e[+-]?\d+)?|min|max|floor|ceil|round|abs|[()+*/^,\-]/gi) || [];
    if (tokens.join('') !== source.replace(/\s/g, '')) throw Error('Unsupported formula: '+source);
    let at=0;
    function atom() {
      let t=tokens[at++];
      if(t==='-') return -atom(); if(t==='+') return atom();
      if(t==='(') {let v=sum(); if(tokens[at++]!==')') throw Error('Missing )'); return v;}
      if (/^(min|max|floor|ceil|round|abs)$/.test(t)) {
        if(tokens[at++]!=='(') throw Error('Missing ('); let args=[sum()];
        while(tokens[at]===','){at++;args.push(sum());} if(tokens[at++]!==')')throw Error('Missing )');
        return Math[t](...args);
      }
      if(t===undefined||!Number.isFinite(Number(t)))throw Error('Invalid number'); return Number(t);
    }
    function power(){let v=atom();if(tokens[at]==='^'){at++;v=v**power();}return v;}
    function product(){let v=power();while(['*','/'].includes(tokens[at])){let op=tokens[at++],r=power();v=op==='*'?v*r:v/r;}return v;}
    function sum(){let v=product();while(['+','-'].includes(tokens[at])){let op=tokens[at++],r=product();v=op==='+'?v+r:v-r;}return v;}
    const v=sum(); if(at!==tokens.length||!Number.isFinite(v))throw Error('Invalid expression: '+source);return v;
  }
  function parameter(data, name, key, level=1) {
    const p=data.skills[name]?.parameters[key]; if(!p)throw Error('Unknown parameter '+name+':'+key);
    let v=Number(p.base)+Number(p['per-level']||0)*(level-1);
    if(p.min!==undefined)v=Math.max(v,p.min);if(p.max!==undefined)v=Math.min(v,p.max);return v;
  }
  function resolve(data, skill, text, context={}) {
    const level=context.skillLevel||1, character=context.characterLevel||30, ranks=context.ranks||{};
    function token(t) {
      if(t==='mmocore_level')return character;
      if(t.startsWith('mnl_'))return ranks[t.slice(4)]||0;
      if(t.startsWith('mmocore_skill_parameter_')){const [key,name]=t.slice(24).split(':');return parameter(data,name,key,level);}
      if(t.startsWith('tcpriest_param:')){const [,name,key]=t.split(':');return parameter(data,name,key,1);}
      if(t.startsWith('tcpriest_damageScale:')){const name=t.split(':')[1];return parameter(data,name,'damage',level)/parameter(data,name,'damage',1);}
      if(t.startsWith('tcpriest_healingScale:'))return 1;
      if(data.skills[skill].parameters[t])return parameter(data,skill,t,level);
      throw Error('Unknown placeholder '+t);
    }
    let s=text.replace(/\{([^{}]+)\}/g,(_,t)=>String(token(t)));
    s=s.replace(/%(?:math_(?:(\d+):_)?|javascript_loreNumber_(\d+):_)([^%]+)%/g,(_,a,b,expr)=>String(arithmetic(expr)));
    s=s.replace(/%((?:mmocore_skill_parameter_|tcpriest_)[^%]+)%/g,(_,t)=>String(token(t)));
    if(/%[a-z_]|\{[^}]+\}/i.test(s))throw Error('Unresolved lore '+s);
    return numbers.text(s,true);
  }
  function lore(data, skill, node, rank, context={}) {
    const source=context.rich ? (node.richLore||node.lore) : node.lore;
    const keys=Object.keys(source).map(Number).filter(k=>k<=rank).sort((a,b)=>b-a);
    const result=(source[String(keys[0]??0)]||[]).map(l=>resolve(data,skill,l,{...context,ranks:{[node.id]:rank}}));
    if(node.executionNote)result.push('伤害加成：'+node.executionNote);return result;
  }
  function pathCells(skill) {
    const cells=new Map(), dirs=[[0,-1],[1,0],[0,1],[-1,0]];
    for(const n of skill.nodes)for(const p of n.parents){
      const parent=skill.nodes.find(n=>n.id===p.id);if(!parent)throw Error('Missing parent '+p.id);
      const connected=new Set([...p.path,[n.x,n.y],[parent.x,parent.y]].map(p=>p.join(',')));
      for(const [x,y] of p.path){const key=[x,y].join(','),a=cells.get(key)||[0,0,0,0];
        dirs.forEach(([dx,dy],d)=>{if(connected.has([x+dx,y+dy].join(',')))a[d]=2;});cells.set(key,a);}
    }
    return [...cells].map(([key,a])=>({xy:key.split(',').map(Number),code:a[0]+3*a[1]+9*a[2]+27*a[3]}));
  }
  const mechanicLinks={
    '持续伤害':'damage-over-time','召唤物伤害':'summons?id=damage','召唤物治疗':'summons?id=healing',
    '物理伤害':'damage?id=types','火焰伤害':'damage?id=types','冰霜伤害':'damage?id=types','雷电伤害':'damage?id=types','毒素伤害':'damage?id=types',
    '暴击率':'damage?id=critical','暴击伤害':'damage?id=critical','攻击速度':'attributes?id=speed','法力消耗':'attributes?id=cost','冷却缩减':'attributes?id=cooldown',
    '护盾':'shield','护甲':'defense?id=armor','抗性':'defense?id=armor','躲闪':'defense?id=dodge','格挡':'defense?id=block','吸血':'defense?id=healing',
    '点燃':'status-effects?id=ignite','冻伤':'status-effects?id=frostbite','中毒':'status-effects?id=poison','静电':'status-effects?id=static','流血':'status-effects?id=bleed',
    '破甲':'status-effects?id=armor-break','感电':'status-effects?id=shock','迟缓':'status-effects?id=slow','冰缓':'status-effects?id=chill','致盲':'status-effects?id=blind',
    '缓慢诅咒':'status-effects?id=slow-curse','火花电荷':'status-effects?id=spark','毒素爆发':'status-effects?id=poison-burst','治疗降低':'status-effects?id=healing-reduction',
    '热诚':'status-effects?id=zeal','横扫之势':'status-effects?id=sweep-momentum','跃击之势':'status-effects?id=leap-momentum','狂怒':'status-effects?id=fury',
    '眩晕':'status-effects?id=control','冻结':'status-effects?id=control','沉默':'status-effects?id=control','定身':'status-effects?id=control','净化':'status-effects?id=cleanse','韧性':'status-effects?id=tenacity'
  };
  const mechanicPattern=new RegExp(Object.keys(mechanicLinks).sort((a,b)=>b.length-a.length).join('|'),'g');
  function linkMechanics(text,render=escape){let result='',at=0;for(const m of text.matchAll(mechanicPattern)){result+=render(text.slice(at,m.index))+`<a class="mechanic-link" href="#/combat/${mechanicLinks[m[0]]}">${render(m[0])}</a>`;at=m.index+m[0].length;}return result+render(text.slice(at));}
  function renderLore(data,text,links=false){const render=s=>[...s].map(c=>data.assets.loreIcons?.[c]?`<img class="lore-icon" src="${escape(data.assets.loreIcons[c])}" alt="" aria-hidden="true">`:escape(c)).join('');return links?linkMechanics(text,render):render(text);}
  const api={fmt,escape,arithmetic,parameter,resolve,lore,pathCells,renderLore,linkMechanics,mechanicLinks};
  if(typeof module!=='undefined')module.exports=api;
  global.TopCraftCombat=api;
  if(typeof document==='undefined')return;

  let dataPromise, activeCleanup;
  api.mount=async function () {
    activeCleanup?.();activeCleanup=null;
    const roots=[...document.querySelectorAll('[data-skill-tree]:not([data-mounted])')];if(!roots.length)return;
    dataPromise ||= fetch('assets/data/combat.json').then(r=>{if(!r.ok)throw Error('数据加载失败');return r.json();});
    try {const data=await dataPromise;for(const root of roots)if(root.isConnected)activeCleanup=mount(root,data);}
    catch(e){for(const r of roots)r.textContent='技能树加载失败，请刷新页面重试。';console.error(e);}
  };
  function mount(root,data){
    root.dataset.mounted='true';root.classList.add('skill-tree');
    const skill=data.skills[root.dataset.skillTree];
    let selected=skill.nodes.find(n=>n.root)||skill.nodes[0],rank=1,expanded=false;
    const ctx={skillLevel:1,characterLevel:30};
    const all=[...skill.nodes.map(n=>[n.x,n.y]),...pathCells(skill).map(p=>p.xy)];
    const minX=Math.min(...all.map(p=>p[0]))-1,minY=Math.min(...all.map(p=>p[1]))-1;
    const cols=Math.max(...all.map(p=>p[0]))-minX+2,rows=Math.max(...all.map(p=>p[1]))-minY+2;
    root.innerHTML=`<div class="tree-controls"><strong>${skill.name}<small>${skill.nodes.length} 个节点 · ${skill.budget} 点</small></strong><label>技能等级 <select class="skill-level" aria-label="技能等级">${Array.from({length:10},(_,i)=>`<option>${i+1}</option>`).join('')}</select></label><label>职业等级 <input class="character-level" aria-label="职业等级" type="number" min="1" max="30" value="30"></label><label class="node-picker-label">节点 <select class="node-picker" aria-label="查找节点">${skill.nodes.map(n=>`<option value="${escape(n.id)}">${escape(n.name)}</option>`).join('')}</select></label><button type="button" class="tree-expand" aria-expanded="false">全屏查看</button></div><div class="tree-layout"><div class="tree-window" aria-label="完整技能树"><div class="tree-canvas"></div></div><section class="node-detail" aria-label="已选节点详情" aria-live="polite"></section></div><p class="tree-caption">悬停查看效果 · 点击查看节点等级 · Tab / Enter 选择节点</p><div class="tree-tooltip" role="tooltip" hidden></div>`;
    const canvas=root.querySelector('.tree-canvas'),viewport=root.querySelector('.tree-window'),detail=root.querySelector('.node-detail'),tip=root.querySelector('.tree-tooltip'),expand=root.querySelector('.tree-expand'),picker=root.querySelector('.node-picker');
    let cell=48,tipAnchor=null;
    function place(el,x,y){el.dataset.x=x;el.dataset.y=y;el.style.left=(x-minX)*cell+'px';el.style.top=(y-minY)*cell+'px';}
    for(const p of pathCells(skill)){const src=data.assets.paths[p.code];if(!src)continue;const img=document.createElement('img');img.src=src;img.alt='';img.className='tree-path';if(p.code===54)img.style.clipPath='inset(0 50% 0 0)';place(img,...p.xy);canvas.append(img);}
    function choose(n){selected=n;rank=1;tip.hidden=true;picker.value=n.id;renderDetail();}
    for(const n of skill.nodes){const b=document.createElement('button');b.type='button';b.className='tree-node';b.setAttribute('aria-label',`${n.name}，最高 ${n.max} 级`);b.dataset.node=n.id;
      b.innerHTML=`<img src="${n.icon}" alt="" draggable="false"><span>${n.max}</span>`;place(b,n.x,n.y);canvas.append(b);
      b.addEventListener('click',()=>choose(n));b.addEventListener('mouseenter',()=>showTip(n,b));b.addEventListener('mouseleave',()=>tip.hidden=true);
      b.addEventListener('focus',()=>requestAnimationFrame(()=>{if(document.activeElement===b)showTip(n,b);}));b.addEventListener('blur',()=>tip.hidden=true);
    }
    function parentText(n){return n.parents.length?n.parents.map(p=>`${p.id}${p.level ? ` ${p.level} 级` : `（无等级要求）`}`).join('；'):'无';}
    function lines(n,r,links=false){return lore(data,skill.name,n,r,{...ctx,rich:true}).map(l=>renderLore(data,l,links));}
    function renderDetail(){
      canvas.querySelectorAll('.tree-node').forEach(b=>b.classList.toggle('selected',b.dataset.node===selected.id));
      detail.innerHTML=`<div class="node-title"><img src="${selected.icon}" alt=""><div><small>技能节点</small><h3>${escape(selected.name)}</h3></div></div><p class="node-meta">前置：${escape(parentText(selected))}<br>每级 ${selected.cost} 点 · 最高 ${selected.max} 级</p><div class="rank-picks" aria-label="节点预览等级">${Array.from({length:selected.max},(_,i)=>`<button type="button" data-rank="${i+1}" aria-pressed="${rank===i+1}">${i+1} 级</button>`).join('')}</div><div class="node-lore">${lines(selected,rank,true).map(l=>`<p>${l}</p>`).join('')}</div><p class="preview-note">技能 ${ctx.skillLevel} 级 · 职业 ${ctx.characterLevel} 级<br>节点基础效果，无其他节点及装备加成</p>`;
      detail.querySelectorAll('[data-rank]').forEach(b=>b.onclick=()=>{rank=Number(b.dataset.rank);renderDetail();detail.querySelector(`[data-rank="${rank}"]`).focus();});
    }
    function showTip(n,b){if(window.matchMedia('(hover: none)').matches)return;tipAnchor={n,b};tip.innerHTML=`<strong>${escape(n.name)}</strong><small>前置：${escape(parentText(n))} · 最高 ${n.max} 级</small>${lines(n,1).map(l=>`<p>${l}</p>`).join('')}<small>1 级效果 · 点击查看各级数值</small>`;tip.hidden=false;
      const rect=b.getBoundingClientRect();tip.style.left=Math.max(8,Math.min(window.innerWidth-340,rect.right+12))+'px';tip.style.top=Math.max(8,Math.min(window.innerHeight-tip.offsetHeight-8,rect.top))+'px';}
    function layout(){cell=Math.max(1,Math.min(64,(viewport.clientWidth-16)/cols,(viewport.clientHeight-16)/rows));canvas.style.setProperty('--tile',cell+'px');canvas.style.width=cols*cell+'px';canvas.style.height=rows*cell+'px';for(const el of canvas.children)place(el,Number(el.dataset.x),Number(el.dataset.y));}
    let savedOverflow='';
    function setExpanded(value){expanded=value;tip.hidden=true;root.classList.toggle('tree-expanded',value);expand.textContent=value?'退出全屏':'全屏查看';expand.setAttribute('aria-expanded',String(value));
      if(value){savedOverflow=document.body.style.overflow;document.body.style.overflow='hidden';root.setAttribute('role','dialog');root.setAttribute('aria-modal','true');root.setAttribute('aria-label',skill.name+'完整技能树');}
      else{document.body.style.overflow=savedOverflow;root.removeAttribute('role');root.removeAttribute('aria-modal');}
      requestAnimationFrame(layout);
    }
    root.querySelector('.skill-level').onchange=e=>{ctx.skillLevel=Number(e.target.value);tip.hidden=true;renderDetail();};
    root.querySelector('.character-level').onchange=e=>{ctx.characterLevel=Math.min(30,Math.max(1,Number(e.target.value)||1));e.target.value=ctx.characterLevel;tip.hidden=true;renderDetail();};
    picker.onchange=()=>choose(skill.nodes.find(n=>n.id===picker.value));expand.onclick=()=>setExpanded(!expanded);
    root.addEventListener('keydown',e=>{
      if(e.key==='Escape'){tip.hidden=true;if(expanded){setExpanded(false);expand.focus();}}
      if(expanded&&e.key==='Tab'){const focusable=[...root.querySelectorAll('button,select,input,a[href]')].filter(el=>!el.disabled&&el.getClientRects().length),first=focusable[0],last=focusable.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}}
    });
    function trackTip(){if(!tip.hidden&&tipAnchor)showTip(tipAnchor.n,tipAnchor.b);}
    document.addEventListener('scroll',trackTip,true);
    function selectLinkedNode(){const id=new URLSearchParams(location.hash.split('?')[1]||'').get('node');const n=skill.nodes.find(n=>n.id===id);if(n)choose(n);}
    window.addEventListener('hashchange',selectLinkedNode);
    const resize=new ResizeObserver(layout);resize.observe(viewport);renderDetail();selectLinkedNode();requestAnimationFrame(layout);
    return ()=>{if(expanded)setExpanded(false);resize.disconnect();document.removeEventListener('scroll',trackTip,true);window.removeEventListener('hashchange',selectLinkedNode);};
  }
})(typeof window==='undefined'?globalThis:window);
