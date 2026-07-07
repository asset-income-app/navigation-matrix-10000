#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
站点内容扩充引擎 - 为所有站点添加丰富的链接内容
"""

import json
import random
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
SITES_DIR = ROOT_DIR / "02-sites"
DATA_DIR = ROOT_DIR / "data"

# ==================== 基础链接库 ====================

BASE_CATEGORIES = {
    "政务服务": {
        "icon": "🏛️",
        "links": [
            {"name": "中国政府网", "url": "https://www.gov.cn/"},
            {"name": "国家政务服务平台", "url": "https://www.gov.cn/fuwu/"},
            {"name": "12345政务服务热线", "url": "tel:12345"},
            {"name": "国务院客户端", "url": "https://app.gov.cn/"},
            {"name": "国家信访局", "url": "https://www.gjxfj.gov.cn/"},
            {"name": "中国普法网", "url": "http://www.legalinfo.gov.cn/"},
            {"name": "国家统计局", "url": "http://www.stats.gov.cn/"},
            {"name": "国家知识产权局", "url": "https://www.cnipa.gov.cn/"},
            {"name": "中国海关", "url": "http://www.customs.gov.cn/"},
            {"name": "国家税务局", "url": "https://www.chinatax.gov.cn/"},
        ]
    },
    "社保医保": {
        "icon": "🏥",
        "links": [
            {"name": "国家社保公共服务平台", "url": "https://si.12333.gov.cn/"},
            {"name": "国家医保服务平台", "url": "https://fuwu.nhsa.gov.cn/"},
            {"name": "12333社保查询热线", "url": "tel:12333"},
            {"name": "人社部政务服务平台", "url": "http://www.mohrss.gov.cn/"},
            {"name": "中国社会保障网", "url": "http://www.cnss.cn/"},
            {"name": "医保电子凭证", "url": "https://www.nhsa.gov.cn/"},
            {"name": "养老金查询", "url": "https://si.12333.gov.cn/"},
            {"name": "社保卡服务", "url": "https://si.12333.gov.cn/"},
            {"name": "异地就医备案", "url": "https://fuwu.nhsa.gov.cn/"},
            {"name": "生育保险查询", "url": "https://si.12333.gov.cn/"},
        ]
    },
    "交通出行": {
        "icon": "🚌",
        "links": [
            {"name": "12306火车票官网", "url": "https://www.12306.cn/"},
            {"name": "携程旅行", "url": "https://www.ctrip.com/"},
            {"name": "高德地图", "url": "https://www.amap.com/"},
            {"name": "百度地图", "url": "https://map.baidu.com/"},
            {"name": "去哪儿旅行", "url": "https://www.qunar.com/"},
            {"name": "飞猪旅行", "url": "https://www.fliggy.com/"},
            {"name": "滴滴出行", "url": "https://www.didiglobal.com/"},
            {"name": "中国民航局", "url": "http://www.caac.gov.cn/"},
            {"name": "航班查询", "url": "https://www.variflight.com/"},
            {"name": "汽车票预订", "url": "https://www.bus365.com/"},
            {"name": "中国铁路", "url": "http://www.china-railway.com.cn/"},
            {"name": "公路客运查询", "url": "http://www.chinabus.cn/"},
        ]
    },
    "教育学习": {
        "icon": "📚",
        "links": [
            {"name": "中国教育在线", "url": "https://www.eol.cn/"},
            {"name": "学信网", "url": "https://www.chsi.com.cn/"},
            {"name": "中国研究生招生信息网", "url": "https://yz.chsi.com.cn/"},
            {"name": "中国大学MOOC", "url": "https://www.icourse163.org/"},
            {"name": "国家中小学智慧教育平台", "url": "https://www.zxx.edu.cn/"},
            {"name": "中国知网", "url": "https://www.cnki.net/"},
            {"name": "万方数据", "url": "https://www.wanfangdata.com.cn/"},
            {"name": "维普资讯", "url": "http://www.cqvip.com/"},
            {"name": "中国教育考试网", "url": "https://www.neea.edu.cn/"},
            {"name": "高考网", "url": "https://www.gaokao.com/"},
            {"name": "考研网", "url": "https://www.kaoyan.com/"},
            {"name": "公务员考试网", "url": "https://www.chinagwy.org/"},
        ]
    },
    "生活服务": {
        "icon": "🏠",
        "links": [
            {"name": "美团", "url": "https://www.meituan.com/"},
            {"name": "饿了么", "url": "https://www.ele.me/"},
            {"name": "58同城", "url": "https://www.58.com/"},
            {"name": "大众点评", "url": "https://www.dianping.com/"},
            {"name": "贝壳找房", "url": "https://www.ke.com/"},
            {"name": "安居客", "url": "https://www.anjuke.com/"},
            {"name": "自如租房", "url": "https://www.ziroom.com/"},
            {"name": "家政服务", "url": "https://www.58.com/home/"},
            {"name": "同城招聘", "url": "https://www.58.com/job/"},
            {"name": "二手交易", "url": "https://www.58.com/ershou/"},
            {"name": "同城交友", "url": "https://www.58.com/jiaoyou/"},
            {"name": "宠物服务", "url": "https://www.58.com/pet/"},
        ]
    },
    "新闻资讯": {
        "icon": "📰",
        "links": [
            {"name": "人民网", "url": "http://www.people.com.cn/"},
            {"name": "新华网", "url": "http://www.xinhuanet.com/"},
            {"name": "央视网", "url": "https://www.cctv.com/"},
            {"name": "央视新闻", "url": "https://news.cctv.com/"},
            {"name": "今日头条", "url": "https://www.toutiao.com/"},
            {"name": "腾讯新闻", "url": "https://news.qq.com/"},
            {"name": "网易新闻", "url": "https://news.163.com/"},
            {"name": "搜狐新闻", "url": "https://news.sohu.com/"},
            {"name": "新浪新闻", "url": "https://news.sina.com.cn/"},
            {"name": "澎湃新闻", "url": "https://www.thepaper.cn/"},
            {"name": "界面新闻", "url": "https://www.jiemian.com/"},
            {"name": "中国新闻网", "url": "https://www.chinanews.com/"},
        ]
    },
    "购物电商": {
        "icon": "🛒",
        "links": [
            {"name": "淘宝", "url": "https://www.taobao.com/"},
            {"name": "京东", "url": "https://www.jd.com/"},
            {"name": "拼多多", "url": "https://www.pinduoduo.com/"},
            {"name": "天猫", "url": "https://www.tmall.com/"},
            {"name": "苏宁易购", "url": "https://www.suning.com/"},
            {"name": "唯品会", "url": "https://www.vip.com/"},
            {"name": "得物", "url": "https://www.poizon.com/"},
            {"name": "小红书商城", "url": "https://www.xiaohongshu.com/"},
            {"name": "抖音电商", "url": "https://www.douyin.com/"},
            {"name": "快手电商", "url": "https://www.kuaishou.com/"},
            {"name": "网易严选", "url": "https://you.163.com/"},
            {"name": "国美在线", "url": "https://www.gome.com.cn/"},
        ]
    },
    "娱乐休闲": {
        "icon": "🎮",
        "links": [
            {"name": "豆瓣", "url": "https://www.douban.com/"},
            {"name": "B站", "url": "https://www.bilibili.com/"},
            {"name": "爱奇艺", "url": "https://www.iqiyi.com/"},
            {"name": "腾讯视频", "url": "https://v.qq.com/"},
            {"name": "优酷", "url": "https://www.youku.com/"},
            {"name": "芒果TV", "url": "https://www.mgtv.com/"},
            {"name": "网易云音乐", "url": "https://music.163.com/"},
            {"name": "QQ音乐", "url": "https://y.qq.com/"},
            {"name": "酷狗音乐", "url": "https://www.kugou.com/"},
            {"name": "抖音", "url": "https://www.douyin.com/"},
            {"name": "快手", "url": "https://www.kuaishou.com/"},
            {"name": "微博", "url": "https://weibo.com/"},
        ]
    },
    "金融理财": {
        "icon": "💰",
        "links": [
            {"name": "中国工商银行", "url": "https://www.icbc.com.cn/"},
            {"name": "中国建设银行", "url": "https://www.ccb.com/"},
            {"name": "中国农业银行", "url": "https://www.abchina.com/"},
            {"name": "中国银行", "url": "https://www.boc.cn/"},
            {"name": "招商银行", "url": "https://www.cmbchina.com/"},
            {"name": "支付宝", "url": "https://www.alipay.com/"},
            {"name": "微信支付", "url": "https://weixin.qq.com/"},
            {"name": "东方财富", "url": "https://www.eastmoney.com/"},
            {"name": "同花顺", "url": "https://www.10jqka.com.cn/"},
            {"name": "雪球", "url": "https://xueqiu.com/"},
            {"name": "蚂蚁财富", "url": "https://www.antfortune.com/"},
            {"name": "京东金融", "url": "https://jr.jd.com/"},
        ]
    },
    "医疗健康": {
        "icon": "⚕️",
        "links": [
            {"name": "国家卫健委", "url": "http://www.nhc.gov.cn/"},
            {"name": "健康中国", "url": "http://www.jkchina.cn/"},
            {"name": "挂号网", "url": "https://www.guahao.com/"},
            {"name": "好大夫在线", "url": "https://www.haodf.com/"},
            {"name": "丁香医生", "url": "https://www.dxy.com/"},
            {"name": "春雨医生", "url": "https://www.chunyuyisheng.com/"},
            {"name": "平安健康", "url": "https://www.pk.cn/"},
            {"name": "京东健康", "url": "https://www.jdhealth.com/"},
            {"name": "阿里健康", "url": "https://www.alihealth.cn/"},
            {"name": "120急救", "url": "tel:120"},
            {"name": "疫情防控", "url": "http://www.nhc.gov.cn/xcs/xxgzbd/gzbd_index.shtml"},
            {"name": "疫苗接种", "url": "https://www.nip.chinacdc.cn/"},
        ]
    },
    "法律维权": {
        "icon": "⚖️",
        "links": [
            {"name": "中国法律服务网", "url": "http://www.12348.gov.cn/"},
            {"name": "12348法律援助热线", "url": "tel:12348"},
            {"name": "司法部", "url": "http://www.moj.gov.cn/"},
            {"name": "中国法院网", "url": "https://www.chinacourt.org/"},
            {"name": "最高人民法院", "url": "http://www.court.gov.cn/"},
            {"name": "中国裁判文书网", "url": "https://wenshu.court.gov.cn/"},
            {"name": "消费者协会", "url": "http://www.cca.org.cn/"},
            {"name": "12315消费者投诉", "url": "tel:12315"},
            {"name": "劳动仲裁", "url": "http://www.mohrss.gov.cn/"},
            {"name": "知识产权维权", "url": "https://www.cnipa.gov.cn/"},
        ]
    },
    "求职招聘": {
        "icon": "💼",
        "links": [
            {"name": "智联招聘", "url": "https://www.zhaopin.com/"},
            {"name": "前程无忧", "url": "https://www.51job.com/"},
            {"name": "BOSS直聘", "url": "https://www.zhipin.com/"},
            {"name": "猎聘", "url": "https://www.liepin.com/"},
            {"name": "拉勾网", "url": "https://www.lagou.com/"},
            {"name": "应届生求职网", "url": "https://www.yingjiesheng.com/"},
            {"name": "中国公共招聘网", "url": "http://www.job.mohrss.gov.cn/"},
            {"name": "事业单位招聘", "url": "http://www.gjw.gov.cn/"},
            {"name": "公务员考试", "url": "https://www.chinagwy.org/"},
            {"name": "银行招聘", "url": "https://www.yinhangzhaopin.com/"},
        ]
    },
    "科技数码": {
        "icon": "💻",
        "links": [
            {"name": "中关村在线", "url": "https://www.zol.com.cn/"},
            {"name": "太平洋电脑网", "url": "https://www.pconline.com.cn/"},
            {"name": "天极网", "url": "https://www.yesky.com/"},
            {"name": "IT之家", "url": "https://www.ithome.com/"},
            {"name": "雷锋网", "url": "https://www.leiphone.com/"},
            {"name": "36氪", "url": "https://36kr.com/"},
            {"name": "虎嗅网", "url": "https://www.huxiu.com/"},
            {"name": "爱范儿", "url": "https://www.ifanr.com/"},
            {"name": "极客公园", "url": "https://www.geekpark.net/"},
            {"name": "数码之家", "url": "https://www.digiteye.cn/"},
        ]
    },
    "AI智能工具": {
        "icon": "🤖",
        "links": [
            {"name": "ChatGPT", "url": "https://chat.openai.com/"},
            {"name": "文心一言", "url": "https://yiyan.baidu.com/"},
            {"name": "通义千问", "url": "https://tongyi.aliyun.com/"},
            {"name": "Kimi智能助手", "url": "https://kimi.moonshot.cn/"},
            {"name": "豆包", "url": "https://www.doubao.com/"},
            {"name": "讯飞星火", "url": "https://xinghuo.xfyun.cn/"},
            {"name": "智谱清言", "url": "https://chatglm.cn/"},
            {"name": "腾讯混元", "url": "https://hunyuan.tencent.com/"},
            {"name": "百川智能", "url": "https://www.baichuan-ai.com/"},
            {"name": "Midjourney", "url": "https://www.midjourney.com/"},
        ]
    },
    "紧急求助": {
        "icon": "🚨",
        "links": [
            {"name": "报警电话110", "url": "tel:110"},
            {"name": "急救电话120", "url": "tel:120"},
            {"name": "火警电话119", "url": "tel:119"},
            {"name": "交通事故122", "url": "tel:122"},
            {"name": "消费者投诉12315", "url": "tel:12315"},
            {"name": "政务服务12345", "url": "tel:12345"},
            {"name": "法律援助12348", "url": "tel:12348"},
            {"name": "社保咨询12333", "url": "tel:12333"},
            {"name": "邮政投诉11185", "url": "tel:11185"},
            {"name": "电力服务95598", "url": "tel:95598"},
        ]
    },
}

# ==================== 城市特色链接模板 ====================

def get_city_specific_links(city_name, city_pinyin):
    """生成城市特色链接"""
    city_links = {
        "本地政务": {
            "icon": "🏛️",
            "links": [
                {"name": f"{city_name}人民政府", "url": f"http://www.{city_pinyin}.gov.cn/"},
                {"name": f"{city_name}政务服务网", "url": f"http://zwfw.{city_pinyin}.gov.cn/"},
                {"name": f"{city_name}12345热线", "url": "tel:12345"},
                {"name": f"{city_name}人社局", "url": f"http://rsj.{city_pinyin}.gov.cn/"},
                {"name": f"{city_name}教育局", "url": f"http://jyj.{city_pinyin}.gov.cn/"},
            ]
        },
        "本地交通": {
            "icon": "🚌",
            "links": [
                {"name": f"{city_name}公交查询", "url": f"http://bus.{city_pinyin}.gov.cn/"},
                {"name": f"{city_name}地铁", "url": f"http://metro.{city_pinyin}.gov.cn/"},
                {"name": f"{city_name}交通局", "url": f"http://jtj.{city_pinyin}.gov.cn/"},
                {"name": f"{city_name}出租车", "url": f"http://taxi.{city_pinyin}.gov.cn/"},
                {"name": f"{city_name}实时路况", "url": f"https://www.amap.com/"},
            ]
        },
        "本地生活": {
            "icon": "🏠",
            "links": [
                {"name": f"{city_name}美团", "url": f"https://www.meituan.com/{city_pinyin}/"},
                {"name": f"{city_name}饿了么", "url": f"https://www.ele.me/{city_pinyin}/"},
                {"name": f"{city_name}58同城", "url": f"https://www.58.com/{city_pinyin}/"},
                {"name": f"{city_name}大众点评", "url": f"https://www.dianping.com/{city_pinyin}/"},
                {"name": f"{city_name}本地招聘", "url": f"https://www.zhaopin.com/{city_pinyin}/"},
            ]
        },
        "本地医疗": {
            "icon": "⚕️",
            "links": [
                {"name": f"{city_name}卫健委", "url": f"http://wsjkw.{city_pinyin}.gov.cn/"},
                {"name": f"{city_name}医院挂号", "url": f"https://www.guahao.com/{city_pinyin}/"},
                {"name": f"{city_name}疾控中心", "url": f"http://cdc.{city_pinyin}.gov.cn/"},
                {"name": f"{city_name}急救中心", "url": "tel:120"},
                {"name": f"{city_name}社区卫生", "url": f"http://health.{city_pinyin}.gov.cn/"},
            ]
        },
        "本地房产": {
            "icon": "🏠",
            "links": [
                {"name": f"{city_name}贝壳找房", "url": f"https://{city_pinyin}.ke.com/"},
                {"name": f"{city_name}安居客", "url": f"https://{city_pinyin}.anjuke.com/"},
                {"name": f"{city_name}自如租房", "url": f"https://www.ziroom.com/{city_pinyin}/"},
                {"name": f"{city_name}房管局", "url": f"http://fgj.{city_pinyin}.gov.cn/"},
                {"name": f"{city_name}公积金", "url": f"http://gjj.{city_pinyin}.gov.cn/"},
            ]
        },
    }
    return city_links


# ==================== 行业特色链接模板 ====================

def get_niche_specific_links(niche_name, niche_pinyin):
    """生成行业特色链接"""
    # 通用行业链接模板
    niche_links = {
        "行业资源": {
            "icon": "📚",
            "links": [
                {"name": f"{niche_name}资讯", "url": f"https://www.baidu.com/s?wd={niche_name}"},
                {"name": f"{niche_name}论坛", "url": f"https://tieba.baidu.com/f?kw={niche_name}"},
                {"name": f"{niche_name}知乎话题", "url": f"https://www.zhihu.com/topic/{niche_name}"},
                {"name": f"{niche_name}豆瓣小组", "url": f"https://www.douban.com/group/search?q={niche_name}"},
                {"name": f"{niche_name}微博话题", "url": f"https://s.weibo.com/topic/{niche_name}"},
            ]
        },
        "学习资料": {
            "icon": "📖",
            "links": [
                {"name": f"{niche_name}教程", "url": f"https://www.bilibili.com/search?keyword={niche_name}教程"},
                {"name": f"{niche_name}视频课程", "url": f"https://www.icourse163.org/search/{niche_name}"},
                {"name": f"{niche_name}书籍推荐", "url": f"https://www.douban.com/search?q={niche_name}书籍"},
                {"name": f"{niche_name}学习路线", "url": f"https://www.zhihu.com/search?q={niche_name}学习路线"},
                {"name": f"{niche_name}在线练习", "url": f"https://www.baidu.com/s?wd={niche_name}练习"},
            ]
        },
        "工具软件": {
            "icon": "🔧",
            "links": [
                {"name": f"{niche_name}软件下载", "url": f"https://www.baidu.com/s?wd={niche_name}软件"},
                {"name": f"{niche_name}在线工具", "url": f"https://www.baidu.com/s?wd={niche_name}在线工具"},
                {"name": f"{niche_name}APP推荐", "url": f"https://www.baidu.com/s?wd={niche_name}APP"},
                {"name": f"{niche_name}开源项目", "url": f"https://github.com/search?q={niche_name}"},
                {"name": f"{niche_name}模板资源", "url": f"https://www.baidu.com/s?wd={niche_name}模板"},
            ]
        },
        "社区交流": {
            "icon": "💬",
            "links": [
                {"name": f"{niche_name}QQ群", "url": f"https://jq.qq.com/?_wv=1027&k={niche_name}"},
                {"name": f"{niche_name}微信群", "url": f"https://weixin.qq.com/"},
                {"name": f"{niche_name}社区论坛", "url": f"https://www.baidu.com/s?wd={niche_name}论坛"},
                {"name": f"{niche_name}公众号", "url": f"https://weixin.sogou.com/weixin?type=1&query={niche_name}"},
                {"name": f"{niche_name}知识星球", "url": f"https://www.zsxq.com/"},
            ]
        },
        "考试认证": {
            "icon": "📝",
            "links": [
                {"name": f"{niche_name}考试报名", "url": f"https://www.baidu.com/s?wd={niche_name}考试"},
                {"name": f"{niche_name}证书查询", "url": f"https://www.baidu.com/s?wd={niche_name}证书查询"},
                {"name": f"{niche_name}考试大纲", "url": f"https://www.baidu.com/s?wd={niche_name}考试大纲"},
                {"name": f"{niche_name}历年真题", "url": f"https://www.baidu.com/s?wd={niche_name}真题"},
                {"name": f"{niche_name}培训机构", "url": f"https://www.baidu.com/s?wd={niche_name}培训"},
            ]
        },
        "就业发展": {
            "icon": "💼",
            "links": [
                {"name": f"{niche_name}招聘", "url": f"https://www.zhaopin.com/search/?kw={niche_name}"},
                {"name": f"{niche_name}岗位", "url": f"https://www.zhipin.com/job_detail/?query={niche_name}"},
                {"name": f"{niche_name}薪资", "url": f"https://www.zhipin.com/salary/{niche_name}"},
                {"name": f"{niche_name}职业发展", "url": f"https://www.zhihu.com/search?q={niche_name}职业"},
                {"name": f"{niche_name}面试题", "url": f"https://www.baidu.com/s?wd={niche_name}面试题"},
            ]
        },
    }
    return niche_links


def enrich_city_site(city_name, city_pinyin):
    """为城市站生成丰富的内容"""
    categories = []
    
    # 添加基础分类（每个分类取8-12条链接）
    for cat_name, cat_data in BASE_CATEGORIES.items():
        links = random.sample(cat_data["links"], min(10, len(cat_data["links"])))
        categories.append({
            "name": cat_name,
            "icon": cat_data["icon"],
            "links": links
        })
    
    # 添加城市特色分类
    city_links = get_city_specific_links(city_name, city_pinyin)
    for cat_name, cat_data in city_links.items():
        categories.append({
            "name": f"{city_name}{cat_name}",
            "icon": cat_data["icon"],
            "links": cat_data["links"]
        })
    
    return categories


def enrich_niche_site(niche_name, niche_pinyin):
    """为行业站生成丰富的内容"""
    categories = []
    
    # 添加基础分类
    for cat_name, cat_data in BASE_CATEGORIES.items():
        links = random.sample(cat_data["links"], min(8, len(cat_data["links"])))
        categories.append({
            "name": cat_name,
            "icon": cat_data["icon"],
            "links": links
        })
    
    # 添加行业特色分类
    niche_links = get_niche_specific_links(niche_name, niche_pinyin)
    for cat_name, cat_data in niche_links.items():
        categories.append({
            "name": cat_name,
            "icon": cat_data["icon"],
            "links": cat_data["links"]
        })
    
    return categories


def enrich_hybrid_site(city_name, city_pinyin, niche_name, niche_pinyin):
    """为混合站生成丰富的内容"""
    categories = []
    
    # 添加基础分类（精简版）
    essential_cats = ["政务服务", "交通出行", "生活服务", "新闻资讯", "紧急求助"]
    for cat_name in essential_cats:
        cat_data = BASE_CATEGORIES[cat_name]
        links = random.sample(cat_data["links"], min(6, len(cat_data["links"])))
        categories.append({
            "name": cat_name,
            "icon": cat_data["icon"],
            "links": links
        })
    
    # 添加城市特色（精简版）
    city_links = get_city_specific_links(city_name, city_pinyin)
    for cat_name in ["本地政务", "本地生活"]:
        cat_data = city_links[cat_name]
        categories.append({
            "name": f"{city_name}{cat_name}",
            "icon": cat_data["icon"],
            "links": cat_data["links"][:3]
        })
    
    # 添加行业特色（精简版）
    niche_links = get_niche_specific_links(niche_name, niche_pinyin)
    for cat_name in ["行业资源", "学习资料", "工具软件"]:
        cat_data = niche_links[cat_name]
        categories.append({
            "name": cat_name,
            "icon": cat_data["icon"],
            "links": cat_data["links"][:4]
        })
    
    return categories


def update_all_sites():
    """更新所有站点的内容"""
    print("=" * 60)
    print("  站点内容扩充引擎")
    print("=" * 60)
    
    # 更新城市站
    cities_dir = SITES_DIR / "cities"
    if cities_dir.exists():
        city_count = 0
        for city_dir in cities_dir.iterdir():
            if city_dir.is_dir():
                config_path = city_dir / "config.json"
                if config_path.exists():
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    city_name = config.get('cityName', '')
                    city_pinyin = config.get('cityPinyin', city_dir.name)
                    
                    new_categories = enrich_city_site(city_name, city_pinyin)
                    config['categories'] = new_categories
                    
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(config, f, ensure_ascii=False, indent=2)
                    
                    city_count += 1
                    if city_count % 20 == 0:
                        print(f"  城市站进度: {city_count}")
        
        print(f"✓ 城市站更新完成: {city_count} 个")
    
    # 更新行业站
    niches_dir = SITES_DIR / "niches"
    if niches_dir.exists():
        niche_count = 0
        for niche_dir in niches_dir.iterdir():
            if niche_dir.is_dir():
                config_path = niche_dir / "config.json"
                if config_path.exists():
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    niche_name = config.get('nicheName', '')
                    niche_pinyin = config.get('nichePinyin', niche_dir.name)
                    
                    new_categories = enrich_niche_site(niche_name, niche_pinyin)
                    config['categories'] = new_categories
                    
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(config, f, ensure_ascii=False, indent=2)
                    
                    niche_count += 1
                    if niche_count % 20 == 0:
                        print(f"  行业站进度: {niche_count}")
        
        print(f"✓ 行业站更新完成: {niche_count} 个")
    
    # 更新混合站（分批处理，避免内存溢出）
    hybrids_dir = SITES_DIR / "hybrids"
    if hybrids_dir.exists():
        hybrid_dirs = [d for d in hybrids_dir.iterdir() if d.is_dir()]
        total_hybrids = len(hybrid_dirs)
        print(f"混合站总数: {total_hybrids}")
        
        hybrid_count = 0
        for hybrid_dir in hybrid_dirs:
            config_path = hybrid_dir / "config.json"
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    city_name = config.get('cityName', '')
                    city_pinyin = config.get('cityPinyin', '')
                    niche_name = config.get('nicheName', '')
                    niche_pinyin = config.get('nichePinyin', '')
                    
                    new_categories = enrich_hybrid_site(city_name, city_pinyin, niche_name, niche_pinyin)
                    config['categories'] = new_categories
                    
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(config, f, ensure_ascii=False, indent=2)
                    
                    hybrid_count += 1
                    if hybrid_count % 200 == 0:
                        print(f"  混合站进度: {hybrid_count}/{total_hybrids}")
                except Exception as e:
                    pass
        
        print(f"✓ 混合站更新完成: {hybrid_count} 个")
    
    print("\n" + "=" * 60)
    print("  内容扩充完成!")
    print("=" * 60)


if __name__ == '__main__':
    update_all_sites()