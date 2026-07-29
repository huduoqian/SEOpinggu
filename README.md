<div align="center">
  <h1>🔍 SEOpinggu</h1>
  <p><em>轻量级 · 可扩展的 SEO 内容质量评估利器</em></p>
  <p>一键诊断网页内容健康度，给出专业级优化建议</p>
  
  <!-- 徽章区域（请将 yourusername 替换为你的真实用户名） -->
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen" alt="PRs Welcome">
  <img src="https://img.shields.io/github/stars/yourusername/SEOpinggu?style=social" alt="GitHub Stars">
</div>

---

## 📖 项目简介

**SEOpinggu**（SEO 评估）是一款专为内容创作者、SEO 从业者及开发者设计的开源工具。它不仅能像常规工具一样检查关键词密度，更能从**可读性**、**内容结构**、**用户体验**和**技术规范**四个维度深度剖析页面，最终输出 0~100 的综合健康分。

与市面上动辄收费的 SaaS 工具不同，SEOpinggu 完全开源、可离线运行、支持二次开发，方便你集成到自己的 CI/CD 流水线或 CMS 系统中。

---

## ✨ 核心特性

- ⚖️ **多维度评分**：加权计算 8 大核心指标，拒绝单一维度的片面评价。
- 📝 **智能文本分析**：集成 `textstat` 库，计算 Flesch Reading Ease 等可读性指数。
- 🔑 **关键词深度追踪**：不仅计算密度，还检查关键词是否出现在 Title、Description、H1 及正文前 100 字内。
- 🖼️ **媒体资产审计**：自动统计图片总数，识别缺失 `Alt` 属性的图片，兼顾 SEO 与可访问性（A11y）。
- 🔗 **链接生态分析**：区分内部链接与外部链接，评估站点互链健康度。
- 🚀 **多种使用方式**：支持 **命令行（CLI）**、**Python 模块导入** 以及 **JSON 格式输出**，便于与自动化工具结合。

---

## 📊 评估维度与权重

| 评估维度 | 权重 | 优秀标准 | 检测重点 |
| :--- | :--- | :--- | :--- |
| **Title 标签** | 15% | 长度 30~60 字符 | 是否包含关键词、是否缺失 |
| **Meta Description** | 12% | 长度 120~160 字符 | 是否包含关键词、是否缺失 |
| **内容标题层级 (H1~H3)** | 15% | H1 唯一，H2≥2 个，H3≥1 个 | 结构是否扁平、关键词是否在标题中 |
| **关键词密度 (KD)** | 15% | 1.5% ~ 4.0% | 是否堆砌或严重稀疏、开头是否出现 |
| **文本可读性** | 10% | Flesch ≥ 60 | 句式是否过于复杂、文本是否流畅 |
| **图片 Alt 属性** | 10% | 100% 图片含 Alt | 是否遗漏、是否为空字符串 |
| **链接分布** | 8% | 内链 ≥3，外链 ≥2 | 站内站外链接比例是否健康 |
| **内容长度** | 15% | ≥ 800 单词 | 是否属于“空洞页面” |

---

## 🛠️ 技术栈

- **Python 3.8+** —— 核心开发语言
- **BeautifulSoup4** —— 灵活的 HTML/XML 解析
- **Requests** —— 稳健的 HTTP 请求处理
- **textstat** —— 业界标准的可读性计算库
- **Click** —— 构建优雅的命令行交互界面

---

## 📦 快速安装与使用

### 1. 克隆到本地
```bash
git clone https://github.com/yourusername/SEOpinggu.git
cd SEOpinggu
