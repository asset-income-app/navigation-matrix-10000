#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
收入追踪引擎 - 记录和统计收入数据
"""

import json
import os
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
MONITOR_DIR = ROOT_DIR / "04-monitor"
DATA_DIR = ROOT_DIR / "data"


def record_revenue(record_type, site, amount, **kwargs):
    """记录一笔收入"""
    today = datetime.now().strftime('%Y-%m-%d')
    revenue_file = DATA_DIR / "revenue.json"

    # 加载现有数据
    if revenue_file.exists():
        with open(revenue_file, 'r', encoding='utf-8') as f:
            revenue = json.load(f)
    else:
        revenue = {'records': []}

    # 添加记录
    record = {
        'id': f"R{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'date': today,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'type': record_type,
        'site': site,
        'amount': amount,
        **kwargs
    }
    revenue['records'].append(record)

    # 保存
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(revenue_file, 'w', encoding='utf-8') as f:
        json.dump(revenue, f, ensure_ascii=False, indent=2)

    print(f"  [OK] 记录收入: {record_type} | {site} | ¥{amount}")
    return record


def generate_revenue_report():
    """生成收入报告"""
    os.makedirs(MONITOR_DIR, exist_ok=True)

    revenue_file = DATA_DIR / "revenue.json"
    if revenue_file.exists():
        with open(revenue_file, 'r', encoding='utf-8') as f:
            revenue = json.load(f)
    else:
        revenue = {'records': []}

    records = revenue.get('records', [])
    today = datetime.now().strftime('%Y-%m-%d')
    this_month = today[:7]

    daily_total = sum(r['amount'] for r in records if r['date'] == today)
    monthly_total = sum(r['amount'] for r in records if r['date'].startswith(this_month))
    total = sum(r['amount'] for r in records)

    # 按类型统计
    by_type = {}
    for r in records:
        t = r['type']
        by_type[t] = by_type.get(t, 0) + r['amount']

    # 按站点统计
    by_site = {}
    for r in records:
        s = r['site']
        by_site[s] = by_site.get(s, 0) + r['amount']

    type_labels = {
        'ad': '广告收入',
        'listing': '商家收录',
        'pin': '分类置顶',
        'affiliate': '联盟返佣',
        'banner': '广告位'
    }

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>收入仪表盘 - 导航矩阵</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, sans-serif; background: #f0f4f8; color: #1e293b; padding: 24px; }}
        .header {{ background: linear-gradient(135deg, #059669, #10b981); color: #fff; border-radius: 16px; padding: 32px; margin-bottom: 24px; }}
        .header h1 {{ font-size: 28px; margin-bottom: 8px; }}
        .header .date {{ opacity: 0.9; font-size: 14px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }}
        .stat-card {{ background: #fff; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; }}
        .stat-num {{ font-size: 36px; font-weight: 700; color: #059669; }}
        .stat-label {{ color: #64748b; font-size: 14px; margin-top: 4px; }}
        .section {{ background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
        .section h2 {{ font-size: 20px; margin-bottom: 16px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ text-align: left; padding: 12px; border-bottom: 2px solid #e2e8f0; color: #64748b; font-size: 14px; }}
        td {{ padding: 12px; border-bottom: 1px solid #f1f5f9; }}
        .empty {{ text-align: center; padding: 48px; color: #94a3b8; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>收入仪表盘</h1>
        <p class="date">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <div class="stats">
        <div class="stat-card"><div class="stat-num">¥{daily_total}</div><div class="stat-label">今日收入</div></div>
        <div class="stat-card"><div class="stat-num">¥{monthly_total}</div><div class="stat-label">本月收入</div></div>
        <div class="stat-card"><div class="stat-num">¥{total}</div><div class="stat-label">累计收入</div></div>
        <div class="stat-card"><div class="stat-num">{len(records)}</div><div class="stat-label">交易笔数</div></div>
    </div>

    <div class="section">
        <h2>按收入类型</h2>"""

    if by_type:
        html += """
        <table>
            <thead><tr><th>类型</th><th>金额</th><th>占比</th></tr></thead>
            <tbody>"""
        for t, amount in sorted(by_type.items(), key=lambda x: -x[1]):
            pct = round(amount / total * 100, 1) if total > 0 else 0
            label = type_labels.get(t, t)
            html += f"<tr><td>{label}</td><td>¥{amount}</td><td>{pct}%</td></tr>"
        html += "</tbody></table>"
    else:
        html += '<div class="empty">暂无收入数据</div>'

    html += """
    </div>

    <div class="section">
        <h2>按站点统计</h2>"""

    if by_site:
        html += """
        <table>
            <thead><tr><th>站点</th><th>金额</th></tr></thead>
            <tbody>"""
        for s, amount in sorted(by_site.items(), key=lambda x: -x[1]):
            html += f"<tr><td>{s}</td><td>¥{amount}</td></tr>"
        html += "</tbody></table>"
    else:
        html += '<div class="empty">暂无站点数据</div>'

    html += """
    </div>

    <div class="section">
        <h2>最近交易</h2>"""

    if records:
        html += """
        <table>
            <thead><tr><th>日期</th><th>类型</th><th>站点</th><th>金额</th><th>备注</th></tr></thead>
            <tbody>"""
        for r in records[-20:]:
            label = type_labels.get(r['type'], r['type'])
            notes = r.get('notes', r.get('merchant', ''))
            html += f"<tr><td>{r['date']}</td><td>{label}</td><td>{r['site']}</td><td>¥{r['amount']}</td><td>{notes}</td></tr>"
        html += "</tbody></table>"
    else:
        html += '<div class="empty">暂无交易记录</div>'

    html += """
    </div>
</body>
</html>"""

    report_path = MONITOR_DIR / "revenue-dashboard.html"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"收入报告已生成: {report_path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='收入追踪引擎')
    parser.add_argument('--record', action='store_true', help='记录收入')
    parser.add_argument('--type', type=str, help='收入类型')
    parser.add_argument('--site', type=str, help='站点名称')
    parser.add_argument('--amount', type=int, help='金额')
    parser.add_argument('--report', action='store_true', help='生成报告')
    parser.add_argument('--merchant', type=str, default='', help='商家名称')
    args = parser.parse_args()

    print("=" * 60)
    print("  收入追踪引擎 v1.0")
    print("=" * 60)

    if args.record and args.type and args.site and args.amount:
        record_revenue(args.type, args.site, args.amount, merchant=args.merchant)

    generate_revenue_report()


if __name__ == '__main__':
    main()
