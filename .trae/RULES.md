# 导航矩阵统一版 - 开发规则

## 核心铁律

### 1. 源代码管理
- **永远不要直接修改 `02-sites/` 里的任何文件**
- 所有功能、样式、内容修改，**只在 `01-templates/` 或 `core-engine/` 中做**
- 修改完成后，运行 `python core-engine/generate_all.py` 一键重新生成所有站点

### 2. 三维站点体系
- **城市站** (`02-sites/cities/`): 以城市为核心的本地导航
- **行业站** (`02-sites/niches/`): 以垂直行业为核心的专业导航
- **组合站** (`02-sites/hybrids/`): 行业×城市的组合导航

### 3. 配置文件规范
- 所有站点数据存储在 `config.json` 中
- 城市站必须包含: `siteType`, `cityName`, `cityPinyin`, `province`, `categories`
- 行业站必须包含: `siteType`, `nicheName`, `nichePinyin`, `siteTitle`, `siteDescription`, `categories`
- 组合站必须包含: `siteType`, `cityName`, `nicheName`, `categories`
- 每个分类至少5个链接，最多20个链接

### 4. 数据内嵌规范
- HTML必须通过 `window.__SITE_CONFIG__` 内嵌config.json数据
- script.js优先读取内嵌数据，备用fetch config.json
- 确保file://协议下双击index.html可直接打开

### 5. 模板变体规范
- 共5套模板变体: blue/green/orange/purple/dark
- 站点模板分配由 `data/template-assignment.json` 决定
- 同类站点随机分配不同变体，确保视觉多样性
- 所有变体共享base框架，仅CSS变量不同

### 6. 链接收录规则
- 优先收录官方网站，第三方网站仅限知名平台
- 所有链接必须是完整可访问的地址（https://或http://或tel:开头）
- 链接名称要清晰易懂
- 每个站点必须有联系方式: 邮箱931249697@qq.com, QQ 931249697

### 7. 部署规则
- 部署平台: Cloudflare Pages
- 部署前必须备份到 `06-backups/`
- 部署后必须验证站点可正常访问
- 分批部署，每批50个站点

### 8. SEO规则
- 每个站点必须有sitemap.xml和robots.txt
- 每个站点的description必须略有不同
- 不要在同一天提交所有网站
- 每个站点必须有meta标签和Open Graph标签

### 9. 法律合规规则
- 绝对不要上传任何有版权的内容
- 只做官方链接的跳转
- 每个站底部添加免责声明

### 10. 成本控制规则
- 前期不买独立域名，使用Cloudflare Pages免费子域名
- 不买服务器，Cloudflare免费托管
- 所有工作由AI完成

## 互联规则

### 总站与所有站点互联
1. 每个站点底部显示超级总站链接
2. 每个站点顶部显示"导航百科"按钮
3. 超级总站包含所有站点入口
4. 流量闭环: 总站 → 子站 → 总站

### 城市站之间互联
- 同省份城市互相推荐
- 相邻城市互相导流

### 行业站之间互联
- 相关行业互相推荐
- 同一大类下的行业互相导流

### 城市站与行业站互联
- 城市站包含本地相关行业入口
- 行业站包含主要城市入口

## 收费标准

| 服务类型 | 价格 | 说明 |
|----------|------|------|
| 商家收录 | 300元/年 | 分类内任意位置 |
| 分类置顶 | 500元/月 | 分类顶部第一位 |
| 首页推荐 | 2000元/月 | 首页显著位置 |
| 广告位 | 0.3元/天起 | 侧边栏/横幅广告位 |

## 维护规则

### 每日任务（自动）
1. 自动检查所有链接有效性
2. 自动汇总流量数据
3. 自动生成健康报告

### 每周任务（自动）
1. 批量检查失效链接
2. 生成周度健康报告
3. 生成周度收入报告

### 每月任务（人工+自动）
1. 整理月度收入报告
2. 联系潜在广告主
3. 备份所有网站文件

## 文件命名规则

| 文件类型 | 命名规则 | 示例 |
|----------|----------|------|
| 城市文件夹 | 城市拼音 | beijing/ |
| 行业文件夹 | 行业拼音 | kaoyan/ |
| 组合站文件夹 | 行业拼音-城市拼音 | kaoyan-beijing/ |
| 配置文件 | config.json | config.json |
| 页面文件 | index.html | index.html |
| 样式文件 | style.css | style.css |
| 脚本文件 | script.js | script.js |
| 站点地图 | sitemap.xml | sitemap.xml |
| 爬虫规则 | robots.txt | robots.txt |
| 部署配置 | _headers | _headers |
| 备份文件 | YYYY-MM-DD_说明.zip | 2026-06-17_初始版本.zip |
