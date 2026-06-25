---
name: "revenue-tracker"
description: "收入追踪引擎。统计广告收入、商家收录收入、返佣收入，生成收入报告。调用时机：收入统计、商家收款、收入分析时。"
---

# 收入追踪引擎

## 功能概述

- 统计广告联盟收入
- 记录商家收录收入
- 追踪联盟返佣收入
- 生成收入报告（HTML可视化）
- 收入趋势分析

## 调用时机

- 商家付费收录时记录
- 每日/每月收入汇总
- 用户查看收入数据
- 收入异常分析

## 核心命令

### 1. 记录收入
```bash
python core-engine/revenue_tracker.py --record --type listing --site beijing --amount 300
```

### 2. 生成日报
```bash
python core-engine/revenue_tracker.py --report --daily
```

### 3. 生成月报
```bash
python core-engine/revenue_tracker.py --report --monthly
```

### 4. 收入汇总
```bash
python core-engine/revenue_tracker.py --summary
```

## 收入类型

| 类型 | 说明 | 记录方式 |
|------|------|----------|
| ad | 广告联盟收入 | 自动同步 |
| listing | 商家收录 | 手动记录 |
| pin | 分类置顶 | 手动记录 |
| affiliate | 联盟返佣 | 自动同步 |
| banner | 广告位 | 手动记录 |

## 收入数据结构

```json
{
  "date": "2026-06-17",
  "records": [
    {
      "type": "listing",
      "site": "beijing",
      "category": "教育考试",
      "merchant": "学而思",
      "amount": 300,
      "period": "year",
      "notes": "年费收录"
    }
  ],
  "dailyTotal": 300,
  "monthlyTotal": 3000
}
```

## 收入报告

报告生成在 `04-monitor/revenue-dashboard.html`，包含:
- 今日/本月/本年收入汇总
- 各站点收入排行
- 收入类型分布
- 收入趋势图
- 待收款清单

## 收费标准

| 服务 | 价格 |
|------|------|
| 商家收录 | 300元/年 |
| 分类置顶 | 500元/月 |
| 首页推荐 | 2000元/月 |
| 广告位 | 0.3元/天起 |

## 使用示例

```
用户: 记录北京站学而思收录收入300元
AI调用: revenue-tracker技能，记录到收入系统

用户: 查看本月收入
AI调用: revenue-tracker技能，生成月度报告

用户: 生成收入仪表盘
AI调用: revenue-tracker技能，生成 revenue-dashboard.html
```

## 注意事项

- 收入数据每日备份
- 付费收录需验证付款后再记录
- 收入报告自动生成
- 敏感财务数据不公开
