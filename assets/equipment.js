(function (root) {
  'use strict';
  const numbers = root.TopCraftNumbers || require('./numbers.js');
  const fmt = numbers.value;
  const escape = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  function range(stat, level) {
    const center = Number(stat.base || 0) + Number(stat.scale || 0) * level;
    const spread = Number(stat['max-spread'] || 0);
    return { center, min: center * (1 - spread), max: center * (1 + spread) };
  }
  const upgrade = (value, level) => value * Math.pow(1.05, level);
  let pending;
  function getData() {
    if (!pending) pending = fetch('assets/data/equipment.json').then(r => {
      if (!r.ok) throw new Error('equipment data unavailable');
      return r.json();
    }).catch(e => { pending = null; throw e; });
    return pending;
  }
  const value = (s, level, unit) => {
    const r = range(s, level);
    return (r.min === r.max ? fmt(r.center) : fmt(r.min) + '–' + fmt(r.max)) + (unit || '');
  };
  function validLevel(input) { return input.validity.valid && Number.isSafeInteger(input.valueAsNumber) && input.valueAsNumber >= 1; }
  function statName(data, key) {
    const label = (data.icons?.[key] ? '<img class="eq-stat-icon" src="' + escape(data.icons[key]) + '" alt="">' : '') + escape(data.labels[key]);
    return data.links?.[key] ? '<a href="' + escape(data.links[key]) + '">' + label + '</a>' : label;
  }
  function mount() {
    const main = document.querySelector('#main');
    if (!main) return;
    main.querySelectorAll('[data-eq-filter]').forEach(input => {
      if (input.dataset.ready) return;
      input.dataset.ready = 'true';
      const cards = [...main.querySelectorAll('[data-eq-search]')];
      const status = main.querySelector('.eq-filter-status');
      function filter() {
        const query = input.value.trim().toLocaleLowerCase();
        let visible = 0;
        cards.forEach(card => { card.hidden = !card.dataset.eqSearch.toLocaleLowerCase().includes(query); if (!card.hidden) visible++; });
        main.querySelectorAll('.eq-category').forEach(section => { section.hidden = !section.querySelector('.eq-item:not([hidden])'); });
        status.textContent = query ? (visible ? '找到 ' + visible + ' 项' : '没有找到匹配条目，请换一个名称。') : '共 ' + cards.length + ' 项';
      }
      input.addEventListener('input', filter); filter();
    });
    main.querySelectorAll('.eq-upgrade').forEach(panel => {
      if (panel.dataset.ready) return;
      panel.dataset.ready = 'true';
      const [amount, level] = panel.querySelectorAll('input'), output = panel.querySelector('output');
      function update() {
        output.textContent = amount.validity.valid && level.validity.valid && amount.value !== '' && level.value !== '' && Number.isFinite(upgrade(Number(amount.value), Number(level.value)))
          ? '强化后：' + fmt(upgrade(Number(amount.value), Number(level.value)))
          : '请输入有效数值（强化等级 0–15）。';
      }
      panel.addEventListener('input', update); update();
    });
    const panels = [...main.querySelectorAll('.eq-growth, .eq-affixes')].filter(p => !p.dataset.ready);
    if (!panels.length) return;
    panels.forEach(p => { p.dataset.ready = 'true'; });
    getData().then(data => {
      panels.forEach(panel => {
        if (!panel.isConnected) return;
        const input = panel.querySelector('input'), select = panel.querySelector('select');
        const output = panel.querySelector('.eq-growth-result, .eq-affix-result');
        function update() {
          if (!validLevel(input)) { output.textContent = '请输入大于或等于 1 的整数等级。'; return; }
          const level = input.valueAsNumber;
          if (select) {
            const pool = data.affixes[select.value];
            output.innerHTML = '<p>' + escape(select.value) + '装备 · 随机附加 ' + pool.min + '–' + pool.max + ' 项</p><div class="eq-table-scroll"><table><thead><tr><th>词条</th><th>分级</th><th>' + level + ' 级范围</th></tr></thead><tbody>' +
              Object.entries(pool.stats).map(([key, s]) => '<tr><td>' + statName(data, key) + '</td><td>' + escape(s.rank) + '</td><td>' + value(s.growth, level, data.units[key]) + '</td></tr>').join('') + '</tbody></table></div>';
          } else {
            const type = data.types[panel.dataset.eqType];
            output.innerHTML = '<p><b>' + level + ' 级' + escape(type.name) + '</b> · 基础属性候选范围</p><dl class="eq-stats">' +
              Object.entries(type.stats).map(([key, s]) => '<div><dt>' + statName(data, key) + (type.guaranteed.includes(key) ? ' · 必有' : '') + '</dt><dd>' + value(s, level, data.units[key]) + '</dd></div>').join('') + '</dl>' +
              (type.durability ? '<p>最大耐久：' + value(type.durability, level, '') + '</p>' : '');
          }
        }
        input.addEventListener('input', update); select?.addEventListener('change', update); update();
      });
    }).catch(() => panels.forEach(p => {
      if (p.isConnected) p.querySelector('.eq-growth-result, .eq-affix-result').textContent = '数值查询暂未加载，可查看下方成长表，或刷新页面重试。';
      delete p.dataset.ready;
    }));
  }
  const api = { range, upgrade, fmt, mount };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.TopCraftEquipment = api;
})(typeof window !== 'undefined' ? window : globalThis);
