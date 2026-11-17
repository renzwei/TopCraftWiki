# 帮助与社交图标调整 · 2026-11-17

## 新增素材

使用内置 image_gen 生成 5 枚透明背景像素图标，存放于 `assets/editorial-icons/`。完整提示词、生成源路径、尺寸和 SHA-256 记录于 `editorial-icons.json`。

- `command-reference.png`：帮助页的常用命令入口。
- `connection-diagnostics.png`：帮助页的连接与显示问题入口。
- `feedback-letter.png`：帮助页的问题反馈入口。
- `party-follow.png`：队伍跟随步骤。
- `rally-point.png`：抵达后集合步骤。

## 原版素材与状态示意

邀请码流程新增复制 `gui/invite/content_code.png`、`content_select.png`，分别替换邀请队伍、添加好友图标。原版文件来源和校验值加入 `social-assets.json`；未修改服务器文件。

交易页“放入物品与金币”使用已有专属装备行囊和原版金币图标组合；“双方确认”使用 CSS 红绿状态示意及文字标签，不宣称是游戏截图。依据 `plugins/TradeMe/config.yml` 的 `Buttons.Confirm`：`Accepted=GREEN_STAINED_GLASS_PANE`，`NotAccepted=RED_STAINED_GLASS_PANE`。颜色之外保留文字，避免只靠颜色区分状态。

菜单教学、资源包排查、实际按钮操作说明、奖励图标及首页指定保留的四个图标均未替换。`.work/install_editorial_icons.py` 是一次性迁移脚本，不重复执行。页面正文为直接维护内容，`scripts/build_social_data.py` 不生成这四页正文。

## 验证

5 张生成图均验证了 RGBA 透明通道。`scripts/check_wiki.py` 检查 143 篇 Markdown、8,786 个本地引用与 984 个原版素材，错误为 0；`git diff --check` 通过。浏览器确认帮助页 3 个入口、邀请码 2 张原版图、跟随 2 张新图正常加载，并检查交易确认文字与手机端横向溢出。

视觉检查发现帮助页的通用按钮选择器会影响侧栏和页头，已使用 `:where(.markdown-section)` 将其限制在正文，保留原有优先级及现代筛选按钮配色。
