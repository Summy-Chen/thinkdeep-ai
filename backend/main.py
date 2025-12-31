#!/usr/bin/env python3
"""
AI Daily Digest - 主程序
每日自动抓取AI领域最新资讯，生成简报并发送邮件
"""

import os
import sys
import logging
from datetime import datetime
import argparse

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import RSS_FEEDS, EMAIL_CONFIG, SYSTEM_CONFIG, LLM_CONFIG
from src.rss_fetcher import RSSFetcher
from src.llm_analyzer import LLMAnalyzer
from src.digest_generator import DigestGenerator
from src.email_sender import EmailSender
import json

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            os.path.join(os.path.dirname(__file__), 'logs', f'digest_{datetime.now().strftime("%Y%m%d")}.log'),
            encoding='utf-8'
        )
    ]
)
logger = logging.getLogger(__name__)

class AIDailyDigest:
    """AI每日简报主类"""
    
    def __init__(self):
        """初始化各模块"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.fetcher = RSSFetcher(
            RSS_FEEDS, 
            data_dir=os.path.join(base_dir, SYSTEM_CONFIG['data_dir'])
        )
        
        self.analyzer = LLMAnalyzer(
            model=LLM_CONFIG.get('model', 'gpt-4.1-nano'),
            max_tokens=LLM_CONFIG.get('max_tokens', 500)
        ) if LLM_CONFIG.get('enabled', True) else None
        
        self.generator = DigestGenerator(
            output_dir=os.path.join(base_dir, SYSTEM_CONFIG['output_dir']),
            title=SYSTEM_CONFIG.get('digest_title', 'AI 每日简报')
        )
        
        self.email_sender = EmailSender(EMAIL_CONFIG)
    
    def run(self, send_email: bool = True, save_file: bool = True, 
            hours_back: int = 48, update_web: bool = True, web_data_path: str = None) -> dict:
        """
        运行完整的简报生成流程
        
        Args:
            send_email: 是否发送邮件
            save_file: 是否保存文件
            hours_back: 抓取多少小时内的文章
            
        Returns:
            包含运行结果的字典
        """
        result = {
            'success': False,
            'articles_count': 0,
            'file_path': None,
            'email_sent': False,
            'error': None
        }
        
        try:
            logger.info("=" * 50)
            logger.info("开始生成 AI 每日简报")
            logger.info("=" * 50)
            
            # 1. 抓取RSS源
            logger.info("步骤 1/4: 抓取RSS源...")
            articles = self.fetcher.fetch_all_feeds(
                max_articles_per_source=SYSTEM_CONFIG.get('max_articles_per_source', 5),
                hours_back=hours_back
            )
            
            if not articles:
                logger.warning("未获取到任何新文章")
                result['error'] = "未获取到任何新文章"
                return result
            
            result['articles_count'] = len(articles)
            logger.info(f"共获取 {len(articles)} 篇文章")
            
            # 2. LLM分析（如果启用）
            analysis = None
            categories = None
            
            if self.analyzer:
                logger.info("步骤 2/4: 使用LLM进行智能分析...")
                
                # 生成综合分析
                analysis = self.analyzer.generate_daily_digest(articles)
                
                # 分类文章
                categories = self.analyzer.categorize_articles(articles)
                
                # 为重要文章生成中文摘要（限制数量以节省API调用）
                priority_articles = [a for a in articles if a.get('priority', 5) <= 2][:10]
                for article in priority_articles:
                    if not article.get('chinese_summary'):
                        article['chinese_summary'] = self.analyzer.summarize_article(article)
                
                logger.info("LLM分析完成")
            else:
                logger.info("步骤 2/4: LLM分析已禁用，跳过...")
            
            # 3. 生成简报
            logger.info("步骤 3/4: 生成Markdown简报...")
            
            # 限制文章总数
            max_articles = SYSTEM_CONFIG.get('max_total_articles', 30)
            articles = articles[:max_articles]
            
            markdown_content = self.generator.generate_markdown(
                articles, 
                analysis=analysis,
                categories=categories
            )
            
            # 保存文件
            if save_file:
                file_path = self.generator.save_digest(markdown_content)
                result['file_path'] = file_path
                logger.info(f"简报已保存到: {file_path}")

            # 更新网页数据
            if update_web:
                try:
                    web_data = {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "articles": articles,
                        "analysis": analysis
                    }
                    
                    # 如果没有提供路径，使用默认路径（本地开发环境）
                    if not web_data_path:
                        web_public_dir = "/home/ubuntu/ai-digest-web/client/public"
                        os.makedirs(web_public_dir, exist_ok=True)
                        target_path = os.path.join(web_public_dir, "data.json")
                    else:
                        # 使用传入的路径
                        target_dir = os.path.dirname(web_data_path)
                        if target_dir:
                            os.makedirs(target_dir, exist_ok=True)
                        target_path = web_data_path
                    
                    with open(target_path, 'w', encoding='utf-8') as f:
                        json.dump(web_data, f, ensure_ascii=False, indent=2)
                    
                    logger.info(f"网页数据已更新到: {target_path}")
                except Exception as e:
                    logger.error(f"更新网页数据失败: {e}")
            
            # 4. 发送邮件
            if send_email:
                logger.info("步骤 4/4: 发送邮件...")
                
                if not self.email_sender.is_configured():
                    logger.warning("邮件未配置，跳过发送")
                    logger.info("请在 config.py 中配置 EMAIL_CONFIG")
                else:
                    # 生成HTML版本
                    html_content = self.generator.generate_html(markdown_content)
                    
                    # 发送邮件
                    today = datetime.now().strftime("%Y-%m-%d")
                    subject = f"AI 每日简报 - {today}"
                    
                    email_sent = self.email_sender.send_email(
                        subject=subject,
                        html_content=html_content,
                        markdown_content=markdown_content,
                        attachment_path=result.get('file_path')
                    )
                    
                    result['email_sent'] = email_sent
                    if email_sent:
                        logger.info("邮件发送成功")
                    else:
                        logger.warning("邮件发送失败")
            else:
                logger.info("步骤 4/4: 跳过邮件发送")
            
            result['success'] = True
            logger.info("=" * 50)
            logger.info("简报生成完成！")
            logger.info("=" * 50)
            
        except Exception as e:
            logger.error(f"生成简报时发生错误: {e}", exc_info=True)
            result['error'] = str(e)
        
        return result
    
    def test_fetch(self) -> None:
        """测试RSS抓取"""
        logger.info("测试RSS抓取...")
        articles = self.fetcher.fetch_all_feeds(max_articles_per_source=2, hours_back=72)
        
        print(f"\n获取到 {len(articles)} 篇文章:\n")
        for i, article in enumerate(articles[:10], 1):
            print(f"{i}. [{article['source_name']}] {article['title']}")
            print(f"   链接: {article['link'][:80]}...")
            print()
    
    def test_email(self) -> None:
        """测试邮件发送"""
        logger.info("测试邮件发送...")
        if self.email_sender.is_configured():
            if self.email_sender.send_test_email():
                print("测试邮件发送成功！")
            else:
                print("测试邮件发送失败，请检查配置。")
        else:
            print("邮件未配置，请先在 config.py 中配置 EMAIL_CONFIG")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='AI Daily Digest - AI领域每日简报生成器')
    parser.add_argument('--no-email', action='store_true', help='不发送邮件')
    parser.add_argument('--no-save', action='store_true', help='不保存文件')
    parser.add_argument('--hours', type=int, default=48, help='抓取多少小时内的文章（默认48）')
    parser.add_argument('--test-fetch', action='store_true', help='测试RSS抓取')
    parser.add_argument('--test-email', action='store_true', help='测试邮件发送')
    parser.add_argument('--update-web-path', type=str, help='更新网页数据文件路径')
    
    args = parser.parse_args()
    
    # 确保日志目录存在
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(base_dir, 'logs'), exist_ok=True)
    
    digest = AIDailyDigest()
    
    if args.test_fetch:
        digest.test_fetch()
    elif args.test_email:
        digest.test_email()
    else:
        result = digest.run(
            send_email=not args.no_email,
            save_file=not args.no_save,
            hours_back=args.hours,
            update_web=args.update_web_path is not None,
            web_data_path=args.update_web_path
        )
        
        print("\n" + "=" * 50)
        print("运行结果:")
        print(f"  - 成功: {result['success']}")
        print(f"  - 文章数: {result['articles_count']}")
        print(f"  - 文件路径: {result['file_path']}")
        print(f"  - 邮件已发送: {result['email_sent']}")
        if result['error']:
            print(f"  - 错误: {result['error']}")
        print("=" * 50)


if __name__ == "__main__":
    main()
