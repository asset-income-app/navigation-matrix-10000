#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML重新生成引擎 - 根据更新的config.json重新生成所有HTML文件
"""

import json
import random
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = ROOT_DIR / "01-templates"
SITES_DIR = ROOT_DIR / "02-sites"

VARIANTS = ['variant-blue', 'variant-green', 'variant-orange', 'variant-purple', 'variant-dark']
CENTRAL_HUB_URL = "https://navigation-matrix-hub.pages.dev"


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


def generate_html(template_html, config):
    """生成HTML文件"""
    embedded_config = json.dumps(config, ensure_ascii=False, separators=(',', ':'))
    
    site_type = config.get('siteType', '')
    if site_type == 'city':
        site_name = config['cityName'] + '便民导航'
        site_icon = '🏠'
    elif site_type == 'niche':
        site_name = config.get('nicheName', '') + '导航'
        site_icon = '🔗'
    else:
        site_name = config.get('cityName', '') + config.get('nicheName', '') + '导航'
        site_icon = '🔗'
    
    replacements = {
        '{{SITE_TITLE}}': config.get('siteTitle', ''),
        '{{SITE_DESCRIPTION}}': config.get('siteDescription', ''),
        '{{SITE_KEYWORDS}}': config.get('siteKeywords', ''),
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
    """生成CSS文件"""
    if variant_css:
        return variant_css + '\n' + base_css
    return base_css


def regenerate_all_html():
    """重新生成所有站点的HTML"""
    print("=" * 60)
    print("  HTML重新生成引擎")
    print("=" * 60)
    
    templates = load_template()
    print("模板加载完成")
    
    # 重新生成城市站
    cities_dir = SITES_DIR / "cities"
    if cities_dir.exists():
        city_count = 0
        for city_dir in cities_dir.iterdir():
            if city_dir.is_dir():
                config_path = city_dir / "config.json"
                if config_path.exists():
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    variant = config.get('variant', random.choice(VARIANTS))
                    variant_css = load_variant(variant)
                    
                    html = generate_html(templates['index.html'], config)
                    css = generate_css(templates['style.css'], variant_css)
                    
                    with open(city_dir / 'index.html', 'w', encoding='utf-8') as f:
                        f.write(html)
                    with open(city_dir / 'style.css', 'w', encoding='utf-8') as f:
                        f.write(css)
                    
                    city_count += 1
                    if city_count % 20 == 0:
                        print(f"  城市站进度: {city_count}")
        
        print(f"✓ 城市站HTML更新: {city_count} 个")
    
    # 重新生成行业站
    niches_dir = SITES_DIR / "niches"
    if niches_dir.exists():
        niche_count = 0
        for niche_dir in niches_dir.iterdir():
            if niche_dir.is_dir():
                config_path = niche_dir / "config.json"
                if config_path.exists():
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    variant = config.get('variant', random.choice(VARIANTS))
                    variant_css = load_variant(variant)
                    
                    html = generate_html(templates['index.html'], config)
                    css = generate_css(templates['style.css'], variant_css)
                    
                    with open(niche_dir / 'index.html', 'w', encoding='utf-8') as f:
                        f.write(html)
                    with open(niche_dir / 'style.css', 'w', encoding='utf-8') as f:
                        f.write(css)
                    
                    niche_count += 1
                    if niche_count % 20 == 0:
                        print(f"  行业站进度: {niche_count}")
        
        print(f"✓ 行业站HTML更新: {niche_count} 个")
    
    # 重新生成混合站
    hybrids_dir = SITES_DIR / "hybrids"
    if hybrids_dir.exists():
        hybrid_dirs = [d for d in hybrids_dir.iterdir() if d.is_dir()]
        total_hybrids = len(hybrid_dirs)
        print(f"混合站总数: {total_hybrids}")
        
        hybrid_count = 0
        for hybrid_dir in hybrid_dirs:
            config_path = hybrid_dir / "config.json"
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    variant = config.get('variant', random.choice(VARIANTS))
                    variant_css = load_variant(variant)
                    
                    html = generate_html(templates['index.html'], config)
                    css = generate_css(templates['style.css'], variant_css)
                    
                    with open(hybrid_dir / 'index.html', 'w', encoding='utf-8') as f:
                        f.write(html)
                    with open(hybrid_dir / 'style.css', 'w', encoding='utf-8') as f:
                        f.write(css)
                    
                    hybrid_count += 1
                    if hybrid_count % 200 == 0:
                        print(f"  混合站进度: {hybrid_count}/{total_hybrids}")
                except Exception as e:
                    pass
        
        print(f"✓ 混合站HTML更新: {hybrid_count} 个")
    
    print("\n" + "=" * 60)
    print("  HTML重新生成完成!")
    print("=" * 60)


if __name__ == '__main__':
    regenerate_all_html()