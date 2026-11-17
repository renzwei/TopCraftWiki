(function () {
  'use strict';
  const dialog=document.querySelector('.wiki-search-dialog'), backdrop=document.querySelector('.wiki-backdrop'), topButton=document.querySelector('.wiki-top'), widthButton=document.querySelector('.wiki-width');
  let route='/', headings=[], toastTimer, scrollFrame=0, sidebarFrame=0;
  const collapsed=new Map();
  function toast(message) {
    let node=document.querySelector('.wiki-toast');
    if(!node){node=document.createElement('div');node.className='wiki-toast';node.setAttribute('role','status');document.body.append(node);}
    node.textContent=message;clearTimeout(toastTimer);toastTimer=setTimeout(()=>node.remove(),2200);
  }
  async function copy(text){try{await navigator.clipboard.writeText(text);toast('已复制');}catch(_){toast('无法自动复制，请选中文字后手动复制');}}
  function syncDrawer(){
    const open=innerWidth<=768&&document.body.classList.contains('close');backdrop.hidden=!open;
    const sidebar=document.querySelector('.sidebar');if(sidebar)sidebar.inert=innerWidth<=768?!open:document.body.classList.contains('close');
    const toggle=document.querySelector('.sidebar-toggle');
    if(toggle){toggle.setAttribute('aria-expanded',String(innerWidth<=768?open:!document.body.classList.contains('close')));toggle.setAttribute('aria-label','展开或收起章节目录');}
    document.body.style.overflow=open?'hidden':'';
  }
  backdrop.addEventListener('click',()=>document.body.classList.remove('close'));
  new MutationObserver(syncDrawer).observe(document.body,{attributes:true,attributeFilter:['class']});
  addEventListener('resize',syncDrawer);
  function adoptSearch(){
    const search=document.querySelector('.sidebar .search');
    if(search){document.querySelector('.wiki-search-host').replaceChildren(search);const input=search.querySelector('input');input?.setAttribute('aria-label','搜索 Wiki');input?.setAttribute('placeholder','搜索职业、技能、材料、玩法…');}
    document.querySelector('.wiki-search-host input')?.setAttribute('aria-label','搜索 Wiki');
    const clear=document.querySelector('.wiki-search-host .clear-button');
    if(clear&&!clear.dataset.accessible){clear.dataset.accessible='true';clear.setAttribute('role','button');clear.setAttribute('aria-label','清除搜索');clear.tabIndex=0;clear.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();clear.click();dialog.querySelector('input')?.focus();}});}
  }
  function openSearch(){adoptSearch();if(!dialog.open)dialog.showModal();dialog.querySelector('input')?.focus();}
  document.querySelector('.wiki-search-trigger').addEventListener('click',openSearch);
  document.querySelector('.wiki-search-close').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',event=>{
    if(event.target.closest('.matching-post a'))dialog.close();
    if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();}
  });
  document.addEventListener('keydown',event=>{
    if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==='k'){event.preventDefault();openSearch();}
    if(event.key==='Escape'&&!dialog.open&&innerWidth<=768)document.body.classList.remove('close');
  });
  try{document.body.classList.toggle('wiki-wide',localStorage.getItem('topcraft-wide')==='true');}catch(_){}
  widthButton.setAttribute('aria-pressed',String(document.body.classList.contains('wiki-wide')));
  widthButton.addEventListener('click',()=>{const wide=document.body.classList.toggle('wiki-wide');widthButton.setAttribute('aria-pressed',String(wide));try{localStorage.setItem('topcraft-wide',String(wide));}catch(_){}dispatchEvent(new Event('resize'));});
  topButton.addEventListener('click',()=>window.scrollTo({top:0,behavior:'instant'}));
  function sidebarLinks(){return Array.from(document.querySelectorAll('.sidebar-nav a[href]'));}
  function sidebarIcon(name){
    const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');
    svg.setAttribute('viewBox','0 0 24 24');svg.setAttribute('aria-hidden','true');svg.setAttribute('focusable','false');svg.classList.add('wiki-nav-icon');
    const shape=document.createElementNS('http://www.w3.org/2000/svg','path');
    shape.setAttribute('d',name==='home'?'m3 10 9-7 9 7v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1Z':'m9 5 7 7-7 7');
    svg.append(shape);return svg;
  }
  function path(link){return(link.getAttribute('href')||'').replace(/^.*#/,'').split('?')[0].replace(/\.md$/,'')||'/';}
  function updateNavigation(){
    const main=document.querySelector('.markdown-section');if(!main||!main.querySelector('.wiki-page-meta'))return;
    const links=sidebarLinks(),index=links.findIndex(a=>path(a)===route),current=links[index]||links.filter(a=>path(a)!=='/'&&route.startsWith(path(a)+'/')).sort((a,b)=>path(b).length-path(a).length)[0];
    const section=current?.closest('.wiki-section')?.querySelector('.wiki-section-toggle')?.textContent||(route==='/'?'玩家手册':'资料库');
    links.forEach(a=>{if(a===current)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
    const label=main.querySelector('.wiki-section-name');if(label&&label.textContent!==section)label.textContent=section;
    const pager=main.querySelector('.wiki-pagination');if(!pager||pager.dataset.route===route&&pager.children.length)return;
    pager.replaceChildren();pager.dataset.route=route;if(route==='/'||index<0)return;
    [links[index-1],links[index+1]].forEach((item,i)=>{
      if(!item){pager.append(document.createElement('span'));return;}
      const a=document.createElement('a');a.href=item.getAttribute('href');const small=document.createElement('small');small.textContent=i===0?'← 上一篇':'下一篇 →';const strong=document.createElement('strong');strong.textContent=item.textContent;a.append(small,strong);pager.append(a);
    });
  }
  function setupSidebar(){
    const nav=document.querySelector('.sidebar-nav');if(!nav)return;
    nav.querySelectorAll(':scope > ul > li').forEach((li,index)=>{
      const home=li.querySelector(':scope > a, :scope > p > a');
      if(home&&path(home)==='/'&&!home.classList.contains('wiki-home-link')){
        home.classList.add('wiki-home-link');home.prepend(sidebarIcon('home'));
      }
      const list=li.querySelector(':scope > ul');if(!list||li.querySelector(':scope > .wiki-section-toggle'))return;
      const p=li.querySelector(':scope > p');const title=p?.textContent.trim()||Array.from(li.childNodes).filter(n=>n.nodeType===3).map(n=>n.textContent).join('').trim();if(!title)return;
      li.classList.add('wiki-section');const button=document.createElement('button');button.type='button';button.className='wiki-section-toggle';button.textContent=title;
      button.append(sidebarIcon('chevron'));list.id='wiki-nav-section-'+index;button.setAttribute('aria-controls',list.id);
      const containsCurrent=Array.from(list.querySelectorAll('a')).some(a=>path(a)===route||(path(a)!=='/'&&route.startsWith(path(a)+'/'))||a.parentElement.classList.contains('active')),open=containsCurrent||collapsed.get(title)===false;
      list.hidden=!open;button.setAttribute('aria-expanded',String(open));
      button.addEventListener('click',event=>{
        // Docsify closes the mobile drawer on body clicks; expanding a section stays inside it.
        event.stopPropagation();
        const expanded=button.getAttribute('aria-expanded')!=='true';button.setAttribute('aria-expanded',String(expanded));list.hidden=!expanded;collapsed.set(title,!expanded);
      });
      if(!p)Array.from(li.childNodes).filter(n=>n.nodeType===3).forEach(n=>n.textContent='');li.insertBefore(button,list);
    });
    updateNavigation();adoptSearch();
  }
  function watchSidebar(){
    const sidebar=document.querySelector('.sidebar');if(!sidebar||sidebar.dataset.modernObserved)return;
    sidebar.dataset.modernObserved='true';
    new MutationObserver(()=>{if(!sidebarFrame)sidebarFrame=requestAnimationFrame(()=>{sidebarFrame=0;setupSidebar();});}).observe(sidebar,{childList:true,subtree:true});setupSidebar();
  }
  function syncScroll(){topButton.hidden=scrollY<500;let current=headings[0];headings.forEach(h=>{if(h.getBoundingClientRect().top<=140)current=h;});document.querySelectorAll('.wiki-toc a').forEach(a=>a.setAttribute('aria-current',String(a.dataset.heading===current?.id)));}
  addEventListener('scroll',()=>{if(!scrollFrame)scrollFrame=requestAnimationFrame(()=>{scrollFrame=0;syncScroll();});},{passive:true});
  function mount(nextRoute){
    route=nextRoute;document.body.classList.toggle('home-page',route==='/');
    if(route==='/')document.title='TopCraft Wiki · 玩家资料库';
    const main=document.querySelector('.markdown-section'),h1=main?.querySelector('h1');if(!h1||h1.dataset.modernMounted){watchSidebar();return;}h1.dataset.modernMounted='true';
    const meta=document.createElement('div');meta.className='wiki-page-meta';meta.innerHTML='<a href="#/">Wiki</a><span aria-hidden="true">/</span><span class="wiki-section-name">资料库</span><button type="button">复制页面链接</button>';meta.querySelector('button').addEventListener('click',()=>copy(location.href));
    const crumb=main.querySelector('.wiki-breadcrumb,.eq-breadcrumb,.world-breadcrumb,.life-breadcrumb');
    if(crumb){crumb.classList.add('wiki-native-crumb');meta.querySelector('.wiki-section-name').replaceWith(crumb);}
    main.prepend(meta);
    headings=Array.from(main.querySelectorAll(':scope > h2[id], :scope > h3[id]'));document.body.classList.toggle('has-page-toc',headings.length>1&&route!=='/');const toc=document.querySelector('.wiki-toc');toc.replaceChildren();
    if(headings.length>1&&route!=='/'){
      const title=document.createElement('strong');title.textContent='本页目录';toc.append(title);const nav=document.createElement('nav');
      headings.forEach(h=>{const a=document.createElement('a');a.textContent=h.textContent;a.href='#'+route+'?id='+encodeURIComponent(h.id);a.dataset.heading=h.id;if(h.tagName==='H3')a.className='toc-sub';nav.append(a);});toc.append(nav);
      const outline=document.createElement('details');outline.className='wiki-outline';const summary=document.createElement('summary');summary.textContent='本页目录 · '+headings.filter(h=>h.tagName==='H2').length+' 个章节';outline.append(summary,nav.cloneNode(true));const lead=main.querySelector(':scope > .lead')||h1;lead.after(outline);outline.addEventListener('click',e=>{if(e.target.closest('a'))outline.open=false;});
    }
    const pager=document.createElement('nav');pager.className='wiki-pagination';pager.setAttribute('aria-label','章节导航');const end=main.querySelector('.page-end');if(end)end.before(pager);else main.append(pager);
    main.querySelectorAll('[data-copy-server]').forEach(b=>b.addEventListener('click',()=>copy('topcraft.cc')));
    watchSidebar();setupSidebar();
    const active=sidebarLinks().find(a=>a.getAttribute('aria-current')==='page');const group=active?.closest('.wiki-section');const groupButton=group?.querySelector('.wiki-section-toggle');if(groupButton?.getAttribute('aria-expanded')==='false')groupButton.click();
    syncDrawer();syncScroll();requestAnimationFrame(()=>{watchSidebar();adoptSearch();});
  }
  window.TopCraftModern={mount};
})();
