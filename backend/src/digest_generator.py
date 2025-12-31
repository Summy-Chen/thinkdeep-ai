"""
简报生成模块
将抓取的文章整理成格式化的Markdown简报
"""

import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class DigestGenerator:
    """简报生成器"""
    
    def __init__(self, output_dir: str = "output", title: str = "AI 每日简报"):
        """
        初始化生成器
        
        Args:
            output_dir: 输出目录
            title: 简报标题
        """
        self.output_dir = output_dir
        self.title = title
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_markdown(self, articles: List[Dict], 
                          analysis: Optional[Dict] = None,
                          categories: Optional[Dict[str, List[Dict]]] = None) -> str:
        """
        生成Markdown格式的简报
        
        Args:
            articles: 文章列表
            analysis: LLM分析结果
            categories: 分类后的文章
            
        Returns:
            Markdown格式的简报内容
        """
        today = datetime.now().strftime("%Y年%m月%d日")
        weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.now().weekday()]
        
        md_content = f"""# {self.title}

**{today} {weekday}** | 共收录 {len(articles)} 篇文章

---

"""
        
        # 添加综合分析
        if analysis:
            md_content += """## 📊 今日概览

"""
            if analysis.get('overview'):
                md_content += f"{analysis['overview']}\n\n"
            
            if analysis.get('highlights'):
                md_content += "### 🔥 今日要点\n\n"
                for i, highlight in enumerate(analysis['highlights'], 1):
                    md_content += f"{i}. {highlight}\n"
                md_content += "\n"
            
            if analysis.get('trends'):
                md_content += "### 📈 趋势观察\n\n"
                for trend in analysis['trends']:
                    md_content += f"- {trend}\n"
                md_content += "\n"
            
            if analysis.get('recommendation'):
                md_content += f"### ⭐ 今日推荐\n\n{analysis['recommendation']}\n\n"
            
            md_content += "---\n\n"
        
        # 按分类展示文章
        if categories:
            md_content += "## 📰 详细内容\n\n"
            
            category_icons = {
                "大语言模型": "🤖",
                "AI应用与产品": "🚀",
                "研究与论文": "📚",
                "行业动态": "🏢",
                "其他": "📌"
            }
            
            for category, cat_articles in categories.items():
                if cat_articles:
                    icon = category_icons.get(category, "📌")
                    md_content += f"### {icon} {category}\n\n"
                    
                    for article in cat_articles[:10]:  # 每个分类最多10篇
                        md_content += self._format_article(article)
                    
                    md_content += "\n"
        else:
            # 如果没有分类，按来源展示
            md_content += "## 📰 最新文章\n\n"
            
            # 按来源分组
            by_source = {}
            for article in articles:
                source = article.get('source_name', '其他')
                if source not in by_source:
                    by_source[source] = []
                by_source[source].append(article)
            
            for source, source_articles in by_source.items():
                md_content += f"### 📍 {source}\n\n"
                for article in source_articles[:5]:
                    md_content += self._format_article(article)
                md_content += "\n"
        
        # 添加页脚
        md_content += """---

## 📌 关于本简报

本简报由 AI Daily Digest 自动生成，汇集了以下信息源的最新内容：

- **公司博客**: OpenAI, Google AI, Anthropic
- **学术研究**: Berkeley AI Research, MIT AI News, arXiv
- **技术博客**: Simon Willison, Lilian Weng, The Batch
- **社区讨论**: Hacker News, Reddit ML

如有问题或建议，请回复此邮件。

---
*生成时间: {timestamp}*
""".format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        return md_content
    
    def _format_article(self, article: Dict) -> str:
        """格式化单篇文章"""
        title = article.get('title', '无标题')
        link = article.get('link', '#')
        summary = article.get('chinese_summary', article.get('summary', ''))
        source = article.get('source_name', '')
        
        # 解析发布时间
        pub_date = article.get('published', '')
        if pub_date:
            try:
                dt = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                pub_date = dt.strftime("%m-%d %H:%M")
            except:
                pub_date = pub_date[:10] if len(pub_date) > 10 else pub_date
        
        formatted = f"**[{title}]({link})**\n"
        if pub_date:
            formatted += f"*{source} | {pub_date}*\n\n"
        else:
            formatted += f"*{source}*\n\n"
        
        if summary:
            # 限制摘要长度
            if len(summary) > 300:
                summary = summary[:300] + "..."
            formatted += f"> {summary}\n\n"
        
        return formatted
    
    def save_digest(self, content: str, filename: Optional[str] = None) -> str:
        """
        保存简报到文件
        
        Args:
            content: Markdown内容
            filename: 文件名（可选）
            
        Returns:
            保存的文件路径
        """
        if not filename:
            filename = f"ai_digest_{datetime.now().strftime('%Y%m%d')}.md"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"简报已保存到: {filepath}")
        return filepath
    
    def generate_html(self, markdown_content: str) -> str:
        """
        将Markdown转换为HTML（用于邮件发送）
        
        Args:
            markdown_content: Markdown内容
            
        Returns:
            HTML内容
        """
        import markdown
        
        # 转换Markdown到HTML
        html_body = markdown.markdown(
            markdown_content,
            extensions=['tables', 'fenced_code', 'toc']
        )
        
        # 包装成完整的HTML文档
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        h3 {{
            color: #7f8c8d;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 10px 0;
            padding: 10px 20px;
            background-color: #f8f9fa;
            color: #666;
        }}
        hr {{
            border: none;
            border-top: 1px solid #eee;
            margin: 20px 0;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            font-size: 0.9em;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_body}
    </div>
</body>
</html>
"""
        return html_content


def test_generator():
    """测试生成器"""
    generator = DigestGenerator(output_dir="/home/ubuntu/ai_daily_digest/output")
    
    test_articles = [
        {
            "title": "OpenAI Releases GPT-5",
            "link": "https://openai.com/blog/gpt-5",
            "summary": "OpenAI发布了GPT-5，具有更强的推理能力。",
            "source_name": "OpenAI Blog",
            "published": "2024-01-15T10:00:00",
            "category": "company"
        },
        {
            "title": "Google Announces Gemini 2.0",
            "link": "https://ai.google/gemini-2",
            "summary": "Google推出Gemini 2.0，在多模态任务上表现出色。",
            "source_name": "Google AI Blog",
            "published": "2024-01-15T09:00:00",
            "category": "company"
        }
    ]
    
    test_analysis = {
        "overview": "今日AI领域最重要的动态是OpenAI和Google分别发布了新一代模型。",
        "highlights": ["GPT-5发布", "Gemini 2.0推出", "模型推理能力大幅提升"],
        "trends": ["大模型竞争加剧", "多模态成为标配"],
        "recommendation": "OpenAI Releases GPT-5 - 这是今年最重要的模型发布"
    }
    
    content = generator.generate_markdown(test_articles, test_analysis)
    filepath = generator.save_digest(content)
    print(f"测试简报已保存到: {filepath}")
    print("\n预览:\n")
    print(content[:1000])


if __name__ == "__main__":
    test_generator()
