<nav class="wiki-breadcrumb" aria-label="当前位置"><span>战斗机制</span><span>›</span><a href="#/combat/damage">伤害与暴击</a><span>›</span><span>召唤物</span></nav>

# 召唤物

<p class="lead">天神、圣眼与图腾独立攻击或治疗，使用召唤物专属属性。</p>

<nav class="mechanics-tabs" aria-label="战斗机制"><a href="#/combat/attributes">角色属性</a><a href="#/combat/damage" aria-current="page">伤害与暴击</a><a href="#/combat/defense">防御与恢复</a><a href="#/combat/status-effects">状态与控制</a></nav>

<nav class="entry-nav" aria-label="本页条目"><a href="#/combat/summons?id=types">召唤技能</a><a href="#/combat/summons?id=inheritance">属性继承</a><a href="#/combat/summons?id=damage">伤害</a><a href="#/combat/summons?id=healing">治疗</a><a href="#/combat/summons?id=control">控制与换装</a></nav>

## 召唤技能 :id=types

<div class="mechanic-cards"><a class="mechanic-card" href="#/combat/skills/divine-descent"><img class="pixel-icon" src="assets/server/priest_texture/skill_icon/divine_descent.png" alt=""><strong>天神降临</strong><span>召唤天神，节点改变形态与作战能力</span></a><a class="mechanic-card" href="#/combat/skills/watchful-eye"><img class="pixel-icon" src="assets/server/priest_texture/skill_icon/watchful_eye.png" alt=""><strong>守望之眼</strong><span>召唤圣眼，节点提供攻击、治疗与净化</span></a><a class="mechanic-card" href="#/combat/skills/totem"><img class="pixel-icon" src="assets/server/warrior_texture/skill_icon/totem.png" alt=""><strong>图腾</strong><span>召唤图腾，发射尖刺并附加节点效果</span></a></div>

## 属性继承 :id=inheritance

召唤物在召唤时获得主人的 <strong>召唤物生命、伤害、治疗、攻击速度和移动速度加成</strong>。技能等级与技能树决定该召唤物的基础数值和能力。

| 属性 | 作用 |
| --- | --- |
| 召唤物生命 | 提高召唤物生命 |
| 召唤物伤害 | 提高召唤物伤害，包括其施加的持续伤害 |
| 召唤物治疗 | 提高召唤物对友军的治疗 |
| 召唤物攻击速度 | 提高召唤物的攻击速度 |
| 召唤物移动速度 | 提高可移动召唤物的移动速度 |

## <img class="pixel-icon" src="assets/server/stats/summon_damage_bonus.png" alt=""> 召唤物伤害 :id=damage

<div class="formula">召唤物伤害 = 基础伤害 ×（1 + 召唤物伤害加成 ÷ 100）</div>

之后再计算目标的护甲、对应抗性及其他适用减伤。例如基础伤害 100、召唤物伤害 +40%，目标减伤前的伤害为 <strong>140</strong>。

主人的普通元素、全元素、法术、近战等增伤，以及暴击和吸血属性，不直接作用于召唤物。召唤物的具体攻击与节点倍率见对应技能树。

## <img class="pixel-icon" src="assets/server/stats/summon_healing_bonus.png" alt=""> 召唤物治疗 :id=healing

召唤物治疗享受主人的召唤物治疗加成；被治疗者再按自身的受到治疗加成提高恢复量。

<div class="formula">恢复量 = 基础治疗 ×（1 + 召唤物治疗加成 ÷ 100）<br>×（1 + 目标受到治疗加成 ÷ 100）</div>

基础治疗 100、召唤物治疗 +20%、目标受到治疗 +10% 时，恢复量为 <strong>132</strong>。治疗降低等状态会继续影响实际恢复，恢复量不超过目标已损失的生命。

## 更换装备与控制状态 :id=control

已经存在的召唤物沿用召唤时的属性。更换装备或调整加点后，新的召唤物使用新的属性与加点。

主人被眩晕、冻结或沉默时，已经召唤的天神与圣眼仍可继续行动。现有召唤物也可通过[净罪之光](#/combat/skills/divine-descent?node=净罪之光&id=技能树)、[净愈之瞳](#/combat/skills/watchful-eye?node=净愈之瞳&id=技能树)净化友军。

<div class="page-end">TopCraft 玩家手册 · 更新于 2026-11-14</div>
