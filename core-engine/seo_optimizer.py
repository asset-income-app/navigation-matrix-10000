#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO优化系统 - seo_optimizer.py
自动化SEO优化，提升站点搜索排名
"""

import os
import json
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).parent.parent
SITES_DIR = ROOT_DIR / "02-sites"
DATA_DIR = ROOT_DIR / "data"

def optimize_site_seo(site_dir, site_type):
    """优化单个站点的SEO"""
    config_file = site_dir / "config.json"
    
    if not config_file.exists():
        return False
    
    config = json.loads(config_file.read_text(encoding='utf-8'))
    
    # SEO优化项
    optimizations = []
    
    # 1. 优化标题
    if 'siteTitle' in config:
        title = config['siteTitle']
        if len(title) < 30:
            # 标题太短，补充关键词
            if site_type == 'city':
                title += f" - {config.get('cityName', '')}本地导航"
            elif site_type == 'niche':
                title += f" - {config.get('nicheCategory', '')}导航"
            elif site_type == 'hybrid':
                title += f" - {config.get('cityName', '')}{config.get('nicheName', '')}导航"
            config['siteTitle'] = title
            optimizations.append('标题优化')
    
    # 2. 优化描述
    if 'siteDescription' in config:
        desc = config['siteDescription']
        if len(desc) < 50:
            # 描述太短，补充内容
            if site_type == 'city':
                desc += f"覆盖{config.get('cityName', '')}政务、社保、医疗、教育、交通、生活等全方位导航服务。"
            elif site_type == 'niche':
                desc += f"提供{config.get('nicheName', '')}最新资讯、学习资源、工具软件、社区论坛等一站式服务。"
            elif site_type == 'hybrid':
                desc += f"专注{config.get('cityName', '')}{config.get('nicheName', '')}领域，提供本地化专业导航服务。"
            config['siteDescription'] = desc
            optimizations.append('描述优化')
    
    # 3. 添加关键词
    if 'keywords' not in config:
        keywords = []
        if site_type == 'city':
            city_name = config.get('cityName', '')
            keywords = [city_name, f"{city_name}导航", f"{city_name}网站导航", f"{city_name}网址导航"]
        elif site_type == 'niche':
            niche_name = config.get('nicheName', '')
            keywords = [niche_name, f"{niche_name}导航", f"{niche_name}网站导航", f"{niche_name}学习"]
        elif site_type == 'hybrid':
            city_name = config.get('cityName', '')
            niche_name = config.get('nicheName', '')
            keywords = [f"{city_name}{niche_name}", f"{city_name}{niche_name}导航", f"{city_name}{niche_name}服务"]
        config['keywords'] = keywords
        optimizations.append('关键词优化')
    
    # 4. 优化robots.txt
    robots_file = site_dir / "robots.txt"
    if robots_file.exists():
        robots_content = robots_file.read_text()
        if 'Sitemap' not in robots_content:
            site_pinyin = config.get('cityPinyin') or config.get('nichePinyin') or config.get('sitePinyin', '')
            if site_pinyin:
                sitemap_url = f"https://{site_pinyin}-nav.pages.dev/sitemap.xml"
                robots_content += f"\nSitemap: {sitemap_url}\n"
                robots_file.write_text(robots_content)
                optimizations.append('robots.txt优化')
    
    # 5. 优化sitemap.xml
    sitemap_file = site_dir / "sitemap.xml"
    if sitemap_file.exists():
        sitemap_content = sitemap_file.read_text()
        # 添加更多URL（分类页面）
        if len(sitemap_content) < 500:
            categories = config.get('categories', [])
            additional_urls = []
            for cat in categories:
                cat_name = cat.get('name', '')
                if cat_name:
                    additional_urls.append(f"""
  <url>
    <loc>https://{config.get('cityPinyin') or config.get('nichePinyin') or config.get('sitePinyin', '')}-nav.pages.dev/#{cat_name}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
""")
            if additional_urls:
                sitemap_content = sitemap_content.replace('</urlset>', ''.join(additional_urls) + '</urlset>')
                sitemap_file.write_text(sitemap_content)
                optimizations.append('sitemap.xml优化')
    
    # 保存优化后的配置
    if optimizations:
        config_file.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding='utf-8')
    
    return optimizations

def batch_optimize_seo():
    """批量优化所有站点SEO"""
    print("\n" + "="*60)
    print("🔍 SEO优化系统 - 批量优化")
    print("="*60)
    
    total_optimized = 0
    total_optimizations = 0
    
    for site_type in ['cities', 'niches', 'hybrids']:
        type_dir = SITES_DIR / site_type
        if not type_dir.exists():
            continue
        
        sites = [d for d in type_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        print(f"\n优化 {site_type} 类型站点 ({len(sites)} 个)...")
        
        for site_dir in sites:
            optimizations = optimize_site_seo(site_dir, site_type)
            
            if optimizations:
                total_optimized += 1
                total_optimizations += len(optimizations)
                print(f"  ✅ {site_dir.name}: {', '.join(optimizations)}")
    
    # 生成SEO优化报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_sites": total_optimized,
        "total_optimizations": total_optimizations,
        "optimization_types": {
            "标题优化": 0,
            "描述优化": 0,
            "关键词优化": 0,
            "robots.txt优化": 0,
            "sitemap.xml优化": 0
        }
    }
    
    report_file = DATA_DIR / "logs" / "seo_optimization_report.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(json.dumps(report, indent=2))
    
    print("\n" + "="*60)
    print("📊 SEO优化报告")
    print("="*60)
    print(f"优化站点数: {total_optimized}")
    print(f"优化项总数: {total_optimizations}")
    print(f"报告文件: {report_file}")
    print("="*60)

def generate_seo_keywords():
    """生成SEO关键词库"""
    print("\n" + "="*60)
    print("📝 生成SEO关键词库")
    print("="*60)
    
    keywords_db = {
        "城市关键词": [],
        "行业关键词": [],
        "组合关键词": []
    }
    
    # 从cities.json提取关键词
    cities_file = DATA_DIR / "cities.json"
    if cities_file.exists():
        cities = json.loads(cities_file.read_text(encoding='utf-8'))
        for city in cities:
            city_name = city.get('cityName', '')
            if city_name:
                keywords_db["城市关键词"].extend([
                    city_name,
                    f"{city_name}导航",
                    f"{city_name}网站导航",
                    f"{city_name}网址导航",
                    f"{city_name}本地服务"
                ])
    
    # 从niches.json提取关键词
    niches_file = DATA_DIR / "niches.json"
    if niches_file.exists():
        niches = json.loads(niches_file.read_text(encoding='utf-8'))
        for niche in niches:
            niche_name = niche.get('nicheName', '')
            niche_category = niche.get('nicheCategory', '')
            if niche_name:
                keywords_db["行业关键词"].extend([
                    niche_name,
                    f"{niche_name}导航",
                    f"{niche_name}网站导航",
                    f"{niche_name}学习",
                    f"{niche_name}培训",
                    f"{niche_category}导航"
                ])
    
    # 生成组合关键词
    for city_kw in keywords_db["城市关键词"][:50]:
        for niche_kw in keywords_db["行业关键词"][:50]:
            if not city_kw.endswith('导航') and not niche_kw.endswith('导航'):
                keywords_db["组合关键词"].append(f"{city_kw}{niche_kw}")
    
    # 保存关键词库
    keywords_file = DATA_DIR / "seo_keywords.json"
    keywords_file.write_text(json.dumps(keywords_db, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"✅ 已生成关键词库")
    print(f"  城市关键词: {len(keywords_db['城市关键词'])} 个")
    print(f"  行业关键词: {len(keywords_db['行业关键词'])} 个")
    print(f"  组合关键词: {len(keywords_db['组合关键词'])} 个")
    print(f"  文件: {keywords_file}")
    print("="*60)

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "optimize":
            batch_optimize_seo()
        elif command == "keywords":
            generate_seo_keywords()
        else:
            print("用法: python seo_optimizer.py [optimize|keywords]")
    else:
        # 默认执行所有优化
        batch_optimize_seo()
        generate_seo_keywords()

if __name__ == "__main__":
    main()