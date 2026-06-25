// ===== 导航站核心脚本 =====
(function() {
    'use strict';

    // 获取配置数据
    const config = window.__SITE_CONFIG__ || {};

    // 渲染分类
    function renderCategories() {
        const grid = document.getElementById('categoriesGrid');
        if (!grid || !config.categories) return;

        grid.innerHTML = config.categories.map(cat => {
            const links = (cat.links || []).map(link => {
                const desc = link.desc ? `<span class="link-desc">${link.desc}</span>` : '';
                return `<li><a href="${link.url}" target="_blank" rel="noopener">${link.name}${desc}</a></li>`;
            }).join('');

            return `
                <div class="category-card" data-category="${cat.name}">
                    <div class="category-header">
                        <span class="category-icon">${cat.icon || '📁'}</span>
                        <span class="category-name">${cat.name}</span>
                    </div>
                    <ul class="link-list">${links}</ul>
                </div>
            `;
        }).join('');
    }

    // 搜索过滤
    window.filterLinks = function() {
        const query = document.getElementById('searchInput').value.toLowerCase();
        const cards = document.querySelectorAll('.category-card');

        cards.forEach(card => {
            const links = card.querySelectorAll('.link-list li');
            let hasMatch = false;

            links.forEach(li => {
                const text = li.textContent.toLowerCase();
                if (text.includes(query)) {
                    li.style.display = '';
                    hasMatch = true;
                } else {
                    li.style.display = 'none';
                }
            });

            card.style.display = hasMatch ? '' : 'none';
        });
    };

    // 回到顶部
    window.scrollToTop = function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    // 滚动监听
    window.addEventListener('scroll', function() {
        const btn = document.getElementById('backToTop');
        if (btn) {
            btn.style.display = window.scrollY > 300 ? 'block' : 'none';
        }
    });

    // 初始化
    document.addEventListener('DOMContentLoaded', function() {
        renderCategories();

        // 如果没有内嵌数据，尝试fetch
        if (!window.__SITE_CONFIG__) {
            fetch('config.json')
                .then(r => r.json())
                .then(data => {
                    window.__SITE_CONFIG__ = data;
                    renderCategories();
                })
                .catch(err => console.error('加载配置失败:', err));
        }
    });
})();
