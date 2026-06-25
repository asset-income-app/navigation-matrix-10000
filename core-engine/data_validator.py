#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据验证系统 - data_validator.py
验证所有站点数据的完整性和正确性
"""

import os
import json
from datetime import datetime
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
SITES_DIR = ROOT_DIR / "02-sites"
LOGS_DIR = DATA_DIR / "logs"

def validate_config(config, site_type):
    """验证配置文件"""
    errors = []
    warnings = []
    
    # 必要字段检查
    required_fields = {
        'city': ['siteType', 'cityName', 'cityPinyin', 'province', 'categories'],
        'niche': ['siteType', 'nicheName', 'nichePinyin', 'siteTitle', 'siteDescription', 'categories'],
        'hybrid': ['siteType', 'cityName', 'nicheName', 'categories']
    }
    
    for field in required_fields.get(site_type, []):
        if field not in config:
            errors.append(f"缺少必要字段: {field}")
    
    # 分类检查
    if 'categories' in config:
        if not config['categories']:
            errors.append("categories为空")
        
        for i, cat in enumerate(config['categories']):
            if 'name' not in cat:
                errors.append(f"分类{i}缺少name")
            
            if 'links' not in cat:
                warnings.append(f"分类{i}缺少links")
            elif not cat['links']:
                warnings.append(f"分类{i}的links为空")
            elif len(cat['links']) < 5:
                warnings.append(f"分类{i}链接数量少于5个")
            elif len(cat['links']) > 20:
                warnings.append(f"分类{i}链接数量超过20个")
            
            # 链接格式检查
            for j, link in enumerate(cat.get('links', [])):
                if 'url' not in link:
                    errors.append(f"分类{i}链接{j}缺少url")
                elif not link['url'].startswith(('http://', 'https://', 'tel:')):
                    errors.append(f"分类{i}链接{j} URL格式错误: {link['url']}")
                
                if 'name' not in link:
                    warnings.append(f"分类{i}链接{j}缺少name")
    
    # 联系方式检查
    if 'contact' not in config:
        warnings.append("缺少contact字段")
    
    return {"errors": errors, "warnings": warnings}

def validate_site(site_dir, site_type):
    """验证单个站点"""
    results = {
        "site": site_dir.name,
        "type": site_type,
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # 检查必要文件
    required_files = ['config.json', 'index.html']
    for file in required_files:
        if not (site_dir / file).exists():
            results['errors'].append(f"缺少文件: {file}")
            results['valid'] = False
    
    # 验证config.json
    config_file = site_dir / "config.json"
    if config_file.exists():
        try:
            config = json.loads(config_file.read_text())
            validation = validate_config(config, site_type)
            
            results['errors'].extend(validation['errors'])
            results['warnings'].extend(validation['warnings'])
            
            if validation['errors']:
                results['valid'] = False
                
        except json.JSONDecodeError as e:
            results['errors'].append(f"config.json格式错误: {e}")
            results['valid'] = False
    
    # 验证index.html
    index_file = site_dir / "index.html"
    if index_file.exists():
        content = index_file.read_text()
        
        if 'window.__SITE_CONFIG__' not in content:
            results['warnings'].append("index.html缺少内嵌数据")
        
        if '<title>' not in content:
            results['warnings'].append("index.html缺少title标签")
        
        if '</html>' not in content:
            results['errors'].append("index.html不完整")
            results['valid'] = False
    
    # 验证SEO文件
    seo_files = ['robots.txt', 'sitemap.xml']
    for file in seo_files:
        if not (site_dir / file).exists():
            results['warnings'].append(f"缺少SEO文件: {file}")
    
    return results

def validate_all_sites():
    """验证所有站点"""
    print("\n" + "="*60)
    print("🔍 数据验证开始")
    print("="*60)
    
    all_results = []
    valid_count = 0
    invalid_count = 0
    total_errors = 0
    total_warnings = 0
    
    for site_type in ['cities', 'niches', 'hybrids']:
        type_dir = SITES_DIR / site_type
        if not type_dir.exists():
            continue
        
        print(f"\n验证 {site_type}...")
        
        for site_dir in type_dir.iterdir():
            if site_dir.is_dir() and not site_dir.name.startswith('.'):
                result = validate_site(site_dir, site_type)
                all_results.append(result)
                
                if result['valid']:
                    valid_count += 1
                else:
                    invalid_count += 1
                
                total_errors += len(result['errors'])
                total_warnings += len(result['warnings'])
                
                # 显示状态
                if result['errors']:
                    print(f"  ❌ {site_dir.name}: {len(result['errors'])} 错误")
                elif result['warnings']:
                    print(f"  ⚠️ {site_dir.name}: {len(result['warnings'])} 警告")
                else:
                    print(f"  ✅ {site_dir.name}: 通过")
    
    # 生成报告
    print("\n" + "="*60)
    print("📊 验证结果")
    print("="*60)
    print(f"站点总数: {valid_count + invalid_count}")
    print(f"通过站点: {valid_count}")
    print(f"问题站点: {invalid_count}")
    print(f"错误总数: {total_errors}")
    print(f"警告总数: {total_warnings}")
    
    # 保存报告
    report_file = LOGS_DIR / "daily" / datetime.now().strftime("%Y-%m") / f"validation_{datetime.now().strftime('%Y-%m-%d')}.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": valid_count + invalid_count,
            "valid": valid_count,
            "invalid": invalid_count,
            "errors": total_errors,
            "warnings": total_warnings
        },
        "sites": all_results
    }
    report_file.write_text(json.dumps(report_data, indent=2))
    
    print(f"\n报告已保存: {report_file}")
    
    # 显示问题站点详情
    if invalid_count > 0:
        print("\n问题站点详情:")
        for site in all_results:
            if site['errors']:
                print(f"\n{site['site']} ({site['type']}):")
                for error in site['errors']:
                    print(f"  ❌ {error}")
    
    return report_data

def show_validation_report():
    """显示验证报告"""
    print("\n" + "="*60)
    print("📊 数据验证报告")
    print("="*60)
    
    # 找最新报告
    report_dir = LOGS_DIR / "daily"
    if not report_dir.exists():
        print("没有验证报告")
        return
    
    latest_report = None
    for month_dir in sorted(report_dir.iterdir(), reverse=True):
        if month_dir.is_dir():
            reports = sorted(month_dir.glob("validation_*.json"), reverse=True)
            if reports:
                latest_report = reports[0]
                break
    
    if not latest_report:
        print("没有验证报告")
        return
    
    report = json.loads(latest_report.read_text())
    
    print(f"报告时间: {report['timestamp']}")
    print(f"站点总数: {report['summary']['total']}")
    print(f"通过率: {report['summary']['valid'] / report['summary']['total'] * 100:.1f}%")
    
    # 显示问题站点
    problem_sites = [s for s in report['sites'] if s['errors']]
    if problem_sites:
        print(f"\n问题站点 ({len(problem_sites)} 个):")
        for site in problem_sites[:10]:
            print(f"  {site['site']}: {len(site['errors'])} 错误")

def validate_data_files():
    """验证数据文件"""
    print("\n" + "="*60)
    print("🔍 数据文件验证")
    print("="*60)
    
    data_files = ['cities.json', 'niches.json', 'master-links.json', 'template-assignment.json']
    
    for file in data_files:
        file_path = DATA_DIR / file
        if not file_path.exists():
            print(f"❌ {file}: 不存在")
            continue
        
        try:
            data = json.loads(file_path.read_text())
            
            if isinstance(data, list):
                print(f"✅ {file}: {len(data)} 条记录")
            elif isinstance(data, dict):
                print(f"✅ {file}: {len(data)} 个键")
            else:
                print(f"⚠️ {file}: 格式异常")
                
        except json.JSONDecodeError:
            print(f"❌ {file}: JSON格式错误")

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "validate":
            validate_all_sites()
        elif command == "report":
            show_validation_report()
        elif command == "data":
            validate_data_files()
        elif command == "site":
            if len(sys.argv) >= 4:
                site_dir = SITES_DIR / sys.argv[3] / sys.argv[2]
                result = validate_site(site_dir, sys.argv[3])
                print(f"\n站点: {sys.argv[2]}")
                print(f"状态: {'通过' if result['valid'] else '失败'}")
                if result['errors']:
                    print("错误:")
                    for e in result['errors']:
                        print(f"  ❌ {e}")
                if result['warnings']:
                    print("警告:")
                    for w in result['warnings']:
                        print(f"  ⚠️ {w}")
        else:
            print("用法: python data_validator.py [validate|report|data|site]")
    else:
        # 默认验证所有
        validate_all_sites()
        validate_data_files()

if __name__ == "__main__":
    main()