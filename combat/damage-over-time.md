<nav class="wiki-breadcrumb" aria-label="当前位置"><span>战斗机制</span><span>›</span><a href="#/combat/damage">伤害与暴击</a><span>›</span><span>持续伤害</span></nav>

# 持续伤害

<p class="lead">点燃、冻伤、中毒、静电与流血持续造成伤害。伤害随层数增加，使用持续伤害属性加成。</p>

<nav class="mechanics-tabs" aria-label="战斗机制"><a href="#/combat/attributes">角色属性</a><a href="#/combat/damage" aria-current="page">伤害与暴击</a><a href="#/combat/defense">防御与恢复</a><a href="#/combat/status-effects">状态与控制</a></nav>

<nav class="entry-nav" aria-label="本页条目"><a href="#/combat/damage-over-time?id=ailments">五种持续伤害</a><a href="#/combat/damage-over-time?id=stacking">叠层与持续时间</a><a href="#/combat/damage-over-time?id=scaling">伤害加成</a><a href="#/combat/damage-over-time?id=interaction">防御与净化</a></nav>

## 五种持续伤害 :id=ailments

| 状态 | 伤害元素 | 每层每次基础伤害 | 技能标注时长 | 伤害间隔 |
| --- | --- | --- | --- | --- |
| <img class="pixel-icon" src="assets/server/abilities/ignite.png" alt=""> 点燃 | 火焰 | 10 | 3 秒 | 约 0.55 秒 |
| <img class="pixel-icon" src="assets/server/abilities/frostbite.png" alt=""> 冻伤 | 冰霜 | 10 | 3 秒 | 约 0.55 秒 |
| <img class="pixel-icon" src="assets/server/abilities/toxic_fumes.png" alt=""> 中毒 | 毒素 | 10 | 3 秒 | 约 0.55 秒 |
| <img class="pixel-icon" src="assets/server/abilities/static.png" alt=""> 静电 | 雷电 | 10 | 3 秒 | 0.5 秒 |
| <img class="pixel-icon" src="assets/server/abilities/bleed.png" alt=""> 流血 | 物理 | 10 | 3 秒 | 约 0.55 秒 |

技能可以改变状态的伤害、时长或施加层数，具体效果见对应技能树。

## 叠层与持续时间 :id=stacking

这五种状态没有玩法层数上限，每次伤害随当前层数增加。3 层状态每次造成的基础伤害为 `10 × 3 = 30`。

<strong>同一来源再次叠加时，不刷新剩余时间。</strong> 后加的层数随原状态一同结束。连续叠层提高当前伤害，但不会一直延长这次状态。

技能说明中的“3 秒内 60 点伤害”描述单层完整持续时的基础总伤害。点燃、冻伤、中毒和流血约每 0.55 秒伤害一次，静电每 0.5 秒一次；中途叠层或提前净化时，总伤害会随之改变。

## <img class="pixel-icon" src="assets/server/stats/dot_damage_bonus.png" alt=""> 持续伤害加成 :id=scaling

<div class="formula">每次持续伤害 = 每层基础伤害 × 当前层数<br>×［1 +（通用持续伤害加成 + 对应元素持续伤害加成）÷ 100］</div>

| 属性 | 对玩家施加的持续伤害 |
| --- | --- |
| 持续伤害加成 | 生效 |
| 对应元素持续伤害加成 | 生效 |
| 普通元素、全元素、法术、近战、远程等增伤 | 不生效 |
| 暴击率与暴击伤害 | 不生效，持续伤害不暴击 |
| 破甲、感电等直接伤害易伤 | 不生效 |

例如 3 层点燃，通用持续伤害 +20%、火焰持续伤害 +30%，每次伤害为 `10 × 3 × 1.5 = 45`，再计算目标的火焰抗性与其他适用减伤。

召唤物施加的持续伤害使用[召唤物伤害加成](combat/summons.md)。

## 防御与净化 :id=interaction

持续伤害会受到目标对应防御的减免：流血使用物理防御，其他四种使用对应元素抗性。持续伤害不会被躲闪或举盾格挡，但可被护盾抵消。

点燃、冻伤、中毒、静电、流血均可通过[净化](#/combat/status-effects?id=cleanse)解除。普通吸血和法术吸血不从持续伤害中恢复生命。

<div class="page-end">TopCraft 玩家手册 · 更新于 2026-11-14</div>
