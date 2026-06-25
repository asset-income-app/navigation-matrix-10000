#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动修复系统 - auto_repair.py
自动检测和修复站点问题，确保站点健康运行
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
SITES_DIR = ROOT_DIR / "02-sites"
LOGS_DIR = DATA_DIR / "logs"

# 模板目录
TEMPLATES_DIR = ROOT_DIR / "01-templates" / "base"

def check_site_health(site_dir):
    """检查站点健康状态"""
    issues = []
    
    # 检查必要文件
    required_files = ['config.json', 'index.html', 'style.css', 'script.js']
    for file in required_files:
        if not (site_dir / file).exists():
            issues.append(f"缺少文件: {file}")
    
    # 检查config.json格式
    config_file = site_dir / "config.json"
    if config_file.exists():
        try:
            config = json.loads(config_file.read_text())
            
            # 检查必要字段
            if 'siteType' not in config:
                issues.append("config.json缺少siteType")
            if 'categories' not in config or not config['categories']:
                issues.append("config.json缺少categories或为空")
            
            # 检查链接数量
            total_links = sum(len(cat.get('links', [])) for cat in config.get('categories', []))
            if total_links < 5:
                issues.append(f"链接数量过少: {total_links}")
            
        except json.JSONDecodeError:
            issues.append("config.json格式错误")
    
    # 检查index.html内嵌数据
    index_file = site_dir / "index.html"
    if index_file.exists():
        content = index_file.read_text()
        if 'window.__SITE_CONFIG__' not in content:
            issues.append("index.html缺少内嵌数据")
    
    return issues

def repair_missing_files(site_dir, site_type):
    """修复缺失文件"""
    site_name = site_dir.name
    
    # 从模板复制缺失文件
    for template_file in ['style.css', 'script.js']:
        target_file = site_dir / template_file
        if not target_file.exists():
            shutil.copy(TEMPLATES_DIR / template_file, target_file)
            print(f"  ✅ 已复制: {template_file}")
    
    # 生成index.html（如果缺失）
    index_file = site_dir / "index.html"
    if not index_file.exists():
        config_file = site_dir / "config.json"
        if config_file.exists():
            config = json.loads(config_file.read_text())
            generate_index_html(site_dir, config)
            print(f"  ✅ 已生成: index.html")
    
    # 生成SEO文件
    for seo_file in ['robots.txt', 'sitemap.xml', '_headers']:
        if not (site_dir / seo_file).exists():
            generate_seo_file(site_dir, seo_file, site_type)
            print(f"  ✅ 已生成: {seo_file}")

def repair_config_json(site_dir):
    """修复config.json"""
    config_file = site_dir / "config.json"
    
    if not config_file.exists():
        # 创建最小配置
        config = {
            "siteType": "unknown",
            "siteTitle": site_dir.name,
            "categories": []
        }
        config_file.write_text(json.dumps(config, indent=2))
        print(f"  ✅ 已创建: config.json")
        return
    
    try:
        config = json.loads(config_file.read_text())
        
        # 修复缺失字段
        if 'siteType' not in config:
            config['siteType'] = 'unknown'
        
        if 'categories' not in config:
            config['categories'] = []
        
        # 修复空分类
        for cat in config['categories']:
            if 'links' not in cat:
                cat['links'] = []
            if 'name' not in cat:
                cat['name'] = '未命名分类'
        
        config_file.write_text(json.dumps(config, indent=2))
        print(f"  ✅ 已修复: config.json")
        
    except json.JSONDecodeError:
        # JSON格式错误，重新创建
        print(f"  ⚠️ JSON格式错误，重新创建")
        config = {"siteType": "unknown", "siteTitle": site_dir.name, "categories": []}
        config_file.write_text(json.dumps(config, indent=2))

def repair_index_html(site_dir):
    """修复index.html内嵌数据"""
    index_file = site_dir / "index.html"
    config_file = site_dir / "config.json"
    
    if not index_file.exists() or not config_file.exists():
        return
    
    config = json.loads(config_file.read_text())
    content = index_file.read_text()
    
    # 检查是否有内嵌数据
    if 'window.__SITE_CONFIG__' not in content:
        # 添加内嵌数据
        config_script = f'<script>window.__SITE_CONFIG__ = {json.dumps(config)};</script>'
        
        # 在<head>后插入
        if '</head>' in content:
            content = content.replace('</head>', config_script + '</head>')
            index_file.write_text(content)
            print(f"  ✅ 已添加内嵌数据")

def generate_index_html(site_dir, config):
    """生成index.html"""
    template_file = TEMPLATES_DIR / "index.html"
    if not template_file.exists():
        return
    
    content = template_file.read_text()
    
    # 内嵌配置
    config_script = f'<script>window.__SITE_CONFIG__ = {json.dumps(config)};</script>'
    content = content.replace('</head>', config_script + '</head>')
    
    # 替换标题
    if 'siteTitle' in config:
        content = content.replace('<title>导航站</title>', f'<title>{config["siteTitle"]}</title>')
    
    (site_dir / "index.html").write_text(content)

def generate_seo_file(site_dir, seo_file, site_type):
    """生成SEO文件"""
    site_name = site_dir.name
    
    if seo_file == 'robots.txt':
        content = f"""User-agent: *
Allow: /
Sitemap: https://{site_name}-nav.pages.dev/sitemap.xml
"""
    elif seo_file == 'sitemap.xml':
        content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://{site_name}-nav.pages.dev/</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""
    elif seo_file == '_headers':
        content = """/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
"""
    
    (site_dir / seo_file).write_text(content)

def repair_site(site_name, site_type):
    """修复单个站点"""
    site_dir = SITES_DIR / site_type / site_name
    
    if not site_dir.exists():
        print(f"❌ 站点不存在: {site_name}")
        return False
    
    print(f"\n🔧 修复站点: {site_name}")
    
    # 检查问题
    issues = check_site_health(site_dir)
    
    if not issues:
        print(f"  ✅ 站点健康，无需修复")
        return True
    
    print(f"  发现问题: {len(issues)} 个")
    for issue in issues:
        print(f"    - {issue}")
    
    # 执行修复
    repair_missing_files(site_dir, site_type)
    repair_config_json(site_dir)
    repair_index_html(site_dir)
    
    # 再次检查
    new_issues = check_site_health(site_dir)
    
    if new_issues:
        print(f"  ⚠️ 仍有问题: {len(new_issues)} 个")
        return False
    else:
        print(f"  ✅ 修复完成")
        return True

def repair_all_sites():
    """修复所有站点"""
    print("\n" + "="*60)
    print("🔧 批量修复所有站点")
    print("="*60)
    
    repaired = 0
    failed = 0
    
    for site_type in ['cities', 'niches', 'hybrids']:
        type_dir = SITES_DIR / site_type
        if not type_dir.exists():
            continue
        
        for site_dir in type_dir.iterdir():
            if site_dir.is_dir() and not site_dir.name.startswith('.'):
                if repair_site(site_dir.name, site_type):
                    repaired += 1
                else:
                    failed += 1
    
    print("\n" + "="*60)
    print(f"✅ 修复完成: {repaired} 个成功, {failed} 个失败")
    print("="*60)
    
    # 记录日志
    log_file = LOGS_DIR / "daily" / datetime.now().strftime("%Y-%m") / f"repair_{datetime.now().strftime('%Y-%m-%d')}.json"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "repaired": repaired,
        "failed": failed
    }
    log_file.write_text(json.dumps(log_data, indent=2))

def show_repair_report():
    """显示修复报告"""
    print("\n" + "="*60)
    print("📊 修复报告")
    print("="*60)
    
    # 扫描所有站点问题
    total_issues = 0
    problem_sites = []
    
    for site_type in ['cities', 'niches', 'hybrids']:
        type_dir = SITES_DIR / site_type
        if not type_dir.exists():
            continue
        
        for site_dir in type_dir.iterdir():
            if site_dir.is_dir() and not site_dir.name.startswith('.'):
                issues = check_site_health(site_dir)
                if issues:
                    total_issues += len(issues)
                    problem_sites.append({
                        "name": site_dir.name,
                        "type": site_type,
                        "issues": issues
                    })
    
    print(f"\n站点总数: {sum(1 for _ in SITES_DIR.rglob('config.json'))}")
    print(f"问题站点: {len(problem_sites)} 个")
    print(f"问题总数: {total_issues} 个")
    
    if problem_sites:
        print("\n问题站点列表:")
        for site in problem_sites[:10]:
            print(f"\n  {site['name']} ({site['type']}):")
            for issue in site['issues']:
                print(f"    - {issue}")

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "repair":
            if len(sys.argv) >= 4:
                repair_site(sys.argv[2], sys.argv[3])
            else:
                repair_all_sites()
        elif command == "check":
            if len(sys.argv) >= 4:
                site_dir = SITES_DIR / sys.argv[3] / sys.argv[2]
                issues = check_site_health(site_dir)
                print(f"\n站点: {sys.argv[2]}")
                if issues:
                    print(f"问题: {len(issues)} 个")
                    for issue in issues:
                        print(f"  - {issue}")
                else:
                    print("✅ 健康")
            else:
                show_repair_report()
        else:
            print("用法: python auto_repair.py [repair|check]")
    else:
        # 默认检查并修复
        show_repair_report()
        repair_all_sites()

if __name__ == "__main__":
    main()