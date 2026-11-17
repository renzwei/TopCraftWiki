<p class="eyebrow">TOPCRAFT / 组队与社交</p>

# 金币与玩家交易

<p class="lead">通过玩家档案发送交易请求，在交换界面放入物品并调整金币数量。双方确认、倒计时结束后完成交换。</p>

<div class="social-note">玩家间交易需要<strong>玩家或以上身份</strong>。新人累计游玩 15 分钟后自动晋升；这一限制针对玩家间交易，与 NPC 买卖是不同功能。<a href="#/social/permissions">查看社交身份与权限</a>。</div>

<div class="social-facts"><div><b>15 秒</b>接受交易请求的时间</div><div><b>3 秒</b>双方确认后的倒计时</div><div><b>0</b>金币交易税</div></div>

## 发起并完成交易

<div class="social-steps"><section class="social-step"><header><img class="social-icon" src="assets/server/social/trade.png" alt="发起交易图标"><strong>发送请求</strong></header><p>脱离战斗后，潜行右键打开对方档案，点击“发起交易”。对方在 15 秒内点击聊天中的接受按钮。</p></section><section class="social-step"><header><span class="trade-offer-icons" aria-hidden="true"><img src="assets/home-icons/equipment-items.png" alt=""><img src="assets/server/guide/inventory-coin.png" alt=""></span><strong>放入物品与金币</strong></header><p>将要交出的物品放在自己的交易区域，通过金币按钮调整金额。双方分别设置自己提供的内容。</p></section><section class="social-step"><header><span class="trade-confirm-icon" aria-hidden="true"><span></span><span></span></span><strong>双方确认</strong></header><p>点击确认按钮。<span class="trade-confirm-legend"><span><i class="trade-state-pending" aria-hidden="true"></i>红色玻璃板：尚未确认</span><span><i class="trade-state-accepted" aria-hidden="true"></i>绿色玻璃板：已确认</span></span>双方确认后开始 3 秒倒计时，倒计时结束后完成交换；只有一方确认时还不会成交。</p></section></div>

查看对方提供的物品时，可悬停阅读名称、数量、词条与使用条件。交易得到的物品仍保留自身的等级、职业和使用限制，具体见[武器与穿戴](equipment/slots.md)。

## 调整金币金额

金币按钮显示当前提供金额与可用余额。**左键增加、右键减少**；按住 **Shift** 时，以该按钮步长的 **10 倍**调整。

| 金币按钮步长 | 普通点击 | Shift 点击 |
| --- | --- | --- |
| 1 | 增减 1 | 增减 10 |
| 100 | 增减 100 | 增减 1,000 |
| 10,000 | 增减 10,000 | 增减 100,000 |
| 1,000,000 | 增减 1,000,000 | 增减 10,000,000 |

不能提供超过自己余额的金币。金币交易不收固定税或比例税：提供 **100 金币**，对方收到 **100 金币**。

## 交易条件与中止

<div class="social-table"><table><thead><tr><th>条件或操作</th><th>结果</th></tr></thead><tbody><tr><td>刚刚参与战斗</td><td>战斗后 10 秒内不能交易。</td></tr><tr><td>交易过程中移动</td><td>交易取消。</td></tr><tr><td>交易过程中受到伤害</td><td>交易取消。</td></tr><tr><td>双方处于不同游戏模式</td><td>不能互相交易。</td></tr><tr><td>双方来自同一 IP</td><td>不能互相交易；同一家庭或共享网络可能遇到这一限制。</td></tr><tr><td>双方处于不同世界</td><td>允许发送交易请求，不要求站在彼此附近。</td></tr><tr><td>背包空间不足</td><td>无法正常接收本次交易物品，需要腾出空间后再交易。</td></tr><tr><td>物品不能放入交易区域</td><td>该物品受到交易限制，不能通过本次交易交换。</td></tr></tbody></table></div>

交易未成交就取消时，双方不会完成金币交换，已放入的物品退还各自持有者。对方拒绝、请求超过 15 秒未接受时，也不会建立交易。

## 金币从哪里来、用在哪里？

自己的余额可在个人信息中查看。公开玩家档案不展示他人的金币。

| 内容 | 查询位置 |
| --- | --- |
| 出售作物、矿物、木材与鱼获 | [资源收购与按等级计算的卖价](life/market.md) |
| 购买生活工具、鱼竿和食材 | [商店价格表](life/market.md) |
| 修理工具与装备 | [维修费用与操作](life/market.md?id=维修) |
| 鱼竿部件改造 | [鱼饵与渔具改装](life/tackle.md) |
| 邀请新玩家获得金币 | [邀请奖励与累计里程碑](social/invitations.md) |
| 与其他玩家交换物品和金币 | 本页的交易流程 |

生活商店收购价会随对应职业等级变化；玩家之间交易的金额由双方自行设置。海盗币用于芬恩处的特定鱼竿兑换，是物品形式的专用货币，与金币余额分别使用。

## 常见问题

| 问题 | 原因与操作 |
| --- | --- |
| 是好友，为什么仍不能交易？ | 好友关系不会取消战斗、游戏模式、同 IP 或其他交易限制。 |
| 同住的两名玩家无法交易 | 当前禁止同 IP 之间交易，不是好友关系或距离问题。 |
| 点了确认却没有成交 | 对方也需确认，并等待 3 秒倒计时结束。 |
| 交易突然关闭 | 移动或受伤都会取消交易；重新站定并脱离战斗后再发起。 |
| 金额变化太大 | Shift 点击使用十倍步长，普通点击使用按钮标注的步长。 |
| 发起请求后没有进入界面 | 等待对方接受；15 秒过期后需要重新发送。 |

<nav class="social-nav"><a href="#/social/profile">玩家档案与好友</a><a href="#/life/market">商人、收购与维修</a><a href="#/equipment/overview">装备与道具</a></nav>

<div class="page-end">TopCraft 玩家手册 · 组队与社交 · 2026-11-17</div>
