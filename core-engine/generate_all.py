#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导航矩阵统一版 - 核心生成引擎
一键生成城市站、行业站、组合站
"""

import json
import os
import sys
import hashlib
import argparse
from datetime import datetime
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = ROOT_DIR / "01-templates"
SITES_DIR = ROOT_DIR / "02-sites"
DATA_DIR = ROOT_DIR / "data"
HUB_DIR = ROOT_DIR / "03-central-hub"
DEPLOYED_DIR = ROOT_DIR / "05-deployed"

# 模板变体
VARIANTS = ['variant-blue', 'variant-green', 'variant-orange', 'variant-purple', 'variant-dark']

# 联系方式
CONTACT_EMAIL = "931249697@qq.com"
CONTACT_QQ = "931249697"
CENTRAL_HUB_URL = "https://daohangbaike-nav.pages.dev"


def get_variant(site_name):
    """基于站点名称hash分配模板变体"""
    hash_val = int(hashlib.md5(site_name.encode()).hexdigest(), 16)
    return VARIANTS[hash_val % len(VARIANTS)]


def load_json(filepath):
    """加载JSON文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"  [ERROR] JSON解析失败 {filepath}: {e}")
        return None


def save_json(filepath, data):
    """保存JSON文件"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_template(filepath):
    """读取模板文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def generate_sitemap(site_url, site_name):
    """生成sitemap.xml"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{site_url}</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>"""


def generate_robots(site_url):
    """生成robots.txt"""
    return f"""User-agent: *
Allow: /
Sitemap: {site_url}/sitemap.xml"""


def generate_headers():
    """生成_headers文件"""
    return """/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin"""


def generate_site(site_dir, config, site_type):
    """生成单个站点的所有文件"""
    os.makedirs(site_dir, exist_ok=True)

    # 确定站点名称和URL
    if site_type == 'city':
        site_name = config.get('cityName', '未知')
        site_pinyin = config.get('cityPinyin', 'unknown')
        site_url = f"https://{site_pinyin}-nav.pages.dev"
        site_title = f"{site_name}导航 - 最全的{site_name}生活服务导航"
        site_desc = f"{site_name}导航站，汇集{site_name}最优质的政务服务、生活服务、交通出行等网站，一站式满足您的所有需求。"
        site_icon = "🏙️"
    elif site_type == 'niche':
        site_name = config.get('nicheName', '未知')
        site_pinyin = config.get('nichePinyin', 'unknown')
        site_url = f"https://{site_pinyin}-nav.pages.dev"
        site_title = config.get('siteTitle', f'{site_name}导航')
        site_desc = config.get('siteDescription', f'{site_name}导航站')
        site_icon = "🏷️"
    else:  # hybrid
        city = config.get('cityName', '')
        niche = config.get('nicheName', '')
        site_name = f"{city}{niche}"
        site_pinyin = config.get('sitePinyin', f"{niche}-{city}")
        site_url = f"https://{site_pinyin}.pages.dev"
        site_title = f"{city}{niche}导航 - {city}{niche}网站大全"
        site_desc = f"{city}{niche}导航站，汇集{city}最优质的{niche}相关网站和资源。"
        site_icon = "🔗"

    # 获取模板变体
    variant = get_variant(site_pinyin)

    # 读取模板
    base_template_dir = TEMPLATES_DIR / "base"
    variant_dir = TEMPLATES_DIR / "variants" / variant

    html_template = read_template(base_template_dir / "index.html")
    base_css = read_template(base_template_dir / "style.css")
    variant_css = read_template(variant_dir / "style.css")
    js_code = read_template(base_template_dir / "script.js")

    # 合并CSS: 变体变量 + 基础样式
    full_css = variant_css + "\n" + base_css

    # 替换HTML模板变量
    html = html_template
    html = html.replace('{{SITE_TITLE}}', site_title)
    html = html.replace('{{SITE_DESCRIPTION}}', site_desc)
    html = html.replace('{{SITE_KEYWORDS}}', f"{site_name}导航,{site_name}网站,{site_name}网址大全")
    html = html.replace('{{SITE_NAME}}', site_name)
    html = html.replace('{{SITE_ICON}}', site_icon)
    html = html.replace('{{CENTRAL_HUB_URL}}', CENTRAL_HUB_URL)
    html = html.replace('{{EMBEDDED_CONFIG}}', json.dumps(config, ensure_ascii=False))

    # 写入文件
    with open(os.path.join(site_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    with open(os.path.join(site_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(full_css)
    with open(os.path.join(site_dir, 'script.js'), 'w', encoding='utf-8') as f:
        f.write(js_code)
    with open(os.path.join(site_dir, 'config.json'), 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    with open(os.path.join(site_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(generate_sitemap(site_url, site_name))
    with open(os.path.join(site_dir, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(generate_robots(site_url))
    with open(os.path.join(site_dir, '_headers'), 'w', encoding='utf-8') as f:
        f.write(generate_headers())

    return {
        'name': site_name,
        'pinyin': site_pinyin,
        'type': site_type,
        'url': site_url,
        'variant': variant,
        'categories': len(config.get('categories', [])),
        'links': sum(len(cat.get('links', [])) for cat in config.get('categories', []))
    }


def generate_cities():
    """生成所有城市站"""
    cities_data = load_json(DATA_DIR / "cities.json")
    if not cities_data:
        print("[!] 未找到 cities.json，跳过城市站生成")
        return []

    results = []
    cities_dir = SITES_DIR / "cities"

    for city in cities_data:
        city_pinyin = city.get('cityPinyin', '')
        if not city_pinyin:
            continue

        site_dir = cities_dir / city_pinyin
        config = {
            'siteType': 'city',
            'cityName': city.get('cityName', ''),
            'cityPinyin': city_pinyin,
            'province': city.get('province', ''),
            'categories': city.get('categories', [])
        }

        info = generate_site(site_dir, config, 'city')
        results.append(info)
        print(f"  [CITY] {info['name']} - {info['categories']}分类 {info['links']}链接 ({info['variant']})")

    return results


def generate_niches():
    """生成所有行业站"""
    niches_data = load_json(DATA_DIR / "niches.json")
    if not niches_data:
        print("[!] 未找到 niches.json，跳过行业站生成")
        return []

    results = []
    niches_dir = SITES_DIR / "niches"

    for niche in niches_data:
        niche_pinyin = niche.get('nichePinyin', '')
        if not niche_pinyin:
            continue

        site_dir = niches_dir / niche_pinyin
        config = {
            'siteType': 'niche',
            'nicheName': niche.get('nicheName', ''),
            'nichePinyin': niche_pinyin,
            'siteTitle': niche.get('siteTitle', f"{niche.get('nicheName', '')}导航"),
            'siteDescription': niche.get('siteDescription', ''),
            'categories': niche.get('categories', [])
        }

        info = generate_site(site_dir, config, 'niche')
        results.append(info)
        print(f"  [NICHE] {info['name']} - {info['categories']}分类 {info['links']}链接 ({info['variant']})")

    return results


def generate_hybrids():
    """生成组合站"""
    hybrids_data = load_json(DATA_DIR / "hybrids.json")
    if not hybrids_data:
        print("[!] 未找到 hybrids.json，跳过组合站生成")
        return []

    results = []
    hybrids_dir = SITES_DIR / "hybrids"

    for hybrid in hybrids_data:
        site_pinyin = hybrid.get('sitePinyin', '')
        if not site_pinyin:
            continue

        site_dir = hybrids_dir / site_pinyin
        config = {
            'siteType': 'hybrid',
            'cityName': hybrid.get('cityName', ''),
            'nicheName': hybrid.get('nicheName', ''),
            'sitePinyin': site_pinyin,
            'categories': hybrid.get('categories', [])
        }

        info = generate_site(site_dir, config, 'hybrid')
        results.append(info)
        print(f"  [HYBRID] {info['name']} - {info['categories']}分类 {info['links']}链接 ({info['variant']})")

    return results


def generate_central_hub(all_sites):
    """生成超级总站"""
    os.makedirs(HUB_DIR, exist_ok=True)

    cities = [s for s in all_sites if s['type'] == 'city']
    niches = [s for s in all_sites if s['type'] == 'niche']
    hybrids = [s for s in all_sites if s['type'] == 'hybrid']

    hub_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>导航百科 - 万站导航矩阵总站</title>
    <meta name="description" content="导航百科，汇集{len(all_sites)}个优质导航站，覆盖城市、行业、组合三大维度，一站式导航服务。">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f0f4f8; color: #1e293b; }}
        .header {{ background: linear-gradient(135deg, #2563eb, #7c3aed); color: #fff; padding: 48px 24px; text-align: center; }}
        .header h1 {{ font-size: 36px; margin-bottom: 12px; }}
        .header p {{ font-size: 18px; opacity: 0.9; }}
        .stats {{ display: flex; justify-content: center; gap: 48px; margin-top: 24px; }}
        .stat {{ text-align: center; }}
        .stat-num {{ font-size: 32px; font-weight: 700; }}
        .stat-label {{ font-size: 14px; opacity: 0.8; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 32px 24px; }}
        .section {{ margin-bottom: 48px; }}
        .section-title {{ font-size: 24px; font-weight: 700; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 3px solid #2563eb; display: flex; align-items: center; gap: 8px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }}
        .card {{ background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: transform 0.2s; text-align: center; }}
        .card:hover {{ transform: translateY(-4px); box-shadow: 0 4px 16px rgba(0,0,0,0.12); }}
        .card a {{ color: #2563eb; font-weight: 600; text-decoration: none; }}
        .card-icon {{ font-size: 32px; margin-bottom: 8px; }}
        .card-meta {{ font-size: 12px; color: #64748b; margin-top: 8px; }}
        .footer {{ background: #1e293b; color: #cbd5e1; padding: 32px 24px; text-align: center; }}
        .footer a {{ color: #93c5fd; }}
        @media (max-width: 768px) {{ .stats {{ flex-direction: column; gap: 16px; }} .grid {{ grid-template-columns: 1fr 1fr; }} }}
    </style>
</head>
<body>
    <div class="header">
        <h1>导航百科</h1>
        <p>万站导航矩阵 · 一站直达全网</p>
        <div class="stats">
            <div class="stat"><div class="stat-num">{len(cities)}</div><div class="stat-label">城市导航</div></div>
            <div class="stat"><div class="stat-num">{len(niches)}</div><div class="stat-label">行业导航</div></div>
            <div class="stat"><div class="stat-num">{len(hybrids)}</div><div class="stat-label">组合导航</div></div>
            <div class="stat"><div class="stat-num">{len(all_sites)}</div><div class="stat-label">总站点数</div></div>
        </div>
    </div>
    <div class="container">"""

    # 城市站
    if cities:
        hub_html += """
        <div class="section">
            <div class="section-title">🏙️ 城市导航</div>
            <div class="grid">"""
        for s in cities:
            hub_html += f"""
                <div class="card">
                    <div class="card-icon">🏙️</div>
                    <a href="{s['url']}" target="_blank">{s['name']}</a>
                    <div class="card-meta">{s['categories']}分类 · {s['links']}链接</div>
                </div>"""
        hub_html += """
            </div>
        </div>"""

    # 行业站
    if niches:
        hub_html += """
        <div class="section">
            <div class="section-title">🏷️ 行业导航</div>
            <div class="grid">"""
        for s in niches:
            hub_html += f"""
                <div class="card">
                    <div class="card-icon">🏷️</div>
                    <a href="{s['url']}" target="_blank">{s['name']}</a>
                    <div class="card-meta">{s['categories']}分类 · {s['links']}链接</div>
                </div>"""
        hub_html += """
            </div>
        </div>"""

    # 组合站
    if hybrids:
        hub_html += """
        <div class="section">
            <div class="section-title">🔗 组合导航</div>
            <div class="grid">"""
        for s in hybrids:
            hub_html += f"""
                <div class="card">
                    <div class="card-icon">🔗</div>
                    <a href="{s['url']}" target="_blank">{s['name']}</a>
                    <div class="card-meta">{s['categories']}分类 · {s['links']}链接</div>
                </div>"""
        hub_html += """
            </div>
        </div>"""

    hub_html += f"""
    </div>
    <div class="footer">
        <p>导航百科 · 万站导航矩阵</p>
        <p>联系邮箱: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> | QQ: {CONTACT_QQ}</p>
        <p>本站仅提供链接跳转服务，所有内容归原网站所有</p>
        <p>© 2026 导航百科. All rights reserved.</p>
    </div>
</body>
</html>"""

    with open(HUB_DIR / 'index.html', 'w', encoding='utf-8') as f:
        f.write(hub_html)

    print(f"  [HUB] 超级总站已生成 ({len(all_sites)}个站点入口)")


def generate_management_data(all_sites):
    """生成管理数据"""
    os.makedirs(DEPLOYED_DIR, exist_ok=True)

    management = {
        'lastUpdate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'totalSites': len(all_sites),
        'siteTypes': {
            'city': len([s for s in all_sites if s['type'] == 'city']),
            'niche': len([s for s in all_sites if s['type'] == 'niche']),
            'hybrid': len([s for s in all_sites if s['type'] == 'hybrid'])
        },
        'totalLinks': sum(s['links'] for s in all_sites),
        'totalCategories': sum(s['categories'] for s in all_sites),
        'variants': {v: len([s for s in all_sites if s['variant'] == v]) for v in VARIANTS},
        'sites': all_sites
    }

    save_json(DEPLOYED_DIR / 'management.json', management)
    print(f"  [MGMT] 管理数据已生成 (总计{len(all_sites)}站)")


def main():
    parser = argparse.ArgumentParser(description='导航矩阵统一生成引擎')
    parser.add_argument('--type', choices=['cities', 'niches', 'hybrids', 'all'], default='all', help='生成类型')
    parser.add_argument('--site', type=str, help='生成指定站点')
    args = parser.parse_args()

    print("=" * 60)
    print("  导航矩阵统一生成引擎 v1.0")
    print("=" * 60)
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  模式: {args.type}")
    print()

    all_sites = []

    if args.type in ('cities', 'all'):
        print("[1] 生成城市站...")
        all_sites.extend(generate_cities())
        print()

    if args.type in ('niches', 'all'):
        print("[2] 生成行业站...")
        all_sites.extend(generate_niches())
        print()

    if args.type in ('hybrids', 'all'):
        print("[3] 生成组合站...")
        all_sites.extend(generate_hybrids())
        print()

    if all_sites:
        print("[4] 生成超级总站...")
        generate_central_hub(all_sites)
        print()

        print("[5] 生成管理数据...")
        generate_management_data(all_sites)
        print()

    # 汇总报告
    print("=" * 60)
    print("  生成完成!")
    print("=" * 60)
    print(f"  总站点数: {len(all_sites)}")
    print(f"  总分类数: {sum(s['categories'] for s in all_sites)}")
    print(f"  总链接数: {sum(s['links'] for s in all_sites)}")
    variant_stats = ', '.join(f"{v}={len([s for s in all_sites if s['variant']==v])}" for v in VARIANTS)
    print(f"  模板分布: {variant_stats}")
    print()


if __name__ == '__main__':
    main()
