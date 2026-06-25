# 导航矩阵统一版 - 智能体配置

## 智能体架构（32个AI员工）

本项目采用分层智能体架构，实现全自动化的万站矩阵管理：

```
┌─────────────────────────────────────────────────────────────────┐
│                    核心管理层 (5个)                               │
│  unified-generator  - 万站生成引擎                               │
│  unified-deployer   - 统一部署引擎                               │
│  unified-monitor    - 健康监控引擎                               │
│  site-manager       - 站点管理器                                 │
│  scheduler          - 任务调度器                                 │
└─────────────────────────────────────────────────────────────────┘
                    ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                    扩展生成层 (3个)                               │
│  city-expander      - 城市扩展器 (52→333)                        │
│  niche-expander     - 行业扩展器 (100→500)                       │
│  hybrid-generator   - 组合站生成器 (→万级)                       │
└─────────────────────────────────────────────────────────────────┘
                    ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                    自动运维层 (3个)                               │
│  auto-backup        - 自动备份器                                 │
│  auto-repair        - 自动修复器                                 │
│  performance-optimizer - 性能优化器                              │
└─────────────────────────────────────────────────────────────────┘
                    ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                    变现管理层 (4个)                               │
│  ad-manager         - 广告管理器                                 │
│  merchant-manager   - 商家收录管理器                             │
│  affiliate-manager  - 联盟返佣管理器                             │
│  revenue-tracker    - 收入追踪引擎                               │
└─────────────────────────────────────────────────────────────────┘
                    ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                    数据分析层 (4个)                               │
│  traffic-analyzer   - 流量分析器                                 │
│  revenue-analyzer   - 收入分析器                                 │
│  seo-analyzer       - SEO分析器                                  │
│  competitor-spy     - 竞品监控器                                 │
└─────────────────────────────────────────────────────────────────┘
                    ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                    内容优化层 (4个)                               │
│  link-engine        - 链接引擎                                   │
│  seo-optimizer      - SEO优化引擎                                │
│  content-generator  - 内容生成器                                 │
│  keyword-optimizer  - 关键词优化器                               │
│  batch-cleaner      - 批量清理器                                 │
└─────────────────────────────────────────────────────────────────┘
                    ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                    用户服务层 (3个)                               │
│  customer-service   - 客服助手                                   │
│  feedback-collector - 反馈收集器                                 │
│  domain-manager     - 域名管理器                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 27个AI员工职责表

| 编号 | 技能名称 | 职责 | 自动化程度 |
|------|----------|------|------------|
| 1 | unified-generator | 万站生成总指挥 | 手动触发 |
| 2 | unified-deployer | 批量部署执行 | 手动触发 |
| 3 | unified-monitor | 健康状态监控 | 自动运行 |
| 4 | site-manager | 单站点管理 | 手动触发 |
| 5 | scheduler | 任务调度中心 | 自动运行 |
| 6 | city-expander | 城市站扩展 | 手动触发 |
| 7 | niche-expander | 行业站扩展 | 手动触发 |
| 8 | hybrid-generator | 组合站生成 | 手动触发 |
| 9 | auto-backup | 数据备份 | 自动运行 |
| 10 | auto-repair | 问题修复 | 自动运行 |
| 11 | performance-optimizer | 性能优化 | 自动运行 |
| 12 | ad-manager | 广告管理 | 手动触发 |
| 13 | merchant-manager | 商家收录 | 手动触发 |
| 14 | affiliate-manager | 联盟返佣 | 手动触发 |
| 15 | revenue-tracker | 收入统计 | 自动运行 |
| 16 | traffic-analyzer | 流量分析 | 自动运行 |
| 17 | revenue-analyzer | 收入分析 | 自动运行 |
| 18 | seo-analyzer | SEO分析 | 自动运行 |
| 19 | competitor-spy | 竞品监控 | 自动运行 |
| 20 | link-engine | 链接采集检查 | 可自动 |
| 21 | seo-optimizer | SEO优化 | 可自动 |
| 22 | content-generator | 内容生成 | 手动触发 |
| 23 | keyword-optimizer | 关键词优化 | 手动触发 |
| 24 | batch-cleaner | 数据清理 | 手动触发 |
| 25 | customer-service | 客服支持 | 手动触发 |
| 26 | feedback-collector | 反馈收集 | 自动运行 |
| 27 | domain-manager | 域名管理 | 手动触发 |

## 自动化任务清单

### 全自动任务（无需人工干预）
| 任务 | 执行者 | 频率 |
|------|--------|------|
| 健康检查 | unified-monitor | 每日 |
| 数据备份 | auto-backup | 每日 |
| 收入统计 | revenue-tracker | 每日 |
| 流量分析 | traffic-analyzer | 每日 |
| SEO检查 | seo-analyzer | 每周 |
| 竞品监控 | competitor-spy | 每周 |
| 反馈收集 | feedback-collector | 实时 |
| 问题修复 | auto-repair | 发现问题时 |

### 半自动任务（需确认后执行）
| 任务 | 执行者 | 触发条件 |
|------|--------|----------|
| 城市扩展 | city-expander | 用户请求 |
| 行业扩展 | niche-expander | 用户请求 |
| 组合生成 | hybrid-generator | 用户请求 |
| 商家收录 | merchant-manager | 收款确认 |
| 广告添加 | ad-manager | 用户请求 |
| 移动端优化 | mobile-optimizer | 用户请求 |
| 社交推广 | social-promoter | 用户请求 |

## 智能体协作流程

### 扩展流程
```
用户: 扩展城市站到333个
→ scheduler 调度
→ city-expander 获取城市数据
→ unified-generator 批量生成
→ auto-backup 备份
→ unified-deployer 部署
→ unified-monitor 验证
→ 完成报告
```

### 商家收录流程
```
商家付款 → merchant-manager 审核
→ site-manager 添加链接
→ revenue-tracker 记录收入
→ unified-generator 重新生成
→ unified-deployer 部署
→ customer-service 通知商家
```

### 自动维护流程
```
每日定时 → scheduler 触发
→ unified-monitor 检查健康
→ auto-repair 修复问题
→ link-engine 检查链接
→ seo-analyzer SEO检查
→ revenue-tracker 统计收入
→ traffic-analyzer 流量分析
→ 生成日报
```

## 技能配置文件位置

所有技能配置在 `.trae/skills/{技能名}/SKILL.md`