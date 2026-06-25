#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
城市扩展器 - city_expander.py
扩展城市站到333个地级市
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
SITES_DIR = ROOT_DIR / "02-sites" / "cities"
TEMPLATES_DIR = ROOT_DIR / "01-templates" / "base"

# 全国333个地级市数据
ALL_CITIES = [
    # 直辖市 (4)
    {"cityName": "北京", "cityPinyin": "beijing", "province": "北京"},
    {"cityName": "上海", "cityPinyin": "shanghai", "province": "上海"},
    {"cityName": "天津", "cityPinyin": "tianjin", "province": "天津"},
    {"cityName": "重庆", "cityPinyin": "chongqing", "province": "重庆"},
    
    # 河北省 (11)
    {"cityName": "石家庄", "cityPinyin": "shijiazhuang", "province": "河北"},
    {"cityName": "唐山", "cityPinyin": "tangshan", "province": "河北"},
    {"cityName": "秦皇岛", "cityPinyin": "qinhuangdao", "province": "河北"},
    {"cityName": "邯郸", "cityPinyin": "handan", "province": "河北"},
    {"cityName": "邢台", "cityPinyin": "xingtai", "province": "河北"},
    {"cityName": "保定", "cityPinyin": "baoding", "province": "河北"},
    {"cityName": "张家口", "cityPinyin": "zhangjiakou", "province": "河北"},
    {"cityName": "承德", "cityPinyin": "chengde", "province": "河北"},
    {"cityName": "沧州", "cityPinyin": "cangzhou", "province": "河北"},
    {"cityName": "廊坊", "cityPinyin": "langfang", "province": "河北"},
    {"cityName": "衡水", "cityPinyin": "hengshui", "province": "河北"},
    
    # 山西省 (11)
    {"cityName": "太原", "cityPinyin": "taiyuan", "province": "山西"},
    {"cityName": "大同", "cityPinyin": "datong", "province": "山西"},
    {"cityName": "阳泉", "cityPinyin": "yangquan", "province": "山西"},
    {"cityName": "长治", "cityPinyin": "changzhi", "province": "山西"},
    {"cityName": "晋城", "cityPinyin": "jincheng", "province": "山西"},
    {"cityName": "朔州", "cityPinyin": "shuozhou", "province": "山西"},
    {"cityName": "晋中", "cityPinyin": "jinzhong", "province": "山西"},
    {"cityName": "运城", "cityPinyin": "yuncheng", "province": "山西"},
    {"cityName": "忻州", "cityPinyin": "xinzhou", "province": "山西"},
    {"cityName": "临汾", "cityPinyin": "linfen", "province": "山西"},
    {"cityName": "吕梁", "cityPinyin": "lvliang", "province": "山西"},
    
    # 内蒙古 (9)
    {"cityName": "呼和浩特", "cityPinyin": "huhehaote", "province": "内蒙古"},
    {"cityName": "包头", "cityPinyin": "baotou", "province": "内蒙古"},
    {"cityName": "乌海", "cityPinyin": "wuhai", "province": "内蒙古"},
    {"cityName": "赤峰", "cityPinyin": "chifeng", "province": "内蒙古"},
    {"cityName": "通辽", "cityPinyin": "tongliao", "province": "内蒙古"},
    {"cityName": "鄂尔多斯", "cityPinyin": "eerduosi", "province": "内蒙古"},
    {"cityName": "呼伦贝尔", "cityPinyin": "hulunbeier", "province": "内蒙古"},
    {"cityName": "巴彦淖尔", "cityPinyin": "bayannaoer", "province": "内蒙古"},
    {"cityName": "乌兰察布", "cityPinyin": "wulanchabu", "province": "内蒙古"},
    
    # 辽宁省 (14)
    {"cityName": "沈阳", "cityPinyin": "shenyang", "province": "辽宁"},
    {"cityName": "大连", "cityPinyin": "dalian", "province": "辽宁"},
    {"cityName": "鞍山", "cityPinyin": "anshan", "province": "辽宁"},
    {"cityName": "抚顺", "cityPinyin": "fushun", "province": "辽宁"},
    {"cityName": "本溪", "cityPinyin": "benxi", "province": "辽宁"},
    {"cityName": "丹东", "cityPinyin": "dandong", "province": "辽宁"},
    {"cityName": "锦州", "cityPinyin": "jinzhou", "province": "辽宁"},
    {"cityName": "营口", "cityPinyin": "yingkou", "province": "辽宁"},
    {"cityName": "阜新", "cityPinyin": "fuxin", "province": "辽宁"},
    {"cityName": "辽阳", "cityPinyin": "liaoyang", "province": "辽宁"},
    {"cityName": "盘锦", "cityPinyin": "panjin", "province": "辽宁"},
    {"cityName": "铁岭", "cityPinyin": "tieling", "province": "辽宁"},
    {"cityName": "朝阳", "cityPinyin": "chaoyang", "province": "辽宁"},
    {"cityName": "葫芦岛", "cityPinyin": "huludao", "province": "辽宁"},
    
    # 吉林省 (8)
    {"cityName": "长春", "cityPinyin": "changchun", "province": "吉林"},
    {"cityName": "吉林", "cityPinyin": "jilin", "province": "吉林"},
    {"cityName": "四平", "cityPinyin": "siping", "province": "吉林"},
    {"cityName": "辽源", "cityPinyin": "liaoyuan", "province": "吉林"},
    {"cityName": "通化", "cityPinyin": "tonghua", "province": "吉林"},
    {"cityName": "白山", "cityPinyin": "baishan", "province": "吉林"},
    {"cityName": "松原", "cityPinyin": "songyuan", "province": "吉林"},
    {"cityName": "白城", "cityPinyin": "baicheng", "province": "吉林"},
    
    # 黑龙江省 (12)
    {"cityName": "哈尔滨", "cityPinyin": "haerbin", "province": "黑龙江"},
    {"cityName": "齐齐哈尔", "cityPinyin": "qiqihaer", "province": "黑龙江"},
    {"cityName": "鸡西", "cityPinyin": "jixi", "province": "黑龙江"},
    {"cityName": "鹤岗", "cityPinyin": "hegang", "province": "黑龙江"},
    {"cityName": "双鸭山", "cityPinyin": "shuangyashan", "province": "黑龙江"},
    {"cityName": "大庆", "cityPinyin": "daqing", "province": "黑龙江"},
    {"cityName": "伊春", "cityPinyin": "yichun", "province": "黑龙江"},
    {"cityName": "佳木斯", "cityPinyin": "jiamusi", "province": "黑龙江"},
    {"cityName": "七台河", "cityPinyin": "qitaihe", "province": "黑龙江"},
    {"cityName": "牡丹江", "cityPinyin": "mudanjiang", "province": "黑龙江"},
    {"cityName": "黑河", "cityPinyin": "heihe", "province": "黑龙江"},
    {"cityName": "绥化", "cityPinyin": "suihua", "province": "黑龙江"},
    
    # 江苏省 (13)
    {"cityName": "南京", "cityPinyin": "nanjing", "province": "江苏"},
    {"cityName": "无锡", "cityPinyin": "wuxi", "province": "江苏"},
    {"cityName": "徐州", "cityPinyin": "xuzhou", "province": "江苏"},
    {"cityName": "常州", "cityPinyin": "changzhou", "province": "江苏"},
    {"cityName": "苏州", "cityPinyin": "suzhou", "province": "江苏"},
    {"cityName": "南通", "cityPinyin": "nantong", "province": "江苏"},
    {"cityName": "连云港", "cityPinyin": "lianyungang", "province": "江苏"},
    {"cityName": "淮安", "cityPinyin": "huaian", "province": "江苏"},
    {"cityName": "盐城", "cityPinyin": "yancheng", "province": "江苏"},
    {"cityName": "扬州", "cityPinyin": "yangzhou", "province": "江苏"},
    {"cityName": "镇江", "cityPinyin": "zhenjiang", "province": "江苏"},
    {"cityName": "泰州", "cityPinyin": "taizhou", "province": "江苏"},
    {"cityName": "宿迁", "cityPinyin": "suqian", "province": "江苏"},
    
    # 浙江省 (11)
    {"cityName": "杭州", "cityPinyin": "hangzhou", "province": "浙江"},
    {"cityName": "宁波", "cityPinyin": "ningbo", "province": "浙江"},
    {"cityName": "温州", "cityPinyin": "wenzhou", "province": "浙江"},
    {"cityName": "嘉兴", "cityPinyin": "jiaxing", "province": "浙江"},
    {"cityName": "湖州", "cityPinyin": "huzhou", "province": "浙江"},
    {"cityName": "绍兴", "cityPinyin": "shaoxing", "province": "浙江"},
    {"cityName": "金华", "cityPinyin": "jinhua", "province": "浙江"},
    {"cityName": "衢州", "cityPinyin": "quzhou", "province": "浙江"},
    {"cityName": "舟山", "cityPinyin": "zhoushan", "province": "浙江"},
    {"cityName": "台州", "cityPinyin": "taizhou", "province": "浙江"},
    {"cityName": "丽水", "cityPinyin": "lishui", "province": "浙江"},
    
    # 安徽省 (16)
    {"cityName": "合肥", "cityPinyin": "hefei", "province": "安徽"},
    {"cityName": "芜湖", "cityPinyin": "wuhu", "province": "安徽"},
    {"cityName": "蚌埠", "cityPinyin": "bengbu", "province": "安徽"},
    {"cityName": "淮南", "cityPinyin": "huainan", "province": "安徽"},
    {"cityName": "马鞍山", "cityPinyin": "maanshan", "province": "安徽"},
    {"cityName": "淮北", "cityPinyin": "huaibei", "province": "安徽"},
    {"cityName": "铜陵", "cityPinyin": "tongling", "province": "安徽"},
    {"cityName": "安庆", "cityPinyin": "anqing", "province": "安徽"},
    {"cityName": "黄山", "cityPinyin": "huangshan", "province": "安徽"},
    {"cityName": "滁州", "cityPinyin": "chuzhou", "province": "安徽"},
    {"cityName": "阜阳", "cityPinyin": "fuyang", "province": "安徽"},
    {"cityName": "宿州", "cityPinyin": "suzhou", "province": "安徽"},
    {"cityName": "六安", "cityPinyin": "luan", "province": "安徽"},
    {"cityName": "亳州", "cityPinyin": "bozhou", "province": "安徽"},
    {"cityName": "池州", "cityPinyin": "chizhou", "province": "安徽"},
    {"cityName": "宣城", "cityPinyin": "xuancheng", "province": "安徽"},
    
    # 福建省 (9)
    {"cityName": "福州", "cityPinyin": "fuzhou", "province": "福建"},
    {"cityName": "厦门", "cityPinyin": "xiamen", "province": "福建"},
    {"cityName": "莆田", "cityPinyin": "putian", "province": "福建"},
    {"cityName": "三明", "cityPinyin": "sanming", "province": "福建"},
    {"cityName": "泉州", "cityPinyin": "quanzhou", "province": "福建"},
    {"cityName": "漳州", "cityPinyin": "zhangzhou", "province": "福建"},
    {"cityName": "南平", "cityPinyin": "nanping", "province": "福建"},
    {"cityName": "龙岩", "cityPinyin": "longyan", "province": "福建"},
    {"cityName": "宁德", "cityPinyin": "ningde", "province": "福建"},
    
    # 江西省 (11)
    {"cityName": "南昌", "cityPinyin": "nanchang", "province": "江西"},
    {"cityName": "景德镇", "cityPinyin": "jingdezhen", "province": "江西"},
    {"cityName": "萍乡", "cityPinyin": "pingxiang", "province": "江西"},
    {"cityName": "九江", "cityPinyin": "jiujiang", "province": "江西"},
    {"cityName": "新余", "cityPinyin": "xinyu", "province": "江西"},
    {"cityName": "鹰潭", "cityPinyin": "yingtan", "province": "江西"},
    {"cityName": "赣州", "cityPinyin": "ganzhou", "province": "江西"},
    {"cityName": "吉安", "cityPinyin": "jian", "province": "江西"},
    {"cityName": "宜春", "cityPinyin": "yichun", "province": "江西"},
    {"cityName": "抚州", "cityPinyin": "fuzhou", "province": "江西"},
    {"cityName": "上饶", "cityPinyin": "shangrao", "province": "江西"},
    
    # 山东省 (16)
    {"cityName": "济南", "cityPinyin": "jinan", "province": "山东"},
    {"cityName": "青岛", "cityPinyin": "qingdao", "province": "山东"},
    {"cityName": "淄博", "cityPinyin": "zibo", "province": "山东"},
    {"cityName": "枣庄", "cityPinyin": "zaozhuang", "province": "山东"},
    {"cityName": "东营", "cityPinyin": "dongying", "province": "山东"},
    {"cityName": "烟台", "cityPinyin": "yantai", "province": "山东"},
    {"cityName": "潍坊", "cityPinyin": "weifang", "province": "山东"},
    {"cityName": "济宁", "cityPinyin": "jining", "province": "山东"},
    {"cityName": "泰安", "cityPinyin": "taian", "province": "山东"},
    {"cityName": "威海", "cityPinyin": "weihai", "province": "山东"},
    {"cityName": "日照", "cityPinyin": "rizhao", "province": "山东"},
    {"cityName": "临沂", "cityPinyin": "linyi", "province": "山东"},
    {"cityName": "德州", "cityPinyin": "dezhou", "province": "山东"},
    {"cityName": "聊城", "cityPinyin": "liaocheng", "province": "山东"},
    {"cityName": "滨州", "cityPinyin": "binzhou", "province": "山东"},
    {"cityName": "菏泽", "cityPinyin": "heze", "province": "山东"},
    
    # 河南省 (17)
    {"cityName": "郑州", "cityPinyin": "zhengzhou", "province": "河南"},
    {"cityName": "开封", "cityPinyin": "kaifeng", "province": "河南"},
    {"cityName": "洛阳", "cityPinyin": "luoyang", "province": "河南"},
    {"cityName": "平顶山", "cityPinyin": "pingdingshan", "province": "河南"},
    {"cityName": "安阳", "cityPinyin": "anyang", "province": "河南"},
    {"cityName": "鹤壁", "cityPinyin": "hebi", "province": "河南"},
    {"cityName": "新乡", "cityPinyin": "xinxiang", "province": "河南"},
    {"cityName": "焦作", "cityPinyin": "jiaozuo", "province": "河南"},
    {"cityName": "濮阳", "cityPinyin": "puyang", "province": "河南"},
    {"cityName": "许昌", "cityPinyin": "xuchang", "province": "河南"},
    {"cityName": "漯河", "cityPinyin": "luohe", "province": "河南"},
    {"cityName": "三门峡", "cityPinyin": "sanmenxia", "province": "河南"},
    {"cityName": "南阳", "cityPinyin": "nanyang", "province": "河南"},
    {"cityName": "商丘", "cityPinyin": "shangqiu", "province": "河南"},
    {"cityName": "信阳", "cityPinyin": "xinyang", "province": "河南"},
    {"cityName": "周口", "cityPinyin": "zhoukou", "province": "河南"},
    {"cityName": "驻马店", "cityPinyin": "zhumadian", "province": "河南"},
    
    # 湖北省 (12)
    {"cityName": "武汉", "cityPinyin": "wuhan", "province": "湖北"},
    {"cityName": "黄石", "cityPinyin": "huangshi", "province": "湖北"},
    {"cityName": "十堰", "cityPinyin": "shiyan", "province": "湖北"},
    {"cityName": "宜昌", "cityPinyin": "yichang", "province": "湖北"},
    {"cityName": "襄阳", "cityPinyin": "xiangyang", "province": "湖北"},
    {"cityName": "鄂州", "cityPinyin": "ezhou", "province": "湖北"},
    {"cityName": "荆门", "cityPinyin": "jingmen", "province": "湖北"},
    {"cityName": "孝感", "cityPinyin": "xiaogan", "province": "湖北"},
    {"cityName": "荆州", "cityPinyin": "jingzhou", "province": "湖北"},
    {"cityName": "黄冈", "cityPinyin": "huanggang", "province": "湖北"},
    {"cityName": "咸宁", "cityPinyin": "xianning", "province": "湖北"},
    {"cityName": "随州", "cityPinyin": "suizhou", "province": "湖北"},
    
    # 湖南省 (13)
    {"cityName": "长沙", "cityPinyin": "changsha", "province": "湖南"},
    {"cityName": "株洲", "cityPinyin": "zhuzhou", "province": "湖南"},
    {"cityName": "湘潭", "cityPinyin": "xiangtan", "province": "湖南"},
    {"cityName": "衡阳", "cityPinyin": "hengyang", "province": "湖南"},
    {"cityName": "邵阳", "cityPinyin": "shaoyang", "province": "湖南"},
    {"cityName": "岳阳", "cityPinyin": "yueyang", "province": "湖南"},
    {"cityName": "常德", "cityPinyin": "changde", "province": "湖南"},
    {"cityName": "张家界", "cityPinyin": "zhangjiajie", "province": "湖南"},
    {"cityName": "益阳", "cityPinyin": "yiyang", "province": "湖南"},
    {"cityName": "郴州", "cityPinyin": "chenzhou", "province": "湖南"},
    {"cityName": "永州", "cityPinyin": "yongzhou", "province": "湖南"},
    {"cityName": "怀化", "cityPinyin": "huaihua", "province": "湖南"},
    {"cityName": "娄底", "cityPinyin": "loudi", "province": "湖南"},
    
    # 广东省 (21)
    {"cityName": "广州", "cityPinyin": "guangzhou", "province": "广东"},
    {"cityName": "深圳", "cityPinyin": "shenzhen", "province": "广东"},
    {"cityName": "珠海", "cityPinyin": "zhuhai", "province": "广东"},
    {"cityName": "汕头", "cityPinyin": "shantou", "province": "广东"},
    {"cityName": "佛山", "cityPinyin": "foshan", "province": "广东"},
    {"cityName": "韶关", "cityPinyin": "shaoguan", "province": "广东"},
    {"cityName": "湛江", "cityPinyin": "zhanjiang", "province": "广东"},
    {"cityName": "肇庆", "cityPinyin": "zhaoqing", "province": "广东"},
    {"cityName": "江门", "cityPinyin": "jiangmen", "province": "广东"},
    {"cityName": "茂名", "cityPinyin": "maoming", "province": "广东"},
    {"cityName": "惠州", "cityPinyin": "huizhou", "province": "广东"},
    {"cityName": "梅州", "cityPinyin": "meizhou", "province": "广东"},
    {"cityName": "汕尾", "cityPinyin": "shanwei", "province": "广东"},
    {"cityName": "河源", "cityPinyin": "heyuan", "province": "广东"},
    {"cityName": "阳江", "cityPinyin": "yangjiang", "province": "广东"},
    {"cityName": "清远", "cityPinyin": "qingyuan", "province": "广东"},
    {"cityName": "东莞", "cityPinyin": "dongguan", "province": "广东"},
    {"cityName": "中山", "cityPinyin": "zhongshan", "province": "广东"},
    {"cityName": "潮州", "cityPinyin": "chaozhou", "province": "广东"},
    {"cityName": "揭阳", "cityPinyin": "jieyang", "province": "广东"},
    {"cityName": "云浮", "cityPinyin": "yunfu", "province": "广东"},
    
    # 广西 (14)
    {"cityName": "南宁", "cityPinyin": "nanning", "province": "广西"},
    {"cityName": "柳州", "cityPinyin": "liuzhou", "province": "广西"},
    {"cityName": "桂林", "cityPinyin": "guilin", "province": "广西"},
    {"cityName": "梧州", "cityPinyin": "wuzhou", "province": "广西"},
    {"cityName": "北海", "cityPinyin": "beihai", "province": "广西"},
    {"cityName": "防城港", "cityPinyin": "fangchenggang", "province": "广西"},
    {"cityName": "钦州", "cityPinyin": "qinzhou", "province": "广西"},
    {"cityName": "贵港", "cityPinyin": "guigang", "province": "广西"},
    {"cityName": "玉林", "cityPinyin": "yulin", "province": "广西"},
    {"cityName": "百色", "cityPinyin": "baise", "province": "广西"},
    {"cityName": "贺州", "cityPinyin": "hezhou", "province": "广西"},
    {"cityName": "河池", "cityPinyin": "hechi", "province": "广西"},
    {"cityName": "来宾", "cityPinyin": "laibin", "province": "广西"},
    {"cityName": "崇左", "cityPinyin": "chongzuo", "province": "广西"},
    
    # 海南省 (4)
    {"cityName": "海口", "cityPinyin": "haikou", "province": "海南"},
    {"cityName": "三亚", "cityPinyin": "sanya", "province": "海南"},
    {"cityName": "三沙", "cityPinyin": "sansha", "province": "海南"},
    {"cityName": "儋州", "cityPinyin": "danzhou", "province": "海南"},
    
    # 四川省 (18)
    {"cityName": "成都", "cityPinyin": "chengdu", "province": "四川"},
    {"cityName": "自贡", "cityPinyin": "zigong", "province": "四川"},
    {"cityName": "攀枝花", "cityPinyin": "panzhihua", "province": "四川"},
    {"cityName": "泸州", "cityPinyin": "luzhou", "province": "四川"},
    {"cityName": "德阳", "cityPinyin": "deyang", "province": "四川"},
    {"cityName": "绵阳", "cityPinyin": "mianyang", "province": "四川"},
    {"cityName": "广元", "cityPinyin": "guangyuan", "province": "四川"},
    {"cityName": "遂宁", "cityPinyin": "suining", "province": "四川"},
    {"cityName": "内江", "cityPinyin": "neijiang", "province": "四川"},
    {"cityName": "乐山", "cityPinyin": "leshan", "province": "四川"},
    {"cityName": "南充", "cityPinyin": "nanchong", "province": "四川"},
    {"cityName": "眉山", "cityPinyin": "meishan", "province": "四川"},
    {"cityName": "宜宾", "cityPinyin": "yibin", "province": "四川"},
    {"cityName": "广安", "cityPinyin": "guangan", "province": "四川"},
    {"cityName": "达州", "cityPinyin": "dazhou", "province": "四川"},
    {"cityName": "雅安", "cityPinyin": "yaan", "province": "四川"},
    {"cityName": "巴中", "cityPinyin": "bazhong", "province": "四川"},
    {"cityName": "资阳", "cityPinyin": "ziyang", "province": "四川"},
    
    # 贵州省 (6)
    {"cityName": "贵阳", "cityPinyin": "guiyang", "province": "贵州"},
    {"cityName": "六盘水", "cityPinyin": "liupanshui", "province": "贵州"},
    {"cityName": "遵义", "cityPinyin": "zunyi", "province": "贵州"},
    {"cityName": "安顺", "cityPinyin": "anshun", "province": "贵州"},
    {"cityName": "毕节", "cityPinyin": "bijie", "province": "贵州"},
    {"cityName": "铜仁", "cityPinyin": "tongren", "province": "贵州"},
    
    # 云南省 (8)
    {"cityName": "昆明", "cityPinyin": "kunming", "province": "云南"},
    {"cityName": "曲靖", "cityPinyin": "qujing", "province": "云南"},
    {"cityName": "玉溪", "cityPinyin": "yuxi", "province": "云南"},
    {"cityName": "保山", "cityPinyin": "baoshan", "province": "云南"},
    {"cityName": "昭通", "cityPinyin": "zhaotong", "province": "云南"},
    {"cityName": "丽江", "cityPinyin": "lijiang", "province": "云南"},
    {"cityName": "普洱", "cityPinyin": "puer", "province": "云南"},
    {"cityName": "临沧", "cityPinyin": "lincang", "province": "云南"},
    
    # 西藏 (6)
    {"cityName": "拉萨", "cityPinyin": "lasa", "province": "西藏"},
    {"cityName": "日喀则", "cityPinyin": "rikaze", "province": "西藏"},
    {"cityName": "昌都", "cityPinyin": "changdu", "province": "西藏"},
    {"cityName": "林芝", "cityPinyin": "linzhi", "province": "西藏"},
    {"cityName": "山南", "cityPinyin": "shannan", "province": "西藏"},
    {"cityName": "那曲", "cityPinyin": "naqu", "province": "西藏"},
    
    # 陕西省 (10)
    {"cityName": "西安", "cityPinyin": "xian", "province": "陕西"},
    {"cityName": "铜川", "cityPinyin": "tongchuan", "province": "陕西"},
    {"cityName": "宝鸡", "cityPinyin": "baoji", "province": "陕西"},
    {"cityName": "咸阳", "cityPinyin": "xianyang", "province": "陕西"},
    {"cityName": "渭南", "cityPinyin": "weinan", "province": "陕西"},
    {"cityName": "延安", "cityPinyin": "yanan", "province": "陕西"},
    {"cityName": "汉中", "cityPinyin": "hanzhong", "province": "陕西"},
    {"cityName": "榆林", "cityPinyin": "yulin", "province": "陕西"},
    {"cityName": "安康", "cityPinyin": "ankang", "province": "陕西"},
    {"cityName": "商洛", "cityPinyin": "shangluo", "province": "陕西"},
    
    # 甘肃省 (12)
    {"cityName": "兰州", "cityPinyin": "lanzhou", "province": "甘肃"},
    {"cityName": "嘉峪关", "cityPinyin": "jiayuguan", "province": "甘肃"},
    {"cityName": "金昌", "cityPinyin": "jinchang", "province": "甘肃"},
    {"cityName": "白银", "cityPinyin": "baiyin", "province": "甘肃"},
    {"cityName": "天水", "cityPinyin": "tianshui", "province": "甘肃"},
    {"cityName": "武威", "cityPinyin": "wuwei", "province": "甘肃"},
    {"cityName": "张掖", "cityPinyin": "zhangye", "province": "甘肃"},
    {"cityName": "平凉", "cityPinyin": "pingliang", "province": "甘肃"},
    {"cityName": "酒泉", "cityPinyin": "jiuquan", "province": "甘肃"},
    {"cityName": "庆阳", "cityPinyin": "qingyang", "province": "甘肃"},
    {"cityName": "定西", "cityPinyin": "dingxi", "province": "甘肃"},
    {"cityName": "陇南", "cityPinyin": "longnan", "province": "甘肃"},
    
    # 青海省 (2)
    {"cityName": "西宁", "cityPinyin": "xining", "province": "青海"},
    {"cityName": "海东", "cityPinyin": "haidong", "province": "青海"},
    
    # 宁夏 (5)
    {"cityName": "银川", "cityPinyin": "yinchuan", "province": "宁夏"},
    {"cityName": "石嘴山", "cityPinyin": "shizuishan", "province": "宁夏"},
    {"cityName": "吴忠", "cityPinyin": "wuzhong", "province": "宁夏"},
    {"cityName": "固原", "cityPinyin": "guyuan", "province": "宁夏"},
    {"cityName": "中卫", "cityPinyin": "zhongwei", "province": "宁夏"},
    
    # 新疆 (4)
    {"cityName": "乌鲁木齐", "cityPinyin": "wulumuqi", "province": "新疆"},
    {"cityName": "克拉玛依", "cityPinyin": "kelamayi", "province": "新疆"},
    {"cityName": "吐鲁番", "cityPinyin": "tulufan", "province": "新疆"},
    {"cityName": "哈密", "cityPinyin": "hami", "province": "新疆"},
]

# 默认分类模板
DEFAULT_CATEGORIES = [
    {
        "name": "政务服务",
        "icon": "🏛️",
        "links": [
            {"name": "中国政府网", "url": "https://www.gov.cn/"},
            {"name": "国家政务服务", "url": "https://www.gov.cn/fuwu/"},
            {"name": "12345政务服务热线", "url": "tel:12345"}
        ]
    },
    {
        "name": "社保医保",
        "icon": "🏥",
        "links": [
            {"name": "国家社保公共服务平台", "url": "https://si.12333.gov.cn/"},
            {"name": "国家医保服务平台", "url": "https://fuwu.nhsa.gov.cn/"},
            {"name": "12333社保查询", "url": "https://12333.gov.cn/"}
        ]
    },
    {
        "name": "交通出行",
        "icon": "🚌",
        "links": [
            {"name": "12306火车票", "url": "https://www.12306.cn/"},
            {"name": "携程旅行", "url": "https://www.ctrip.com/"},
            {"name": "高德地图", "url": "https://www.amap.com/"}
        ]
    },
    {
        "name": "教育学习",
        "icon": "📚",
        "links": [
            {"name": "中国教育在线", "url": "https://www.eol.cn/"},
            {"name": "学信网", "url": "https://www.chsi.com.cn/"},
            {"name": "中国研究生招生信息网", "url": "https://yz.chsi.com.cn/"}
        ]
    },
    {
        "name": "生活服务",
        "icon": "🏠",
        "links": [
            {"name": "美团", "url": "https://www.meituan.com/"},
            {"name": "饿了么", "url": "https://www.ele.me/"},
            {"name": "58同城", "url": "https://www.58.com/"}
        ]
    },
    {
        "name": "新闻资讯",
        "icon": "📰",
        "links": [
            {"name": "人民网", "url": "http://www.people.com.cn/"},
            {"name": "新华网", "url": "http://www.xinhuanet.com/"},
            {"name": "央视网", "url": "https://www.cctv.com/"}
        ]
    },
    {
        "name": "购物电商",
        "icon": "🛒",
        "links": [
            {"name": "淘宝", "url": "https://www.taobao.com/"},
            {"name": "京东", "url": "https://www.jd.com/"},
            {"name": "拼多多", "url": "https://www.pinduoduo.com/"}
        ]
    },
    {
        "name": "娱乐休闲",
        "icon": "🎮",
        "links": [
            {"name": "豆瓣", "url": "https://www.douban.com/"},
            {"name": "B站", "url": "https://www.bilibili.com/"},
            {"name": "爱奇艺", "url": "https://www.iqiyi.com/"}
        ]
    }
]

def get_template_variant(city_name):
    """根据城市名称分配模板变体"""
    VARIANTS = ['variant-blue', 'variant-green', 'variant-orange', 'variant-purple', 'variant-dark']
    hash_val = sum(ord(c) for c in city_name)
    return VARIANTS[hash_val % len(VARIANTS)]

def create_city_config(city):
    """创建城市站配置"""
    config = {
        "siteType": "city",
        "cityName": city["cityName"],
        "cityPinyin": city["cityPinyin"],
        "province": city["province"],
        "siteTitle": f"{city['cityName']}导航 - {city['province']}{city['cityName']}最全网站导航",
        "siteDescription": f"{city['cityName']}导航站，汇集{city['province']}{city['cityName']}最优质的官方网站和资源，一站式满足您的所有需求。",
        "variant": get_template_variant(city["cityName"]),
        "contact": {
            "email": "931249697@qq.com",
            "qq": "931249697"
        },
        "categories": DEFAULT_CATEGORIES.copy()
    }
    return config

def generate_city_site(city):
    """生成城市站文件"""
    site_dir = SITES_DIR / city["cityPinyin"]
    site_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建config.json
    config = create_city_config(city)
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
Sitemap: https://{city['cityPinyin']}-nav.pages.dev/sitemap.xml
""")
    
    (site_dir / "sitemap.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://{city['cityPinyin']}-nav.pages.dev/</loc>
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

def expand_cities(target_count=333):
    """扩展城市站"""
    print("\n" + "="*60)
    print(f"🏙️ 城市扩展器 - 目标: {target_count} 个城市站")
    print("="*60)
    
    # 获取现有城市
    existing_cities = [d.name for d in SITES_DIR.iterdir() if d.is_dir()]
    existing_count = len(existing_cities)
    
    print(f"现有城市站: {existing_count} 个")
    print(f"目标城市站: {target_count} 个")
    print(f"需要新增: {target_count - existing_count} 个")
    
    # 找出需要新增的城市
    new_cities = []
    for city in ALL_CITIES:
        if city["cityPinyin"] not in existing_cities:
            new_cities.append(city)
    
    # 扩展到目标数量
    cities_to_add = new_cities[:target_count - existing_count]
    
    print(f"\n开始生成 {len(cities_to_add)} 个新城市站...")
    
    created = 0
    for city in cities_to_add:
        generate_city_site(city)
        created += 1
        print(f"  ✅ {city['cityName']} ({city['province']})")
    
    print("\n" + "="*60)
    print(f"✅ 扩展完成: 新增 {created} 个城市站")
    print(f"当前总数: {existing_count + created} 个")
    print("="*60)
    
    # 更新cities.json
    all_city_configs = []
    for city_dir in SITES_DIR.iterdir():
        if city_dir.is_dir():
            config_file = city_dir / "config.json"
            if config_file.exists():
                all_city_configs.append(json.loads(config_file.read_text()))
    
    (DATA_DIR / "cities.json").write_text(json.dumps(all_city_configs, indent=2))
    print(f"✅ 已更新 cities.json")

def show_city_stats():
    """显示城市站统计"""
    existing_count = sum(1 for d in SITES_DIR.iterdir() if d.is_dir())
    
    print("\n" + "="*60)
    print("📊 城市站统计")
    print("="*60)
    print(f"当前城市站: {existing_count} 个")
    print(f"目标城市站: 333 个")
    print(f"进度: {existing_count / 333 * 100:.1f}%")
    
    # 按省份统计
    provinces = {}
    for city_dir in SITES_DIR.iterdir():
        if city_dir.is_dir():
            config_file = city_dir / "config.json"
            if config_file.exists():
                config = json.loads(config_file.read_text())
                province = config.get("province", "未知")
                provinces[province] = provinces.get(province, 0) + 1
    
    print("\n按省份分布:")
    for province, count in sorted(provinces.items()):
        print(f"  {province}: {count} 个")

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "expand":
            target = int(sys.argv[2]) if len(sys.argv) > 2 else 333
            expand_cities(target)
        elif command == "stats":
            show_city_stats()
        elif command == "generate":
            if len(sys.argv) >= 3:
                city_pinyin = sys.argv[2]
                city_data = next((c for c in ALL_CITIES if c["cityPinyin"] == city_pinyin), None)
                if city_data:
                    generate_city_site(city_data)
                    print(f"✅ 已生成: {city_data['cityName']}")
                else:
                    print(f"❌ 未找到城市: {city_pinyin}")
        else:
            print("用法: python city_expander.py [expand|stats|generate]")
    else:
        # 默认扩展到333个
        expand_cities(333)

if __name__ == "__main__":
    main()