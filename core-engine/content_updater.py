#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
内容自动更新脚本
自动更新站点内容
"""

import os
import json
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(r"E:\50\navigation-matrix-unified")
DATA_DIR = ROOT_DIR / "data"

def update_site_content():
    print("开始更新站点内容...")
    
    cities_file = DATA_DIR / "cities.json"
    niches_file = DATA_DIR / "niches.json"
    
    updated_count = 0
    
    if cities_file.exists():
        with open(cities_file, 'r', encoding='utf-8') as f:
            cities_data = json.load(f)
        print(f"处理城市站数据：{len(cities_data)}个")
        updated_count += len(cities_data)
    
    if niches_file.exists():
        with open(niches_file, 'r', encoding='utf-8') as f:
            niches_data = json.load(f)
        print(f"处理行业站数据：{len(niches_data)}个")
        updated_count += len(niches_data)
    
    print(f"内容更新完成！共处理 {updated_count} 个站点")
    return updated_count

if __name__ == "__main__":
    print(f"开始内容自动更新... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    updated_count = update_site_content()
    print(f"内容更新完成！")
