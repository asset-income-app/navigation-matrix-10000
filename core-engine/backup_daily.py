#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
每日数据备份脚本
自动备份所有重要数据文件
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(r"E:\50\navigation-matrix-unified")
DATA_DIR = ROOT_DIR / "data"
BACKUP_DIR = ROOT_DIR / "backups"

BACKUP_FILES = [
    "cities.json",
    "niches.json",
    "hybrids.json",
    "site_content.json",
    "automation_config.json",
    "monetization_config.json"
]

def create_daily_backup():
    today = datetime.now().strftime("%Y-%m-%d")
    daily_backup_dir = BACKUP_DIR / f"daily_{today}"
    daily_backup_dir.mkdir(parents=True, exist_ok=True)
    
    backup_count = 0
    for filename in BACKUP_FILES:
        source_file = DATA_DIR / filename
        if source_file.exists():
            dest_file = daily_backup_dir / filename
            shutil.copy2(source_file, dest_file)
            backup_count += 1
            print(f"已备份：{filename}")
    
    print(f"每日备份完成！共备份 {backup_count} 个文件")
    return backup_count

if __name__ == "__main__":
    print(f"开始每日数据备份... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    backup_count = create_daily_backup()
    print(f"每日备份完成！")
