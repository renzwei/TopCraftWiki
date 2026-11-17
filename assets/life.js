(() => {
  'use strict';
  let pending;
  const number=(value,min,max,fallback)=>Number.isFinite(Number(value))&&String(value).trim()!==''?Math.max(min,Math.min(max,Number(value))):fallback;
  const integer=(v,min,max,fallback)=>Math.floor(number(v,min,max,fallback));
  const numbers=typeof window!=='undefined'&&window.TopCraftNumbers||require('./numbers.js');
  const format=numbers.value;
  // The server rounds each unit price HALF_UP before multiplying by quantity.
  function salePrice(base,bonus,level) {
    function decimal(s) {const [a,b='']=String(s).split('.');return [BigInt(a+b),10n**BigInt(b.length)];}
    const [b,bd]=decimal(base),[r,rd]=decimal(bonus),den=bd*rd;
    const scaled=b*(rd+r*BigInt(level))*100n;
    const cents=(scaled*2n+den)/(2n*den);
    return `${cents/100n}.${String(cents%100n).padStart(2,'0')}`;
  }
  function reward(data,skill,cycle,level) {
    let value=0;
    for(const row of data.rewards[skill][cycle])if(row.min_level<=level)value=row.experience;
    return value;
  }
  function fishProbabilities(weights,luck) {
    const power=Math.pow(1+.07*luck,-.33333333333);
    const adjusted=weights.map(w=>Math.pow(w,power)),total=adjusted.reduce((a,b)=>a+b,0);
    return adjusted.map(w=>100*w/total);
  }
  function xp(curve,level,target) {
    let total=0;
    for(let l=level;l<target;l++)total+=curve[Math.min(curve.length,l)-1];
    return {next:level===100?0:curve[Math.min(curve.length,level)-1],total};
  }
  function mountFilter(root,data) {
    if(!root.isConnected || root.dataset.ready)return;root.dataset.ready='true';
    const main=root.closest('.markdown-section'),rows=[...main.querySelectorAll('[data-life-row]')];
    const query=new URLSearchParams(location.hash.split('?')[1]||'');
    const search=root.querySelector('[data-life-search]'),profession=root.querySelector('[data-life-prof]'),level=root.querySelector('[data-life-level]'),eligible=root.querySelector('[data-life-eligible]'),cycle=root.querySelector('[data-life-cycle]');
    if(profession && [...profession.options].some(o=>o.value===query.get('profession')))profession.value=query.get('profession');
    if(level && query.has('level')){level.value=integer(query.get('level'),1,100,100);eligible.checked=true;}
    if(cycle && [...cycle.options].some(o=>o.value===query.get('cycle')))cycle.value=query.get('cycle');
    const anchor=rows.find(r=>r.id===query.get('id'));
    if(anchor){if(profession)profession.value=anchor.dataset.profession||'';if(level)level.value=Math.max(1,Number(anchor.dataset.level)||1);if(eligible)eligible.checked=false;}
    function refresh() {
      const lv=level?integer(level.value,1,100,1):100,needle=search.value.trim().toLocaleLowerCase();let count=0;
      for(const row of rows) {
        const min=Number(row.dataset.level)||1,max=Number(row.dataset.maxLevel)||100;
        const available=lv>=min && lv<=max;
        const match=!needle || (row.dataset.name+' '+row.textContent).toLocaleLowerCase().includes(needle);
        row.hidden=!(match && (!profession?.value || row.dataset.profession===profession.value) && (!cycle?.value || row.dataset.cycle===cycle.value) && (!eligible?.checked || available));
        if(!row.hidden)count++;
        const result=row.querySelector('[data-reward]');
        if(result)result.textContent=available?`${lv} 级时奖励 ${format(reward(data,row.dataset.profession,row.dataset.cycle,lv))} ${data.professions[row.dataset.profession]}经验`:`当前等级不可接取（要求 ${min}–${max} 级）`;
        row.querySelectorAll('[data-choice-level]').forEach(choice=>{
          choice.hidden=Number(choice.dataset.choiceLevel)>lv;
          const status=choice.querySelector('[data-choice-status]');
          if(status)status.textContent=Number(choice.dataset.craftLevel)>lv?' · 当前等级尚不能制作':'';
        });
      }
      root.querySelector('[data-life-count]').textContent=`${count} / ${rows.length} 项`;
      const empty=main.querySelector('.life-empty');if(empty)empty.hidden=count>0;
    }
    root.addEventListener('input',refresh);root.addEventListener('change',refresh);refresh();
    const sale=root.querySelector('[data-sale-level]');
    if(sale) {
      const update=()=>{const lv=integer(sale.value,1,100,1);main.querySelectorAll('[data-sale-base]').forEach(el=>{const price=salePrice(el.dataset.saleBase,el.dataset.saleBonus,lv);el.textContent=format(price);el.title='精确单价：'+price+' 金币';});};
      sale.addEventListener('input',update);update();
    }
    const luck=root.querySelector('[data-fish-luck]');
    if(luck) {
      const update=()=>{const probs=fishProbabilities(rows.map(r=>Number(r.dataset.weight)),number(luck.value,0,1000,0));rows.forEach((row,i)=>{row.querySelector('[data-fish-prob]').textContent=format(probs[i])+'%';});};
      luck.addEventListener('input',update);update();
    }
  }
  function mountXP(root,data) {
    if(!root.isConnected || root.dataset.ready)return;root.dataset.ready='true';
    const prof=root.querySelector('[data-xp-prof]'),level=root.querySelector('[data-xp-level]'),target=root.querySelector('[data-xp-target]'),result=root.querySelector('[data-xp-result]');
    function refresh() {
      const lv=integer(level.value,1,100,1),to=integer(target.value,1,100,25),value=xp(data.curves[prof.value],lv,to);
      result.textContent=to<lv?'目标等级不能低于当前等级。':`${data.professions[prof.value]} ${lv} 级${lv===100?'已满级':' → '+(lv+1)+' 级需要 '+format(value.next)+' 经验'}；${lv} → ${to} 级共需 ${format(value.total)} 经验。`;
    }
    root.addEventListener('input',refresh);root.addEventListener('change',refresh);refresh();
  }
  window.TopCraftLife={mount() {
    const roots=[...document.querySelectorAll('[data-life-filter]:not([data-ready]),[data-life-xp]:not([data-ready])')];
    if(!roots.length)return;
    pending ||= fetch('assets/data/life.json').then(r=>{if(!r.ok)throw new Error('数据加载失败');return r.json();}).catch(e=>{pending=null;throw e;});
    pending.then(data=>roots.forEach(root=>root.hasAttribute('data-life-xp')?mountXP(root,data):mountFilter(root,data))).catch(()=>roots.forEach(root=>{if(root.isConnected)root.insertAdjacentHTML('beforeend','<p role="status">查询暂时无法加载，请刷新重试。下方静态资料仍可阅读。</p>');}));
  }};
  if(typeof module!=='undefined')module.exports={salePrice,reward,fishProbabilities,xp};
})();
