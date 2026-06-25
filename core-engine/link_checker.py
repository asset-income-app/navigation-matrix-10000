#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
链接检查系统 - link_checker.py
检查所有站点链接的有效性，发现失效链接
"""

import os
import json
import urllib.request
import urllib.error
import socket
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
SITES_DIR = ROOT_DIR / "02-sites"
LOGS_DIR = DATA_DIR / "logs"

# 超时设置
TIMEOUT = 10  # 秒
MAX_WORKERS = 20  # 并发数

def check_link(url):
    """检查单个链接"""
    if url.startswith('tel:') or url.startswith('mailto:'):
        return {"status": "skip", "reason": "非HTTP链接"}
    
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) LinkChecker/1.0'}
        )
        
        response = urllib.request.urlopen(req, timeout=TIMEOUT)
        status_code = response.getcode()
        
        if status_code == 200:
            return {"status": "ok", "code": status_code}
        elif status_code in [301, 302, 303, 307, 308]:
            return {"status": "redirect", "code": status_code}
        else:
            return {"status": "error", "code": status_code}
            
    except urllib.error.HTTPError as e:
        return {"status": "error", "code": e.code, "reason": str(e)}
    except urllib.error.URLError as e:
        return {"status": "error", "reason": f"URL错误: {e.reason}"}
    except socket.timeout:
        return {"status": "error", "reason": "超时"}
    except Exception as e:
        return {"status": "error", "reason": str(e)}

def check_site_links(site_dir):
    """检查站点所有链接"""
    config_file = site_dir / "config.json"
    if not config_file.exists():
        return None
    
    config = json.loads(config_file.read_text())
    
    results = {
        "site": site_dir.name,
        "total": 0,
        "ok": 0,
        "redirect": 0,
        "error": 0,
        "skip": 0,
        "broken_links": []
    }
    
    all_links = []
    for cat in config.get('categories', []):
        for link in cat.get('links', []):
            all_links.append({
                "url": link.get('url', ''),
                "name": link.get('name', ''),
                "category": cat.get('name', '')
            })
    
    results["total"] = len(all_links)
    
    # 并发检查
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_link = {
            executor.submit(check_link, link['url']): link
            for link in all_links
        }
        
        for future in as_completed(future_to_link):
            link = future_to_link[future]
            try:
                result = future.result()
                
                if result['status'] == 'ok':
                    results['ok'] += 1
                elif result['status'] == 'redirect':
                    results['redirect'] += 1
                elif result['status'] == 'error':
                    results['error'] += 1
                    results['broken_links'].append({
                        "url": link['url'],
                        "name": link['name'],
                        "category": link['category'],
                        "reason": result.get('reason', '未知')
                    })
                else:
                    results['skip'] += 1
                    
            except Exception as e:
                results['error'] += 1
                results['broken_links'].append({
                    "url": link['url'],
                    "name": link['name'],
                    "category": link['category'],
                    "reason": str(e)
                })
    
    return results

def check_all_sites():
    """检查所有站点链接"""
    print("\n" + "="*60)
    print("🔗 链接检查开始")
    print("="*60)
    
    all_results = []
    total_links = 0
    total_ok = 0
    total_error = 0
    
    for site_type in ['cities', 'niches', 'hybrids']:
        type_dir = SITES_DIR / site_type
        if not type_dir.exists():
            continue
        
        print(f"\n检查 {site_type}...")
        
        for site_dir in type_dir.iterdir():
            if site_dir.is_dir() and not site_dir.name.startswith('.'):
                result = check_site_links(site_dir)
                if result:
                    all_results.append(result)
                    total_links += result['total']
                    total_ok += result['ok']
                    total_error += result['error']
                    
                    # 显示进度
                    if result['error'] > 0:
                        print(f"  ⚠️ {site_dir.name}: {result['error']}/{result['total']} 失效")
                    else:
                        print(f"  ✅ {site_dir.name}: {result['total']} 全部正常")
    
    # 生成报告
    print("\n" + "="*60)
    print("📊 检查结果")
    print("="*60)
    print(f"总链接数: {total_links}")
    print(f"正常链接: {total_ok} ({total_ok/total_links*100:.1f}%)")
    print(f"失效链接: {total_error} ({total_error/total_links*100:.1f}%)")
    
    # 保存报告
    report_file = LOGS_DIR / "daily" / datetime.now().strftime("%Y-%m") / f"links_{datetime.now().strftime('%Y-%m-%d')}.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_links": total_links,
            "ok": total_ok,
            "error": total_error,
            "ok_rate": total_ok / total_links * 100 if total_links > 0 else 0
        },
        "sites": all_results
    }
    report_file.write_text(json.dumps(report_data, indent=2))
    
    print(f"\n报告已保存: {report_file}")
    
    # 显示失效链接详情
    if total_error > 0:
        print("\n失效链接详情:")
        for site in all_results:
            if site['broken_links']:
                print(f"\n{site['site']}:")
                for link in site['broken_links'][:5]:
                    print(f"  - {link['name']}: {link['url']}")
                    print(f"    原因: {link['reason']}")
    
    return report_data

def show_broken_links():
    """显示失效链接"""
    print("\n" + "="*60)
    print("❌ 失效链接列表")
    print("="*60)
    
    # 找最新的报告
    report_dir = LOGS_DIR / "daily"
    if not report_dir.exists():
        print("没有检查报告")
        return
    
    latest_report = None
    for month_dir in sorted(report_dir.iterdir(), reverse=True):
        if month_dir.is_dir():
            reports = sorted(month_dir.glob("links_*.json"), reverse=True)
            if reports:
                latest_report = reports[0]
                break
    
    if not latest_report:
        print("没有检查报告")
        return
    
    report = json.loads(latest_report.read_text())
    
    print(f"报告时间: {report['timestamp']}")
    print(f"失效链接: {report['summary']['error']} 个")
    
    for site in report['sites']:
        if site['broken_links']:
            print(f"\n{site['site']} ({len(site['broken_links'])} 个):")
            for link in site['broken_links']:
                print(f"  - {link['name']}")
                print(f"    URL: {link['url']}")
                print(f"    分类: {link['category']}")
                print(f"    原因: {link['reason']}")

def export_broken_links(output_file):
    """导出失效链接"""
    report_dir = LOGS_DIR / "daily"
    if not report_dir.exists():
        return
    
    latest_report = None
    for month_dir in sorted(report_dir.iterdir(), reverse=True):
        if month_dir.is_dir():
            reports = sorted(month_dir.glob("links_*.json"), reverse=True)
            if reports:
                latest_report = reports[0]
                break
    
    if not latest_report:
        return
    
    report = json.loads(latest_report.read_text())
    
    # 导出CSV格式
    output_path = Path(output_file)
    lines = ["站点,链接名称,URL,分类,失效原因"]
    
    for site in report['sites']:
        for link in site['broken_links']:
            lines.append(f"{site['site']},{link['name']},{link['url']},{link['category']},{link['reason']}")
    
    output_path.write_text('\n'.join(lines))
    print(f"✅ 已导出: {output_path}")

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            check_all_sites()
        elif command == "show":
            show_broken_links()
        elif command == "export":
            if len(sys.argv) >= 3:
                export_broken_links(sys.argv[2])
            else:
                export_broken_links("broken_links.csv")
        elif command == "site":
            if len(sys.argv) >= 4:
                site_dir = SITES_DIR / sys.argv[3] / sys.argv[2]
                result = check_site_links(site_dir)
                if result:
                    print(f"\n站点: {sys.argv[2]}")
                    print(f"总链接: {result['total']}")
                    print(f"正常: {result['ok']}")
                    print(f"失效: {result['error']}")
                    if result['broken_links']:
                        print("\n失效链接:")
                        for link in result['broken_links']:
                            print(f"  - {link['name']}: {link['reason']}")
        else:
            print("用法: python link_checker.py [check|show|export|site]")
    else:
        # 默认检查所有站点
        check_all_sites()

if __name__ == "__main__":
    main()