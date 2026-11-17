# Wiki 维护说明

一般正文直接维护在各栏目 Markdown 文件中。三个职业页、18 个技能页和技能图鉴由生成脚本维护，技能交互说明编辑在 `combat-editorial.json`。审阅基线：2026-11-13 的本地 top-craft2 工作目录；未连接运行中的服务器。

- `sources.json`：每页的服务器相对来源路径。路径相对于服务器仓库，不发布为玩家链接。
- `assets.json`：复用图片的源路径、SHA-256 与生成图片说明。服务器图标原样复制，网页用 CSS 保持像素边缘。
- `imagegen-prompts.json`：内置 ImageGen 的完整提示词。
- 新版保留 Docsify 与原 CNAME；本次未提交、推送或部署。
- 原 info/class/weapon 入口保留跳转说明，补齐原先缺失的 profession/mob/map 入口。
- 旧截图保留文件但不用于当前攻略，以免误导。生成图片明确标为概念图。

## 后续核对

1. 服务器正式连接地址、支持客户端版本、群链接。
2. 秘境正式开放、赛季入口、奖励与完整实机攻略。
3. 落日森林任务奖励、后续章节、精英生成点与世界命名。
4. 锻造、冶炼及装备强化/镶嵌/分解/鉴定的完整玩家流程。
5. NPC 实机坐标、主城截图与最终 HUD 截图。

Windows 本地预览：双击仓库根目录的 `启动预览.cmd`，再打开 `http://127.0.0.1:8765/`。启动器依次寻找 PATH 中的 Node、常规安装目录及当前用户已有的 Codex 运行时，无需手动配置 PATH。保持启动窗口打开，按 Ctrl+C 停止服务。已配置 Node 的环境也可运行 `node scripts/preview.mjs`。不要直接用 file:// 打开，Docsify 需要读取 Markdown。

## 前端依赖

Docsify 4.13.1 本地托管；许可证见 `assets/vendor/LICENSE-docsify`。`search-topcraft.js` 基于同版官方 search.js，仅在索引保存前移除 HTML 标记与 Markdown 图片语法，防止搜索摘要显示源码。升级时保留此处理。

## 职业与战斗数据维护

18 个技能、380 个节点来自 MythicLib 技能参数及 MMOCore 中文职业实际引用的技能树。`assets/data/combat.json` 保留节点坐标、前置、路径格、原始数值表达式及图片对应关系。`combat-assets.json` 记录复用图片的来源与 SHA-256；不要手工重绘原图。

1. `python scripts/export_combat.py C:/Users/10740/Documents/top-craft2`：只读服务器目录，导出数据和原版贴图。此维护命令需要 PyYAML；浏览 Wiki 不需要 Python。
2. `node scripts/build_combat_reference.cjs`：生成三个职业页、18 个技能页、技能图鉴及完整搜索路径。技能描述来自游戏 lore，移除颜色、字体图标、手动换行并代入 1 级数值。线性成长展示初始值与每级增量。额外交互说明来自 `combat-editorial.json`，默认折叠；不要直接编辑生成页面。
3. `node scripts/check_combat.cjs`：检查拓扑、路径图片、参数求值及 4,812 组节点／技能／职业等级组合。
4. `python scripts/check_wiki.py`：检查链接、HTML 空行和两份资产清单的哈希。

`combat-corrections.json` 保存人工核实的界面／执行差异，进入根节点悬停与固定详情。当前包含寒冰箭、闪电链、陨石的真实伤害标签。公式解释另核对伤害、承伤、治疗、召唤物处理器及 Java 实现。

`combat-lore-copy.json` 保存少量节点的玩家文案覆盖，保留原始数值表达式。游戏内描述含“配置节点”等维护措辞时，可在这里改写；服务器更新对应节点后必须复核覆盖。节点富文本保留内容图标并映射到原版 PNG；仅移除游戏排版字符。

## 正文写作约定

2026-11-14 文案修订：正文面向玩家，说明对象、效果、条件、消耗、时长与成长。维护过程、配置字段、脚本分支、核验经过及待办只放在本目录。保持数值与机制细节，不以删减内容代替改写。

- 职业介绍先写战斗方式；技能介绍先写动作、目标和效果。
- 以事实描述代替劝告，例如“每第三次横扫伤害提高 75%”，不写“不要认为每次都造成三段”。
- 数值口径放进表头或简短图注，例如“基础生命”“节点基础效果”，不在每段重复提醒。
- 玩家操作保留必要步骤；“检查实现是否接管”“不能把参数代入”等核对口吻不进入正文。
- 实际使用限制仍须明确，例如充能与回溯的冲突、前置等级、冷却和点数花费。
- 尚未开放的内容用简短“测试中／奖励待公布”标记，不向玩家叙述资料收集过程。
- 同步维护静态页面、交互提示与生成模板，防止导出时恢复旧文案。

写法参考：[FF14 中文维基·战士](https://ff14.huijiwiki.com/wiki/战士)的职业定位与技能分类，以及 [Minecraft Wiki·Armor](https://minecraft.wiki/w/Armor)的机制解释、适用范围与数值表。仅参考条目组织方式，TopCraft 数据仍来自本地服务器资料。

2026-11-14 第二次结构修订按用户指定改用 ARPG 技能条目：参考 [Last Epoch Wiki·Fireball](https://lastepoch.fandom.com/wiki/Fireball) 的职业、解锁、消耗、说明与成长信息区，[Diablo Wiki·Bash](https://www.diablowiki.net/index.php?mobileaction=toggle_view_mobile&title=Bash) 与 [暗黑破坏神 III 官方技能页](https://eu.diablo3.blizzard.com/en-us/class/barbarian/active/bash) 的职业内技能导航和技能效果优先顺序。目录分“职业与技能”和“战斗机制”，18 个技能由职业页、同职业技能栏与搜索访问。升级与按键教程独立为 `combat/progression.md`。

技能树仅提供全树视图，按原坐标与路径自适应画布；可展开到全屏，保留悬停、选节点、节点等级预览和键盘操作。正文不再重复输出节点目录或逐级成长表。预览只代入当前节点等级，其他节点为 0；不自动套前置奖励、装备、目标防御。未知占位符直接报错，不以 0 静默掩盖。公式解析器仅支持有限算术，不执行配置中的 JavaScript。

技能线性公式已核对本地 MythicLib `LinearScalingFormula.evaluate`：base + perLevel × (level−1)。免费树重置核对本地 `TopCraftSkillTreeRefund$FreeReset`；普通技能与通用属性重置仍是独立资源。基础攻击共享计时核对 `PriestRangedAttack` 与 `timing.yml`。

浏览器验收记录与截图位于忽略目录 `.work/`。已检查 18 个技能页面和搜索；未启动游戏服、未做实机战斗测试，也未发布网站。

## 战斗机制条目维护（2026-11-14）

侧栏保留四个入口：角色属性、伤害与暴击、防御与恢复、状态与控制。持续伤害、召唤物、护盾为独立详细条目，通过入口卡片进入。升级与技能加点、加点方案与预设归入职业与技能。正文直接维护在 combat/*.md，`.work` 下的一次性迁移脚本不作为后续内容生成源。

- 页面使用稳定的 `:id=...` 章节锚点；状态资料卡使用 article id。不要随标题调整随意更换 id。
- `assets/combat.js` 的 mechanicLinks 维护术语跳转；职业与技能页生成时使用同一份链接映射，节点详情也支持跳转。悬停提示保留纯预览。
- `?node=节点名称&id=技能树` 支持打开技能页并选中对应节点；普通页内锚点不改变选中节点。
- 状态图鉴复用 BetterHud 注册表指向的原版图片，新增图片来源及哈希在 assets.json。技能节点描述的图标仍按 ItemsAdder 字体配置映射。
- 搜索插件额外索引状态资料卡，结果直接定位对应卡片；更新正文后递增 assets/wiki.js 的搜索 namespace。
- 目录借鉴最后纪元的状态总览、暗黑3的机制条目互链。数值只依据 TopCraft 实现，不移植外部游戏规则。

### 本次发现的实现与说明差异

迟缓与冰缓：技能 lore 和 Aura 文件注释标注 8% 减速，但当前 YAML 只见 Aura、层数、表现与时长管理；在 plugins 的 YAML/JS/JSON/Skript 和 plugin-src Java 搜索中未发现对应移速修改。正文保留技能标注值并明确实际减速幅度待确认，未推定每层线性叠加的实际移速。需游戏内测量或找到运行插件中的实际处理后补定论；此次不修改服务器。

冻结通过 STUN 实现，参加眩晕／沉默共享的连续控制保护；旧正文漏写冻结，已修正。举盾格挡规则来自 ShieldBlockHandler.java 与 plugins/MMOItems/shield-block.yml，和 Aura 护盾分别说明。

通用死亡免疫 YAML 的注释描述“致死时保留 1 点生命”，当前有效语句却是取消受伤事件，设置生命的语句已注释。正文不承诺 1 点生命或触发次数，具体保命规则仍链接相应技能。
