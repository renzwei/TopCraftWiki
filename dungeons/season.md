<p class="eyebrow">TOPCRAFT / 秘境挑战</p>

# 赛季评分与嘉奖

<p class="lead">挑战层数决定基础分，完成速度决定时间加分。每张地图保留你的最好成绩，各地图成绩相加形成赛季总分。</p>

打开[秘境入口](dungeons/entry.md?id=发起入场)，点击<strong>秘境征途</strong>，查看赛季纪录、排名和嘉奖进度。本页介绍第一赛季的评分规则。

## 成绩计算器

<div class="dg-panel" data-dungeon-tool="score"><div class="dg-controls"><label>挑战地图<select name="map"><option value="1001">蘑菇森林 · 12 分钟</option><option value="1003">赤沙遗迹 · 12 分钟</option><option value="1004">樱落溪涧 · 15 分钟</option></select></label><label>挑战层数<input name="layer" type="number" min="1" max="100000" step="1" value="10"></label><label>实际用时 · 分<input name="minutes" type="number" min="0" max="14400" step="1" value="8"></label><label>实际用时 · 秒<input name="seconds" type="number" min="0" max="59.999" step="0.001" value="0"></label><label>全队死亡次数<input name="deaths" type="number" min="0" max="100000" step="1" value="0"></label></div><p role="status" class="dg-error">正在加载…</p><div class="dg-results" aria-live="polite"></div><p class="dg-note">用于已通关的挑战。实际用时不含罚时；若输入游戏结算界面显示的耗时，请将死亡次数设为 0，避免重复计算。1 层按无钥匙挑战计算。</p></div>

## 单次通关如何评分

<strong>基础分 = 10 × 挑战层数 + 10。</strong> 例如，10 层基础分为 110 分，20 层为 210 分。

限时通关时，加上 <strong>20 × 剩余时间占比</strong>的时间分，最多加 10 分。剩余时间占比为「剩余时间 ÷ 通关时限」；在时限一半以内完成，即获得全部 10 分时间加分。

| 10 层蘑菇森林的结算耗时 | 结果 | 显示分数 |
| --- | --- | --- |
| 6:00 | 裂界速通，获得全部时间加分 | 120 |
| 8:00 | 裂界速通 | 116 |
| 12:00 | 恰好限时通关，无时间加分 | 110 |
| 12:01 | 超时通关 | 76 |
| 18:00 及以后 | 达到超时评分下限 | 55 |

<strong>超时通关</strong>没有时间加分，得分从接近基础分的 70% 开始，随超时继续降低，最低为基础分的 50%。超时比例为「超出时间 ÷ 通关时限」，得分为：

基础分 × max（50%，70% − 40% × 超时比例）。

因此，刚超过时限时，分数会明显下降。死亡罚时也计入这一判定。

界面显示整数分，省略不足 1 分的小数；排名比较保留更精细的成绩。因此，看起来同分的两条纪录仍可能有先后。

## 个人纪录与赛季总分

每张地图只取个人最好的一次成绩。刷新纪录后，总分只增加新旧成绩的差额，不会把每次通关分数重复相加。

例如，蘑菇森林 116 分、赤沙遗迹 108 分、樱落溪涧 120 分，总分为 <strong>344 分</strong>。后来蘑菇森林提高到 126 分，总分变为 <strong>354 分</strong>；再次打出 116 分则不增加总分。

组队通关时，保留结算资格的成员分别记录本局成绩。单图排行榜优先比较分数，其次比较层数，再比较结算耗时；总分榜按赛季总分排列。成绩绑定玩家，切换职业不会额外建立一份可叠加的单图分数。

## 赛季嘉奖

<div class="dg-badges"><div><img src="assets/server/dungeons/gold.png" alt="黄金徽章"><strong>黄金</strong><span>600 分</span></div><div><img src="assets/server/dungeons/diamond.png" alt="钻石徽章"><strong>钻石</strong><span>900 分</span></div><div><img src="assets/server/dungeons/emerald.png" alt="绿宝石徽章"><strong>绿宝石</strong><span>1200 分</span></div><div><img src="assets/server/dungeons/obsidian.png" alt="黑曜石徽章"><strong>黑曜石</strong><span>1650 分</span></div><div><img src="assets/server/dungeons/crying-obsidian.png" alt="哭泣黑曜石徽章"><strong>哭泣黑曜石</strong><span>2200 分</span></div></div>

以上为第一赛季的总分门槛。<strong>各档物品奖励尚未公布</strong>；当前没有可列出的装备、货币或箱子奖励。地图中的咒玉、跃动彩虹和同心属于本次挑战的增益，分别在地图攻略中介绍。

## 常见问题

### 达到裂界速通，为什么不是满额时间加分？

裂界速通要求在 70% 时限内完成，满额时间加分则要求在 50% 时限内完成。两者是不同门槛。

### 打了更高层，为什么没有刷新纪录？

个人纪录首先比较分数。高层超时的得分可能低于较低层的限时通关；可使用上方计算器比较。

### 同一张图换职业再打，会增加一份分数吗？

不会。该地图仍然只有一份个人最好成绩；换职业后打出更好的成绩，才会更新纪录和赛季总分。

<div class="dg-page-nav"><a href="#/dungeons/rules">← 通关规则</a><a href="#/dungeons/overview">选择地图 →</a></div>

<div class="page-end">TopCraft 玩家手册 · 更新于 2026-11-17</div>
