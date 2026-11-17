const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'..'),ctx={window:{},module:{exports:{}}};
vm.runInNewContext(fs.readFileSync(path.join(root,'assets/social.js'),'utf8'),ctx);
const {joinRange}=ctx.module.exports,rules=JSON.parse(fs.readFileSync(path.join(root,'assets/data/social.json'),'utf8'));
for(const [input,low,high] of [['10,12,15',10,15],['1',1,6],['30',25,30],['12，12 13',8,17],['25,30',25,30]]){
 const r=joinRange(input,rules);assert.equal(r.low,low);assert.equal(r.high,high);
}
for(const input of ['','10,16','1,1,1,1,1,1,1,1','1,1,1,1,1,1,1,1,1','0','31','2.5','NaN','<script>'])assert.ok(joinRange(input,rules).error,input);
// Every advertised joining level preserves the whole-party limit, including boundary levels.
for(let a=1;a<=rules.maxLevel;a++)for(let b=a;b<=Math.min(rules.maxLevel,a+rules.maxSpread);b++){
 const r=joinRange(a+','+b,rules);
 for(let c=1;c<=rules.maxLevel;c++)assert.equal(c>=r.low&&c<=r.high,Math.max(a,b,c)-Math.min(a,b,c)<=rules.maxSpread);
}
console.log('Social party range: examples, invalid input, full parties and all boundary combinations passed.');
