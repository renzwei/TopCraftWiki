(function () {
  'use strict';
  const fields = {
    connection: ['连接时的完整提示：', '无法连接／下载失败／加载失败：', '发生在加载资源包前还是之后：'],
    display: ['异常物品、图标或界面名称：', '其他资源包与客户端模组：', '停用相关资源包后的结果：'],
    combat: ['职业与等级：', '技能名称、等级与技能槽：', '施放时的法力、冷却与状态：'],
    item: ['物品完整名称与品质：', '操作前后的数量、耐久或强化等级：', '交易对象或制作配方（如适用）：'],
    quest: ['任务／生活委托／礼包名称：', '当前任务阶段与目标：', '完成时间与领取时的提示：'],
    dungeon: ['地图、赛季与挑战层数：', '队长与队员名称：', '钥匙持有者及使用前后层数：', '所处阶段（入场／备战／挑战／结算）：', '是否死亡、断线或离开：'],
    other: ['相关玩法或页面：']
  };
  function template(type) {
    return ['问题概述：', '游戏角色名：', '发生时间（日期、时分、时区）：', '所在世界／地点：', '客户端版本：', '', ...fields[type], '', '操作步骤：', '1. ', '2. ', '3. ', '', '预期结果：', '实际结果与完整提示：', '是否每次都发生：', '已尝试的方法与结果：', '截图或视频说明：'].join('\n');
  }
  async function copy(text, button, status) {
    try {
      await navigator.clipboard.writeText(text);
      status.textContent = '已复制。';
    } catch (_) {
      status.textContent = '未能自动复制，请选中文字后按 Ctrl+C（Mac 使用 ⌘C）。';
      const field = button.closest('[data-feedback]')?.querySelector('textarea');
      if (field) { field.focus(); field.select(); }
    }
  }
  function revealAnchor(root) {
    const query = location.hash.split('?')[1] || '';
    const id = new URLSearchParams(query).get('id');
    if (!id) return;
    const target = root.querySelectorAll('[id]');
    const normalize = value => value.toLocaleLowerCase().replace(/\s+/g, '-');
    const match = Array.from(target).find(node => normalize(node.id) === normalize(id));
    const detail = match?.closest('details');
    if (detail) {
      root.querySelector('[data-help-reset]')?.click();
      detail.open = true;
      requestAnimationFrame(() => detail.scrollIntoView({block:'start', behavior:'instant'}));
    }
  }
  function mount() {
    const root = document.querySelector('.help-page .markdown-section');
    const heading = root?.querySelector('h1');
    if (!heading || heading.dataset.helpMounted) return;
    heading.dataset.helpMounted = 'true';
    const search = root.querySelector('[data-help-search]');
    if (search) {
      const entries = Array.from(root.querySelectorAll('[data-help-entry]'));
      const categories = Array.from(root.querySelectorAll('[data-help-category]'));
      const count = root.querySelector('[data-help-count]');
      let category = '全部';
      const filter = () => {
        const words = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
        let visible = 0;
        entries.forEach(entry => {
          const haystack = (entry.textContent + ' ' + (entry.dataset.keywords || '')).toLocaleLowerCase();
          entry.hidden = !(category === '全部' || category === entry.dataset.category) || !words.every(word => haystack.includes(word));
          if (!entry.hidden) visible++;
        });
        count.textContent = visible ? `找到 ${visible} 项，共 ${entries.length} 项` : '没有找到。试试更短的关键词，或清除筛选；仍有疑问可查看“问题反馈”。';
      };
      search.addEventListener('input', filter);
      categories.forEach(button => button.addEventListener('click', () => {
        category = button.dataset.helpCategory;
        categories.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
        filter();
      }));
      root.querySelector('[data-help-reset]').addEventListener('click', () => {
        search.value = ''; category = '全部';
        categories.forEach(item => item.setAttribute('aria-pressed', String(item.dataset.helpCategory === category)));
        filter();
      });
      filter();
    }
    root.querySelectorAll('[data-copy-command]').forEach(button => button.addEventListener('click', () => {
      copy(button.dataset.copyCommand, button, button.closest('.help-command').querySelector('[role=status]'));
    }));
    const feedback = root.querySelector('[data-feedback]');
    if (feedback) {
      const select = feedback.querySelector('select');
      const field = feedback.querySelector('textarea');
      const status = feedback.querySelector('[role=status]');
      field.value = template(select.value);
      // The template is read-only so changing categories never discards a player's report.
      select.addEventListener('change', () => { field.value = template(select.value); status.textContent = ''; });
      feedback.querySelector('button').addEventListener('click', event => copy(field.value, event.currentTarget, status));
    }
    revealAnchor(root);
  }
  window.addEventListener('hashchange', () => {
    const root = document.querySelector('.help-page .markdown-section');
    if (root) revealAnchor(root);
  });
  window.TopCraftHelp = {mount};
})();
