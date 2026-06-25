#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成组合站数据文件 - generate_hybrids_data.py
"""

import json
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
SITES_DIR = ROOT_DIR / "02-sites" / "hybrids"
DATA_DIR = ROOT_DIR / "data"

def generate_hybrids_json():
    """生成组合站数据文件"""
    hybrids_data = []
    
    for site_dir in SITES_DIR.iterdir():
        if site_dir.is_dir() and not site_dir.name.startswith('.'):
            config_file = site_dir / "config.json"
            if config_file.exists():
                try:
                    config = json.loads(config_file.read_text(encoding='utf-8'))
                    # 添加sitePinyin字段（目录名）
                    config['sitePinyin'] = site_dir.name
                    hybrids_data.append(config)
                except json.JSONDecodeError:
                    print(f"  [ERROR] {site_dir.name} config.json 解析失败")
    
    # 保存数据文件
    output_file = DATA_DIR / "hybrids.json"
    output_file.write_text(json.dumps(hybrids_data, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"\n✅ 已生成 hybrids.json ({len(hybrids_data)} 个组合站)")
    return len(hybrids_data)

if __name__ == "__main__":
    generate_hybrids_json()