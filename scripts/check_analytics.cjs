'use strict';
const assert = require('node:assert/strict'), fs = require('node:fs'), vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname,'../assets/analytics.js'),'utf8');
function setup(hostname='wiki.topcraft.cc', protocol='https:') {
  const scripts=[],timers=new Map(),input={value:''}; let id=0;
  const context={window:{TopCraftSearchPaths:['/','/guide/help','/equipment/overview']},
    location:{hostname,protocol,origin:protocol+'//'+hostname,pathname:'/'},
    document:{title:'TopCraft Wiki',referrer:'https://example.com/page?private=value#secret',head:{append:s=>scripts.push(s)},
      createElement:()=>({}),querySelector:()=>input}, URL,
    setTimeout:fn=>{timers.set(++id,fn);return id;},clearTimeout:key=>timers.delete(key)};
  vm.runInNewContext(source,context);
  return {context,scripts,input,api:context.window.TopCraftAnalytics,
    flush(){const pending=[...timers.values()];timers.clear();pending.forEach(fn=>fn());},
    events(){return Array.from(context.window.dataLayer||[],a=>Array.from(a)).filter(a=>a[0]==='event');}};
}
for(const [host,protocol] of [['127.0.0.1','http:'],['localhost','http:'],['example.com','https:'],['wiki.topcraft.cc','http:']]){
  const s=setup(host,protocol);assert.equal(s.scripts.length,0);assert.equal(s.api,undefined);
}
const s=setup();
assert.equal(s.scripts.length,1);
assert.equal(s.scripts[0].src,'https://www.googletagmanager.com/gtag/js?id=G-GGTHGX9V8E');
assert.equal(s.context.window.dataLayer[1][2].send_page_view,false);
s.api.mount('/');s.api.mount('/?id=目录');
assert.equal(s.events().length,1);
assert.equal(s.events()[0][2].page_referrer,'https://example.com/page');
s.context.document.title='装备与道具 · TopCraft 玩家手册';
s.api.mount('/equipment/overview.md');s.api.mount('/equipment/overview?id=强化');
assert.equal(s.events().length,2);
assert.equal(s.events()[1][2].page_location,'https://wiki.topcraft.cc/#/equipment/overview');
assert.equal(s.events()[1][2].page_title,s.context.document.title);
assert.equal(s.events()[1][2].page_referrer,'https://wiki.topcraft.cc/#/');
s.api.mount('/');assert.equal(s.events().length,3);
s.input.value='不存在的材料';
s.api.search(s.input.value,0,false);s.flush();assert.equal(s.events().length,3);
s.api.search(s.input.value,1,true);s.flush();assert.equal(s.events().length,3);
s.api.search(s.input.value,0,true);s.flush();assert.equal(s.events()[3][1],'search_no_results');
s.api.search(s.input.value,0,true);s.flush();assert.equal(s.events().length,4);
for(const query of ['a@b.cc','https://example.com','123456789','火']){
  s.input.value=query;s.api.search(query,0,true);s.flush();assert.equal(s.events().length,4);
}
s.input.value='另一个词';s.api.search(s.input.value,0,true);s.input.value='';s.flush();assert.equal(s.events().length,4);
s.input.value='另一个词';s.api.search(s.input.value,0,true);s.api.mount('/guide/help');s.flush();assert.equal(s.events().length,5);
s.api.mount('/not-a-page');assert.equal(s.events().length,5);
console.log('GA4: production-only loading, manual page views, canonical routes, anchor deduplication, referrers and settled empty searches passed.');
