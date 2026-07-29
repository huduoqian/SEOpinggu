"""
SEOpinggu 核心评估模块
"""
import re
import statistics
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import textstat

class SEOEvaluator:
    """SEO 内容评估器"""

    def __init__(self, html_content, url="", keyword=""):
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.url = url
        self.keyword = keyword.lower().strip() if keyword else ""
        self.text = self.soup.get_text()
        self.clean_text = re.sub(r'\s+', ' ', self.text).strip()

    def get_title_score(self):
        """检查 Title 标签"""
        title_tag = self.soup.find('title')
        if not title_tag or not title_tag.string:
            return 0, "未设置 Title 标签"
        title = title_tag.string.strip()
        length = len(title)
        if 30 <= length <= 60:
            score = 100
            msg = f"标题长度完美 ({length} 字符)"
        elif 20 <= length < 30 or 60 < length <= 80:
            score = 70
            msg = f"标题长度适中 ({length} 字符)"
        else:
            score = 40
            msg = f"标题长度不理想 ({length} 字符)，建议 30~60"

        # 检查关键词是否在标题中
        if self.keyword and self.keyword in title.lower():
            score += 5
            msg += "，且包含关键词 ✓"
        else:
            msg += "，建议加入目标关键词"
        return min(score, 100), msg

    def get_description_score(self):
        """检查 Meta Description"""
        desc_tag = self.soup.find('meta', attrs={'name': 'description'})
        if not desc_tag or not desc_tag.get('content'):
            return 0, "未设置 Description"
        desc = desc_tag['content'].strip()
        length = len(desc)
        if 120 <= length <= 160:
            score = 100
            msg = f"描述长度完美 ({length} 字符)"
        elif 80 <= length < 120 or 160 < length <= 200:
            score = 70
            msg = f"描述长度适中 ({length} 字符)"
        else:
            score = 40
            msg = f"描述长度不理想 ({length} 字符)，建议 120~160"

        if self.keyword and self.keyword in desc.lower():
            score += 5
            msg += "，且包含关键词 ✓"
        else:
            msg += "，建议加入目标关键词"
        return min(score, 100), msg

    def get_heading_score(self):
        """检查 H1~H3 结构"""
        h1s = self.soup.find_all('h1')
        h2s = self.soup.find_all('h2')
        h3s = self.soup.find_all('h3')

        score = 0
        msgs = []
        if len(h1s) == 1:
            score += 40
            msgs.append("H1 数量正确 (1个)")
        elif len(h1s) == 0:
            msgs.append("❌ 缺少 H1 标签")
        else:
            score += 15
            msgs.append(f"⚠️ H1 过多 ({len(h1s)}个)，建议仅保留1个")

        if len(h2s) >= 2:
            score += 30
            msgs.append(f"H2 数量合理 ({len(h2s)}个)")
        elif len(h2s) == 0:
            msgs.append("建议增加 H2 子标题划分内容")
        else:
            score += 15
            msgs.append(f"H2 数量偏少 ({len(h2s)}个)")

        if len(h3s) >= 1:
            score += 30
            msgs.append(f"H3 使用良好 ({len(h3s)}个)")
        else:
            msgs.append("建议增加 H3 细化内容层级")

        # 关键词在标题中加分
        for tag in ['h1', 'h2', 'h3']:
            for elem in self.soup.find_all(tag):
                if self.keyword and self.keyword in elem.get_text().lower():
                    score += 3
                    msgs.append(f"✅ {tag.upper()} 包含关键词")
                    break

        return min(score, 100), "；".join(msgs)

    def get_keyword_density(self):
        """计算关键词密度（简化版）"""
        if not self.keyword:
            return 50, "未指定关键词，跳过此项"

        words = re.findall(r'\w+', self.clean_text.lower())
        total = len(words)
        if total == 0:
            return 0, "页面无正文内容"

        count = words.count(self.keyword)
        # 也检查复合词，比如 "SEO" 在 "SEO优化" 中
        count += sum(1 for w in words if self.keyword in w and w != self.keyword)
        
        density = (count / total) * 100
        if 1.5 <= density <= 4.0:
            score = 100
            msg = f"关键词密度完美 ({density:.2f}%)"
        elif 0.8 <= density < 1.5 or 4.0 < density <= 6.0:
            score = 70
            msg = f"关键词密度适中 ({density:.2f}%)"
        elif density > 6.0:
            score = 40
            msg = f"关键词密度过高 ({density:.2f}%)，疑似堆砌"
        else:
            score = 30
            msg = f"关键词密度过低 ({density:.2f}%)"

        # 检查前100个词是否出现
        first_100 = ' '.join(words[:100])
        if self.keyword in first_100:
            score += 5
            msg += "，开头100字已出现 ✓"
        return min(score, 100), msg

    def get_readability_score(self):
        """可读性（Flesch Reading Ease）"""
        if len(self.clean_text) < 100:
            return 60, "文本过短，可读性评估参考性有限"

        try:
            flesch = textstat.flesch_reading_ease(self.clean_text)
            if flesch >= 60:
                score = 90
                msg = f"可读性良好 (Flesch: {flesch:.1f})"
            elif 40 <= flesch < 60:
                score = 70
                msg = f"可读性一般 (Flesch: {flesch:.1f})"
            else:
                score = 40
                msg = f"可读性较差 (Flesch: {flesch:.1f})，建议简化句式"
            return score, msg
        except:
            return 60, "可读性计算异常"

    def get_images_score(self):
        """图片 Alt 检测"""
        imgs = self.soup.find_all('img')
        if not imgs:
            return 80, "页面无图片（可忽略）"

        missing_alt = [img for img in imgs if not img.get('alt') or img['alt'].strip() == '']
        total = len(imgs)
        missing = len(missing_alt)

        if missing == 0:
            return 100, f"所有 {total} 张图片都有 Alt 属性 ✓"
        elif missing / total <= 0.3:
            score = 70
            msg = f"{missing}/{total} 张图片缺少 Alt，建议补充"
        else:
            score = 40
            msg = f"{missing}/{total} 张图片缺少 Alt，影响可访问性和SEO"
        return score, msg

    def get_links_score(self):
        """链接统计"""
        a_tags = self.soup.find_all('a', href=True)
        internal = []
        external = []
        base_domain = urlparse(self.url).netloc if self.url else ""

        for a in a_tags:
            href = a['href']
            if href.startswith('#') or href.startswith('javascript:'):
                continue
            if href.startswith('/') or (base_domain and base_domain in href):
                internal.append(href)
            else:
                external.append(href)

        if len(internal) + len(external) == 0:
            return 50, "未检测到任何链接，建议增加内链"

        score = 60
        msg = f"内链 {len(internal)} 个"
        if len(internal) >= 3:
            score += 20
            msg += " (数量充足)"
        elif len(internal) >= 1:
            score += 10

        msg += f"，外链 {len(external)} 个"
        if len(external) >= 2:
            score += 10
            msg += " (外链质量良好)"
        return min(score, 100), msg

    def get_content_length_score(self):
        """内容长度"""
        # 去掉标签、脚本、样式的纯文本长度
        for script in self.soup(["script", "style"]):
            script.decompose()
        text = self.soup.get_text()
        word_count = len(re.findall(r'\w+', text))
        
        if word_count >= 800:
            score = 100
            msg = f"内容丰富 ({word_count} 词)"
        elif 400 <= word_count < 800:
            score = 75
            msg = f"内容适中 ({word_count} 词)，建议增加到800词以上"
        elif 200 <= word_count < 400:
            score = 50
            msg = f"内容偏少 ({word_count} 词)，建议扩充"
        else:
            score = 20
            msg = f"内容过短 ({word_count} 词)，严重影响SEO"
        return score, msg

    def evaluate_all(self):
        """执行全部评估，返回综合得分和详细报告"""
        results = {
            'title': self.get_title_score(),
            'description': self.get_description_score(),
            'headings': self.get_heading_score(),
            'keyword': self.get_keyword_density(),
            'readability': self.get_readability_score(),
            'images': self.get_images_score(),
            'links': self.get_links_score(),
            'content_length': self.get_content_length_score(),
        }

        # 加权计算总分（不同模块权重不同）
        weights = {
            'title': 0.15,
            'description': 0.12,
            'headings': 0.15,
            'keyword': 0.15,
            'readability': 0.10,
            'images': 0.10,
            'links': 0.08,
            'content_length': 0.15,
        }

        total_score = 0
        details = []
        for key, (score, msg) in results.items():
            total_score += score * weights[key]
            details.append({
                'item': key,
                'score': score,
                'message': msg
            })

        return {
            'total_score': round(total_score, 1),
            'details': details,
            'keyword': self.keyword,
            'url': self.url
        }