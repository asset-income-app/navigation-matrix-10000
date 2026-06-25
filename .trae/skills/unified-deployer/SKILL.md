---
name: "unified-deployer"
description: "统一部署引擎。批量部署站点到Cloudflare Pages。调用时机：需要部署新站点、更新已部署站点、批量上线时。"
---

# 统一部署引擎

## 功能概述

- 批量部署站点到Cloudflare Pages
- 单站部署
- 更新部署
- 域名配置
- 部署验证

## 调用时机

- 新站点生成后需要部署
- 站点更新后需要重新部署
- 批量上线新站点
- 部署配置变更

## 核心命令

### 1. 部署所有站点
```bash
python core-engine/deploy.py --all
```

### 2. 部署指定类型
```bash
python core-engine/deploy.py --type cities
python core-engine/deploy.py --type niches
python core-engine/deploy.py --type hybrids
```

### 3. 部署指定站点
```bash
python core-engine/deploy.py --site beijing
```

### 4. 验证部署
```bash
python core-engine/deploy.py --verify
```

## 部署流程

1. **备份** - 将当前版本备份到 `06-backups/`
2. **准备** - 生成部署清单
3. **部署** - 分批上传到Cloudflare Pages
4. **验证** - 检查每个站点是否可访问
5. **报告** - 生成部署报告

## Cloudflare Pages配置

每个站点的部署配置:
```toml
# _headers
/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
```

## 批量部署策略

- 每批50个站点
- 批次间隔30秒
- 失败自动重试3次
- 部署完成后自动验证

## 使用示例

```
用户: 部署所有城市站
AI调用: unified-deployer技能，运行 deploy.py --type cities

用户: 部署北京站
AI调用: unified-deployer技能，运行 deploy.py --site beijing

用户: 验证所有站点
AI调用: unified-deployer技能，运行 deploy.py --verify
```

## 注意事项

- 部署前必须备份
- 分批部署避免触发限制
- 部署后必须验证
- 记录部署日志到 `05-deployed/deploy-log.json`
