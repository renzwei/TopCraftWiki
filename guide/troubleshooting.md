<p class="eyebrow">TOPCRAFT / 帮助</p>

# 连接与显示问题

<p class="lead">先找到屏幕上出现的情况，再按顺序处理。TopCraft 使用 Minecraft Java 版 1.21，服务器地址为 topcraft.cc。</p>

<div class="help-notice">无法进入游戏时，保留断开连接界面的完整提示。能够进入游戏时，点击<strong>背包 → 主菜单 → 服务器公告</strong>查看通知。</div>

## 无法连接服务器

<section class="help-symptom"><h3>提示版本不兼容</h3><ol><li>退出到启动器，确认启动的是 Minecraft <strong>Java 版 1.21</strong>。</li><li>重新启动游戏，在多人游戏列表连接 <code>topcraft.cc</code>。</li></ol><p><strong>处理后：</strong>应不再出现版本不匹配提示。如果仍然出现，保存提示中的客户端和服务器版本文字。</p></section>

<section class="help-symptom"><h3>未知主机、连接超时或连接被拒绝</h3><ol><li>编辑服务器条目，核对地址为 <code>topcraft.cc</code>，没有多余空格、中文标点或 <code>https://</code>。</li><li>确认电脑可以正常联网，再返回服务器列表刷新并重试。</li><li>如果其他网络服务正常，仍无法连接，保留失败提示和发生时间，稍后再试。</li></ol><p><strong>处理后：</strong>应能进入连接或资源包加载阶段。超时也可能与服务器暂时不可用有关，不能仅凭这一条提示判断原因；持续失败时，按<a href="#/guide/feedback">连接问题模板</a>记录信息。</p></section>

## 资源包下载或加载失败

<section class="help-symptom"><h3>曾拒绝资源包，或进入时没有接受下载</h3><ol><li>回到“多人游戏”，选中 TopCraft，点击“编辑”。</li><li>将“服务器资源包”设为“启用”，保存后重新连接。</li><li>如出现下载确认，接受并等待加载完成。</li></ol><p><strong>处理后：</strong>进入世界后，背包应显示自定义按钮和背景。拒绝资源包可能导致连接中断。</p></section>

<section class="help-symptom"><h3>下载失败、加载失败，或加载时断开</h3><ol><li>保存完整提示，区分是在下载过程中失败，还是下载后加载失败。</li><li>退出到服务器列表，确认网络正常并重新连接。</li><li>仍失败时，记录客户端版本、失败阶段和发生时间；如装有模组或其他资源包，也一并记录。</li></ol><p><strong>处理后：</strong>应完成加载并进入世界。持续失败时使用<a href="#/guide/feedback">连接问题模板</a>保存信息；无需为排查这一步删除存档或重装整个游戏。</p></section>

## 图标或菜单显示异常

<div class="help-example"><img class="help-icon" src="assets/server/guide/inventory-backpack.png" alt="游戏内额外背包图标"><img class="help-icon" src="assets/server/guide/inventory-skills.png" alt="游戏内技能图标"><img class="help-icon" src="assets/server/guide/inventory-class_select.png" alt="游戏内职业选择图标"><p>背包中使用的实际图标：额外背包、技能、职业选择。可对照它们确认资源包是否显示正常。</p></div>

<section class="help-symptom"><h3>图标变成方框、菜单背景缺失或物品变成普通纸张</h3><ol><li>先按上方步骤启用服务器资源包，并等待加载完成。</li><li>若启用了其他界面或字体资源包，暂时停用这些资源包后重新连接。</li><li>重新打开同一个界面，对比图标和背景是否恢复。</li></ol><p><strong>处理后：</strong>图标应恢复为对应图案，菜单背景正常显示。如果仍异常，截取整个界面，记录界面名称、客户端版本和使用中的模组、资源包。</p></section>

<section class="help-symptom"><h3>只有一件物品或一个图标异常</h3><p>先查看背包中的其他自定义图标是否正常。如果其他内容正常，记录异常物品的完整名称、所在界面，以及手持、背包内等不同位置的显示情况。使用<a href="#/guide/feedback">显示问题模板</a>附上截图。</p><p><strong>判断方法：</strong>同一件物品在不同位置的截图，能帮助区分物品外观问题与整个界面的显示问题。</p></section>

## 技能栏为空或显示警示

<p>技能栏的空槽、冷却遮罩和法力警示各有含义。先对照<a href="#/guide/interface?id=技能栏的四种状态">技能栏的四种状态</a>查看当前显示。</p>

| 看到的情况 | 处理方法 | 正常结果 |
| --- | --- | --- |
| 某个槽位显示“未装配” | 点击<strong>背包 → 打开技能</strong>，选中技能，再左键点击下方槽位。 | 该槽位出现已绑定技能的图标。 |
| 图标有倒计时或遮罩 | 等待技能冷却结束。 | 冷却结束后恢复就绪显示。 |
| 法力警示 | 等待法力恢复，达到该技能消耗。 | 法力足够时警示解除。 |
| 图标正常，按键却没有反应 | 对照[基本操作](guide/controls.md)检查对应动作按键与潜行组合；查看是否处于控制状态。 | 满足施放条件后，使用对应动作可施放技能。 |

## 仍然没有解决

记录出现问题的时间、完整提示和已经尝试的方法。显示问题尽量保留整个界面的截图，包含物品提示或技能栏；连接问题保留断开连接画面。

<strong>反馈入口待公布。</strong> 可先在[问题反馈](guide/feedback.md)复制模板并保存记录。

<nav class="guide-nav"><a href="#/guide/join">加入游戏与资源包</a><a href="#/guide/help">帮助与常见问题</a><a href="#/guide/feedback">问题反馈</a></nav>

<div class="page-end">TopCraft 玩家手册 · 更新于 2026-11-17</div>
