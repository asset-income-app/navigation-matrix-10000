#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
万站生成引擎 - 根据模板和数据生成所有站点文件
"""

import json
import os
import random
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = ROOT_DIR / "01-templates"
SITES_DIR = ROOT_DIR / "02-sites"
DATA_DIR = ROOT_DIR / "data"

VARIANTS = ['variant-blue', 'variant-green', 'variant-orange', 'variant-purple', 'variant-dark']
CENTRAL_HUB_URL = "https://daohangbaike-nav.pages.dev"


def load_json(filepath):
    """加载JSON文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(filepath, data):
    """保存JSON文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_template():
    """加载基础模板文件"""
    templates = {}
    base_dir = TEMPLATES_DIR / "base"
    for filename in ['index.html', 'style.css', 'script.js']:
        filepath = base_dir / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            templates[filename] = f.read()
    return templates


def load_variant(variant_name):
    """加载变体CSS"""
    variant_dir = TEMPLATES_DIR / "variants" / variant_name
    if variant_dir.exists():
        css_path = variant_dir / "style.css"
        if css_path.exists():
            with open(css_path, 'r', encoding='utf-8') as f:
                return f.read()
    return ""


def generate_config(site_data):
    """生成站点配置"""
    site_type = site_data.get('siteType', '')
    if site_type == 'city':
        return {
            'siteType': 'city',
            'cityName': site_data['cityName'],
            'cityPinyin': site_data['cityPinyin'],
            'province': site_data.get('province', ''),
            'siteTitle': f"{site_data['cityName']}便民导航 - 最全面的{site_data['cityName']}网站导航",
            'siteDescription': f"{site_data['cityName']}便民导航站，汇集{site_data['cityName']}各类官方网站和实用链接，一站式满足您的所有需求。",
            'siteKeywords': f"{site_data['cityName']},导航,便民,{site_data['cityName']}导航,{site_data['cityName']}便民服务",
            'categories': site_data.get('categories', []),
            'variant': site_data.get('variant', 'variant-blue'),
            'centralHubUrl': CENTRAL_HUB_URL
        }
    else:
        return {
            'siteType': 'niche',
            'nicheName': site_data['nicheName'],
            'nichePinyin': site_data['nichePinyin'],
            'siteTitle': site_data.get('siteTitle', f"{site_data['nicheName']}导航 - 最全面的{site_data['nicheName']}网站导航"),
            'siteDescription': site_data.get('siteDescription', f"{site_data['nicheName']}导航站，汇集{site_data['nicheName']}各类优质网站和资源，一站式满足您的所有需求。"),
            'siteKeywords': site_data.get('siteKeywords', f"{site_data['nicheName']},导航,{site_data['nicheName']}资源,{site_data['nicheName']}网站"),
            'categories': site_data.get('categories', []),
            'variant': site_data.get('variant', 'variant-blue'),
            'centralHubUrl': CENTRAL_HUB_URL
        }


def generate_html(template_html, config):
    """生成HTML文件"""
    embedded_config = json.dumps(config, ensure_ascii=False, separators=(',', ':'))
    
    site_type = config.get('siteType', '')
    if site_type == 'city':
        site_name = config['cityName'] + '便民导航'
        site_icon = '🏠'
    else:
        site_name = config['nicheName'] + '导航'
        site_icon = '🔗'
    
    replacements = {
        '{{SITE_TITLE}}': config['siteTitle'],
        '{{SITE_DESCRIPTION}}': config['siteDescription'],
        '{{SITE_KEYWORDS}}': config['siteKeywords'],
        '{{SITE_NAME}}': site_name,
        '{{SITE_ICON}}': site_icon,
        '{{CENTRAL_HUB_URL}}': CENTRAL_HUB_URL,
        '{{EMBEDDED_CONFIG}}': embedded_config
    }
    
    html = template_html
    for key, value in replacements.items():
        html = html.replace(key, value)
    
    return html


def generate_css(base_css, variant_css):
    """生成CSS文件（基础+变体）"""
    if variant_css:
        return variant_css + '\n' + base_css
    return base_css


def generate_sitemap(site_name, site_type):
    """生成sitemap.xml"""
    if site_type == 'city':
        pinyin = site_name
    else:
        pinyin = site_name
    
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://{pinyin}-nav.pages.dev/</loc>
        <lastmod>2026-07-06</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>"""
    return sitemap


def generate_robots():
    """生成robots.txt"""
    return """User-agent: *
Allow: /
Sitemap: /sitemap.xml"""


def generate_headers():
    """生成Cloudflare _headers文件"""
    return """/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:;"""


def generate_site(site_data, templates):
    """生成单个站点的所有文件"""
    site_type = site_data.get('siteType', '')
    
    if site_type == 'city':
        site_key = site_data['cityPinyin']
        site_dir = SITES_DIR / 'cities' / site_key
    else:
        site_key = site_data['nichePinyin']
        site_dir = SITES_DIR / 'niches' / site_key
    
    site_dir.mkdir(parents=True, exist_ok=True)
    
    config = generate_config(site_data)
    variant_css = load_variant(config['variant'])
    
    html = generate_html(templates['index.html'], config)
    css = generate_css(templates['style.css'], variant_css)
    
    files = {
        'index.html': html,
        'style.css': css,
        'script.js': templates['script.js'],
        'config.json': json.dumps(config, ensure_ascii=False, indent=2),
        'sitemap.xml': generate_sitemap(site_key, site_type),
        'robots.txt': generate_robots(),
        '_headers': generate_headers()
    }
    
    for filename, content in files.items():
        filepath = site_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return site_key


def assign_variants(data_list):
    """为站点随机分配模板变体"""
    for item in data_list:
        item['variant'] = random.choice(VARIANTS)
    return data_list


def generate_all():
    """生成所有站点"""
    print("=" * 60)
    print("  万站生成引擎 v1.0")
    print("=" * 60)
    print()
    
    templates = load_template()
    print("✓ 模板加载完成")
    
    cities = load_json(DATA_DIR / "cities.json")
    niches = load_json(DATA_DIR / "niches.json")
    print(f"✓ 数据加载完成 - 城市站: {len(cities)}, 行业站: {len(niches)}")
    
    cities = assign_variants(cities)
    niches = assign_variants(niches)
    print("✓ 模板变体分配完成")
    
    all_data = cities + niches
    total_sites = len(all_data)
    
    print(f"\n开始生成 {total_sites} 个站点...")
    
    city_count = 0
    niche_count = 0
    errors = []
    
    for i, site_data in enumerate(all_data, 1):
        try:
            site_key = generate_site(site_data, templates)
            if site_data.get('siteType') == 'city':
                city_count += 1
            else:
                niche_count += 1
            
            if i % 20 == 0:
                print(f"  进度: {i}/{total_sites}")
        except Exception as e:
            errors.append(f"{site_key}: {str(e)}")
            print(f"  ✗ 生成失败: {site_key}")
    
    template_counts = {}
    for item in all_data:
        variant = item.get('variant', 'unknown')
        template_counts[variant] = template_counts.get(variant, 0) + 1
    
    print("\n" + "=" * 60)
    print("  生成完成!")
    print("=" * 60)
    print(f"\n  城市站: {city_count}")
    print(f"  行业站: {niche_count}")
    print(f"  总计: {city_count + niche_count}")
    print(f"\n  模板分配:")
    for variant, count in template_counts.items():
        print(f"    {variant}: {count}个")
    
    if errors:
        print(f"\n  错误数: {len(errors)}")
        for error in errors[:5]:
            print(f"    ✗ {error}")
    
    save_json(DATA_DIR / "template-assignment.json", {
        'timestamp': '2026-07-06',
        'cities': [{k: v for k, v in c.items() if k in ['cityName', 'cityPinyin', 'variant']} for c in cities],
        'niches': [{k: v for k, v in n.items() if k in ['nicheName', 'nichePinyin', 'variant']} for n in niches],
        'templateCounts': template_counts
    })
    
    print("\n✓ 模板分配记录已保存")


if __name__ == '__main__':
    generate_all()