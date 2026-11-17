<nav class="wiki-breadcrumb" aria-label="当前位置"><span>战斗机制</span><span>›</span><span>伤害与暴击</span></nav>

# 伤害与暴击

<p class="lead">从技能的元素和标签判断适用加成，查看直接伤害、暴击及特殊伤害的计算方式。</p>

<nav class="mechanics-tabs" aria-label="战斗机制"><a href="#/combat/attributes">角色属性</a><a href="#/combat/damage" aria-current="page">伤害与暴击</a><a href="#/combat/defense">防御与恢复</a><a href="#/combat/status-effects">状态与控制</a></nav>

<nav class="entry-nav" aria-label="本页条目"><a href="#/combat/damage?id=types">元素与标签</a><a href="#/combat/damage?id=hits">击中</a><a href="#/combat/damage?id=bonuses">伤害加成</a><a href="#/combat/damage?id=critical">暴击</a><a href="#/combat/damage?id=special">持续与召唤伤害</a></nav>

## 伤害元素与技能标签 :id=types

| 元素 | 对应固定与百分比词条 |
| --- | --- |
| <img class="pixel-icon" src="assets/server/stats/physical_damage.png" alt="物理"> 物理 | 物理伤害，不属于全元素 |
| <img class="pixel-icon" src="assets/server/stats/fire.png" alt="火焰"> 火焰 | 火焰伤害、全元素伤害 |
| <img class="pixel-icon" src="assets/server/stats/ice.png" alt="冰霜"> 冰霜 | 冰霜伤害、全元素伤害 |
| <img class="pixel-icon" src="assets/server/stats/thunder.png" alt="雷电"> 雷电 | 雷电／闪电伤害、全元素伤害 |
| <img class="pixel-icon" src="assets/server/stats/poison.png" alt="毒素"> 毒素 | 毒素伤害、全元素伤害 |

伤害同时具有元素和标签。例如飞锤是物理伤害，带远程、法术标签；魔切是雷电伤害，带近战、范围、法术标签。对应元素和标签的增伤可同时生效。位移、治疗表示技能功能，本身不提供伤害加成。

| 标签 | 适用属性或作用 |
| --- | --- |
| 近战 | 近战伤害加成；暴击伤害按近战规则选择 |
| 远程 | 远程伤害加成 |
| 法术 | 法术伤害加成、技能暴击率；符合条件时可法术吸血 |
| 范围 | 范围伤害加成 |
| 爆炸 | 爆炸伤害加成 |
| 击中 | 躲闪、举盾和击中触发效果的判定条件 |
| 治疗、位移 | 表示技能功能；伤害仍按各段攻击自身标签计算 |

寒冰箭主箭和陨石主撞击享受法术、爆炸增伤；闪电链享受法术增伤。这三种攻击不享受远程增伤。各段攻击的加成详见对应技能页。

<img class="pixel-icon" src="assets/server/stats/attack_damage.png" alt="武器伤害"> 职业技能以各自的基础伤害计算，武器面板伤害不会直接加到技能伤害上。

## 击中与直接伤害 :id=hits

“击中”用于判断躲闪、举盾和部分命中触发效果。技能是否属于击中，以技能说明为准；持续伤害不属于击中。

直接伤害表示一次攻击立即造成的伤害。伤害元素、攻击标签与“击中”分别描述攻击的不同性质。例如飞锤可以同时具有物理元素、远程与法术标签，并触发击中相关效果。

## <img class="pixel-icon" src="assets/server/stats/damage_increase.png" alt=""> 固定伤害与百分比加成 :id=bonuses

玩家直接伤害先加入适用的固定加成，再计算百分比加成、暴击与易伤。目标的护甲、抗性和减伤在之后生效。

<div class="formula">（技能本段伤害 + 对应元素固定加成 + 适用的全元素固定加成）<br>× 暴击倍率（未暴击为 1）<br>× 暴击元素专属倍率（仅本次暴击时）<br>× [1 + 各适用百分比加成之和 ÷ 100]<br>× 目标对应元素易伤倍率</div>

单元素、全元素、法术／近战／远程／范围／爆炸、伤害提高，以及对应怪物品阶增伤，属于同一组百分比加成，<strong>相加后计算</strong>。技能节点改变基础伤害或伤害系数时，先计算节点效果。

例：某段火焰远程法术基础伤害 100，火焰固定 +10，全元素固定 +5；火焰 +20%、全元素 +10%、法术 +30%、远程 +15%、伤害提高 +5%。未暴击、目标无易伤时：

`(100 + 10 + 5) × (1 + 0.20 + 0.10 + 0.30 + 0.15 + 0.05) = 207`

目标还会通过[防御属性](combat/defense.md)降低这部分伤害。物理伤害不会加入全元素固定值或全元素百分比。

普通、精英、领主、首领增伤分别作用于对应品阶的怪物。例如攻击精英时，仅精英增伤生效。

## <img class="pixel-icon" src="assets/server/stats/crit_chance.png" alt=""> 暴击率与暴击伤害 :id=critical

每次直接伤害判定一次暴击。暴击率为<strong>通用暴击率 + 技能额外暴击率</strong>；带法术标签的攻击再加上<strong>技能暴击率</strong>，最终范围为 0～100%。

| 伤害段 | 适用的暴击伤害 |
| --- | --- |
| 带近战标签 | 普通暴击伤害，再计技能额外倍率 |
| 没有近战、带法术标签 | 技能暴击伤害，再计技能额外倍率 |
| 其他直接伤害 | 普通暴击伤害，再计技能额外倍率 |

200% 暴击伤害使本次伤害变为 <strong>2 倍</strong>。元素暴击伤害加成单独相乘：例如 100 点基础伤害、200% 暴击伤害、10% 火焰暴击伤害加成，暴击后为 `100 × 2 × 1.1 = 220`，再计算其他增伤与目标防御。

## 持续伤害与召唤物 :id=special

持续伤害与召唤物使用各自的加成。点燃不会因为施加它的火球暴击而暴击；召唤物也不直接套用主人的法术伤害属性。

<div class="mechanic-cards"><a class="mechanic-card" href="#/combat/damage-over-time"><img class="pixel-icon" src="assets/server/stats/dot_damage_bonus.png" alt=""><strong>持续伤害</strong><span>点燃、冻伤、中毒、静电与流血；叠层和伤害间隔</span></a><a class="mechanic-card" href="#/combat/summons"><img class="pixel-icon" src="assets/server/stats/summon_damage_bonus.png" alt=""><strong>召唤物</strong><span>天神、圣眼与图腾的属性继承、伤害和治疗</span></a></div>

<div class="page-end">TopCraft 玩家手册 · 更新于 2026-11-14</div>
