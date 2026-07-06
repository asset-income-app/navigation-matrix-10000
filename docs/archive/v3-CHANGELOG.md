# 变更日志

## v3.5.0 (2026-06-12) - 联系方式更新与部署完成

### 变更
- 联系方式更新为真实信息：邮箱 931249697@qq.com，QQ号 931249697
- 所有52个站点footer联系方式统一更新
- 城市站footer：商家入驻/合作请联系：931249697@qq.com（QQ: 931249697）
- 导航总站footer：收录申请请联系：931249697@qq.com（QQ: 931249697）

### 部署状态
- 51个城市站已全部部署到Cloudflare Pages（手工拖拽部署）
- 导航总站已部署：https://daohangbaike-nav.pages.dev
- **52个站点矩阵全部上线** ✅
- 部署清单：DEPLOY-LIST.md（按文件夹字母顺序排列）

## v3.4.0 (2026-06-11) - 部署平台切换

### 变更
- 部署平台从Netlify切换到Cloudflare Pages
- 域名格式从 `xxx-nav.netlify.app` 改为 `xxx-nav.pages.dev`
- 配置文件从 `netlify.toml` 改为 `_headers`（Cloudflare专用）
- 部署脚本从 `deploy-all.ps1` 改为 `deploy-cf.ps1`
- CLI工具从 Netlify CLI 改为 Wrangler

### 新增
- `deploy-cf.ps1` - Cloudflare Pages批量部署脚本
- `_headers` 文件生成（Cloudflare安全头配置）
- `sitemap.xml` 和 `robots.txt` 自动生成（域名已更新）

### 优势
- 无限带宽（Netlify仅100GB/月）
- 500次构建/月（Netlify仅300次）
- 300+全球CDN节点
- 内置DDoS防护（免费）
- 国内访问更快（Anycast网络）

## v3.3.0 (2026-06-11) - 数据修正与文档同步

### 修复
- 修正所有文档中的链接数统计：111→114（城市站），5661→5955（总链接）
- 修正generate_mega.py注释：50个→51个城市站
- 修正城市站总链接数：5661→5814

### 变更
- 本地服务分类链接从4条增加到10条（+6条本地政府链接）
- 每站链接数从111增加到114
- 总链接数从5661增加到5955
- 所有文档数据与代码实际输出完全同步

## v3.2.0 (2026-06-11) - 全面体检与文档更新

### 新增
- 15个服务分类（原13个，新增房产家居、金融理财、AI工具）
- HTML内嵌config.json数据（EMBEDDED_CONFIG），直接打开文件即可显示
- 每站7个文件（原4个，新增sitemap.xml/robots.txt/netlify.toml）
- Netlify安全头配置（X-Frame-Options/X-Content-Type-Options/Referrer-Policy）
- 结构化数据（schema.org WebSite）
- 全面体检诊断系统（7维度99.3分）
- CHANGELOG.md变更日志
- FAQ.md常见问题

### 修复
- 修复直接打开HTML文件显示空白的问题（CORS限制）
- 修复导航总站缺少EMBEDDED_CONFIG的问题
- 修复导航总站config.json缺少cityName/cityPinyin/province字段
- 修复导航总站script.js不支持内嵌数据的问题
- 修复分类名不一致问题（生活缴费→生活服务，新闻资讯→新闻媒体）

### 变更
- 每站链接数从94个增加到111个
- 总链接数从4935条增加到5661条
- 每站文件数从4个增加到7个
- 总文件数从228个增加到364个
- 健康度从87.3分（B）提升到99.3分（A+）

## v3.1.0 (2026-06-11) - SEO优化与部署准备

### 新增
- 52个站点sitemap.xml
- 52个站点robots.txt
- 52个站点netlify.toml
- deploy-packages/部署包目录
- deploy-all.ps1批量部署脚本
- deploy-guide.md部署指南

### 变更
- 域名统一为 `{pinyin}-nav.netlify.app`
- management.json更新为51个城市+1总站

## v3.0.0 (2026-06-10) - 项目初始化

### 新增
- 51个城市站完整生成
- 导航总站（导航百科）
- 母版模板
- generate_mega.py一键生成脚本
- 6个技能（central-controller/city-site-manager/batch-updater/link-collector/link-checker/deployer）
- 3个规则文件（RULES.md/AGENTS.md/MCP.md）
- OVERVIEW.md生态系统总览
- README.md项目主文档
- development-guide.md开发指南
- operations-manual.md运营手册
- infrastructure.md配套设施文档
- city-data.md城市数据总表
- management.json管理数据
