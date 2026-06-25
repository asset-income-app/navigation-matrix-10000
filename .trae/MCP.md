# 导航矩阵统一版 - MCP外部连接配置

## 已接入MCP

### Airbnb MCP
- **用途**: 旅游导航站扩展
- **工具**: airbnb_search, airbnb_listing_details
- **状态**: 已接入
- **应用场景**: 城市站旅游分类、旅游行业站

## 待接入MCP

### Cloudflare MCP
- **用途**: 自动部署、DNS管理、缓存清理
- **工具**: pages_deploy, dns_manage, cache_purge
- **状态**: 待接入
- **应用场景**: 批量部署到Cloudflare Pages

### 百度统计 MCP
- **用途**: 流量数据同步
- **工具**: get_traffic_data, get_realtime_data
- **状态**: 待接入
- **应用场景**: 收入仪表盘、流量分析

### 百度联盟 MCP
- **用途**: 广告收入数据
- **工具**: get_revenue_data, get_ad_performance
- **状态**: 待接入
- **应用场景**: 收入追踪

### Google Search Console MCP
- **用途**: SEO数据、索引状态
- **工具**: get_index_status, get_search_analytics
- **状态**: 待接入
- **应用场景**: SEO优化

## MCP使用规则

1. MCP工具调用前必须检查工具schema
2. 所有MCP调用参数必须通过args字段传递
3. MCP调用失败时记录日志并降级处理
4. 敏感信息（API密钥）不硬编码，使用环境变量

## 自定义MCP开发计划

### link-checker-mcp
- **功能**: 批量检查链接有效性
- **输入**: URL列表
- **输出**: 链接状态报告

### site-generator-mcp
- **功能**: 一键生成站点
- **输入**: 站点配置
- **输出**: 生成的站点文件

### revenue-aggregator-mcp
- **功能**: 汇总多平台收入
- **输入**: 时间范围
- **输出**: 收入报告
