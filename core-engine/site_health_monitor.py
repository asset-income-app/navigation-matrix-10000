#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
站点健康监控脚本 - 检查批次站点健康状态、生成报告
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
TEMP_BATCHES = [
    ROOT_DIR / "temp-batch1",
    ROOT_DIR / "temp-batch2",
    ROOT_DIR / "temp-batch3",
    ROOT_DIR / "temp-batch4",
    ROOT_DIR / "temp-batch5"
]

def check_batch_sites():
    """检查批次站点"""
    print("=" * 60)
    print("站点健康监控报告")
    print("=" * 60)
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 检查批次站点
    print("批次站点检查:")
    print("-" * 60)
    
    for i, batch_dir in enumerate(TEMP_BATCHES, 1):
        if not batch_dir.exists():
            print(f"批次{i}: ❌ 目录不存在")
            continue
        
        index_file = batch_dir / "index.html"
        if index_file.exists():
            file_size = index_file.stat().st_size
            print(f"批次{i}: ✅ index.html存在 ({file_size} bytes)")
        else:
            print(f"批次{i}: ❌ index.html不存在")
    
    print()
    
    # 检查数据文件
    print("数据文件检查:")
    print("-" * 60)
    
    data_files = ['cities.json', 'niches.json', 'hybrids.json', 'master-links.json', 'seo_keywords.json']
    
    for data_file in data_files:
        file_path = DATA_DIR / data_file
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                count = len(data) if isinstance(data, list) else len(data.keys())
                print(f"{data_file}: ✅ 有效 ({count} 条数据)")
            except Exception as e:
                print(f"{data_file}: ❌ 解析错误: {e}")
        else:
            print(f"{data_file}: ❌ 文件不存在")
    
    print()
    
    # 统计站点数量
    print("站点统计:")
    print("-" * 60)
    
    try:
        with open(DATA_DIR / 'cities.json', 'r', encoding='utf-8') as f:
            cities = json.load(f)
        city_count = len(cities)
        print(f"城市站: {city_count} 个")
    except:
        print("城市站: 数据文件不存在")
    
    try:
        with open(DATA_DIR / 'niches.json', 'r', encoding='utf-8') as f:
            niches = json.load(f)
        niche_count = len(niches)
        print(f"行业站: {niche_count} 个")
    except:
        print("行业站: 数据文件不存在")
    
    try:
        with open(DATA_DIR / 'hybrids.json', 'r', encoding='utf-8') as f:
            hybrids = json.load(f)
        hybrid_count = len(hybrids)
        print(f"组合站: {hybrid_count} 个")
    except:
        print("组合站: 数据文件不存在")
    
    total = city_count + niche_count + hybrid_count
    print(f"总站点: {total} 个")
    
    print()
    print("=" * 60)
    print("监控报告完成")
    print("=" * 60)

def main():
    """主函数"""
    check_batch_sites()

if __name__ == '__main__':
    main()