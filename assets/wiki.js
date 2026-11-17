document.querySelector('.skip-link').addEventListener('click', function (event) {
  event.preventDefault(); event.stopPropagation();
  const main = document.querySelector('#main');
  if (main) { main.focus(); main.scrollIntoView(); }
}, true);
document.addEventListener('click', function (event) {
  if (window.innerWidth <= 768 && event.target.closest('.sidebar a[href]')) {
    document.body.classList.remove('close');
  }
}, true);
window.$docsify = {
  name: '<span class="brand-mark">T</span><span>TopCraft<small>玩家手册 / WIKI</small></span>',
  nameLink: '#/', homepage: 'README.md', loadSidebar: true, loadNavbar: true,
  coverpage: false, subMaxLevel: 0, auto2top: true, relativePath: false, topMargin: 88,
  alias: { '/.*/_sidebar.md': '/_sidebar.md', '/.*/_navbar.md': '/_navbar.md' },
  notFoundPage: '_404.md',
  search: { paths: window.TopCraftSearchPaths || 'auto', placeholder: '搜索技能、材料、玩法…', noData: '暂时没有找到，试试职业名或物品名。', depth: 3, namespace: 'topcraft-wiki-ui-entrypoints-v22', maxAge: 86400000 },
  plugins: [function (hook, vm) {
    hook.doneEach(function () {
      const main = document.querySelector('.markdown-section');
      document.body.classList.toggle('combat-page', /^\/combat\/(warrior|mage|priest|skills)(\/|$)/.test(vm.route.path));
      document.body.classList.toggle('mechanics-page', /^\/combat\/(attributes|damage|defense|status-effects|damage-over-time|summons|shield)$/.test(vm.route.path));
      document.body.classList.toggle('equipment-page', /^\/equipment\//.test(vm.route.path));
      document.body.classList.toggle('world-page', /^\/world\//.test(vm.route.path));
      document.body.classList.toggle('life-page', /^\/life\//.test(vm.route.path));
      document.body.classList.toggle('social-page', /^\/social\//.test(vm.route.path));
      document.body.classList.toggle('guide-page', /^\/guide\//.test(vm.route.path));
      document.body.classList.toggle('help-page', /^\/guide\/(help|commands|troubleshooting|feedback)$/.test(vm.route.path));
      document.body.classList.toggle('dungeon-page', /^\/dungeons\//.test(vm.route.path));
      if (main) { main.id = 'main'; main.setAttribute('tabindex', '-1'); }
      const title = main?.querySelector('h1')?.textContent;
      if (title) document.title = title + ' · TopCraft 玩家手册';
      const toggle = document.querySelector('.sidebar-toggle');
      if (toggle) toggle.setAttribute('aria-label', '展开或收起目录');
      document.querySelector('.search input')?.setAttribute('aria-label', '搜索 Wiki');
      window.TopCraftCombat?.mount();
      window.TopCraftEquipment?.mount();
      window.TopCraftWorld?.mount();
      window.TopCraftLife?.mount();
      window.TopCraftSocial?.mount();
      window.TopCraftGuide?.mount();
      window.TopCraftDungeons?.mount();
      window.TopCraftHelp?.mount();
      window.TopCraftModern?.mount(vm.route.path);
      window.TopCraftNumbers?.mount(main);
    });
  }]
};
