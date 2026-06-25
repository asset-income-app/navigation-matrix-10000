#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务调度中心 - scheduler.py
自动调度所有定时任务，确保万站矩阵有序运行
"""

import os
import json
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
TASKS_DIR = DATA_DIR / "tasks"
LOGS_DIR = DATA_DIR / "logs"

# 任务配置
TASKS = {
    "daily": [
        {"name": "健康检查", "script": "monitor.py", "time": "06:00"},
        {"name": "数据备份", "script": "auto_backup.py", "time": "07:00"},
        {"name": "收入统计", "script": "revenue_tracker.py", "time": "08:00"},
        {"name": "链接检查", "script": "link_checker.py", "time": "09:00"},
    ],
    "weekly": [
        {"name": "SEO检查", "script": "seo_analyzer.py", "time": "周一 10:00"},
        {"name": "竞品监控", "script": "competitor_spy.py", "time": "周三 10:00"},
        {"name": "合规检查", "script": "compliance_checker.py", "time": "周五 10:00"},
    ],
    "monthly": [
        {"name": "月度报告", "script": "monthly_report.py", "time": "1日 09:00"},
        {"name": "数据清理", "script": "batch_cleaner.py", "time": "15日 10:00"},
    ]
}

def get_task_status():
    """获取任务状态"""
    pending_file = TASKS_DIR / "pending.json"
    running_file = TASKS_DIR / "running.json"
    completed_file = TASKS_DIR / "completed.json"
    
    pending = json.loads(pending_file.read_text()) if pending_file.exists() else []
    running = json.loads(running_file.read_text()) if running_file.exists() else []
    completed = json.loads(completed_file.read_text()) if completed_file.exists() else []
    
    return {"pending": pending, "running": running, "completed": completed}

def save_task_status(status):
    """保存任务状态"""
    (TASKS_DIR / "pending.json").write_text(json.dumps(status["pending"], indent=2))
    (TASKS_DIR / "running.json").write_text(json.dumps(status["running"], indent=2))
    (TASKS_DIR / "completed.json").write_text(json.dumps(status["completed"], indent=2))

def add_task(task_name, script, scheduled_time):
    """添加新任务"""
    status = get_task_status()
    new_task = {
        "id": f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{task_name}",
        "name": task_name,
        "script": script,
        "scheduled_time": scheduled_time,
        "created_at": datetime.now().isoformat(),
        "status": "pending"
    }
    status["pending"].append(new_task)
    save_task_status(status)
    print(f"✅ 任务已添加: {task_name} @ {scheduled_time}")
    return new_task

def run_task(task):
    """执行任务"""
    status = get_task_status()
    
    # 从pending移到running
    status["pending"] = [t for t in status["pending"] if t["id"] != task["id"]]
    task["status"] = "running"
    task["started_at"] = datetime.now().isoformat()
    status["running"].append(task)
    save_task_status(status)
    
    print(f"🚀 开始执行: {task['name']}")
    
    # 执行脚本
    script_path = ROOT_DIR / "core-engine" / task["script"]
    if script_path.exists():
        try:
            result = subprocess.run(
                ["python", str(script_path)],
                capture_output=True,
                text=True,
                timeout=3600  # 1小时超时
            )
            task["output"] = result.stdout[-500:] if result.stdout else ""
            task["error"] = result.stderr[-500:] if result.stderr else ""
            task["success"] = result.returncode == 0
        except subprocess.TimeoutExpired:
            task["error"] = "任务超时"
            task["success"] = False
        except Exception as e:
            task["error"] = str(e)
            task["success"] = False
    else:
        task["error"] = f"脚本不存在: {task['script']}"
        task["success"] = False
    
    # 从running移到completed
    status["running"] = [t for t in status["running"] if t["id"] != task["id"]]
    task["status"] = "completed"
    task["completed_at"] = datetime.now().isoformat()
    status["completed"].append(task)
    save_task_status(status)
    
    # 记录日志
    log_result(task)
    
    print(f"✅ 任务完成: {task['name']} - {'成功' if task['success'] else '失败'}")
    return task

def log_result(task):
    """记录任务结果"""
    log_dir = LOGS_DIR / "daily" / datetime.now().strftime("%Y-%m")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d')}_tasks.json"
    
    logs = json.loads(log_file.read_text()) if log_file.exists() else []
    logs.append(task)
    log_file.write_text(json.dumps(logs, indent=2))

def check_and_run_tasks():
    """检查并执行到期任务"""
    status = get_task_status()
    now = datetime.now()
    
    for task in status["pending"]:
        scheduled = datetime.fromisoformat(task["scheduled_time"])
        if now >= scheduled:
            run_task(task)

def schedule_all_tasks():
    """调度所有定时任务"""
    now = datetime.now()
    
    # 每日任务
    for task in TASKS["daily"]:
        scheduled_time = now.replace(
            hour=int(task["time"].split(":")[0]),
            minute=int(task["time"].split(":")[1]),
            second=0
        )
        if scheduled_time > now:
            add_task(task["name"], task["script"], scheduled_time.isoformat())
    
    # 每周任务
    for task in TASKS["weekly"]:
        day_name = task["time"].split(" ")[0]
        hour = int(task["time"].split(" ")[1].split(":")[0])
        minute = int(task["time"].split(" ")[1].split(":")[1])
        
        day_map = {"周一": 0, "周二": 1, "周三": 2, "周四": 3, "周五": 4, "周六": 5, "周日": 6}
        target_day = day_map.get(day_name, 0)
        
        days_ahead = target_day - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        
        scheduled_time = now + timedelta(days=days_ahead)
        scheduled_time = scheduled_time.replace(hour=hour, minute=minute, second=0)
        add_task(task["name"], task["script"], scheduled_time.isoformat())

def show_status():
    """显示任务状态"""
    status = get_task_status()
    
    print("\n" + "="*60)
    print("📊 任务调度中心状态")
    print("="*60)
    print(f"⏳ 待执行: {len(status['pending'])} 个")
    print(f"🚀 执行中: {len(status['running'])} 个")
    print(f"✅ 已完成: {len(status['completed'])} 个")
    print("="*60)
    
    if status["pending"]:
        print("\n待执行任务:")
        for t in status["pending"][:5]:
            print(f"  - {t['name']} @ {t['scheduled_time']}")
    
    if status["running"]:
        print("\n执行中任务:")
        for t in status["running"]:
            print(f"  - {t['name']} (开始: {t['started_at']})")
    
    if status["completed"]:
        print("\n最近完成:")
        for t in status["completed"][-5:]:
            status_icon = "✅" if t["success"] else "❌"
            print(f"  {status_icon} {t['name']} @ {t['completed_at']}")

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "status":
            show_status()
        elif command == "schedule":
            schedule_all_tasks()
        elif command == "run":
            status = get_task_status()
            if status["pending"]:
                run_task(status["pending"][0])
            else:
                print("没有待执行任务")
        elif command == "add":
            if len(sys.argv) >= 4:
                add_task(sys.argv[2], sys.argv[3], datetime.now().isoformat())
        else:
            print("用法: python scheduler.py [status|schedule|run|add]")
    else:
        # 默认显示状态并检查任务
        show_status()
        check_and_run_tasks()

if __name__ == "__main__":
    main()