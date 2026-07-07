#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
收入分析脚本 - 分析站点收入潜力，生成收入报告
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"

def analyze_revenue_potential():
    """分析收入潜力"""
    print("=" * 60)
    print("收入潜力分析报告")
    print("=" * 60)
    print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 站点数量统计
    cities_file = DATA_DIR / 'cities.json'
    niches_file = DATA_DIR / 'niches.json'
    hybrids_file = DATA_DIR / 'hybrids.json'
    
    city_count = 0
    niche_count = 0
    hybrid_count = 0
    
    if cities_file.exists():
        with open(cities_file, 'r', encoding='utf-8') as f:
            cities = json.load(f)
            city_count = len(cities)
    
    if niches_file.exists():
        with open(niches_file, 'r', encoding='utf-8') as f:
            niches = json.load(f)
            niche_count = len(niches)
    
    if hybrids_file.exists():
        with open(hybrids_file, 'r', encoding='utf-8') as f:
            hybrids = json.load(f)
            hybrid_count = len(hybrids)
    
    total_sites = city_count + niche_count + hybrid_count
    
    print("站点数量统计:")
    print("-" * 60)
    print(f"城市站: {city_count}个")
    print(f"行业站: {niche_count}个")
    print(f"组合站: {hybrid_count}个")
    print(f"总站点: {total_sites}个")
    print()
    
    # 收入来源分析
    print("收入来源分析:")
    print("-" * 60)
    
    # 广告收入估算
    # 城市站：每个站平均广告收入 50-200元/月
    city_ad_revenue = city_count * 100
    # 行业站：每个站平均广告收入 30-100元/月
    niche_ad_revenue = niche_count * 50
    # 组合站：每个站平均广告收入 20-80元/月
    hybrid_ad_revenue = hybrid_count * 40
    
    total_ad_revenue = city_ad_revenue + niche_ad_revenue + hybrid_ad_revenue
    
    print(f"广告收入估算:")
    print(f"  城市站广告收入: {city_ad_revenue}元/月")
    print(f"  行业站广告收入: {niche_ad_revenue}元/月")
    print(f"  组合站广告收入: {hybrid_ad_revenue}元/月")
    print(f"  总广告收入: {total_ad_revenue}元/月")
    print(f"  年广告收入: {total_ad_revenue * 12}元")
    print()
    
    # 联盟收入估算
    # 城市站：每个站平均联盟收入 30-100元/月
    city_affiliate_revenue = city_count * 60
    # 行业站：每个站平均联盟收入 50-150元/月
    niche_affiliate_revenue = niche_count * 80
    # 组合站：每个站平均联盟收入 20-60元/月
    hybrid_affiliate_revenue = hybrid_count * 30
    
    total_affiliate_revenue = city_affiliate_revenue + niche_affiliate_revenue + hybrid_affiliate_revenue
    
    print(f"联盟收入估算:")
    print(f"  城市站联盟收入: {city_affiliate_revenue}元/月")
    print(f"  行业站联盟收入: {niche_affiliate_revenue}元/月")
    print(f"  组合站联盟收入: {hybrid_affiliate_revenue}元/月")
    print(f"  总联盟收入: {total_affiliate_revenue}元/月")
    print(f"  年联盟收入: {total_affiliate_revenue * 12}元")
    print()
    
    # 商品销售收入估算
    # 城市站：每个站平均商品收入 20-80元/月
    city_product_revenue = city_count * 40
    # 行业站：每个站平均商品收入 30-100元/月
    niche_product_revenue = niche_count * 50
    # 组合站：每个站平均商品收入 10-40元/月
    hybrid_product_revenue = hybrid_count * 20
    
    total_product_revenue = city_product_revenue + niche_product_revenue + hybrid_product_revenue
    
    print(f"商品销售收入估算:")
    print(f"  城市站商品收入: {city_product_revenue}元/月")
    print(f"  行业站商品收入: {niche_product_revenue}元/月")
    print(f"  组合站商品收入: {hybrid_product_revenue}元/月")
    print(f"  总商品收入: {total_product_revenue}元/月")
    print(f"  年商品收入: {total_product_revenue * 12}元")
    print()
    
    # 服务收入估算
    # 城市站：每个站平均服务收入 10-40元/月
    city_service_revenue = city_count * 20
    # 行业站：每个站平均服务收入 20-80元/月
    niche_service_revenue = niche_count * 30
    # 组合站：每个站平均服务收入 5-20元/月
    hybrid_service_revenue = hybrid_count * 10
    
    total_service_revenue = city_service_revenue + niche_service_revenue + hybrid_service_revenue
    
    print(f"服务收入估算:")
    print(f"  城市站服务收入: {city_service_revenue}元/月")
    print(f"  行业站服务收入: {niche_service_revenue}元/月")
    print(f"  组合站服务收入: {hybrid_service_revenue}元/月")
    print(f"  总服务收入: {total_service_revenue}元/月")
    print(f"  年服务收入: {total_service_revenue * 12}元")
    print()
    
    # 总收入估算
    total_monthly_revenue = total_ad_revenue + total_affiliate_revenue + total_product_revenue + total_service_revenue
    total_yearly_revenue = total_monthly_revenue * 12
    
    print("总收入估算:")
    print("-" * 60)
    print(f"月总收入: {total_monthly_revenue}元")
    print(f"年总收入: {total_yearly_revenue}元")
    print()
    
    # 收入来源占比分析
    print("收入来源占比分析:")
    print("-" * 60)
    ad_percentage = (total_ad_revenue / total_monthly_revenue) * 100
    affiliate_percentage = (total_affiliate_revenue / total_monthly_revenue) * 100
    product_percentage = (total_product_revenue / total_monthly_revenue) * 100
    service_percentage = (total_service_revenue / total_monthly_revenue) * 100
    
    print(f"广告收入占比: {ad_percentage:.1f}%")
    print(f"联盟收入占比: {affiliate_percentage:.1f}%")
    print(f"商品销售占比: {product_percentage:.1f}%")
    print(f"服务收入占比: {service_percentage:.1f}%")
    print()
    
    # 收入优化建议
    print("收入优化建议:")
    print("-" * 60)
    print("1. 广告优化：增加广告位，优化广告类型，提升广告收入")
    print("2. 联盟优化：增加联盟产品，优化转化路径，提升联盟收入")
    print("3. 商品优化：增加商品种类，优化商品展示，提升商品收入")
    print("4. 服务优化：增加服务项目，优化服务质量，提升服务收入")
    print("5. 站点扩展：增加站点数量，扩大收入来源，提升总收入")
    print()
    
    # 收入增长预测
    print("收入增长预测:")
    print("-" * 60)
    print("保守预测（10%增长）：")
    print(f"  月收入: {total_monthly_revenue * 1.1:.0f}元")
    print(f"  年收入: {total_yearly_revenue * 1.1:.0f}元")
    print()
    print("正常预测（20%增长）：")
    print(f"  月收入: {total_monthly_revenue * 1.2:.0f}元")
    print(f"  年收入: {total_yearly_revenue * 1.2:.0f}元")
    print()
    print("乐观预测（50%增长）：")
    print(f"  月收入: {total_monthly_revenue * 1.5:.0f}元")
    print(f"  年收入: {total_yearly_revenue * 1.5:.0f}元")
    print()
    
    print("=" * 60)
    print("收入分析报告完成")
    print("=" * 60)

def main():
    """主函数"""
    analyze_revenue_potential()

if __name__ == '__main__':
    main()