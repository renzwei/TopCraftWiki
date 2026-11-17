const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),data=require('../assets/data/combat.json'),C=require('../assets/combat.js');
let count=0;const errors=[];
for(const s of Object.values(data.skills)){
 const ids=new Set(s.nodes.map(n=>n.id));
 assert.equal(ids.size,s.nodes.length); assert.equal(s.nodes.filter(n=>n.root).length,1);
 const seen=new Set();function visit(n,stack=new Set()) {if(stack.has(n.id))throw Error('Cycle '+n.id);if(seen.has(n.id))return;stack.add(n.id);for(const p of n.parents){assert(ids.has(p.id));const parent=s.nodes.find(n=>n.id===p.id);assert(p.level<=parent.max);visit(parent,new Set(stack));}seen.add(n.id);} s.nodes.forEach(n=>visit(n));
 for(const p of C.pathCells(s))if(!data.assets.paths[p.code])errors.push(`${s.name}: missing path ${p.code} at ${p.xy}`);
 for(const n of s.nodes){assert(fs.existsSync(path.join(root,n.icon)));for(let r=1;r<=n.max;r++)for(const skillLevel of [1,10])for(const characterLevel of [1,30]){
  try{const plain=C.lore(data,s.name,n,r,{skillLevel,characterLevel});const rich=C.lore(data,s.name,n,r,{skillLevel,characterLevel,rich:true});
   assert.deepEqual(rich.map(l=>[...l].filter(c=>!data.assets.loreIcons[c]).join('').trim()),plain);
   count++;}catch(e){errors.push(`${s.name}/${n.id}/${r}: ${e.message}`);}
 }}
 for(const l of s.lore)try{C.resolve(data,s.name,l);}catch(e){errors.push(e.message);}
}
assert.equal(C.parameter(data,'火球术','damage',1),5);assert.equal(C.parameter(data,'火球术','damage',10),32);
assert.equal(C.parameter(data,'圣光弹','healing',10),19.5);
assert.equal(C.arithmetic('1+0.04*(min(30,max(1,30))-1)'),2.16);
assert.throws(()=>C.arithmetic('process.exit()'));
for(const src of Object.values(data.assets.loreIcons))assert(fs.existsSync(path.join(root,src)));
const zeal=data.skills['飞锤'].nodes.find(n=>n.id==='飞锤热诚');
const zealHtml=C.lore(data,'飞锤',zeal,1,{rich:true}).map(l=>C.renderLore(data,l)).join('');
assert(zealHtml.includes('abilities/flying_hammer_zeal.png'));
assert(zealHtml.includes('stats/stacks.png'));
assert.equal(C.renderLore(data,'<script>'), '&lt;script&gt;');
assert(C.linkMechanics('火花电荷').includes('status-effects?id=spark'));
assert.equal((C.linkMechanics('召唤物伤害').match(/<a /g)||[]).length,1);
assert(!C.linkMechanics('<script>护盾</script>').includes('<script>'));
for(const route of Object.values(C.mechanicLinks)){
 const [slug,query]=route.split('?'),page=fs.readFileSync(path.join(root,'combat',slug+'.md'),'utf8');
 if(query){const id=new URLSearchParams(query).get('id');assert(page.includes('id="'+id+'"')||page.includes(':id='+id),`Missing entry ${route}`);}
}
console.log(`${Object.keys(data.skills).length} skills, ${count} rank/level previews checked.`);
if(errors.length){console.error(errors.slice(0,35).join('\n'));console.error(errors.length+' errors');process.exitCode=1;}else console.log('Combat data and formulas passed.');
