#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO优化脚本 - 分析和优化站点SEO
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"

def analyze_seo_keywords():
    """分析SEO关键词"""
    print("=" * 60)
    print("SEO关键词优化报告")
    print("=" * 60)
    print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 检查SEO关键词文件
    seo_keywords_file = DATA_DIR / 'seo_keywords.json'
    
    if seo_keywords_file.exists():
        try:
            with open(seo_keywords_file, 'r', encoding='utf-8') as f:
                keywords = json.load(f)
            
            print("SEO关键词统计:")
            print("-" * 60)
            print(f"关键词数量: {len(keywords)}")
            
            # 分析关键词类型
            for keyword in keywords:
                if isinstance(keyword, dict):
                    name = keyword.get('name', 'Unknown')
                    category = keyword.get('category', 'Unknown')
                    priority = keyword.get('priority', 'Unknown')
                    print(f"- {name}: {category} (优先级: {priority})")
            
            print()
            print("SEO优化建议:")
            print("-" * 60)
            print("1. 增加关键词数量，扩展关键词库")
            print("2. 优化关键词优先级，提升核心关键词")
            print("3. 创建关键词组合，生成组合站关键词")
            print("4. 监控关键词排名，定期更新SEO策略")
            
        except Exception as e:
            print(f"SEO关键词文件解析错误: {e}")
    else:
        print("SEO关键词文件不存在")
    
    print()
    
    # 分析城市站SEO潜力
    cities_file = DATA_DIR / 'cities.json'
    if cities_file.exists():
        try:
            with open(cities_file, 'r', encoding='utf-8') as f:
                cities = json.load(f)
            
            print("城市站SEO潜力分析:")
            print("-" * 60)
            print(f"城市站数量: {len(cities)}")
            print("SEO潜力: 每个城市站可生成多个关键词组合")
            print("建议: 为每个城市站创建地区性关键词")
            
        except Exception as e:
            print(f"城市站文件解析错误: {e}")
    
    print()
    
    # 分析行业站SEO潜力
    niches_file = DATA_DIR / 'niches.json'
    if niches_file.exists():
        try:
            with open(niches_file, 'r', encoding='utf-8') as f:
                niches = json.load(f)
            
            print("行业站SEO潜力分析:")
            print("-" * 60)
            print(f"行业站数量: {len(niches)}")
            print("SEO潜力: 每个行业站可生成多个关键词组合")
            print("建议: 为每个行业站创建专业性关键词")
            
        except Exception as e:
            print(f"行业站文件解析错误: {e}")
    
    print()
    
    # 分析组合站SEO潜力
    hybrids_file = DATA_DIR / 'hybrids.json'
    if hybrids_file.exists():
        try:
            with open(hybrids_file, 'r', encoding='utf-8') as f:
                hybrids = json.load(f)
            
            print("组合站SEO潜力分析:")
            print("-" * 60)
            print(f"组合站数量: {len(hybrids)}")
            print("SEO潜力: 组合站关键词具有地域+行业双重优势")
            print("建议: 为每个组合站创建精准关键词")
            
        except Exception as e:
            print(f"组合站文件解析错误: {e}")
    
    print()
    print("=" * 60)
    print("SEO优化报告完成")
    print("=" * 60)

def main():
    """主函数"""
    analyze_seo_keywords()

if __name__ == '__main__':
    main()