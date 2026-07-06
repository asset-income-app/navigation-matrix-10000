# Git自动部署方案（推荐）

## 优势
- 一次推送，自动部署所有站点
- 无需手动操作，Cloudflare自动构建
- 支持增量更新，只推送变更部分
- **1000站只需一次操作，5-10分钟完成**

## 前置准备

### 1. 安装Git（如果未安装）
下载地址: https://git-scm.com/download/win
安装后重启PowerShell

### 2. 注册GitHub账号
网址: https://github.com/
（如果已有账号可跳过）

### 3. 注册Cloudflare账号
网址: https://dash.cloudflare.com/
（如果已有账号可跳过）

## 部署步骤

### 步骤1: 创建GitHub仓库
1. 登录GitHub
2. 点击右上角 "+" → "New repository"
3. Repository name: `navigation-matrix-unified`
4. 选择 Public
5. **不要勾选** "Add a README file"
6. **不要勾选** "Add .gitignore"
7. 点击 "Create repository"

### 步骤2: 推送代码到GitHub
```powershell
# 进入项目目录
cd e:\50\navigation-matrix-unified

# 初始化Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "初始提交: 1000站导航矩阵"

# 设置主分支
git branch -M main

# 连接远程仓库（替换YOUR_USERNAME为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/navigation-matrix-unified.git

# 推送
git push -u origin main
```

**首次推送时间**: 约10-30分钟（1000站，约30000个文件）

### 步骤3: 连接Cloudflare Pages
1. 登录 Cloudflare Dashboard: https://dash.cloudflare.com/
2. 左侧菜单 → "Pages"
3. 点击 "Create a project"
4. 选择 "Connect to Git"
5. 选择 GitHub
6. 授权 Cloudflare 访问 GitHub
7. 选择仓库: `navigation-matrix-unified`
8. 配置构建:
   - Production branch: `main`
   - Build command: **留空**（无需构建）
   - Build output directory: `02-sites`
9. 点击 "Save and Deploy"

### 步骤4: 等待部署完成
- Cloudflare自动开始部署
- 部署时间: 约5-10分钟
- 完成后会显示部署成功

## 站点访问地址
- 超级总站: https://navigation-matrix-unified.pages.dev
- 城市站: https://{city}-nav.pages.dev
- 行业站: https://{niche}-nav.pages.dev
- 组合站: https://{niche}-{city}-nav.pages.dev

## 后续更新
每次修改代码后，只需：
```powershell
git add .
git commit -m "更新说明"
git push
```
Cloudflare自动重新部署变更部分。

## 注意事项
1. 首次推送可能需要较长时间（1000站）
2. 建议使用 .gitignore 排除不必要的文件（已自动生成）
3. Cloudflare Pages免费额度: 500次构建/月
4. 每个站点独立访问地址，无需额外配置

## 常见问题

### Q: 推送失败怎么办？
A: 检查GitHub用户名是否正确，仓库是否已创建

### Q: Cloudflare部署失败怎么办？
A: 检查Build output directory是否设置为 `02-sites`

### Q: 如何查看部署状态？
A: Cloudflare Dashboard → Pages → 项目详情 → Deployments

### Q: 如何添加自定义域名？
A: Cloudflare Dashboard → Pages → 项目详情 → Custom domains