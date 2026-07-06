# 全国三线城市便民导航站矩阵

> 52个站点 · 5955条真实链接 · 15个服务分类 · 零代码开发 · 免费托管 · 被动收入

## 项目简介

全国三线城市便民导航站矩阵是一个由 **1个导航总站 + 51个城市站** 组成的三层金字塔架构网站群。每个城市站收录当地政府、社保、医保、交通、教育等便民服务官方链接，为三线城市居民提供一站式便民导航服务。

**核心特点：**
- 零代码开发：纯AI生成，无需编程知识
- 零成本运营：Netlify免费托管，无服务器费用
- 被动收入：百度联盟广告 + 商家付费收录 + 分类置顶广告
- 万物互联：总站与城市站互相导流，形成流量闭环
- 数据内嵌：HTML直接嵌入config.json数据，直接打开文件即可显示

## 架构总览

```
                    ┌──────────────────────┐
                    │   第三层：导航总站     │
                    │   导航百科             │
                    │   daohangbaike-nav    │
                    │   .pages.dev        │
                    └──────────┬───────────┘
                               │ 互相导流
          ┌────────────────────┼────────────────────┐
          │                    │                     │
   ┌──────┴──────┐    ┌───────┴──────┐     ┌───────┴──────┐
   │ 唐山便民导航 │    │ 洛阳便民导航  │ ... │ 榆林便民导航  │
   │ tangshan-nav│    │ luoyang-nav  │     │ yulin-nav    │
   │ .pages.dev│    │ .pages.dev │     │ .pages.dev │
   └─────────────┘    └──────────────┘     └──────────────┘
          │                    │                     │
          └────────────────────┼────────────────────┘
                               │ 批量同步
                    ┌──────────┴───────────┐
                    │   第一层：母版模板     │
                    │   01-master-template  │
                    └──────────────────────┘
```

## 目录结构

```
navigation-matrix-v3/
├── 01-master-template/          # 母版模板（所有城市站的源代码）
│   ├── config.json              # 模板配置文件
│   ├── index.html               # 页面结构（含内嵌数据）
│   ├── style.css                # 样式表
│   ├── script.js                # 交互脚本
│   ├── sitemap.xml              # 站点地图
│   ├── robots.txt               # 爬虫规则
│   └── _headers                 # Cloudflare安全头配置
│
├── 02-city-sites/               # 51个城市站（由脚本自动生成）
│   ├── tangshan/                # 唐山站
│   │   ├── config.json          # 唐山专属配置（114条本地链接）
│   │   ├── index.html           # 页面（含内嵌数据）
│   │   ├── style.css            # 样式
│   │   ├── script.js            # 脚本
│   │   ├── sitemap.xml          # 站点地图
│   │   ├── robots.txt           # 爬虫规则
│   │   └── _headers             # Cloudflare安全头配置
│   ├── luoyang/                 # 洛阳站
│   └── ...（共51个城市）
│
├── 03-master-navigation/        # 导航总站
│   ├── config.json              # 总站配置（含51城市链接+全国服务）
│   ├── index.html               # 页面（含内嵌数据）
│   ├── style.css                # 样式
│   ├── script.js                # 脚本
│   ├── sitemap.xml              # 站点地图
│   ├── robots.txt               # 爬虫规则
│   └── _headers                 # Cloudflare安全头配置
│
├── 04-deployed/                 # 部署管理
│   └── management.json          # 站点管理数据（流量/收入/状态）
│
├── 05-seo/                      # SEO工具
│   └── all-sitemaps.xml         # 全站sitemap汇总
│
├── 06-backups/                  # 备份目录
│   └── link-reports/            # 链接检查报告
│
├── .trae/                       # 配套设施
│   ├── skills/                  # 6个自动化技能
│   │   ├── central-controller/  # 中央总站控制器
│   │   ├── city-site-manager/   # 城市站管理器
│   │   ├── batch-updater/       # 批量更新器
│   │   ├── link-collector/      # 链接收集器
│   │   ├── link-checker/        # 链接检查器
│   │   └── deployer/            # 部署器
│   ├── AGENTS.md                # 智能体架构
│   ├── MCP.md                   # 外部连接配置
│   ├── RULES.md                 # 开发规则
│   └── OVERVIEW.md              # 生态系统总览
│
├── docs/                        # 项目文档
│   ├── development-guide.md     # 开发指南
│   ├── operations-manual.md     # 运营手册
│   ├── infrastructure.md        # 配套设施文档
│   ├── city-data.md             # 城市数据总表
│   ├── deploy-guide.md          # 部署指南
│   ├── CHANGELOG.md             # 变更日志
│   └── FAQ.md                   # 常见问题
│
└── generate_mega.py             # 一键生成脚本（核心工具）
```

## 技术栈

| 技术 | 用途 | 说明 |
|------|------|------|
| HTML5 | 页面结构 | 语义化标签，SEO友好，内嵌配置数据 |
| CSS3 | 样式设计 | CSS变量、Grid布局、响应式 |
| JavaScript | 交互功能 | 原生JS，无框架依赖，优先内嵌数据 |
| JSON | 数据配置 | 每个城市独立config.json |
| Python | 生成脚本 | 一键生成51个站点 |
| Netlify | 免费托管 | 静态网站托管，自动HTTPS，安全头配置 |

## 城市站功能

每个城市站包含以下功能：

1. **分类导航** - 15个便民服务分类，点击展开/收起
2. **实时搜索** - 输入关键词即时过滤链接
3. **回到顶部** - 滚动后出现回到顶部按钮
4. **响应式设计** - 完美适配手机/平板/电脑
5. **本地化链接** - 每个城市收录本地政府、社保、医保等官方链接
6. **数据内嵌** - HTML直接嵌入config.json数据，无需HTTP服务器也能显示
7. **SEO优化** - 结构化数据、sitemap、robots.txt、安全头

### 15个服务分类

| 序号 | 分类名称 | 图标 | 内容说明 |
|------|----------|------|----------|
| 1 | 政务服务 | 🏛️ | 市政府、政务网、人社局、住建局、教育局 |
| 2 | 社保医保 | 💊 | 社保平台、医保局、公积金中心、养老金 |
| 3 | 交通出行 | 🚌 | 公交公司、12306、本地交通信息 |
| 4 | 车辆服务 | 🚗 | 车管所、交管12123、驾考、违章查询 |
| 5 | 医疗健康 | 🏥 | 卫健委、人民医院、中医院、疾控中心 |
| 6 | 教育考试 | 📚 | 教育局、考试院、招生办、学校 |
| 7 | 生活服务 | 💡 | 自来水、供电、燃气、供暖、邮政 |
| 8 | 紧急电话 | 🆘 | 110、120、119、122、95598、12315、12345 |
| 9 | 吃喝玩乐 | 🎉 | 文旅局、景点、美食、公园 |
| 10 | 企业服务 | 🏢 | 工商局、税务局、市场监管局 |
| 11 | 房产家居 | 🏘️ | 住建局、贝壳找房、安居客、链家 |
| 12 | 金融理财 | 💰 | 工商银行、建设银行、支付宝、微信支付 |
| 13 | 新闻媒体 | 📰 | 本地日报、电视台、新闻网 |
| 14 | AI工具 | 🤖 | ChatGPT、DeepSeek、豆包、通义千问 |
| 15 | 本地服务 | 📍 | 本地特色便民服务（每个城市不同） |

## 导航总站功能

导航总站（导航百科）包含28个分类，覆盖：

- **城市导航** - 51个城市站入口
- **按省份分组** - 19个省份分组导航
- **全国性服务** - 政府服务、社保医保、交通出行等通用链接
- **行业垂直导航** - 程序员、设计师、产品经理等职业导航
- **工具导航** - 开发工具、设计工具、效率工具
- **资源导航** - 学习资源、素材资源、开源项目

## 快速开始

### 前置条件

- Python 3.6+（用于运行生成脚本）
- 浏览器（用于本地预览）
- Netlify账号（用于部署上线）

### 一键生成所有站点

```bash
cd e:\50\navigation-matrix-v3
python generate_mega.py
```

脚本将自动：
1. 生成51个城市站（7个文件/站：config.json + index.html + style.css + script.js + sitemap.xml + robots.txt + _headers）
2. 生成导航总站（7个文件）
3. 更新母版模板（7个文件）

### 本地预览

```bash
# 预览导航总站
cd 03-master-navigation
python -m http.server 8080

# 预览某个城市站
cd 02-city-sites/tangshan
python -m http.server 8081
```

也可以直接双击打开 `index.html` 文件（数据已内嵌，无需服务器）。

### 部署到Cloudflare Pages

详见 [docs/deploy-guide.md](docs/deploy-guide.md)

## 收入模式

| 收入来源 | 单价 | 适用站点 | 预估月收入 |
|----------|------|----------|------------|
| 百度联盟广告 | CPC/CPM | 所有站点 | 500-2000元 |
| 商家收录 | 300元/年 | 城市站 | 1500-5000元 |
| 分类置顶 | 500元/月 | 城市站 | 1000-3000元 |
| 总站收录 | 200元/永久 | 导航总站 | 200-1000元 |
| 总站首页推荐 | 2000元/月 | 导航总站 | 0-2000元 |

## 51个城市站清单

| 序号 | 城市 | 拼音 | 省份 | 域名 |
|------|------|------|------|------|
| 1 | 唐山 | tangshan | 河北 | tangshan-nav.pages.dev |
| 2 | 洛阳 | luoyang | 河南 | luoyang-nav.pages.dev |
| 3 | 保定 | baoding | 河北 | baoding-nav.pages.dev |
| 4 | 邯郸 | handan | 河北 | handan-nav.pages.dev |
| 5 | 沧州 | cangzhou | 河北 | cangzhou-nav.pages.dev |
| 6 | 廊坊 | langfang | 河北 | langfang-nav.pages.dev |
| 7 | 潍坊 | weifang | 山东 | weifang-nav.pages.dev |
| 8 | 临沂 | linyi | 山东 | linyi-nav.pages.dev |
| 9 | 济宁 | jining | 山东 | jining-nav.pages.dev |
| 10 | 淄博 | zibo | 山东 | zibo-nav.pages.dev |
| 11 | 威海 | weihai | 山东 | weihai-nav.pages.dev |
| 12 | 台州 | taizhou | 浙江 | taizhou-nav.pages.dev |
| 13 | 镇江 | zhenjiang | 江苏 | zhenjiang-nav.pages.dev |
| 14 | 淮安 | huaian | 江苏 | huaian-nav.pages.dev |
| 15 | 连云港 | lianyungang | 江苏 | lianyungang-nav.pages.dev |
| 16 | 盐城 | yancheng | 江苏 | yancheng-nav.pages.dev |
| 17 | 宿迁 | suqian | 江苏 | suqian-nav.pages.dev |
| 18 | 湖州 | huzhou | 浙江 | huzhou-nav.pages.dev |
| 19 | 阜阳 | fuyang | 安徽 | fuyang-nav.pages.dev |
| 20 | 芜湖 | wuhu | 安徽 | wuhu-nav.pages.dev |
| 21 | 滁州 | chuzhou | 安徽 | chuzhou-nav.pages.dev |
| 22 | 上饶 | shangrao | 江西 | shangrao-nav.pages.dev |
| 23 | 九江 | jiujiang | 江西 | jiujiang-nav.pages.dev |
| 24 | 赣州 | ganzhou | 江西 | ganzhou-nav.pages.dev |
| 25 | 宜昌 | yichang | 湖北 | yichang-nav.pages.dev |
| 26 | 襄阳 | xiangyang | 湖北 | xiangyang-nav.pages.dev |
| 27 | 岳阳 | yueyang | 湖南 | yueyang-nav.pages.dev |
| 28 | 衡阳 | hengyang | 湖南 | hengyang-nav.pages.dev |
| 29 | 株洲 | zhuzhou | 湖南 | zhuzhou-nav.pages.dev |
| 30 | 常德 | changde | 湖南 | changde-nav.pages.dev |
| 31 | 南阳 | nanyang | 河南 | nanyang-nav.pages.dev |
| 32 | 新乡 | xinxiang | 河南 | xinxiang-nav.pages.dev |
| 33 | 桂林 | guilin | 广西 | guilin-nav.pages.dev |
| 34 | 柳州 | liuzhou | 广西 | liuzhou-nav.pages.dev |
| 35 | 绵阳 | mianyang | 四川 | mianyang-nav.pages.dev |
| 36 | 宜宾 | yibin | 四川 | yibin-nav.pages.dev |
| 37 | 遵义 | zunyi | 贵州 | zunyi-nav.pages.dev |
| 38 | 兰州 | lanzhou | 甘肃 | lanzhou-nav.pages.dev |
| 39 | 银川 | yinchuan | 宁夏 | yinchuan-nav.pages.dev |
| 40 | 海口 | haikou | 海南 | haikou-nav.pages.dev |
| 41 | 汕头 | shantou | 广东 | shantou-nav.pages.dev |
| 42 | 湛江 | zhanjiang | 广东 | zhanjiang-nav.pages.dev |
| 43 | 肇庆 | zhaoqing | 广东 | zhaoqing-nav.pages.dev |
| 44 | 江门 | jiangmen | 广东 | jiangmen-nav.pages.dev |
| 45 | 莆田 | putian | 福建 | putian-nav.pages.dev |
| 46 | 龙岩 | longyan | 福建 | longyan-nav.pages.dev |
| 47 | 漳州 | zhangzhou | 福建 | zhangzhou-nav.pages.dev |
| 48 | 宁德 | ningde | 福建 | ningde-nav.pages.dev |
| 49 | 咸阳 | xianyang | 陕西 | xianyang-nav.pages.dev |
| 50 | 鄂尔多斯 | eerduosi | 内蒙古 | eerduosi-nav.pages.dev |
| 51 | 榆林 | yulin | 陕西 | yulin-nav.pages.dev |

## 项目统计

| 指标 | 数值 |
|------|------|
| 总站点数 | 52（1总站 + 51城市站） |
| 总链接数 | 5,955 |
| 城市站平均链接数 | 114 |
| 服务分类数 | 15（城市站）+ 28（总站） |
| 覆盖省份 | 19个 |
| 每站文件数 | 7个 |
| 总文件数 | 364 |
| 技能数 | 6个 |
| 配套文档 | 17个 |
| 健康度 | 99.3分（A+） |

## 许可证

本项目仅供个人学习和研究使用。所有链接指向的网站内容归原网站所有。
