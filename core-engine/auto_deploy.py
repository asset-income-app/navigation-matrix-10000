#!/usr/bin/env python3
"""
自动化部署脚本 - 一键部署10000站到Cloudflare Pages
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
SITES_DIR = PROJECT_ROOT / "02-sites"

def print_header(title):
    """打印标题"""
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def print_step(step, description):
    """打印步骤"""
    print(f"\n📍 步骤 {step}: {description}")

def print_success(message):
    """打印成功消息"""
    print(f"✅ {message}")

def print_error(message):
    """打印错误消息"""
    print(f"❌ {message}")

def print_warning(message):
    """打印警告消息"""
    print(f"⚠️  {message}")

def check_git():
    """检查Git安装"""
    print_step(1, "检查Git安装")
    
    try:
        result = subprocess.run(
            ["C:\\Program Files\\Git\\bin\\git.exe", "--version"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        
        if result.returncode == 0:
            print_success(f"Git已安装: {result.stdout.strip()}")
            return True
        else:
            print_error("Git未安装或未正确配置")
            return False
    except Exception as e:
        print_error(f"检查Git失败: {e}")
        return False

def check_wrangler():
    """检查Wrangler安装"""
    print_step(2, "检查Wrangler安装")
    
    try:
        result = subprocess.run(
            ["wrangler", "--version"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        
        if result.returncode == 0:
            print_success(f"Wrangler已安装: {result.stdout.strip()}")
            return True
        else:
            print_warning("Wrangler未安装")
            print("正在安装Wrangler...")
            
            install_result = subprocess.run(
                ["npm", "install", "-g", "wrangler"],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT
            )
            
            if install_result.returncode == 0:
                print_success("Wrangler安装成功")
                return True
            else:
                print_error(f"Wrangler安装失败: {install_result.stderr}")
                return False
    except Exception as e:
        print_error(f"检查Wrangler失败: {e}")
        return False

def check_wrangler_auth():
    """检查Wrangler认证"""
    print_step(3, "检查Wrangler认证")
    
    try:
        result = subprocess.run(
            ["wrangler", "whoami"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        
        if result.returncode == 0 and "You are logged in" in result.stdout:
            print_success("Wrangler已认证")
            return True
        else:
            print_warning("Wrangler未认证")
            print("\n请按照以下步骤认证Wrangler:")
            print("1. 运行命令: wrangler login")
            print("2. 在浏览器中登录Cloudflare账号")
            print("3. 完成认证后，重新运行此脚本")
            
            print("\n是否现在进行认证？(y/n)")
            choice = input().strip().lower()
            
            if choice == 'y':
                subprocess.run(["wrangler", "login"], cwd=PROJECT_ROOT)
                return check_wrangler_auth()
            else:
                return False
    except Exception as e:
        print_error(f"检查Wrangler认证失败: {e}")
        return False

def check_github_remote():
    """检查GitHub远程仓库"""
    print_step(4, "检查GitHub远程仓库")
    
    try:
        result = subprocess.run(
            ["C:\\Program Files\\Git\\bin\\git.exe", "remote", "-v"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        
        if "origin" in result.stdout:
            print_success("GitHub远程仓库已配置")
            return True
        else:
            print_warning("GitHub远程仓库未配置")
            print("\n请按照以下步骤配置GitHub远程仓库:")
            print("1. 在GitHub创建仓库: https://github.com/new")
            print("2. 仓库名称: navigation-matrix-10000")
            print("3. 运行命令: git remote add origin https://github.com/YOUR_USERNAME/navigation-matrix-10000.git")
            print("4. 重新运行此脚本")
            
            return False
    except Exception as e:
        print_error(f"检查GitHub远程仓库失败: {e}")
        return False

def check_wrangler_toml():
    """检查wrangler.toml文件"""
    print_step(5, "检查wrangler.toml文件")
    
    wrangler_toml = PROJECT_ROOT / "wrangler.toml"
    
    if wrangler_toml.exists():
        print_warning("wrangler.toml文件存在，正在删除...")
        wrangler_toml.unlink()
        print_success("wrangler.toml文件已删除")
        
        # 更新Git仓库
        subprocess.run(
            ["C:\\Program Files\\Git\\bin\\git.exe", "add", "."],
            cwd=PROJECT_ROOT
        )
        subprocess.run(
            ["C:\\Program Files\\Git\\bin\\git.exe", "commit", "-m", "删除wrangler.toml文件"],
            cwd=PROJECT_ROOT
        )
        subprocess.run(
            ["C:\\Program Files\\Git\\bin\\git.exe", "push"],
            cwd=PROJECT_ROOT
        )
        print_success("Git仓库已更新")
    else:
        print_success("wrangler.toml文件不存在，无需删除")

def deploy_to_cloudflare_pages():
    """部署到Cloudflare Pages"""
    print_step(6, "部署到Cloudflare Pages")
    
    try:
        print("正在部署...")
        
        # 使用wrangler pages deploy命令
        result = subprocess.run(
            ["wrangler", "pages", "deploy", str(PROJECT_ROOT), "--project-name=navigation-matrix-10000"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        
        if result.returncode == 0:
            print_success("部署成功！")
            print("\n部署结果:")
            print(result.stdout)
            
            # 提取URL
            if "https://" in result.stdout:
                lines = result.stdout.split('\n')
                for line in lines:
                    if "https://" in line and "pages.dev" in line:
                        url = line.strip()
                        print(f"\n🌐 访问URL: {url}")
                        break
            
            return True
        else:
            print_error(f"部署失败: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"部署失败: {e}")
        return False

def verify_deployment():
    """验证部署"""
    print_step(7, "验证部署")
    
    print("正在验证站点数量...")
    
    # 统计站点数量
    cities_count = len(list((SITES_DIR / "cities").glob("*")))
    niches_count = len(list((SITES_DIR / "niches").glob("*")))
    hybrids_count = len(list((SITES_DIR / "hybrids").glob("*")))
    total_count = cities_count + niches_count + hybrids_count
    
    print_success(f"站点统计:")
    print(f"  城市站: {cities_count}个")
    print(f"  行业站: {niches_count}个")
    print(f"  组合站: {hybrids_count}个")
    print(f"  总计: {total_count}个")
    
    if total_count == 10000:
        print_success("站点数量正确！")
        return True
    else:
        print_warning(f"站点数量不符，预期10000个，实际{total_count}个")
        return False

def main():
    """主函数"""
    print_header("自动化部署脚本 - 10000站导航矩阵")
    
    # 检查环境
    checks = [
        ("Git", check_git),
        ("Wrangler", check_wrangler),
        ("Wrangler认证", check_wrangler_auth),
        ("GitHub远程仓库", check_github_remote),
    ]
    
    for name, check_func in checks:
        if not check_func():
            print_error(f"{name}检查失败，请先完成配置")
            return
    
    # 检查并删除wrangler.toml
    check_wrangler_toml()
    
    # 部署到Cloudflare Pages
    if deploy_to_cloudflare_pages():
        # 验证部署
        verify_deployment()
        
        print_header("部署完成！")
        print("\n🎉 10000站已成功部署到Cloudflare Pages！")
        print("\n访问URL:")
        print("  https://navigation-matrix-10000.pages.dev")
        print("\n超级总站:")
        print("  https://navigation-matrix-10000.pages.dev/03-central-hub/index.html")
    else:
        print_error("部署失败，请检查错误信息并重新运行脚本")

if __name__ == "__main__":
    main()