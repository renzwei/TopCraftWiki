# 帮助章节维护 · 2026-11-16

正文直接维护于 `guide/help.md`、`guide/commands.md`、`guide/troubleshooting.md`、`guide/feedback.md`。`.work/write_help.py` 仅为本次批量写入工具，不是持续生成源。交互由 `assets/help.js`、样式由 `assets/help.css` 提供。未修改服务器配置。

## 结构与检索

- 帮助页保留旧地址及常用命令、如何反馈等锚点。24 个问答具有稳定 ID，支持分类、关键词和同义词检索。旧标题的空格与连字符形式均可定位并展开。
- 问答纳入全站搜索，搜索结果直接定位具体问题；搜索命名空间提升到 help-v19。
- 26 条玩家命令按用途筛选并复制，参数占位符保留中文提示和替换示例。未收录管理、测试、发放类命令。
- 反馈模板按七类问题提供只读预览和复制；不收集、不储存、不提交玩家报告。复制失败时提供手动选择复制提示。
- 手机沿用现有侧栏交互。帮助页禁用浏览器原生平滑滚动，避免与 Docsify 的锚点滚动冲突。

## 内容依据与未定事项

- 沿用各章节已经核对的事实及 `_maintenance/{guide,social,life,equipment,dungeons,world}.md` 和对应来源映射；具体规则链接到这些章节，避免重复维护大段攻略。
- 再核对 MMOCore commands.yml、zMenu commands、TopCraftProfessionMarket/plugin.yml、TopCraftLifeQuests/plugin.yml、TopAppreciation、TopInvite、TopCraftPartyRecruitment、topcraft-dungeon-keys 和 topcraft-dungeon-progress 的命令注册。赞赏命令需具有使用权限，不承诺所有玩家默认可用。
- 用户确认公开地址 topcraft.cc、Java 版 1.21；取消职业点限制是计划，Wiki 不宣称已完成服务器变更。
- 用户确认森林 NPC 传送尚未添加、首把秘境钥匙获取方式尚未确定。
- 本次用户确认反馈渠道尚未确定。明确写“反馈入口待公布”，移除旧文“联系方式见游戏内公告”的无依据说法。
- 仅复用已有服务器图标，其来源与哈希沿用 guide-assets.json；没有新生成的游戏界面或故障截图。

## 验证

运行 scripts/check_wiki.py、JavaScript 语法检查和 git diff --check。浏览器验证分类与关键词交集、清除筛选、无结果提示、旧锚点展开、路由切换后重新绑定、命令剪贴板内容、反馈类型切换及复制。检查桌面与 390px 手机视口的四页布局。
