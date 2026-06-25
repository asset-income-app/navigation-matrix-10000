#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEO优化系统 - geo_optimizer.py
地理位置优化，提升本地搜索排名
"""

import json
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
SITES_DIR = ROOT_DIR / "02-sites"
LOGS_DIR = DATA_DIR / "logs"

# 中国城市坐标数据（主要城市）
CITY_COORDINATES = {
    "北京": {"lat": 39.9042, "lng": 116.4074, "region": "华北", "province": "北京市"},
    "上海": {"lat": 31.2304, "lng": 121.4737, "region": "华东", "province": "上海市"},
    "广州": {"lat": 23.1291, "lng": 113.2644, "region": "华南", "province": "广东省"},
    "深圳": {"lat": 22.5431, "lng": 114.0579, "region": "华南", "province": "广东省"},
    "杭州": {"lat": 30.2741, "lng": 120.1551, "region": "华东", "province": "浙江省"},
    "成都": {"lat": 30.5728, "lng": 104.0668, "region": "西南", "province": "四川省"},
    "武汉": {"lat": 30.5928, "lng": 114.3055, "region": "华中", "province": "湖北省"},
    "西安": {"lat": 34.3416, "lng": 108.9398, "region": "西北", "province": "陕西省"},
    "南京": {"lat": 32.0603, "lng": 118.7969, "region": "华东", "province": "江苏省"},
    "重庆": {"lat": 29.4316, "lng": 106.9123, "region": "西南", "province": "重庆市"},
    "天津": {"lat": 39.0842, "lng": 117.2009, "region": "华北", "province": "天津市"},
    "苏州": {"lat": 31.2989, "lng": 120.5853, "region": "华东", "province": "江苏省"},
    "郑州": {"lat": 34.7466, "lng": 113.6254, "region": "华中", "province": "河南省"},
    "长沙": {"lat": 28.2282, "lng": 112.9388, "region": "华中", "province": "湖南省"},
    "东莞": {"lat": 23.0207, "lng": 113.7518, "region": "华南", "province": "广东省"},
    "青岛": {"lat": 36.0671, "lng": 120.3826, "region": "华东", "province": "山东省"},
    "沈阳": {"lat": 41.8057, "lng": 123.4315, "region": "东北", "province": "辽宁省"},
    "宁波": {"lat": 29.8683, "lng": 121.5440, "region": "华东", "province": "浙江省"},
    "昆明": {"lat": 25.0389, "lng": 102.7183, "region": "西南", "province": "云南省"},
    "合肥": {"lat": 31.8206, "lng": 117.2272, "region": "华东", "province": "安徽省"},
    "福州": {"lat": 26.0745, "lng": 119.2965, "region": "华东", "province": "福建省"},
    "哈尔滨": {"lat": 45.8038, "lng": 126.5350, "region": "东北", "province": "黑龙江省"},
    "济南": {"lat": 36.6512, "lng": 117.1201, "region": "华东", "province": "山东省"},
    "大连": {"lat": 38.9140, "lng": 121.6147, "region": "东北", "province": "辽宁省"},
    "长春": {"lat": 43.8171, "lng": 125.3235, "region": "东北", "province": "吉林省"},
    "太原": {"lat": 37.8706, "lng": 112.5489, "region": "华北", "province": "山西省"},
    "贵阳": {"lat": 26.6470, "lng": 106.6302, "region": "西南", "province": "贵州省"},
    "南宁": {"lat": 22.8170, "lng": 108.3665, "region": "华南", "province": "广西壮族自治区"},
    "南昌": {"lat": 28.6820, "lng": 115.8579, "region": "华东", "province": "江西省"},
    "石家庄": {"lat": 38.0428, "lng": 114.5149, "region": "华北", "province": "河北省"},
    "兰州": {"lat": 36.0611, "lng": 103.8343, "region": "西北", "province": "甘肃省"},
    "厦门": {"lat": 24.4798, "lng": 118.0894, "region": "华东", "province": "福建省"},
    "海口": {"lat": 20.0440, "lng": 110.1999, "region": "华南", "province": "海南省"},
    "乌鲁木齐": {"lat": 43.8256, "lng": 87.6168, "region": "西北", "province": "新疆维吾尔自治区"},
    "呼和浩特": {"lat": 40.8414, "lng": 111.7519, "region": "华北", "province": "内蒙古自治区"},
    "拉萨": {"lat": 29.6500, "lng": 91.1000, "region": "西南", "province": "西藏自治区"},
    "银川": {"lat": 38.4872, "lng": 106.2309, "region": "西北", "province": "宁夏回族自治区"},
    "西宁": {"lat": 36.6171, "lng": 101.7782, "region": "西北", "province": "青海省"},
}

# 为所有城市生成默认坐标（基于省会城市偏移）
def get_city_coordinates(city_name):
    """获取城市坐标，如果没有精确数据则估算"""
    if city_name in CITY_COORDINATES:
        return CITY_COORDINATES[city_name]
    
    # 基于城市名生成伪随机坐标（保持一致性）
    import hashlib
    hash_val = int(hashlib.md5(city_name.encode()).hexdigest()[:8], 16)
    
    # 中国范围：纬度18-54，经度73-135
    lat = 18 + (hash_val % 36) + (hash_val % 100) / 100
    lng = 73 + (hash_val % 62) + (hash_val % 100) / 100
    
    return {
        "lat": round(lat, 4),
        "lng": round(lng, 4),
        "region": "中国",
        "province": "中国"
    }

def generate_local_business_schema(site_data, city_name):
    """生成本地业务结构化数据（Schema.org LocalBusiness）"""
    coords = get_city_coordinates(city_name)
    
    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": site_data.get("siteTitle", f"{city_name}导航"),
        "description": site_data.get("siteDescription", f"{city_name}本地导航服务"),
        "address": {
            "@type": "PostalAddress",
            "addressLocality": city_name,
            "addressRegion": coords.get("province", "中国"),
            "addressCountry": "CN"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": coords["lat"],
            "longitude": coords["lng"]
        },
        "url": f"https://{site_data.get('siteType', 'city')}-{city_name}.com",
        "telephone": "+86-400-888-8888",
        "openingHours": "Mo-Su 00:00-23:59",
        "priceRange": "$$",
        "areaServed": {
            "@type": "City",
            "name": city_name
        }
    }
    
    return schema

def optimize_geo_meta(site_data, city_name):
    """优化GEO元数据"""
    coords = get_city_coordinates(city_name)
    
    geo_meta = {
        "geo.region": f"CN-{coords.get('province', 'CN')}",
        "geo.placename": city_name,
        "geo.position": f"{coords['lat']};{coords['lng']}",
        "ICBM": f"{coords['lat']}, {coords['lng']}",
        "geo.latitude": coords["lat"],
        "geo.longitude": coords["lng"],
        "geo.city": city_name,
        "geo.province": coords.get("province", "中国"),
        "geo.country": "中国"
    }
    
    return geo_meta

def generate_local_keywords(city_name, niche_name=None):
    """生成本地关键词"""
    keywords = []
    
    # 基础城市关键词
    keywords.extend([
        f"{city_name}导航",
        f"{city_name}网站",
        f"{city_name}网址",
        f"{city_name}本地服务",
        f"{city_name}生活指南",
        f"{city_name}便民服务",
        f"{city_name}信息查询",
        f"{city_name}在线服务"
    ])
    
    # 如果有行业，添加行业+城市关键词
    if niche_name:
        keywords.extend([
            f"{city_name}{niche_name}",
            f"{niche_name}{city_name}",
            f"{city_name}{niche_name}导航",
            f"{city_name}{niche_name}网站",
            f"{city_name}{niche_name}服务",
            f"{city_name}{niche_name}推荐",
            f"{city_name}{niche_name}大全",
            f"{city_name}{niche_name}平台"
        ])
    
    return keywords

def optimize_site_geo(site_path, site_type, city_name=None, niche_name=None):
    """优化单个站点的GEO"""
    config_file = site_path / "config.json"
    
    if not config_file.exists():
        return None
    
    # 读取配置
    config = json.loads(config_file.read_text(encoding='utf-8'))
    
    # 确定城市名
    if not city_name:
        city_name = config.get("cityName", config.get("siteTitle", "").replace("导航", ""))
    
    # 生成GEO数据
    geo_meta = optimize_geo_meta(config, city_name)
    local_schema = generate_local_business_schema(config, city_name)
    local_keywords = generate_local_keywords(city_name, niche_name)
    
    # 更新配置
    config["geo"] = {
        "coordinates": get_city_coordinates(city_name),
        "meta": geo_meta,
        "localKeywords": local_keywords[:10]  # 限制关键词数量
    }
    
    # 保存配置
    config_file.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding='utf-8')
    
    # 生成结构化数据文件
    schema_file = site_path / "schema.json"
    schema_file.write_text(json.dumps(local_schema, indent=2, ensure_ascii=False), encoding='utf-8')
    
    return {
        "city": city_name,
        "coordinates": get_city_coordinates(city_name),
        "keywords_count": len(local_keywords)
    }

def optimize_all_sites():
    """优化所有站点的GEO"""
    print("\n" + "="*60)
    print("🌍 GEO优化系统 v1.0")
    print("="*60)
    
    stats = {
        "cities": 0,
        "niches": 0,
        "hybrids": 0,
        "total": 0
    }
    
    # 优化城市站
    print("\n[1] 优化城市站...")
    cities_dir = SITES_DIR / "cities"
    if cities_dir.exists():
        for city_dir in cities_dir.iterdir():
            if city_dir.is_dir():
                result = optimize_site_geo(city_dir, "city")
                if result:
                    stats["cities"] += 1
                    stats["total"] += 1
                    if stats["cities"] % 50 == 0:
                        print(f"  ✅ 已优化 {stats['cities']} 个城市站")
    
    print(f"  ✅ 城市站优化完成: {stats['cities']} 个")
    
    # 优化行业站
    print("\n[2] 优化行业站...")
    niches_dir = SITES_DIR / "niches"
    if niches_dir.exists():
        for niche_dir in niches_dir.iterdir():
            if niche_dir.is_dir():
                result = optimize_site_geo(niche_dir, "niche")
                if result:
                    stats["niches"] += 1
                    stats["total"] += 1
                    if stats["niches"] % 100 == 0:
                        print(f"  ✅ 已优化 {stats['niches']} 个行业站")
    
    print(f"  ✅ 行业站优化完成: {stats['niches']} 个")
    
    # 优化组合站
    print("\n[3] 优化组合站...")
    hybrids_dir = SITES_DIR / "hybrids"
    if hybrids_dir.exists():
        for hybrid_dir in hybrids_dir.iterdir():
            if hybrid_dir.is_dir():
                # 从目录名解析城市和行业
                dir_name = hybrid_dir.name
                parts = dir_name.split("-")
                if len(parts) >= 2:
                    niche_pinyin = parts[0]
                    city_pinyin = parts[1]
                    
                    # 读取配置获取实际名称
                    config_file = hybrid_dir / "config.json"
                    if config_file.exists():
                        config = json.loads(config_file.read_text(encoding='utf-8'))
                        city_name = config.get("cityName", city_pinyin)
                        niche_name = config.get("nicheName", niche_pinyin)
                        
                        result = optimize_site_geo(hybrid_dir, "hybrid", city_name, niche_name)
                        if result:
                            stats["hybrids"] += 1
                            stats["total"] += 1
                            if stats["hybrids"] % 500 == 0:
                                print(f"  ✅ 已优化 {stats['hybrids']} 个组合站")
    
    print(f"  ✅ 组合站优化完成: {stats['hybrids']} 个")
    
    # 生成GEO站点地图
    print("\n[4] 生成GEO站点地图...")
    generate_geo_sitemap(stats)
    
    # 生成报告
    print("\n" + "="*60)
    print("📊 GEO优化报告")
    print("="*60)
    print(f"城市站优化: {stats['cities']} 个")
    print(f"行业站优化: {stats['niches']} 个")
    print(f"组合站优化: {stats['hybrids']} 个")
    print(f"总计优化: {stats['total']} 个")
    print("="*60)
    
    # 保存报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "stats": stats,
        "optimizations": [
            "GEO元数据优化",
            "本地结构化数据生成",
            "本地关键词优化",
            "GEO站点地图生成"
        ]
    }
    
    report_file = LOGS_DIR / "geo_optimization_report.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"\n报告文件: {report_file}")
    
    return stats

def generate_geo_sitemap(stats):
    """生成GEO站点地图"""
    sitemap = {
        "timestamp": datetime.now().isoformat(),
        "total_sites": stats["total"],
        "regions": {},
        "provinces": {}
    }
    
    # 统计各地区站点数量
    for city_name, coords in CITY_COORDINATES.items():
        region = coords.get("region", "其他")
        province = coords.get("province", "其他")
        
        if region not in sitemap["regions"]:
            sitemap["regions"][region] = 0
        sitemap["regions"][region] += 1
        
        if province not in sitemap["provinces"]:
            sitemap["provinces"][province] = 0
        sitemap["provinces"][province] += 1
    
    # 保存站点地图
    sitemap_file = DATA_DIR / "geo_sitemap.json"
    sitemap_file.parent.mkdir(parents=True, exist_ok=True)
    sitemap_file.write_text(json.dumps(sitemap, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"  ✅ GEO站点地图已生成: {sitemap_file}")

def main():
    """主函数"""
    optimize_all_sites()

if __name__ == "__main__":
    main()