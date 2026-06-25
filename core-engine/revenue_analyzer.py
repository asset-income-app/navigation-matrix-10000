#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
收入分析系统 - revenue_analyzer.py
分析站点收入数据，优化变现策略
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
import random

ROOT_DIR = Path(__file__).parent.parent
SITES_DIR = ROOT_DIR / "02-sites"
DATA_DIR = ROOT_DIR / "data"

def generate_mock_revenue_data():
    """生成模拟收入数据（用于测试）"""
    print("\n" + "="*60)
    print("💰 收入分析系统 - 生成模拟数据")
    print("="*60)
    
    revenue_data = {
        "timestamp": datetime.now().isoformat(),
        "sites": []
    }
    
    for site_type in ['cities', 'niches', 'hybrids']:
        type_dir = SITES_DIR / site_type
        if not type_dir.exists():
            continue
        
        sites = [d for d in type_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        for site_dir in sites:
            # 模拟收入数据
            daily_revenue = random.uniform(0.5, 10.0)
            ad_revenue = daily_revenue * random.uniform(0.6, 0.8)
            affiliate_revenue = daily_revenue * random.uniform(0.1, 0.3)
            other_revenue = daily_revenue - ad_revenue - affiliate_revenue
            
            revenue_data["sites"].append({
                "site_name": site_dir.name,
                "site_type": site_type,
                "daily_revenue": round(daily_revenue, 2),
                "monthly_revenue": round(daily_revenue * 30, 2),
                "revenue_sources": {
                    "ad_revenue": round(ad_revenue, 2),
                    "affiliate_revenue": round(affiliate_revenue, 2),
                    "other_revenue": round(other_revenue, 2)
                },
                "conversion_rate": round(random.uniform(0.01, 0.05), 4),
                "avg_order_value": round(random.uniform(10, 100), 2)
            })
    
    # 保存收入数据
    revenue_file = DATA_DIR / "logs" / "revenue_data.json"
    revenue_file.parent.mkdir(parents=True, exist_ok=True)
    revenue_file.write_text(json.dumps(revenue_data, indent=2))
    
    print(f"✅ 已生成模拟收入数据")
    print(f"  站点数: {len(revenue_data['sites'])}")
    print(f"  文件: {revenue_file}")
    print("="*60)
    
    return revenue_data

def analyze_revenue_data():
    """分析收入数据"""
    print("\n" + "="*60)
    print("📊 收入数据分析")
    print("="*60)
    
    revenue_file = DATA_DIR / "logs" / "revenue_data.json"
    
    if not revenue_file.exists():
        print("⚠️  收入数据不存在，生成模拟数据...")
        revenue_data = generate_mock_revenue_data()
    else:
        revenue_data = json.loads(revenue_file.read_text())
    
    # 计算统计数据
    total_daily_revenue = sum(s['daily_revenue'] for s in revenue_data['sites'])
    total_monthly_revenue = sum(s['monthly_revenue'] for s in revenue_data['sites'])
    avg_daily_revenue = total_daily_revenue / len(revenue_data['sites'])
    avg_conversion_rate = sum(s['conversion_rate'] for s in revenue_data['sites']) / len(revenue_data['sites'])
    
    # 按站点类型统计
    type_stats = {}
    for site_type in ['cities', 'niches', 'hybrids']:
        type_sites = [s for s in revenue_data['sites'] if s['site_type'] == site_type]
        if type_sites:
            type_stats[site_type] = {
                "count": len(type_sites),
                "total_daily_revenue": sum(s['daily_revenue'] for s in type_sites),
                "avg_daily_revenue": sum(s['daily_revenue'] for s in type_sites) / len(type_sites),
                "total_monthly_revenue": sum(s['monthly_revenue'] for s in type_sites)
            }
    
    # 按收入来源统计
    source_stats = {
        "ad_revenue": sum(s['revenue_sources']['ad_revenue'] for s in revenue_data['sites']),
        "affiliate_revenue": sum(s['revenue_sources']['affiliate_revenue'] for s in revenue_data['sites']),
        "other_revenue": sum(s['revenue_sources']['other_revenue'] for s in revenue_data['sites'])
    }
    
    # 找出高收入站点
    high_revenue_sites = sorted(revenue_data['sites'], key=lambda x: x['daily_revenue'], reverse=True)[:10]
    
    # 找出低收入站点
    low_revenue_sites = sorted(revenue_data['sites'], key=lambda x: x['daily_revenue'])[:10]
    
    # 生成分析报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_sites": len(revenue_data['sites']),
            "total_daily_revenue": round(total_daily_revenue, 2),
            "total_monthly_revenue": round(total_monthly_revenue, 2),
            "avg_daily_revenue": round(avg_daily_revenue, 2),
            "avg_conversion_rate": round(avg_conversion_rate, 4)
        },
        "type_stats": type_stats,
        "source_stats": source_stats,
        "high_revenue_sites": [{"site_name": s['site_name'], "daily_revenue": s['daily_revenue']} for s in high_revenue_sites],
        "low_revenue_sites": [{"site_name": s['site_name'], "daily_revenue": s['daily_revenue']} for s in low_revenue_sites],
        "recommendations": []
    }
    
    # 生成优化建议
    if avg_daily_revenue < 2:
        report["recommendations"].append("平均收入偏低，建议增加广告位和优化广告展示")
    
    if avg_conversion_rate < 0.02:
        report["recommendations"].append("转化率偏低，建议优化用户体验和引导转化")
    
    if source_stats['affiliate_revenue'] < source_stats['ad_revenue'] * 0.2:
        report["recommendations"].append("联盟收入占比低，建议增加联盟推广链接")
    
    # 保存分析报告
    report_file = DATA_DIR / "logs" / "revenue_analysis_report.json"
    report_file.write_text(json.dumps(report, indent=2))
    
    print("\n💰 收入统计:")
    print(f"  总站点数: {len(revenue_data['sites'])}")
    print(f"  总日收入: ¥{round(total_daily_revenue, 2)}")
    print(f"  总月收入: ¥{round(total_monthly_revenue, 2)}")
    print(f"  平均日收入: ¥{round(avg_daily_revenue, 2)}/站")
    print(f"  平均转化率: {round(avg_conversion_rate * 100, 2)}%")
    
    print("\n📈 类型统计:")
    for site_type, stats in type_stats.items():
        print(f"  {site_type}: {stats['count']}站, ¥{round(stats['total_daily_revenue'], 2)}/天, 平均¥{round(stats['avg_daily_revenue'], 2)}/站")
    
    print("\n📊 收入来源:")
    print(f"  广告收入: ¥{round(source_stats['ad_revenue'], 2)}/天 ({round(source_stats['ad_revenue']/total_daily_revenue*100, 2)}%)")
    print(f"  联盟收入: ¥{round(source_stats['affiliate_revenue'], 2)}/天 ({round(source_stats['affiliate_revenue']/total_daily_revenue*100, 2)}%)")
    print(f"  其他收入: ¥{round(source_stats['other_revenue'], 2)}/天 ({round(source_stats['other_revenue']/total_daily_revenue*100, 2)}%)")
    
    print("\n🔥 高收入站点 (前10):")
    for site in high_revenue_sites:
        print(f"  {site['site_name']}: ¥{site['daily_revenue']}/天")
    
    print("\n⚠️  低收入站点 (前10):")
    for site in low_revenue_sites:
        print(f"  {site['site_name']}: ¥{site['daily_revenue']}/天")
    
    print("\n💡 优化建议:")
    for rec in report["recommendations"]:
        print(f"  - {rec}")
    
    print(f"\n报告文件: {report_file}")
    print("="*60)
    
    return report

def generate_revenue_forecast():
    """生成收入预测"""
    print("\n" + "="*60)
    print("🔮 收入预测")
    print("="*60)
    
    revenue_file = DATA_DIR / "logs" / "revenue_data.json"
    
    if not revenue_file.exists():
        print("⚠️  收入数据不存在，请先运行收入分析")
        return
    
    revenue_data = json.loads(revenue_file.read_text())
    
    # 基于当前数据预测未来30天收入
    current_daily_revenue = sum(s['daily_revenue'] for s in revenue_data['sites'])
    
    forecast = {
        "timestamp": datetime.now().isoformat(),
        "current_daily_revenue": round(current_daily_revenue, 2),
        "predictions": []
    }
    
    # 简单预测模型（假设每天增长3%）
    for i in range(1, 31):
        predicted_revenue = current_daily_revenue * (1 + 0.03 * i)
        forecast["predictions"].append({
            "day": i,
            "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
            "predicted_daily_revenue": round(predicted_revenue, 2),
            "predicted_monthly_revenue": round(predicted_revenue * 30, 2),
            "growth_rate": f"{3*i}%"
        })
    
    # 保存预测数据
    forecast_file = DATA_DIR / "logs" / "revenue_forecast.json"
    forecast_file.write_text(json.dumps(forecast, indent=2))
    
    print(f"当前日收入: ¥{round(current_daily_revenue, 2)}")
    print(f"当前月收入: ¥{round(current_daily_revenue * 30, 2)}")
    print("\n未来30天预测:")
    for pred in forecast["predictions"][::7]:  # 每周显示一次
        print(f"  第{pred['day']}天 ({pred['date']}): ¥{pred['predicted_daily_revenue']}/天 (增长{pred['growth_rate']})")
    
    print(f"\n预测文件: {forecast_file}")
    print("="*60)

def optimize_revenue_strategy():
    """优化收入策略"""
    print("\n" + "="*60)
    print("🎯 收入策略优化")
    print("="*60)
    
    revenue_file = DATA_DIR / "logs" / "revenue_data.json"
    
    if not revenue_file.exists():
        print("⚠️  收入数据不存在，请先运行收入分析")
        return
    
    revenue_data = json.loads(revenue_file.read_text())
    
    # 分析收入结构
    source_stats = {
        "ad_revenue": sum(s['revenue_sources']['ad_revenue'] for s in revenue_data['sites']),
        "affiliate_revenue": sum(s['revenue_sources']['affiliate_revenue'] for s in revenue_data['sites']),
        "other_revenue": sum(s['revenue_sources']['other_revenue'] for s in revenue_data['sites'])
    }
    
    total_revenue = sum(source_stats.values())
    
    # 生成优化策略
    strategies = []
    
    # 1. 广告优化策略
    if source_stats['ad_revenue'] < total_revenue * 0.6:
        strategies.append({
            "name": "增加广告位",
            "description": "在首页和分类页增加更多广告位，提升广告收入占比",
            "expected_increase": "20-30%"
        })
    
    # 2. 联盟优化策略
    if source_stats['affiliate_revenue'] < total_revenue * 0.15:
        strategies.append({
            "name": "增加联盟推广",
            "description": "增加淘宝、京东、拼多多等联盟推广链接",
            "expected_increase": "15-25%"
        })
    
    # 3. 转化率优化策略
    avg_conversion = sum(s['conversion_rate'] for s in revenue_data['sites']) / len(revenue_data['sites'])
    if avg_conversion < 0.03:
        strategies.append({
            "name": "优化转化路径",
            "description": "优化用户引导流程，增加转化按钮和引导文案",
            "expected_increase": "10-20%"
        })
    
    # 保存策略
    strategy_file = DATA_DIR / "logs" / "revenue_strategies.json"
    strategy_file.write_text(json.dumps(strategies, indent=2))
    
    print("💡 收入优化策略:")
    for i, strategy in enumerate(strategies, 1):
        print(f"\n{i}. {strategy['name']}")
        print(f"   描述: {strategy['description']}")
        print(f"   预期增长: {strategy['expected_increase']}")
    
    print(f"\n策略文件: {strategy_file}")
    print("="*60)

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "analyze":
            analyze_revenue_data()
        elif command == "forecast":
            generate_revenue_forecast()
        elif command == "optimize":
            optimize_revenue_strategy()
        elif command == "mock":
            generate_mock_revenue_data()
        else:
            print("用法: python revenue_analyzer.py [analyze|forecast|optimize|mock]")
    else:
        # 默认执行分析
        analyze_revenue_data()
        generate_revenue_forecast()
        optimize_revenue_strategy()

if __name__ == "__main__":
    main()