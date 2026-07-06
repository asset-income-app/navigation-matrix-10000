# 开发指南

## 技术架构

### 整体架构

本项目采用**纯静态网站**架构，无后端服务器、无数据库、无框架依赖：

```
用户浏览器
    │
    ├── index.html  ──→  页面结构 + 内嵌配置数据
    ├── style.css   ──→  样式表现
    ├── script.js   ──→  交互逻辑（优先读取内嵌数据）
    └── config.json ──→  数据配置（HTTP服务器模式备用）
```

**核心设计原则：**
- 数据与视图分离：所有内容存储在config.json，页面由JS动态渲染
- 数据内嵌：HTML直接嵌入config.json数据，直接打开文件即可显示
- 零依赖：纯HTML/CSS/JS，无需Node.js、Webpack等构建工具
- 一键生成：修改母版模板后，运行Python脚本即可批量更新所有城市站

### 数据流

```
generate_mega.py
    │
    ├── 读取 CITIES 字典（51城市数据）
    ├── 读取 NATIONAL_LINKS（全国通用链接）
    │
    ├── 生成 02-city-sites/{city}/config.json  ← 每个城市独立配置
    ├── 生成 02-city-sites/{city}/index.html   ← 内嵌config.json数据
    ├── 生成 02-city-sites/{city}/style.css    ← 从模板生成
    ├── 生成 02-city-sites/{city}/script.js    ← 优先内嵌数据
    ├── 生成 02-city-sites/{city}/sitemap.xml  ← SEO站点地图
    ├── 生成 02-city-sites/{city}/robots.txt   ← 爬虫规则
    ├── 生成 02-city-sites/{city}/_headers ← Cloudflare安全头配置
    │
    ├── 生成 03-master-navigation/  ← 总站7个文件
    └── 生成 01-master-template/    ← 母版7个文件
```

### 数据内嵌机制

```javascript
// HTML中嵌入数据
<script>var EMBEDDED_CONFIG = {config.json数据};</script>

// script.js加载逻辑
function loadConfig() {
    // 优先使用内嵌数据（直接打开文件也能显示）
    if (typeof EMBEDDED_CONFIG !== 'undefined') {
        var data = EMBEDDED_CONFIG;
        // 渲染页面...
        return;
    }
    // 备用：通过HTTP请求加载config.json
    fetch('config.json').then(r => r.json()).then(data => {
        // 渲染页面...
    });
}
```

## 文件规范

### 每个站点包含7个文件

| 文件 | 用途 | 必需 |
|------|------|------|
| config.json | 城市配置数据 | 是 |
| index.html | 页面结构（含内嵌数据） | 是 |
| style.css | 样式表 | 是 |
| script.js | 交互脚本 | 是 |
| sitemap.xml | SEO站点地图 | 是 |
| robots.txt | 爬虫规则 | 是 |
| _headers | Cloudflare安全头配置 | 是 |

### config.json 格式（城市站）

```json
{
  "cityName": "唐山",
  "cityPinyin": "tangshan",
  "province": "河北",
  "categories": [
    {
      "name": "政务服务",
      "icon": "🏛️",
      "links": [
        {"name": "唐山市人民政府", "url": "http://www.tangshan.gov.cn/"},
        {"name": "唐山政务服务网", "url": "https://ts.hbzwfw.gov.cn/"}
      ]
    }
  ]
}
```

**字段说明：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cityName | string | 是 | 城市中文名称 |
| cityPinyin | string | 是 | 城市拼音（用于目录名和域名） |
| province | string | 是 | 所在省份 |
| categories | array | 是 | 分类数组（15个） |
| categories[].name | string | 是 | 分类名称 |
| categories[].icon | string | 否 | 分类图标（emoji） |
| categories[].links | array | 是 | 链接数组 |
| categories[].links[].name | string | 是 | 链接显示名称 |
| categories[].links[].url | string | 是 | 链接URL |

### config.json 格式（导航总站）

```json
{
  "siteName": "导航百科",
  "siteDesc": "全网精选优质垂直导航站目录 · 覆盖51个三线城市便民服务",
  "cityName": "导航百科",
  "cityPinyin": "daohangbaike",
  "province": "全国",
  "categories": [
    {
      "name": "城市导航",
      "icon": "🏙️",
      "links": [
        {"name": "唐山", "url": "https://tangshan-nav.pages.dev"}
      ]
    }
  ]
}
```

## 开发流程

### 场景1：添加新功能到所有网站

```
1. 修改 01-master-template/ 中的模板文件
2. 修改 generate_mega.py 中的模板代码
3. 运行 python generate_mega.py 重新生成所有站点
4. 本地预览验证
5. 部署到Netlify
```

### 场景2：更新某个城市的链接

```
1. 修改 generate_mega.py 中 CITIES 字典的对应城市数据
2. 运行 python generate_mega.py 重新生成
3. 或直接修改 02-city-sites/{city}/config.json（需同步更新HTML内嵌数据）
4. 部署更新
```

### 场景3：添加新城市

```
1. 在 generate_mega.py 的 CITIES 字典中添加新城市数据
2. 运行 python generate_mega.py
3. 在 03-master-navigation/config.json 中添加新城市链接
4. 在 04-deployed/management.json 中添加新城市记录
5. 部署新站点
```

## 样式系统

### CSS变量

```css
:root {
    --primary: #2563eb;        /* 主色调：蓝色 */
    --primary-dark: #1d4ed8;   /* 深蓝 */
    --primary-light: #dbeafe;  /* 浅蓝背景 */
    --bg: #f0f4f8;             /* 页面背景 */
    --card-bg: #ffffff;        /* 卡片背景 */
    --text: #1e293b;           /* 主文字 */
    --text-s: #64748b;         /* 次要文字 */
    --border: #e2e8f0;         /* 边框色 */
    --radius: 14px;            /* 圆角 */
}
```

### 响应式断点

| 断点 | 宽度 | 适配设备 |
|------|------|----------|
| 默认 | >768px | 桌面端 |
| 平板 | ≤768px | 平板/小屏 |
| 手机 | ≤480px | 手机 |

## JavaScript功能

### 核心模块

| 函数 | 功能 | 说明 |
|------|------|------|
| loadConfig() | 加载配置 | 优先读取EMBEDDED_CONFIG，备用fetch config.json |
| updatePageMeta() | 更新元数据 | 动态设置标题、描述、版权 |
| renderCategories() | 渲染分类 | 根据config.json生成分类列表 |
| toggleCategory(i) | 展开/收起 | 切换分类的展开状态 |
| initSearch() | 初始化搜索 | 绑定搜索事件 |
| performSearch() | 执行搜索 | 实时过滤链接 |
| initBackToTop() | 回到顶部 | 滚动显示按钮，点击回顶 |

### 搜索算法

```
输入关键词 → 转小写
→ 遍历所有分类和链接
→ 链接名称包含关键词 → 显示
→ 链接名称不包含 → 隐藏
→ 分类内无匹配链接 → 隐藏整个分类
→ 全部无匹配 → 显示"未找到"提示
```

## 生成脚本

### generate_mega.py 核心结构

```python
CITIES = {
    "tangshan": {
        "cn": "唐山",
        "prov": "河北",
        "gov": "http://www.tangshan.gov.cn/",
        "zwfw": "https://ts.hbzwfw.gov.cn/",
        "rsj": "http://rsj.tangshan.gov.cn/",
        "ybj": "https://tsyb.tangshan.gov.cn/",
        "gjj": "http://www.tsgjj.com/"
    },
    # ... 其他51个城市
}

NATIONAL_LINKS = {
    # 全国通用链接数据（15个分类）
}

def gen_city_config(pinyin, data):
    """生成单个城市的config.json - 15个分类"""

def gen_city_html(config_json):
    """生成城市站HTML - 内嵌config.json数据"""

def gen_city_css():
    """生成城市站CSS"""

def gen_city_js():
    """生成城市站JS - 优先EMBEDDED_CONFIG"""

def main():
    """主函数 - 生成51个城市站 + 导航总站 + 母版"""
```

### 运行方式

```bash
# 生成所有站点（约10秒）
python generate_mega.py
```

## 部署指南

详见 [deploy-guide.md](deploy-guide.md)

## 搜索引擎优化

### SEO检查清单

- [x] 每个页面有独立的 `<title>` 标签
- [x] 每个页面有 `<meta description>`
- [x] 每个页面有 `<meta keywords>`
- [x] 每个页面有 `<meta robots>`
- [x] 每个页面有 `<link rel="canonical">`
- [x] 每个页面有结构化数据（schema.org）
- [x] 使用语义化HTML5标签
- [x] 所有链接使用 `target="_blank"` 和 `rel="noopener"`
- [x] 响应式设计，适配移动端
- [x] 每个站点有 sitemap.xml
- [x] 每个站点有 robots.txt
- [x] Netlify安全头（X-Frame-Options等）
- [x] 页面加载速度快（纯静态，无框架）

### 提交搜索引擎

1. **百度站长平台**：https://ziyuan.baidu.com
2. **必应站长工具**：https://www.bing.com/webmasters
3. **搜狗站长平台**：https://zhanzhang.sogou.com

## 常见问题

### Q: 直接打开HTML文件显示空白？
v3版本已修复：HTML内嵌了config.json数据，直接双击打开即可显示内容。

### Q: 如何修改所有网站的底部信息？
修改 `generate_mega.py` 中的 `gen_city_html()` 函数，然后运行 `python generate_mega.py` 重新生成。

### Q: 如何添加新的服务分类？
在 `generate_mega.py` 的 `gen_city_config()` 函数中添加新分类模板，然后重新生成。

### Q: 链接失效了怎么办？
1. 使用 `link-checker` 技能检查失效链接
2. 使用 `link-collector` 技能收集新链接
3. 更新 `generate_mega.py` 中的 CITIES 数据
4. 重新生成并部署

### Q: 如何添加广告位？
在 `gen_city_html()` 函数中添加广告位容器，然后重新生成所有站点。广告代码从百度联盟获取。
