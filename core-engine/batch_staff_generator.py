"""
执行员工技能批量生成器
自动生成所有剩余的执行员工技能文件
"""

import os
import json

# 技能根目录
SKILLS_ROOT = r"E:\50\navigation-matrix-unified\.trae\skills"

# 执行员工模板定义
STAFF_TEMPLATES = {
    # SEO管理板块执行员工
    "keyword-researcher": {
        "leader": "keyword-optimizer-leader",
        "name": "关键词研究员",
        "description": "关键词研究员，负责研究关键词、分析关键词竞争度、挖掘关键词机会。向keyword-optimizer-leader汇报。",
        "responsibilities": ["研究关键词", "分析关键词竞争度", "挖掘关键词机会", "生成关键词研究报告"]
    },
    "keyword-tracker": {
        "leader": "keyword-optimizer-leader",
        "name": "关键词追踪员",
        "description": "关键词追踪员，负责追踪关键词排名、监控关键词变化、分析关键词趋势。向keyword-optimizer-leader汇报。",
        "responsibilities": ["追踪关键词排名", "监控关键词变化", "分析关键词趋势", "生成关键词追踪报告"]
    },
    "keyword-reporter": {
        "leader": "keyword-optimizer-leader",
        "name": "关键词报告员",
        "description": "关键词报告员，负责生成关键词报告、统计关键词数据、提供关键词优化建议。向keyword-optimizer-leader汇报。",
        "responsibilities": ["生成关键词报告", "统计关键词数据", "分析关键词表现", "提供关键词优化建议"]
    },
    
    # 流量管理板块执行员工
    "traffic-monitor": {
        "leader": "traffic-monitor-leader",
        "name": "流量监控员",
        "description": "流量监控员，负责监控流量数据、检测流量异常、预警流量风险。向traffic-monitor-leader汇报。",
        "responsibilities": ["监控流量数据", "检测流量异常", "预警流量风险", "生成流量监控报告"]
    },
    "traffic-tracker": {
        "leader": "traffic-monitor-leader",
        "name": "流量追踪员",
        "description": "流量追踪员，负责追踪流量来源、分析流量路径、优化流量引导。向traffic-monitor-leader汇报。",
        "responsibilities": ["追踪流量来源", "分析流量路径", "优化流量引导", "生成流量追踪报告"]
    },
    
    # 健康管理板块执行员工
    "health-monitor": {
        "leader": "health-monitor-leader",
        "name": "健康监控员",
        "description": "健康监控员，负责监控站点健康、收集健康数据、分析健康指标。向health-monitor-leader汇报。",
        "responsibilities": ["监控站点健康", "收集健康数据", "分析健康指标", "生成健康监控报告"]
    },
    "health-reporter": {
        "leader": "health-monitor-leader",
        "name": "健康报告员",
        "description": "健康报告员，负责生成健康报告、统计健康数据、提供健康优化建议。向health-monitor-leader汇报。",
        "responsibilities": ["生成健康报告", "统计健康数据", "分析健康趋势", "提供健康优化建议"]
    },
    
    # 数据管理板块执行员工
    "data-validator": {
        "leader": "data-validation-leader",
        "name": "数据验证员",
        "description": "数据验证员，负责验证数据完整性、检查数据准确性、确保数据一致性。向data-validation-leader汇报。",
        "responsibilities": ["验证数据完整性", "检查数据准确性", "确保数据一致性", "生成数据验证报告"]
    },
    "data-backup-executor": {
        "leader": "data-backup-leader",
        "name": "数据备份执行员",
        "description": "数据备份执行员，负责执行数据备份、管理备份文件、验证备份完整性。向data-backup-leader汇报。",
        "responsibilities": ["执行数据备份", "管理备份文件", "验证备份完整性", "生成备份执行报告"]
    }
}

def generate_skill_file(staff_id, template):
    """生成单个技能文件"""
    skill_dir = os.path.join(SKILLS_ROOT, staff_id)
    skill_file = os.path.join(skill_dir, "SKILL.md")
    
    # 创建技能目录
    os.makedirs(skill_dir, exist_ok=True)
    
    # 生成技能内容
    content = f"""---
name: "{staff_id}"
description: "{template['description']}"
---

# {template['name']}

## 职位说明
**职位名称：** {template['name']}
**汇报对象：** {template['leader']}
**工作性质：** 执行员工

## 核心职责
"""
    
    # 添加职责
    for i, resp in enumerate(template['responsibilities'], 1):
        content += f"{i}. **{resp}**\n"
    
    content += f"""
## 工作流程
1. **任务接收：** 接收上级任务指令
2. **工作执行：** 执行具体工作任务
3. **结果验证：** 验证工作成果质量
4. **报告提交：** 提交工作执行报告

## 关键指标
- 工作完成率：95%
- 质量达标率：90%
- 报告及时性：100%

## 使用示例
```
执行具体工作任务
生成工作执行报告
提交质量验证结果
```
"""
    
    # 写入文件
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return skill_file

def batch_generate_all_staff():
    """批量生成所有执行员工技能"""
    generated_files = []
    
    for staff_id, template in STAFF_TEMPLATES.items():
        skill_file = generate_skill_file(staff_id, template)
        generated_files.append(skill_file)
        print(f"✅ 已创建：{staff_id}")
    
    return generated_files

# 执行批量生成
if __name__ == "__main__":
    print("开始批量生成执行员工技能...")
    print("=" * 50)
    
    generated_files = batch_generate_all_staff()
    
    print("=" * 50)
    print(f"批量生成完成！共生成 {len(generated_files)} 个执行员工技能文件")
    print("\n生成文件列表：")
    for file in generated_files:
        print(f"  - {file}")