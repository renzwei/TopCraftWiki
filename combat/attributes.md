<nav class="wiki-breadcrumb" aria-label="当前位置"><span>战斗机制</span><span>›</span><span>角色属性</span></nav>

# 角色属性

<p class="lead">查看属性的作用、加点收益，以及攻击速度、冷却与法力之间的关系。</p>

<nav class="mechanics-tabs" aria-label="战斗机制"><a href="#/combat/attributes" aria-current="page">角色属性</a><a href="#/combat/damage">伤害与暴击</a><a href="#/combat/defense">防御与恢复</a><a href="#/combat/status-effects">状态与控制</a></nav>

<nav class="entry-nav" aria-label="本页条目"><a href="#/combat/attributes?id=talents">天赋加点</a><a href="#/combat/attributes?id=life">生命</a><a href="#/combat/attributes?id=mana">法力与回蓝</a><a href="#/combat/attributes?id=speed">攻击速度</a><a href="#/combat/attributes?id=cooldown">冷却缩减</a><a href="#/combat/attributes?id=cost">法力消耗</a><a href="#/combat/attributes?id=movement">移动速度</a></nav>

<div class="mechanic-cards"><a class="mechanic-card" href="#/combat/damage"><img class="pixel-icon" src="assets/server/stats/damage_increase.png" alt=""><strong>伤害与暴击</strong><span>伤害加成、元素、标签与暴击</span></a><a class="mechanic-card" href="#/combat/defense"><img class="pixel-icon" src="assets/server/stats/defense.png" alt=""><strong>防御与恢复</strong><span>护甲、抗性、护盾与治疗</span></a></div>

## 天赋与属性点 :id=talents

点击<strong>背包 → 打开技能 → 天赋属性</strong>，查看可用属性点并分配天赋。要查看加点和装备后的战斗属性，返回背包，点击<strong>个人信息</strong>打开角色详情。

每个职业共有 <strong>30 点属性点</strong>，1 级获得 1 点，此后每级获得 1 点。单项天赋最多投入 <strong>20 点</strong>。重置全部天赋消耗 1 个属性重置点。

| 天赋 | 每点效果 | 20 点效果 |
| --- | --- | --- |
| 力量 | 伤害提高 +1%；持续伤害 +1% | 各 +20% |
| 敏捷 | 攻速 +0.75%；通用暴击率 +0.2 个百分点；移速 +0.1% | 攻速 +15%；暴击率 +4 个百分点；移速 +2% |
| 体质 | 最大生命 +1.5%；受到治疗 +0.5% | 最大生命 +30%；受到治疗 +10% |
| 精神 | 最大法力 +1%；每秒法力恢复 +0.04 | 最大法力 +20%；每秒回蓝 +0.8 |
| 专注 | 冷却缩减 +0.3%；法力消耗降低 +0.25% | 冷却缩减 +6%；法力消耗降低 +5% |

暴击率按百分点相加：原有 5% 暴击率，投入 20 点敏捷后变为 9%。力量分别提高直接伤害与持续伤害；两项加成用于各自对应的伤害类型。

属性点、技能点和技能树点数分别使用，获取与重置方式见[升级与技能加点](combat/progression.md)。

## <img class="pixel-icon" src="assets/server/stats/health.png" alt=""> 生命与生命恢复 :id=life

最大生命决定角色能够承受多少伤害；生命恢复表示每秒自然恢复的生命。体质提高最大生命与受到治疗，恢复效果的计算见[治疗与吸血](#/combat/defense?id=healing)。

各职业初始生命、法力和每级成长见[战士](combat/warrior.md)、[法师](combat/mage.md)、[牧师](combat/priest.md)。

## <img class="pixel-icon" src="assets/server/stats/mana.png" alt=""> 法力与法力恢复 :id=mana

法力用于施放技能。最大法力提高可连续施放技能的次数，法力恢复提高持续作战时的回蓝速度。战斗中仍会自然恢复法力。

三种职业的基础回蓝均为 <strong>每秒 2 点</strong>。投入 20 点精神后，增加 0.8 点，变为 <strong>每秒 2.8 点</strong>。

最大法力的百分比加成提高法力上限。例如 30 级战士基础法力为 158，20 点精神提供 +20%，得到 `158 × 1.2 = 189.6` 点法力。

## <img class="pixel-icon" src="assets/server/stats/attack_speed.png" alt=""> 攻击速度 :id=speed

攻击速度影响横扫、裂震斩、火球术、魔切、神辉斩和圣光弹的施放频率。同职业的两种基础攻击共用攻击间隔，交替使用也受这个间隔限制。

<div class="formula">平均攻击间隔 = 1 秒 ÷（1 + 攻速加成 ÷ 100）</div>

| 攻速加成 | 平均攻击间隔 | 每秒施放次数 |
| --- | --- | --- |
| 0% | 1 秒 | 1 次 |
| 50% | 约 0.67 秒 | 1.5 次 |
| 100% | 0.5 秒 | 2 次 |

游戏按 0.05 秒更新攻击间隔，相邻两次施放的间隔可能略有差异。上述技能即使显示 0 秒冷却，也需要等待攻击间隔结束。

## <img class="pixel-icon" src="assets/server/stats/ability_haste.png" alt=""> 冷却缩减 :id=cooldown

冷却缩减减少技能施放后的等待时间。攻击速度缩短基础攻击间隔，冷却缩减作用于技能冷却，两者分别计算。

<div class="formula">技能冷却 = 基础冷却 ×（1 − 冷却缩减 ÷ 100）</div>

20 点专注提供 6% 冷却缩减，10 秒冷却缩短至 <strong>9.4 秒</strong>。闪现回溯等特殊冷却规则见对应[技能详情](combat/skills.md)。举盾后的冷却使用盾牌自身的[盾牌冷却缩减](#/combat/defense?id=block)。

## <img class="pixel-icon" src="assets/server/stats/mana.png" alt=""> 法力消耗降低 :id=cost

法力消耗降低按百分比减少每次施法消耗，有效范围为 <strong>0～100%</strong>。技能树改变的消耗先计入技能，再计算此属性。

<div class="formula">实际消耗 = 技能消耗 ×（1 − 法力消耗降低 ÷ 100）</div>

魔切消耗 6 点法力，20 点专注提供 5% 减耗，实际消耗为 <strong>5.7 点</strong>。圣翼巡礼消耗 30 点，在相同减耗下消耗 <strong>28.5 点</strong>。

## <img class="pixel-icon" src="assets/server/stats/movement_speed.png" alt=""> 移动速度 :id=movement

移动速度提高角色行走时的速度。敏捷每点提供 0.1% 移速；狂怒等增益也能提供移速加成。传送距离、跃击距离和冲锋行为由各技能决定。

限制移动的效果见[状态与控制](#/combat/status-effects?id=control)。

<div class="page-end">TopCraft 玩家手册 · 更新于 2026-11-17</div>
