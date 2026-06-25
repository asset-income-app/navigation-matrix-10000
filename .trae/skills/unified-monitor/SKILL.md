---
name: "unified-monitor"
description: "统一监控引擎。自动检查所有站点健康状态、链接有效性，生成健康报告。调用时机：定期维护、健康检查、自动修复时。"
---

# 统一监控引擎

## 功能概述

- 自动检查所有站点可访问性
- 批量检查链接有效性
- 生成健康报告（HTML可视化）
- 自动修复失效链接
- 监控站点性能

## 调用时机

- 每日自动健康检查
- 用户要求检查站点状态
- 部署后验证
- 定期维护

## 核心命令

### 1. 全量健康检查
```bash
python core-engine/monitor.py --check-all
```

### 2. 检查指定站点
```bash
python core-engine/monitor.py --check-site beijing
```

### 3. 检查链接有效性
```bash
python core-engine/monitor.py --check-links
```

### 4. 生成健康报告
```bash
python core-engine/monitor.py --report
```

### 5. 自动修复
```bash
python core-engine/monitor.py --auto-fix
```

## 健康检查项目

| 检查项 | 说明 | 健康标准 |
|--------|------|----------|
| 站点可访问 | HTTP状态码 | 200 |
| HTML完整性 | 包含必要元素 | 通过 |
| 配置数据 | 内嵌数据完整 | 通过 |
| 链接有效性 | URL可访问 | 95%+有效 |
| SEO文件 | sitemap/robots存在 | 通过 |
| 响应速度 | 页面加载时间 | <3秒 |

## 健康报告

报告生成在 `04-monitor/health-report.html`，包含:
- 总体健康度评分
- 各站点状态列表
- 失效链接清单
- 修复建议
- 趋势图表

## 自动修复逻辑

1. 发现失效链接 → 标记为待修复
2. 查找替代链接 → 从链接库中寻找
3. 更新config.json → 重新生成站点
4. 记录修复日志

## 使用示例

```
用户: 检查所有站点健康状态
AI调用: unified-monitor技能，运行 monitor.py --check-all

用户: 生成健康报告
AI调用: unified-monitor技能，运行 monitor.py --report

用户: 自动修复问题
AI调用: unified-monitor技能，运行 monitor.py --auto-fix
```

## 注意事项

- 链接检查可能耗时较长，建议分批
- 自动修复前先备份
- 健康报告自动更新到 `04-monitor/`
- 严重问题需通知用户确认
