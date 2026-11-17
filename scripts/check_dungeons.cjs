const assert=require('node:assert/strict');
const {calculate,multiplier}=require('../assets/dungeons.js');
const rules=require('../assets/data/dungeons.json');
const score=(layer,time,deaths=0,map='1001')=>calculate(rules,map,layer,time,deaths);
// Values at the discontinuities are important: rapid, timed, overtime and floor.
assert.equal(score(10,360).score,120);
// Match finish()'s double comparison: 720000 * .7 is just below 504000.
assert.equal(score(10,503.999).rapid,true);
assert.equal(score(10,504).rapid,false);
assert.equal(score(10,504).score,116);
assert.equal(score(10,504.001).rapid,false);
assert.equal(score(10,720).timed,true);
assert.equal(score(10,720).score,110);
assert.equal(score(10,720).key,11);
assert.equal(score(10,720.001).timed,false);
assert.equal(score(10,721).score,76);
assert.equal(score(10,721).key,9);
assert.equal(score(10,1080).score,55);
assert.equal(score(10,5000).score,55);
assert.equal(score(10,700,2).effectiveMs,730000);
assert.equal(score(10,700,2).timed,false);
assert.equal(score(10,490,1).rapid,false);
assert.equal(score(2,900).key,2);
assert.equal(score(1,300).key,null);
assert.equal(score(100000,300).key,100000);
assert.equal(score(10,630,0,'1004').rapid,true);
assert.equal(score(10,900,0,'1004').timed,true);
assert.equal(score(10,1350,0,'1004').score,55);
for(const a of [[0,20],[-1,20],[1.5,20],[100001,20],[NaN,20],[10,-1],[10,Infinity],[10,20,-1],[10,20,0.2]])assert.ok(score(...a).error);
assert.ok(calculate(rules,'invalid',1,30,0).error);
assert.equal(multiplier(1,rules.growth),'1.0 倍');
assert.equal(multiplier(2,rules.growth),'1.2 倍');
assert.ok(!multiplier(100000,rules.growth).includes('Infinity'));
// Time can never improve a completed run's score; death penalty equals extra time.
for(const map of rules.maps)for(const layer of [1,2,10,50,100000]){
 let prior=Infinity;
 for(let t=0;t<=map.limit*2;t+=7){const r=score(layer,t,0,map.id);assert.ok(r.rawScore<=prior);prior=r.rawScore;assert.equal(score(layer,t,2,map.id).rawScore,score(layer,t+30,0,map.id).rawScore);}
}
console.log('Dungeon calculations: threshold boundaries, key limits, input validation, score monotonicity and death penalties passed.');
