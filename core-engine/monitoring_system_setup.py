"""
实时监控系统脚本
创建实时监控和报警系统
"""

import json
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(r"E:\50\navigation-matrix-unified")
DATA_DIR = ROOT_DIR / "data"
MONITOR_DIR = ROOT_DIR / "04-monitor"

def create_real_time_monitor():
    """创建实时监控系统配置"""
    print("创建实时监控系统...")
    
    monitor_config = {
        "real_time_monitor": {
            "enabled": True,
            "version": "1.0",
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            
            "health_monitor": {
                "check_interval": 300,  # 5分钟
                "alert_threshold": {
                    "health_score_below": 90,
                    "error_rate_above": 5,
                    "link_failure_above": 10
                },
                "notification": {
                    "enabled": True,
                    "channels": ["console", "file"],
                    "priority": "high"
                }
            },
            
            "performance_monitor": {
                "check_interval": 600,  # 10分钟
                "metrics": [
                    "response_time",
                    "load_time",
                    "throughput",
                    "error_rate"
                ],
                "thresholds": {
                    "response_time_above": 2.0,  # 2秒
                    "load_time_above": 5.0,      # 5秒
                    "error_rate_above": 1.0      # 1%
                }
            },
            
            "traffic_monitor": {
                "check_interval": 1800,  # 30分钟
                "metrics": [
                    "daily_traffic",
                    "hourly_traffic",
                    "traffic_source",
                    "conversion_rate"
                ],
                "alert_rules": {
                    "traffic_drop_above": 20,    # 20%下降
                    "traffic_spike_above": 200   # 200%激增
                }
            },
            
            "revenue_monitor": {
                "check_interval": 3600,  # 1小时
                "metrics": [
                    "daily_revenue",
                    "hourly_revenue",
                    "revenue_source",
                    "conversion_rate"
                ],
                "alert_rules": {
                    "revenue_drop_above": 15,    # 15%下降
                    "revenue_spike_above": 150   # 150%激增
                }
            },
            
            "system_monitor": {
                "check_interval": 600,  # 10分钟
                "metrics": [
                    "cpu_usage",
                    "memory_usage",
                    "disk_usage",
                    "network_status"
                ],
                "thresholds": {
                    "cpu_usage_above": 80,      # 80%
                    "memory_usage_above": 85,   # 85%
                    "disk_usage_above": 90      # 90%
                }
            }
        },
        
        "alert_system": {
            "enabled": True,
            "channels": {
                "console": {
                    "enabled": True,
                    "min_priority": "low"
                },
                "file": {
                    "enabled": True,
                    "log_file": str(MONITOR_DIR / "alerts.log"),
                    "min_priority": "medium"
                },
                "email": {
                    "enabled": False,
                    "recipients": [],
                    "min_priority": "high"
                }
            },
            
            "alert_levels": {
                "low": {
                    "description": "轻微问题",
                    "color": "yellow",
                    "action": "记录日志"
                },
                "medium": {
                    "description": "中度问题",
                    "color": "orange",
                    "action": "发送通知"
                },
                "high": {
                    "description": "严重问题",
                    "color": "red",
                    "action": "立即响应"
                },
                "critical": {
                    "description": "紧急问题",
                    "color": "black",
                    "action": "紧急处理"
                }
            },
            
            "alert_rules": [
                {
                    "rule_id": "health_score_low",
                    "condition": "health_score < 90",
                    "level": "medium",
                    "message": "站点健康度低于90分"
                },
                {
                    "rule_id": "traffic_drop",
                    "condition": "traffic_drop > 20%",
                    "level": "high",
                    "message": "流量下降超过20%"
                },
                {
                    "rule_id": "revenue_drop",
                    "condition": "revenue_drop > 15%",
                    "level": "high",
                    "message": "收入下降超过15%"
                },
                {
                    "rule_id": "system_resource_high",
                    "condition": "cpu_usage > 80%",
                    "level": "medium",
                    "message": "系统资源使用过高"
                }
            ]
        },
        
        "monitoring_dashboard": {
            "enabled": True,
            "refresh_interval": 60,  # 60秒
            "widgets": [
                {
                    "name": "站点健康概览",
                    "type": "health_score",
                    "position": "top-left",
                    "size": "large"
                },
                {
                    "name": "实时流量监控",
                    "type": "traffic_chart",
                    "position": "top-right",
                    "size": "large"
                },
                {
                    "name": "收入趋势图",
                    "type": "revenue_chart",
                    "position": "middle-left",
                    "size": "medium"
                },
                {
                    "name": "系统性能监控",
                    "type": "performance_chart",
                    "position": "middle-right",
                    "size": "medium"
                },
                {
                    "name": "报警通知列表",
                    "type": "alert_list",
                    "position": "bottom",
                    "size": "full"
                }
            ]
        },
        
        "statistics": {
            "total_checks": 0,
            "alerts_triggered": 0,
            "issues_resolved": 0,
            "uptime": "100%"
        }
    }
    
    # 保存监控配置
    config_file = DATA_DIR / "monitoring_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(monitor_config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 监控配置已创建：{config_file}")
    return monitor_config

def create_alert_handler():
    """创建报警处理脚本"""
    print("创建报警处理脚本...")
    
    alert_script = MONITOR_DIR / "alert_handler.py"
    
    content = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
报警处理脚本
处理各种监控报警
"""

import json
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(r"E:\\50\\navigation-matrix-unified")
DATA_DIR = ROOT_DIR / "data"
MONITOR_DIR = ROOT_DIR / "04-monitor"

def load_monitoring_config():
    """加载监控配置"""
    config_file = DATA_DIR / "monitoring_config.json"
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def handle_alert(alert_type, alert_level, message):
    """处理报警"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    alert_record = {
        "timestamp": timestamp,
        "type": alert_type,
        "level": alert_level,
        "message": message,
        "status": "triggered"
    }
    
    # 记录报警日志
    log_file = MONITOR_DIR / "alerts.log"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{timestamp} [{alert_level.upper()}] {alert_type}: {message}\\n")
    
    print(f"⚠️ 报警触发：[{alert_level}] {alert_type} - {message}")
    
    return alert_record

if __name__ == "__main__":
    print("报警处理脚本已加载")
'''
    
    with open(alert_script, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 报警处理脚本已创建：{alert_script}")

def main():
    """主函数"""
    print("开始创建实时监控系统...")
    print(f"创建时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # 创建实时监控配置
    create_real_time_monitor()
    
    # 创建报警处理脚本
    create_alert_handler()
    
    print("=" * 70)
    print("实时监控系统创建完成！")
    
    print("\n监控系统功能：")
    print("  - 健康监控（5分钟检查）")
    print("  - 性能监控（10分钟检查）")
    print("  - 流量监控（30分钟检查）")
    print("  - 收入监控（1小时检查）")
    print("  - 系统监控（10分钟检查）")
    print("  - 报警系统（多级报警）")
    print("  - 监控仪表板（60秒刷新）")

if __name__ == "__main__":
    main()