#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
组合站生成器 - hybrid_generator.py
生成行业×城市组合站，快速扩展到万级规模
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
SITES_DIR = ROOT_DIR / "02-sites" / "hybrids"
TEMPLATES_DIR = ROOT_DIR / "01-templates" / "base"

# 高价值组合（精选167个）
HIGH_VALUE_COMBINATIONS = [
    # 教育培训 × 重点城市
    {"niche": "考研", "city": "北京"},
    {"niche": "考研", "city": "上海"},
    {"niche": "考研", "city": "南京"},
    {"niche": "考研", "city": "武汉"},
    {"niche": "考研", "city": "西安"},
    {"niche": "公务员", "city": "北京"},
    {"niche": "公务员", "city": "上海"},
    {"niche": "公务员", "city": "广州"},
    {"niche": "公务员", "city": "深圳"},
    {"niche": "雅思", "city": "北京"},
    {"niche": "雅思", "city": "上海"},
    {"niche": "雅思", "city": "广州"},
    {"niche": "托福", "city": "北京"},
    {"niche": "托福", "city": "上海"},
    {"niche": "编程", "city": "北京"},
    {"niche": "编程", "city": "上海"},
    {"niche": "编程", "city": "深圳"},
    {"niche": "编程", "city": "杭州"},
    {"niche": "Python", "city": "北京"},
    {"niche": "Python", "city": "上海"},
    {"niche": "Python", "city": "深圳"},
    {"niche": "Java", "city": "北京"},
    {"niche": "Java", "city": "上海"},
    {"niche": "Java", "city": "深圳"},
    
    # 健康医疗 × 重点城市
    {"niche": "中医", "city": "北京"},
    {"niche": "中医", "city": "上海"},
    {"niche": "中医", "city": "广州"},
    {"niche": "养生", "city": "北京"},
    {"niche": "养生", "city": "上海"},
    {"niche": "养生", "city": "成都"},
    {"niche": "健身", "city": "北京"},
    {"niche": "健身", "city": "上海"},
    {"niche": "健身", "city": "深圳"},
    {"niche": "瑜伽", "city": "北京"},
    {"niche": "瑜伽", "city": "上海"},
    {"niche": "瑜伽", "city": "成都"},
    {"niche": "美容", "city": "北京"},
    {"niche": "美容", "city": "上海"},
    {"niche": "美容", "city": "广州"},
    {"niche": "医美", "city": "北京"},
    {"niche": "医美", "city": "上海"},
    {"niche": "医美", "city": "成都"},
    
    # 生活服务 × 重点城市
    {"niche": "搬家", "city": "北京"},
    {"niche": "搬家", "city": "上海"},
    {"niche": "搬家", "city": "广州"},
    {"niche": "搬家", "city": "深圳"},
    {"niche": "家政", "city": "北京"},
    {"niche": "家政", "city": "上海"},
    {"niche": "家政", "city": "广州"},
    {"niche": "家政", "city": "深圳"},
    {"niche": "装修", "city": "北京"},
    {"niche": "装修", "city": "上海"},
    {"niche": "装修", "city": "广州"},
    {"niche": "装修", "city": "深圳"},
    {"niche": "婚庆", "city": "北京"},
    {"niche": "婚庆", "city": "上海"},
    {"niche": "婚庆", "city": "广州"},
    {"niche": "摄影", "city": "北京"},
    {"niche": "摄影", "city": "上海"},
    {"niche": "摄影", "city": "成都"},
    {"niche": "宠物", "city": "北京"},
    {"niche": "宠物", "city": "上海"},
    {"niche": "宠物", "city": "广州"},
    {"niche": "母婴", "city": "北京"},
    {"niche": "母婴", "city": "上海"},
    {"niche": "母婴", "city": "广州"},
    
    # 财经金融 × 重点城市
    {"niche": "投资", "city": "北京"},
    {"niche": "投资", "city": "上海"},
    {"niche": "投资", "city": "深圳"},
    {"niche": "理财", "city": "北京"},
    {"niche": "理财", "city": "上海"},
    {"niche": "理财", "city": "深圳"},
    {"niche": "股票", "city": "北京"},
    {"niche": "股票", "city": "上海"},
    {"niche": "股票", "city": "深圳"},
    {"niche": "基金", "city": "北京"},
    {"niche": "基金", "city": "上海"},
    {"niche": "基金", "city": "深圳"},
    {"niche": "保险", "city": "北京"},
    {"niche": "保险", "city": "上海"},
    {"niche": "保险", "city": "广州"},
    {"niche": "贷款", "city": "北京"},
    {"niche": "贷款", "city": "上海"},
    {"niche": "贷款", "city": "深圳"},
    
    # 科技互联网 × 重点城市
    {"niche": "人工智能", "city": "北京"},
    {"niche": "人工智能", "city": "上海"},
    {"niche": "人工智能", "city": "深圳"},
    {"niche": "大数据", "city": "北京"},
    {"niche": "大数据", "city": "上海"},
    {"niche": "大数据", "city": "深圳"},
    {"niche": "云计算", "city": "北京"},
    {"niche": "云计算", "city": "上海"},
    {"niche": "云计算", "city": "深圳"},
    {"niche": "区块链", "city": "北京"},
    {"niche": "区块链", "city": "上海"},
    {"niche": "区块链", "city": "深圳"},
    {"niche": "SEO", "city": "北京"},
    {"niche": "SEO", "city": "上海"},
    {"niche": "SEO", "city": "广州"},
    {"niche": "小程序", "city": "北京"},
    {"niche": "小程序", "city": "上海"},
    {"niche": "小程序", "city": "深圳"},
    
    # 文化娱乐 × 重点城市
    {"niche": "音乐", "city": "北京"},
    {"niche": "音乐", "city": "上海"},
    {"niche": "音乐", "city": "成都"},
    {"niche": "影视", "city": "北京"},
    {"niche": "影视", "city": "上海"},
    {"niche": "影视", "city": "广州"},
    {"niche": "游戏", "city": "北京"},
    {"niche": "游戏", "city": "上海"},
    {"niche": "游戏", "city": "深圳"},
    {"niche": "旅游", "city": "北京"},
    {"niche": "旅游", "city": "上海"},
    {"niche": "旅游", "city": "成都"},
    {"niche": "美食", "city": "北京"},
    {"niche": "美食", "city": "上海"},
    {"niche": "美食", "city": "广州"},
    {"niche": "美食", "city": "成都"},
    {"niche": "摄影", "city": "北京"},
    {"niche": "摄影", "city": "上海"},
    {"niche": "摄影", "city": "成都"},
    
    # 商务职场 × 重点城市
    {"niche": "求职", "city": "北京"},
    {"niche": "求职", "city": "上海"},
    {"niche": "求职", "city": "深圳"},
    {"niche": "招聘", "city": "北京"},
    {"niche": "招聘", "city": "上海"},
    {"niche": "招聘", "city": "深圳"},
    {"niche": "创业", "city": "北京"},
    {"niche": "创业", "city": "上海"},
    {"niche": "创业", "city": "深圳"},
    {"niche": "专利", "city": "北京"},
    {"niche": "专利", "city": "上海"},
    {"niche": "专利", "city": "深圳"},
    {"niche": "商标", "city": "北京"},
    {"niche": "商标", "city": "上海"},
    {"niche": "商标", "city": "广州"},
    
    # 交通汽车 × 重点城市
    {"niche": "汽车", "city": "北京"},
    {"niche": "汽车", "city": "上海"},
    {"niche": "汽车", "city": "广州"},
    {"niche": "驾照", "city": "北京"},
    {"niche": "驾照", "city": "上海"},
    {"niche": "驾照", "city": "广州"},
    {"niche": "二手车", "city": "北京"},
    {"niche": "二手车", "city": "上海"},
    {"niche": "二手车", "city": "广州"},
    
    # 房产家居 × 重点城市
    {"niche": "房产", "city": "北京"},
    {"niche": "房产", "city": "上海"},
    {"niche": "房产", "city": "深圳"},
    {"niche": "买房", "city": "北京"},
    {"niche": "买房", "city": "上海"},
    {"niche": "买房", "city": "深圳"},
    {"niche": "租房", "city": "北京"},
    {"niche": "租房", "city": "上海"},
    {"niche": "租房", "city": "深圳"},
    {"niche": "装修", "city": "北京"},
    {"niche": "装修", "city": "上海"},
    {"niche": "装修", "city": "广州"},
    {"niche": "家具", "city": "北京"},
    {"niche": "家具", "city": "上海"},
    {"niche": "家具", "city": "广州"},
    
    # 社交媒体 × 重点城市
    {"niche": "微信运营", "city": "北京"},
    {"niche": "微信运营", "city": "上海"},
    {"niche": "微信运营", "city": "深圳"},
    {"niche": "抖音", "city": "北京"},
    {"niche": "抖音", "city": "上海"},
    {"niche": "抖音", "city": "广州"},
    {"niche": "小红书", "city": "北京"},
    {"niche": "小红书", "city": "上海"},
    {"niche": "小红书", "city": "杭州"},
    
    # 综合其他 × 重点城市
    {"niche": "PPT", "city": "北京"},
    {"niche": "PPT", "city": "上海"},
    {"niche": "PPT", "city": "深圳"},
    {"niche": "Excel", "city": "北京"},
    {"niche": "Excel", "city": "上海"},
    {"niche": "Excel", "city": "深圳"},
    {"niche": "Word", "city": "北京"},
    {"niche": "Word", "city": "上海"},
    {"niche": "Word", "city": "广州"},
]

def get_template_variant(name):
    """根据名称分配模板变体"""
    VARIANTS = ['variant-blue', 'variant-green', 'variant-orange', 'variant-purple', 'variant-dark']
    hash_val = sum(ord(c) for c in name)
    return VARIANTS[hash_val % len(VARIANTS)]

def create_hybrid_config(niche_name, city_name):
    """创建组合站配置"""
    site_name = f"{niche_name}-{city_name}"
    site_pinyin = f"{niche_name.lower()}-{city_name.lower()}"
    
    config = {
        "siteType": "hybrid",
        "nicheName": niche_name,
        "cityName": city_name,
        "siteTitle": f"{city_name}{niche_name}导航 - {city_name}{niche_name}最全网站导航",
        "siteDescription": f"{city_name}{niche_name}导航站，汇集{city_name}{niche_name}最优质的官方网站和资源，一站式满足您的所有需求。",
        "variant": get_template_variant(site_name),
        "contact": {
            "email": "931249697@qq.com",
            "qq": "931249697"
        },
        "categories": [
            {
                "name": "本地服务",
                "links": [
                    {"name": f"{city_name}{niche_name}搜索", "url": f"https://www.baidu.com/s?wd={city_name}{niche_name}", "desc": f"搜索{city_name}{niche_name}相关信息"},
                    {"name": "美团", "url": "https://www.meituan.com/", "desc": f"{city_name}本地服务"},
                    {"name": "58同城", "url": "https://www.58.com/", "desc": f"{city_name}本地信息"}
                ]
            },
            {
                "name": "学习资源",
                "links": [
                    {"name": "知乎", "url": "https://www.zhihu.com/", "desc": f"{niche_name}经验问答"},
                    {"name": "B站", "url": f"https://search.bilibili.com/all?keyword={niche_name}", "desc": f"{niche_name}视频教程"},
                    {"name": "小红书", "url": "https://www.xiaohongshu.com/", "desc": f"{niche_name}经验分享"}
                ]
            },
            {
                "name": "工具平台",
                "links": [
                    {"name": "百度搜索", "url": f"https://www.baidu.com/s?wd={niche_name}工具", "desc": f"搜索{niche_name}相关工具"},
                    {"name": "知乎推荐", "url": "https://www.zhihu.com/", "desc": f"{niche_name}工具推荐"}
                ]
            },
            {
                "name": "社区交流",
                "links": [
                    {"name": "知乎", "url": "https://www.zhihu.com/", "desc": f"{niche_name}交流社区"},
                    {"name": "豆瓣", "url": "https://www.douban.com/", "desc": f"{niche_name}分享社区"},
                    {"name": "贴吧", "url": "https://tieba.baidu.com/", "desc": f"{niche_name}贴吧"}
                ]
            },
            {
                "name": "资讯动态",
                "links": [
                    {"name": "人民网", "url": "http://www.people.com.cn/", "desc": "新闻资讯"},
                    {"name": "新华网", "url": "http://www.xinhuanet.com/", "desc": "新闻资讯"},
                    {"name": "微博", "url": f"https://s.weibo.com/weibo?q={niche_name}", "desc": f"{niche_name}热门话题"}
                ]
            },
            {
                "name": "综合平台",
                "links": [
                    {"name": "百度搜索", "url": f"https://www.baidu.com/s?wd={city_name}{niche_name}", "desc": f"搜索{city_name}{niche_name}相关信息"},
                    {"name": "B站视频", "url": f"https://search.bilibili.com/all?keyword={city_name}{niche_name}", "desc": f"{city_name}{niche_name}视频教程"},
                    {"name": "微博", "url": f"https://s.weibo.com/weibo?q={city_name}{niche_name}", "desc": f"{city_name}{niche_name}热门话题"}
                ]
            }
        ]
    }
    return config, site_pinyin

def generate_hybrid_site(niche_name, city_name):
    """生成组合站文件"""
    config, site_pinyin = create_hybrid_config(niche_name, city_name)
    
    site_dir = SITES_DIR / site_pinyin
    site_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建config.json
    (site_dir / "config.json").write_text(json.dumps(config, indent=2))
    
    # 复制模板文件
    for template_file in ['style.css', 'script.js']:
        shutil.copy(TEMPLATES_DIR / template_file, site_dir / template_file)
    
    # 生成index.html
    template_html = (TEMPLATES_DIR / "index.html").read_text()
    config_script = f'<script>window.__SITE_CONFIG__ = {json.dumps(config)};</script>'
    html = template_html.replace('</head>', config_script + '</head>')
    html = html.replace('<title>导航站</title>', f'<title>{config["siteTitle"]}</title>')
    (site_dir / "index.html").write_text(html)
    
    # 生成SEO文件
    (site_dir / "robots.txt").write_text(f"""User-agent: *
Allow: /
Sitemap: https://{site_pinyin}-nav.pages.dev/sitemap.xml
""")
    
    (site_dir / "sitemap.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://{site_pinyin}-nav.pages.dev/</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
""")
    
    (site_dir / "_headers").write_text("""/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
""")
    
    return site_dir

def generate_hybrid_sites(target_count=167):
    """生成组合站"""
    print("\n" + "="*60)
    print(f"🔗 组合站生成器 - 目标: {target_count} 个组合站")
    print("="*60)
    
    # 获取现有组合站
    existing_hybrids = [d.name for d in SITES_DIR.iterdir() if d.is_dir()]
    existing_count = len(existing_hybrids)
    
    print(f"现有组合站: {existing_count} 个")
    print(f"目标组合站: {target_count} 个")
    print(f"需要新增: {target_count - existing_count} 个")
    
    # 计算需要新增的数量
    needed = target_count - existing_count
    
    # 直接从城市和行业数据中动态组合
    # 加载城市和行业数据
    cities_data = json.loads((ROOT_DIR / "data" / "cities.json").read_text()) if (ROOT_DIR / "data" / "cities.json").exists() else []
    niches_data = json.loads((ROOT_DIR / "data" / "niches.json").read_text()) if (ROOT_DIR / "data" / "niches.json").exists() else []
    
    # 动态生成组合
    combinations_to_add = []
    for niche in niches_data[:150]:  # 取前150个行业
        for city in cities_data[:100]:  # 取前100个城市
            niche_name = niche.get("nicheName", "")
            city_name = city.get("cityName", "")
            if niche_name and city_name:
                site_name = f"{niche_name}-{city_name}"
                if site_name not in existing_hybrids and site_name not in [f"{c['niche']}-{c['city']}" for c in combinations_to_add]:
                    combinations_to_add.append({"niche": niche_name, "city": city_name})
                    if len(combinations_to_add) >= needed:
                        break
        if len(combinations_to_add) >= needed:
            break
    
    # 限制到需要的数量
    combinations_to_add = combinations_to_add[:needed]
    
    print(f"\n开始生成 {len(combinations_to_add)} 个新组合站...")
    
    created = 0
    for combo in combinations_to_add:
        generate_hybrid_site(combo["niche"], combo["city"])
        created += 1
        print(f"  ✅ {combo['niche']} × {combo['city']}")
    
    print("\n" + "="*60)
    print(f"✅ 生成完成: 新增 {created} 个组合站")
    print(f"当前总数: {existing_count + created} 个")
    print("="*60)

def show_hybrid_stats():
    """显示组合站统计"""
    existing_count = sum(1 for d in SITES_DIR.iterdir() if d.is_dir())
    
    print("\n" + "="*60)
    print("📊 组合站统计")
    print("="*60)
    print(f"当前组合站: {existing_count} 个")
    print(f"目标组合站: 167 个（首批）")
    print(f"进度: {existing_count / 167 * 100:.1f}%")

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "generate":
            target = int(sys.argv[2]) if len(sys.argv) > 2 else 167
            generate_hybrid_sites(target)
        elif command == "stats":
            show_hybrid_stats()
        elif command == "custom":
            if len(sys.argv) >= 4:
                niche = sys.argv[2]
                city = sys.argv[3]
                generate_hybrid_site(niche, city)
                print(f"✅ 已生成: {niche} × {city}")
        else:
            print("用法: python hybrid_generator.py [generate|stats|custom]")
    else:
        # 默认生成167个
        generate_hybrid_sites(167)

if __name__ == "__main__":
    main()