#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动备份系统 - auto_backup.py
自动备份所有站点数据和配置，防止数据丢失
"""

import os
import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
BACKUPS_DIR = DATA_DIR / "backups"
SITES_DIR = ROOT_DIR / "02-sites"

def backup_sites(backup_type="daily"):
    """备份所有站点"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    backup_dir = BACKUPS_DIR / backup_type / datetime.now().strftime("%Y-%m")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    backup_file = backup_dir / f"backup_{timestamp}.zip"
    
    print(f"🔄 开始备份 ({backup_type})...")
    
    # 创建zip备份
    with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # 备份站点数据
        for site_type in ['cities', 'niches', 'hybrids']:
            type_dir = SITES_DIR / site_type
            if type_dir.exists():
                for site_dir in type_dir.iterdir():
                    if site_dir.is_dir() and not site_dir.name.startswith('.'):
                        config_file = site_dir / "config.json"
                        if config_file.exists():
                            zf.write(config_file, f"{site_type}/{site_dir.name}/config.json")
        
        # 备份数据文件
        for data_file in ['cities.json', 'niches.json', 'master-links.json', 'template-assignment.json']:
            file_path = DATA_DIR / data_file
            if file_path.exists():
                zf.write(file_path, f"data/{data_file}")
        
        # 备份管理数据
        management_file = ROOT_DIR / "05-deployed" / "management.json"
        if management_file.exists():
            zf.write(management_file, "management.json")
    
    # 记录备份信息
    backup_info = {
        "timestamp": timestamp,
        "type": backup_type,
        "file": str(backup_file),
        "size_kb": backup_file.stat().st_size / 1024,
        "sites_count": sum(1 for _ in SITES_DIR.rglob("config.json")),
        "created_at": datetime.now().isoformat()
    }
    
    info_file = backup_dir / f"backup_{timestamp}_info.json"
    info_file.write_text(json.dumps(backup_info, indent=2))
    
    print(f"✅ 备份完成: {backup_file.name}")
    print(f"   大小: {backup_info['size_kb']:.1f} KB")
    print(f"   站点: {backup_info['sites_count']} 个")
    
    return backup_file

def backup_single_site(site_name, site_type):
    """备份单个站点"""
    site_dir = SITES_DIR / site_type / site_name
    if not site_dir.exists():
        print(f"❌ 站点不存在: {site_name}")
        return None
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    backup_dir = BACKUPS_DIR / "manual" / datetime.now().strftime("%Y-%m")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    backup_file = backup_dir / f"{site_name}_{timestamp}.zip"
    
    with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in site_dir.iterdir():
            if file.is_file():
                zf.write(file, file.name)
    
    print(f"✅ 站点备份完成: {backup_file.name}")
    return backup_file

def list_backups(backup_type=None):
    """列出所有备份"""
    print("\n" + "="*60)
    print("📦 备份列表")
    print("="*60)
    
    backup_types = [backup_type] if backup_type else ['daily', 'manual']
    
    for bt in backup_types:
        type_dir = BACKUPS_DIR / bt
        if not type_dir.exists():
            continue
        
        print(f"\n{bt}备份:")
        
        for month_dir in sorted(type_dir.iterdir()):
            if month_dir.is_dir():
                backups = sorted(month_dir.glob("backup_*.zip"))
                for backup in backups[-5:]:  # 只显示最近5个
                    info_file = backup.parent / f"{backup.stem}_info.json"
                    if info_file.exists():
                        info = json.loads(info_file.read_text())
                        print(f"  📦 {backup.name}")
                        print(f"     时间: {info['timestamp']}")
                        print(f"     大小: {info['size_kb']:.1f} KB")
                        print(f"     站点: {info['sites_count']} 个")

def restore_backup(backup_file):
    """恢复备份"""
    backup_path = Path(backup_file)
    if not backup_path.exists():
        print(f"❌ 备份文件不存在: {backup_file}")
        return False
    
    print(f"🔄 开始恢复: {backup_path.name}")
    
    # 先备份当前状态
    print("⚠️  先备份当前状态...")
    backup_sites("manual")
    
    # 解压恢复
    with zipfile.ZipFile(backup_path, 'r') as zf:
        zf.extractall(ROOT_DIR)
    
    print(f"✅ 恢复完成")
    return True

def cleanup_old_backups(keep_days=30):
    """清理旧备份"""
    print("🧹 清理旧备份...")
    
    cutoff = datetime.now() - timedelta(days=keep_days)
    
    for backup_type in ['daily', 'manual']:
        type_dir = BACKUPS_DIR / backup_type
        if not type_dir.exists():
            continue
        
        for month_dir in type_dir.iterdir():
            if month_dir.is_dir():
                for backup in month_dir.glob("backup_*.zip"):
                    # 从文件名提取时间
                    timestamp_str = backup.stem.replace("backup_", "").split("_")[0]
                    try:
                        backup_time = datetime.strptime(timestamp_str, "%Y-%m-%d")
                        if backup_time < cutoff:
                            backup.unlink()
                            info_file = backup.parent / f"{backup.stem}_info.json"
                            if info_file.exists():
                                info_file.unlink()
                            print(f"  🗑️ 已删除: {backup.name}")
                    except:
                        pass
    
    print("✅ 清理完成")

def show_backup_stats():
    """显示备份统计"""
    print("\n" + "="*60)
    print("📊 备份统计")
    print("="*60)
    
    total_size = 0
    total_count = 0
    
    for backup_type in ['daily', 'manual']:
        type_dir = BACKUPS_DIR / backup_type
        if type_dir.exists():
            backups = list(type_dir.rglob("backup_*.zip"))
            count = len(backups)
            size = sum(b.stat().st_size for b in backups) / (1024 * 1024)  # MB
            
            total_count += count
            total_size += size
            
            print(f"\n{backup_type}:")
            print(f"  数量: {count} 个")
            print(f"  大小: {size:.2f} MB")
    
    print(f"\n总计:")
    print(f"  数量: {total_count} 个")
    print(f"  大小: {total_size:.2f} MB")

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "backup":
            backup_type = sys.argv[2] if len(sys.argv) > 2 else "daily"
            backup_sites(backup_type)
        elif command == "site":
            if len(sys.argv) >= 4:
                backup_single_site(sys.argv[2], sys.argv[3])
        elif command == "list":
            backup_type = sys.argv[2] if len(sys.argv) > 2 else None
            list_backups(backup_type)
        elif command == "restore":
            if len(sys.argv) >= 3:
                restore_backup(sys.argv[2])
        elif command == "cleanup":
            keep_days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            cleanup_old_backups(keep_days)
        elif command == "stats":
            show_backup_stats()
        else:
            print("用法: python auto_backup.py [backup|site|list|restore|cleanup|stats]")
    else:
        # 默认执行每日备份
        backup_sites("daily")

if __name__ == "__main__":
    main()