#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同步hybrids.json与实际生成的混合站目录
"""

import json
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
SITES_DIR = ROOT_DIR / "02-sites"
DATA_DIR = ROOT_DIR / "data"


def sync_hybrids():
    """从实际目录同步hybrids.json"""
    print("=" * 60)
    print("  同步混合站数据")
    print("=" * 60)
    
    hybrids_dir = SITES_DIR / 'hybrids'
    
    # 获取所有混合站目录
    hybrid_dirs = [d.name for d in hybrids_dir.iterdir() if d.is_dir()]
    print(f"混合站目录数: {len(hybrid_dirs)}")
    
    # 加载现有hybrids.json
    existing_hybrids = []
    try:
        with open(DATA_DIR / "hybrids.json", 'r', encoding='utf-8') as f:
            existing_hybrids = json.load(f)
        print(f"hybrids.json现有条目: {len(existing_hybrids)}")
    except:
        print("hybrids.json不存在或为空")
    
    # 创建sitePinyin集合用于快速查找
    existing_pinyins = set()
    for h in existing_hybrids:
        sp = h.get('sitePinyin', '')
        if sp:
            existing_pinyins.add(sp)
    
    # 从目录中读取config.json，构建新的hybrids数据
    new_hybrids = existing_hybrids.copy()
    added_count = 0
    
    for dir_name in hybrid_dirs:
        if dir_name not in existing_pinyins:
            # 尝试读取config.json
            config_path = hybrids_dir / dir_name / 'config.json'
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    new_entry = {
                        'siteType': 'hybrid',
                        'sitePinyin': dir_name,
                        'cityName': config.get('cityName', ''),
                        'nicheName': config.get('nicheName', ''),
                        'siteTitle': config.get('siteTitle', ''),
                        'siteDescription': config.get('siteDescription', ''),
                        'categories': config.get('categories', [])
                    }
                    new_hybrids.append(new_entry)
                    added_count += 1
                except:
                    pass
    
    print(f"新增条目: {added_count}")
    print(f"同步后总数: {len(new_hybrids)}")
    
    # 保存更新后的hybrids.json
    with open(DATA_DIR / "hybrids.json", 'w', encoding='utf-8') as f:
        json.dump(new_hybrids, f, ensure_ascii=False, indent=2)
    
    print("hybrids.json已同步")
    
    # 更新总站数统计
    cities_count = len(list((SITES_DIR / 'cities').iterdir())) if (SITES_DIR / 'cities').exists() else 0
    niches_count = len(list((SITES_DIR / 'niches').iterdir())) if (SITES_DIR / 'niches').exists() else 0
    hybrids_count = len(hybrid_dirs)
    
    print("\n" + "=" * 60)
    print("  站点统计")
    print("=" * 60)
    print(f"城市站: {cities_count}")
    print(f"行业站: {niches_count}")
    print(f"混合站: {hybrids_count}")
    print(f"总计: {cities_count + niches_count + hybrids_count}")


if __name__ == '__main__':
    sync_hybrids()