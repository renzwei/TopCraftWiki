# 秘境章节维护

玩家页面位于 `dungeons/`，共享组件为 `assets/dungeons.css` 与 `assets/dungeons.js`。

## 数据和证据

运行 `scripts/build_dungeon_data.py <server-root>`，读取当前服务器目录，刷新 `assets/data/dungeons.json`、11 张服务器原图和来源哈希。脚本只写 Wiki，不修改服务器。

- 入场、钥匙：TopCraftDungeonKeys config/entrance、SeasonEntrance、DungeonStore、TopCraftDungeonKeys。
- 评分、嘉奖：TopCraftDungeonProgress definitions/season-1.json、ScoreRules、ScorePoints、ProgressStore。
- 地图：MythicMobs 蘑菇森林技能、赤沙遗迹、樱落溪涧技能。disabled 文件不作为现行攻略来源。
- 图标：ItemsAdder 已有钥匙按钮、白/墨咒玉、火焰、跃动彩虹；徽章来自服务器 UI 原图。全部原样复制，见 dungeon-assets.json。雷核原图是模型 UV 图集，不作为可读图标展示。
- 流程和机制图为 HTML/SVG 示意，不是游戏截图或可通行地形图。坐标取实际生成点；不捏造连续可走路线。

首次钥匙来源：用户于 2026-11-16 确认尚未确定。无钥匙 1 层不写成首次发钥匙入口；reclaim 仅补领已有绑定钥匙。嘉奖门槛已配置，items 为空；通关奖励也没有正式物品发放内容。

评分内部单位是百分之一分。JS 使用 BigInt 复现整数除法，界面显示 raw/100 向下取整；不将 60000 误写为 60000 分。比分保留小数精度而 UI 显示整数。总分按各图最好分数之和更新，不按职业另计，不累计每次成绩。

裂界判定复现 finish() 的 double 比较：720000 * 0.70 略小于 504000，所以 503999 ms 为 RAPID，504000 ms 为 TIMED；900000 * 0.70 等于 630000。显示时限仍为 8:24 / 10:30。测试保留这一实际边界，不擅自修改服务器或把计算器取整为意图值。

难度每层乘 1.16。30 是数值参考等级，不是入场等级限制。极高层查询用科学计数法避免 Infinity；不据此保证游戏运行时支持任意高的伤害值。

## 验证与运行边界

`scripts/check_wiki.py` 检查链接与图片哈希；`scripts/check_dungeons.cjs` 检查评分、限时边界、死亡罚时与钥匙上下限。页面在桌面和窄屏检查输入、导航与图示。

本次依据本地配置与实现编写，未连接线上运行中的赛季数据库，也未进行游戏实机通关。仓库存在待加载更新包；赛季定义会保存为运行快照，重新部署时需要同步核对实际赛季快照与已加载插件。不能把文件修改日期当成线上已生效的证据。

参考[最后纪元官方 Dungeons](https://support.lastepoch.com/hc/en-us/articles/46363322070683-What-are-Dungeons)的地图专属机制组织，以及[Diablo Wiki Greater Rifts](https://www.diablowiki.net/Greater_Rifts)的难度/计时/排名组织；TopCraft 的具体数值全部来自本服。
