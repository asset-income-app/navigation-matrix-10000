# 常见问题

## 页面显示问题

### Q: 直接打开HTML文件显示空白？
v3版本已修复。HTML内嵌了config.json数据（EMBEDDED_CONFIG变量），直接双击打开index.html即可看到完整内容，无需HTTP服务器。

### Q: 通过HTTP服务器打开页面空白？
检查浏览器控制台（F12）是否有错误。确保所有文件（config.json/index.html/style.css/script.js）在同一目录下。

### Q: 分类展开后没有链接？
检查config.json中对应分类的links数组是否为空。运行 `python generate_mega.py` 重新生成。

## 开发问题

### Q: 如何修改所有网站的底部信息？
修改 `generate_mega.py` 中的 `gen_city_html()` 函数，然后运行 `python generate_mega.py` 重新生成所有站点。

### Q: 如何添加新的服务分类？
1. 在 `generate_mega.py` 的 `gen_city_config()` 函数中添加新分类
2. 运行 `python generate_mega.py` 重新生成
3. 所有51个城市站将自动包含新分类

### Q: 如何更新某个城市的链接？
1. 修改 `generate_mega.py` 中 CITIES 字典的对应城市数据
2. 运行 `python generate_mega.py` 重新生成
3. 或直接修改 `02-city-sites/{city}/config.json`（但需同步更新HTML内嵌数据）

### Q: 修改config.json后页面没变化？
因为HTML内嵌了数据，直接修改config.json不会生效。需要运行 `python generate_mega.py` 重新生成HTML。

### Q: 如何添加新城市？
1. 在 `generate_mega.py` 的 CITIES 字典中添加新城市数据
2. 运行 `python generate_mega.py`
3. 在总站config.json中添加新城市链接
4. 部署新站点

## 部署问题

### Q: Netlify站点名称已被占用？
在名称后加数字，如 `tangshan-nav2`，或使用其他前缀。

### Q: 部署后页面空白？
v3版本已修复此问题（数据内嵌）。如果仍有问题，检查_headers是否正确部署。

### Q: 如何批量部署52个站点？
详见 [deploy-guide.md](deploy-guide.md)，支持手动拖拽、CLI批量、ZIP包三种方式。

### Q: 如何更新已部署的站点？
1. 修改本地文件并重新生成
2. 登录Netlify，进入对应站点
3. 拖拽新文件到部署区域
4. 或使用Wrangler CLI：`npx wrangler pages deploy . --project-name=站点名称`

## 运营问题

### Q: 如何接入百度联盟？
1. 注册 https://union.baidu.com
2. 提交网站审核（需先部署上线）
3. 获取广告代码
4. 在 `gen_city_html()` 中添加广告位
5. 重新生成并部署

### Q: 如何提交搜索引擎？
1. 百度站长平台：https://ziyuan.baidu.com
2. 必应站长工具：https://www.bing.com/webmasters
3. 搜狗站长平台：https://zhanzhang.sogou.com
4. 分3批提交，每周一批

### Q: 链接失效了怎么办？
1. 使用 `link-checker` 技能检查失效链接
2. 使用 `link-collector` 技能收集新链接
3. 更新 `generate_mega.py` 中的 CITIES 数据
4. 重新生成并部署

### Q: 如何添加商家收录？
1. 在对应城市站的config.json中找到目标分类
2. 在links数组中添加商家链接
3. 运行 `python generate_mega.py` 重新生成HTML
4. 部署更新

## 技术问题

### Q: 为什么用纯静态网站而不是WordPress？
- 零成本：Netlify免费托管，WordPress需要服务器
- 零维护：无需更新插件、无需担心安全漏洞
- 高性能：纯静态页面加载极快
- 易扩展：修改模板即可批量更新51个站点

### Q: 为什么HTML内嵌数据而不是用fetch？
- 直接打开文件也能显示（无CORS限制）
- 加载更快（减少一次HTTP请求）
- 离线可用
- fetch作为备用方案，HTTP服务器模式下仍可用

### Q: 项目总成本是多少？
- 域名：0元（使用Netlify子域名）
- 服务器：0元（Netlify免费托管）
- 开发：0元（AI生成代码）
- **总成本：0元**

### Q: 预估月收入多少？
- 启动期（1-3月）：0-500元
- 成长期（4-6月）：500-2000元
- 稳定期（7-12月）：2000-5000元
