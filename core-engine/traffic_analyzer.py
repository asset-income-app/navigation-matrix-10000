#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
流量分析系统 - traffic_analyzer.py
分析站点流量数据，优化流量策略
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
import random

ROOT_DIR = Path(__file__).parent.parent
SITES_DIR = ROOT_DIR / "02-sites"
DATA_DIR = ROOT_DIR / "data"

def generate_mock_traffic_data():
    """生成模拟流量数据（用于测试）"""
    print("\n" + "="*60)
    print("📊 流量分析系统 - 生成模拟数据")
    print("="*60)
    
    traffic_data = {
        "timestamp": datetime.now().isoformat(),
        "sites": []
    }
    
    for site_type in ['cities', 'niches', 'hybrids']:
        type_dir = SITES_DIR / site_type
        if not type_dir.exists():
            continue
        
        sites = [d for d in type_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        for site_dir in sites:
            # 模拟流量数据
            daily_visitors = random.randint(50, 500)
            daily_page_views = daily_visitors * random.randint(2, 5)
            bounce_rate = random.uniform(0.3, 0.7)
            avg_session_duration = random.randint(30, 300)
            
            traffic_data["sites"].append({
                "site_name": site_dir.name,
                "site_type": site_type,
                "daily_visitors": daily_visitors,
                "daily_page_views": daily_page_views,
                "bounce_rate": round(bounce_rate, 2),
                "avg_session_duration": avg_session_duration,
                "traffic_sources": {
                    "direct": random.randint(10, 30),
                    "organic_search": random.randint(30, 60),
                    "social_media": random.randint(5, 20),
                    "referral": random.randint(5, 15)
                },
                "top_pages": [
                    {"path": "/", "views": random.randint(20, 100)},
                    {"path": "/#services", "views": random.randint(10, 50)},
                    {"path": "/#education", "views": random.randint(10, 50)}
                ]
            })
    
    # 保存流量数据
    traffic_file = DATA_DIR / "logs" / "traffic_data.json"
    traffic_file.parent.mkdir(parents=True, exist_ok=True)
    traffic_file.write_text(json.dumps(traffic_data, indent=2))
    
    print(f"✅ 已生成模拟流量数据")
    print(f"  站点数: {len(traffic_data['sites'])}")
    print(f"  文件: {traffic_file}")
    print("="*60)
    
    return traffic_data

def analyze_traffic_data():
    """分析流量数据"""
    print("\n" + "="*60)
    print("📈 流量数据分析")
    print("="*60)
    
    traffic_file = DATA_DIR / "logs" / "traffic_data.json"
    
    if not traffic_file.exists():
        print("⚠️  流量数据不存在，生成模拟数据...")
        traffic_data = generate_mock_traffic_data()
    else:
        traffic_data = json.loads(traffic_file.read_text())
    
    # 计算统计数据
    total_visitors = sum(s['daily_visitors'] for s in traffic_data['sites'])
    total_page_views = sum(s['daily_page_views'] for s in traffic_data['sites'])
    avg_bounce_rate = sum(s['bounce_rate'] for s in traffic_data['sites']) / len(traffic_data['sites'])
    avg_session_duration = sum(s['avg_session_duration'] for s in traffic_data['sites']) / len(traffic_data['sites'])
    
    # 按站点类型统计
    type_stats = {}
    for site_type in ['cities', 'niches', 'hybrids']:
        type_sites = [s for s in traffic_data['sites'] if s['site_type'] == site_type]
        if type_sites:
            type_stats[site_type] = {
                "count": len(type_sites),
                "total_visitors": sum(s['daily_visitors'] for s in type_sites),
                "avg_visitors": sum(s['daily_visitors'] for s in type_sites) / len(type_sites),
                "total_page_views": sum(s['daily_page_views'] for s in type_sites)
            }
    
    # 找出高流量站点
    high_traffic_sites = sorted(traffic_data['sites'], key=lambda x: x['daily_visitors'], reverse=True)[:10]
    
    # 找出低流量站点
    low_traffic_sites = sorted(traffic_data['sites'], key=lambda x: x['daily_visitors'])[:10]
    
    # 生成分析报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_sites": len(traffic_data['sites']),
            "total_visitors": total_visitors,
            "total_page_views": total_page_views,
            "avg_bounce_rate": round(avg_bounce_rate, 2),
            "avg_session_duration": round(avg_session_duration, 2)
        },
        "type_stats": type_stats,
        "high_traffic_sites": [{"site_name": s['site_name'], "visitors": s['daily_visitors']} for s in high_traffic_sites],
        "low_traffic_sites": [{"site_name": s['site_name'], "visitors": s['daily_visitors']} for s in low_traffic_sites],
        "recommendations": []
    }
    
    # 生成优化建议
    if avg_bounce_rate > 0.5:
        report["recommendations"].append("跳出率偏高，建议优化首页内容和导航结构")
    
    if avg_session_duration < 60:
        report["recommendations"].append("用户停留时间短，建议增加互动内容和引导")
    
    if total_visitors < 10000:
        report["recommendations"].append("总流量偏低，建议加强SEO优化和社交媒体推广")
    
    # 保存分析报告
    report_file = DATA_DIR / "logs" / "traffic_analysis_report.json"
    report_file.write_text(json.dumps(report, indent=2))
    
    print("\n📊 流量统计:")
    print(f"  总站点数: {len(traffic_data['sites'])}")
    print(f"  总访问量: {total_visitors} 人/天")
    print(f"  总浏览量: {total_page_views} 页/天")
    print(f"  平均跳出率: {round(avg_bounce_rate * 100, 2)}%")
    print(f"  平均停留时间: {round(avg_session_duration, 2)}秒")
    
    print("\n📈 类型统计:")
    for site_type, stats in type_stats.items():
        print(f"  {site_type}: {stats['count']}站, {stats['total_visitors']}人/天, 平均{round(stats['avg_visitors'], 2)}人/站")
    
    print("\n🔥 高流量站点 (前10):")
    for site in high_traffic_sites:
        print(f"  {site['site_name']}: {site['daily_visitors']} 人/天")
    
    print("\n⚠️  低流量站点 (前10):")
    for site in low_traffic_sites:
        print(f"  {site['site_name']}: {site['daily_visitors']} 人/天")
    
    print("\n💡 优化建议:")
    for rec in report["recommendations"]:
        print(f"  - {rec}")
    
    print(f"\n报告文件: {report_file}")
    print("="*60)
    
    return report

def generate_traffic_forecast():
    """生成流量预测"""
    print("\n" + "="*60)
    print("🔮 流量预测")
    print("="*60)
    
    traffic_file = DATA_DIR / "logs" / "traffic_data.json"
    
    if not traffic_file.exists():
        print("⚠️  流量数据不存在，请先运行流量分析")
        return
    
    traffic_data = json.loads(traffic_file.read_text())
    
    # 基于当前数据预测未来7天流量
    current_visitors = sum(s['daily_visitors'] for s in traffic_data['sites'])
    
    forecast = {
        "timestamp": datetime.now().isoformat(),
        "current_daily_visitors": current_visitors,
        "predictions": []
    }
    
    # 简单预测模型（假设每天增长5%）
    for i in range(1, 8):
        predicted_visitors = current_visitors * (1 + 0.05 * i)
        forecast["predictions"].append({
            "day": i,
            "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
            "predicted_visitors": round(predicted_visitors),
            "growth_rate": f"{5*i}%"
        })
    
    # 保存预测数据
    forecast_file = DATA_DIR / "logs" / "traffic_forecast.json"
    forecast_file.write_text(json.dumps(forecast, indent=2))
    
    print(f"当前日访问量: {current_visitors} 人")
    print("\n未来7天预测:")
    for pred in forecast["predictions"]:
        print(f"  第{pred['day']}天 ({pred['date']}): {pred['predicted_visitors']} 人 (增长{pred['growth_rate']})")
    
    print(f"\n预测文件: {forecast_file}")
    print("="*60)

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "analyze":
            analyze_traffic_data()
        elif command == "forecast":
            generate_traffic_forecast()
        elif command == "mock":
            generate_mock_traffic_data()
        else:
            print("用法: python traffic_analyzer.py [analyze|forecast|mock]")
    else:
        # 默认执行分析
        analyze_traffic_data()
        generate_traffic_forecast()

if __name__ == "__main__":
    main()