---
name: "unified-generator"
description: "万站矩阵统一生成引擎。一键生成城市站、行业站、组合站。调用时机：需要批量生成新站点、扩展站点矩阵、全局重新生成时。"
---

# 统一生成引擎

## 功能概述

一键生成整个导航矩阵的所有站点：
- 批量生成城市站（333个地级市）
- 批量生成行业站（500个垂直行业）
- 批量生成组合站（行业×城市）
- 随机分配模板变体确保多样性
- 自动内嵌配置数据到HTML

## 调用时机

- 用户需要批量生成新站点
- 需要扩展站点矩阵到更多城市/行业
- 需要全局重新生成所有站点
- 添加新模板变体后重新生成

## 核心命令

### 1. 生成所有站点
```bash
python core-engine/generate_all.py
```

### 2. 只生成城市站
```bash
python core-engine/generate_all.py --type cities
```

### 3. 只生成行业站
```bash
python core-engine/generate_all.py --type niches
```

### 4. 只生成组合站
```bash
python core-engine/generate_all.py --type hybrids
```

### 5. 生成指定站点
```bash
python core-engine/generate_all.py --site beijing
python core-engine/generate_all.py --site kaoyan
```

## 工作流程

1. 读取 `data/cities.json` 获取城市列表
2. 读取 `data/niches.json` 获取行业列表
3. 读取 `data/template-assignment.json` 获取模板分配
4. 读取 `01-templates/` 获取模板文件
5. 为每个站点:
   - 读取对应 `config.json`
   - 随机选择模板变体
   - 将config数据内嵌到HTML
   - 生成7个文件(index.html, style.css, script.js, config.json, sitemap.xml, robots.txt, _headers)
6. 生成超级总站
7. 生成管理数据 `05-deployed/management.json`
8. 输出生成报告

## 模板变体分配逻辑

```python
variants = ['variant-blue', 'variant-green', 'variant-orange', 'variant-purple', 'variant-dark']
# 基于站点名称hash分配，确保同一站点每次生成使用相同变体
variant = variants[hash(site_name) % len(variants)]
```

## 使用示例

```
用户: 生成所有城市站
AI调用: unified-generator技能，运行 generate_all.py --type cities

用户: 添加北京考研导航站
AI调用: unified-generator技能，创建组合站配置并生成

用户: 重新生成所有站点
AI调用: unified-generator技能，运行 generate_all.py
```

## 注意事项

- 生成前确保 `data/` 目录数据完整
- 生成后会覆盖 `02-sites/` 中的现有文件
- 大规模生成建议分批进行
- 生成后需运行 unified-deployer 部署
