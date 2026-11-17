(() => {
  'use strict';
  const inventory={
    info:['个人信息','悬停查看角色资料；点击打开角色详情，查看当前职业、金币和战斗属性。生活职业等级可从主菜单的“生活技能”查看。','角色属性','combat/attributes'],
    bag:['额外背包','点击打开随身储物空间。这里用来存放物品，放入的装备不会因此穿戴到身上。','武器与穿戴','equipment/slots'],
    skills:['打开技能','选择职业技能后，左键点击下方技能槽绑定，右键槽位解绑。界面左下角可打开“天赋属性”，右下角可打开“技能树”。','第一次绑定技能','guide/start?id=绑定第一个技能'],
    class:['职业选择','查看战士、法师、牧师，点击职业下方的选择按钮进入确认页，再点击“确认选择”。','职业选择步骤','guide/start?id=选择职业'],
    menu:['主菜单','点击任务手册、生活委托、生活技能、组队大厅、职业流派或服务器公告，进入对应功能。','主菜单六个按钮','guide/interface?id=主菜单六个按钮']
  };
  const menus={
    quests:['任务手册','查看任务目标、计数和冒险记录。任务需先与对应 NPC 对话接取。','任务与任务手册','quests/overview'],
    commissions:['生活委托','打开每日生活委托，再从界面切换每日与每周任务。查看本期目标、计数和奖励。','每日与每周生活委托','life/commissions'],
    professions:['生活技能','查看八项生活职业及各自的等级、经验。悬停职业图标查看具体资料。','生活职业总览','life/overview'],
    party:['组队大厅','点击队伍头像加入招募中的队伍，或点击下方“我的队伍”创建和管理队伍。大厅可在主城和落日森林打开。','组队与招募','social/party'],
    builds:['职业流派','点击“新建 Build”保存当前方案，或选择已有方案进行查看和切换。','加点方案与预设','combat/builds'],
    announcements:['服务器公告','点击查看服务器公告与通知。','帮助与常见问题','guide/help']
  };
  const states={
    ready:['可以施放','图标下方出现就绪标记。按绑定的键位施放；施放后可能进入冷却或攻击间隔。'],
    cooldown:['冷却中','图标覆盖冷却遮罩并显示剩余时间。示例中的 3.2 表示还需等待约 3.2 秒。'],
    mana:['法力不足','图标变暗，并显示法力警示。恢复足够法力后才能施放。'],
    empty:['尚未绑定','槽位没有技能图标。打开技能界面，选中技能，再左键点击下方槽位。']
  };
  function setDetail(root,entry){
    const box=root.querySelector('.guide-detail');
    box.replaceChildren();
    const title=document.createElement('strong'),p=document.createElement('p');title.textContent=entry[0];p.textContent=entry[1];box.append(title,p);
    if(entry[2]){const a=document.createElement('a');a.href='#/'+entry[3];a.textContent=entry[2]+' →';box.append(a);}
  }
  window.TopCraftGuide={mount(){
    document.querySelectorAll('[data-guide-demo]:not([data-ready])').forEach(root=>{
      root.dataset.ready='true';
      const type=root.dataset.guideDemo,items=type==='inventory'?inventory:type==='menu'?menus:states;
      const buttons=[...root.querySelectorAll('button[data-info]')];
      const select=button=>{
        const id=button.dataset.info;if(!items[id])return;
        buttons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));setDetail(root,items[id]);
        if(type==='hud')root.querySelectorAll('[data-show]').forEach(el=>{el.hidden=!el.dataset.show.split(' ').includes(id);});
      };
      buttons.forEach(button=>button.addEventListener('click',()=>select(button)));
      if(buttons.length)select(buttons[0]);
    });
  }};
})();
