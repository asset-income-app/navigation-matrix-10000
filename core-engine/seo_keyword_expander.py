#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO关键词扩展脚本 - 扩展SEO关键词库，提升流量潜力
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"

def generate_seo_keywords():
    """生成SEO关键词"""
    print("=" * 80)
    print("SEO关键词扩展脚本")
    print("=" * 80)
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 加载现有数据
    cities_file = DATA_DIR / 'cities.json'
    niches_file = DATA_DIR / 'niches.json'
    
    cities = []
    niches = []
    
    if cities_file.exists():
        with open(cities_file, 'r', encoding='utf-8') as f:
            cities = json.load(f)
    
    if niches_file.exists():
        with open(niches_file, 'r', encoding='utf-8') as f:
            niches = json.load(f)
    
    print(f"城市数量: {len(cities)}")
    print(f"行业数量: {len(niches)}")
    print()
    
    # 生成关键词列表
    keywords = []
    
    # 1. 城市关键词
    print("生成城市关键词...")
    for city in cities[:100]:  # 前100个城市
        city_name = city.get('name', city) if isinstance(city, dict) else city
        keywords.append({
            'keyword': f'{city_name}导航',
            'category': 'city',
            'priority': 'high',
            'type': 'primary'
        })
        keywords.append({
            'keyword': f'{city_name}网站',
            'category': 'city',
            'priority': 'high',
            'type': 'secondary'
        })
        keywords.append({
            'keyword': f'{city_name}网址',
            'category': 'city',
            'priority': 'medium',
            'type': 'tertiary'
        })
    
    # 2. 行业关键词
    print("生成行业关键词...")
    for niche in niches[:100]:  # 前100个行业
        niche_name = niche.get('name', niche) if isinstance(niche, dict) else niche
        keywords.append({
            'keyword': f'{niche_name}导航',
            'category': 'niche',
            'priority': 'high',
            'type': 'primary'
        })
        keywords.append({
            'keyword': f'{niche_name}网站',
            'category': 'niche',
            'priority': 'high',
            'type': 'secondary'
        })
        keywords.append({
            'keyword': f'{niche_name}网址',
            'category': 'niche',
            'priority': 'medium',
            'type': 'tertiary'
        })
    
    # 3. 组合关键词（城市+行业）
    print("生成组合关键词...")
    for city in cities[:50]:  # 前50个城市
        city_name = city.get('name', city) if isinstance(city, dict) else city
        for niche in niches[:50]:  # 前50个行业
            niche_name = niche.get('name', niche) if isinstance(niche, dict) else niche
            keywords.append({
                'keyword': f'{city_name}{niche_name}导航',
                'category': 'hybrid',
                'priority': 'medium',
                'type': 'combination'
            })
            keywords.append({
                'keyword': f'{city_name}{niche_name}网站',
                'category': 'hybrid',
                'priority': 'medium',
                'type': 'combination'
            })
    
    # 4. 通用关键词
    print("生成通用关键词...")
    general_keywords = [
        '网站导航', '网址导航', '导航网站', '网站大全',
        '网址大全', '网站目录', '网址目录', '网站列表',
        '导航系统', '网站导航系统', '网址导航系统',
        '城市导航', '行业导航', '城市网站导航', '行业网站导航',
        '综合导航', '多城市导航', '多行业导航',
        '网站收录', '网址收录', '网站推荐', '网址推荐'
    ]
    
    for keyword in general_keywords:
        keywords.append({
            'keyword': keyword,
            'category': 'general',
            'priority': 'high',
            'type': 'general'
        })
    
    # 5. SEO优化关键词
    print("生成SEO优化关键词...")
    seo_keywords = [
        'SEO导航', 'SEO网站', 'SEO网址',
        '搜索引擎导航', '搜索引擎网站', '搜索引擎网址',
        '关键词导航', '关键词网站', '关键词网址',
        '优化导航', '优化网站', '优化网址'
    ]
    
    for keyword in seo_keywords:
        keywords.append({
            'keyword': keyword,
            'category': 'seo',
            'priority': 'medium',
            'type': 'seo'
        })
    
    # 统计关键词数量
    print()
    print("关键词生成统计:")
    print("-" * 80)
    
    city_keywords = [k for k in keywords if k['category'] == 'city']
    niche_keywords = [k for k in keywords if k['category'] == 'niche']
    hybrid_keywords = [k for k in keywords if k['category'] == 'hybrid']
    general_keywords = [k for k in keywords if k['category'] == 'general']
    seo_keywords = [k for k in keywords if k['category'] == 'seo']
    
    print(f"城市关键词: {len(city_keywords)}个")
    print(f"行业关键词: {len(niche_keywords)}个")
    print(f"组合关键词: {len(hybrid_keywords)}个")
    print(f"通用关键词: {len(general_keywords)}个")
    print(f"SEO关键词: {len(seo_keywords)}个")
    print(f"总关键词: {len(keywords)}个")
    
    # 检查是否达到目标
    if len(keywords) >= 500:
        print()
        print(f"✅ 关键词数量达标！已生成{len(keywords)}个关键词，超过目标500个！")
    else:
        print()
        print(f"⚠️ 关键词数量不足，还需生成{500 - len(keywords)}个关键词")
    
    # 保存关键词
    seo_keywords_file = DATA_DIR / 'seo_keywords.json'
    
    with open(seo_keywords_file, 'w', encoding='utf-8') as f:
        json.dump(keywords, f, ensure_ascii=False, indent=2)
    
    print()
    print(f"关键词已保存至: {seo_keywords_file}")
    
    # 计算流量潜力提升
    original_keywords = 3
    new_keywords = len(keywords)
    keyword_improvement = (new_keywords / original_keywords) * 100
    
    print()
    print("流量潜力提升分析:")
    print("-" * 80)
    print(f"原始关键词数量: {original_keywords}个")
    print(f"新关键词数量: {new_keywords}个")
    print(f"关键词数量提升: {keyword_improvement:.0f}%")
    print()
    
    # 预估流量提升
    original_traffic = 73715400  # 年流量潜力
    estimated_traffic_boost = keyword_improvement / 100 * 0.3  # 假设30%转化率
    estimated_new_traffic = original_traffic * (1 + estimated_traffic_boost)
    
    print(f"原始年流量潜力: {original_traffic}访问")
    print(f"预估流量提升率: {estimated_traffic_boost * 100:.0f}%")
    print(f"预估新年流量潜力: {estimated_new_traffic:.0f}访问")
    print(f"流量增加: {estimated_new_traffic - original_traffic:.0f}访问/年")
    
    print()
    print("=" * 80)
    print("SEO关键词扩展完成！")
    print("=" * 80)
    
    return keywords

def main():
    """主函数"""
    generate_seo_keywords()

if __name__ == '__main__':
    main()