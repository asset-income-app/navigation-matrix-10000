"""
系统实际运行测试脚本
验证所有自动化脚本的运行效果
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(r"E:\50\navigation-matrix-unified")
CORE_ENGINE_DIR = ROOT_DIR / "core-engine"

# 测试脚本列表
TEST_SCRIPTS = [
    "monitor.py",
    "backup_daily.py",
    "content_updater.py",
    "seo_optimizer.py",
    "traffic_analyzer.py",
    "revenue_analyzer.py"
]

def run_script_test(script_name):
    """运行单个脚本测试"""
    script_path = CORE_ENGINE_DIR / script_name
    
    if not script_path.exists():
        print(f"⚠️ 脚本不存在：{script_name}")
        return False
    
    print(f"\n测试脚本：{script_name}")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            ["python", str(script_path)],
            cwd=str(CORE_ENGINE_DIR),
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print(f"✅ 测试成功：{script_name}")
            print(f"输出：{result.stdout[:500]}")
            return True
        else:
            print(f"❌ 测试失败：{script_name}")
            print(f"错误：{result.stderr[:500]}")
            return False
    except Exception as e:
        print(f"❌ 测试异常：{script_name}")
        print(f"异常信息：{str(e)}")
        return False

def run_all_tests():
    """运行所有脚本测试"""
    print("开始系统实际运行测试...")
    print(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    success_count = 0
    fail_count = 0
    
    for script in TEST_SCRIPTS:
        if run_script_test(script):
            success_count += 1
        else:
            fail_count += 1
    
    print("\n" + "=" * 70)
    print(f"系统测试完成！")
    print(f"  - 成功：{success_count} 个脚本")
    print(f"  - 失败：{fail_count} 个脚本")
    print(f"  - 成功率：{success_count / len(TEST_SCRIPTS) * 100:.1f}%")
    
    return success_count, fail_count

if __name__ == "__main__":
    success, fail = run_all_tests()
    
    if fail == 0:
        print("\n✅ 所有脚本测试通过！系统运行稳定。")
    else:
        print(f"\n⚠️ 有 {fail} 个脚本测试失败，需要修复。")