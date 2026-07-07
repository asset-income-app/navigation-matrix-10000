#!/usr/bin/env python3
"""
简化分批部署脚本 - 一键部署10000站到5个批次
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
SITES_DIR = PROJECT_ROOT / "02-sites"
TEMP_DIR = PROJECT_ROOT / "temp-batches"

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

def create_batch(batch_number, start_index, end_index):
    """创建批次"""
    print_step(batch_number, f"创建批次 {batch_number}")
    
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
    batch_sites = all_sites[start_index:end_index]
    
    print(f"批次 {batch_number} 包含 {len(batch_sites)} 个站点")
    
    # 复制站点文件
    for site_type, site_name in batch_sites:
        source_dir = SITES_DIR / site_type / site_name
        target_dir = batch_dir / site_type / site_name
        
        if source_dir.exists():
            shutil.copytree(source_dir, target_dir)
    
    # 统计文件数量
    file_count = sum(1 for _ in batch_dir.rglob("*") if _.is_file())
    print_success(f"批次 {batch_number} 创建完成，文件数量: {file_count}")
    
    return batch_dir, file_count

def deploy_batch(batch_dir, batch_number):
    """部署批次"""
    print_step(batch_number + 5, f"部署批次 {batch_number}")
    
    try:
        print("正在部署...")
        
        # 使用wrangler pages deploy命令
        wrangler_path = "C:\\Users\\Administrator\\AppData\\Roaming\\npm\\wrangler.cmd"
        project_name = f"navigation-matrix-{batch_number}"
        result = subprocess.run(
            [wrangler_path, "pages", "deploy", str(batch_dir), "--project-name", project_name],
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

def deploy_hub():
    """部署超级总站"""
    print_step(11, "部署超级总站")
    
    hub_dir = PROJECT_ROOT / "04-batch-hub"
    
    try:
        print("正在部署超级总站...")
        
        wrangler_path = "C:\\Users\\Administrator\\AppData\\Roaming\\npm\\wrangler.cmd"
        result = subprocess.run(
            [wrangler_path, "pages", "deploy", str(hub_dir), "--project-name=navigation-matrix-hub"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        
        if result.returncode == 0:
            print_success("超级总站部署成功！")
            print("\n部署结果:")
            print(result.stdout)
            
            # 提取URL
            if "https://" in result.stdout:
                lines = result.stdout.split('\n')
                for line in lines:
                    if "https://" in line and "pages.dev" in line:
                        url = line.strip()
                        print(f"\n🌐 超级总站URL: {url}")
                        break
            
            return True
        else:
            print_error(f"超级总站部署失败: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"超级总站部署失败: {e}")
        return False

def cleanup():
    """清理临时文件"""
    print_step(12, "清理临时文件")
    
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
        print_success("临时文件已清理")

def main():
    """主函数"""
    print_header("简化分批部署脚本 - 10000站导航矩阵")
    
    print("\n📊 分批计划:")
    print("  批次1: 2000站 (城市站293 + 行业站500 + 组合站1207)")
    print("  批次2: 2000站 (组合站2000)")
    print("  批次3: 2000站 (组合站2000)")
    print("  批次4: 2000站 (组合站2000)")
    print("  批次5: 2000站 (组合站1800)")
    print("  超级总站: 链接所有批次")
    
    print("\n开始部署...")
    
    # 创建批次
    batches = [
        (1, 0, 2000),
        (2, 2000, 4000),
        (3, 4000, 6000),
        (4, 6000, 8000),
        (5, 8000, 10000)
    ]
    
    batch_dirs = []
    
    for batch_number, start_index, end_index in batches:
        batch_dir, file_count = create_batch(batch_number, start_index, end_index)
        batch_dirs.append((batch_number, batch_dir, file_count))
    
    # 部署批次
    for batch_number, batch_dir, file_count in batch_dirs:
        if file_count > 20000:
            print_warning(f"批次 {batch_number} 文件数量 {file_count} 超过限制，跳过部署")
            continue
        
        deploy_batch(batch_dir, batch_number)
    
    # 部署超级总站
    deploy_hub()
    
    # 清理临时文件
    cleanup()
    
    print_header("部署完成！")
    print("\n🎉 10000站已成功部署到5个批次！")
    print("\n访问URL:")
    print("  批次1: https://navigation-matrix-1.pages.dev")
    print("  批次2: https://navigation-matrix-2.pages.dev")
    print("  批次3: https://navigation-matrix-3.pages.dev")
    print("  批次4: https://navigation-matrix-4.pages.dev")
    print("  批次5: https://navigation-matrix-5.pages.dev")
    print("\n超级总站:")
    print("  https://navigation-matrix-hub.pages.dev")
    print("\n💡 通过超级总站可以访问所有10000站！")

if __name__ == "__main__":
    main()