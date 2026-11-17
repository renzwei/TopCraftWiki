# UI 入口核对 · 2026-11-17

玩家正文优先描述完整点击路径；未找到完整 UI 路径的功能保留入口命令，进入后继续用按钮操作。帮助中的 26 条命令、筛选与复制功能保留。服务器配置未修改。

## 已核实入口

| 入口 | 依据（相对服务器仓库） |
| --- | --- |
| 背包：个人信息、额外背包、打开技能、职业选择、主菜单 | `plugins/TopCraftEquipmentSlots/config.yml`、`plugin-src/TopCraftEquipmentSlots/TopCraftEquipmentSlots.java` |
| 主菜单：任务手册、生活委托、生活技能、组队大厅、职业流派、服务器公告 | `plugins/zMenu/inventories/main_menu.yml` |
| 技能界面左下角天赋属性、右下角技能树 | `plugins/MMOCore/gui/skill-list.yml` |
| 生活委托的每日任务／每周任务切换 | `plugins/zMenu/inventories/life_quests_daily.yml` |
| 组队大厅 → 我的队伍 → 创建／管理队伍；点击招募直接加入 | `plugin-src/TopCraftPartyRecruitment/TopCraftPartyRecruitment.java` |
| 脱战后潜行右键玩家 → 档案 → 添加好友、邀请队伍、发起交易、赞赏 | `plugins/PlayerProfiles/gui.yml`、`plugin-src/TopCraftProfileActions/` |
| 主城职业 NPC → 制作／收购；奖励 NPC → 礼包 | `plugins/TopCraftProfessionMarket/profession-npcs.yml`、`plugin-src/TopCraftProfessionMarket/ProfessionNpcs.java` |
| 秘境入口 → 秘境征途；备战面板 → 使用钥匙／开始挑战 | `plugin-src/topcraft-dungeon-keys/` |

## 仍需命令的入口

- `/修复`：未找到已连接的修理 NPC 或菜单按钮。森林修理相关对白不能视为实际修复入口。
- `/invite`：打开邀请好友界面；后续选择邀请人、输入邀请码、确认绑定通过界面操作。
- `/mmocore:friends`：打开好友列表。其他玩家档案只有添加好友；好友列表按钮属于自己的档案，尚未找到无需命令打开自己档案的完整路径。背包“个人信息”打开的是 zMenu 角色详情，不是 PlayerProfiles。
- `/obsidian`：打开秘境入口；没有把计划中的 NPC 写成已上线入口。
- `/tcdungeon panel`：进入秘境后打开备战面板。手持钥匙右键使用仅在已准备的副本内生效，不代替入场步骤。
- `/dungeonkey reclaim`：补领已有绑定钥匙，未找到 UI 按钮。

## 维护范围

同步正文、首页快捷入口、背包／主菜单交互说明和帮助中的点击路径。`scripts/build_life.py` 同步维护生活职业总览、委托和修理文案，避免重新生成后恢复命令优先的说明。`.work/ui_first.py` 与 `.work/finish_ui_first.py` 为一次性迁移脚本，不重复执行。全站搜索命名空间更新为 `topcraft-wiki-ui-entrypoints-v22`。

## 验证

`scripts/check_wiki.py` 检查 143 篇 Markdown、8,786 个本地引用和 982 个原版资源，错误为 0。`assets/guide.js`、`assets/wiki.js` 通过 Node 语法检查，`git diff --check` 通过。浏览器验证背包“打开技能”、主菜单“职业流派／组队大厅”的说明、桌面与 390px 手机宽度、帮助的分类筛选及复制 `/skills`。命令速查仍有 26 项。
