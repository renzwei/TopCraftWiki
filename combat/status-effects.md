<nav class="wiki-breadcrumb" aria-label="当前位置"><span>战斗机制</span><span>›</span><span>状态与控制</span></nav>

# 状态与控制

<p class="lead">通过图标查找增益、减益与控制效果，了解持续时间、叠层、净化及首领破韧。</p>

<nav class="mechanics-tabs" aria-label="战斗机制"><a href="#/combat/attributes">角色属性</a><a href="#/combat/damage">伤害与暴击</a><a href="#/combat/defense">防御与恢复</a><a href="#/combat/status-effects" aria-current="page">状态与控制</a></nav>

<nav class="entry-nav" aria-label="本页条目"><a href="#/combat/status-effects?id=dot">持续伤害</a><a href="#/combat/status-effects?id=debuffs">减益状态</a><a href="#/combat/status-effects?id=control">行动控制</a><a href="#/combat/status-effects?id=buffs">增益状态</a><a href="#/combat/status-effects?id=tenacity">韧性与免控</a><a href="#/combat/status-effects?id=boss">首领破韧</a><a href="#/combat/status-effects?id=cleanse">净化</a></nav>

## 持续伤害状态 :id=dot

<div class="status-grid"><article class="status-card" id="ignite"><div class="status-heading"><img class="status-icon" src="assets/server/buffs/ignite.png" alt=""><h3>点燃</h3></div><p>持续造成火焰伤害；每层每次基础伤害 <strong>10</strong>。</p><dl><div><dt>标注时长</dt><dd>3 秒</dd></div><div><dt>伤害间隔</dt><dd>约 0.55 秒</dd></div><div><dt>层数</dt><dd>无玩法上限</dd></div><div><dt>叠加刷新</dt><dd>不刷新</dd></div><div><dt>净化</dt><dd>可以</dd></div></dl><p class="status-related"><a href="#/combat/damage-over-time">伤害加成与叠层规则 →</a></p></article><article class="status-card" id="frostbite"><div class="status-heading"><img class="status-icon" src="assets/server/buffs/frostbite.png" alt=""><h3>冻伤</h3></div><p>持续造成冰霜伤害；每层每次基础伤害 <strong>10</strong>。</p><dl><div><dt>标注时长</dt><dd>3 秒</dd></div><div><dt>伤害间隔</dt><dd>约 0.55 秒</dd></div><div><dt>层数</dt><dd>无玩法上限</dd></div><div><dt>叠加刷新</dt><dd>不刷新</dd></div><div><dt>净化</dt><dd>可以</dd></div></dl><p class="status-related"><a href="#/combat/damage-over-time">伤害加成与叠层规则 →</a></p></article><article class="status-card" id="poison"><div class="status-heading"><img class="pixel-icon" src="assets/server/stats/dome.png" alt=""><h3>中毒</h3></div><p>持续造成毒素伤害；每层每次基础伤害 <strong>10</strong>。</p><dl><div><dt>标注时长</dt><dd>3 秒</dd></div><div><dt>伤害间隔</dt><dd>约 0.55 秒</dd></div><div><dt>层数</dt><dd>无玩法上限</dd></div><div><dt>叠加刷新</dt><dd>不刷新</dd></div><div><dt>净化</dt><dd>可以</dd></div></dl><p class="status-related"><a href="#/combat/damage-over-time">伤害加成与叠层规则 →</a></p></article><article class="status-card" id="static"><div class="status-heading"><img class="status-icon" src="assets/server/buffs/static.png" alt=""><h3>静电</h3></div><p>持续造成雷电伤害；每层每次基础伤害 <strong>10</strong>。</p><dl><div><dt>标注时长</dt><dd>3 秒</dd></div><div><dt>伤害间隔</dt><dd>0.5 秒</dd></div><div><dt>层数</dt><dd>无玩法上限</dd></div><div><dt>叠加刷新</dt><dd>不刷新</dd></div><div><dt>净化</dt><dd>可以</dd></div></dl><p class="status-related"><a href="#/combat/damage-over-time">伤害加成与叠层规则 →</a></p></article><article class="status-card" id="bleed"><div class="status-heading"><img class="status-icon" src="assets/server/buffs/bleed.png" alt=""><h3>流血</h3></div><p>持续造成物理伤害；每层每次基础伤害 <strong>10</strong>。</p><dl><div><dt>标注时长</dt><dd>3 秒</dd></div><div><dt>伤害间隔</dt><dd>约 0.55 秒</dd></div><div><dt>层数</dt><dd>无玩法上限</dd></div><div><dt>叠加刷新</dt><dd>不刷新</dd></div><div><dt>净化</dt><dd>可以</dd></div></dl><p class="status-related"><a href="#/combat/damage-over-time">伤害加成与叠层规则 →</a></p></article></div>

同一来源后加的层数随原状态一同结束；技能可改变时长或层数。完整计算与防御规则见[持续伤害](combat/damage-over-time.md)。

## 减益状态 :id=debuffs

<div class="status-grid"><article class="status-card" id="armor-break"><div class="status-heading"><img class="status-icon" src="assets/server/buffs/armor_break.png" alt=""><h3>破甲</h3></div><p>每层使目标受到的<strong>物理直接伤害提高 5%</strong>，10 层时为 1.5 倍。不提高流血伤害。</p><dl><div><dt>默认时长</dt><dd>4 秒</dd></div><div><dt>层数上限</dt><dd>10 层</dd></div><div><dt>叠加刷新</dt><dd>刷新</dd></div><div><dt>净化</dt><dd>可以</dd></div></dl><p class="status-related"><a href="#/combat/damage?id=bonuses">易伤与伤害加成 →</a></p></article><article class="status-card" id="shock"><div class="status-heading"><img class="status-icon" src="assets/server/buffs/electrified.png" alt=""><h3>感电</h3></div><p>每层使目标受到的<strong>雷电直接伤害提高 5%</strong>，10 层时为 1.5 倍。不提高静电伤害。</p><dl><div><dt>默认时长</dt><dd>4 秒</dd></div><div><dt>层数上限</dt><dd>10 层</dd></div><div><dt>叠加刷新</dt><dd>刷新</dd></div><div><dt>净化</dt><dd>可以</dd></div></dl><p class="status-related"><a href="#/combat/skills/chain-lightning">闪电链 →</a></p></article><article class="status-card" id="slow"><div class="status-heading"><img class="status-icon" src="assets/server/buffs/slow.png" alt=""><h3>迟缓</h3></div><p>可触发对迟缓目标生效的技能效果。游戏内说明标注移动速度降低 <strong>8%</strong>；实际减速幅度尚待确认。</p><dl><div><dt>默认时长</dt><dd>4 秒，受韧性影响</dd></div><div><dt>层数上限</dt><dd>10 层</dd></div><div><dt>叠加刷新</dt><dd>刷新</dd></div><div><dt>净化</dt><dd>可以</dd></div></dl><p class="status-related"><a href="#/combat/skills">相关技能与节点 →</a></p></article><article class="status-card" id="chill"><div class="status-heading"><img class="status-icon" src="assets/server/buffs/ice_slow.png" alt=""><h3>冰缓</h3></div><p>可触发对冰缓目标生效的技能效果。游戏内说明标注移动速度降低 <strong>8%</strong>；实际减速幅度尚待确认。</p><dl><div><dt>默认时长</dt><dd>4 秒，受韧性影响</dd></div><div><dt>层数上限</dt><dd>10 层</dd></div><div><dt>叠加刷新</dt><dd>刷新</dd></div><div><dt>净化</dt><dd>可以</dd></div></dl><p class="status-related"><a href="#/combat/skills">相关技能与节点 →</a></p></article><article class="status-card" id="blind"><div class="status-heading"><img class="status-icon" src="assets/server/buffs/blind.png" alt=""><h3>致盲</h3></div><p>使目标的普通攻击失效。</p><dl><div><dt>默认时长</dt><dd>4 秒，受韧性影响</dd></div><div><dt>层数上限</dt><dd>1 层</dd></div><div><dt>再次施加</dt><dd>刷新时间</dd></div><div><dt>净化</dt><dd>可以</dd></div></dl></article><article class="status-card" id="slow-curse"><div class="status-heading"><img class="pixel-icon" src="assets/server/abilities/cobra_curse.png" alt=""><h3>缓慢诅咒</h3></div><p>按当前层数提高缓慢药水等级，限制目标移动。</p><dl><div><dt>默认时长</dt><dd>约 3.55 秒，受韧性影响</dd></div><div><dt>层数上限</dt><dd>100 层</dd></div><div><dt>叠加刷新</dt><dd>不刷新</dd></div><div><dt>净化</dt><dd>可以</dd></div></dl></article><article class="status-card" id="healing-reduction"><div class="status-heading"><img class="status-icon" src="assets/server/buffs/healing_suppression.png" alt=""><h3>治疗降低</h3></div><p>减少目标受到的治疗。默认降低 <strong>20%</strong>；不同技能可提供不同幅度与持续时间。</p><dl><div><dt>默认时长</dt><dd>4 秒</dd></div><div><dt>层数上限</dt><dd>1 层</dd></div><div><dt>再次施加</dt><dd>替换原效果</dd></div><div><dt>净化</dt><dd>可以</dd></div></dl><p class="status-related"><a href="#/combat/defense?id=healing">治疗计算 →</a></p></article><article class="status-card" id="spark"><div class="status-heading"><img class="status-icon" src="assets/server/buffs/spark_charge.png" alt=""><h3>火花电荷</h3></div><p>持续时间结束或再次施加时引爆，造成范围雷电伤害。爆炸伤害由施加它的技能决定。</p><dl><div><dt>持续时间</dt><dd>2 秒</dd></div><div><dt>再次施加</dt><dd>触发引爆</dd></div><div><dt>净化</dt><dd>可以，但解除也会触发结束爆炸</dd></div></dl><p class="status-related"><a href="#/combat/skills/chain-lightning">闪电链 →</a></p></article><article class="status-card" id="poison-burst"><div class="status-heading"><img class="status-icon" src="assets/server/buffs/toxin_burst.png" alt=""><h3>毒素爆发</h3></div><p>到期后造成范围毒素伤害并施加中毒。爆炸伤害和中毒层数由技能决定。</p><dl><div><dt>持续时间</dt><dd>2 秒</dd></div><div><dt>层数上限</dt><dd>1 层</dd></div><div><dt>再次施加</dt><dd>不刷新</dd></div><div><dt>净化</dt><dd>不可以</dd></div></dl><p class="status-related"><a href="#/combat/skills/totem">图腾 →</a></p></article></div>

## 眩晕、冻结、沉默与定身 :id=control

| 状态 | 移动 | 施放新技能 | 主要规则 |
| --- | --- | --- | --- |
| <img class="status-icon" src="assets/server/buffs/stun.png" alt=""> 眩晕 | 禁止 | 禁止 | 受韧性与连续控制保护影响；可打断部分读条 |
| <img class="status-icon" src="assets/server/buffs/freeze.png" alt=""> 冻结 | 禁止 | 禁止 | 受韧性与连续控制保护影响；可触发冰封、破冰效果 |
| <img class="status-icon" src="assets/server/buffs/silence.png" alt=""> 沉默 | 允许 | 禁止 | 受韧性与连续控制保护影响；可打断部分读条 |
| <img class="status-icon" src="assets/server/buffs/slow.png" alt=""> 定身 | 禁止 | 允许 | 限制移动，仍可使用允许施放的技能 |

这些控制均可被普通净化移除。控制时长由施加技能决定，同一时间受到多次控制，不会把所有持续时间简单相加。

被眩晕、冻结或沉默时，已发射的弹体、已召唤的天神与圣眼继续行动。现有召唤物仍可通过净化技能帮助友军。

机制强制控制会同时限制移动与施法，不能通过普通净化解除。

## 增益状态 :id=buffs

<div class="status-grid"><article class="status-card" id="zeal"><div class="status-heading"><img class="pixel-icon" src="assets/server/abilities/flying_hammer_zeal.png" alt=""><h3>热诚</h3></div><p>每层提高 <strong>4% 物理伤害</strong>与 <strong>2 个百分点技能暴击率</strong>。</p><dl><div><dt>持续时间</dt><dd>5 秒</dd></div><div><dt>叠加刷新</dt><dd>刷新</dd></div><div><dt>层数上限</dt><dd>由飞锤热诚节点决定</dd></div></dl><p class="status-related"><a href="#/combat/skills/flying-hammer?node=飞锤热诚&id=技能树">飞锤热诚</a> · <a href="#/combat/skills/flying-hammer?node=拾取热诚&id=技能树">拾取热诚</a></p></article><article class="status-card" id="sweep-momentum"><div class="status-heading"><img class="status-icon" src="assets/server/buffs/sweep_momentum.png" alt=""><h3>横扫之势</h3></div><p>横扫击中时获得，逐层提高横扫伤害。其他节点可提高层数上限、持续时间或追加恢复与暴击伤害。</p><dl><div><dt>基础时长</dt><dd>3 秒</dd></div><div><dt>基础上限</dt><dd>5 层</dd></div><div><dt>每层增伤</dt><dd>由横扫之势节点等级决定</dd></div></dl><p class="status-related"><a href="#/combat/skills/sweep?node=横扫之势&id=技能树">横扫之势</a> · <a href="#/combat/skills/sweep?node=猛势&id=技能树">猛势</a> · <a href="#/combat/skills/sweep?node=守势&id=技能树">守势</a></p></article><article class="status-card" id="leap-momentum"><div class="status-heading"><img class="status-icon" src="assets/server/buffs/leap_momentum.png" alt=""><h3>跃击之势</h3></div><p>施放跃击时获得，提高跃击伤害。</p><dl><div><dt>持续时间</dt><dd>5 秒</dd></div><div><dt>层数上限</dt><dd>5 层</dd></div><div><dt>每层增伤</dt><dd>由跃击之势节点等级决定</dd></div></dl><p class="status-related"><a href="#/combat/skills/leap?node=跃击之势&id=技能树">跃击之势</a></p></article><article class="status-card" id="fury"><div class="status-heading"><img class="status-icon" src="assets/server/buffs/fury.png" alt=""><h3>狂怒</h3></div><p>每层提高 <strong>5% 攻击速度</strong>与 <strong>3% 移动速度</strong>。</p><dl><div><dt>持续时间</dt><dd>12 秒</dd></div><div><dt>层数上限</dt><dd>99 层</dd></div><div><dt>叠加刷新</dt><dd>刷新</dd></div></dl><p class="status-related"><a href="#/combat/attributes?id=speed">攻击速度 →</a></p></article></div>

| 其他增益 | 效果 | 详细规则 |
| --- | --- | --- |
| <img class="pixel-icon" src="assets/server/stats/dome.png" alt=""> 护盾 | 在生命之前吸收伤害，破盾不溢出扣血 | <a href="#/combat/shield">护盾</a> |
| <img class="status-icon" src="assets/server/buffs/invulnerability.png" alt=""> 无敌 | 阻止受到伤害；持续时间由技能决定 | <a href="#/combat/skills">技能图鉴</a> |
| <img class="status-icon" src="assets/server/buffs/control_immunity.png" alt=""> 免疫控制 | 阻止适用控制生效；与无敌分别作用 | <a href="#/combat/status-effects?id=tenacity">韧性与免控</a> |
| <img class="pixel-icon" src="assets/server/stats/dome.png" alt=""> 持续生命恢复 | 按技能规定的频率恢复生命 | <a href="#/combat/defense?id=healing">治疗与恢复</a> |
| <img class="pixel-icon" src="assets/server/stats/dome.png" alt=""> 治疗提高 | 增加治疗量，数值与时长由来源技能决定 | <a href="#/combat/defense?id=healing">治疗与恢复</a> |
| <img class="pixel-icon" src="assets/server/stats/dome.png" alt=""> 法力恢复 | 补充法力，具体恢复量由来源技能决定 | <a href="#/combat/attributes?id=mana">法力</a> |
| <img class="pixel-icon" src="assets/server/stats/dome.png" alt=""> 受到伤害降低 | 在持续期间减少承受的伤害 | <a href="#/combat/defense?id=reduction">伤害减免</a> |
| <img class="pixel-icon" src="assets/server/stats/dome.png" alt=""> 移速加成 | 在持续期间提高移动速度 | <a href="#/combat/attributes?id=movement">移动速度</a> |

死亡免疫可在持续期间阻止伤害导致的死亡，持续时间与触发条件见提供该效果的技能。职业专属状态的数值与成长可通过技能树节点查看。

## <img class="pixel-icon" src="assets/server/stats/tenacity.png" alt=""> 韧性与连续控制保护 :id=tenacity

韧性缩短适用控制的持续时间，有效上限为 <strong>75%</strong>。

<div class="formula">控制时长 = 基础时长 ×（1 − 韧性 ÷ 100）</div>

| 基础 2 秒控制 | 0% 韧性 | 25% 韧性 | 50% 韧性 | 75% 及以上韧性 |
| --- | --- | --- | --- | --- |
| 最终时长 | 2 秒 | 1.5 秒 | 1 秒 | 0.5 秒 |

时长按 0.05 秒向下取整，最短为 0.05 秒。

眩晕、冻结与沉默共用最多 <strong>5 秒</strong>的连续控制时间；同时受到这些控制时，每秒仍只消耗 1 秒额度。脱离控制后，每秒恢复 1 秒额度，最高恢复至 5 秒。

额度耗尽时，上述控制立即结束，并获得 <strong>2 秒</strong>对应控制免疫。后续控制的持续时间最多为当时剩余额度。

## 首领韧性条与反制 :id=boss

拥有韧性条的首领受到普通控制时，控制会转为韧性伤害。韧性耗尽后，首领进入破韧眩晕。通用韧性值为 <strong>1000</strong>，特殊首领以其机制说明为准。

| 行为或阶段 | 通用数值 |
| --- | --- |
| 施加有效控制 | 50 点韧性伤害 |
| 成功反制 | 250 点韧性伤害 |
| 每次造成伤害 | 0.1 点韧性伤害，与本次伤害量无关 |
| 破韧眩晕 | 6 秒 |
| 破韧后的恢复阶段 | 1 秒 |

破韧眩晕不能被普通净化解除。对普通或精英怪物成功反制可打断技能时，会造成 <strong>2 秒眩晕</strong>，再受韧性和连续控制保护影响。

## 净化 :id=cleanse

净化移除指定负面状态。一次净化移除多少种状态、影响哪些目标，由提供净化的技能决定。

| 可以解除 | 不能解除 |
| --- | --- |
| 眩晕、冻结、沉默、定身 | 破韧眩晕、机制强制控制 |
| 点燃、冻伤、中毒、静电、流血 | 毒素爆发 |
| 迟缓、冰缓、致盲、缓慢诅咒 | 护盾、无敌、免疫控制等增益 |
| 破甲、感电、治疗降低、火花电荷 | — |

<strong>净化火花电荷也会触发其结束爆炸。</strong> 解除该状态并不等于取消爆炸。

<a href="#/combat/skills/divine-descent?node=净罪之光&id=技能树">净罪之光</a>可清除友军可净化的负面效果并恢复生命；<a href="#/combat/skills/watchful-eye?node=净愈之瞳&id=技能树">净愈之瞳</a>定期移除守护友军的一种可净化负面效果。

<div class="page-end">TopCraft 玩家手册 · 更新于 2026-11-14</div>
