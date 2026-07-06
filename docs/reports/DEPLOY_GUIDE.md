# Cloudflare Pages 部署指南

## 方法1: Git自动部署（推荐）

### 步骤1: 创建Git仓库
```bash
cd navigation-matrix-unified
git init
git add .
git commit -m "初始提交"
```

### 步骤2: 推送到GitHub
1. 在GitHub创建新仓库: `navigation-matrix-unified`
2. 推送代码:
```bash
git remote add origin https://github.com/你的用户名/navigation-matrix-unified.git
git push -u origin main
```

### 步骤3: 连接Cloudflare Pages
1. 登录 Cloudflare Dashboard
2. 进入 Pages > Create a project
3. 选择 "Connect to Git"
4. 选择GitHub仓库 `navigation-matrix-unified`
5. 配置:
   - Project name: `navigation-matrix-unified`
   - Production branch: `main`
   - Build command: 无需构建
   - Build output directory: `/`
6. 点击 "Save and Deploy"

### 步骤4: 等待部署完成
- Cloudflare会自动部署所有站点
- 部署完成后，每个站点可通过:
  - `https://{站点名}-nav.pages.dev` 访问
  - 或自定义域名

---

## 方法2: 直接上传（手动）

### 步骤1: 安装Wrangler
```bash
npm install -g wrangler
```

### 步骤2: 登录Cloudflare
```bash
wrangler login
```

### 步骤3: 创建Pages项目
```bash
wrangler pages project create navigation-matrix-unified
```

### 步骤4: 上传站点
```bash
wrangler pages deploy ./02-sites --project-name=navigation-matrix-unified
```

---

## 方法3: 分批部署（适合大量站点）

### 每批50个站点
```bash
# 第1批: 城市站
wrangler pages deploy ./02-sites/cities --project-name=navigation-matrix-unified

# 第2批: 行业站
wrangler pages deploy ./02-sites/niches --project-name=navigation-matrix-unified
```

---

## 验证部署

### 检查站点访问
```bash
# 测试站点是否可访问
curl https://baoding-nav.pages.dev
curl https://kaoyan-nav.pages.dev
```

### 查看部署状态
- Cloudflare Dashboard > Pages > navigation-matrix-unified
- 查看部署历史和日志

---

## 自定义域名（可选）

### 添加自定义域名
1. Cloudflare Dashboard > Pages > navigation-matrix-unified > Custom domains
2. 添加域名: `你的域名.com`
3. 配置DNS解析

---

## 注意事项

1. **免费额度**: Cloudflare Pages免费版每月500次部署
2. **站点数量**: 单个项目可部署无限站点
3. **文件大小**: 单文件最大25MB
4. **总大小**: 项目总大小不超过500MB

---

## 部署后维护

### 更新站点
```bash
# 修改后重新部署
git add .
git commit -m "更新站点"
git push
```

### 自动部署
- 每次Git推送，Cloudflare自动重新部署
- 无需手动操作

---

## 当前站点清单

- [保定](https://baoding-nav.pages.dev) (cities)
- [沧州](https://cangzhou-nav.pages.dev) (cities)
- [常德](https://changde-nav.pages.dev) (cities)
- [滁州](https://chuzhou-nav.pages.dev) (cities)
- [鄂尔多斯](https://eerduosi-nav.pages.dev) (cities)
- [阜阳](https://fuyang-nav.pages.dev) (cities)
- [赣州](https://ganzhou-nav.pages.dev) (cities)
- [桂林](https://guilin-nav.pages.dev) (cities)
- [海口](https://haikou-nav.pages.dev) (cities)
- [邯郸](https://handan-nav.pages.dev) (cities)
- [衡阳](https://hengyang-nav.pages.dev) (cities)
- [淮安](https://huaian-nav.pages.dev) (cities)
- [湖州](https://huzhou-nav.pages.dev) (cities)
- [江门](https://jiangmen-nav.pages.dev) (cities)
- [济宁](https://jining-nav.pages.dev) (cities)
- [九江](https://jiujiang-nav.pages.dev) (cities)
- [廊坊](https://langfang-nav.pages.dev) (cities)
- [兰州](https://lanzhou-nav.pages.dev) (cities)
- [连云港](https://lianyungang-nav.pages.dev) (cities)
- [临沂](https://linyi-nav.pages.dev) (cities)

... 共 152 个站点
