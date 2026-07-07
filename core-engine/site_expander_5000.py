#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
站点扩展脚本5000站 - 扩展站点数量至5000站目标
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"

def expand_sites_to_5000():
    """扩展站点数量至5000站"""
    print("=" * 80)
    print("站点扩展脚本5000站")
    print("=" * 80)
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 加载现有数据
    cities_file = DATA_DIR / 'cities.json'
    niches_file = DATA_DIR / 'niches.json'
    hybrids_file = DATA_DIR / 'hybrids.json'
    
    cities = []
    niches = []
    hybrids = []
    
    if cities_file.exists():
        with open(cities_file, 'r', encoding='utf-8') as f:
            cities = json.load(f)
    
    if niches_file.exists():
        with open(niches_file, 'r', encoding='utf-8') as f:
            niches = json.load(f)
    
    if hybrids_file.exists():
        with open(hybrids_file, 'r', encoding='utf-8') as f:
            hybrids = json.load(f)
    
    current_sites = len(cities) + len(niches) + len(hybrids)
    target_sites = 5000
    needed_sites = target_sites - current_sites
    
    print(f"当前站点数量: {current_sites}")
    print(f"目标站点数量: {target_sites}")
    print(f"还需站点数量: {needed_sites}")
    print()
    
    # 生成新组合站点
    print("生成新组合站点至5000站...")
    
    # 计算需要的组合数量
    # 我们有293个城市和500个行业
    # 城市站：293个
    # 行业站：500个
    # 当前组合站：1207个
    # 需要新增组合站：3000个
    
    # 使用所有城市和行业组合
    new_hybrids = []
    
    # 计算需要的组合数量
    remaining_cities = cities[10:]  # 从第11个城市开始（已使用10个）
    remaining_niches = niches[4:]  # 从第5个行业开始（已使用4个）
    
    print(f"剩余城市数量: {len(remaining_cities)}")
    print(f"剩余行业数量: {len(remaining_niches)}")
    print()
    
    # 生成组合（需要约3000个新组合站）
    # 283个城市 × 500个行业 = 141,500个潜在组合
    # 我们只需要3000个，所以选择性生成
    
    generated_count = 0
    max_combinations = needed_sites
    
    # 生成组合
    for city_idx, city in enumerate(remaining_cities):
        city_name = city.get('cityName', '')
        city_pinyin = city.get('cityPinyin', '')
        
        if not city_name or not city_pinyin:
            continue
        
        for niche_idx, niche in enumerate(remaining_niches):
            niche_name = niche.get('nicheName', '')
            niche_pinyin = niche.get('nichePinyin', '')
            
            if not niche_name or not niche_pinyin:
                continue
            
            # 检查是否已存在
            slug = f"{city_pinyin}-{niche_pinyin}"
            existing_slugs = [h.get('slug', '') for h in hybrids]
            
            if slug not in existing_slugs:
                new_hybrid = {
                    'siteType': 'hybrid',
                    'cityName': city_name,
                    'cityPinyin': city_pinyin,
                    'nicheName': niche_name,
                    'nichePinyin': niche_pinyin,
                    'slug': slug,
                    'title': f"{city_name}{niche_name}导航",
                    'description': f"{city_name}{niche_name}导航网站是一个专业的地区+行业组合导航平台。",
                    'keywords': f"{city_name}{niche_name}导航,{city_name}{niche_name}网站,{city_name}{niche_name}网址",
                    'priority': 'medium'
                }
                
                new_hybrids.append(new_hybrid)
                generated_count += 1
                
                if generated_count >= max_combinations:
                    break
        
        if generated_count >= max_combinations:
            break
    
    print(f"新组合站点数量: {len(new_hybrids)}")
    
    # 合并新组合站点到现有hybrids数据
    updated_hybrids = hybrids + new_hybrids
    
    print(f"更新后组合站点数量: {len(updated_hybrids)}")
    print()
    
    # 保存更新后的hybrids数据
    with open(hybrids_file, 'w', encoding='utf-8') as f:
        json.dump(updated_hybrids, f, ensure_ascii=False, indent=2)
    
    print(f"hybrids数据已更新: {hybrids_file}")
    print()
    
    # 计算新的站点总数
    new_total_sites = len(cities) + len(niches) + len(updated_hybrids)
    
    print("站点扩展统计:")
    print("-" * 80)
    print(f"城市站数量: {len(cities)}")
    print(f"行业站数量: {len(niches)}")
    print(f"组合站数量: {len(updated_hybrids)}")
    print(f"总站点数量: {new_total_sites}")
    print()
    
    # 检查是否达到目标
    if new_total_sites >= target_sites:
        print(f"✅ 站点数量达标！已达到{new_total_sites}站，超过目标{target_sites}站！")
    else:
        print(f"⚠️ 站点数量不足，还需{target_sites - new_total_sites}站")
    
    # 计算流量潜力提升
    print()
    print("流量潜力提升分析:")
    print("-" * 80)
    
    original_sites = 2000
    new_sites_count = new_total_sites
    sites_improvement = (new_sites_count / original_sites) * 100
    
    print(f"原始站点数量: {original_sites}")
    print(f"新站点数量: {new_sites_count}")
    print(f"站点数量提升: {sites_improvement:.0f}%")
    print()
    
    # 预估流量提升
    original_traffic = 74883400  # 年流量潜力
    estimated_traffic_boost = (sites_improvement / 100) - 1
    estimated_new_traffic = original_traffic * (1 + estimated_traffic_boost)
    
    print(f"原始年流量潜力: {original_traffic}访问")
    print(f"预估流量提升率: {estimated_traffic_boost * 100:.0f}%")
    print(f"预估新年流量潜力: {estimated_new_traffic:.0f}访问")
    print(f"流量增加: {estimated_new_traffic - original_traffic:.0f}访问/年")
    
    # 计算收入潜力提升
    print()
    print("收入潜力提升分析:")
    print("-" * 80)
    
    original_revenue = 3481920  # 年收入潜力
    estimated_revenue_boost = (sites_improvement / 100) - 1
    estimated_new_revenue = original_revenue * (1 + estimated_revenue_boost)
    
    print(f"原始年收入潜力: {original_revenue}元")
    print(f"预估收入提升率: {estimated_revenue_boost * 100:.0f}%")
    print(f"预估新年收入潜力: {estimated_new_revenue:.0f}元")
    print(f"收入增加: {estimated_new_revenue - original_revenue:.0f}元/年")
    
    print()
    print("=" * 80)
    print("站点扩展5000站完成！")
    print("=" * 80)
    
    return new_hybrids

def main():
    """主函数"""
    expand_sites_to_5000()

if __name__ == '__main__':
    main()