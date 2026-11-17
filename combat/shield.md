<nav class="wiki-breadcrumb" aria-label="当前位置"><span>战斗机制</span><span>›</span><a href="#/combat/defense">防御与恢复</a><span>›</span><span>护盾</span></nav>

# 护盾

<p class="lead">护盾在生命之前吸收伤害。破盾的这一次伤害不会继续扣除生命。</p>

<nav class="mechanics-tabs" aria-label="战斗机制"><a href="#/combat/attributes">角色属性</a><a href="#/combat/damage">伤害与暴击</a><a href="#/combat/defense" aria-current="page">防御与恢复</a><a href="#/combat/status-effects">状态与控制</a></nav>

<nav class="entry-nav" aria-label="本页条目"><a href="#/combat/shield?id=absorption">伤害吸收</a><a href="#/combat/shield?id=gain">护盾获得</a><a href="#/combat/shield?id=decay">自然衰减</a><a href="#/combat/shield?id=timed">定时与保留</a><a href="#/combat/shield?id=related">相关技能</a></nav>

## <img class="pixel-icon" src="assets/server/stats/dome.png" alt=""> 伤害吸收与破盾 :id=absorption

受击时只要还有护盾，就抵消本次伤害，并按 <strong>护甲与抗性减伤前的伤害</strong>扣除护盾。超出护盾的部分不会扣除生命。

例如剩余 <strong>1 点护盾</strong>时受到 <strong>100 点伤害</strong>：护盾耗尽，生命不减少。之后再次受伤时，才会由其他防御与生命承受。

举盾格挡先于护盾生效。未被格挡的伤害由护盾吸收；护盾已抵消的伤害不会再判定躲闪，也不累计躲闪失败次数。持续伤害同样会消耗护盾。

## 护盾获得加成 :id=gain

护盾获得量使用接收者的护盾获得加成。队友为你提供护盾时，也以你自身的该项属性计算。

<div class="formula">获得护盾 = 原始护盾量 ×（1 + 护盾获得加成 ÷ 100）</div>

例如技能提供 100 点护盾，接收者拥有 +20% 护盾获得，实际获得 <strong>120 点</strong>。

## 普通护盾的自然衰减 :id=decay

普通护盾除了受伤消耗，还会每秒自然衰减一次：

| 当前护盾 | 每次自然衰减 |
| --- | --- |
| 不超过 10 点 | 1 点 |
| 超过 10 点 | 约为当前护盾的 10%，按整数护盾计算 |

护盾越多，每秒自然损失也越多。持续获得护盾可以补充消耗；护盾保留效果可以改变衰减后的最低护盾。

## 定时护盾与护盾保留 :id=timed

定时护盾按照技能规定的时间持续。普通护盾与定时护盾同时存在时，先消耗普通护盾，再消耗定时护盾；本次破盾仍不产生额外生命伤害。

护盾保留限制的是自然衰减，不会免除受击消耗。保留数值、持续时间与获得条件见提供该效果的技能节点。

## 相关技能 :id=related

[魔切](combat/skills/mana-slash.md)、[飞锤](combat/skills/flying-hammer.md)、[跃击](combat/skills/leap.md)、[天赐圣剑](combat/skills/heavenly-sword.md)等技能可通过节点获得或改变护盾。

护盾、举盾和无敌的区别见[防御与恢复](combat/defense.md)与[增益状态](#/combat/status-effects?id=buffs)。

<div class="page-end">TopCraft 玩家手册 · 更新于 2026-11-14</div>
