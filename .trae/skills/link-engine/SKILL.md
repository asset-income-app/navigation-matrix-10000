---
name: "link-engine"
description: "链接引擎。自动采集、检查、修复链接。调用时机：链接数据缺失、链接检查、链接修复时。"
---

# 链接引擎

## 功能概述

- 自动采集行业/城市相关链接
- 批量检查链接有效性
- 自动修复失效链接
- 链接质量评估
- 统一链接库管理

## 调用时机

- 新站点需要填充链接
- 定期链接健康检查
- 发现失效链接需要修复
- 扩展站点链接数量

## 核心命令

### 1. 采集链接
```bash
python core-engine/link_engine.py --collect --niche kaoyan
python core-engine/link_engine.py --collect --city beijing
```

### 2. 检查链接
```bash
python core-engine/link_engine.py --check --site beijing
python core-engine/link_engine.py --check --all
```

### 3. 修复链接
```bash
python core-engine/link_engine.py --fix --site beijing
```

### 4. 更新链接库
```bash
python core-engine/link_engine.py --update-library
```

## 链接采集策略

### 城市站链接采集
1. 政府官方网站（gov.cn）
2. 本地服务平台
3. 全国性平台的本地入口
4. 紧急电话号码

### 行业站链接采集
1. 行业官方网站
2. 学习资源平台
3. 工具软件
4. 社区论坛
5. 资讯媒体
6. 搜索引擎入口

### 组合站链接采集
1. 城市本地+行业相关
2. 本地行业服务商
3. 本地行业资讯

## 链接质量评估

| 等级 | 标准 | 处理 |
|------|------|------|
| A级 | 官方网站、知名平台 | 优先收录 |
| B级 | 行业知名网站 | 正常收录 |
| C级 | 一般网站 | 谨慎收录 |
| D级 | 不明网站 | 不收录 |

## 自动修复逻辑

1. 检测到失效链接
2. 从统一链接库查找替代
3. 如果无替代，标记为待补充
4. 更新config.json
5. 重新生成站点

## 统一链接库

`data/master-links.json` 存储所有链接:
```json
{
  "official": [...],
  "platforms": [...],
  "tools": [...],
  "local": [...],
  "emergency": [...]
}
```

## 使用示例

```
用户: 为考研站采集更多链接
AI调用: link-engine技能，运行 link_engine.py --collect --niche kaoyan

用户: 检查所有站点的链接
AI调用: link-engine技能，运行 link_engine.py --check --all

用户: 修复北京站的失效链接
AI调用: link-engine技能，运行 link_engine.py --fix --site beijing
```

## 注意事项

- 采集链接时遵守robots.txt
- 不要过度请求同一域名
- 链接检查分批进行
- 修复后需重新生成站点
