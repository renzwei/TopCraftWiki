# 好友系统更正 · 2026-11-17

用户明确确认实际好友功能使用 PartyAndFriends。此前 Wiki 误把 PlayerProfiles 档案中的旧调用链当成全服好友系统，忽略了已安装的 `PAFInstallOnBungeeCordAndLobbyServers.jar` 与 `plugins/PartyAndFriendsGUI/config.yml`，并据此错误推断好友人数无法推进晋升。此次撤回该结论。

## 实际来源

- GUI 配置：`plugins/PartyAndFriendsGUI/config.yml`，自定义中文语言启用。JAR 的 plugin.yml 标识 PartyAndFriendsGUI 1.0.261-E。
- 快捷栏 ProfileItem 启用，名称“个人资料”，右键打开；AlwaysOpenFriendMenu=false，会恢复上次菜单。底部 FriendItem、FriendRequestItem、SettingsItem 均启用。
- 手持个人资料物品潜行右键玩家可发送或接受已有申请。Wiki 不推荐攻击玩家发送申请，即使该选项也启用。
- 好友列表展示在线/离线与服务器、上次在线；没有 MMOCore 职业等级信息。离线使用骷髅头。四种排序启用。
- FriendAcceptMenu 使用绿色接受、红色拒绝；FriendDetailView 有删除、队伍邀请、前往服务器。ConfirmFriendDeleteMenu.Use=false，因此删除直接生效，旧稿“右键头像后再次确认”错误。
- 好友设置的六项功能均启用，修改后自动关闭菜单。好友系统的社交队伍不代替当前 Wiki 已核对的 MMOCore 冒险队伍与秘境流程。
- GUI 命令配置：friendsgui、friendrequest、friendsettings。`/friend add` 同时来自当前 NoFriendsItem 文案及 JAR 内 config_bungee.yml；未将代理默认申请超时等数值当作服务器当前配置。
- SocialRank 配置明确绑定 `%friendsapi_friendcount%`，注释为总好友数，不含在线筛选与待处理申请。结合用户确认，晋升说明改为 PartyAndFriends 已建立的好友关系；未进行在线服实测。

## 工作范围与更正

用户明确确认服务器正常，任务仅为将 Wiki 的好友介绍改为 PartyAndFriends，不涉及服务器改造、代理目录排查或玩家数据迁移。

上一轮误改的 TopCraftProfileActions 源码、插件 JAR、PlayerProfiles 菜单、MMOCore 命令和命令白名单均已恢复；新增构建脚本与测试已撤回，构建产物移出服务器仓库。原插件通过备份哈希核对。没有启动或重启服务器。

Wiki 保留 PartyAndFriends 的物品入口、好友菜单、申请、设置与备用命令说明，删除依赖上述误改的档案好友入口描述。以后此任务只修改 Wiki，服务器内容仅作为资料读取。

## 官方功能依据

- [PartyAndFriends 作者发布页](https://www.spigotmc.org/resources/9531/)：好友申请、在线状态、所在服务器、好友互动、申请与隐私设置、GUI 入口。页面同时链接 Extended Edition 与作者维护的 Wiki。
- [作者维护的 GUI 配置说明](https://simonsator.de/files/paf-config/1.0.66-GUI/index.php)：菜单与设置选项。按钮名称和当前启用项结合本地中文配置说明，身份好友上限来自用户提供的《玩家社交权限分级》，不当作插件默认值。

## Wiki 范围

重写 social/profile.md；同步修正身份权限、晋升、帮助、菜单指引、按键与命令页。新增申请列表、好友设置及发送申请的命令速查。源索引移除 MMOCore 好友 GUI，加入 PartyAndFriends 配置与 JAR。搜索缓存 namespace 更新为 topcraft-wiki-partyandfriends-v26。

验证：Wiki 检查通过（144 页、8,824 个本地引用、984 项资源），搜索缓存测试通过；浏览器确认好友页九个章节、图标加载和 390 px 无溢出，命令检索出现 friendsgui / friend add / friendrequest / friendsettings。
