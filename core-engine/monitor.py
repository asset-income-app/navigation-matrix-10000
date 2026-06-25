#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康监控引擎 - 检查站点健康状态、生成报告
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
SITES_DIR = ROOT_DIR / "02-sites"
DEPLOYED_DIR = ROOT_DIR / "05-deployed"
MONITOR_DIR = ROOT_DIR / "04-monitor"


def check_site_files(site_dir):
    """检查站点文件完整性"""
    required_files = ['index.html', 'style.css', 'script.js', 'config.json', 'sitemap.xml', 'robots.txt', '_headers']
    missing = []
    for f in required_files:
        if not (site_dir / f).exists():
            missing.append(f)
    return missing


def check_embedded_config(site_dir):
    """检查HTML是否内嵌了配置数据"""
    html_file = site_dir / "index.html"
    if not html_file.exists():
        return False
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    return '__SITE_CONFIG__' in content


def check_config_valid(site_dir):
    """检查config.json是否有效"""
    config_file = site_dir / "config.json"
    if not config_file.exists():
        return False, 0, 0
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        categories = config.get('categories', [])
        total_links = sum(len(cat.get('links', [])) for cat in categories)
        return True, len(categories), total_links
    except:
        return False, 0, 0


def scan_all_sites():
    """扫描所有站点"""
    print("扫描所有站点...")
    results = []
    site_types = ['cities', 'niches', 'hybrids']

    for site_type in site_types:
        type_dir = SITES_DIR / site_type
        if not type_dir.exists():
            continue

        for site_dir in sorted(type_dir.iterdir()):
            if not site_dir.is_dir() or site_dir.name.startswith('.'):
                continue

            site_name = site_dir.name
            missing_files = check_site_files(site_dir)
            has_embedded = check_embedded_config(site_dir)
            config_valid, cat_count, link_count = check_config_valid(site_dir)

            health = 'healthy'
            issues = []
            if missing_files:
                health = 'warning'
                issues.append(f"缺失文件: {', '.join(missing_files)}")
            if not has_embedded:
                health = 'warning'
                issues.append("未内嵌配置数据")
            if not config_valid:
                health = 'error'
                issues.append("config.json无效")
            if cat_count == 0:
                health = 'error'
                issues.append("无分类数据")
            if link_count == 0:
                health = 'error'
                issues.append("无链接数据")

            results.append({
                'name': site_name,
                'type': site_type,
                'health': health,
                'categories': cat_count,
                'links': link_count,
                'issues': issues
            })

    return results


def generate_report(results):
    """生成HTML健康报告"""
    os.makedirs(MONITOR_DIR, exist_ok=True)

    total = len(results)
    healthy = len([r for r in results if r['health'] == 'healthy'])
    warning = len([r for r in results if r['health'] == 'warning'])
    error = len([r for r in results if r['health'] == 'error'])
    total_links = sum(r['links'] for r in results)
    total_cats = sum(r['categories'] for r in results)
    health_score = round(healthy / total * 100, 1) if total > 0 else 0

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>健康报告 - 导航矩阵</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, sans-serif; background: #f0f4f8; color: #1e293b; padding: 24px; }}
        .header {{ background: #fff; border-radius: 16px; padding: 32px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
        .header h1 {{ font-size: 28px; margin-bottom: 8px; }}
        .header .date {{ color: #64748b; font-size: 14px; }}
        .score {{ font-size: 48px; font-weight: 700; margin: 16px 0; }}
        .score.healthy {{ color: #10b981; }}
        .score.warning {{ color: #f59e0b; }}
        .score.error {{ color: #ef4444; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }}
        .stat-card {{ background: #fff; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; }}
        .stat-num {{ font-size: 36px; font-weight: 700; }}
        .stat-label {{ color: #64748b; font-size: 14px; margin-top: 4px; }}
        .table-container {{ background: #fff; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); overflow-x: auto; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ text-align: left; padding: 12px; border-bottom: 2px solid #e2e8f0; color: #64748b; font-size: 14px; }}
        td {{ padding: 12px; border-bottom: 1px solid #f1f5f9; }}
        .badge {{ padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
        .badge.healthy {{ background: #d1fae5; color: #065f46; }}
        .badge.warning {{ background: #fef3c7; color: #92400e; }}
        .badge.error {{ background: #fee2e2; color: #991b1b; }}
        .issues {{ color: #ef4444; font-size: 13px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>导航矩阵健康报告</h1>
        <p class="date">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <div class="score {'healthy' if health_score >= 95 else 'warning' if health_score >= 80 else 'error'}">{health_score}分</div>
        <p>健康度评分</p>
    </div>

    <div class="stats">
        <div class="stat-card"><div class="stat-num">{total}</div><div class="stat-label">总站点数</div></div>
        <div class="stat-card"><div class="stat-num" style="color:#10b981">{healthy}</div><div class="stat-label">健康站点</div></div>
        <div class="stat-card"><div class="stat-num" style="color:#f59e0b">{warning}</div><div class="stat-label">警告站点</div></div>
        <div class="stat-card"><div class="stat-num" style="color:#ef4444">{error}</div><div class="stat-label">错误站点</div></div>
        <div class="stat-card"><div class="stat-num">{total_cats}</div><div class="stat-label">总分类数</div></div>
        <div class="stat-card"><div class="stat-num">{total_links}</div><div class="stat-label">总链接数</div></div>
    </div>

    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>站点名称</th>
                    <th>类型</th>
                    <th>状态</th>
                    <th>分类数</th>
                    <th>链接数</th>
                    <th>问题</th>
                </tr>
            </thead>
            <tbody>"""

    for r in results:
        issues_text = '<br>'.join(r['issues']) if r['issues'] else '-'
        type_label = {'cities': '城市站', 'niches': '行业站', 'hybrids': '组合站'}.get(r['type'], r['type'])
        health_labels = {'healthy': '健康', 'warning': '警告', 'error': '错误'}
        html += f"""
                <tr>
                    <td>{r['name']}</td>
                    <td>{type_label}</td>
                    <td><span class="badge {r['health']}">{health_labels.get(r['health'], r['health'])}</span></td>
                    <td>{r['categories']}</td>
                    <td>{r['links']}</td>
                    <td class="issues">{issues_text}</td>
                </tr>"""

    html += """
            </tbody>
        </table>
    </div>
</body>
</html>"""

    report_path = MONITOR_DIR / "health-report.html"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)

    # 同时保存JSON报告
    report_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total': total,
        'healthy': healthy,
        'warning': warning,
        'error': error,
        'healthScore': health_score,
        'totalLinks': total_links,
        'totalCategories': total_cats,
        'sites': results
    }
    with open(MONITOR_DIR / "health-report.json", 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    print(f"报告已生成: {report_path}")
    return health_score


def main():
    print("=" * 60)
    print("  健康监控引擎 v1.0")
    print("=" * 60)
    print()

    results = scan_all_sites()
    score = generate_report(results)

    print()
    print(f"  总站点: {len(results)}")
    print(f"  健康: {len([r for r in results if r['health']=='healthy'])}")
    print(f"  警告: {len([r for r in results if r['health']=='warning'])}")
    print(f"  错误: {len([r for r in results if r['health']=='error'])}")
    print(f"  健康度: {score}分")
    print()


if __name__ == '__main__':
    main()
