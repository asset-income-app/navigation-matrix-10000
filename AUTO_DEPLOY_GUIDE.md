# 自动化部署脚本运行指南

## 🎯 目标

**一键部署10000站到Cloudflare Pages**

---

## 📋 只需3步

### 第1步：安装Wrangler

**打开PowerShell，运行命令：**
```powershell
npm install -g wrangler
```

**等待安装完成（约1-2分钟）**

---

### 第2步：认证Wrangler

**运行命令：**
```powershell
wrangler login
```

**在浏览器中：**
- 登录Cloudflare账号
- 授权Wrangler访问
- 完成认证

---

### 第3步：运行自动化脚本

**运行命令：**
```powershell
python core-engine/auto_deploy.py
```

**脚本会自动完成：**
- 检查环境
- 删除wrangler.toml
- 部署到Cloudflare Pages
- 验证部署结果

---

## ✅ 部署完成后

**访问URL：**
- https://navigation-matrix-10000.pages.dev

**超级总站：**
- https://navigation-matrix-10000.pages.dev/03-central-hub/index.html

---

## 🔧 如果遇到问题

### Q1: npm未安装

**解决方案：**
- 安装Node.js：https://nodejs.org
- 安装后重启PowerShell

### Q2: Wrangler安装失败

**解决方案：**
- 检查网络连接
- 使用管理员权限运行PowerShell

### Q3: Wrangler认证失败

**解决方案：**
- 检查Cloudflare账号是否正确
- 清除浏览器缓存后重试

---

## 💡 优势

**自动化脚本优势：**
- 一键完成所有配置
- 自动检查环境
- 自动删除错误文件
- 自动部署站点
- 自动验证结果

**无需手动操作：**
- 无需手动配置Cloudflare Pages
- 无需手动修改构建设置
- 无需手动触发部署

---

## 📊 部署统计

**预计时间：**
- 安装Wrangler：1-2分钟
- 认证Wrangler：1分钟
- 运行脚本：5-10分钟
- **总计：7-13分钟**

---

## ✅ 检查清单

**运行脚本前检查：**
- [ ] Node.js已安装
- [ ] npm已安装
- [ ] Wrangler已安装
- [ ] Wrangler已认证
- [ ] Git已安装
- [ ] GitHub仓库已创建

**运行脚本后检查：**
- [ ] 脚本运行成功
- [ ] 部署成功
- [ ] 访问URL正常
- [ ] 站点数量正确

---

**告诉我"准备好了"，我会指导您运行脚本。**