#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署辅助系统 - deploy_helper.py
辅助Cloudflare Pages部署，生成部署清单和配置
"""

import os
import json
from datetime import datetime
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
SITES_DIR = ROOT_DIR / "02-sites"
DEPLOYED_DIR = ROOT_DIR / "05-deployed"

def generate_deploy_list():
    """生成部署清单"""
    print("\n" + "="*60)
    print("📝 生成部署清单")
    print("="*60)
    
    deploy_list = []
    
    for site_type in ['cities', 'niches', 'hybrids']:
        type_dir = SITES_DIR / site_type
        if not type_dir.exists():
            continue
        
        for site_dir in type_dir.iterdir():
            if site_dir.is_dir() and not site_dir.name.startswith('.'):
                config_file = site_dir / "config.json"
                if config_file.exists():
                    config = json.loads(config_file.read_text())
                    
                    deploy_item = {
                        "name": site_dir.name,
                        "type": site_type,
                        "displayName": config.get('cityName') or config.get('nicheName') or site_dir.name,
                        "path": str(site_dir.relative_to(ROOT_DIR)),
                        "url": f"https://{site_dir.name}-nav.pages.dev",
                        "files": [f.name for f in site_dir.iterdir() if f.is_file()]
                    }
                    deploy_list.append(deploy_item)
    
    # 保存清单
    deploy_file = DEPLOYED_DIR / "deploy_list.json"
    deploy_file.parent.mkdir(parents=True, exist_ok=True)
    deploy_file.write_text(json.dumps(deploy_list, indent=2))
    
    print(f"✅ 已生成部署清单: {len(deploy_list)} 个站点")
    print(f"文件: {deploy_file}")
    
    return deploy_list

def generate_wrangler_config():
    """生成Wrangler配置"""
    print("\n" + "="*60)
    print("📝 生成Wrangler配置")
    print("="*60)
    
    config = {
        "name": "navigation-matrix-unified",
        "compatibility_date": "2024-01-01",
        "pages_build_output_dir": "02-sites"
    }
    
    config_file = ROOT_DIR / "wrangler.toml"
    config_content = f"""
name = "{config['name']}"
compatibility_date = "{config['compatibility_date']}"
pages_build_output_dir = "{config['pages_build_output_dir']}"

# 部署配置
[site]
bucket = "./02-sites"
"""
    
    config_file.write_text(config_content)
    print(f"✅ 已生成: {config_file}")

def generate_deployment_guide():
    """生成部署指南"""
    print("\n" + "="*60)
    print("📝 生成部署指南")
    print("="*60)
    
    guide = """# Cloudflare Pages 部署指南

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

"""
    
    # 添加站点列表
    deploy_list = generate_deploy_list()
    
    for site in deploy_list[:20]:
        guide += f"- [{site['displayName']}]({site['url']}) ({site['type']})\n"
    
    guide += f"\n... 共 {len(deploy_list)} 个站点\n"
    
    guide_file = ROOT_DIR / "DEPLOY_GUIDE.md"
    guide_file.write_text(guide)
    
    print(f"✅ 已生成: {guide_file}")

def show_deploy_status():
    """显示部署状态"""
    print("\n" + "="*60)
    print("📊 部署状态")
    print("="*60)
    
    # 读取管理数据
    management_file = DEPLOYED_DIR / "management.json"
    if management_file.exists():
        management = json.loads(management_file.read_text())
        
        print(f"总站点: {management['totalSites']}")
        print(f"城市站: {management['siteTypes']['city']}")
        print(f"行业站: {management['siteTypes']['niche']}")
        print(f"组合站: {management['siteTypes']['hybrid']}")
        print(f"总链接: {management['totalLinks']}")
        
        # 显示模板分布
        print("\n模板分布:")
        for variant, count in management['variants'].items():
            print(f"  {variant}: {count} 个")
    
    # 读取部署清单
    deploy_file = DEPLOYED_DIR / "deploy_list.json"
    if deploy_file.exists():
        deploy_list = json.loads(deploy_file.read_text())
        
        print(f"\n部署清单: {len(deploy_list)} 个站点")

def check_deploy_readiness():
    """检查部署准备状态"""
    print("\n" + "="*60)
    print("🔍 部署准备检查")
    print("="*60)
    
    checks = []
    
    # 检查必要文件
    required_files = [
        '01-templates/base/index.html',
        '01-templates/base/style.css',
        '01-templates/base/script.js',
        'data/cities.json',
        'data/niches.json',
        'data/master-links.json'
    ]
    
    for file in required_files:
        file_path = ROOT_DIR / file
        if file_path.exists():
            checks.append({"item": file, "status": "✅"})
        else:
            checks.append({"item": file, "status": "❌"})
    
    # 检查站点数量
    sites_count = sum(1 for _ in SITES_DIR.rglob("config.json"))
    checks.append({"item": f"站点数量: {sites_count}", "status": "✅" if sites_count > 0 else "❌"})
    
    # 检查站点完整性
    complete_sites = 0
    incomplete_sites = 0
    
    for site_type in ['cities', 'niches', 'hybrids']:
        type_dir = SITES_DIR / site_type
        if type_dir.exists():
            for site_dir in type_dir.iterdir():
                if site_dir.is_dir():
                    has_index = (site_dir / "index.html").exists()
                    has_config = (site_dir / "config.json").exists()
                    
                    if has_index and has_config:
                        complete_sites += 1
                    else:
                        incomplete_sites += 1
    
    checks.append({"item": f"完整站点: {complete_sites}", "status": "✅"})
    checks.append({"item": f"不完整站点: {incomplete_sites}", "status": "⚠️" if incomplete_sites > 0 else "✅"})
    
    # 显示检查结果
    for check in checks:
        print(f"{check['status']} {check['item']}")
    
    # 总结
    ready = all(c['status'] == '✅' for c in checks)
    
    print("\n" + "="*60)
    if ready:
        print("✅ 部署准备完成，可以开始部署")
    else:
        print("⚠️ 存在问题，请先修复")
    print("="*60)

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "list":
            generate_deploy_list()
        elif command == "config":
            generate_wrangler_config()
        elif command == "guide":
            generate_deployment_guide()
        elif command == "status":
            show_deploy_status()
        elif command == "check":
            check_deploy_readiness()
        elif command == "prepare":
            generate_deploy_list()
            generate_wrangler_config()
            generate_deployment_guide()
            check_deploy_readiness()
        else:
            print("用法: python deploy_helper.py [list|config|guide|status|check|prepare]")
    else:
        # 默认检查准备状态
        check_deploy_readiness()

if __name__ == "__main__":
    main()