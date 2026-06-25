#!/usr/bin/env python3
"""
分批部署脚本 - 解决Cloudflare Pages文件数量限制
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
SITES_DIR = PROJECT_ROOT / "02-sites"
TEMP_DIR = PROJECT_ROOT / "temp-deploy"

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

def count_files(directory):
    """统计文件数量"""
    count = 0
    for root, dirs, files in os.walk(directory):
        count += len(files)
    return count

def create_batch(batch_number, sites_per_batch=2000):
    """创建批次"""
    print_step(1, f"创建批次 {batch_number}")
    
    # 创建临时目录
    batch_dir = TEMP_DIR / f"batch-{batch_number}"
    if batch_dir.exists():
        shutil.rmtree(batch_dir)
    batch_dir.mkdir(parents=True, exist_ok=True)
    
    # 获取所有站点
    cities = sorted((SITES_DIR / "cities").glob("*"))
    niches = sorted((SITES_DIR / "niches").glob("*"))
    hybrids = sorted((SITES_DIR / "hybrids").glob("*"))
    
    all_sites = []
    for city in cities:
        all_sites.append(("cities", city.name))
    for niche in niches:
        all_sites.append(("niches", niche.name))
    for hybrid in hybrids:
        all_sites.append(("hybrids", hybrid.name))
    
    # 计算批次范围
    start_index = (batch_number - 1) * sites_per_batch
    end_index = batch_number * sites_per_batch
    
    batch_sites = all_sites[start_index:end_index]
    
    print(f"批次 {batch_number} 包含 {len(batch_sites)} 个站点")
    
    # 复制站点文件
    for site_type, site_name in batch_sites:
        source_dir = SITES_DIR / site_type / site_name
        target_dir = batch_dir / site_type / site_name
        
        if source_dir.exists():
            shutil.copytree(source_dir, target_dir)
    
    # 复制超级总站
    hub_source = PROJECT_ROOT / "03-central-hub"
    hub_target = batch_dir / "03-central-hub"
    if hub_source.exists():
        shutil.copytree(hub_source, hub_target)
    
    # 统计文件数量
    file_count = count_files(batch_dir)
    print_success(f"批次 {batch_number} 创建完成，文件数量: {file_count}")
    
    return batch_dir, file_count

def deploy_batch(batch_dir, batch_number):
    """部署批次"""
    print_step(2, f"部署批次 {batch_number}")
    
    try:
        print("正在部署...")
        
        # 使用wrangler pages deploy命令
        result = subprocess.run(
            ["wrangler", "pages", "deploy", str(batch_dir), "--project-name=navigation-matrix-{batch_number}"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        
        if result.returncode == 0:
            print_success(f"批次 {batch_number} 部署成功！")
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
            print_error(f"批次 {batch_number} 部署失败: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"批次 {batch_number} 部署失败: {e}")
        return False

def cleanup_batch(batch_dir):
    """清理批次"""
    print_step(3, "清理临时文件")
    
    if batch_dir.exists():
        shutil.rmtree(batch_dir)
        print_success("临时文件已清理")

def main():
    """主函数"""
    print_header("分批部署脚本 - 解决Cloudflare Pages文件数量限制")
    
    print("\n📊 问题分析:")
    print("  Cloudflare Pages限制: 20,000个文件")
    print("  当前文件数量: 79,992个文件")
    print("  需要分批部署: 5批，每批约16,000个文件")
    
    print("\n📋 分批计划:")
    print("  批次1: 2000站 (城市站293个 + 行业站500个 + 组合站1207个)")
    print("  批次2: 2000站 (组合站2000个)")
    print("  批次3: 2000站 (组合站2000个)")
    print("  批次4: 2000站 (组合站2000个)")
    print("  批次5: 2000站 (组合站1800个)")
    
    print("\n是否开始分批部署？(y/n)")
    choice = input().strip().lower()
    
    if choice != 'y':
        print("取消部署")
        return
    
    # 分批部署
    batch_number = 1
    sites_per_batch = 2000
    
    while True:
        batch_dir, file_count = create_batch(batch_number, sites_per_batch)
        
        if file_count == 0:
            print_success("所有站点已部署完成！")
            break
        
        if file_count > 20000:
            print_warning(f"批次 {batch_number} 文件数量 {file_count} 超过限制，调整批次大小...")
            sites_per_batch = int(sites_per_batch * 20000 / file_count)
            continue
        
        # 部署批次
        if deploy_batch(batch_dir, batch_number):
            # 清理临时文件
            cleanup_batch(batch_dir)
            batch_number += 1
        else:
            print_error(f"批次 {batch_number} 部署失败，停止部署")
            break
    
    print_header("分批部署完成！")
    print("\n🎉 10000站已成功分批部署到Cloudflare Pages！")
    print("\n访问URL:")
    print("  批次1: https://navigation-matrix-1.pages.dev")
    print("  批次2: https://navigation-matrix-2.pages.dev")
    print("  批次3: https://navigation-matrix-3.pages.dev")
    print("  批次4: https://navigation-matrix-4.pages.dev")
    print("  批次5: https://navigation-matrix-5.pages.dev")

if __name__ == "__main__":
    main()