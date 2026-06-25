---
name: "seo-optimizer"
description: "SEO优化引擎。优化站点SEO、管理搜索引擎提交、生成sitemap。调用时机：SEO优化、搜索引擎提交、meta标签优化时。"
---

# SEO优化引擎

## 功能概述

- 自动生成sitemap.xml和robots.txt
- 优化meta标签和Open Graph
- 管理搜索引擎提交
- 关键词优化
- SEO健康检查

## 调用时机

- 新站点上线前SEO优化
- 定期SEO维护
- 搜索引擎提交
- SEO问题诊断

## 核心命令

### 1. SEO优化单站
```bash
python core-engine/seo_optimizer.py --optimize --site beijing
```

### 2. 批量SEO优化
```bash
python core-engine/seo_optimizer.py --optimize --all
```

### 3. 生成sitemap
```bash
python core-engine/seo_optimizer.py --sitemap --all
```

### 4. SEO健康检查
```bash
python core-engine/seo_optimizer.py --audit --all
```

### 5. 生成提交计划
```bash
python core-engine/seo_optimizer.py --submit-plan
```

## SEO优化项目

### Meta标签优化
```html
<title>{站点标题} - 关键词1 关键词2</title>
<meta name="description" content="{独特描述}">
<meta name="keywords" content="{关键词列表}">
<meta property="og:title" content="{标题}">
<meta property="og:description" content="{描述}">
<meta property="og:type" content="website">
```

### Sitemap生成
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{站点URL}</loc>
    <lastmod>{更新日期}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

### Robots.txt
```
User-agent: *
Allow: /
Sitemap: {站点URL}/sitemap.xml
```

## 搜索引擎提交策略

| 搜索引擎 | 提交方式 | 频率 |
|----------|----------|------|
| 百度 | 站长平台提交 | 每周一批 |
| 必应 | 站长工具提交 | 每周一批 |
| 搜狗 | 站长平台提交 | 每月一批 |
| Google | Search Console | 每周一批 |

## SEO差异化策略

- 每个站点的title略有不同
- description必须独特
- 关键词根据城市/行业定制
- 避免内容完全重复

## 使用示例

```
用户: 优化所有站点的SEO
AI调用: seo-optimizer技能，运行 seo_optimizer.py --optimize --all

用户: 生成提交计划
AI调用: seo-optimizer技能，运行 seo_optimizer.py --submit-plan

用户: 检查SEO问题
AI调用: seo-optimizer技能，运行 seo_optimizer.py --audit --all
```

## 注意事项

- 不要同一天提交所有站点
- 每个站点description必须不同
- sitemap更新后需重新部署
- 提交前确保站点可访问
