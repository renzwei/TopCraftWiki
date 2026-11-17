# 完美格挡资料核对 · 2026-11-16

玩家正文：`combat/defense.md#perfect-block`，位于举盾格挡之下；页首索引及自动页内目录均可定位。

核对服务器当前目录：

- `plugins/MMOItems/shield-block.yml`：启用完美格挡，窗口 6 tick，基础冷却 5 秒。
- `plugin-src/TopCraftDivineDescent/ShieldBlockHandler.java`：`0 <= getActiveItemUsedTime() < 6`；主手、副手均支持。实际举盾、正耐久、无盾牌冷却与击中条件全部满足才结算。完美格挡跳过耐久与小数磨损扣除，但仍清除举盾状态、执行相同冷却并取消本次伤害。6 tick 边界按普通格挡处理。
- `plugins/MythicMobs/skills/职业技能/格挡处理器.yml`：公共效果为空，普通音高 1、完美音高 1.6，均为盾牌格挡音效；没有反击或眩晕效果。
- `plugin-src/TopCraftDivineDescent/tests/ShieldPerfectBlockTest.java`：核对现有边界、双手、免耐久与冷却测试的断言。本次只修改 Wiki，未运行游戏服务器或改动插件。

原正文“成功格挡必定消耗耐久”已改为区分普通与完美格挡，并补上剩余 80 耐久挡住 100 伤害的对照示例。

同步修正装备栏位页面及其生成脚本的格挡链接，从护盾锚点改为举盾格挡锚点。搜索缓存版本递增至 perfect-block-v21，便于直接搜索新增条目。全站引用校验通过，浏览器已确认正文和目录链接正常。
