# 部署指南

> 52个站点 · Cloudflare Pages免费托管 · 无限带宽 · 零成本部署

## 为什么选择Cloudflare Pages

### Cloudflare Pages vs Netlify 核心对比

| 特性 | Cloudflare Pages | Netlify |
|------|------------------|---------|
| **免费带宽** | **无限** | 100GB/月（超出暂停） |
| **免费构建** | 500次/月 | 300次/月 |
| **CDN节点** | 300+全球节点 | 多云网络 |
| **DDoS防护** | **内置免费** | 需付费 |
| **国内访问** | 更快（Anycast网络） | 较慢 |
| **SSL证书** | 自动免费 | 自动免费 |
| **CLI工具** | Wrangler | Netlify CLI |

**结论：Cloudflare Pages更适合本项目——无限带宽、全球加速、免费安全防护。**

## 部署核心问题

### 为什么每个站点需要独立部署？

**是的，每个站点都是独立的Cloudflare Pages站点，需要单独部署。**

原因：
- 每个站点有独立的域名（如 `tangshan.pages.dev`）
- 每个站点有独立的SSL证书
- 每个站点有独立的部署历史
- Cloudflare Pages不支持一个站点下有多个子站点

**这意味着：**
- 首次部署需要创建52个Cloudflare Pages站点
- 每个站点需要单独部署7个文件
- 后续更新也需要单独更新每个站点

## 部署架构

```
本地开发环境
    │
    ├── generate_mega.py 生成所有站点
    │
    ├── 02-city-sites/{city}/  ← 51个城市站（各7个文件）
    │   ├── config.json
    │   ├── index.html (含EMBEDDED_CONFIG)
    │   ├── style.css
    │   ├── script.js
    │   ├── sitemap.xml
    │   ├── robots.txt
    │   └── _headers (Cloudflare安全头配置)
    │
    ├── 03-master-navigation/  ← 导航总站（7个文件）
    │
    └── 部署到 Cloudflare Pages（52个独立站点）
        ├── tangshan.pages.dev
        ├── baoding.pages.dev
        ├── handan.pages.dev
        ├── ... (共51个城市站)
        └── daohangbaike.pages.dev (总站)
```

## 部署前准备

### 1. 注册Cloudflare账号
1. 访问 https://dash.cloudflare.com/sign-up
2. 使用邮箱注册（免费）
3. 免费套餐足够使用（无限带宽、500次构建/月）

### 2. 安装Wrangler CLI（可选，推荐）
```bash
npm install -g wrangler
wrangler login
```

### 3. 生成所有站点
```bash
cd e:\50\navigation-matrix-v3
python generate_mega.py
```

生成完成后，每个城市站目录包含7个文件。

## 三种部署方式对比

### 方式1：手动拖拽部署（最简单）

**操作步骤：**
1. 登录 https://dash.cloudflare.com
2. 点击左侧 "Workers & Pages"
3. 点击 "Create application" → "Pages" → "Upload assets"
4. 输入项目名称（如 `tangshan-nav`）
5. 将城市站文件夹（如 `02-city-sites/tangshan/`）拖入上传区域
6. 点击 "Deploy site"
7. 等待部署完成（约30秒）
8. 访问 `https://tangshan.pages.dev`
9. 重复52次

**优点：**
- 简单直观，无需命令行
- 适合新手
- 每个站点独立创建，便于管理

**缺点：**
- 需要重复52次操作（51个城市站 + 1个总站）
- 每次约2分钟，总计约100分钟
- 后续更新也需要重复操作

**适用场景：**
- 首次部署
- 不熟悉命令行的用户
- 只部署少量站点

---

### 方式2：Wrangler CLI批量部署（推荐）

**前提条件：**
- 已安装Wrangler CLI
- 已登录Cloudflare账号

**操作步骤：**

#### 步骤1：安装并登录Wrangler
```bash
npm install -g wrangler
wrangler login
```

#### 步骤2：使用批量部署脚本
创建 `deploy-cf.ps1` 文件：

```powershell
# 批量部署所有站点到Cloudflare Pages
# 使用方法：在项目根目录运行 .\deploy-cf.ps1

$cities = @(
    "tangshan", "baoding", "handan", "cangzhou", "langfang",
    "weifang", "linyi", "jining", "zibo", "weihai",
    "zhenjiang", "huaian", "lianyungang", "yancheng", "suqian",
    "taizhou", "huzhou", "fuyang", "wuhu", "chuzhou",
    "shangrao", "jiujiang", "ganzhou", "yichang", "xiangyang",
    "yueyang", "hengyang", "zhuzhou", "changde", "luoyang",
    "nanyang", "xinxiang", "guilin", "liuzhou", "mianyang",
    "yibin", "zunyi", "lanzhou", "yinchuan", "haikou",
    "shantou", "zhanjiang", "zhaoqing", "jiangmen", "putian",
    "longyan", "zhangzhou", "ningde", "xianyang", "yulin",
    "eerduosi"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "开始批量部署 51 个城市站到Cloudflare Pages" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$successCount = 0
$failCount = 0

foreach ($city in $cities) {
    Write-Host "`n[$($cities.IndexOf($city) + 1)/51] 部署 $city ..." -ForegroundColor Yellow
    
    $cityPath = "02-city-sites\$city"
    
    if (Test-Path $cityPath) {
        $result = npx wrangler pages deploy $cityPath --project-name="$city-nav" 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ $city 部署成功 → https://$city.pages.dev" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host "✗ $city 部署失败: $result" -ForegroundColor Red
            $failCount++
        }
        
        Start-Sleep -Seconds 2
    } else {
        Write-Host "✗ $city 目录不存在" -ForegroundColor Red
        $failCount++
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "部署导航总站 ..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$result = npx wrangler pages deploy "03-master-navigation" --project-name="daohangbaike-nav" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 导航总站部署成功 → https://daohangbaike.pages.dev" -ForegroundColor Green
    $successCount++
} else {
    Write-Host "✗ 导航总站部署失败: $result" -ForegroundColor Red
    $failCount++
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "部署完成" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "成功: $successCount 个站点" -ForegroundColor Green
Write-Host "失败: $failCount 个站点" -ForegroundColor Red
Write-Host "`n站点列表:" -ForegroundColor Cyan
Write-Host "  城市站: https://tangshan.pages.dev 等51个" -ForegroundColor White
Write-Host "  导航总站: https://daohangbaike.pages.dev" -ForegroundColor White
```

**优点：**
- 自动化，一键部署所有站点
- 首次部署自动创建站点
- 可重复执行（后续更新）
- 显示部署进度和结果
- 失败站点会标记出来

**缺点：**
- 需要安装Wrangler CLI
- 需要熟悉命令行

**适用场景：**
- 首次部署
- 批量修改后重新部署
- 定期维护更新

---

### 方式3：Git仓库部署（自动化）

**操作步骤：**

#### 步骤1：将项目推送到GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/navigation-matrix.git
git push -u origin main
```

#### 步骤2：在Cloudflare Pages连接GitHub
1. 登录Cloudflare Dashboard
2. 点击 "Workers & Pages" → "Create application" → "Pages" → "Connect to Git"
3. 选择GitHub，授权Cloudflare访问
4. 选择仓库 `navigation-matrix`
5. 配置：
   - 生产分支：`main`
   - 构建命令：`python generate_mega.py`（或 `exit 0`）
   - 输出目录：`02-city-sites/tangshan`（每个站点单独配置）
6. 点击 "Save and Deploy"

**注意：** Git集成方式需要为每个站点单独创建项目，配置不同的输出目录。

**优点：**
- 最自动化，每次push自动部署
- 版本控制，便于回滚
- 团队协作友好
- Preview部署（每个PR自动生成预览URL）

**缺点：**
- 配置复杂，需要为52个站点分别配置
- 需要熟悉Git操作

**适用场景：**
- 团队协作开发
- 需要版本控制
- 频繁更新迭代

---

## 推荐方案：Wrangler CLI批量部署

### 第一步：安装Wrangler（5分钟）

```bash
npm install -g wrangler
wrangler login
```

### 第二步：批量部署（约15分钟）

```powershell
# 生成所有站点
python generate_mega.py

# 执行批量部署
.\deploy-cf.ps1
```

**Wrangler会自动创建站点并部署，无需手动创建。**

---

## 部署时间估算

| 方式 | 首次部署 | 后续更新 | 适用人群 |
|------|----------|----------|----------|
| 手动拖拽 | 104分钟 | 104分钟 | 新手 |
| Wrangler CLI | **15分钟** | **10分钟** | 进阶用户（推荐） |
| Git仓库 | 120分钟（配置） | 自动（秒级） | 团队协作 |

---

## 部署详细步骤

### 步骤1：创建Cloudflare Pages站点

为每个城市创建一个Cloudflare Pages站点：

| 序号 | 城市 | 项目名称 | 域名 |
|------|------|----------|------|
| 1 | 唐山 | tangshan-nav | tangshan.pages.dev |
| 2 | 保定 | baoding-nav | baoding.pages.dev |
| 3 | 邯郸 | handan-nav | handan.pages.dev |
| ... | ... | ... | ... |
| 51 | 鄂尔多斯 | eerduosi-nav | eerduosi.pages.dev |
| 52 | 导航百科 | daohangbaike-nav | daohangbaike.pages.dev |

### 步骤2：部署站点文件

每个站点包含7个文件：

| 文件 | 用途 | 大小 |
|------|------|------|
| config.json | 城市配置数据 | ~15KB |
| index.html | 页面结构（含内嵌数据） | ~25KB |
| style.css | 样式表 | ~8KB |
| script.js | 交互脚本 | ~5KB |
| sitemap.xml | SEO站点地图 | ~1KB |
| robots.txt | 爬虫规则 | ~0.1KB |
| _headers | Cloudflare安全头配置 | ~0.2KB |
| **总计** | - | **~55KB** |

### 步骤3：验证部署

部署完成后，必须验证每个站点：

1. 访问 `https://{pinyin}.pages.dev`
2. 检查页面是否正常显示（标题、分类、链接）
3. 测试搜索功能（输入关键词，检查过滤效果）
4. 测试分类展开/收起（点击分类标题）
5. 测试链接跳转（点击任意链接）
6. 检查移动端适配（缩小浏览器窗口）
7. 检查底部版权信息

### 步骤4：配置自定义域名（可选）

如果购买了独立域名：

1. 在Cloudflare中添加域名：
   - Pages项目设置 → Custom domains → Add domain
   - 输入域名（如 `tangshan-nav.com`）

2. Cloudflare会自动配置DNS和SSL证书

3. 如果域名已在Cloudflare托管，配置更快（几分钟）

---

## SEO文件说明

### sitemap.xml

每个站点自动生成sitemap.xml：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://tangshan.pages.dev/</loc>
    <lastmod>2026-06-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

**作用：**
- 告诉搜索引擎站点有哪些页面
- 提高搜索引擎收录效率
- 每次部署后自动更新

### robots.txt

每个站点自动生成robots.txt：

```
User-agent: *
Allow: /
Sitemap: https://tangshan.pages.dev/sitemap.xml
```

**作用：**
- 允许所有搜索引擎爬取
- 指定sitemap位置
- 防止搜索引擎爬取不需要的页面

### _headers

每个站点自动生成 `_headers` 文件（Cloudflare专用）：

```
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-XSS-Protection: 1; mode=block
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

**作用：**
- 配置安全头，防止XSS攻击
- 防止页面被iframe嵌入
- 保护用户隐私
- 强制HTTPS访问

---

## 更新部署

### 单站更新

当只需要更新单个站点时：

```powershell
# 进入城市站目录
cd 02-city-sites/tangshan

# 部署更新
npx wrangler pages deploy . --project-name=tangshan-nav

# 返回项目根目录
cd ../..
```

### 批量更新

当需要更新所有站点时：

```powershell
# 1. 修改 generate_mega.py 或母版模板
# 2. 重新生成所有站点
python generate_mega.py

# 3. 批量部署更新
.\deploy-cf.ps1
```

### 紧急修复

当某个站点出现问题时：

```powershell
# 快速修复单个站点
npx wrangler pages deploy 02-city-sites/tangshan --project-name=tangshan-nav
```

---

## 部署检查清单

### 部署前检查

- [ ] 运行 `python generate_mega.py` 生成最新文件
- [ ] 检查所有城市站目录存在（51个）
- [ ] 检查每个目录包含7个文件
- [ ] 检查config.json数据正确（cityName/cityPinyin/province/categories）
- [ ] 检查index.html包含EMBEDDED_CONFIG变量
- [ ] 检查sitemap.xml/robots.txt/_headers存在
- [ ] 备份到 `06-backups/` 目录

### 部署后验证

- [ ] 访问站点确认页面正常显示
- [ ] 检查页面标题正确（"{城市}便民服务导航"）
- [ ] 测试搜索功能正常
- [ ] 测试分类展开/收起正常
- [ ] 测试链接跳转正常
- [ ] 检查移动端适配正常
- [ ] 检查底部版权信息正确
- [ ] 检查sitemap.xml可访问
- [ ] 检查robots.txt可访问
- [ ] 检查HTTPS强制跳转

### 部署后提交

- [ ] 提交站点到百度站长平台
- [ ] 提交站点到必应站长工具
- [ ] 提交站点到搜狗站长平台
- [ ] 记录站点URL到management.json

---

## 常见部署问题

### Q: 站点名称已被占用？

**原因：** Cloudflare Pages项目名称全局唯一，可能被其他用户占用。

**解决方案：**
- 在名称后加数字，如 `tangshan-nav2`
- 或使用其他前缀，如 `tangshan-city-nav`

### Q: 部署后页面空白？

**原因：** v2版本存在CORS限制，直接打开HTML无法加载config.json。

**解决方案：** v3版本已修复，HTML内嵌了EMBEDDED_CONFIG数据。如果仍有问题：
- 检查index.html是否包含 `<script>var EMBEDDED_CONFIG = ...</script>`
- 检查script.js是否优先读取EMBEDDED_CONFIG
- 检查浏览器控制台是否有错误

### Q: Wrangler登录失败？

**原因：** 浏览器未自动打开或网络问题。

**解决方案：**
```bash
# 手动获取授权码
wrangler login --method=manual

# 或使用API Token
wrangler login --api-token=YOUR_API_TOKEN
```

### Q: 部署超时？

**原因：** 文件数量过多或网络不稳定。

**解决方案：**
- 检查网络连接
- 使用 `--skip-caching` 参数加速：
```bash
npx wrangler pages deploy . --project-name=tangshan-nav --skip-caching
```

### Q: 自定义域名无法访问？

**原因：** DNS记录配置错误或DNS传播未完成。

**解决方案：**
1. 确保域名已添加到Cloudflare（DNS托管）
2. 在Pages项目中添加自定义域名
3. Cloudflare会自动配置DNS记录
4. 等待DNS传播（几分钟到几小时）

### Q: 能否一次性部署所有站点？

**答案：** 可以！使用Wrangler CLI批量部署脚本。

```powershell
.\deploy-cf.ps1
```

Wrangler会自动创建并部署所有站点。

### Q: 能否用一个域名部署所有站点？

**答案：** 可以，需要购买独立域名并配置子域名。

**方案：**
- 购买域名（如 `daohang.com`）
- 配置子域名（如 `tangshan.daohang.com`）
- 每个子域名指向对应的Cloudflare Pages站点
- 成本：域名费用约50-100元/年

### Q: 部署失败怎么办？

**常见原因：**
- Wrangler未登录
- 项目名称已存在（但属于其他账号）
- 文件不完整

**解决方案：**
1. 检查登录状态：
```bash
wrangler whoami
```

2. 检查文件完整性：
```powershell
cd 02-city-sites/tangshan
ls  # 应显示7个文件
```

3. 查看详细错误：
```bash
npx wrangler pages deploy . --project-name=tangshan-nav --verbose
```

### Q: 如何查看部署日志？

**方法：**
1. 登录Cloudflare Dashboard
2. 进入 "Workers & Pages"
3. 点击项目名称
4. 查看 "Deployments" 标签
5. 点击具体部署查看详细日志

### Q: Direct Upload和Git集成有什么区别？

| 方式 | Direct Upload | Git集成 |
|------|---------------|---------|
| 部署方式 | Wrangler或拖拽上传 | Git push自动部署 |
| 构建环境 | 本地构建 | Cloudflare云端构建 |
| 版本控制 | 无自动版本控制 | Git历史自动关联 |
| Preview | 无 | 每个PR自动生成预览URL |
| 切换 | **不能切换到Git** | 可以手动部署 |

**注意：** 选择Direct Upload后，不能切换到Git集成，需要创建新项目。

---

## Cloudflare Pages免费额度详情

| 资源 | 免费额度 | 说明 |
|------|----------|------|
| 构建次数 | 500次/月 | 超出需付费 |
| 带宽 | **无限** | 无流量限制 |
| 请求数 | 无限 | 无请求限制 |
| 站点数 | 无限 | 可创建无限站点 |
| 自定义域名 | 100个 | 超出需付费 |
| Workers请求 | 100,000次/天 | 用于动态功能 |
| DDoS防护 | **免费** | 自动防护 |
| SSL证书 | **免费** | 自动配置 |

**本项目52个站点，每月构建约10次（维护更新），完全在免费额度内。**

---

## 成本估算

| 项目 | 费用 | 说明 |
|------|------|------|
| Cloudflare托管 | 0元/月 | 免费套餐（无限带宽） |
| SSL证书 | 0元 | Cloudflare自动配置 |
| CDN | 0元 | Cloudflare全球CDN（300+节点） |
| DDoS防护 | 0元 | Cloudflare内置防护 |
| 域名 | 0元 | 使用Cloudflare子域名 |
| 开发 | 0元 | AI生成代码 |
| 维护 | 0元 | AI辅助维护 |
| **总计** | **0元/月** | 完全零成本 |

---

## 部署最佳实践

### 1. 使用Wrangler CLI
推荐使用CLI批量部署，效率最高：
```powershell
.\deploy-cf.ps1
```

### 2. 备份机制
每次部署前备份：
```powershell
# 创建备份
$date = Get-Date -Format "yyyy-MM-dd"
Compress-Archive -Path "02-city-sites","03-master-navigation" -DestinationPath "06-backups\$date-backup.zip"
```

### 3. 版本控制
使用Git管理代码：
```bash
git add .
git commit -m "Update before deploy"
git push
```

### 4. 监控机制
部署后监控站点状态：
- 使用百度统计监控流量
- 定期检查站点可访问性
- 监控失效链接比例

### 5. 文档记录
记录每次部署：
- 部署时间
- 部署站点列表
- 部署结果（成功/失败）
- 部署问题及解决方案

---

## 部署脚本

完整的批量部署脚本已包含在项目中：
- `deploy-cf.ps1` - Cloudflare Pages批量部署脚本（推荐）
- `deploy-single.ps1` - 单站点部署脚本

---

## 下一步

部署完成后：
1. 提交所有站点到搜索引擎
2. 申请百度联盟广告
3. 开始运营推广
4. 定期维护更新