"""
完整执行员工技能批量生成器 - 最终版本
自动生成所有剩余的执行员工技能文件
"""

import os

SKILLS_ROOT = r"E:\50\navigation-matrix-unified\.trae\skills"

# 完整的板块负责人到执行员工映射规则
COMPLETE_BLOCK_STAFF_RULES = {
    # SEO管理板块（已完成部分，补充剩余）
    "keyword-optimizer-leader": [
        ("keyword-researcher", "关键词研究员", "研究关键词、分析竞争度"),
        ("keyword-optimizer", "关键词优化员", "优化关键词布局"),
        ("keyword-tracker", "关键词追踪员", "追踪关键词排名"),
        ("keyword-reporter", "关键词报告员", "生成关键词报告"),
    ],
    "link-optimizer-leader": [
        ("content-seo-optimizer", "内容SEO优化员", "优化内容SEO"),
        ("content-seo-analyzer", "内容SEO分析师", "分析内容SEO效果"),
        ("content-seo-checker", "内容SEO检查员", "检查内容SEO质量"),
        ("content-seo-reporter", "内容SEO报告员", "生成内容SEO报告"),
    ],
    "tech-seo-leader": [
        ("tech-seo-optimizer", "技术SEO优化员", "优化技术SEO元素"),
        ("tech-seo-analyzer", "技术SEO分析师", "分析技术SEO数据"),
        ("tech-seo-checker", "技术SEO检查员", "检查技术SEO质量"),
        ("tech-seo-reporter", "技术SEO报告员", "生成技术SEO报告"),
    ],
    "backlink-optimizer-leader": [
        ("backlink-builder", "外链建设员", "建设外部链接"),
        ("backlink-analyzer", "外链分析师", "分析外链质量"),
        ("backlink-checker", "外链检查员", "检查外链状态"),
        ("backlink-reporter", "外链报告员", "生成外链报告"),
    ],
    "seo-monitor-leader": [
        ("seo-monitor", "SEO监控员", "监控SEO表现"),
        ("seo-analyzer", "SEO分析师", "分析SEO数据"),
        ("seo-tracker", "SEO追踪员", "追踪SEO变化"),
        ("seo-reporter", "SEO报告员", "生成SEO报告"),
    ],
    
    # 健康管理板块（已完成部分，补充剩余）
    "health-monitor-leader": [
        ("health-monitor", "健康监控员", "监控站点健康"),
        ("health-data-collector", "健康数据收集员", "收集健康数据"),
        ("health-analyzer", "健康分析师", "分析健康数据"),
        ("health-reporter", "健康报告员", "生成健康报告"),
    ],
    "health-diagnosis-leader": [
        ("health-diagnostician", "健康诊断员", "诊断健康问题"),
        ("health-problem-analyzer", "健康问题分析师", "分析健康问题"),
        ("health-solution-designer", "健康解决方案设计师", "设计健康解决方案"),
        ("health-evaluator", "健康评估员", "评估健康方案"),
    ],
    "health-repair-leader": [
        ("health-repairer", "健康修复员", "修复健康问题"),
        ("auto-repairer", "自动修复员", "自动修复常见问题"),
        ("repair-verifier", "修复验证员", "验证修复效果"),
        ("repair-reporter", "修复报告员", "生成修复报告"),
    ],
    "health-prevention-leader": [
        ("health-preventer", "健康预防员", "预防健康问题"),
        ("health-alerter", "健康预警员", "发出健康预警"),
        ("health-strategy-planner", "健康策略规划员", "规划健康预防策略"),
        ("health-trainer", "健康培训员", "培训健康预防知识"),
    ],
    
    # 流量管理板块（已完成部分，补充剩余）
    "traffic-analysis-leader": [
        ("traffic-analyzer-exec", "流量分析执行员", "分析流量数据"),
        ("traffic-source-analyzer", "流量来源分析师", "分析流量来源"),
        ("traffic-path-analyzer", "流量路径分析师", "分析流量路径"),
        ("traffic-reporter", "流量报告员", "生成流量报告"),
    ],
    "traffic-optimizer-leader": [
        ("traffic-optimizer-exec", "流量优化执行员", "执行流量优化"),
        ("traffic-channel-optimizer", "流量渠道优化员", "优化流量渠道"),
        ("traffic-conversion-optimizer", "流量转化优化员", "优化流量转化"),
        ("traffic-optimization-reporter", "流量优化报告员", "生成流量优化报告"),
    ],
    "traffic-monitor-leader": [
        ("traffic-monitor", "流量监控员", "监控流量数据"),
        ("traffic-tracker", "流量追踪员", "追踪流量变化"),
        ("traffic-alerter", "流量预警员", "发出流量预警"),
        ("traffic-monitor-reporter", "流量监控报告员", "生成流量监控报告"),
    ],
    "traffic-forecast-leader": [
        ("traffic-forecaster", "流量预测员", "预测流量趋势"),
        ("traffic-model-builder", "流量模型构建员", "构建流量预测模型"),
        ("traffic-scenario-analyzer", "流量场景分析师", "分析流量场景"),
        ("traffic-forecast-reporter", "流量预测报告员", "生成流量预测报告"),
    ],
    
    # 收入管理板块（全新）
    "revenue-analysis-leader": [
        ("revenue-analyzer-exec", "收入分析执行员", "分析收入数据"),
        ("revenue-source-analyzer", "收入来源分析师", "分析收入来源"),
        ("revenue-trend-analyzer", "收入趋势分析师", "分析收入趋势"),
        ("revenue-analysis-reporter", "收入分析报告员", "生成收入分析报告"),
    ],
    "revenue-optimizer-leader": [
        ("revenue-optimizer-exec", "收入优化执行员", "执行收入优化"),
        ("revenue-channel-optimizer", "收入渠道优化员", "优化收入渠道"),
        ("revenue-strategy-optimizer", "收入策略优化员", "优化收入策略"),
        ("revenue-optimization-reporter", "收入优化报告员", "生成收入优化报告"),
    ],
    "monetization-strategy-leader": [
        ("monetization-strategy-designer", "变现策略设计师", "设计变现策略"),
        ("monetization-channel-developer", "变现渠道开发员", "开发变现渠道"),
        ("monetization-method-tester", "变现方法测试员", "测试变现方法"),
        ("monetization-strategy-reporter", "变现策略报告员", "生成变现策略报告"),
    ],
    "revenue-forecast-leader": [
        ("revenue-forecaster", "收入预测员", "预测收入趋势"),
        ("revenue-model-builder", "收入模型构建员", "构建收入预测模型"),
        ("revenue-scenario-analyzer", "收入场景分析师", "分析收入场景"),
        ("revenue-forecast-reporter", "收入预测报告员", "生成收入预测报告"),
    ],
    
    # 部署管理板块（全新）
    "deploy-execution-leader": [
        ("deploy-executor", "部署执行员", "执行部署任务"),
        ("deploy-batch-manager", "部署批次管理员", "管理部署批次"),
        ("deploy-file-preparer", "部署文件准备员", "准备部署文件"),
        ("deploy-execution-reporter", "部署执行报告员", "生成部署执行报告"),
    ],
    "deploy-monitor-leader": [
        ("deploy-monitor", "部署监控员", "监控部署状态"),
        ("deploy-status-tracker", "部署状态追踪员", "追踪部署状态"),
        ("deploy-error-detector", "部署错误检测员", "检测部署错误"),
        ("deploy-monitor-reporter", "部署监控报告员", "生成部署监控报告"),
    ],
    "deploy-optimizer-leader": [
        ("deploy-optimizer", "部署优化员", "优化部署流程"),
        ("deploy-performance-optimizer", "部署性能优化员", "优化部署性能"),
        ("deploy-efficiency-improver", "部署效率提升员", "提升部署效率"),
        ("deploy-optimization-reporter", "部署优化报告员", "生成部署优化报告"),
    ],
    "deploy-backup-leader": [
        ("deploy-backup-executor", "部署备份执行员", "执行部署备份"),
        ("deploy-backup-validator", "部署备份验证员", "验证部署备份"),
        ("deploy-backup-manager", "部署备份管理员", "管理部署备份"),
        ("deploy-backup-reporter", "部署备份报告员", "生成部署备份报告"),
    ],
    
    # 内容管理板块（全新）
    "content-generation-leader": [
        ("content-generator-exec", "内容生成执行员", "执行内容生成"),
        ("content-template-designer", "内容模板设计师", "设计内容模板"),
        ("content-quality-generator", "内容质量生成员", "生成高质量内容"),
        ("content-generation-reporter", "内容生成报告员", "生成内容生成报告"),
    ],
    "content-review-leader": [
        ("content-reviewer", "内容审核员", "审核内容质量"),
        ("content-standard-checker", "内容标准检查员", "检查内容标准"),
        ("content-error-detector", "内容错误检测员", "检测内容错误"),
        ("content-review-reporter", "内容审核报告员", "生成内容审核报告"),
    ],
    "content-update-leader": [
        ("content-updater-general", "内容更新通用员", "更新内容信息"),
        ("content-refresh-executor", "内容刷新执行员", "执行内容刷新"),
        ("content-version-manager", "内容版本管理员", "管理内容版本"),
        ("content-update-reporter", "内容更新报告员", "生成内容更新报告"),
    ],
    "content-optimizer-leader": [
        ("content-optimizer-exec", "内容优化执行员", "执行内容优化"),
        ("content-seo-optimizer-general", "内容SEO优化通用员", "优化内容SEO"),
        ("content-quality-improver", "内容质量提升员", "提升内容质量"),
        ("content-optimization-reporter", "内容优化报告员", "生成内容优化报告"),
    ],
    
    # 数据管理板块（补充剩余）
    "data-validation-leader": [
        ("data-validator", "数据验证员", "验证数据完整性"),
        ("data-integrity-checker", "数据完整性检查员", "检查数据完整性"),
        ("data-accuracy-validator", "数据准确性验证员", "验证数据准确性"),
        ("data-validation-reporter", "数据验证报告员", "生成数据验证报告"),
    ],
    "data-backup-leader": [
        ("data-backup-executor", "数据备份执行员", "执行数据备份"),
        ("data-backup-scheduler", "数据备份调度员", "调度数据备份"),
        ("data-backup-validator", "数据备份验证员", "验证数据备份"),
        ("data-backup-reporter", "数据备份报告员", "生成数据备份报告"),
    ],
    "data-analysis-leader": [
        ("data-analyzer-exec", "数据分析执行员", "执行数据分析"),
        ("data-statistician", "数据统计员", "统计数据信息"),
        ("data-trend-analyzer", "数据趋势分析师", "分析数据趋势"),
        ("data-analysis-reporter", "数据分析报告员", "生成数据分析报告"),
    ],
    "data-security-leader": [
        ("data-security-guard", "数据安全员", "保障数据安全"),
        ("data-privacy-protector", "数据隐私保护员", "保护数据隐私"),
        ("data-access-controller", "数据访问控制员", "控制数据访问"),
        ("data-security-reporter", "数据安全报告员", "生成数据安全报告"),
    ],
    
    # 系统维护板块（全新）
    "system-monitor-leader": [
        ("system-monitor-exec", "系统监控执行员", "执行系统监控"),
        ("system-status-tracker", "系统状态追踪员", "追踪系统状态"),
        ("system-alert-handler", "系统警报处理员", "处理系统警报"),
        ("system-monitor-reporter", "系统监控报告员", "生成系统监控报告"),
    ],
    "system-maintenance-leader": [
        ("system-maintainer", "系统维护员", "维护系统运行"),
        ("system-cleaner", "系统清理员", "清理系统垃圾"),
        ("system-optimizer-general", "系统优化通用员", "优化系统性能"),
        ("system-maintenance-reporter", "系统维护报告员", "生成系统维护报告"),
    ],
    "system-upgrade-leader": [
        ("system-upgrade-executor", "系统升级执行员", "执行系统升级"),
        ("system-version-updater", "系统版本更新员", "更新系统版本"),
        ("system-compatibility-tester", "系统兼容性测试员", "测试系统兼容性"),
        ("system-upgrade-reporter", "系统升级报告员", "生成系统升级报告"),
    ],
    "system-security-leader": [
        ("system-security-guard", "系统安全员", "保障系统安全"),
        ("system-threat-detector", "系统威胁检测员", "检测系统威胁"),
        ("system-vulnerability-fixer", "系统漏洞修复员", "修复系统漏洞"),
        ("system-security-reporter", "系统安全报告员", "生成系统安全报告"),
    ],
    
    # GEO管理板块（全新）
    "geo-optimizer-leader": [
        ("geo-optimizer-exec", "GEO优化执行员", "执行GEO优化"),
        ("geo-location-optimizer", "地理位置优化员", "优化地理位置"),
        ("geo-targeting-optimizer", "地理定向优化员", "优化地理定向"),
        ("geo-optimization-reporter", "GEO优化报告员", "生成GEO优化报告"),
    ],
    "geo-monitor-leader": [
        ("geo-monitor-exec", "GEO监控执行员", "执行GEO监控"),
        ("geo-performance-tracker", "地理表现追踪员", "追踪地理表现"),
        ("geo-trend-analyzer", "地理趋势分析师", "分析地理趋势"),
        ("geo-monitor-reporter", "GEO监控报告员", "生成GEO监控报告"),
    ],
    "geo-analysis-leader": [
        ("geo-analyzer-exec", "GEO分析执行员", "执行GEO分析"),
        ("geo-data-collector", "地理数据收集员", "收集地理数据"),
        ("geo-pattern-analyzer", "地理模式分析师", "分析地理模式"),
        ("geo-analysis-reporter", "GEO分析报告员", "生成GEO分析报告"),
    ],
    "geo-forecast-leader": [
        ("geo-forecaster", "地理预测员", "预测地理趋势"),
        ("geo-trend-predictor", "地理趋势预测员", "预测地理趋势"),
        ("geo-model-builder", "地理模型构建员", "构建地理预测模型"),
        ("geo-forecast-reporter", "地理预测报告员", "生成地理预测报告"),
    ],
    
    # 技术管理板块（全新）
    "tech-optimizer-leader": [
        ("tech-optimizer-exec", "技术优化执行员", "执行技术优化"),
        ("tech-performance-optimizer", "技术性能优化员", "优化技术性能"),
        ("tech-efficiency-improver", "技术效率提升员", "提升技术效率"),
        ("tech-optimization-reporter", "技术优化报告员", "生成技术优化报告"),
    ],
    "tech-monitor-leader": [
        ("tech-monitor-exec", "技术监控执行员", "执行技术监控"),
        ("tech-status-tracker", "技术状态追踪员", "追踪技术状态"),
        ("tech-alert-handler", "技术警报处理员", "处理技术警报"),
        ("tech-monitor-reporter", "技术监控报告员", "生成技术监控报告"),
    ],
    "tech-upgrade-leader": [
        ("tech-upgrade-executor", "技术升级执行员", "执行技术升级"),
        ("tech-version-updater", "技术版本更新员", "更新技术版本"),
        ("tech-compatibility-tester", "技术兼容性测试员", "测试技术兼容性"),
        ("tech-upgrade-reporter", "技术升级报告员", "生成技术升级报告"),
    ],
    "tech-security-leader": [
        ("tech-security-guard", "技术安全员", "保障技术安全"),
        ("tech-threat-detector", "技术威胁检测员", "检测技术威胁"),
        ("tech-vulnerability-fixer", "技术漏洞修复员", "修复技术漏洞"),
        ("tech-security-reporter", "技术安全报告员", "生成技术安全报告"),
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
    
    for leader_id, staff_list in COMPLETE_BLOCK_STAFF_RULES.items():
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
    print("开始完整批量生成所有执行员工技能...")
    print("=" * 70)
    
    generated, skipped = batch_generate_all()
    
    print("=" * 70)
    print(f"完整批量生成完成！")
    print(f"  - 新生成：{generated} 个执行员工技能")
    print(f"  - 已存在：{len(skipped)} 个执行员工技能")
    print(f"  - 本次处理：{generated + len(skipped)} 个")
    print(f"  - 总板块数：{len(COMPLETE_BLOCK_STAFF_RULES)} 个板块")
    
    if skipped:
        print(f"\n已存在的{len(skipped)}个技能已跳过")