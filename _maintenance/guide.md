# 开始冒险维护 · 2026-11-16

五页正文直接维护于 `guide/join.md`、`start.md`、`controls.md`、`interface.md`、`rewards.md`；`help.md` 为相关排障与命令索引。`scripts/build_guide_data.py` 仅刷新引用数据、复制原图并重建搜索路由，不覆盖正文。服务器只读，未启动游戏服务器。

## 玩家入口与用户确认

- 用户明确公开地址为 `topcraft.cc`，客户端版本为 Java 版 `1.21`。不从服务器监听地址推导公开域名，也不将版本扩写成任意 1.21.x。
- 用户明确计划移除选择和切换职业的职业点消耗。当前目录仍为初始 0 点、选职业检查至少 1 点，确认时扣 1 点。Wiki 采用“将取消”的说明，并提供残留不足提示的处理方式，不宣称服务器修改已经完成。本次没有修改服务端。
- 用户已在世界探索任务中确认：主城与落日森林尚无玩家传送入口，计划通过 NPC 传送。保留未开放说明，不能编造第一条出城路线。

## 核对依据

来源映射见 `guide-sources.json` 和 `sources.json`。36 张原图的原路径与 SHA-256 见 `guide-assets.json`；另复用已有技能按键图片和 ImageGen 冒险插画。界面示意由 HTML/CSS 组合原图，未改写服务器贴图，也未生成假游戏截图。

- ItemsAdder 的 `apply_on_join.enabled=false` 不等于没有自动下发。`apply_during_chunk_load_phase=true`；已安装 4.0.5 的 `itemsadder.m.ar.cn` 对应这一设置，`acg.ow()` 将资源包写入登录加载阶段的发送路径。TopCraftPackCompat 在修复合并后刷新登录资源包。旧分析中仅依据 apply_on_join 的判断已纠正。
- 当前自托管地址为回环地址，公共下载连通性未做实机验证，Wiki 不刊载内部下载地址。连接域名和版本采用用户确认；并未连接公网游戏服务器测试。
- 背包五入口来自 TopCraftEquipmentSlots raw slots 0–4，分别为个人信息、额外背包、技能、职业、主菜单。位置按 Java 背包的结果槽与 2×2 槽位绘制。个人信息既可悬停查看，也可点击执行角色详情命令。
- 主菜单实际六项为任务、生活委托、生活技能、队伍、流派、公告；已修复旧 Wiki 把公告写作帮助的问题。
- SkillList 点击技能设为 selected；槽位左键绑定、右键解绑、Shift+左键选中已绑定技能。MMOCore KEY_COMBOS 为左键/F/潜行左键/潜行右键/Q，组合超时 10 tick。图标使用固定默认键位，客户端改键应按对应动作操作。
- HUD 状态示意仅展示单个槽位：就绪、冷却、法力不足、空槽。3.2 秒是演示值，不能当成火球术固定冷却；资源栏 12 级/420 生命/80 法力也是演示数值。
- 奖励基于 DailyReward 2.14.0 已安装实现：`EnoughPlayTimeChecker` 按原版游玩统计 tick/20/60 判断 100 分钟；并非每日要再玩 100 分钟。`DataManager.initiatePlayer` 为未记录的新玩家创建 now+24h/168h/720h 的首次等待，因为三个 available-after-first-join 均为 false。`CooldownManager$1` 在领取后存储 now+cooldown。由此区分现实时间倒计时与累计游玩门槛。
- 奖励不按日历午夜、周一或每月一日重置，不累积多份补领。每种礼包独立计时；普通与 premium 配置本次内容相同，不承诺任何额外等级奖励。
- 背包容量检查只检测至少一个空格，并非完整模拟三类物品入包。页面建议整理空间，不承诺仅一个空格能容纳全部奖励。
- 奖励 NPC 坐标来自 Citizens saves；其命令为 dailyrewards:rewards。主城页面和世界生成器默认奖励链接已同步改到 guide/rewards，避免下次生成覆盖。

## 参考与验证

参考 Last Epoch 官方 Unlocking Skills 的“入口—操作—结果”和配图方式，Diablo Wiki Interface 的按界面区分目录方式；D3 页面含 Beta 资料，未采用其规则或按键。

- https://support.lastepoch.com/hc/en-us/articles/46363194853915-Unlocking-Skills
- https://www.diablowiki.net/Interface

静态检查使用 `python scripts/check_wiki.py`，脚本语法使用 `node --check assets/guide.js`。浏览器检查包括背包说明切换、主菜单按钮、四种技能状态、键盘激活、手机布局、跨页深链接和全站搜索。更新正文或目录时递增 `assets/wiki.js` 搜索 namespace。

完整浏览器截图保存在 `.work/guide-desktop.png`、`.work/guide-mobile.png`。本次验收不包含 Minecraft 内的首次登录、职业切换或实际领取奖励。

本次全站检查：138 个 Markdown 页面、8623 处本地引用、971 项资产，无缺失或哈希错误；JavaScript 语法与 `git diff --check` 通过。连接信息、三种礼包金额与冷却、首次等待配置和五个搜索路由另行比对通过。390 px 下页面未横向溢出，较宽奖励表在自身容器内滚动；搜索“100 分钟”及技能绑定说明的跨页锚点均已验证。
