<p class="eyebrow">TOPCRAFT / 秘境挑战</p>

# 层数难度与通关规则

<p class="lead">层数决定敌人的强度，结算耗时决定通关评价。结算耗时包含实际挑战时间与全队死亡罚时。</p>

## 层数与敌人强度

黑曜石秘境每提高 1 层，敌人生命和伤害的层数倍率都乘以 <strong>1.16</strong>，即比上一层提高 <strong>16%</strong>。同一敌人在第 L 层相对于 1 层的倍率为 <strong>1.16<sup>L−1</sup></strong>。

<div class="dg-panel" data-dungeon-tool="difficulty"><h3>层数难度查询</h3><div class="dg-controls"><label>挑战层数<input name="layer" type="number" min="1" max="100000" step="1" value="10"></label></div><p role="status" class="dg-error">正在加载…</p><div class="dg-results" aria-live="polite"></div><p class="dg-note">比较同一种敌人在不同层数的强度。首领技能、地面机关和按最大生命造成的伤害，分别见各地图攻略。</p></div>

敌人种类之间仍有各自的生命与攻击差异。按玩家最大生命百分比造成的机制伤害，例如樱落溪涧的魂魄触碰，不用上述倍率换算。

## 限时与裂界速通

| 地图 | 通关时限 | 裂界速通时限 |
| --- | --- | --- |
| [蘑菇森林](dungeons/mushroom.md) | 12:00 | 8:24 |
| [赤沙遗迹](dungeons/desert.md) | 12:00 | 8:24 |
| [樱落溪涧](dungeons/sakura.md) | 15:00 | 10:30 |

在通关时限内击败最终首领，为<strong>限时通关</strong>；结算耗时不超过通关时限的 <strong>70%</strong>，获得<strong>裂界速通</strong>评价。超过时限仍可继续挑战，击败首领后按超时通关结算。

游戏中的「裂界剩余」表示距离速通截止还有多久，不是本局剩余的通关时间。裂界时间耗尽后，仍有机会完成普通限时通关。

## 死亡与复活

蘑菇森林、赤沙遗迹、樱落溪涧均允许死亡后复活继续挑战。<strong>每名成员每死亡一次，全队结算耗时增加 15 秒。</strong> 同时阵亡两人即增加 30 秒；同一人多次死亡会分别计入。

结算耗时 = 实际挑战耗时 + 全队死亡次数 × 15 秒。

例如，蘑菇森林实际用时 11:40，全队死亡 2 次，结算耗时为 <strong>12:10</strong>，属于超时通关。实际用时 8:10、死亡 1 次，则为 <strong>8:25</strong>，仍然限时通关，但未达到裂界速通。

死亡罚时同时影响通关评价、钥匙结算和赛季评分。计时界面已经包含罚时，用游戏中显示的结算耗时时无需再加一次。

## 通关后会发生什么

击败最终首领后停止计时，显示通关评价、耗时与分数，并在约 <strong>10 秒</strong>后返回。使用过钥匙时，同步结算钥匙层数与下一张地图；详细例子见[入场与钥匙](dungeons/entry.md)。

当前三张秘境的正式通关物品奖励尚未公布。赛季纪录、排名和嘉奖门槛见[赛季评分与嘉奖](dungeons/season.md)。

## 计算本次结果

输入不含罚时的实际用时和全队死亡次数，即可在[成绩计算器](dungeons/season.md?id=成绩计算器)中查询评价、分数与钥匙结果。

<div class="dg-page-nav"><a href="#/dungeons/entry">← 入场与钥匙</a><a href="#/dungeons/season">赛季评分与嘉奖 →</a></div>

<div class="page-end">TopCraft 玩家手册 · 更新于 2026-11-16</div>
