(() => {
  'use strict';
  function joinRange(text,rules) {
    const raw=text.trim();
    if(!raw)return {error:'请输入至少一名现有队员的等级。'};
    const tokens=raw.split(/[,，、;；\s]+/),levels=tokens.map(Number);
    if(tokens.some(t=>!/^\d+$/.test(t))||levels.some(n=>!Number.isSafeInteger(n)||n<1||n>rules.maxLevel))return {error:'等级须为 1–'+rules.maxLevel+' 的整数，可用逗号或空格分隔。'};
    if(levels.length>rules.maxMembers)return {error:'队伍最多 '+rules.maxMembers+' 人，请核对输入人数。'};
    const min=Math.min(...levels),max=Math.max(...levels),count=levels.length;
    if(count===rules.maxMembers)return {count,min,max,error:'队伍已有 '+count+' 人，人数已满。'};
    if(max-min>rules.maxSpread)return {count,min,max,error:'当前最高与最低等级相差 '+(max-min)+' 级，超过 '+rules.maxSpread+' 级，暂时不能加入新队员。'};
    return {count,min,max,low:Math.max(1,max-rules.maxSpread),high:Math.min(rules.maxLevel,min+rules.maxSpread)};
  }
  let data;
  window.TopCraftSocial={mount(){
    const root=document.querySelector('[data-party-calculator]:not([data-ready])');if(!root)return;
    data ||= fetch('assets/data/social.json').then(r=>{if(!r.ok)throw Error('data');return r.json();}).catch(e=>{data=null;throw e;});
    data.then(rules=>{
      if(!root.isConnected||root.dataset.ready)return;root.dataset.ready='true';
      const field=root.querySelector('input'),result=root.querySelector('[role=status]');
      const update=()=>{const r=joinRange(field.value,rules);result.textContent=r.error||r.count+' 人队伍 · 等级 '+r.min+'–'+r.max+'：可加入 '+r.low+'–'+r.high+' 级的玩家，剩余 '+(rules.maxMembers-r.count)+' 个位置。';};
      field.addEventListener('input',update);update();
    }).catch(()=>{if(root.isConnected)root.querySelector('[role=status]').textContent='查询暂时无法加载，可按下方规则计算。';});
  }};
  if(typeof module!=='undefined')module.exports={joinRange};
})();
