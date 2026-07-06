# 变更日志

## v4.1.0 (2026-07-06) - 新电脑迁移与环境恢复

### 环境恢复
- Git 2.54.0 安装到 D:\Git（避开C盘）
- Node.js v24.18.0 安装到 D:\NodeJS
- Python 3.12.10 保持原有位置
- Wrangler 4.107.0（Cloudflare部署工具）
- SSH密钥重新生成（ed25519，邮箱931249697@qq.com）
- PATH环境变量已修复，所有工具可用

### 项目清理
- 删除空目录：06-backups, .wrangler/tmp, data/backups/*, data/logs/*
- 删除临时目录：temp-batch1-5, temp-deploy
- 删除异常目录：`linyi上传到此`（含中文名，导致配置错误）
- 删除旧Git安装包：Git-2.45.0-64-bit.exe

### 文档整理
- 创建统一docs目录结构：docs/archive, docs/reports, docs/guides
- 移动根目录旧文档到 docs/archive（50.md, 技术文档.md等）
- 移动v3/v1项目文档到 docs/archive（带v3-/v1-前缀）
- 移动unified根目录报告文件到 docs/reports（13个MD文件）
- CHANGELOG.md移至docs目录

### 当前统计
- 总站点数：9998个（城市站292个 + 行业站500个 + 混合站9206个）
- 文档已全面整理，项目结构统一

### 待办
- GitHub SSH连接需用户手动添加公钥到GitHub账户
- SSH公钥：`ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKHfnbzK0TucU1ScgxQejFLixRWCku7Ek6uOAOjufGpN 931249697@qq.com`

## v4.0.0 (2026-07-06) - 完全融合与万站生成

### 新增
- 项目完全融合：navigation-matrix-v3 (52个城市站) + vertical-navigation-matrix-v1 (100个行业站)
- 城市站扩展到293个（覆盖全国地级市）
- 行业站扩展到500个（覆盖各类垂直领域）
- 万站生成引擎 `core-engine/generate_all.py`（Python版）
- 万站生成引擎 `core-engine/generate_all.ps1`（PowerShell版）
- 5套模板变体系统（blue/green/orange/purple/dark）
- 每个站点7个文件：index.html, style.css, script.js, config.json, sitemap.xml, robots.txt, _headers
- 超级总站 `03-central-hub/index.html`（含793个站点链接）
- 健康监控报告 `04-monitor/health-report.html`
- 收入仪表盘 `04-monitor/revenue-dashboard.html`
- 200+个技能（AI员工）全部创建完成
- 统一数据层：`data/cities.json`, `data/niches.json`, `data/master-links.json`

### 变更
- 部署平台：Netlify → Cloudflare Pages
- 域名格式：`xxx-nav.netlify.app` → `xxx-nav.pages.dev`
- 配置文件：`netlify.toml` → `_headers`（Cloudflare安全头）
- 联系方式统一为：邮箱 931249697@qq.com，QQ号 931249697

### 统计
- 总站点数：793个（城市站293个 + 行业站500个）
- 总分类数：约61,000个
- 总链接数：约185,000条
- 模板分配：variant-orange(162), variant-green(187), variant-purple(150), variant-blue(135), variant-dark(159)
- 技能数：200+个

## v3.5.0 (2026-06-12) - 联系方式更新与部署完成

### 变更
- 联系方式更新为真实信息：邮箱 931249697@qq.com，QQ号 931249697
- 所有52个站点footer联系方式统一更新
- 城市站footer：商家入驻/合作请联系：931249697@qq.com（QQ: 931249697）
- 导航总站footer：收录申请请联系：931249697@qq.com（QQ: 931249697）

### 部署状态
- 51个城市站已全部部署到Cloudflare Pages（手工拖拽部署）
- 导航总站已部署：https://daohangbaike-nav.pages.dev
- 52个站点矩阵全部上线 ✅

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