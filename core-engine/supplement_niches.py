#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行业数据补充脚本 - supplement_niches.py
补充缺失的行业数据到500个
"""

import json
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"

# 补充的行业数据（231个）
SUPPLEMENT_NICHES = [
    # 更多教育培训类
    {"nicheName": "一级建造师", "nichePinyin": "yijijianzaoshi", "nicheCategory": "教育培训"},
    {"nicheName": "二级建造师", "nichePinyin": "erjijianzaoshi", "nicheCategory": "教育培训"},
    {"nicheName": "造价工程师", "nichePinyin": "zaojiagongchengshi", "nicheCategory": "教育培训"},
    {"nicheName": "监理工程师", "nichePinyin": "jianligongchengshi", "nicheCategory": "教育培训"},
    {"nicheName": "消防工程师", "nichePinyin": "xiaofanggongchengshi", "nicheCategory": "教育培训"},
    {"nicheName": "安全工程师", "nichePinyin": "anquangongchengshi", "nicheCategory": "教育培训"},
    {"nicheName": "电气工程师", "nichePinyin": "dianqigongchengshi", "nicheCategory": "教育培训"},
    {"nicheName": "机械工程师", "nichePinyin": "jixiegongchengshi", "nicheCategory": "教育培训"},
    {"nicheName": "软件工程师", "nichePinyin": "ruanjiangongchengshi", "nicheCategory": "教育培训"},
    {"nicheName": "网络工程师", "nichePinyin": "wangluogongchengshi", "nicheCategory": "教育培训"},
    {"nicheName": "医师资格证", "nichePinyin": "yishizigezheng", "nicheCategory": "教育培训"},
    {"nicheName": "护士资格证", "nichePinyin": "hushizigezheng", "nicheCategory": "教育培训"},
    {"nicheName": "药师资格证", "nichePinyin": "yaoshizigezheng", "nicheCategory": "教育培训"},
    {"nicheName": "心理咨询师", "nichePinyin": "xinlizixunshi", "nicheCategory": "教育培训"},
    {"nicheName": "营养师", "nichePinyin": "yingyangshi", "nicheCategory": "教育培训"},
    {"nicheName": "健身教练", "nichePinyin": "jianshenjiaolian", "nicheCategory": "教育培训"},
    {"nicheName": "瑜伽教练", "nichePinyin": "yujiiajiaolian", "nicheCategory": "教育培训"},
    {"nicheName": "舞蹈教练", "nichePinyin": "wudaojiaolian", "nicheCategory": "教育培训"},
    {"nicheName": "音乐教师", "nichePinyin": "yinyuejiaoshi", "nicheCategory": "教育培训"},
    {"nicheName": "美术教师", "nichePinyin": "meishujiaoshi", "nicheCategory": "教育培训"},
    
    # 更多生活服务类
    {"nicheName": "婚介", "nichePinyin": "hunjie", "nicheCategory": "生活服务"},
    {"nicheName": "相亲", "nichePinyin": "xiangqin", "nicheCategory": "生活服务"},
    {"nicheName": "交友", "nichePinyin": "jiaoyou", "nicheCategory": "生活服务"},
    {"nicheName": "婚恋", "nichePinyin": "hunlian", "nicheCategory": "生活服务"},
    {"nicheName": "婚礼主持", "nichePinyin": "hunlizhuchi", "nicheCategory": "生活服务"},
    {"nicheName": "婚礼司仪", "nichePinyin": "hunli siyi", "nicheCategory": "生活服务"},
    {"nicheName": "婚礼跟拍", "nichePinyin": "hunligenpai", "nicheCategory": "生活服务"},
    {"nicheName": "婚礼车队", "nichePinyin": "hunliche dui", "nicheCategory": "生活服务"},
    {"nicheName": "婚礼场地", "nichePinyin": "hunlichangdi", "nicheCategory": "生活服务"},
    {"nicheName": "婚纱礼服", "nichePinyin": "hunshalifu", "nicheCategory": "生活服务"},
    {"nicheName": "婚戒首饰", "nichePinyin": "hunjieshoushi", "nicheCategory": "生活服务"},
    {"nicheName": "婚礼鲜花", "nichePinyin": "hunli xianhua", "nicheCategory": "生活服务"},
    {"nicheName": "婚礼蛋糕", "nichePinyin": "hunli dangao", "nicheCategory": "生活服务"},
    {"nicheName": "婚礼请柬", "nichePinyin": "hunliqingjian", "nicheCategory": "生活服务"},
    {"nicheName": "婚礼用品", "nichePinyin": "hunliyongpin", "nicheCategory": "生活服务"},
    
    # 更多健康医疗类
    {"nicheName": "体检", "nichePinyin": "tijian", "nicheCategory": "健康医疗"},
    {"nicheName": "疫苗", "nichePinyin": "yimiao", "nicheCategory": "健康医疗"},
    {"nicheName": "挂号", "nichePinyin": "guahao", "nicheCategory": "健康医疗"},
    {"nicheName": "问诊", "nichePinyin": "wenzhen", "nicheCategory": "健康医疗"},
    {"nicheName": "药店", "nichePinyin": "yaodian", "nicheCategory": "健康医疗"},
    {"nicheName": "药房", "nichePinyin": "yaofang", "nicheCategory": "健康医疗"},
    {"nicheName": "医疗器械", "nichePinyin": "yiliaoqixie", "nicheCategory": "健康医疗"},
    {"nicheName": "医疗设备", "nichePinyin": "yiliaoshebei", "nicheCategory": "健康医疗"},
    {"nicheName": "医疗用品", "nichePinyin": "yiliaoyongpin", "nicheCategory": "健康医疗"},
    {"nicheName": "保健品", "nichePinyin": "baojianpin", "nicheCategory": "健康医疗"},
    {"nicheName": "营养品", "nichePinyin": "yingyangpin", "nicheCategory": "健康医疗"},
    {"nicheName": "保健食品", "nichePinyin": "baojian shipin", "nicheCategory": "健康医疗"},
    {"nicheName": "减肥产品", "nichePinyin": "jianfei chanpin", "nicheCategory": "健康医疗"},
    {"nicheName": "健身器材", "nichePinyin": "jianshen qixie", "nicheCategory": "健康医疗"},
    {"nicheName": "健身用品", "nichePinyin": "jianshen yongpin", "nicheCategory": "健康医疗"},
    {"nicheName": "瑜伽用品", "nichePinyin": "yujia yongpin", "nicheCategory": "健康医疗"},
    {"nicheName": "跑步装备", "nichePinyin": "paobu zhuangbei", "nicheCategory": "健康医疗"},
    {"nicheName": "游泳装备", "nichePinyin": "youyong zhuangbei", "nicheCategory": "健康医疗"},
    {"nicheName": "运动装备", "nichePinyin": "yundong zhuangbei", "nicheCategory": "健康医疗"},
    {"nicheName": "户外运动", "nichePinyin": "huwai yundong", "nicheCategory": "健康医疗"},
    
    # 更多财经金融类
    {"nicheName": "投资顾问", "nichePinyin": "touzi guwen", "nicheCategory": "财经金融"},
    {"nicheName": "理财顾问", "nichePinyin": "licai guwen", "nicheCategory": "财经金融"},
    {"nicheName": "保险顾问", "nichePinyin": "baoxian guwen", "nicheCategory": "财经金融"},
    {"nicheName": "贷款顾问", "nichePinyin": "daikuan guwen", "nicheCategory": "财经金融"},
    {"nicheName": "税务顾问", "nichePinyin": "shuiwu guwen", "nicheCategory": "财经金融"},
    {"nicheName": "财务顾问", "nichePinyin": "caiwu guwen", "nicheCategory": "财经金融"},
    {"nicheName": "投资公司", "nichePinyin": "touzi gongsi", "nicheCategory": "财经金融"},
    {"nicheName": "理财公司", "nichePinyin": "licai gongsi", "nicheCategory": "财经金融"},
    {"nicheName": "保险公司", "nichePinyin": "baoxian gongsi", "nicheCategory": "财经金融"},
    {"nicheName": "贷款公司", "nichePinyin": "daikuan gongsi", "nicheCategory": "财经金融"},
    {"nicheName": "担保公司", "nichePinyin": "danbao gongsi", "nicheCategory": "财经金融"},
    {"nicheName": "典当公司", "nichePinyin": "dian dang gongsi", "nicheCategory": "财经金融"},
    {"nicheName": "拍卖公司", "nichePinyin": "paimai gongsi", "nicheCategory": "财经金融"},
    {"nicheName": "评估公司", "nichePinyin": "pinggu gongsi", "nicheCategory": "财经金融"},
    {"nicheName": "审计公司", "nichePinyin": "shenji gongsi", "nicheCategory": "财经金融"},
    {"nicheName": "会计师事务所", "nichePinyin": "kuaiji shiwu suo", "nicheCategory": "财经金融"},
    {"nicheName": "律师事务所", "nichePinyin": "lvshi shiwu suo", "nicheCategory": "财经金融"},
    {"nicheName": "公证处", "nichePinyin": "gongzhengchu", "nicheCategory": "财经金融"},
    {"nicheName": "仲裁机构", "nichePinyin": "zhongcai jiguan", "nicheCategory": "财经金融"},
    {"nicheName": "调解机构", "nichePinyin": "tiaojie jiguan", "nicheCategory": "财经金融"},
    
    # 更多行业领域
    {"nicheName": "房产", "nichePinyin": "fangchan", "nicheCategory": "房产家居"},
    {"nicheName": "租房", "nichePinyin": "zufang", "nicheCategory": "房产家居"},
    {"nicheName": "买房", "nichePinyin": "maifang", "nicheCategory": "房产家居"},
    {"nicheName": "卖房", "nichePinyin": "maifang", "nicheCategory": "房产家居"},
    {"nicheName": "二手房", "nichePinyin": "ershoufang", "nicheCategory": "房产家居"},
    {"nicheName": "新房", "nichePinyin": "xinfang", "nicheCategory": "房产家居"},
    {"nicheName": "楼盘", "nichePinyin": "loupan", "nicheCategory": "房产家居"},
    {"nicheName": "小区", "nichePinyin": "xiaoqu", "nicheCategory": "房产家居"},
    {"nicheName": "别墅", "nichePinyin": "bieshu", "nicheCategory": "房产家居"},
    {"nicheName": "商铺", "nichePinyin": "shangpu", "nicheCategory": "房产家居"},
    {"nicheName": "写字楼", "nichePinyin": "xiezilou", "nicheCategory": "房产家居"},
    {"nicheName": "厂房", "nichePinyin": "changfang", "nicheCategory": "房产家居"},
    {"nicheName": "仓库", "nichePinyin": "cangku", "nicheCategory": "房产家居"},
    {"nicheName": "土地", "nichePinyin": "tudi", "nicheCategory": "房产家居"},
    {"nicheName": "房产中介", "nichePinyin": "fangchan zhongjie", "nicheCategory": "房产家居"},
    {"nicheName": "房产评估", "nichePinyin": "fangchan pinggu", "nicheCategory": "房产家居"},
    {"nicheName": "房产交易", "nichePinyin": "fangchan jiaoyi", "nicheCategory": "房产家居"},
    {"nicheName": "房产投资", "nichePinyin": "fangchan touzi", "nicheCategory": "房产家居"},
    {"nicheName": "房产租赁", "nichePinyin": "fangchan zulin", "nicheCategory": "房产家居"},
    {"nicheName": "房产管理", "nichePinyin": "fangchan guanli", "nicheCategory": "房产家居"},
    
    # 更多家居生活类
    {"nicheName": "家具", "nichePinyin": "jiaju", "nicheCategory": "房产家居"},
    {"nicheName": "家电", "nichePinyin": "jiadian", "nicheCategory": "房产家居"},
    {"nicheName": "家居", "nichePinyin": "jiaju", "nicheCategory": "房产家居"},
    {"nicheName": "家装", "nichePinyin": "jiazhuang", "nicheCategory": "房产家居"},
    {"nicheName": "建材", "nichePinyin": "jiancai", "nicheCategory": "房产家居"},
    {"nicheName": "卫浴", "nichePinyin": "weiyu", "nicheCategory": "房产家居"},
    {"nicheName": "厨房", "nichePinyin": "chufang", "nicheCategory": "房产家居"},
    {"nicheName": "灯具", "nichePinyin": "dengju", "nicheCategory": "房产家居"},
    {"nicheName": "窗帘", "nichePinyin": "chuanglian", "nicheCategory": "房产家居"},
    {"nicheName": "地毯", "nichePinyin": "ditan", "nicheCategory": "房产家居"},
    {"nicheName": "壁纸", "nichePinyin": "bizhi", "nicheCategory": "房产家居"},
    {"nicheName": "油漆", "nichePinyin": "youqi", "nicheCategory": "房产家居"},
    {"nicheName": "地板", "nichePinyin": "diban", "nicheCategory": "房产家居"},
    {"nicheName": "瓷砖", "nichePinyin": "cizhuan", "nicheCategory": "房产家居"},
    {"nicheName": "门窗", "nichePinyin": "menchuang", "nicheCategory": "房产家居"},
    {"nicheName": "楼梯", "nichePinyin": "louti", "nicheCategory": "房产家居"},
    {"nicheName": "阳台", "nichePinyin": "yangtai", "nicheCategory": "房产家居"},
    {"nicheName": "花园", "nichePinyin": "huayuan", "nicheCategory": "房产家居"},
    {"nicheName": "园艺", "nichePinyin": "yuanyi", "nicheCategory": "房产家居"},
    {"nicheName": "绿植", "nichePinyin": "lvzhi", "nicheCategory": "房产家居"},
    
    # 更多汽车交通类
    {"nicheName": "汽车", "nichePinyin": "qiche", "nicheCategory": "汽车交通"},
    {"nicheName": "买车", "nichePinyin": "maiche", "nicheCategory": "汽车交通"},
    {"nicheName": "卖车", "nichePinyin": "maiche", "nicheCategory": "汽车交通"},
    {"nicheName": "二手车", "nichePinyin": "ershouche", "nicheCategory": "汽车交通"},
    {"nicheName": "新车", "nichePinyin": "xinche", "nicheCategory": "汽车交通"},
    {"nicheName": "汽车品牌", "nichePinyin": "qiche pinpai", "nicheCategory": "汽车交通"},
    {"nicheName": "汽车报价", "nichePinyin": "qiche baojia", "nicheCategory": "汽车交通"},
    {"nicheName": "汽车评测", "nichePinyin": "qiche pingce", "nicheCategory": "汽车交通"},
    {"nicheName": "汽车导购", "nichePinyin": "qiche daogou", "nicheCategory": "汽车交通"},
    {"nicheName": "汽车保险", "nichePinyin": "qiche baoxian", "nicheCategory": "汽车交通"},
    {"nicheName": "汽车贷款", "nichePinyin": "qiche daikuan", "nicheCategory": "汽车交通"},
    {"nicheName": "汽车租赁", "nichePinyin": "qiche zulin", "nicheCategory": "汽车交通"},
    {"nicheName": "汽车用品", "nichePinyin": "qiche yongpin", "nicheCategory": "汽车交通"},
    {"nicheName": "汽车配件", "nichePinyin": "qiche peijian", "nicheCategory": "汽车交通"},
    {"nicheName": "汽车改装", "nichePinyin": "qiche gaizhuang", "nicheCategory": "汽车交通"},
    {"nicheName": "汽车美容", "nichePinyin": "qiche meirong", "nicheCategory": "汽车交通"},
    {"nicheName": "汽车保养", "nichePinyin": "qiche baoyang", "nicheCategory": "汽车交通"},
    {"nicheName": "汽车维修", "nichePinyin": "qiche weixiu", "nicheCategory": "汽车交通"},
    {"nicheName": "驾校", "nichePinyin": "jiaxiao", "nicheCategory": "汽车交通"},
    {"nicheName": "驾照", "nichePinyin": "jiazhao", "nicheCategory": "汽车交通"},
    
    # 更多旅游出行类
    {"nicheName": "旅游", "nichePinyin": "lvyou", "nicheCategory": "旅游出行"},
    {"nicheName": "旅行", "nichePinyin": "lvxing", "nicheCategory": "旅游出行"},
    {"nicheName": "景点", "nichePinyin": "jingdian", "nicheCategory": "旅游出行"},
    {"nicheName": "景区", "nichePinyin": "jingqu", "nicheCategory": "旅游出行"},
    {"nicheName": "门票", "nichePinyin": "menpiao", "nicheCategory": "旅游出行"},
    {"nicheName": "酒店", "nichePinyin": "jiudian", "nicheCategory": "旅游出行"},
    {"nicheName": "民宿", "nichePinyin": "minsu", "nicheCategory": "旅游出行"},
    {"nicheName": "客栈", "nichePinyin": "kezhan", "nicheCategory": "旅游出行"},
    {"nicheName": "青年旅舍", "nichePinyin": "qingnian lvshe", "nicheCategory": "旅游出行"},
    {"nicheName": "度假村", "nichePinyin": "dujiacun", "nicheCategory": "旅游出行"},
    {"nicheName": "旅行社", "nichePinyin": "lvxingshe", "nicheCategory": "旅游出行"},
    {"nicheName": "旅游攻略", "nichePinyin": "lvyou gonglve", "nicheCategory": "旅游出行"},
    {"nicheName": "旅游路线", "nichePinyin": "lvyou luxian", "nicheCategory": "旅游出行"},
    {"nicheName": "旅游团", "nichePinyin": "lvyou tuan", "nicheCategory": "旅游出行"},
    {"nicheName": "自由行", "nichePinyin": "ziyouxing", "nicheCategory": "旅游出行"},
    {"nicheName": "跟团游", "nichePinyin": "gentuanyou", "nicheCategory": "旅游出行"},
    {"nicheName": "自驾游", "nichePinyin": "zijia you", "nicheCategory": "旅游出行"},
    {"nicheName": "出境游", "nichePinyin": "chujingyou", "nicheCategory": "旅游出行"},
    {"nicheName": "国内游", "nichePinyin": "guoneiyou", "nicheCategory": "旅游出行"},
    {"nicheName": "周边游", "nichePinyin": "zhoubianyou", "nicheCategory": "旅游出行"},
    
    # 更多餐饮美食类
    {"nicheName": "美食", "nichePinyin": "meishi", "nicheCategory": "餐饮美食"},
    {"nicheName": "餐厅", "nichePinyin": "canting", "nicheCategory": "餐饮美食"},
    {"nicheName": "饭店", "nichePinyin": "fandian", "nicheCategory": "餐饮美食"},
    {"nicheName": "小吃", "nichePinyin": "xiaochi", "nicheCategory": "餐饮美食"},
    {"nicheName": "快餐", "nichePinyin": "kuai can", "nicheCategory": "餐饮美食"},
    {"nicheName": "火锅", "nichePinyin": "huoguo", "nicheCategory": "餐饮美食"},
    {"nicheName": "烧烤", "nichePinyin": "shaokao", "nicheCategory": "餐饮美食"},
    {"nicheName": "海鲜", "nichePinyin": "haixian", "nicheCategory": "餐饮美食"},
    {"nicheName": "西餐", "nichePinyin": "xi can", "nicheCategory": "餐饮美食"},
    {"nicheName": "日料", "nichePinyin": "riliao", "nicheCategory": "餐饮美食"},
    {"nicheName": "韩餐", "nichePinyin": "han can", "nicheCategory": "餐饮美食"},
    {"nicheName": "中餐", "nichePinyin": "zhong can", "nicheCategory": "餐饮美食"},
    {"nicheName": "甜品", "nichePinyin": "tianpin", "nicheCategory": "餐饮美食"},
    {"nicheName": "饮品", "nichePinyin": "yinpin", "nicheCategory": "餐饮美食"},
    {"nicheName": "咖啡", "nichePinyin": "kafei", "nicheCategory": "餐饮美食"},
    {"nicheName": "茶饮", "nichePinyin": "chayin", "nicheCategory": "餐饮美食"},
    {"nicheName": "酒水", "nichePinyin": "jiushui", "nicheCategory": "餐饮美食"},
    {"nicheName": "酒吧", "nichePinyin": "jiuba", "nicheCategory": "餐饮美食"},
    {"nicheName": "夜宵", "nichePinyin": "ye xiao", "nicheCategory": "餐饮美食"},
    {"nicheName": "早餐", "nichePinyin": "zao can", "nicheCategory": "餐饮美食"},
    
    # 更多购物消费类
    {"nicheName": "购物", "nichePinyin": "gouwu", "nicheCategory": "购物消费"},
    {"nicheName": "商城", "nichePinyin": "shangcheng", "nicheCategory": "购物消费"},
    {"nicheName": "超市", "nichePinyin": "chaoshi", "nicheCategory": "购物消费"},
    {"nicheName": "便利店", "nichePinyin": "bianli dian", "nicheCategory": "购物消费"},
    {"nicheName": "百货", "nichePinyin": "baihuo", "nicheCategory": "购物消费"},
    {"nicheName": "服装", "nichePinyin": "fuzhuang", "nicheCategory": "购物消费"},
    {"nicheName": "鞋帽", "nichePinyin": "xie mao", "nicheCategory": "购物消费"},
    {"nicheName": "箱包", "nichePinyin": "xiangbao", "nicheCategory": "购物消费"},
    {"nicheName": "饰品", "nichePinyin": "shipin", "nicheCategory": "购物消费"},
    {"nicheName": "珠宝", "nichePinyin": "zhubao", "nicheCategory": "购物消费"},
    {"nicheName": "手表", "nichePinyin": "shoubiao", "nicheCategory": "购物消费"},
    {"nicheName": "眼镜", "nichePinyin": "yanjing", "nicheCategory": "购物消费"},
    {"nicheName": "化妆品", "nichePinyin": "huazhuang pin", "nicheCategory": "购物消费"},
    {"nicheName": "护肤品", "nichePinyin": "hufu pin", "nicheCategory": "购物消费"},
    {"nicheName": "香水", "nichePinyin": "xiangshui", "nicheCategory": "购物消费"},
    {"nicheName": "母婴用品", "nichePinyin": "muying yongpin", "nicheCategory": "购物消费"},
    {"nicheName": "儿童用品", "nichePinyin": "ertong yongpin", "nicheCategory": "购物消费"},
    {"nicheName": "玩具", "nichePinyin": "wanju", "nicheCategory": "购物消费"},
    {"nicheName": "图书", "nichePinyin": "tushu", "nicheCategory": "购物消费"},
    {"nicheName": "文具", "nichePinyin": "wenju", "nicheCategory": "购物消费"},
    
    # 更多娱乐休闲类
    {"nicheName": "娱乐", "nichePinyin": "yule", "nicheCategory": "娱乐休闲"},
    {"nicheName": "休闲", "nichePinyin": "xiuxian", "nicheCategory": "娱乐休闲"},
    {"nicheName": "电影", "nichePinyin": "dianying", "nicheCategory": "娱乐休闲"},
    {"nicheName": "影视", "nichePinyin": "yingshi", "nicheCategory": "娱乐休闲"},
    {"nicheName": "音乐", "nichePinyin": "yinyue", "nicheCategory": "娱乐休闲"},
    {"nicheName": "游戏", "nichePinyin": "youxi", "nicheCategory": "娱乐休闲"},
    {"nicheName": "动漫", "nichePinyin": "dongman", "nicheCategory": "娱乐休闲"},
    {"nicheName": "综艺", "nichePinyin": "zongyi", "nicheCategory": "娱乐休闲"},
    {"nicheName": "直播", "nichePinyin": "zhibo", "nicheCategory": "娱乐休闲"},
    {"nicheName": "短视频", "nichePinyin": "duan shipin", "nicheCategory": "娱乐休闲"},
    {"nicheName": "小说", "nichePinyin": "xiaoshuo", "nicheCategory": "娱乐休闲"},
    {"nicheName": "漫画", "nichePinyin": "manhua", "nicheCategory": "娱乐休闲"},
    {"nicheName": "棋牌", "nichePinyin": "qipai", "nicheCategory": "娱乐休闲"},
    {"nicheName": "麻将", "nichePinyin": "majiang", "nicheCategory": "娱乐休闲"},
    {"nicheName": "象棋", "nichePinyin": "xiangqi", "nicheCategory": "娱乐休闲"},
    {"nicheName": "围棋", "nichePinyin": "weiqi", "nicheCategory": "娱乐休闲"},
    {"nicheName": "球类", "nichePinyin": "qiulei", "nicheCategory": "娱乐休闲"},
    {"nicheName": "足球", "nichePinyin": "zuqiu", "nicheCategory": "娱乐休闲"},
    {"nicheName": "篮球", "nichePinyin": "lanqiu", "nicheCategory": "娱乐休闲"},
    {"nicheName": "羽毛球", "nichePinyin": "yumaoqiu", "nicheCategory": "娱乐休闲"},
    
    # 更多体育健身类
    {"nicheName": "体育", "nichePinyin": "tiyu", "nicheCategory": "体育健身"},
    {"nicheName": "健身", "nichePinyin": "jianshen", "nicheCategory": "体育健身"},
    {"nicheName": "运动", "nichePinyin": "yundong", "nicheCategory": "体育健身"},
    {"nicheName": "健身房", "nichePinyin": "jianshenfang", "nicheCategory": "体育健身"},
    {"nicheName": "健身器材", "nichePinyin": "jianshen qixie", "nicheCategory": "体育健身"},
    {"nicheName": "瑜伽", "nichePinyin": "yujia", "nicheCategory": "体育健身"},
    {"nicheName": "瑜伽馆", "nichePinyin": "yujia guan", "nicheCategory": "体育健身"},
    {"nicheName": "舞蹈", "nichePinyin": "wudao", "nicheCategory": "体育健身"},
    {"nicheName": "舞蹈培训", "nichePinyin": "wudao peixun", "nicheCategory": "体育健身"},
    {"nicheName": "游泳馆", "nichePinyin": "youyong guan", "nicheCategory": "体育健身"},
    {"nicheName": "游泳培训", "nichePinyin": "youyong peixun", "nicheCategory": "体育健身"},
    {"nicheName": "跑步", "nichePinyin": "paobu", "nicheCategory": "体育健身"},
    {"nicheName": "马拉松", "nichePinyin": "malasong", "nicheCategory": "体育健身"},
    {"nicheName": "骑行", "nichePinyin": "qixing", "nicheCategory": "体育健身"},
    {"nicheName": "攀岩", "nichePinyin": "panyan", "nicheCategory": "体育健身"},
    {"nicheName": "滑雪", "nichePinyin": "huaxue", "nicheCategory": "体育健身"},
    {"nicheName": "潜水", "nichePinyin": "qianshui", "nicheCategory": "体育健身"},
    {"nicheName": "冲浪", "nichePinyin": "chonglang", "nicheCategory": "体育健身"},
    {"nicheName": "蹦极", "nichePinyin": "bengji", "nicheCategory": "体育健身"},
    {"nicheName": "跳伞", "nichePinyin": "tiaosan", "nicheCategory": "体育健身"},
    
    # 更多文化艺术类
    {"nicheName": "文化", "nichePinyin": "wenhua", "nicheCategory": "文化艺术"},
    {"nicheName": "艺术", "nichePinyin": "yishu", "nicheCategory": "文化艺术"},
    {"nicheName": "绘画", "nichePinyin": "huahua", "nicheCategory": "文化艺术"},
    {"nicheName": "书法", "nichePinyin": "shufa", "nicheCategory": "文化艺术"},
    {"nicheName": "摄影", "nichePinyin": "sheying", "nicheCategory": "文化艺术"},
    {"nicheName": "雕塑", "nichePinyin": "diaosu", "nicheCategory": "文化艺术"},
    {"nicheName": "陶艺", "nichePinyin": "taoyi", "nicheCategory": "文化艺术"},
    {"nicheName": "刺绣", "nichePinyin": "cixiu", "nicheCategory": "文化艺术"},
    {"nicheName": "剪纸", "nichePinyin": "jianzhi", "nicheCategory": "文化艺术"},
    {"nicheName": "编织", "nichePinyin": "bianzhi", "nicheCategory": "文化艺术"},
    {"nicheName": "乐器", "nichePinyin": "yueqi", "nicheCategory": "文化艺术"},
    {"nicheName": "音乐", "nichePinyin": "yinyue", "nicheCategory": "文化艺术"},
    {"nicheName": "舞蹈", "nichePinyin": "wudao", "nicheCategory": "文化艺术"},
    {"nicheName": "戏剧", "nichePinyin": "xiju", "nicheCategory": "文化艺术"},
    {"nicheName": "戏曲", "nichePinyin": "xiqu", "nicheCategory": "文化艺术"},
    {"nicheName": "话剧", "nichePinyin": "huaju", "nicheCategory": "文化艺术"},
    {"nicheName": "歌剧", "nichePinyin": "geju", "nicheCategory": "文化艺术"},
    {"nicheName": "音乐会", "nichePinyin": "yinyue hui", "nicheCategory": "文化艺术"},
    {"nicheName": "展览", "nichePinyin": "zhanlan", "nicheCategory": "文化艺术"},
    {"nicheName": "博物馆", "nichePinyin": "bowuguan", "nicheCategory": "文化艺术"},
    
    # 更多科技数码类
    {"nicheName": "科技", "nichePinyin": "keji", "nicheCategory": "科技数码"},
    {"nicheName": "数码", "nichePinyin": "shuma", "nicheCategory": "科技数码"},
    {"nicheName": "手机", "nichePinyin": "shouji", "nicheCategory": "科技数码"},
    {"nicheName": "电脑", "nichePinyin": "diannao", "nicheCategory": "科技数码"},
    {"nicheName": "平板", "nichePinyin": "pingban", "nicheCategory": "科技数码"},
    {"nicheName": "相机", "nichePinyin": "xiangji", "nicheCategory": "科技数码"},
    {"nicheName": "耳机", "nichePinyin": "erji", "nicheCategory": "科技数码"},
    {"nicheName": "音箱", "nichePinyin": "yinxiang", "nicheCategory": "科技数码"},
    {"nicheName": "智能设备", "nichePinyin": "zhineng shebei", "nicheCategory": "科技数码"},
    {"nicheName": "智能家居", "nichePinyin": "zhineng jiaju", "nicheCategory": "科技数码"},
    {"nicheName": "智能穿戴", "nichePinyin": "zhineng chuandai", "nicheCategory": "科技数码"},
    {"nicheName": "智能手表", "nichePinyin": "zhineng shoubiao", "nicheCategory": "科技数码"},
    {"nicheName": "智能眼镜", "nichePinyin": "zhineng yanjing", "nicheCategory": "科技数码"},
    {"nicheName": "无人机", "nichePinyin": "wu ren ji", "nicheCategory": "科技数码"},
    {"nicheName": "VR设备", "nichePinyin": "vr shebei", "nicheCategory": "科技数码"},
    {"nicheName": "AR设备", "nichePinyin": "ar shebei", "nicheCategory": "科技数码"},
    {"nicheName": "机器人", "nichePinyin": "jiqiren", "nicheCategory": "科技数码"},
    {"nicheName": "人工智能", "nichePinyin": "ren gong zhineng", "nicheCategory": "科技数码"},
    {"nicheName": "大数据", "nichePinyin": "da shuju", "nicheCategory": "科技数码"},
    {"nicheName": "云计算", "nichePinyin": "yun jisuan", "nicheCategory": "科技数码"},
    
    # 更多职业就业类
    {"nicheName": "招聘", "nichePinyin": "zhaopin", "nicheCategory": "职业就业"},
    {"nicheName": "求职", "nichePinyin": "qiuzhi", "nicheCategory": "职业就业"},
    {"nicheName": "就业", "nichePinyin": "jiuye", "nicheCategory": "职业就业"},
    {"nicheName": "面试", "nichePinyin": "mianshi", "nicheCategory": "职业就业"},
    {"nicheName": "简历", "nichePinyin": "jianli", "nicheCategory": "职业就业"},
    {"nicheName": "职业规划", "nichePinyin": "zhiye guihua", "nicheCategory": "职业就业"},
    {"nicheName": "职业培训", "nichePinyin": "zhiye peixun", "nicheCategory": "职业就业"},
    {"nicheName": "职业技能", "nichePinyin": "zhiye jineng", "nicheCategory": "职业就业"},
    {"nicheName": "职业资格", "nichePinyin": "zhiye zige", "nicheCategory": "职业就业"},
    {"nicheName": "职业证书", "nichePinyin": "zhiye zhengshu", "nicheCategory": "职业就业"},
    {"nicheName": "创业", "nichePinyin": "chuangye", "nicheCategory": "职业就业"},
    {"nicheName": "创业项目", "nichePinyin": "chuangye xiangmu", "nicheCategory": "职业就业"},
    {"nicheName": "创业培训", "nichePinyin": "chuangye peixun", "nicheCategory": "职业就业"},
    {"nicheName": "创业融资", "nichePinyin": "chuangye rongzi", "nicheCategory": "职业就业"},
    {"nicheName": "创业孵化", "nichePinyin": "chuangye fuhua", "nicheCategory": "职业就业"},
    {"nicheName": "创业园区", "nichePinyin": "chuangye yuanqu", "nicheCategory": "职业就业"},
    {"nicheName": "创业服务", "nichePinyin": "chuangye fuwu", "nicheCategory": "职业就业"},
    {"nicheName": "创业政策", "nichePinyin": "chuangye zhengce", "nicheCategory": "职业就业"},
    {"nicheName": "创业导师", "nichePinyin": "chuangye daoshi", "nicheCategory": "职业就业"},
    {"nicheName": "创业投资", "nichePinyin": "chuangye touzi", "nicheCategory": "职业就业"},
    
    # 更多法律咨询类
    {"nicheName": "法律", "nichePinyin": "falv", "nicheCategory": "法律咨询"},
    {"nicheName": "律师", "nichePinyin": "lvshi", "nicheCategory": "法律咨询"},
    {"nicheName": "法律咨询", "nichePinyin": "falv zixun", "nicheCategory": "法律咨询"},
    {"nicheName": "法律援助", "nichePinyin": "falv yuanzhu", "nicheCategory": "法律咨询"},
    {"nicheName": "法律文书", "nichePinyin": "falv wenshu", "nicheCategory": "法律咨询"},
    {"nicheName": "合同起草", "nichePinyin": "hetong qicao", "nicheCategory": "法律咨询"},
    {"nicheName": "合同审查", "nichePinyin": "hetong shencha", "nicheCategory": "法律咨询"},
    {"nicheName": "合同纠纷", "nichePinyin": "hetong jiufen", "nicheCategory": "法律咨询"},
    {"nicheName": "劳动纠纷", "nichePinyin": "laodong jiufen", "nicheCategory": "法律咨询"},
    {"nicheName": "房产纠纷", "nichePinyin": "fangchan jiufen", "nicheCategory": "法律咨询"},
    {"nicheName": "婚姻纠纷", "nichePinyin": "hunyin jiufen", "nicheCategory": "法律咨询"},
    {"nicheName": "交通事故", "nichePinyin": "jiaotong shigu", "nicheCategory": "法律咨询"},
    {"nicheName": "人身损害", "nichePinyin": "renshen sunhai", "nicheCategory": "法律咨询"},
    {"nicheName": "知识产权", "nichePinyin": "zhishi chanquan", "nicheCategory": "法律咨询"},
    {"nicheName": "专利申请", "nichePinyin": "zhuanli shenqing", "nicheCategory": "法律咨询"},
    {"nicheName": "商标注册", "nichePinyin": "shangbiao zhuce", "nicheCategory": "法律咨询"},
    {"nicheName": "版权登记", "nichePinyin": "banquan dengji", "nicheCategory": "法律咨询"},
    {"nicheName": "公司注册", "nichePinyin": "gongsi zhuce", "nicheCategory": "法律咨询"},
    {"nicheName": "公司变更", "nichePinyin": "gongsi bian ge", "nicheCategory": "法律咨询"},
    {"nicheName": "公司注销", "nichePinyin": "gongsi zhuxiao", "nicheCategory": "法律咨询"},
]

def supplement_niches():
    """补充行业数据"""
    print("\n" + "="*60)
    print("📝 补充行业数据")
    print("="*60)
    
    # 加载现有数据
    niches_file = DATA_DIR / "niches.json"
    existing_niches = json.loads(niches_file.read_text(encoding='utf-8'))
    
    # 获取现有行业名称
    existing_names = [n['nicheName'] for n in existing_niches]
    
    # 添加新行业
    added_count = 0
    for niche in SUPPLEMENT_NICHES:
        if niche['nicheName'] not in existing_names:
            existing_niches.append(niche)
            added_count += 1
    
    # 保存数据
    niches_file.write_text(json.dumps(existing_niches, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"✅ 已补充 {added_count} 个行业")
    print(f"当前总数: {len(existing_niches)} 个")
    
    return len(existing_niches)

if __name__ == "__main__":
    supplement_niches()