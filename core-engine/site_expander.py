"""
站点扩展脚本
从5000站点扩展至10000站点
"""

import json
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(r"E:\50\navigation-matrix-unified")
DATA_DIR = ROOT_DIR / "data"

# 加载现有数据
CITIES_FILE = DATA_DIR / "cities.json"
NICHES_FILE = DATA_DIR / "niches.json"
HYBRIDS_FILE = DATA_DIR / "hybrids.json"

def load_existing_data():
    """加载现有站点数据"""
    print("加载现有站点数据...")
    
    cities = []
    niches = []
    hybrids = []
    
    if CITIES_FILE.exists():
        with open(CITIES_FILE, 'r', encoding='utf-8') as f:
            cities = json.load(f)
        print(f"城市站：{len(cities)}个")
    
    if NICHES_FILE.exists():
        with open(NICHES_FILE, 'r', encoding='utf-8') as f:
            niches = json.load(f)
        print(f"行业站：{len(niches)}个")
    
    if HYBRIDS_FILE.exists():
        with open(HYBRIDS_FILE, 'r', encoding='utf-8') as f:
            hybrids = json.load(f)
        print(f"组合站：{len(hybrids)}个")
    
    total = len(cities) + len(niches) + len(hybrids)
    print(f"总站点：{total}个")
    
    return cities, niches, hybrids

def generate_more_hybrids(cities, niches, existing_hybrids):
    """生成更多组合站"""
    print("\n生成更多组合站数据...")
    
    # 目标：从4207扩展至9000+
    target_count = 9000
    current_count = len(existing_hybrids)
    
    if current_count >= target_count:
        print(f"组合站已达目标：{current_count}个")
        return existing_hybrids
    
    needed_count = target_count - current_count
    print(f"需要生成：{needed_count}个新组合站")
    
    new_hybrids = []
    
    # 简化的生成逻辑：随机组合城市和行业
    for i in range(needed_count):
        city_index = i % len(cities)
        niche_index = i % len(niches)
        
        city = cities[city_index]
        niche = niches[niche_index]
        
        # 创建新的组合站
        hybrid = {
            "id": f"hybrid_{current_count + i + 1}",
            "city": city.get("city", "未知城市"),
            "niche": niche.get("niche", "未知行业"),
            "title": f"{city.get('city', '未知城市')}{niche.get('niche', '未知行业')}导航",
            "description": f"{city.get('city', '未知城市')}{niche.get('niche', '未知行业')}专业导航网站",
            "keywords": [
                city.get("city", "未知城市"),
                niche.get("niche", "未知行业"),
                f"{city.get('city', '未知城市')}{niche.get('niche', '未知行业')}"
            ],
            "priority": "medium",
            "created_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        new_hybrids.append(hybrid)
    
    print(f"已生成：{len(new_hybrids)}个新组合站")
    
    # 合并现有和新组合站
    all_hybrids = existing_hybrids + new_hybrids
    print(f"总组合站：{len(all_hybrids)}个")
    
    return all_hybrids

def save_expanded_data(hybrids):
    """保存扩展后的数据"""
    print("\n保存扩展后的数据...")
    
    with open(HYBRIDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(hybrids, f, indent=2, ensure_ascii=False)
    
    print(f"已保存：{HYBRIDS_FILE}")
    print(f"总组合站数：{len(hybrids)}个")

def calculate_expansion_summary(cities, niches, hybrids):
    """计算扩展后的总结"""
    print("\n扩展总结：")
    print("=" * 60)
    
    total_sites = len(cities) + len(niches) + len(hybrids)
    
    print(f"城市站：{len(cities)}个")
    print(f"行业站：{len(niches)}个")
    print(f"组合站：{len(hybrids)}个")
    print(f"总站点：{total_sites}个")
    
    # 计算流量和收入潜力增长
    # 简化的估算：假设每1000站点增加32.5M访问/年和1.4M收入/年
    
    added_sites = total_sites - 5000  # 从5000扩展
    
    added_traffic = added_sites * 32500  # 32.5M访问/年 per 1000站点
    added_revenue = added_sites * 1400   # 1.4M收入/年 per 1000站点
    
    print(f"\n扩展增长：")
    print(f"新增站点：{added_sites}个")
    print(f"新增年流量：{added_traffic:,}访问")
    print(f"新增年收入：{added_revenue:,}元")
    
    print("=" * 60)

def main():
    """主函数"""
    print("开始站点扩展工作...")
    print(f"扩展时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # 加载现有数据
    cities, niches, hybrids = load_existing_data()
    
    # 生成更多组合站
    expanded_hybrids = generate_more_hybrids(cities, niches, hybrids)
    
    # 保存扩展数据
    save_expanded_data(expanded_hybrids)
    
    # 计算扩展总结
    calculate_expansion_summary(cities, niches, expanded_hybrids)
    
    print("=" * 70)
    print("站点扩展工作完成！")

if __name__ == "__main__":
    main()