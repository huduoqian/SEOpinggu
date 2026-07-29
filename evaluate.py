#!/usr/bin/env python3
"""
SEOpinggu - SEO 内容评估工具
用法:
  python evaluate.py --url https://example.com --keyword "SEO"
  python evaluate.py --file ./sample.html --keyword "优化"
"""
import sys
import json
import requests
from seopinggu.core import SEOEvaluator
import click

@click.command()
@click.option('--url', help='要分析的网页 URL')
@click.option('--file', help='本地 HTML 文件路径')
@click.option('--keyword', default='', help='目标关键词（可选）')
@click.option('--output', default='text', type=click.Choice(['text', 'json']), help='输出格式')
def main(url, file, keyword, output):
    """SEOpinggu 命令行评估工具"""
    
    html_content = None
    target_url = url or file or ""

    if url:
        try:
            print(f"🌐 正在抓取: {url}")
            resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            resp.encoding = resp.apparent_encoding or 'utf-8'
            html_content = resp.text
        except Exception as e:
            print(f"❌ 抓取失败: {e}")
            sys.exit(1)
    elif file:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            print(f"📂 已加载本地文件: {file}")
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            sys.exit(1)
    else:
        print("❌ 请提供 --url 或 --file")
        sys.exit(1)

    # 执行评估
    evaluator = SEOEvaluator(html_content, url=url or file, keyword=keyword)
    result = evaluator.evaluate_all()

    # 输出
    if output == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("\n" + "="*50)
        print(f"📊 SEOpinggu 内容评估报告")
        print("="*50)
        print(f"🔗 目标: {result['url']}")
        print(f"🔑 关键词: {result['keyword'] or '(未指定)'}")
        print("-"*50)
        print(f"🏆 综合评分: {result['total_score']} / 100")
        print("-"*50)
        
        # 分类展示
        good = []
        warn = []
        for item in result['details']:
            if item['score'] >= 80:
                good.append(f"  ✅ {item['item']}: {item['message']}")
            elif item['score'] >= 50:
                warn.append(f"  ⚠️  {item['item']}: {item['message']}")
            else:
                warn.append(f"  ❌ {item['item']}: {item['message']}")
        
        if good:
            print("\n✅ 优点:")
            for g in good:
                print(g)
        if warn:
            print("\n⚠️  待改进:")
            for w in warn:
                print(w)
        
        print("\n" + "="*50)
        print("💡 建议: 优先修复 ❌ 标记的项目，再优化 ⚠️ 项")
        print("="*50)

if __name__ == '__main__':
    main()