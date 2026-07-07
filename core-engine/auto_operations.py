#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化运营脚本 - 整合所有监控和优化脚本，定期运行
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
CORE_ENGINE_DIR = ROOT_DIR / "core-engine"

SCRIPTS = [
    "site_health_monitor.py",
    "seo_optimizer.py",
    "traffic_analyzer.py",
    "revenue_analyzer.py",
    "comprehensive_report.py"
]

def run_all_scripts():
    """运行所有脚本"""
    print("=" * 80)
    print("Navigation Matrix Unified - 自动化运营报告")
    print("=" * 80)
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    success_count = 0
    fail_count = 0
    
    for script in SCRIPTS:
        script_path = CORE_ENGINE_DIR / script
        
        if not script_path.exists():
            print(f"❌ {script} 不存在")
            fail_count += 1
            continue
        
        print(f"正在运行: {script}")
        print("-" * 80)
        
        try:
            # 运行脚本
            result = subprocess.run(
                ["python", str(script_path)],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print(result.stdout)
                print(f"✅ {script} 运行成功")
                success_count += 1
            else:
                print(f"❌ {script} 运行失败")
                print(result.stderr)
                fail_count += 1
            
        except subprocess.TimeoutExpired:
            print(f"❌ {script} 运行超时")
            fail_count += 1
        except Exception as e:
            print(f"❌ {script} 运行异常: {e}")
            fail_count += 1
        
        print()
    
    # 运行总结
    print("=" * 80)
    print("自动化运营运行总结")
    print("=" * 80)
    print(f"总脚本数: {len(SCRIPTS)}")
    print(f"成功运行: {success_count}")
    print(f"失败运行: {fail_count}")
    print(f"成功率: {(success_count/len(SCRIPTS))*100:.1f}%")
    print()
    
    if success_count == len(SCRIPTS):
        print("🎉 所有脚本运行成功！项目状态良好！")
    else:
        print("⚠️ 部分脚本运行失败，请检查并修复")
    
    print()
    print("=" * 80)
    print("自动化运营报告完成")
    print("=" * 80)

def main():
    """主函数"""
    run_all_scripts()

if __name__ == '__main__':
    main()