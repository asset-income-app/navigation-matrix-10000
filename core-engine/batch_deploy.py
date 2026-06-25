#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量部署系统 - batch_deploy.py
一键部署1000站到Cloudflare Pages
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).parent.parent
SITES_DIR = ROOT_DIR / "02-sites"
HUB_DIR = ROOT_DIR / "03-central-hub"
DATA_DIR = ROOT_DIR / "data"
DEPLOYED_DIR = ROOT_DIR / "05-deployed"

def check_wrangler():
    """检查Wrangler是否安装"""
    try:
        result = subprocess.run(["wrangler", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Wrangler已安装")
            return True
    except FileNotFoundError:
        print("❌ Wrangler未安装")
        return False
    return False

def install_wrangler():
    """安装Wrangler"""
    print("\n安装Wrangler...")
    print("运行: npm install -g wrangler")
    
    try:
        result = subprocess.run(["npm", "install", "-g", "wrangler"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Wrangler安装成功")
            return True
        else:
            print(f"❌ 安装失败: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ npm未安装，请先安装Node.js")
        return False

def wrangler_login():
    """Wrangler登录"""
    print("\n登录Cloudflare...")
    print("运行: wrangler login")
    
    try:
        subprocess.run(["wrangler", "login"], check=True)
        print("✅ 登录成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ 登录失败")
        return False

def deploy_single_site(site_name, site_type):
    """部署单个站点"""
    site_dir = SITES_DIR / site_type / site_name
    
    if not site_dir.exists():
        print(f"❌ 站点不存在: {site_name}")
        return False
    
    try:
        # 使用wrangler pages deploy
        cmd = [
            "wrangler", "pages", "deploy",
            str(site_dir),
            "--project-name", f"{site_name}-nav"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {site_name} 部署成功")
            return True
        else:
            print(f"❌ {site_name} 部署失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {site_name} 部署异常: {e}")
        return False

def deploy_hub():
    """部署超级总站"""
    print("\n部署超级总站...")
    
    try:
        cmd = [
            "wrangler", "pages", "deploy",
            str(HUB_DIR),
            "--project-name", "daohangbaike-nav"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 超级总站部署成功")
            print("   URL: https://daohangbaike-nav.pages.dev")
            return True
        else:
            print(f"❌ 超级总站部署失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 超级总站部署异常: {e}")
        return False

def batch_deploy(max_sites=None):
    """批量部署所有站点"""
    print("\n" + "="*60)
    print("🚀 批量部署系统 - Cloudflare Pages")
    print("="*60)
    
    # 检查Wrangler
    if not check_wrangler():
        if not install_wrangler():
            print("\n请手动安装Wrangler:")
            print("  npm install -g wrangler")
            return
    
    # 登录
    if not wrangler_login():
        print("\n请手动登录:")
        print("  wrangler login")
        return
    
    # 部署超级总站
    deploy_hub()
    
    # 部署所有站点
    deployed = 0
    failed = 0
    
    for site_type in ['cities', 'niches', 'hybrids']:
        type_dir = SITES_DIR / site_type
        if not type_dir.exists():
            continue
        
        sites = [d.name for d in type_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        if max_sites:
            sites = sites[:max_sites]
        
        print(f"\n部署 {site_type} 类型站点 ({len(sites)} 个)...")
        
        for i, site_name in enumerate(sites, 1):
            print(f"\n[{i}/{len(sites)}] 部署: {site_name}")
            
            if deploy_single_site(site_name, site_type):
                deployed += 1
            else:
                failed += 1
    
    # 生成部署报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "total": deployed + failed,
        "deployed": deployed,
        "failed": failed,
        "success_rate": f"{deployed / (deployed + failed) * 100:.1f}%"
    }
    
    report_file = DEPLOYED_DIR / "deployment_report.json"
    report_file.write_text(json.dumps(report, indent=2))
    
    print("\n" + "="*60)
    print("📊 部署报告")
    print("="*60)
    print(f"总站点数: {report['total']}")
    print(f"部署成功: {report['deployed']}")
    print(f"部署失败: {report['failed']}")
    print(f"成功率: {report['success_rate']}")
    print(f"报告文件: {report_file}")
    print("="*60)

def generate_git_deployment_guide():
    """生成Git部署指南"""
    guide_file = ROOT_DIR / "GIT_DEPLOY_GUIDE.md"
    
    guide_content = """# Git自动部署方案（推荐）

## 优势
- 一次推送，自动部署所有站点
- 无需手动操作，Cloudflare自动构建
- 支持增量更新，只推送变更部分

## 步骤

### 1. 创建GitHub仓库
```bash
# 在GitHub创建新仓库: navigation-matrix-unified
# 不要添加README、.gitignore等文件
```

### 2. 初始化本地Git
```bash
cd e:\\50\\navigation-matrix-unified
git init
git add .
git commit -m "初始提交: 1000站导航矩阵"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/navigation-matrix-unified.git
git push -u origin main
```

### 3. 连接Cloudflare Pages
1. 登录 Cloudflare Dashboard: https://dash.cloudflare.com/
2. 进入 Pages 页面
3. 点击 "Create a project"
4. 选择 "Connect to Git"
5. 选择 GitHub 仓库: navigation-matrix-unified
6. 配置构建:
   - Production branch: main
   - Build command: (留空)
   - Build output directory: 02-sites
7. 点击 "Save and Deploy"

### 4. 自动部署
- 每次推送代码，Cloudflare自动部署
- 无需手动操作
- 部署时间: 约5-10分钟（首次）
- 后续更新: 只部署变更部分

## 站点访问地址
- 超级总站: https://navigation-matrix-unified.pages.dev
- 城市站: https://{city}-nav.pages.dev
- 行业站: https://{niche}-nav.pages.dev
- 组合站: https://{niche}-{city}-nav.pages.dev

## 注意事项
1. 首次推送可能需要较长时间（1000站）
2. 建议使用 .gitignore 排除不必要的文件
3. Cloudflare Pages免费额度: 500次构建/月
"""
    
    guide_file.write_text(guide_content)
    print(f"\n✅ Git部署指南已生成: {guide_file}")

def generate_wrangler_batch_script():
    """生成Wrangler批量部署脚本"""
    script_file = ROOT_DIR / "deploy_batch.ps1"
    
    script_content = """# Wrangler批量部署脚本
# 使用方法: .\\deploy_batch.ps1

# 检查Wrangler
if (-not (Get-Command wrangler -ErrorAction SilentlyContinue)) {
    Write-Host "安装Wrangler..."
    npm install -g wrangler
}

# 登录Cloudflare
Write-Host "登录Cloudflare..."
wrangler login

# 部署超级总站
Write-Host "部署超级总站..."
wrangler pages deploy 03-central-hub --project-name daohangbaike-nav

# 部署城市站
Write-Host "部署城市站..."
Get-ChildItem -Directory 02-sites\\cities | ForEach-Object {
    $name = $_.Name
    Write-Host "部署: $name"
    wrangler pages deploy "02-sites\\cities\\$name" --project-name "$name-nav"
}

# 部署行业站
Write-Host "部署行业站..."
Get-ChildItem -Directory 02-sites\\niches | ForEach-Object {
    $name = $_.Name
    Write-Host "部署: $name"
    wrangler pages deploy "02-sites\\niches\\$name" --project-name "$name-nav"
}

# 部署组合站
Write-Host "部署组合站..."
Get-ChildItem -Directory 02-sites\\hybrids | ForEach-Object {
    $name = $_.Name
    Write-Host "部署: $name"
    wrangler pages deploy "02-sites\\hybrids\\$name" --project-name "$name-nav"
}

Write-Host "部署完成!"
"""
    
    script_file.write_text(script_content)
    print(f"\n✅ Wrangler批量脚本已生成: {script_file}")

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            check_wrangler()
        elif command == "install":
            install_wrangler()
        elif command == "login":
            wrangler_login()
        elif command == "hub":
            deploy_hub()
        elif command == "batch":
            max_sites = int(sys.argv[2]) if len(sys.argv) > 2 else None
            batch_deploy(max_sites)
        elif command == "guide":
            generate_git_deployment_guide()
            generate_wrangler_batch_script()
        else:
            print("用法: python batch_deploy.py [check|install|login|hub|batch|guide]")
    else:
        # 默认生成指南
        generate_git_deployment_guide()
        generate_wrangler_batch_script()
        
        print("\n" + "="*60)
        print("🚀 部署方案")
        print("="*60)
        print("\n推荐方案: Git自动部署")
        print("  1. 推送到GitHub")
        print("  2. Cloudflare Pages自动构建")
        print("  3. 无需手动操作")
        print("\n备选方案: Wrangler批量部署")
        print("  1. 运行: .\\deploy_batch.ps1")
        print("  2. 自动部署所有站点")
        print("\n详细指南: GIT_DEPLOY_GUIDE.md")
        print("="*60)

if __name__ == "__main__":
    main()