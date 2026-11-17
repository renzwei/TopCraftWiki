/* Build player-facing class and skill entries from game lore and compact editorial notes. */
const fs=require('node:fs'),path=require('node:path'),C=require('../assets/combat.js');
const data=require('../assets/data/combat.json'),notes=require('../_maintenance/combat-editorial.json');
const root=path.resolve(__dirname,'..'),esc=C.escape;
const slugs=['sweep','rift-slash','flying-hammer','charge','leap','totem','fireball','mana-slash','ice-arrow','blink','chain-lightning','meteor','divine-slash','holy-bolt','divine-descent','watchful-eye','holy-pilgrimage','heavenly-sword'];
const names=['横扫','裂震斩','飞锤','冲锋','跃击','图腾','火球术','魔切','寒冰箭','闪现','闪电链','陨石','神辉斩','圣光弹','天神降临','守望之眼','圣翼巡礼','天赐圣剑'];
const pages=Object.fromEntries(names.map((n,i)=>[n,'combat/skills/'+slugs[i]+'.md']));
const classes={战士:{slug:'warrior',intro:'战士拥有三种职业中最高的基础生命，擅长近身范围攻击，可通过冲锋和跃击接近敌人。'},法师:{slug:'mage',intro:'法师使用火焰、冰霜和雷电攻击敌人，可远程施法或近身斩击，并通过闪现调整位置。'},牧师:{slug:'priest',intro:'牧师以神辉攻击敌人、治疗友军，也能召唤天神与圣眼协同作战。'}};
const link=n=>'#/'+pages[n].replace(/\.md$/,'');
const classLink=cls=>'#/combat/'+classes[cls].slug;
function write(file,text){fs.writeFileSync(path.join(root,file),text.trim()+'\n');}
function rich(t){return t.replace(/`([^`]+)`/g,'<code>$1</code>').replace(/\[([^\]]+)\]\(([^)]+)\.md\)/g,'<a href="#/$2">$1</a>');}
function description(s){
 const text=s.lore.filter(l=>!(/^(法力消耗|暴击几率|标签|是击中|受攻击速度|[\u4e00-\u9fff]+[：:])/.test(l))).join('');
 return C.resolve(data,s.name,text,{skillLevel:1,characterLevel:1}).replace(/, /g,'，').replace(/([\u4e00-\u9fff])(\d)/g,'$1 $2').replace(/(\d)([\u4e00-\u9fff])/g,'$1 $2');
}
function mana(s){return s.name==='魔切'?6:s.name==='圣翼巡礼'?s.parameters.cost.base:s.parameters.mana.base;}
function cooldown(s){return s.parameters.cooldown.base?`${s.parameters.cooldown.base} 秒`:'无冷却 · 受攻速影响';}
function value(s,key,unit=''){const p=s.parameters[key];return `${C.fmt(p.base)}${unit}${p['per-level']?`<small>每级 +${C.fmt(p['per-level'])}${unit}</small>`:''}`;}
function stat(label,value){return `<div><dt>${label}</dt><dd>${value}</dd></div>`;}
function stats(s){
 const rows=[stat('法力消耗',mana(s)),stat('冷却时间',cooldown(s))];
 const labels={damage:s.name==='闪现'?'闪现降临伤害':s.name==='图腾'?'每支尖刺伤害':s.name==='天神降临'?'天神普攻伤害':s.name==='守望之眼'?'圣眼伤害':'基础伤害',healing:s.name==='天赐圣剑'?'每秒治疗':'基础治疗',health:'圣眼生命',range:s.name==='闪现'?'传送距离':'距离',radius:'区域半径',height:'升空高度',duration:'持续时间'};
 for(const [key,label] of Object.entries(labels))if(s.parameters[key])rows.push(stat(label,value(s,key,['range','radius','height'].includes(key)?' 格':key==='duration'?' 秒':'')));
 if(s.parameters.durationTicks)rows.push(stat('持续时间',C.fmt(s.parameters.durationTicks.base/20)+' 秒'));
 if(s.name==='图腾'){rows.push(stat('持续时间','12 秒'));rows.push(stat('图腾生命','100<small>职业每级 +4</small>'));}
 if(s.name==='天神降临')rows.push(stat('基础天神生命','牧师最大生命的 100%'));
 if(s.parameters.criticalChance&&s.name!=='图腾'){
  rows.push(stat('技能额外暴击率',value(s,'criticalChance','%')));rows.push(stat('基础暴击伤害',value(s,'criticalPower','%')));
 }
 return `<dl class="skill-stats">${rows.join('')}</dl>`;
}
function tags(s){let text=s.lore.find(l=>l.startsWith('标签：'))?.slice(3)||'';if(s.name==='寒冰箭')text='法术、爆炸';if(s.name==='闪电链')text='法术';if(s.name==='陨石')text='法术、爆炸';return text.split('、').map(t=>`<span><a href="#/combat/damage?id=types">${esc(t)}</a></span>`).join('');}
function siblings(cls,active){return `<nav class="skill-switcher" aria-label="${cls}技能">${Object.values(data.skills).filter(s=>s.class===cls).map(s=>`<a href="${link(s.name)}"${s.name===active?' aria-current="page"':''}><img src="${s.icon}" alt=""><span>${s.name}</span><small>${s.unlock} 级</small></a>`).join('')}</nav>`;}
function skillRow(s){return `<article class="class-skill"><a class="class-skill-icon" href="${link(s.name)}"><img src="${s.icon}" alt="${s.name}"></a><div><div class="class-skill-heading"><h3><a href="${link(s.name)}">${s.name}</a></h3><span>${s.unlock} 级解锁</span></div><p>${C.linkMechanics(description(s))}</p><div class="class-skill-meta"><span>法力 ${mana(s)}</span><span>${cooldown(s)}</span><a href="${link(s.name)}">技能详情与技能树 →</a></div></div></article>`;}
for(const s of Object.values(data.skills)){
 const slug=slugs[names.indexOf(s.name)];
 let md=`<nav class="wiki-breadcrumb" aria-label="当前位置"><a href="#/combat/classes">职业</a><span>›</span><a href="${classLink(s.class)}">${s.class}</a><span>›</span><span>${s.name}</span></nav>\n\n# ${s.name}\n\n`;
 md+=siblings(s.class,s.name)+'\n\n';
 md+=`<section class="skill-overview" aria-label="${s.name}技能效果"><div class="skill-overview-heading"><img src="${s.icon}" alt="${s.name}"><div><div class="skill-tags">${tags(s)}</div><span>${s.class} · ${s.unlock} 级解锁 · 技能上限 ${s.maxLevel} 级</span></div></div><p class="game-description">${C.linkMechanics(description(s))}</p>${stats(s)}${s.name==='闪现'?'<p class="skill-footnote">闪现降临的伤害在学习对应节点后生效。</p>':''}</section>\n\n`;
 md+=`## 技能树\n\n<div data-skill-tree="${s.name}">正在加载 ${s.name} 技能树…</div>\n\n`;
 if(notes[slug]?.length)md+=`<details class="skill-mechanics"><summary>技能交互说明</summary><ul>${notes[slug].map(n=>`<li>${rich(n)}</li>`).join('')}</ul></details>\n\n`;
 md+=`<div class="combat-related"><a href="${classLink(s.class)}">${s.class}全部技能</a><a href="#/combat/progression">升级与技能加点</a><a href="#/combat/damage">伤害与暴击</a><a href="#/combat/defense">防御与恢复</a><a href="#/combat/status-effects">状态与控制</a></div>\n\n<div class="page-end">TopCraft 玩家手册 · 数据更新 ${data.date}</div>`;
 write(pages[s.name],md);
}
for(const [cls,info] of Object.entries(classes)){
 const c=data.classes[cls].attributes;
 let md=`<nav class="wiki-breadcrumb" aria-label="当前位置"><a href="#/combat/classes">职业</a><span>›</span><span>${cls}</span></nav>\n\n# ${cls}\n\n<p class="lead">${info.intro}</p>\n\n<nav class="class-tabs" aria-label="职业">${Object.entries(classes).map(([n,v])=>`<a href="#/combat/${v.slug}"${n===cls?' aria-current="page"':''}>${n}</a>`).join('')}<a href="#/combat/skills">全部技能</a></nav>\n\n## 基础属性\n\n`;
 md+=`<dl class="class-growth">${stat('生命',`${c['max-health'].base}<small>每级 +${c['max-health']['per-level']}</small>`)}${stat('法力',`${c['max-mana'].base}<small>每级 +${c['max-mana']['per-level']}</small>`)}${stat('生命恢复',c['health-regeneration'].base+' / 秒')}${stat('法力恢复',c['mana-regeneration'].base+' / 秒')}</dl>\n\n`;
 md+=`## 职业技能\n\n<div class="class-skills">${Object.values(data.skills).filter(s=>s.class===cls).map(skillRow).join('')}</div>\n\n`;
 md+='<div class="combat-related"><span>职业上限 30 级</span><a href="#/combat/progression">升级、加点与技能操作</a><a href="#/combat/builds">加点方案与预设</a></div>';
 write('combat/'+info.slug+'.md',md);
}
let index='<p class="eyebrow">TOPCRAFT / 职业与技能</p>\n\n# 技能图鉴\n\n<p class="lead">按职业查看技能效果、消耗、成长与技能树。</p>\n\n';
for(const cls of Object.keys(classes))index+=`## ${cls}\n\n<div class="class-skills">${Object.values(data.skills).filter(s=>s.class===cls).map(skillRow).join('')}</div>\n\n`;
write('combat/skills.md',index);
write('_maintenance/combat-pages.json',JSON.stringify(pages,null,2));
const sources=JSON.parse(fs.readFileSync(path.join(root,'_maintenance/sources.json'),'utf8'));
for(const s of Object.values(data.skills))sources[pages[s.name]]=s.sources;
sources['combat/progression.md']=sources['combat/skills.md'];
write('_maintenance/sources.json',JSON.stringify(sources,null,2));
const routes=['/'];for(const dir of ['combat','guide','equipment','world','quests','dungeons','life','social']){
 for(const f of fs.readdirSync(path.join(root,dir),{recursive:true}).filter(f=>f.endsWith('.md')))routes.push('/'+dir+'/'+f.replaceAll('\\','/').replace(/\.md$/,''));
}
write('assets/search-paths.js','window.TopCraftSearchPaths = '+JSON.stringify(routes)+';');
console.log('Built 3 class pages, 18 skill entries, skill index and search routes.');
