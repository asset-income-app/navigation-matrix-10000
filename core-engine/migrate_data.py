#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据迁移脚本 - 将现有两个项目的站点数据迁移到统一项目
"""

import json
import os
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
SITES_DIR = ROOT_DIR / "02-sites"

# 源项目路径
V3_DIR = Path("e:/50/navigation-matrix-v3")
V1_DIR = Path("e:/50/vertical-navigation-matrix-v1")


def migrate_cities():
    """迁移城市站数据"""
    print("[1] 迁移城市站数据...")
    cities_data = []
    cities_source = V3_DIR / "02-city-sites"

    if not cities_source.exists():
        print(f"  [!] 源目录不存在: {cities_source}")
        return

    count = 0
    for city_dir in sorted(cities_source.iterdir()):
        if not city_dir.is_dir() or city_dir.name.startswith('.'):
            continue

        config_file = city_dir / "config.json"
        if not config_file.exists():
            continue

        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 添加siteType
        config['siteType'] = 'city'

        cities_data.append(config)

        # 复制到目标目录
        target_dir = SITES_DIR / "cities" / city_dir.name
        os.makedirs(target_dir, exist_ok=True)
        with open(target_dir / "config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        count += 1

    # 保存统一数据
    save_json(DATA_DIR / "cities.json", cities_data)
    print(f"  [OK] 迁移了 {count} 个城市站")


def migrate_niches():
    """迁移行业站数据"""
    print("[2] 迁移行业站数据...")
    niches_data = []
    niches_source = V1_DIR / "02-niche-sites"

    if not niches_source.exists():
        print(f"  [!] 源目录不存在: {niches_source}")
        return

    count = 0
    for niche_dir in sorted(niches_source.iterdir()):
        if not niche_dir.is_dir() or niche_dir.name.startswith('.'):
            continue

        config_file = niche_dir / "config.json"
        if not config_file.exists():
            continue

        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 添加siteType
        config['siteType'] = 'niche'

        niches_data.append(config)

        # 复制到目标目录
        target_dir = SITES_DIR / "niches" / niche_dir.name
        os.makedirs(target_dir, exist_ok=True)
        with open(target_dir / "config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        count += 1

    # 保存统一数据
    save_json(DATA_DIR / "niches.json", niches_data)
    print(f"  [OK] 迁移了 {count} 个行业站")


def create_master_links():
    """创建统一链接库"""
    print("[3] 创建统一链接库...")

    master_links = {
        "official": [
            {"name": "中国政府网", "url": "https://www.gov.cn/"},
            {"name": "国家政务服务", "url": "https://www.gov.cn/fuwu/"}
        ],
        "platforms": [
            {"name": "百度", "url": "https://www.baidu.com/"},
            {"name": "微信", "url": "https://weixin.qq.com/"},
            {"name": "支付宝", "url": "https://www.alipay.com/"},
            {"name": "淘宝", "url": "https://www.taobao.com/"},
            {"name": "京东", "url": "https://www.jd.com/"},
            {"name": "美团", "url": "https://www.meituan.com/"},
            {"name": "大众点评", "url": "https://www.dianping.com/"},
            {"name": "58同城", "url": "https://www.58.com/"},
            {"name": "携程旅行", "url": "https://www.ctrip.com/"},
            {"name": "高德地图", "url": "https://www.amap.com/"},
            {"name": "百度地图", "url": "https://map.baidu.com/"}
        ],
        "tools": [
            {"name": "ChatGPT", "url": "https://chat.openai.com/"},
            {"name": "文心一言", "url": "https://yiyan.baidu.com/"},
            {"name": "通义千问", "url": "https://tongyi.aliyun.com/"},
            {"name": "Kimi", "url": "https://kimi.moonshot.cn/"},
            {"name": "豆包", "url": "https://www.doubao.com/"}
        ],
        "emergency": [
            {"name": "报警电话 110", "url": "tel:110"},
            {"name": "急救电话 120", "url": "tel:120"},
            {"name": "火警电话 119", "url": "tel:119"},
            {"name": "交通事故 122", "url": "tel:122"},
            {"name": "消费者投诉 12315", "url": "tel:12315"},
            {"name": "政务服务热线 12345", "url": "tel:12345"}
        ],
        "education": [
            {"name": "学信网", "url": "https://www.chsi.com.cn/"},
            {"name": "中国教育考试网", "url": "https://www.neea.edu.cn/"},
            {"name": "中国大学MOOC", "url": "https://www.icourse163.org/"},
            {"name": "国家中小学智慧教育", "url": "https://www.zxx.edu.cn/"},
            {"name": "中国知网", "url": "https://www.cnki.net/"}
        ],
        "finance": [
            {"name": "中国工商银行", "url": "https://www.icbc.com.cn/"},
            {"name": "中国建设银行", "url": "https://www.ccb.com/"},
            {"name": "中国农业银行", "url": "https://www.abchina.com/"},
            {"name": "中国银行", "url": "https://www.boc.cn/"},
            {"name": "招商银行", "url": "https://www.cmbchina.com/"},
            {"name": "东方财富", "url": "https://www.eastmoney.com/"},
            {"name": "同花顺", "url": "https://www.10jqka.com.cn/"}
        ],
        "media": [
            {"name": "人民网", "url": "http://www.people.com.cn/"},
            {"name": "新华网", "url": "http://www.xinhuanet.com/"},
            {"name": "央视新闻", "url": "https://news.cctv.com/"},
            {"name": "今日头条", "url": "https://www.toutiao.com/"},
            {"name": "腾讯新闻", "url": "https://news.qq.com/"}
        ]
    }

    save_json(DATA_DIR / "master-links.json", master_links)
    print(f"  [OK] 统一链接库已创建 ({sum(len(v) for v in master_links.values())}条链接)")


def create_template_assignment():
    """创建模板分配记录"""
    print("[4] 创建模板分配记录...")
    import hashlib

    variants = ['variant-blue', 'variant-green', 'variant-orange', 'variant-purple', 'variant-dark']
    assignment = {}

    # 加载城市和行业数据
    cities = load_json(DATA_DIR / "cities.json") or []
    niches = load_json(DATA_DIR / "niches.json") or []

    for city in cities:
        pinyin = city.get('cityPinyin', '')
        if pinyin:
            hash_val = int(hashlib.md5(pinyin.encode()).hexdigest(), 16)
            assignment[f"city/{pinyin}"] = variants[hash_val % len(variants)]

    for niche in niches:
        pinyin = niche.get('nichePinyin', '')
        if pinyin:
            hash_val = int(hashlib.md5(pinyin.encode()).hexdigest(), 16)
            assignment[f"niche/{pinyin}"] = variants[hash_val % len(variants)]

    save_json(DATA_DIR / "template-assignment.json", assignment)
    print(f"  [OK] 模板分配已创建 ({len(assignment)}个站点)")


def save_json(filepath, data):
    """保存JSON"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(filepath):
    """加载JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def main():
    print("=" * 60)
    print("  数据迁移工具 v1.0")
    print("=" * 60)
    print()

    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(SITES_DIR / "cities", exist_ok=True)
    os.makedirs(SITES_DIR / "niches", exist_ok=True)
    os.makedirs(SITES_DIR / "hybrids", exist_ok=True)

    migrate_cities()
    print()
    migrate_niches()
    print()
    create_master_links()
    print()
    create_template_assignment()
    print()

    print("=" * 60)
    print("  迁移完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
