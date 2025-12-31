"""
LLM 分析模块
使用大语言模型对文章进行智能分析和摘要
"""

import os
import logging
from typing import List, Dict, Optional
from openai import OpenAI

logger = logging.getLogger(__name__)

class LLMAnalyzer:
    """使用LLM进行内容分析"""
    
    def __init__(self, model: str = None, max_tokens: int = None):
        """
        初始化分析器
        
        Args:
            model: 使用的模型名称
            max_tokens: 最大token数
        """
        from config import LLM_CONFIG
        self.model = model or LLM_CONFIG.get('model', 'gpt-4.1-mini')
        self.max_tokens = max_tokens or LLM_CONFIG.get('max_tokens', 1000)
        self.client = OpenAI()  # 使用环境变量中的API Key
    
    def summarize_article(self, article: Dict) -> str:
        """
        为单篇文章生成中文摘要
        
        Args:
            article: 文章字典
            
        Returns:
            中文摘要
        """
        try:
            prompt = f"""请用简洁的中文总结以下AI领域文章的核心内容，突出关键技术点和重要发现。
摘要应该在2-3句话内，适合非技术背景的读者理解。

标题: {article.get('title', '')}
来源: {article.get('source_name', '')}
原文摘要: {article.get('summary', '')[:1000]}

请直接输出中文摘要，不要有任何前缀："""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的AI技术编辑，擅长将复杂的技术内容转化为通俗易懂的中文摘要。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.warning(f"生成摘要失败: {e}")
            # 返回原始摘要的截断版本
            return article.get('summary', '')[:200] + '...' if len(article.get('summary', '')) > 200 else article.get('summary', '')
    
    def generate_daily_digest(self, articles: List[Dict]) -> Dict:
        """
        生成每日简报的综合分析
        
        Args:
            articles: 文章列表
            
        Returns:
            包含分析结果的字典
        """
        if not articles:
            return {
                "overview": "今日暂无新的AI领域重要动态。",
                "highlights": [],
                "trends": []
            }
        
        try:
            # 准备文章摘要
            articles_text = "\n".join([
                f"- [{a['source_name']}] {a['title']}: {a.get('summary', '')[:200]}"
                for a in articles[:20]  # 限制数量避免token过多
            ])
            
            prompt = f"""基于以下今日AI领域的最新文章，请生成一份简报分析：

{articles_text}

请用中文输出以下内容（使用JSON格式）：
{{
    "overview": "今日AI领域整体动态概述（2-3句话）",
    "highlights": ["重点1", "重点2", "重点3"],
    "trends": ["趋势观察1", "趋势观察2"],
    "recommendation": "今日最值得关注的一篇文章标题及原因"
}}

请确保输出是有效的JSON格式："""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位资深AI行业分析师，擅长从海量信息中提炼关键洞察。请用JSON格式输出分析结果。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.5
            )
            
            import json
            result_text = response.choices[0].message.content.strip()
            
            # 尝试提取JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            
            return json.loads(result_text)
            
        except Exception as e:
            logger.warning(f"生成综合分析失败: {e}")
            return {
                "overview": f"今日共收集到 {len(articles)} 篇AI领域相关文章。",
                "highlights": [a['title'] for a in articles[:3]],
                "trends": ["请查看详细文章列表了解更多"],
                "recommendation": articles[0]['title'] if articles else ""
            }
    
    def categorize_articles(self, articles: List[Dict]) -> Dict[str, List[Dict]]:
        """
        将文章按主题分类
        
        Args:
            articles: 文章列表
            
        Returns:
            分类后的文章字典
        """
        categories = {
            "大语言模型": [],
            "AI应用与产品": [],
            "研究与论文": [],
            "行业动态": [],
            "其他": []
        }
        
        for article in articles:
            title_lower = article.get('title', '').lower()
            summary_lower = article.get('summary', '').lower()
            source_category = article.get('category', '')
            
            # 基于关键词和来源分类
            if any(kw in title_lower or kw in summary_lower 
                   for kw in ['llm', 'gpt', 'claude', 'gemini', 'language model', 'transformer', 'chatgpt']):
                categories["大语言模型"].append(article)
            elif any(kw in title_lower or kw in summary_lower 
                     for kw in ['launch', 'release', 'product', 'app', 'tool', 'api']):
                categories["AI应用与产品"].append(article)
            elif source_category == 'research' or 'arxiv' in article.get('source_id', ''):
                categories["研究与论文"].append(article)
            elif source_category == 'company' or any(kw in title_lower 
                     for kw in ['openai', 'google', 'microsoft', 'anthropic', 'meta']):
                categories["行业动态"].append(article)
            else:
                categories["其他"].append(article)
        
        # 移除空分类
        return {k: v for k, v in categories.items() if v}


def test_analyzer():
    """测试分析器"""
    analyzer = LLMAnalyzer()
    
    test_article = {
        "title": "OpenAI Releases GPT-5 with Enhanced Reasoning",
        "source_name": "OpenAI Blog",
        "summary": "OpenAI has announced the release of GPT-5, featuring significantly improved reasoning capabilities and reduced hallucinations. The new model demonstrates state-of-the-art performance on complex problem-solving tasks."
    }
    
    summary = analyzer.summarize_article(test_article)
    print(f"摘要: {summary}")


if __name__ == "__main__":
    test_analyzer()
