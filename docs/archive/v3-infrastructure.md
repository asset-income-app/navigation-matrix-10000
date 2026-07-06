# 配套设施文档

> 6个技能 · 3个规则文件 · 1个管理数据 · 7个文档 · MCP连接

## 技能系统

### 技能清单

| 技能名称 | 层级 | 功能 | 调用时机 |
|----------|------|------|----------|
| central-controller | 中央层 | 总站管理、全局协调 | 总站操作、全局查看 |
| city-site-manager | 城市层 | 单站管理、本地运营 | 单城市操作 |
| batch-updater | 批量层 | 批量更新、功能同步 | 批量修改请求 |
| deployer | 批量层 | 部署管理、域名配置 | 部署请求 |
| link-collector | 辅助层 | 链接收集、数据填充 | 链接数据缺失 |
| link-checker | 辅助层 | 链接检查、健康报告 | 定期维护 |

### 技能详细说明

#### central-controller（中央控制器）
- **位置**: `.trae/skills/central-controller/SKILL.md`
- **功能**: 总站管理、全局协调、数据汇总、收录审核
- **调用场景**: 查看全局数据、总站操作、跨站协调
- **依赖**: 可调用所有其他技能

#### city-site-manager（城市站管理器）
- **位置**: `.trae/skills/city-site-manager/SKILL.md`
- **功能**: 单站管理、本地链接维护、商家收录、本地推广
- **调用场景**: 单城市操作、链接更新、商家添加
- **依赖**: link-collector、deployer

#### batch-updater（批量更新器）
- **位置**: `.trae/skills/batch-updater/SKILL.md`
- **功能**: 批量更新模板、功能同步、样式统一、广告位添加
- **调用场景**: 批量修改、功能升级、样式调整
- **依赖**: generate_mega.py

#### deployer（部署器）
- **位置**: `.trae/skills/deployer/SKILL.md`
- **功能**: 批量部署、单站部署、更新部署、域名配置
- **调用场景**: 部署新站、更新部署、域名管理
- **依赖**: Netlify CLI

#### link-collector（链接收集器）
- **位置**: `.trae/skills/link-collector/SKILL.md`
- **功能**: 自动收集城市官方网站链接、数据填充
- **调用场景**: 新城市添加、链接补充
- **依赖**: 无

#### link-checker（链接检查器）
- **位置**: `.trae/skills/link-checker/SKILL.md`
- **功能**: 批量检查链接有效性、生成健康报告
- **调用场景**: 定期维护、链接更新
- **依赖**: 无

## 规则文件

### RULES.md（开发规则）
- **位置**: `.trae/RULES.md`
- **内容**: 核心铁律、配置规范、数据内嵌规范、链接收录规则、技能调用规则、部署规则、SEO规则、法律合规、成本控制、维护规则、文件命名规则、错误处理
- **关键规则**:
  - 永远不要直接修改 `02-city-sites/`
  - 每个城市站包含15个分类
  - HTML必须内嵌EMBEDDED_CONFIG
  - 每站7个文件（含sitemap.xml/robots.txt/_headers）

### AGENTS.md（智能体配置）
- **位置**: `.trae/AGENTS.md`
- **内容**: 智能体架构、协作流程、触发条件、自动化建议、通信协议
- **架构**: 中央总站 → 批量管理 → 城市站群 → 辅助智能体

### MCP.md（外部连接配置）
- **位置**: `.trae/MCP.md`
- **内容**: MCP服务器配置、工具列表、使用说明
- **已接入**: Airbnb MCP（旅游数据）
- **待接入**: 百度统计、Netlify、百度联盟

## 管理数据

### management.json
- **位置**: `04-deployed/management.json`
- **内容**: 所有站点的基础信息、部署状态、健康度
- **结构**:
```json
{
  "version": "3.2",
  "lastUpdate": "2026-06-11",
  "totalSites": 52,
  "cities": [
    {
      "name": "唐山",
      "pinyin": "tangshan",
      "province": "河北",
      "domain": "tangshan-nav.pages.dev",
      "status": "deployed",
      "links": 114,
      "categories": 15,
      "files": 7
    }
  ],
  "master": {
    "name": "导航百科",
    "domain": "daohangbaike-nav.pages.dev",
    "status": "deployed",
    "links": 141,
    "categories": 28
  }
}
```

## 文档体系

### 文档清单

| 文档 | 位置 | 用途 |
|------|------|------|
| README.md | 项目根目录 | 项目主文档，用户和开发者入口 |
| development-guide.md | docs/ | 开发指南，技术架构和开发流程 |
| operations-manual.md | docs/ | 运营手册，流量和收入策略 |
| infrastructure.md | docs/ | 配套设施文档，技能和工具说明 |
| city-data.md | docs/ | 城市站数据总表，51个城市详情 |
| deploy-guide.md | docs/ | 部署指南，Netlify部署步骤 |
| CHANGELOG.md | docs/ | 变更日志，版本迭代记录 |
| FAQ.md | docs/ | 常见问题，快速解答 |
| OVERVIEW.md | .trae/ | 生态系统总览，架构图和互联机制 |
| RULES.md | .trae/ | 开发规则，核心铁律 |
| AGENTS.md | .trae/ | 智能体配置，协作流程 |
| MCP.md | .trae/ | 外部连接配置 |

### 文档维护规则
1. 代码变更后同步更新相关文档
2. 新增功能必须更新CHANGELOG.md
3. 常见问题必须添加到FAQ.md
4. 分类数/链接数变更必须更新city-data.md和README.md

## MCP连接

### 已接入

#### Airbnb MCP
- **功能**: 搜索Airbnb房源、获取房源详情
- **用途**: 扩展旅游导航分类
- **工具**:
  - `airbnb_search`: 搜索指定城市的Airbnb房源
  - `airbnb_listing_details`: 获取房源详细信息
- **配置位置**: `.trae/mcp.json`

### 待接入

#### 百度统计 MCP
- **功能**: 获取网站流量数据
- **用途**: 自动化流量监控
- **优先级**: 高

#### Netlify MCP
- **功能**: 管理Netlify站点
- **用途**: 自动化部署和管理
- **优先级**: 中

#### 百度联盟 MCP
- **功能**: 获取广告收入数据
- **用途**: 自动化收入监控
- **优先级**: 中

## 一键生成脚本

### generate_mega.py
- **位置**: 项目根目录
- **功能**: 一键生成所有52个站点
- **输入**: CITIES字典（51城市）+ NATIONAL_LINKS（全国链接）
- **输出**:
  - 51个城市站 × 7文件 = 357个文件
  - 1个导航总站 × 7文件 = 7个文件
  - 1个母版 × 7文件 = 7个文件
  - 总计371个文件
- **运行**: `python generate_mega.py`
- **耗时**: 约10秒

## 项目统计

| 指标 | 数值 |
|------|------|
| 技能数 | 6 |
| 规则文件 | 3 |
| 文档文件 | 12 |
| 管理数据 | 1 |
| MCP连接 | 1（已接入）+ 3（待接入） |
| 生成脚本 | 1 |
| 总站点 | 52 |
| 总链接 | 5,661 |
| 总文件 | 364 |
| 健康度 | 99.3分（A+） |
