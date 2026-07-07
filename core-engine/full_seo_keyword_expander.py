#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整SEO关键词扩展脚本 - 扩展SEO关键词至10000个
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"

def expand_seo_keywords_to_10000():
    """扩展SEO关键词至10000个"""
    print("=" * 80)
    print("完整SEO关键词扩展脚本")
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
    
    # 1. 城市关键词（全部城市）
    print("生成全部城市关键词...")
    for city in cities:
        city_name = city.get('cityName', '')
        if not city_name:
            continue
        
        # 基础关键词
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
        keywords.append({
            'keyword': f'{city_name}导航网站',
            'category': 'city',
            'priority': 'high',
            'type': 'primary'
        })
        keywords.append({
            'keyword': f'{city_name}网站导航',
            'category': 'city',
            'priority': 'medium',
            'type': 'secondary'
        })
        keywords.append({
            'keyword': f'{city_name}本地导航',
            'category': 'city',
            'priority': 'medium',
            'type': 'local'
        })
        keywords.append({
            'keyword': f'{city_name}优质网站',
            'category': 'city',
            'priority': 'medium',
            'type': 'quality'
        })
    
    print(f"  城市关键词: {len([k for k in keywords if k['category'] == 'city'])}个")
    
    # 2. 行业关键词（全部行业）
    print("生成全部行业关键词...")
    for niche in niches:
        niche_name = niche.get('nicheName', '')
        if not niche_name:
            continue
        
        # 基础关键词
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
        keywords.append({
            'keyword': f'{niche_name}行业导航',
            'category': 'niche',
            'priority': 'high',
            'type': 'industry'
        })
        keywords.append({
            'keyword': f'{niche_name}专业网站',
            'category': 'niche',
            'priority': 'medium',
            'type': 'professional'
        })
        keywords.append({
            'keyword': f'{niche_name}行业资讯',
            'category': 'niche',
            'priority': 'medium',
            'type': 'news'
        })
        keywords.append({
            'keyword': f'{niche_name}专业导航',
            'category': 'niche',
            'priority': 'medium',
            'type': 'professional_nav'
        })
    
    print(f"  行业关键词: {len([k for k in keywords if k['category'] == 'niche'])}个")
    
    # 3. 组合关键词（城市+行业）
    print("生成组合关键词...")
    for city in cities[:200]:  # 使用200个城市
        city_name = city.get('cityName', '')
        if not city_name:
            continue
        
        for niche in niches[:200]:  # 使用200个行业
            niche_name = niche.get('nicheName', '')
            if not niche_name:
                continue
            
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
            keywords.append({
                'keyword': f'{city_name}{niche_name}网址',
                'category': 'hybrid',
                'priority': 'low',
                'type': 'combination'
            })
            keywords.append({
                'keyword': f'{city_name}{niche_name}本地导航',
                'category': 'hybrid',
                'priority': 'medium',
                'type': 'local_combination'
            })
            keywords.append({
                'keyword': f'{city_name}{niche_name}地区导航',
                'category': 'hybrid',
                'priority': 'low',
                'type': 'region_combination'
            })
    
    print(f"  组合关键词: {len([k for k in keywords if k['category'] == 'hybrid'])}个")
    
    # 4. 通用关键词
    print("生成通用关键词...")
    general_keywords = [
        '网站导航', '网址导航', '导航网站', '网站大全',
        '网址大全', '网站目录', '网址目录', '网站列表',
        '导航系统', '网站导航系统', '网址导航系统',
        '城市导航', '行业导航', '城市网站导航', '行业网站导航',
        '综合导航', '多城市导航', '多行业导航',
        '网站收录', '网址收录', '网站推荐', '网址推荐',
        '优质网站导航', '专业网站导航', '地区网站导航',
        '本地网站导航', '城市导航平台', '行业导航平台',
        '网站导航平台', '网址导航平台', '导航平台',
        '网站导航服务', '网址导航服务', '导航服务',
        '网站导航系统', '网址导航系统', '导航系统',
        '网站资源导航', '网址资源导航', '资源导航',
        '网站指南', '网址指南', '导航指南',
        '网站导览', '网址导览', '导览系统'
    ]
    
    for keyword in general_keywords:
        keywords.append({
            'keyword': keyword,
            'category': 'general',
            'priority': 'high',
            'type': 'general'
        })
    
    print(f"  通用关键词: {len([k for k in keywords if k['category'] == 'general'])}个")
    
    # 5. SEO优化关键词
    print("生成SEO优化关键词...")
    seo_keywords = [
        'SEO导航', 'SEO网站', 'SEO网址',
        '搜索引擎导航', '搜索引擎网站', '搜索引擎网址',
        '关键词导航', '关键词网站', '关键词网址',
        '优化导航', '优化网站', '优化网址',
        'SEO优化导航', 'SEO优化网站', 'SEO优化网址',
        '搜索引擎优化导航', '搜索引擎优化网站', '搜索引擎优化网址',
        '关键词优化导航', '关键词优化网站', '关键词优化网址'
    ]
    
    for keyword in seo_keywords:
        keywords.append({
            'keyword': keyword,
            'category': 'seo',
            'priority': 'medium',
            'type': 'seo'
        })
    
    print(f"  SEO关键词: {len([k for k in keywords if k['category'] == 'seo'])}个")
    
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
    if len(keywords) >= 10000:
        print()
        print(f"✅ 关键词数量达标！已生成{len(keywords)}个关键词，超过目标10000个！")
    else:
        print()
        print(f"⚠️ 关键词数量不足，还需生成{10000 - len(keywords)}个关键词")
        
        # 如果不足，继续生成
        print("继续生成额外关键词...")
        
        # 额外组合关键词
        for city in cities[200:250]:  # 使用更多城市
            city_name = city.get('cityName', '')
            if not city_name:
                continue
            
            for niche in niches[200:250]:  # 使用更多行业
                niche_name = niche.get('nicheName', '')
                if not niche_name:
                    continue
                
                keywords.append({
                    'keyword': f'{city_name}{niche_name}导航',
                    'category': 'hybrid',
                    'priority': 'low',
                    'type': 'extra_combination'
                })
        
        print(f"  额外组合关键词: {len([k for k in keywords if k['category'] == 'hybrid'])}个")
        print(f"总关键词: {len(keywords)}个")
        
        if len(keywords) >= 10000:
            print(f"✅ 关键词数量达标！已生成{len(keywords)}个关键词，超过目标10000个！")
    
    # 保存关键词
    seo_keywords_file = DATA_DIR / 'seo_keywords.json'
    
    with open(seo_keywords_file, 'w', encoding='utf-8') as f:
        json.dump(keywords, f, ensure_ascii=False, indent=2)
    
    print()
    print(f"关键词已保存至: {seo_keywords_file}")
    
    # 计算流量潜力提升
    print()
    print("流量潜力提升分析:")
    print("-" * 80)
    
    original_keywords = 5634
    new_keywords = len(keywords)
    keyword_improvement = (new_keywords / original_keywords) * 100
    
    print(f"原始关键词数量: {original_keywords}个")
    print(f"新关键词数量: {new_keywords}个")
    print(f"关键词数量提升: {keyword_improvement:.0f}%")
    print()
    
    # 预估流量提升
    original_traffic = 93604250  # 年流量潜力（已包含内容优化提升）
    estimated_traffic_boost = keyword_improvement / 100 * 0.2  # 假设20%转化率
    estimated_new_traffic = original_traffic * (1 + estimated_traffic_boost)
    
    print(f"原始年流量潜力: {original_traffic}访问")
    print(f"预估流量提升率: {estimated_traffic_boost * 100:.0f}%")
    print(f"预估新年流量潜力: {estimated_new_traffic:.0f}访问")
    print(f"流量增加: {estimated_new_traffic - original_traffic:.0f}访问/年")
    
    print()
    print("=" * 80)
    print("完整SEO关键词扩展完成！")
    print("=" * 80)
    
    return keywords

def main():
    """主函数"""
    expand_seo_keywords_to_10000()

if __name__ == '__main__':
    main()