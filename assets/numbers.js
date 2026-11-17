/* Presentation only: keep source values and arithmetic at their original precision. */
(function(root){
  'use strict';
  const fixed=new Intl.NumberFormat('zh-CN',{minimumFractionDigits:1,maximumFractionDigits:1});
  function value(n){n=Number(n);return Number.isFinite(n)?fixed.format(Math.abs(n)<.05?0:n):'—';}
  const token=/[+-]?\d+(?:,\d{3})*(?:\.\d+)?(?:e[+-]?\d+)?/gi;
  const countUnit='(?:级|层|个(?!百分点)|件|项|次|人|种|枚|把|支|只|名|套|份|组|点技能|点天赋|点属性|格槽位|tick\\b)';
  const counted=new RegExp('^\\s*(?:[–—~～至/-]\\s*\\d+(?:\\.\\d+)?)?\\s*[\\ue000-\\uf8ff]*\\s*'+countUnit);
  const measured=/^\s*(?:%|％|秒|分钟|小时|金币|经验|倍|格(?!槽位)|米|点(?:伤害|治疗|生命|法力)|(?:物理|火焰|冰霜|雷电|闪电|毒素|持续|技能|近战|远程|召唤物)*伤害|生命|法力|护盾|护甲|抗性)/;
  function text(source,all=false,suffix=''){
    return String(source).replace(token,(raw,offset,s)=>{
      const before=s.slice(0,offset),after=s.slice(offset+raw.length)+suffix;
      // Versions, identifiers, clocks, dates, formula powers and item counts are not measurements.
      if(/[\w.]$/.test(before)||/^[\w.]/.test(after)||/\d:$/.test(before)||/^:\d/.test(after)||/[\d/]\^?$/.test(before)||/^\^/.test(after))return raw;
      if(counted.test(after)||/[×x]\s*$/.test(before)||/第\s*$/.test(before)||/(?:层数|数量|次数|等级|人数|弹射数|目标数)(?:上限|下限)?\s*[:：]?\s*$/.test(before))return raw;
      const metricBefore=/(?:生命|法力|伤害|治疗|护盾|护甲|抗性|攻击速度|飞行速度|冷却时间|持续时间|暴击率|暴击几率|暴击伤害|经验|金币)(?:值|上限|消耗|恢复|加成)?\s*[：:]?\s*$/.test(before);
      const measurementTail=after.replace(/^\s*[–—~～至-]\s*[+-]?\d+(?:\.\d+)?/,'');
      if(!all&&!measured.test(measurementTail)&&!metricBefore)return raw;
      const n=Number(raw.replaceAll(',',''));
      return (raw.startsWith('+')?'+':'')+value(n);
    });
  }
  const metric=/生命|法力|伤害|治疗|攻击|防御|护甲|抗性|恢复|暴击|几率|概率|速度|倍率|加成|成长|经验|价格|卖价|费用|金币|耐久|中心值|数值|持续|冷却|时间|距离|半径/;
  const counter=/等级|层数|数量|次数|用量|收获|门槛|拉竿|人数|点数|阶段|赞赏数量|当前赞赏|累计登录/;
  function mount(main){
    if(!main)return;
    const metrics=new Set(main.querySelectorAll('.skill-stats dd,.class-growth dd,.eq-stats dd'));
    main.querySelectorAll('table').forEach(table=>{
      const headers=Array.from(table.querySelectorAll('thead th')).map(th=>th.textContent);
      table.querySelectorAll('tbody tr').forEach(row=>{
        const cells=Array.from(row.cells),rowLabel=cells[0]?.textContent||'';
        cells.forEach((cell,i)=>{
          const head=headers[i]||'';
          if(i>0&&!counter.test(head)&&((metric.test(head))||(metric.test(rowLabel)&&/基础|当前|每级|效果|上限|下限|范围/.test(head))))metrics.add(cell);
        });
      });
    });
    const skip='a,code,pre,script,style,button,select,textarea,input,h1,h2,h3,h4,nav,.page-end,.eyebrow,.wiki-page-meta,.world-coordinate,.world-map,.guide-facts,[data-number-raw],.formula,.formula-box';
    const walker=document.createTreeWalker(main,NodeFilter.SHOW_TEXT);
    const nodes=[];while(walker.nextNode())nodes.push(walker.currentNode);
    nodes.forEach(node=>{
      const parent=node.parentElement;if(!parent||parent.closest(skip))return;
      let all=false;for(let p=parent;p&&p!==main;p=p.parentElement){if(metrics.has(p)){all=true;break;}}
      const original=node.nodeValue;
      // Adjacent links/icons may split a value from its measurement unit.
      let suffix='';for(let next=node.nextSibling;next;next=next.nextSibling){suffix+=next.textContent||'';if(suffix.length>80)break;}
      // Use following linked labels as context, never rewrite their names or destinations.
      const formatted=text(original,all,suffix);
      if(formatted!==original){
        node.nodeValue=formatted;
        if(!parent.title)parent.title='原始数值：'+original.trim();
      }
    });
  }
  const api={value,text,mount};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;
  else root.TopCraftNumbers=api;
})(typeof window==='undefined'?globalThis:window);
