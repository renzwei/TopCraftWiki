'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname,'../assets/vendor/search-topcraft.js'),'utf8')
  .replace('var NO_DATA_TEXT =', 'globalThis.cacheTest = {init, saveData, index: () => INDEXS}; var NO_DATA_TEXT =');
function setup(entries = {}, options = {}) {
  const storage = {...entries}; let requests = 0;
  Object.defineProperties(storage, {
    getItem:{value:key=>{if(options.disabled)throw Error('disabled');return storage[key]??null;}},
    setItem:{value:(key,value)=>{if(options.full||options.disabled)throw Error('quota');storage[key]=String(value);}},
    removeItem:{value:key=>{if(options.disabled)throw Error('disabled');delete storage[key];}}
  });
  const context={localStorage:storage,$docsify:{plugins:[]},Docsify:{get:()=>{requests++;return{then:()=>{}};}}};
  vm.runInNewContext(source,context);
  return {api:context.cacheTest,storage,requests:()=>requests};
}
const index='docsify.search.index/topcraft-wiki-modern-v20',expiry='docsify.search.expires/topcraft-wiki-modern-v20';
const config={paths:['/'],namespace:'topcraft-wiki-modern-v20'};
const router={router:{getFile:p=>p},config:{}};
const future=String(Date.now()+86400000);
const cached=setup({[index]:'{"/":{"ok":true}}',[expiry]:future,'docsify.search.index/topcraft-wiki-old':'old','docsify.search.expires/topcraft-wiki-old':'old','topcraft-wide':'true','unrelated':'keep'});
cached.api.init(config,router);assert.equal(cached.requests(),0);assert.equal(cached.api.index()['/'].ok,true);assert.equal(cached.storage['topcraft-wide'],'true');assert.equal(cached.storage.unrelated,'keep');assert.equal(cached.storage['docsify.search.index/topcraft-wiki-old'],undefined);
for(const entries of [{[expiry]:future},{[index]:'null',[expiry]:future},{[index]:'broken',[expiry]:future},{[index]:'[]',[expiry]:future},{[index]:'{}',[expiry]:'0'}]){
  const item=setup(entries);assert.doesNotThrow(()=>item.api.init(config,router));assert.equal(item.requests(),1);
}
const full=setup({[expiry]:future},{full:true});assert.doesNotThrow(()=>full.api.saveData(1000,expiry,index));assert.equal(full.storage[expiry],undefined);
const disabled=setup({},{disabled:true});assert.doesNotThrow(()=>disabled.api.init(config,router));assert.equal(disabled.requests(),1);assert.doesNotThrow(()=>disabled.api.saveData(1000,expiry,index));
const normal=setup();normal.api.saveData(1000,expiry,index);assert.equal(normal.storage[index],'{}');assert.ok(Number(normal.storage[expiry])>Date.now());
console.log('Search cache: valid cache, obsolete index cleanup, missing/corrupt cache, quota failure and disabled storage passed.');
