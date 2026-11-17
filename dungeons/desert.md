<p class="eyebrow">TOPCRAFT / 秘境挑战</p>

# 赤沙遗迹

<p class="lead">雷炉中的负雷者能够炸开桥头石闸。护送它们穿过三波阻击，在三次爆破后深入祭坛，迎战会将地面化为熔湖的炎狱恶魔。</p>

<div class="dg-facts"><span>人数<b>1–4 人</b></span><span>通关时限<b>12:00</b></span><span>裂界速通<b>8:24</b></span><span>最终首领<b>炎狱恶魔</b></span></div>

<ol class="dg-flow"><li><a href="#/dungeons/desert?id=雷炉与负雷者">唤醒负雷者</a><small>蓝、金、紫任一雷炉；清守卫后右键。</small></li><li><a href="#/dungeons/desert?id=护送与三次爆破">护送与爆破</a><small>清理三波阻击；累计爆破 3 次。</small></li><li><a href="#/dungeons/desert?id=祭坛与首领">前往祭坛</a><small>攻击金骷髅 5 次，唤醒首领。</small></li><li><a href="#/dungeons/desert?id=熔湖阶段">熔湖决战</a><small>35% 生命触发；8 秒内撤离即将熔化的地面。</small></li></ol>

## 雷炉与负雷者

地图中有蓝、金、紫三座雷炉。先击败炉旁对应的守炉者，再右键雷炉。经过 <strong>5 秒</strong>唤醒，负雷者出现并沿固定路线向桥头前进。

<div class="dg-callout"><img src="assets/server/dungeons/fire.png" alt="火焰图标"><p><strong>同一座雷炉可以反复使用</strong>不需要三座雷炉各完成一次。单人可以反复护送同一路线；队伍也可以分路，同时护送不同雷炉的负雷者。</p></div>

| 雷炉 | 位置 X / Y / Z | 护送方向 |
| --- | --- | --- |
| 蓝色雷炉 | 450.5 / 0 / 2.5 | 从东侧出发，前往桥头 |
| 金色雷炉 | 365.5 / −1 / 10.5 | 从西南侧出发，前往桥头 |
| 紫色雷炉 | 361.5 / 0 / −112.5 | 从西北侧出发，前往桥头 |

三条路线的目标相同，均需处理途中三波阻击。选择路线时，可以结合队伍所在位置和已经清理的敌人，减少往返。

## 护送与三次爆破

负雷者行进到阻击点时会停下，进度显示为「遇袭」。清理该波敌人后，它会继续前进。只跑到终点等待，不能让途中遇袭的负雷者自动完成护送。

到达桥头后，负雷者开始 <strong>3 秒雷核过载</strong>。每次成功爆破使石闸进度增加 1，全队累计 <strong>3 次</strong>即可打开石闸。同一路线的负雷者仍在护送途中时，该雷炉不能再唤醒第二只。

<figure class="dg-diagram" tabindex="0"><svg viewBox="0 0 760 230" role="img" aria-label="蓝色、金色、紫色雷炉的护送路线共同计入三次爆破，之后通往祭坛"><rect x="25" y="15" width="170" height="48" rx="8" fill="#b7dbea"/><rect x="25" y="90" width="170" height="48" rx="8" fill="#e7d69d"/><rect x="25" y="165" width="170" height="48" rx="8" fill="#d6bee6"/><text x="110" y="46" text-anchor="middle" font-size="18">蓝色雷炉</text><text x="110" y="121" text-anchor="middle" font-size="18">金色雷炉</text><text x="110" y="196" text-anchor="middle" font-size="18">紫色雷炉</text><path d="M195 39 H260 V114 H335 M195 114 H335 M195 189 H260 V114 M515 114 H570"/><rect x="335" y="71" width="180" height="87" rx="8" fill="#e1ddce"/><text x="425" y="107" text-anchor="middle" font-size="18">桥头石闸</text><text x="425" y="137" text-anchor="middle" font-size="16">累计爆破 3 次</text><rect x="570" y="76" width="165" height="77" rx="8" fill="#e5bfae"/><text x="652" y="121" text-anchor="middle" font-size="18">金骷髅祭坛</text></svg><figcaption>推进关系示意，非地形路线图。可以三路并行，也可以从同一雷炉反复完成护送。</figcaption></figure>

## 祭坛与首领

石闸崩塌后，前往祭坛，攻击金骷髅 <strong>5 次</strong>唤醒炎狱恶魔。首领以「追火连击」和「焦土烙印」交替进攻，两套动作结束后会有短暂的普通战斗时间。

### 追火连击

连击按 <strong>裂地 → 横扫 → 飞锤 → 坠焰 → 扩散火环</strong>的顺序施放。躲开前一招后继续观察首领动作，尤其不要在飞锤落地后立即回到原位。

以下倍率均相对于首领攻击力，最终伤害还受角色减伤影响。

<div class="dg-mechanics"><div><h3>追火·裂地</h3><p class="dg-number">预警 1.3 秒 · 3 × 10 格矩形 · 135% 攻击力</p><p>沿目标方向冲砸，伤害覆盖狭长的地面区域。</p><p class="dg-response">向矩形两侧移动，比沿长边后退更快离开范围。</p></div><div><h3>追火·横扫</h3><p class="dg-number">蓄力 3 秒 · 前方 140°、8 格 · 115% 攻击力</p><p>前 2 秒追踪最近玩家，最后约 1 秒固定朝向。</p><p class="dg-response">避开扇形正面，利用最后一秒移动到侧后方。</p></div><div><h3>追火·飞锤</h3><p class="dg-number">预警 1.2 秒 · 半径 3 格 · 85% 攻击力</p><p>锁定 32 格内最远玩家的落点，投掷重锤。</p><p class="dg-response">远程成员将落点留在队伍外侧，看到圆圈后立即离开。</p></div><div><h3>追火·坠焰</h3><p class="dg-number">预警 0.9 秒 · 半径 3 格 · 100% 攻击力</p><p>飞锤落地后，首领传送到落点上方继续下砸。</p><p class="dg-response">飞锤与坠焰连续发生，保持离开落点的站位。</p></div><div><h3>扩散火环</h3><p class="dg-number">向外扩散至 16 格 · 115% 攻击力</p><p>下砸后向四周释放贴地火环。</p><p class="dg-response">观察火环接近的时机，跳过贴地火环，或提前退到扩散范围之外。</p></div><div><h3>焦土烙印</h3><p class="dg-number">预警 2 秒 · 半径 2.5 格 · 持续约 6 秒</p><p>锁定最远玩家，在落点留下焦土；焦土每秒造成首领攻击力 25% 的伤害。</p><p class="dg-response">把落点引离队友与通路，移出圆圈后继续避开留下的焦土地带。</p></div></div>

## 熔湖阶段

首领生命降至 <strong>35%</strong>时，中止当前动作，移动到战场指定位置，施放 <strong>8 秒「熔狱倾覆」</strong>。施法结束后，部分地面变为真实熔岩，战斗继续。

<div class="dg-timeline"><div style="flex:65"><strong>100% → 35% 生命</strong><small>追火连击与焦土烙印交替</small></div><div style="flex:35"><strong>35% 以下</strong><small>8 秒熔湖转阶段，随后继续战斗</small></div></div>

利用这 8 秒观察地面和周围落脚处，撤到未熔化的平台或岸边，再继续输出。不要把常规站位留在熔岩内：<strong>处于熔岩中，每 0.5 秒受到最大生命 6% 的伤害</strong>。失足后优先离开熔岩，再恢复生命。

## 常见问题

### 负雷者为什么停住了？

查看护送进度是否显示「遇袭」。返回负雷者附近，清理本波阻击敌人后继续护送。

### 必须同时走三条路线吗？

不需要。石闸计算全队累计爆破次数，同一雷炉可以重复召唤。分路能同时推进，但每路都需要有人处理阻击。

### 首领飞锤已经落地，为什么原地又受到一次伤害？

飞锤后紧接坠焰下砸，随后还有扩散火环。离开第一次落点后，等整套连击结束再调整输出位置。

<div class="dg-page-nav"><a href="#/dungeons/overview">← 秘境总览</a><a href="#/dungeons/rules">死亡与计时</a><a href="#/dungeons/season">成绩与奖励</a></div>

<div class="page-end">TopCraft 玩家手册 · 更新于 2026-11-16</div>
