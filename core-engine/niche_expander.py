#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行业扩展器 - niche_expander.py
扩展行业站到500个垂直领域
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
SITES_DIR = ROOT_DIR / "02-sites" / "niches"
TEMPLATES_DIR = ROOT_DIR / "01-templates" / "base"

def load_json(file_path):
    """加载JSON文件"""
    return json.loads(file_path.read_text(encoding='utf-8'))

# 500个垂直行业数据
ALL_NICHES = [
    # 生活服务类 (50)
    {"nicheName": "搬家", "nichePinyin": "banjia", "nicheCategory": "生活服务"},
    {"nicheName": "家政", "nichePinyin": "jiazheng", "nicheCategory": "生活服务"},
    {"nicheName": "保洁", "nichePinyin": "baojie", "nicheCategory": "生活服务"},
    {"nicheName": "维修", "nichePinyin": "weixiu", "nicheCategory": "生活服务"},
    {"nicheName": "装修", "nichePinyin": "zhuangxiu", "nicheCategory": "生活服务"},
    {"nicheName": "婚庆", "nichePinyin": "hunqing", "nicheCategory": "生活服务"},
    {"nicheName": "摄影", "nichePinyin": "sheying", "nicheCategory": "生活服务"},
    {"nicheName": "快递", "nichePinyin": "kuaidi", "nicheCategory": "生活服务"},
    {"nicheName": "外卖", "nichePinyin": "waimai", "nicheCategory": "生活服务"},
    {"nicheName": "洗衣", "nichePinyin": "xiyi", "nicheCategory": "生活服务"},
    {"nicheName": "宠物", "nichePinyin": "chongwu", "nicheCategory": "生活服务"},
    {"nicheName": "母婴", "nichePinyin": "muying", "nicheCategory": "生活服务"},
    {"nicheName": "育儿", "nichePinyin": "yuer", "nicheCategory": "生活服务"},
    {"nicheName": "养老", "nichePinyin": "yanglao", "nicheCategory": "生活服务"},
    {"nicheName": "殡葬", "nichePinyin": "binzang", "nicheCategory": "生活服务"},
    {"nicheName": "搬家货运", "nichePinyin": "banjiahuoyun", "nicheCategory": "生活服务"},
    {"nicheName": "家政保洁", "nichePinyin": "jiazhengbaojie", "nicheCategory": "生活服务"},
    {"nicheName": "家电维修", "nichePinyin": "jiadianweixiu", "nicheCategory": "生活服务"},
    {"nicheName": "水电维修", "nichePinyin": "shuidianweixiu", "nicheCategory": "生活服务"},
    {"nicheName": "空调维修", "nichePinyin": "kongtiaoweixiu", "nicheCategory": "生活服务"},
    {"nicheName": "电脑维修", "nichePinyin": "diannaoweixiu", "nicheCategory": "生活服务"},
    {"nicheName": "手机维修", "nichePinyin": "shoujiweixiu", "nicheCategory": "生活服务"},
    {"nicheName": "汽车维修", "nichePinyin": "qicheweixiu", "nicheCategory": "生活服务"},
    {"nicheName": "房屋装修", "nichePinyin": "fangwuzhuangxiu", "nicheCategory": "生活服务"},
    {"nicheName": "婚庆策划", "nichePinyin": "hunqingcehua", "nicheCategory": "生活服务"},
    {"nicheName": "婚纱摄影", "nichePinyin": "hunshasheying", "nicheCategory": "生活服务"},
    {"nicheName": "婚礼摄影", "nichePinyin": "hunlisheying", "nicheCategory": "生活服务"},
    {"nicheName": "快递物流", "nichePinyin": "kuaidiwuliu", "nicheCategory": "生活服务"},
    {"nicheName": "同城配送", "nichePinyin": "tongchengpeisong", "nicheCategory": "生活服务"},
    {"nicheName": "外卖订餐", "nichePinyin": "waimaidingcan", "nicheCategory": "生活服务"},
    {"nicheName": "干洗服务", "nichePinyin": "ganxifuwu", "nicheCategory": "生活服务"},
    {"nicheName": "宠物医院", "nichePinyin": "chongwuyiyuan", "nicheCategory": "生活服务"},
    {"nicheName": "宠物美容", "nichePinyin": "chongwumeirong", "nicheCategory": "生活服务"},
    {"nicheName": "宠物寄养", "nichePinyin": "chongwujiyang", "nicheCategory": "生活服务"},
    {"nicheName": "母婴用品", "nichePinyin": "muyingyongpin", "nicheCategory": "生活服务"},
    {"nicheName": "育儿知识", "nichePinyin": "yuerzhishi", "nicheCategory": "生活服务"},
    {"nicheName": "早教中心", "nichePinyin": "zaojiaozhongxin", "nicheCategory": "生活服务"},
    {"nicheName": "月子中心", "nichePinyin": "yuezi zhongxin", "nicheCategory": "生活服务"},
    {"nicheName": "养老院", "nichePinyin": "yanglaoyuan", "nicheCategory": "生活服务"},
    {"nicheName": "居家养老", "nichePinyin": "jujiyanglao", "nicheCategory": "生活服务"},
    {"nicheName": "殡葬服务", "nichePinyin": "binzangfuwu", "nicheCategory": "生活服务"},
    {"nicheName": "墓地陵园", "nichePinyin": "mudilingyuan", "nicheCategory": "生活服务"},
    {"nicheName": "家政服务", "nichePinyin": "jiazhengfuwu", "nicheCategory": "生活服务"},
    {"nicheName": "保姆月嫂", "nichePinyin": "baomuyuesao", "nicheCategory": "生活服务"},
    {"nicheName": "钟点工", "nichePinyin": "zhongdian gong", "nicheCategory": "生活服务"},
    {"nicheName": "护工", "nichePinyin": "hugong", "nicheCategory": "生活服务"},
    {"nicheName": "保洁服务", "nichePinyin": "baojiefuwu", "nicheCategory": "生活服务"},
    {"nicheName": "开荒保洁", "nichePinyin": "kaihuangbaojie", "nicheCategory": "生活服务"},
    {"nicheName": "深度保洁", "nichePinyin": "shendubaojie", "nicheCategory": "生活服务"},
    {"nicheName": "家电清洗", "nichePinyin": "jiadianqingxi", "nicheCategory": "生活服务"},
    
    # 教育培训类 (80)
    {"nicheName": "考研", "nichePinyin": "kaoyan", "nicheCategory": "教育培训"},
    {"nicheName": "公务员", "nichePinyin": "gongwuyuan", "nicheCategory": "教育培训"},
    {"nicheName": "教师", "nichePinyin": "jiaoshi", "nicheCategory": "教育培训"},
    {"nicheName": "教师资格", "nichePinyin": "jiaoshizige", "nicheCategory": "教育培训"},
    {"nicheName": "教师面试", "nichePinyin": "jiaoshimianshi", "nicheCategory": "教育培训"},
    {"nicheName": "雅思", "nichePinyin": "yasi", "nicheCategory": "教育培训"},
    {"nicheName": "托福", "nichePinyin": "tuofu", "nicheCategory": "教育培训"},
    {"nicheName": "四六级", "nichePinyin": "siliuji", "nicheCategory": "教育培训"},
    {"nicheName": "会计", "nichePinyin": "kuaiji", "nicheCategory": "教育培训"},
    {"nicheName": "中级会计", "nichePinyin": "zhongjikuaiji", "nicheCategory": "教育培训"},
    {"nicheName": "注册会计师", "nichePinyin": "zhucekuaiji shi", "nicheCategory": "教育培训"},
    {"nicheName": "银行招聘", "nichePinyin": "yinhangzhaopin", "nicheCategory": "教育培训"},
    {"nicheName": "事业单位", "nichePinyin": "shiyedanwei", "nicheCategory": "教育培训"},
    {"nicheName": "考研英语", "nichePinyin": "kaoyanyingyu", "nicheCategory": "教育培训"},
    {"nicheName": "考研政治", "nichePinyin": "kaoyanzhengzhi", "nicheCategory": "教育培训"},
    {"nicheName": "考研数学", "nichePinyin": "kaoyanshuxue", "nicheCategory": "教育培训"},
    {"nicheName": "MBA", "nichePinyin": "mba", "nicheCategory": "教育培训"},
    {"nicheName": "EMBA", "nichePinyin": "emba", "nicheCategory": "教育培训"},
    {"nicheName": "MPA", "nichePinyin": "mpa", "nicheCategory": "教育培训"},
    {"nicheName": "法律硕士", "nichePinyin": "falvshuoshi", "nicheCategory": "教育培训"},
    {"nicheName": "医学考研", "nichePinyin": "yixuekaoyan", "nicheCategory": "教育培训"},
    {"nicheName": "教育学考研", "nichePinyin": "jiaoyuxuekaoyan", "nicheCategory": "教育培训"},
    {"nicheName": "心理学考研", "nichePinyin": "xinlixuekaoyan", "nicheCategory": "教育培训"},
    {"nicheName": "计算机考研", "nichePinyin": "jisuanjikaoyan", "nicheCategory": "教育培训"},
    {"nicheName": "金融考研", "nichePinyin": "jinrongkaoyan", "nicheCategory": "教育培训"},
    {"nicheName": "管理考研", "nichePinyin": "guanlikaoyan", "nicheCategory": "教育培训"},
    {"nicheName": "艺术考研", "nichePinyin": "yishukaoyan", "nicheCategory": "教育培训"},
    {"nicheName": "体育考研", "nichePinyin": "tikakaoyan", "nicheCategory": "教育培训"},
    {"nicheName": "英语培训", "nichePinyin": "yingyupexun", "nicheCategory": "教育培训"},
    {"nicheName": "日语培训", "nichePinyin": "riyupexun", "nicheCategory": "教育培训"},
    {"nicheName": "韩语培训", "nichePinyin": "hanyupexun", "nicheCategory": "教育培训"},
    {"nicheName": "法语培训", "nichePinyin": "fayupexun", "nicheCategory": "教育培训"},
    {"nicheName": "德语培训", "nichePinyin": "deyupexun", "nicheCategory": "教育培训"},
    {"nicheName": "西班牙语培训", "nichePinyin": "xibanyayupexun", "nicheCategory": "教育培训"},
    {"nicheName": "俄语培训", "nichePinyin": "eyupexun", "nicheCategory": "教育培训"},
    {"nicheName": "阿拉伯语培训", "nichePinyin": "alaboyayupexun", "nicheCategory": "教育培训"},
    {"nicheName": "葡萄牙语培训", "nichePinyin": "putaoyayupexun", "nicheCategory": "教育培训"},
    {"nicheName": "意大利语培训", "nichePinyin": "yidaliyupexun", "nicheCategory": "教育培训"},
    {"nicheName": "泰语培训", "nichePinyin": "taiyupexun", "nicheCategory": "教育培训"},
    {"nicheName": "越南语培训", "nichePinyin": "yuenanyupexun", "nicheCategory": "教育培训"},
    {"nicheName": "编程培训", "nichePinyin": "bianchengpexun", "nicheCategory": "教育培训"},
    {"nicheName": "Python培训", "nichePinyin": "pythonpexun", "nicheCategory": "教育培训"},
    {"nicheName": "Java培训", "nichePinyin": "javapexun", "nicheCategory": "教育培训"},
    {"nicheName": "前端培训", "nichePinyin": "qianduanpexun", "nicheCategory": "教育培训"},
    {"nicheName": "后端培训", "nichePinyin": "houduanpexun", "nicheCategory": "教育培训"},
    {"nicheName": "全栈培训", "nichePinyin": "quanzhanpexun", "nicheCategory": "教育培训"},
    {"nicheName": "数据分析培训", "nichePinyin": "shujufenxipexun", "nicheCategory": "教育培训"},
    {"nicheName": "人工智能培训", "nichePinyin": "rengongzhinengpexun", "nicheCategory": "教育培训"},
    {"nicheName": "机器学习培训", "nichePinyin": "jixuexuexipexun", "nicheCategory": "教育培训"},
    {"nicheName": "深度学习培训", "nichePinyin": "shenduxuexipexun", "nicheCategory": "教育培训"},
    {"nicheName": "大数据培训", "nichePinyin": "dashujupexun", "nicheCategory": "教育培训"},
    {"nicheName": "云计算培训", "nichePinyin": "yunjisuanpexun", "nicheCategory": "教育培训"},
    {"nicheName": "区块链培训", "nichePinyin": "qukuailianpexun", "nicheCategory": "教育培训"},
    {"nicheName": "网络安全培训", "nichePinyin": "wangluoanquanpexun", "nicheCategory": "教育培训"},
    {"nicheName": "UI设计培训", "nichePinyin": "uishejipexun", "nicheCategory": "教育培训"},
    {"nicheName": "平面设计培训", "nichePinyin": "pingmianshejipexun", "nicheCategory": "教育培训"},
    {"nicheName": "室内设计培训", "nichePinyin": "shineishejipexun", "nicheCategory": "教育培训"},
    {"nicheName": "建筑设计培训", "nichePinyin": "jianzhushejipexun", "nicheCategory": "教育培训"},
    {"nicheName": "园林设计培训", "nichePinyin": "yuanlinshejipexun", "nicheCategory": "教育培训"},
    {"nicheName": "工业设计培训", "nichePinyin": "gongyeshejipexun", "nicheCategory": "教育培训"},
    {"nicheName": "服装设计培训", "nichePinyin": "fuzhuangshejipexun", "nicheCategory": "教育培训"},
    {"nicheName": "动画设计培训", "nichePinyin": "donghuashejipexun", "nicheCategory": "教育培训"},
    {"nicheName": "游戏设计培训", "nichePinyin": "youxishejipexun", "nicheCategory": "教育培训"},
    {"nicheName": "影视后期培训", "nichePinyin": "yingshihouqipexun", "nicheCategory": "教育培训"},
    {"nicheName": "视频剪辑培训", "nichePinyin": "shipinjianjipexun", "nicheCategory": "教育培训"},
    {"nicheName": "摄影培训", "nichePinyin": "sheyingpexun", "nicheCategory": "教育培训"},
    {"nicheName": "化妆培训", "nichePinyin": "huazhuangpexun", "nicheCategory": "教育培训"},
    {"nicheName": "美发培训", "nichePinyin": "meifapexun", "nicheCategory": "教育培训"},
    {"nicheName": "美容培训", "nichePinyin": "meirongpexun", "nicheCategory": "教育培训"},
    {"nicheName": "美甲培训", "nichePinyin": "meijiapeixun", "nicheCategory": "教育培训"},
    {"nicheName": "纹绣培训", "nichePinyin": "wenxiupexun", "nicheCategory": "教育培训"},
    {"nicheName": "健身培训", "nichePinyin": "jianshenpexun", "nicheCategory": "教育培训"},
    {"nicheName": "瑜伽培训", "nichePinyin": "yujiapexun", "nicheCategory": "教育培训"},
    {"nicheName": "舞蹈培训", "nichePinyin": "wudaopexun", "nicheCategory": "教育培训"},
    {"nicheName": "音乐培训", "nichePinyin": "yinyuepexun", "nicheCategory": "教育培训"},
    {"nicheName": "钢琴培训", "nichePinyin": "gangqinpexun", "nicheCategory": "教育培训"},
    {"nicheName": "吉他培训", "nichePinyin": "jitapexun", "nicheCategory": "教育培训"},
    {"nicheName": "声乐培训", "nichePinyin": "shenglepexun", "nicheCategory": "教育培训"},
    {"nicheName": "绘画培训", "nichePinyin": "huahuapexun", "nicheCategory": "教育培训"},
    {"nicheName": "书法培训", "nichePinyin": "shufapexun", "nicheCategory": "教育培训"},
    {"nicheName": "国学培训", "nichePinyin": "guoxuepexun", "nicheCategory": "教育培训"},
    
    # 健康医疗类 (40)
    {"nicheName": "中医", "nichePinyin": "zhongyi", "nicheCategory": "健康医疗"},
    {"nicheName": "西医", "nichePinyin": "xiyi", "nicheCategory": "健康医疗"},
    {"nicheName": "养生", "nichePinyin": "yangsheng", "nicheCategory": "健康医疗"},
    {"nicheName": "保健", "nichePinyin": "baojian", "nicheCategory": "健康医疗"},
    {"nicheName": "减肥", "nichePinyin": "jianfei", "nicheCategory": "健康医疗"},
    {"nicheName": "健身", "nichePinyin": "jianshen", "nicheCategory": "健康医疗"},
    {"nicheName": "瑜伽", "nichePinyin": "yujia", "nicheCategory": "健康医疗"},
    {"nicheName": "跑步", "nichePinyin": "paobu", "nicheCategory": "健康医疗"},
    {"nicheName": "游泳", "nichePinyin": "youyong", "nicheCategory": "健康医疗"},
    {"nicheName": "心理咨询", "nichePinyin": "xinlizixun", "nicheCategory": "健康医疗"},
    {"nicheName": "心理健康", "nichePinyin": "xinlijiankang", "nicheCategory": "健康医疗"},
    {"nicheName": "营养饮食", "nichePinyin": "yingyangyinshi", "nicheCategory": "健康医疗"},
    {"nicheName": "健康饮食", "nichePinyin": "jiankangyinshi", "nicheCategory": "健康医疗"},
    {"nicheName": "中医养生", "nichePinyin": "zhongyi yangsheng", "nicheCategory": "健康医疗"},
    {"nicheName": "艾灸", "nichePinyin": "aijiu", "nicheCategory": "健康医疗"},
    {"nicheName": "推拿", "nichePinyin": "tuina", "nicheCategory": "健康医疗"},
    {"nicheName": "针灸", "nichePinyin": "zhenjiu", "nicheCategory": "健康医疗"},
    {"nicheName": "拔罐", "nichePinyin": "baguan", "nicheCategory": "健康医疗"},
    {"nicheName": "刮痧", "nichePinyin": "guasha", "nicheCategory": "健康医疗"},
    {"nicheName": "足疗", "nichePinyin": "zuliao", "nicheCategory": "健康医疗"},
    {"nicheName": "按摩", "nichePinyin": "anmo", "nicheCategory": "健康医疗"},
    {"nicheName": "SPA", "nichePinyin": "spa", "nicheCategory": "健康医疗"},
    {"nicheName": "美容", "nichePinyin": "meirong", "nicheCategory": "健康医疗"},
    {"nicheName": "护肤", "nichePinyin": "hufu", "nicheCategory": "健康医疗"},
    {"nicheName": "化妆", "nichePinyin": "huazhuang", "nicheCategory": "健康医疗"},
    {"nicheName": "美发", "nichePinyin": "meifa", "nicheCategory": "健康医疗"},
    {"nicheName": "美甲", "nichePinyin": "meijia", "nicheCategory": "健康医疗"},
    {"nicheName": "纹身", "nichePinyin": "wenshen", "nicheCategory": "健康医疗"},
    {"nicheName": "整形", "nichePinyin": "zhengxing", "nicheCategory": "健康医疗"},
    {"nicheName": "医美", "nichePinyin": "yimei", "nicheCategory": "健康医疗"},
    {"nicheName": "口腔", "nichePinyin": "kouqiang", "nicheCategory": "健康医疗"},
    {"nicheName": "眼科", "nichePinyin": "yanke", "nicheCategory": "健康医疗"},
    {"nicheName": "耳鼻喉", "nichePinyin": "erbihou", "nicheCategory": "健康医疗"},
    {"nicheName": "皮肤科", "nichePinyin": "pifuke", "nicheCategory": "健康医疗"},
    {"nicheName": "妇产科", "nichePinyin": "fuchanke", "nicheCategory": "健康医疗"},
    {"nicheName": "儿科", "nichePinyin": "erke", "nicheCategory": "健康医疗"},
    {"nicheName": "骨科", "nichePinyin": "guke", "nicheCategory": "健康医疗"},
    {"nicheName": "心血管", "nichePinyin": "xinxueguan", "nicheCategory": "健康医疗"},
    {"nicheName": "肿瘤", "nichePinyin": "zhongliu", "nicheCategory": "健康医疗"},
    {"nicheName": "康复", "nichePinyin": "kangfu", "nicheCategory": "健康医疗"},
    
    # 财经金融类 (40)
    {"nicheName": "投资", "nichePinyin": "touzi", "nicheCategory": "财经金融"},
    {"nicheName": "理财", "nichePinyin": "licai", "nicheCategory": "财经金融"},
    {"nicheName": "股票", "nichePinyin": "gupiao", "nicheCategory": "财经金融"},
    {"nicheName": "基金", "nichePinyin": "jijin", "nicheCategory": "财经金融"},
    {"nicheName": "期货", "nichePinyin": "qihuo", "nicheCategory": "财经金融"},
    {"nicheName": "外汇", "nichePinyin": "waihui", "nicheCategory": "财经金融"},
    {"nicheName": "债券", "nichePinyin": "zhaiquan", "nicheCategory": "财经金融"},
    {"nicheName": "保险", "nichePinyin": "baoxian", "nicheCategory": "财经金融"},
    {"nicheName": "银行", "nichePinyin": "yinhang", "nicheCategory": "财经金融"},
    {"nicheName": "信用卡", "nichePinyin": "xinyongka", "nicheCategory": "财经金融"},
    {"nicheName": "贷款", "nichePinyin": "daikuan", "nicheCategory": "财经金融"},
    {"nicheName": "征信", "nichePinyin": "zhengxin", "nicheCategory": "财经金融"},
    {"nicheName": "税务", "nichePinyin": "shuiwu", "nicheCategory": "财经金融"},
    {"nicheName": "审计", "nichePinyin": "shenji", "nicheCategory": "财经金融"},
    {"nicheName": "财务", "nichePinyin": "caiwu", "nicheCategory": "财经金融"},
    {"nicheName": "证券", "nichePinyin": "zhengquan", "nicheCategory": "财经金融"},
    {"nicheName": "期货交易", "nichePinyin": "qihuojiaoyi", "nicheCategory": "财经金融"},
    {"nicheName": "股票分析", "nichePinyin": "gupiaofenxi", "nicheCategory": "财经金融"},
    {"nicheName": "基金投资", "nichePinyin": "jijintouzi", "nicheCategory": "财经金融"},
    {"nicheName": "理财规划", "nichePinyin": "licaiguihua", "nicheCategory": "财经金融"},
    {"nicheName": "保险规划", "nichePinyin": "baoxianguihua", "nicheCategory": "财经金融"},
    {"nicheName": "车险", "nichePinyin": "chebaoxian", "nicheCategory": "财经金融"},
    {"nicheName": "寿险", "nichePinyin": "shoubaoxian", "nicheCategory": "财经金融"},
    {"nicheName": "健康险", "nichePinyin": "jiankangbaoxian", "nicheCategory": "财经金融"},
    {"nicheName": "意外险", "nichePinyin": "yiwaibaoxian", "nicheCategory": "财经金融"},
    {"nicheName": "财产险", "nichePinyin": "caichanbaoxian", "nicheCategory": "财经金融"},
    {"nicheName": "贷款申请", "nichePinyin": "daikuan shenqing", "nicheCategory": "财经金融"},
    {"nicheName": "房贷", "nichePinyin": "fangdai", "nicheCategory": "财经金融"},
    {"nicheName": "车贷", "nichePinyin": "chedai", "nicheCategory": "财经金融"},
    {"nicheName": "消费贷", "nichePinyin": "xiaofeidai", "nicheCategory": "财经金融"},
    {"nicheName": "经营贷", "nichePinyin": "jingyingdai", "nicheCategory": "财经金融"},
    {"nicheName": "信用贷", "nichePinyin": "xinyongdai", "nicheCategory": "财经金融"},
    {"nicheName": "抵押贷", "nichePinyin": "diyadai", "nicheCategory": "财经金融"},
    {"nicheName": "征信查询", "nichePinyin": "zhengxin chaxun", "nicheCategory": "财经金融"},
    {"nicheName": "征信修复", "nichePinyin": "zhengxin xiufu", "nicheCategory": "财经金融"},
    {"nicheName": "税务筹划", "nichePinyin": "shuiwu chouhua", "nicheCategory": "财经金融"},
    {"nicheName": "税务申报", "nichePinyin": "shuiwu shenbao", "nicheCategory": "财经金融"},
    {"nicheName": "财务报表", "nichePinyin": "caiwu baobiao", "nicheCategory": "财经金融"},
    {"nicheName": "财务管理", "nichePinyin": "caiwu guanli", "nicheCategory": "财经金融"},
    {"nicheName": "投资理财", "nichePinyin": "touzi licai", "nicheCategory": "财经金融"},
]

def get_template_variant(niche_name):
    """根据行业名称分配模板变体"""
    VARIANTS = ['variant-blue', 'variant-green', 'variant-orange', 'variant-purple', 'variant-dark']
    hash_val = sum(ord(c) for c in niche_name)
    return VARIANTS[hash_val % len(VARIANTS)]

def create_niche_config(niche):
    """创建行业站配置"""
    config = {
        "siteType": "niche",
        "nicheName": niche["nicheName"],
        "nichePinyin": niche["nichePinyin"],
        "nicheCategory": niche["nicheCategory"],
        "siteTitle": f"{niche['nicheName']}导航 - 最全的{niche['nicheName']}网站导航",
        "siteDescription": f"{niche['nicheName']}导航站，汇集{niche['nicheName']}最优质的官方网站和资源，一站式满足您的所有需求。",
        "variant": get_template_variant(niche["nicheName"]),
        "contact": {
            "email": "931249697@qq.com",
            "qq": "931249697"
        },
        "categories": [
            {
                "name": "官方网站",
                "links": [
                    {"name": "百度搜索", "url": f"https://www.baidu.com/s?wd={niche['nicheName']}", "desc": f"搜索{niche['nicheName']}相关信息"},
                    {"name": "知乎话题", "url": "https://www.zhihu.com/", "desc": f"{niche['nicheName']}经验问答"},
                    {"name": "小红书", "url": "https://www.xiaohongshu.com/", "desc": f"{niche['nicheName']}经验分享"}
                ]
            },
            {
                "name": "学习资源",
                "links": [
                    {"name": "B站视频", "url": f"https://search.bilibili.com/all?keyword={niche['nicheName']}", "desc": f"{niche['nicheName']}视频教程"},
                    {"name": "知乎问答", "url": "https://www.zhihu.com/", "desc": f"{niche['nicheName']}问答社区"},
                    {"name": "豆瓣小组", "url": "https://www.douban.com/", "desc": f"{niche['nicheName']}交流小组"}
                ]
            },
            {
                "name": "工具软件",
                "links": [
                    {"name": "百度搜索", "url": f"https://www.baidu.com/s?wd={niche['nicheName']}工具", "desc": f"搜索{niche['nicheName']}相关工具"},
                    {"name": "知乎推荐", "url": "https://www.zhihu.com/", "desc": f"{niche['nicheName']}工具推荐"}
                ]
            },
            {
                "name": "社区论坛",
                "links": [
                    {"name": "知乎", "url": "https://www.zhihu.com/", "desc": f"{niche['nicheName']}交流社区"},
                    {"name": "豆瓣", "url": "https://www.douban.com/", "desc": f"{niche['nicheName']}分享社区"},
                    {"name": "贴吧", "url": "https://tieba.baidu.com/", "desc": f"{niche['nicheName']}贴吧"}
                ]
            },
            {
                "name": "资讯媒体",
                "links": [
                    {"name": "人民网", "url": "http://www.people.com.cn/", "desc": "新闻资讯"},
                    {"name": "新华网", "url": "http://www.xinhuanet.com/", "desc": "新闻资讯"}
                ]
            },
            {
                "name": "综合平台",
                "links": [
                    {"name": "百度搜索", "url": f"https://www.baidu.com/s?wd={niche['nicheName']}", "desc": f"百度搜索{niche['nicheName']}相关信息"},
                    {"name": "B站视频", "url": f"https://search.bilibili.com/all?keyword={niche['nicheName']}", "desc": f"B站{niche['nicheName']}视频教程"},
                    {"name": "微博", "url": f"https://s.weibo.com/weibo?q={niche['nicheName']}", "desc": f"微博{niche['nicheName']}热门话题"}
                ]
            }
        ]
    }
    return config

def generate_niche_site(niche):
    """生成行业站文件"""
    site_dir = SITES_DIR / niche["nichePinyin"]
    site_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建config.json
    config = create_niche_config(niche)
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
Sitemap: https://{niche['nichePinyin']}-nav.pages.dev/sitemap.xml
""")
    
    (site_dir / "sitemap.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://{niche['nichePinyin']}-nav.pages.dev/</loc>
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

def expand_niches(target_count=500):
    """扩展行业站"""
    print("\n" + "="*60)
    print(f"🎯 行业扩展器 - 目标: {target_count} 个行业站")
    print("="*60)
    
    # 获取现有行业
    existing_niches = [d.name for d in SITES_DIR.iterdir() if d.is_dir()]
    existing_count = len(existing_niches)
    
    print(f"现有行业站: {existing_count} 个")
    print(f"目标行业站: {target_count} 个")
    print(f"需要新增: {target_count - existing_count} 个")
    
    # 从niches.json读取行业数据
    niches_data = load_json(DATA_DIR / "niches.json")
    
    # 找出需要新增的行业
    new_niches = []
    for niche in niches_data:
        niche_pinyin = niche.get("nichePinyin", "")
        if niche_pinyin and niche_pinyin not in existing_niches:
            new_niches.append(niche)
    
    # 扩展到目标数量
    niches_to_add = new_niches[:target_count - existing_count]
    
    print(f"\n开始生成 {len(niches_to_add)} 个新行业站...")
    
    created = 0
    for niche in niches_to_add:
        generate_niche_site(niche)
        created += 1
        print(f"  ✅ {niche['nicheName']} ({niche['nicheCategory']})")
    
    print("\n" + "="*60)
    print(f"✅ 扩展完成: 新增 {created} 个行业站")
    print(f"当前总数: {existing_count + created} 个")
    print("="*60)
    
    # 更新niches.json
    all_niche_configs = []
    for niche_dir in SITES_DIR.iterdir():
        if niche_dir.is_dir():
            config_file = niche_dir / "config.json"
            if config_file.exists():
                all_niche_configs.append(json.loads(config_file.read_text()))
    
    (DATA_DIR / "niches.json").write_text(json.dumps(all_niche_configs, indent=2))
    print(f"✅ 已更新 niches.json")

def show_niche_stats():
    """显示行业站统计"""
    existing_count = sum(1 for d in SITES_DIR.iterdir() if d.is_dir())
    
    print("\n" + "="*60)
    print("📊 行业站统计")
    print("="*60)
    print(f"当前行业站: {existing_count} 个")
    print(f"目标行业站: 500 个")
    print(f"进度: {existing_count / 500 * 100:.1f}%")
    
    # 按类别统计
    categories = {}
    for niche_dir in SITES_DIR.iterdir():
        if niche_dir.is_dir():
            config_file = niche_dir / "config.json"
            if config_file.exists():
                config = json.loads(config_file.read_text())
                category = config.get("nicheCategory", "未知")
                categories[category] = categories.get(category, 0) + 1
    
    print("\n按类别分布:")
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count} 个")

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "expand":
            target = int(sys.argv[2]) if len(sys.argv) > 2 else 500
            expand_niches(target)
        elif command == "stats":
            show_niche_stats()
        elif command == "generate":
            if len(sys.argv) >= 3:
                niche_pinyin = sys.argv[2]
                niche_data = next((n for n in ALL_NICHES if n["nichePinyin"] == niche_pinyin), None)
                if niche_data:
                    generate_niche_site(niche_data)
                    print(f"✅ 已生成: {niche_data['nicheName']}")
                else:
                    print(f"❌ 未找到行业: {niche_pinyin}")
        else:
            print("用法: python niche_expander.py [expand|stats|generate]")
    else:
        # 默认扩展到500个
        expand_niches(500)

if __name__ == "__main__":
    main()