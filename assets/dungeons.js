(() => {
  'use strict';
  const numbers=typeof window!=='undefined'&&window.TopCraftNumbers||require('./numbers.js');
  function calculate(rules, mapId, layer, seconds, deaths) {
    const map = rules.maps.find(m => m.id === mapId);
    if (!map || !Number.isInteger(layer) || layer < 1 || layer > rules.keyRules['maximum-layer'] ||
        !Number.isFinite(seconds) || seconds < 0 || seconds > 864000 ||
        !Number.isInteger(deaths) || deaths < 0 || deaths > 100000) return {error:'请输入有效数值：层数 1–100000，耗时 0–14400 分钟，死亡次数为非负整数。'};
    const effectiveMs = Math.round(seconds * 1000) + deaths * rules.deathPenalty * 1000;
    const t = BigInt(effectiveMs), limit = BigInt(map.limit * 1000), s = rules.scoreRules, f = s.formula;
    const base = BigInt(f.layerPoints) * BigInt(layer) + BigInt(f.basePoints);
    const timed = t <= limit;
    let raw;
    if (timed) {
      const bonus = (limit - t) * BigInt(f.timeBonusSlope) / limit;
      raw = base + (bonus < BigInt(f.maxTimeBonus) ? bonus : BigInt(f.maxTimeBonus));
    } else {
      const coefficient = limit * BigInt(s.overtimeStartBps) - (t - limit) * BigInt(s.decayBps);
      const floor = limit * BigInt(s.overtimeFloorBps);
      raw = base * (coefficient > floor ? coefficient : floor) / (limit * 10000n);
    }
    return {effectiveMs, score:Number(raw / 100n), rawScore:Number(raw), timed,
      rapid:effectiveMs <= map.limit * 1000 * rules.rapidRatio,
      key:layer === rules.unkeyedLayer ? null : Math.max(rules.keyRules['minimum-layer'],Math.min(rules.keyRules['maximum-layer'],layer + (timed ? rules.keyRules['timed-change'] : rules.keyRules['overtime-change'])))};
  }
  function multiplier(layer, growth) {
    const log = (layer - 1) * Math.log10(growth);
    if (log < 6) return numbers.value(growth ** (layer - 1)) + ' 倍';
    let exponent=Math.floor(log),mantissa=10**(log-exponent);
    if(numbers.value(mantissa)==='10'){mantissa=1;exponent++;}
    return numbers.value(mantissa) + ' × 10^' + exponent + ' 倍';
  }
  function time(ms) {const seconds=Math.floor(ms/1000);return Math.floor(seconds/60)+':'+String(seconds%60).padStart(2,'0');}
  function output(root, values) {
    const result=root.querySelector('.dg-results');result.replaceChildren();
    for(const [label,value] of values){const box=document.createElement('div'),a=document.createElement('span'),b=document.createElement('strong');a.textContent=label;b.textContent=value;box.append(a,b);result.append(box);}
  }
  let dataPromise;
  async function mount(){
    const roots=[...document.querySelectorAll('[data-dungeon-tool]:not([data-ready])')];
    if(!roots.length)return;
    roots.forEach(r=>r.dataset.ready='loading');
    let data;
    try{data=await(dataPromise ||= fetch('assets/data/dungeons.json').then(r=>{if(!r.ok)throw Error();return r.json();}));}
    catch{dataPromise=null;roots.forEach(r=>{delete r.dataset.ready;r.querySelector('[role=status]').textContent='工具暂时无法加载，请刷新页面。下方正文仍可查阅。';});return;}
    roots.forEach(root=>{
      if(!root.isConnected)return;
      root.dataset.ready='true';
      const error=root.querySelector('[role=status]');
      const update=()=>{
        const inputs=[...root.querySelectorAll('input')];
        if(inputs.some(i=>i.value.trim()===''||!i.checkValidity())){error.textContent='请填写有效数值，层数和死亡次数须为整数。';root.querySelector('.dg-results').replaceChildren();return;}
        error.textContent='';
        const layer=Number(root.querySelector('[name=layer]').value);
        if(root.dataset.dungeonTool==='difficulty'){
          output(root,[['挑战层数',layer+' 层'],['生命倍率 · 相对 1 层',multiplier(layer,data.growth)],['伤害倍率 · 相对 1 层',multiplier(layer,data.growth)]]);return;
        }
        const seconds=Number(root.querySelector('[name=minutes]').value)*60+Number(root.querySelector('[name=seconds]').value);
        const r=calculate(data,root.querySelector('[name=map]').value,layer,seconds,Number(root.querySelector('[name=deaths]').value));
        if(r.error){error.textContent=r.error;root.querySelector('.dg-results').replaceChildren();return;}
        output(root,[['结算耗时 · 含全队罚时',time(r.effectiveMs)],['通关评价',r.rapid?'裂界速通':r.timed?'限时通关':'超时通关'],['预计单图成绩',numbers.value(r.score)+' 分'],['通关后的钥匙',r.key===null?'未使用钥匙':r.key+' 层'],['本次死亡罚时',numbers.value(root.querySelector('[name=deaths]').value*data.deathPenalty)+' 秒'],['限时内是否完成',r.timed?'是':'否']]);
      };
      root.addEventListener('input',update);root.addEventListener('change',update);update();
    });
  }
  if(typeof window!=='undefined')window.TopCraftDungeons={mount};
  if(typeof module!=='undefined')module.exports={calculate,multiplier};
})();
