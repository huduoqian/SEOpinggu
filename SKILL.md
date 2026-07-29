---
name: SEOpinggu
description: |
  轻量级 SEO 内容质量评估技能。分析网页或本地 HTML 文件的 Title、Description、标题层级、
  关键词密度、可读性、图片 Alt、链接分布和内容长度，输出 0~100 综合评分及改进建议。
version: 1.0.0
author: your-github-username
license: MIT
tags:
  - SEO
  - content-analysis
  - readability
  - keyword-density
  - python
---

# 🔍 SEOpinggu Skill

## 🧠 用途
本技能帮助内容创作者、SEO 专家和开发者快速诊断一篇网页内容是否满足搜索引擎优化（SEO）的基本要求，并给出可操作的改进清单。

## 🎯 适用场景
- 文章发布前的自检
- 网站内容的批量审计
- 竞品内容对比
- 集成到 CMS、CI 流程或 AI 聊天机器人中

---

## 📥 输入参数 (Input Schema)

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `source` | string | **是** | 网页 URL（如 `https://example.com/page`）或本地 HTML 文件路径（如 `./sample.html`） |
| `keyword` | string | 否 | 目标关键词（例如 `"搜索引擎优化"`）。若提供，将检查关键词在 Title、Description、正文中的出现情况 |
| `output_format` | enum | 否 | 输出格式：`text`（终端友好，默认）或 `json`（结构化数据，方便程序解析） |

---

## 📤 输出数据 (Output Schema)

### 当 `output_format = text` 时
返回一段格式化文本，包含：
- 综合评分（0～100）
- 每个评估维度的得分及文字说明
- 优点列表（✅）和改进点列表（⚠️ / ❌）

### 当 `output_format = json` 时
返回一个 JSON 对象，结构如下：
```json
{
  "total_score": 82.5,
  "url": "https://example.com/article",
  "keyword": "seo优化",
  "details": [
    {
      "item": "title",
      "score": 95,
      "message": "标题长度完美 (48字符)，且包含关键词 ✓"
    },
    {
      "item": "description",
      "score": 100,
      "message": "描述长度完美 (145字符)，且包含关键词 ✓"
    }
    // ... 其他维度（headings, keyword, readability, images, links, content_length）
  ]
}