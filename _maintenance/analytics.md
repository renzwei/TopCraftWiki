# Google Analytics 4

衡量 ID：`G-GGTHGX9V8E`。通过 `assets/analytics.js` 直接加载 Google tag，数据由 Google Analytics 保存。没有引入独立统计后端，也没有同时加载 `GTM-PZVBTNM9`。

## 发布前的后台设置

在 Google Analytics → 管理 → 数据流 → 本网站数据流 → 增强型衡量的齿轮 → 网页浏览 → 显示高级设置，关闭“基于浏览器历史记录事件的网页更改”，然后保存。页面代码使用 `send_page_view: false` 并在 Docsify 正文加载后手动发送页面浏览；增强型衡量的历史事件开关独立于此参数，必须在后台关闭才能避免重复。

发布 Wiki 后，打开 `https://wiki.topcraft.cc` 并切换不同文章，在 GA 的实时报告或 Tag Assistant 中检查数据。这里只完成代码接入，本地测试不会向正式媒体资源发送事件；需要发布后确认真实数据接收情况。尚未修改或验证 Google 账号中的设置。

## 统计口径

- `page_view`：首屏加载、刷新、切换文章、返回其他文章各一次。文章内目录锚点、重复挂载、计算器与技能树操作不重复计数。未列入 `assets/search-paths.js` 的路径不统计。
- `page_title` 为实际文章标题；`page_location` 包含规范化的 `#/文章路径`，排除目录锚点和查询参数。首次来源保留域名与路径，后续来源为前一篇文章。
- `wiki_path` 为文章路径，建议在“管理 → 自定义定义”中注册为事件范围的自定义维度，方便按路径筛选。普通页面热度也可按页面标题查看。
- `search_no_results`：完整搜索索引就绪、无结果且输入停顿 1.5 秒时记录，包含 `search_term` 和 `wiki_path`。同次文章访问中同词不重复；忽略单字、超过 80 字、邮箱、网址与长号码。建议将 `search_term` 注册为事件范围的自定义维度，用于查看内容缺口。
- 访客、会话、每日趋势与页面热度由 GA4 后台汇总。媒体资源报告时区请设为香港。
- 仅正式 HTTPS 域名 `wiki.topcraft.cc` 加载 Google 脚本；localhost、预览地址与其他域名不发送统计。Google 脚本被阻止时不影响 Wiki 加载。未在 Wiki 页面显示公开访问计数。

账号密码、API 密钥或管理员令牌均不需要放入仓库。衡量 ID 是公开的网站接入标识。

## 验证

`node scripts/check_analytics.cjs` 检查域名限制、脚本加载、规范路由、锚点去重、返回页面、无结果搜索、敏感格式排除与标题/来源参数。`scripts/check_search.cjs` 验证原搜索逻辑。

依据：[Google 页面浏览统计](https://developers.google.com/analytics/devguides/collection/ga4/views)、[Google tag 接入](https://developers.google.com/tag-platform/gtagjs)。使用兼容的 `gtag.js` + config 接入方式，配合手动 page_view；不要再通过另一个容器向同一媒体资源重复发送。
