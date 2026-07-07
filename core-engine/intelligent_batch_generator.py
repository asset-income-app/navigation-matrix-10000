"""
智能执行员工技能批量生成器
自动生成所有剩余的执行员工技能文件
"""

import os

SKILLS_ROOT = r"E:\50\navigation-matrix-unified\.trae\skills"

# 板块负责人到执行员工的映射规则
BLOCK_STAFF_RULES = {
    # 关键词优化板块
    "keyword-optimizer-leader": [
        ("keyword-researcher", "关键词研究员", "研究关键词、分析竞争度、挖掘机会"),
        ("keyword-optimizer", "关键词优化员", "优化关键词布局、提升关键词排名"), # 已存在
        ("keyword-tracker", "关键词追踪员", "追踪关键词排名、监控关键词变化"),
        ("keyword-reporter", "关键词报告员", "生成关键词报告、统计关键词数据"),
    ],
    
    # 内容SEO板块
    "link-optimizer-leader": [
        ("content-seo-optimizer", "内容SEO优化员", "优化内容SEO、提升内容相关性"),
        ("content-seo-analyzer", "内容SEO分析师", "分析内容SEO效果、识别SEO问题"),
        ("content-seo-checker", "内容SEO检查员", "检查内容SEO质量、验证SEO标准"),
        ("content-seo-reporter", "内容SEO报告员", "生成内容SEO报告、提供SEO建议"),
    ],
    
    # 技术SEO板块
    "tech-seo-leader": [
        ("tech-seo-optimizer", "技术SEO优化员", "优化技术SEO元素、提升技术SEO表现"),
        ("tech-seo-analyzer", "技术SEO分析师", "分析技术SEO数据、识别技术SEO问题"),
        ("tech-seo-checker", "技术SEO检查员", "检查技术SEO质量、验证技术SEO标准"),
        ("tech-seo-reporter", "技术SEO报告员", "生成技术SEO报告、提供技术SEO建议"),
    ],
    
    # 外链优化板块
    "backlink-optimizer-leader": [
        ("backlink-builder", "外链建设员", "建设外部链接、拓展外链渠道"),
        ("backlink-analyzer", "外链分析师", "分析外链质量、评估外链效果"),
        ("backlink-checker", "外链检查员", "检查外链状态、验证外链有效性"),
        ("backlink-reporter", "外链报告员", "生成外链报告、统计外链数据"),
    ],
    
    # SEO监控板块
    "seo-monitor-leader": [
        ("seo-monitor", "SEO监控员", "监控SEO表现、检测SEO变化"),
        ("seo-analyzer", "SEO分析师", "分析SEO数据、识别SEO问题"), # 已存在
        ("seo-tracker", "SEO追踪员", "追踪SEO变化、分析SEO趋势"),
        ("seo-reporter", "SEO报告员", "生成SEO报告、提供SEO建议"),
    ],
    
    # 健康监控板块
    "health-monitor-leader": [
        ("health-monitor", "健康监控员", "监控站点健康、收集健康数据"),
        ("health-data-collector", "健康数据收集员", "收集健康数据、整理健康指标"),
        ("health-analyzer", "健康分析师", "分析健康数据、识别健康问题"),
        ("health-reporter", "健康报告员", "生成健康报告、提供健康建议"),
    ],
    
    # 健康诊断板块
    "health-diagnosis-leader": [
        ("health-diagnostician", "健康诊断员", "诊断健康问题、分析问题原因"),
        ("health-problem-analyzer", "健康问题分析师", "分析健康问题、评估问题严重性"),
        ("health-solution-designer", "健康解决方案设计师", "设计健康解决方案、规划修复策略"),
        ("health-evaluator", "健康评估员", "评估健康方案、验证方案效果"),
    ],
    
    # 健康修复板块
    "health-repair-leader": [
        ("health-repairer", "健康修复员", "修复健康问题、执行修复方案"),
        ("auto-repairer", "自动修复员", "自动修复常见问题、快速处理异常"), # 已存在为auto-repair
        ("repair-verifier", "修复验证员", "验证修复效果、确认问题解决"),
        ("repair-reporter", "修复报告员", "生成修复报告、记录修复过程"),
    ],
    
    # 健康预防板块
    "health-prevention-leader": [
        ("health-preventer", "健康预防员", "预防健康问题、执行预防措施"),
        ("health-alerter", "健康预警员", "发出健康预警、提醒风险问题"),
        ("health-strategy-planner", "健康策略规划员", "规划健康预防策略、制定预防计划"),
        ("health-trainer", "健康培训员", "培训健康预防知识、指导预防方法"),
    ],
    
    # 流量分析板块
    "traffic-analysis-leader": [
        ("traffic-analyzer-exec", "流量分析执行员", "分析流量数据、识别流量特征"), # 已存在为traffic-analyzer
        ("traffic-source-analyzer", "流量来源分析师", "分析流量来源、评估来源质量"),
        ("traffic-path-analyzer", "流量路径分析师", "分析流量路径、优化路径引导"),
        ("traffic-reporter", "流量报告员", "生成流量报告、提供流量建议"),
    ],
    
    # 流量优化板块
    "traffic-optimizer-leader": [
        ("traffic-optimizer-exec", "流量优化执行员", "执行流量优化、提升流量质量"),
        ("traffic-channel-optimizer", "流量渠道优化员", "优化流量渠道、拓展流量来源"),
        ("traffic-conversion-optimizer", "流量转化优化员", "优化流量转化、提升转化率"),
        ("traffic-optimization-reporter", "流量优化报告员", "生成流量优化报告、统计优化效果"),
    ],
    
    # 流量监控板块
    "traffic-monitor-leader": [
        ("traffic-monitor", "流量监控员", "监控流量数据、检测流量异常"),
        ("traffic-tracker", "流量追踪员", "追踪流量变化、记录流量趋势"),
        ("traffic-alerter", "流量预警员", "发出流量预警、提醒异常流量"),
        ("traffic-monitor-reporter", "流量监控报告员", "生成流量监控报告、统计监控数据"),
    ],
    
    # 流量预测板块
    "traffic-forecast-leader": [
        ("traffic-forecaster", "流量预测员", "预测流量趋势、预估流量数量"),
        ("traffic-model-builder", "流量模型构建员", "构建流量预测模型、优化预测算法"),
        ("traffic-scenario-analyzer", "流量场景分析师", "分析流量场景、预测场景流量"),
        ("traffic-forecast-reporter", "流量预测报告员", "生成流量预测报告、提供预测建议"),
    ],
}

def generate_skill_content(staff_id, staff_name, staff_desc, leader_id):
    """生成技能文件内容"""
    content = f"""---
name: "{staff_id}"
description: "{staff_name}，{staff_desc}。向{leader_id}汇报。Invoke when user asks for {staff_name.replace(' ', '')} related work."
---

# {staff_name}

## 职位说明
**职位名称：** {staff_name}
**汇报对象：** {leader_id}
**工作性质：** 执行员工

## 核心职责
{staff_desc}

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
执行{staff_name}工作任务
生成{staff_name}工作报告
提交{staff_name}工作结果
```
"""
    return content

def batch_generate_all():
    """批量生成所有执行员工技能"""
    total_generated = 0
    skipped = []
    
    for leader_id, staff_list in BLOCK_STAFF_RULES.items():
        for staff_id, staff_name, staff_desc in staff_list:
            # 检查是否已存在
            skill_dir = os.path.join(SKILLS_ROOT, staff_id)
            skill_file = os.path.join(skill_dir, "SKILL.md")
            
            if os.path.exists(skill_file):
                skipped.append(staff_id)
                print(f"⏩ 已存在，跳过：{staff_id}")
                continue
            
            # 创建目录
            os.makedirs(skill_dir, exist_ok=True)
            
            # 生成内容
            content = generate_skill_content(staff_id, staff_name, staff_desc, leader_id)
            
            # 写入文件
            with open(skill_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            total_generated += 1
            print(f"✅ 已创建：{staff_id} ({staff_name})")
    
    return total_generated, skipped

if __name__ == "__main__":
    print("开始智能批量生成执行员工技能...")
    print("=" * 60)
    
    generated, skipped = batch_generate_all()
    
    print("=" * 60)
    print(f"智能批量生成完成！")
    print(f"  - 新生成：{generated} 个执行员工技能")
    print(f"  - 已存在：{len(skipped)} 个执行员工技能")
    print(f"  - 本次处理：{generated + len(skipped)} 个")
    
    if skipped:
        print("\n已存在的技能（已跳过）：")
        for skill_id in skipped:
            print(f"  - {skill_id}")