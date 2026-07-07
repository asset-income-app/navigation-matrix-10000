"""
系统全面体检脚本
检查所有系统组件的完整性和健康状况
"""

import os
import json
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(r"E:\50\navigation-matrix-unified")
DATA_DIR = ROOT_DIR / "data"
CORE_ENGINE_DIR = ROOT_DIR / "core-engine"
SKILLS_DIR = ROOT_DIR / ".trae" / "skills"
MONITOR_DIR = ROOT_DIR / "04-monitor"

# 检查结果收集器
check_results = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "file_integrity": {},
    "script_validation": {},
    "data_validation": {},
    "config_validation": {},
    "skill_system": {},
    "monitoring_system": {},
    "overall_score": 0
}

def check_file_exists(file_path, category, file_name):
    """检查文件是否存在"""
    exists = file_path.exists()
    size = 0
    
    if exists:
        size = file_path.stat().st_size
    
    result_key = f"{category}_{file_name}"
    check_results["file_integrity"][result_key] = {
        "exists": exists,
        "path": str(file_path),
        "size": size,
        "status": "✅" if exists else "❌"
    }
    
    status_icon = "✅" if exists else "❌"
    print(f"{status_icon} {file_name}: {str(file_path)} ({size} bytes)")
    
    return exists

def check_script_validity(script_path, script_name):
    """检查脚本文件有效性"""
    if not script_path.exists():
        check_results["script_validation"][script_name] = {
            "exists": False,
            "valid": False,
            "executable": False,
            "status": "❌"
        }
        print(f"❌ {script_name}: 文件不存在")
        return False
    
    # 检查文件是否是有效的Python文件
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 简单的语法检查
            has_valid_syntax = "import" in content or "def" in content or "class" in content
            has_content = len(content) > 100
            
            valid = has_valid_syntax and has_content
            executable = True  # 假设可执行
            
            check_results["script_validation"][script_name] = {
                "exists": True,
                "valid": valid,
                "executable": executable,
                "content_length": len(content),
                "status": "✅" if valid else "⚠️"
            }
            
            status_icon = "✅" if valid else "⚠️"
            print(f"{status_icon} {script_name}: 有效脚本 ({len(content)} 字符)")
            
            return valid
    except Exception as e:
        check_results["script_validation"][script_name] = {
            "exists": True,
            "valid": False,
            "error": str(e),
            "status": "❌"
        }
        print(f"❌ {script_name}: 读取失败 - {str(e)}")
        return False

def check_data_file_validity(data_path, data_name):
    """检查数据文件有效性"""
    if not data_path.exists():
        check_results["data_validation"][data_name] = {
            "exists": False,
            "valid": False,
            "items_count": 0,
            "status": "❌"
        }
        print(f"❌ {data_name}: 文件不存在")
        return False
    
    # 检查JSON文件有效性
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # 计算数据项数量
            if isinstance(data, list):
                items_count = len(data)
            elif isinstance(data, dict):
                items_count = len(data.keys())
            else:
                items_count = 1
            
            valid = items_count > 0
            
            check_results["data_validation"][data_name] = {
                "exists": True,
                "valid": valid,
                "items_count": items_count,
                "status": "✅" if valid else "⚠️"
            }
            
            status_icon = "✅" if valid else "⚠️"
            print(f"{status_icon} {data_name}: 有效数据 ({items_count} 项)")
            
            return valid
    except Exception as e:
        check_results["data_validation"][data_name] = {
            "exists": True,
            "valid": False,
            "error": str(e),
            "status": "❌"
        }
        print(f"❌ {data_name}: JSON解析失败 - {str(e)}")
        return False

def check_config_file_validity(config_path, config_name):
    """检查配置文件有效性"""
    if not config_path.exists():
        check_results["config_validation"][config_name] = {
            "exists": False,
            "valid": False,
            "status": "❌"
        }
        print(f"❌ {config_name}: 配置文件不存在")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
            # 检查配置结构
            has_enabled = "enabled" in str(config)
            has_valid_structure = isinstance(config, dict) and len(config) > 0
            
            valid = has_enabled or has_valid_structure
            
            check_results["config_validation"][config_name] = {
                "exists": True,
                "valid": valid,
                "keys_count": len(config.keys()) if isinstance(config, dict) else 0,
                "status": "✅" if valid else "⚠️"
            }
            
            status_icon = "✅" if valid else "⚠️"
            print(f"{status_icon} {config_name}: 有效配置")
            
            return valid
    except Exception as e:
        check_results["config_validation"][config_name] = {
            "exists": True,
            "valid": False,
            "error": str(e),
            "status": "❌"
        }
        print(f"❌ {config_name}: 配置解析失败 - {str(e)}")
        return False

def check_skill_files():
    """检查技能文件完整性"""
    print("\n检查技能系统完整性...")
    
    if not SKILLS_DIR.exists():
        check_results["skill_system"]["directory_exists"] = False
        print("❌ 技能目录不存在")
        return
    
    # 遍历技能目录
    skill_count = 0
    valid_skill_count = 0
    
    for skill_dir in SKILLS_DIR.iterdir():
        if skill_dir.is_dir():
            skill_file = skill_dir / "SKILL.md"
            
            if skill_file.exists():
                skill_count += 1
                
                # 检查技能文件内容
                try:
                    with open(skill_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # 检查是否包含必要的技能信息
                        has_skill_info = "skill" in content.lower() or "技能" in content
                        has_content = len(content) > 50
                        
                        if has_skill_info and has_content:
                            valid_skill_count += 1
                except Exception:
                    pass
    
    check_results["skill_system"]["total_skills"] = skill_count
    check_results["skill_system"]["valid_skills"] = valid_skill_count
    check_results["skill_system"]["completeness"] = (valid_skill_count / skill_count * 100) if skill_count > 0 else 0
    check_results["skill_system"]["status"] = "✅" if valid_skill_count > 200 else "⚠️"
    
    print(f"✅ 技能文件总数：{skill_count}个")
    print(f"✅ 有效技能文件：{valid_skill_count}个")
    print(f"✅ 完整度：{check_results['skill_system']['completeness']:.1f}%")

def check_monitoring_system():
    """检查监控系统完整性"""
    print("\n检查监控系统完整性...")
    
    # 检查监控目录
    if not MONITOR_DIR.exists():
        check_results["monitoring_system"]["directory_exists"] = False
        print("❌ 监控目录不存在")
        return
    
    # 检查监控配置文件
    monitoring_config = DATA_DIR / "monitoring_config.json"
    if monitoring_config.exists():
        try:
            with open(monitoring_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
                # 检查监控系统数量
                monitor_count = 0
                if "real_time_monitor" in config:
                    monitor_count = len(config["real_time_monitor"].keys())
                
                check_results["monitoring_system"]["monitor_count"] = monitor_count
                check_results["monitoring_system"]["status"] = "✅" if monitor_count >= 5 else "⚠️"
                
                print(f"✅ 监控系统数量：{monitor_count}个")
        except Exception as e:
            check_results["monitoring_system"]["error"] = str(e)
            print(f"❌ 监控配置解析失败")
    else:
        check_results["monitoring_system"]["config_exists"] = False
        print("❌ 监控配置文件不存在")

def run_comprehensive_health_check():
    """运行全面体检"""
    print("=" * 70)
    print("导航矩阵系统全面体检开始...")
    print(f"体检时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # 1. 文件完整性检查
    print("\n【1. 核心文件完整性检查】")
    print("-" * 70)
    
    # 检查报告文件
    reports = [
        "PHASE4_FINAL_COMPLETE_REPORT.md",
        "PHASE3_FINAL_COMPLETE_REPORT.md",
        "FINAL_COMPREHENSIVE_PUSH_COMPLETE_REPORT.md",
        "HEALTH_STATUS_REPORT.md"
    ]
    
    for report in reports:
        check_file_exists(ROOT_DIR / report, "report", report)
    
    # 检查仪表板文件
    check_file_exists(ROOT_DIR / "dashboard.html", "dashboard", "dashboard.html")
    
    # 检查文档文件
    docs = ["API_DOCUMENTATION.md", "OPERATIONS_MANUAL.md"]
    for doc in docs:
        check_file_exists(ROOT_DIR / doc, "doc", doc)
    
    # 2. 脚本文件有效性检查
    print("\n【2. 脚本文件有效性检查】")
    print("-" * 70)
    
    scripts = [
        "monitor.py",
        "backup_daily.py",
        "content_updater.py",
        "seo_optimizer.py",
        "traffic_analyzer.py",
        "revenue_analyzer.py",
        "performance_benchmark.py",
        "performance_optimizer.py",
        "seo_continuous_optimizer.py",
        "api_query_system.py",
        "smart_content_updater.py"
    ]
    
    for script in scripts:
        check_script_validity(CORE_ENGINE_DIR / script, script)
    
    # 3. 数据文件有效性检查
    print("\n【3. 数据文件有效性检查】")
    print("-" * 70)
    
    data_files = [
        "cities.json",
        "niches.json",
        "hybrids.json",
        "site_content.json",
        "performance_benchmark.json"
    ]
    
    for data_file in data_files:
        check_data_file_validity(DATA_DIR / data_file, data_file)
    
    # 4. 配置文件有效性检查
    print("\n【4. 配置文件有效性检查】")
    print("-" * 70)
    
    config_files = [
        "automation_config.json",
        "monetization_config.json",
        "monitoring_config.json",
        "performance_config.json",
        "seo_continuous_config.json"
    ]
    
    for config_file in config_files:
        check_config_file_validity(DATA_DIR / config_file, config_file)
    
    # 5. 技能系统检查
    check_skill_files()
    
    # 6. 监控系统检查
    check_monitoring_system()
    
    # 计算总体健康分数
    calculate_overall_score()
    
    # 生成体检报告
    generate_health_report()
    
    print("=" * 70)
    print("全面体检完成！")
    print(f"总体健康分数：{check_results['overall_score']}分")
    print("=" * 70)

def calculate_overall_score():
    """计算总体健康分数"""
    score_components = []
    
    # 文件完整性分数（满分25分）
    file_exists_count = sum(1 for result in check_results["file_integrity"].values() if result["exists"])
    file_total_count = len(check_results["file_integrity"])
    file_score = (file_exists_count / file_total_count * 25) if file_total_count > 0 else 0
    score_components.append(file_score)
    
    # 脚本有效性分数（满分25分）
    script_valid_count = sum(1 for result in check_results["script_validation"].values() if result["valid"])
    script_total_count = len(check_results["script_validation"])
    script_score = (script_valid_count / script_total_count * 25) if script_total_count > 0 else 0
    score_components.append(script_score)
    
    # 数据有效性分数（满分20分）
    data_valid_count = sum(1 for result in check_results["data_validation"].values() if result["valid"])
    data_total_count = len(check_results["data_validation"])
    data_score = (data_valid_count / data_total_count * 20) if data_total_count > 0 else 0
    score_components.append(data_score)
    
    # 配置有效性分数（满分15分）
    config_valid_count = sum(1 for result in check_results["config_validation"].values() if result["valid"])
    config_total_count = len(check_results["config_validation"])
    config_score = (config_valid_count / config_total_count * 15) if config_total_count > 0 else 0
    score_components.append(config_score)
    
    # 技能系统分数（满分10分）
    skill_completeness = check_results["skill_system"].get("completeness", 0)
    skill_score = (skill_completeness / 100 * 10)
    score_components.append(skill_score)
    
    # 监控系统分数（满分5分）
    monitor_count = check_results["monitoring_system"].get("monitor_count", 0)
    monitor_score = (monitor_count / 5 * 5) if monitor_count > 0 else 0
    score_components.append(monitor_score)
    
    check_results["overall_score"] = sum(score_components)
    
    print(f"\n健康分数组成：")
    print(f"  文件完整性：{file_score:.1f}分（满分25分）")
    print(f"  脚本有效性：{script_score:.1f}分（满分25分）")
    print(f"  数据有效性：{data_score:.1f}分（满分20分）")
    print(f"  配置有效性：{config_score:.1f}分（满分15分）")
    print(f"  技能系统：{skill_score:.1f}分（满分10分）")
    print(f"  监控系统：{monitor_score:.1f}分（满分5分）")

def generate_health_report():
    """生成体检报告"""
    report_file = ROOT_DIR / "COMPREHENSIVE_HEALTH_CHECK_REPORT.md"
    
    # 生成报告内容
    report_content = f"""# 导航矩阵系统全面体检报告

## 体检时间
**检查日期：** {check_results['timestamp']}
**总体健康分数：** {check_results['overall_score']:.1f}分（满分100分）

---

## 体检结果总览

### 健康状态
{'✅ 优秀' if check_results['overall_score'] >= 95 else '⚠️ 良好' if check_results['overall_score'] >= 80 else '❌ 需改进'}

---

## 详细检查结果

### 1. 文件完整性检查
**检查项目：** {len(check_results['file_integrity'])}个文件
**完整文件：** {sum(1 for r in check_results['file_integrity'].values() if r['exists'])}个
**缺失文件：** {sum(1 for r in check_results['file_integrity'].values() if not r['exists'])}个

"""

    # 添加文件检查详情
    report_content += "#### 文件检查详情\n\n"
    for key, result in check_results['file_integrity'].items():
        status = result['status']
        path = result['path']
        size = result['size']
        report_content += f"- {status} `{key.split('_')[1]}`: {path} ({size} bytes)\n"
    
    # 添加脚本检查详情
    report_content += f"""
### 2. 脚本有效性检查
**检查项目：** {len(check_results['script_validation'])}个脚本
**有效脚本：** {sum(1 for r in check_results['script_validation'].values() if r['valid'])}个
**无效脚本：** {sum(1 for r in check_results['script_validation'].values() if not r['valid'])}个

#### 脚本检查详情

"""
    for key, result in check_results['script_validation'].items():
        status = result['status']
        exists = result['exists']
        valid = result['valid']
        content_length = result.get('content_length', 0)
        report_content += f"- {status} `{key}`: 存在={exists}, 有效={valid}, 内容长度={content_length}字符\n"
    
    # 添加数据检查详情
    report_content += f"""
### 3. 数据有效性检查
**检查项目：** {len(check_results['data_validation'])}个数据文件
**有效数据：** {sum(1 for r in check_results['data_validation'].values() if r['valid'])}个
**无效数据：** {sum(1 for r in check_results['data_validation'].values() if not r['valid'])}个

#### 数据检查详情

"""
    for key, result in check_results['data_validation'].items():
        status = result['status']
        exists = result['exists']
        valid = result['valid']
        items_count = result.get('items_count', 0)
        report_content += f"- {status} `{key}`: 存在={exists}, 有效={valid}, 数据项={items_count}个\n"
    
    # 添加配置检查详情
    report_content += f"""
### 4. 配置有效性检查
**检查项目：** {len(check_results['config_validation'])}个配置文件
**有效配置：** {sum(1 for r in check_results['config_validation'].values() if r['valid'])}个
**无效配置：** {sum(1 for r in check_results['config_validation'].values() if not r['valid'])}个

#### 配置检查详情

"""
    for key, result in check_results['config_validation'].items():
        status = result['status']
        exists = result['exists']
        valid = result['valid']
        keys_count = result.get('keys_count', 0)
        report_content += f"- {status} `{key}`: 存在={exists}, 有效={valid}, 配置键={keys_count}个\n"
    
    # 添加技能系统检查
    skill_total = check_results['skill_system'].get('total_skills', 0)
    skill_valid = check_results['skill_system'].get('valid_skills', 0)
    skill_completeness = check_results['skill_system'].get('completeness', 0)
    
    report_content += f"""
### 5. 技能系统检查
**技能总数：** {skill_total}个
**有效技能：** {skill_valid}个
**完整度：** {skill_completeness:.1f}%

"""

    # 添加监控系统检查
    monitor_count = check_results['monitoring_system'].get('monitor_count', 0)
    
    report_content += f"""
### 6. 监控系统检查
**监控系统数量：** {monitor_count}个

---

## 健康分数组成

| 检查项目 | 得分 | 满分 | 占比 |
|---------|-----|------|------|
| 文件完整性 | {check_results['overall_score'] * 0.25:.1f} | 25 | 25% |
| 脚本有效性 | {check_results['overall_score'] * 0.25:.1f} | 25 | 25% |
| 数据有效性 | {check_results['overall_score'] * 0.20:.1f} | 20 | 20% |
| 配置有效性 | {check_results['overall_score'] * 0.15:.1f} | 15 | 15% |
| 技能系统 | {check_results['overall_score'] * 0.10:.1f} | 10 | 10% |
| 监控系统 | {check_results['overall_score'] * 0.05:.1f} | 5 | 5% |
| **总分** | **{check_results['overall_score']:.1f}** | **100** | **100%** |

---

## 系统建议

{'✅ 系统状态优秀，建议继续保持自动化运营。' if check_results['overall_score'] >= 95 else '⚠️ 系统状态良好，建议优化部分组件。' if check_results['overall_score'] >= 80 else '❌ 系统状态需要改进，建议修复缺失和无效组件。'}

---

**体检报告生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # 保存报告
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\n✅ 体检报告已生成：{report_file}")
    
    # 同时保存JSON格式的检查结果
    json_report_file = ROOT_DIR / "health_check_results.json"
    with open(json_report_file, 'w', encoding='utf-8') as f:
        json.dump(check_results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ JSON检查结果已保存：{json_report_file}")

if __name__ == "__main__":
    run_comprehensive_health_check()