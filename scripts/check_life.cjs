// Arithmetic checks for the player queries; no browser/server changes.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),context={window:{TopCraftNumbers:require('../assets/numbers.js')},module:{exports:{}},Intl};
vm.runInNewContext(fs.readFileSync(path.join(root,'assets/life.js'),'utf8'),context);
const {salePrice,reward,fishProbabilities,xp}=context.module.exports;
const data=JSON.parse(fs.readFileSync(path.join(root,'assets/data/life.json'),'utf8'));
assert.equal(salePrice('1.00','0.01',50),'1.50');
assert.equal(salePrice('1.50','0.01',1),'1.52'); // HALF_UP: 1.515 -> 1.52
assert.equal(salePrice('0.05','0.01',10),'0.06'); // Exact half-cent, not binary floating point.
assert.equal(salePrice('3.25','0.01',100),'6.50');
assert.equal(reward(data,'cooking','daily',1),12);
assert.equal(reward(data,'cooking','daily',5),24);
assert.equal(reward(data,'mining','daily',100),1200);
assert.equal(xp(data.curves.cooking,5,6).total,21);
assert.equal(xp(data.curves.cooking,100,100).total,0);
const weights=data.fish.map(f=>f.weight),zero=fishProbabilities(weights,0),lucky=fishProbabilities(weights,100);
assert.ok(Math.abs(zero.reduce((a,b)=>a+b,0)-100)<1e-10);
assert.ok(Math.abs(lucky.reduce((a,b)=>a+b,0)-100)<1e-10);
const rare=data.fish.findIndex(f=>f.item==='GOLDEN_KING_FISH');
assert.ok(lucky[rare]>zero[rare]);
const common=data.fish.findIndex(f=>f.item==='CLAM');
assert.ok(lucky[common]<zero[common]);
assert.equal(new Set(data.recipes.map(r=>r.id)).size,data.recipes.length);
for(const recipe of data.recipes){assert.ok(recipe.level>=1&&recipe.level<=100);assert.ok(recipe.amount>0);assert.ok(recipe.xp>=0);assert.ok(recipe.ingredients.length);}
console.log(JSON.stringify({recipes:data.recipes.length,fish:data.fish.length,professions:Object.keys(data.curves).length,query_checks:'passed'}));
