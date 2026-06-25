#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志管理系统 - log_manager.py
管理所有日志文件，提供查询和分析功能
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
LOGS_DIR = DATA_DIR / "logs"

def get_log_files(log_type="daily", date=None):
    """获取日志文件"""
    if date:
        month = date.strftime("%Y-%m")
        log_dir = LOGS_DIR / log_type / month
    else:
        log_dir = LOGS_DIR / log_type
    
    if not log_dir.exists():
        return []
    
    return sorted(log_dir.glob("*.json"))

def read_log(log_file):
    """读取日志文件"""
    if not log_file.exists():
        return None
    
    try:
        return json.loads(log_file.read_text())
    except:
        return None

def query_logs(log_type="daily", query=None, days=7):
    """查询日志"""
    print("\n" + "="*60)
    print(f"📋 日志查询 ({log_type})")
    print("="*60)
    
    results = []
    
    # 获取最近几天的日志
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        log_files = get_log_files(log_type, date)
        
        for log_file in log_files:
            log_data = read_log(log_file)
            if log_data:
                # 搜索匹配
                if query:
                    if isinstance(log_data, list):
                        matches = [item for item in log_data if query in str(item)]
                        if matches:
                            results.extend(matches)
                    elif isinstance(log_data, dict):
                        if query in str(log_data):
                            results.append(log_data)
                else:
                    results.append(log_data)
    
    print(f"找到日志: {len(results)} 条")
    
    return results

def show_log_summary(log_type="daily"):
    """显示日志摘要"""
    print("\n" + "="*60)
    print(f"📊 日志摘要 ({log_type})")
    print("="*60)
    
    # 统计各类型日志
    log_types_dir = LOGS_DIR / log_type
    if not log_types_dir.exists():
        print("没有日志")
        return
    
    total_logs = 0
    total_size = 0
    
    for month_dir in sorted(log_types_dir.iterdir()):
        if month_dir.is_dir():
            logs = list(month_dir.glob("*.json"))
            count = len(logs)
            size = sum(f.stat().st_size for f in logs) / 1024
            
            total_logs += count
            total_size += size
            
            print(f"\n{month_dir.name}:")
            print(f"  数量: {count} 个")
            print(f"  大小: {size:.1f} KB")
            
            # 显示最近日志
            for log in sorted(logs, reverse=True)[:3]:
                log_data = read_log(log)
                if log_data:
                    timestamp = log_data.get('timestamp', '未知')
                    print(f"  - {log.name} @ {timestamp}")
    
    print(f"\n总计:")
    print(f"  数量: {total_logs} 个")
    print(f"  大小: {total_size:.1f} KB")

def analyze_logs(log_type="daily", days=30):
    """分析日志"""
    print("\n" + "="*60)
    print(f"📈 日志分析 ({log_type}, 最近{days}天)")
    print("="*60)
    
    # 收集日志数据
    all_logs = []
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        log_files = get_log_files(log_type, date)
        for log_file in log_files:
            log_data = read_log(log_file)
            if log_data:
                all_logs.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "file": log_file.name,
                    "data": log_data
                })
    
    # 分析
    stats = {
        "total_logs": len(all_logs),
        "by_date": {},
        "by_type": {}
    }
    
    for log in all_logs:
        date = log["date"]
        stats["by_date"][date] = stats["by_date"].get(date, 0) + 1
        
        # 按日志类型统计
        log_name = log["file"]
        if "health" in log_name:
            stats["by_type"]["健康检查"] = stats["by_type"].get("健康检查", 0) + 1
        elif "links" in log_name:
            stats["by_type"]["链接检查"] = stats["by_type"].get("链接检查", 0) + 1
        elif "repair" in log_name:
            stats["by_type"]["自动修复"] = stats["by_type"].get("自动修复", 0) + 1
        elif "backup" in log_name:
            stats["by_type"]["自动备份"] = stats["by_type"].get("自动备份", 0) + 1
        elif "tasks" in log_name:
            stats["by_type"]["任务执行"] = stats["by_type"].get("任务执行", 0) + 1
    
    print(f"\n总日志数: {stats['total_logs']}")
    
    print("\n按类型统计:")
    for type_name, count in stats["by_type"].items():
        print(f"  {type_name}: {count} 次")
    
    print("\n按日期统计:")
    for date, count in sorted(stats["by_date"].items()):
        print(f"  {date}: {count} 个")

def cleanup_old_logs(keep_days=90):
    """清理旧日志"""
    print("🧹 清理旧日志...")
    
    cutoff = datetime.now() - timedelta(days=keep_days)
    
    deleted = 0
    
    for log_type in ['daily', 'weekly', 'monthly']:
        log_dir = LOGS_DIR / log_type
        if not log_dir.exists():
            continue
        
        for month_dir in log_dir.iterdir():
            if month_dir.is_dir():
                for log_file in month_dir.glob("*.json"):
                    # 从文件名提取日期
                    date_str = log_file.stem.split("_")[1] if "_" in log_file.stem else None
                    if date_str:
                        try:
                            log_date = datetime.strptime(date_str, "%Y-%m-%d")
                            if log_date < cutoff:
                                log_file.unlink()
                                deleted += 1
                                print(f"  🗑️ {log_file.name}")
                        except:
                            pass
    
    print(f"✅ 已删除 {deleted} 个旧日志")

def export_logs(output_dir, log_type="daily", days=30):
    """导出日志"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    exported = 0
    
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        log_files = get_log_files(log_type, date)
        
        for log_file in log_files:
            target_file = output_path / log_file.name
            shutil.copy(log_file, target_file)
            exported += 1
    
    print(f"✅ 已导出 {exported} 个日志到 {output_path}")

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "query":
            query = sys.argv[2] if len(sys.argv) > 2 else None
            days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
            query_logs("daily", query, days)
        elif command == "summary":
            log_type = sys.argv[2] if len(sys.argv) > 2 else "daily"
            show_log_summary(log_type)
        elif command == "analyze":
            log_type = sys.argv[2] if len(sys.argv) > 2 else "daily"
            days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
            analyze_logs(log_type, days)
        elif command == "cleanup":
            keep_days = int(sys.argv[2]) if len(sys.argv) > 2 else 90
            cleanup_old_logs(keep_days)
        elif command == "export":
            if len(sys.argv) >= 3:
                export_logs(sys.argv[2])
            else:
                export_logs("exported_logs")
        else:
            print("用法: python log_manager.py [query|summary|analyze|cleanup|export]")
    else:
        # 默认显示摘要
        show_log_summary("daily")

if __name__ == "__main__":
    main()