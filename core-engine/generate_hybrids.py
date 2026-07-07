#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
混合站生成引擎 - 生成新增的混合站
"""

import json
import random
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = ROOT_DIR / "01-templates"
SITES_DIR = ROOT_DIR / "02-sites"
DATA_DIR = ROOT_DIR / "data"

VARIANTS = ['variant-blue', 'variant-green', 'variant-orange', 'variant-purple', 'variant-dark']
CENTRAL_HUB_URL = "https://navigation-matrix-hub.pages.dev"


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


def generate_hybrid_config(hybrid_data, variant):
    """生成混合站配置"""
    site_pinyin = hybrid_data.get('sitePinyin', '')
    city_name = hybrid_data.get('cityName', '')
    niche_name = hybrid_data.get('nicheName', '')
    
    # 如果没有sitePinyin，自动生成
    if not site_pinyin:
        niche_pinyin = hybrid_data.get('nichePinyin', niche_name.lower())
        site_pinyin = f"{niche_pinyin}-{city_name}"
    
    return {
        'siteType': 'hybrid',
        'sitePinyin': site_pinyin,
        'cityName': city_name,
        'nicheName': niche_name,
        'siteTitle': hybrid_data.get('siteTitle', f"{city_name}{niche_name}导航 - 最全面的{city_name}{niche_name}网站导航"),
        'siteDescription': hybrid_data.get('siteDescription', f"{city_name}{niche_name}导航站，汇集{city_name}{niche_name}各类优质网站和资源，一站式满足您的所有需求。"),
        'siteKeywords': f"{city_name},{niche_name},导航,{city_name}{niche_name},{city_name}{niche_name}资源",
        'categories': hybrid_data.get('categories', []),
        'variant': variant,
        'centralHubUrl': CENTRAL_HUB_URL
    }


def generate_html(template_html, config):
    """生成HTML文件"""
    embedded_config = json.dumps(config, ensure_ascii=False, separators=(',', ':'))
    
    site_type = config.get('siteType', '')
    if site_type == 'hybrid':
        site_name = config['cityName'] + config['nicheName'] + '导航'
        site_icon = '🔗'
    else:
        site_name = config.get('nicheName', '') + '导航'
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


def generate_sitemap(site_pinyin):
    """生成sitemap.xml"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://navigation-matrix-hub.pages.dev/hybrids/{site_pinyin}/</loc>
        <lastmod>2026-07-06</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>"""


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


def generate_hybrid_site(hybrid_data, templates):
    """生成单个混合站点的所有文件"""
    site_pinyin = hybrid_data.get('sitePinyin', '')
    city_name = hybrid_data.get('cityName', '')
    niche_name = hybrid_data.get('nicheName', '')
    
    # 生成sitePinyin
    if not site_pinyin:
        niche_pinyin = hybrid_data.get('nichePinyin', niche_name.lower())
        site_pinyin = f"{niche_pinyin}-{city_name}"
    
    site_dir = SITES_DIR / 'hybrids' / site_pinyin
    site_dir.mkdir(parents=True, exist_ok=True)
    
    variant = random.choice(VARIANTS)
    config = generate_hybrid_config(hybrid_data, variant)
    variant_css = load_variant(variant)
    
    html = generate_html(templates['index.html'], config)
    css = generate_css(templates['style.css'], variant_css)
    
    files = {
        'index.html': html,
        'style.css': css,
        'script.js': templates['script.js'],
        'config.json': json.dumps(config, ensure_ascii=False, indent=2),
        'sitemap.xml': generate_sitemap(site_pinyin),
        'robots.txt': generate_robots(),
        '_headers': generate_headers()
    }
    
    for filename, content in files.items():
        filepath = site_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return site_pinyin


def generate_new_hybrids():
    """生成新增的混合站"""
    print("=" * 60)
    print("  混合站生成引擎")
    print("=" * 60)
    
    # 加载模板
    templates = load_template()
    print("模板加载完成")
    
    # 加载hybrids数据
    hybrids = load_json(DATA_DIR / "hybrids.json")
    print(f"hybrids.json总数: {len(hybrids)}")
    
    # 检查已生成的目录
    existing_dirs = set()
    hybrids_dir = SITES_DIR / 'hybrids'
    if hybrids_dir.exists():
        for d in hybrids_dir.iterdir():
            if d.is_dir():
                existing_dirs.add(d.name)
    
    print(f"已生成混合站目录: {len(existing_dirs)}")
    
    # 找出需要生成的新站点
    to_generate = []
    for h in hybrids:
        site_pinyin = h.get('sitePinyin', '')
        if not site_pinyin:
            niche_pinyin = h.get('nichePinyin', h.get('nicheName', '').lower())
            city_name = h.get('cityName', '')
            site_pinyin = f"{niche_pinyin}-{city_name}"
        
        if site_pinyin not in existing_dirs:
            to_generate.append(h)
    
    print(f"需要生成的新站点: {len(to_generate)}")
    
    if len(to_generate) == 0:
        print("没有需要生成的新站点")
        return
    
    # 生成新站点
    print(f"\n开始生成 {len(to_generate)} 个新混合站...")
    
    generated = 0
    errors = []
    
    for i, hybrid_data in enumerate(to_generate, 1):
        try:
            site_pinyin = generate_hybrid_site(hybrid_data, templates)
            generated += 1
            if i % 20 == 0:
                print(f"  进度: {i}/{len(to_generate)}")
        except Exception as e:
            errors.append(f"{hybrid_data.get('sitePinyin', 'unknown')}: {str(e)}")
            print(f"  生成失败: {hybrid_data.get('sitePinyin', 'unknown')}")
    
    print("\n" + "=" * 60)
    print("  生成完成!")
    print("=" * 60)
    print(f"  新生成: {generated}")
    print(f"  总混合站: {len(existing_dirs) + generated}")
    
    if errors:
        print(f"\n  错误数: {len(errors)}")
        for error in errors[:5]:
            print(f"    - {error}")


if __name__ == '__main__':
    generate_new_hybrids()