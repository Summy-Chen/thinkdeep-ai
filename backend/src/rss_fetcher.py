"""
RSS Feed 抓取模块
负责从配置的RSS源获取最新文章
"""

import feedparser
import requests
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
import logging
import hashlib
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import SYSTEM_CONFIG

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RSSFetcher:
    """RSS源抓取器"""
    
    def __init__(self, feeds_config: Dict, data_dir: str = "data"):
        """
        初始化抓取器
        
        Args:
            feeds_config: RSS源配置字典
            data_dir: 数据存储目录
        """
        self.feeds_config = feeds_config
        self.data_dir = data_dir
        self.cache_file = os.path.join(data_dir, "article_cache.json")
        self.seen_articles = self._load_cache()
        
        # 请求头，模拟浏览器
        self.headers = {
            "User-Agent": SYSTEM_CONFIG.get('user_agent', 'ThinkDeep.ai/1.0'),
            "Accept": "application/rss+xml, application/xml, text/xml, */*",
        }
    
    def _load_cache(self) -> set:
        """加载已抓取文章的缓存"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    # 只保留最近7天的缓存
                    cutoff = (datetime.now() - timedelta(days=7)).isoformat()
                    return set(k for k, v in data.items() if v.get('date', '') > cutoff)
            except Exception as e:
                logger.warning(f"加载缓存失败: {e}")
        return set()
    
    def _save_cache(self, new_articles: List[Dict]):
        """保存文章缓存"""
        try:
            cache_data = {}
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)
            
            for article in new_articles:
                article_id = self._get_article_id(article)
                cache_data[article_id] = {
                    'date': datetime.now().isoformat(),
                    'title': article.get('title', '')[:100]
                }
            
            # 清理旧缓存
            cutoff = (datetime.now() - timedelta(days=7)).isoformat()
            cache_data = {k: v for k, v in cache_data.items() if v.get('date', '') > cutoff}
            
            os.makedirs(self.data_dir, exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            logger.warning(f"保存缓存失败: {e}")
    
    def _get_article_id(self, article: Dict) -> str:
        """生成文章唯一ID"""
        content = f"{article.get('title', '')}{article.get('link', '')}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _parse_date(self, entry) -> Optional[datetime]:
        """解析文章发布日期"""
        date_fields = ['published_parsed', 'updated_parsed', 'created_parsed']
        for field in date_fields:
            if hasattr(entry, field) and getattr(entry, field):
                try:
                    time_struct = getattr(entry, field)
                    # 转换为带时区的datetime (UTC)
                    dt = datetime(*time_struct[:6], tzinfo=timezone.utc)
                    return dt
                except:
                    continue
        return None
    
    def _is_valid_link(self, url: str) -> bool:
        """验证链接是否有效"""
        if not url or not isinstance(url, str):
            return False
        # 确保链接以 http:// 或 https:// 开头
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            return False
        # 基本URL格式验证
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            if not parsed.netloc:  # 必须有域名
                return False
            return True
        except:
            return False
    
    def _normalize_link(self, url: str) -> str:
        """规范化链接，确保可以正确跳转"""
        if not url:
            return url
        url = url.strip()
        # 移除常见的跟踪参数（可选，保留原始链接）
        # 这里我们保留原始链接，确保用户可以访问源网页
        return url

    def fetch_single_feed(self, feed_id: str, feed_config: Dict, 
                          max_articles: int = 5,
                          hours_back: int = 24,
                          retry_attempts: int = 3,
                          retry_delay: int = 2) -> List[Dict]:
        """
        抓取单个RSS源
        
        Args:
            feed_id: 源ID
            feed_config: 源配置
            max_articles: 最大文章数
            hours_back: 抓取多少小时内的文章
            
        Returns:
            文章列表
        """
        articles = []
        url = feed_config.get('url', '')
        name = feed_config.get('name', feed_id)
        
        # 获取该源的自定义时间窗口（如果有）
        source_hours_back = feed_config.get('hours_back_override', hours_back)
        
        # 重试机制
        last_exception = None
        for attempt in range(retry_attempts):
            try:
                if attempt > 0:
                    logger.info(f"重试抓取 {name} (第 {attempt + 1}/{retry_attempts} 次)...")
                    time.sleep(retry_delay * attempt)  # 递增延迟
                
                logger.info(f"正在抓取: {name}")
                
                # 使用requests获取内容，处理一些特殊情况
                response = requests.get(url, headers=self.headers, timeout=15)
                response.raise_for_status()
                break  # 成功则跳出重试循环
                
            except requests.exceptions.Timeout:
                last_exception = f"超时"
                if attempt == retry_attempts - 1:
                    logger.warning(f"抓取 {name} 超时（已重试 {retry_attempts} 次）")
                    return articles
                continue
            except requests.exceptions.RequestException as e:
                last_exception = str(e)
                if attempt == retry_attempts - 1:
                    logger.warning(f"抓取 {name} 失败: {e}（已重试 {retry_attempts} 次）")
                    return articles
                continue
        
        try:
            
            # 解析RSS
            feed = feedparser.parse(response.content)
            
            if feed.bozo and not feed.entries:
                logger.warning(f"解析 {name} 时出现问题: {feed.bozo_exception}")
                return articles
            
            # 使用带时区的当前时间，优先使用源的自定义时间窗口
            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=source_hours_back)
            
            for entry in feed.entries[:max_articles * 2]:  # 多取一些以防过滤后不够
                try:
                    # 解析日期
                    pub_date = self._parse_date(entry)
                    
                    # 严格过滤旧文章
                    if pub_date:
                        if pub_date < cutoff_time:
                            continue
                    else:
                        # 如果没有日期，使用更保守的策略
                        # 对于没有日期的文章，如果源优先级高，放宽时间限制
                        source_priority = feed_config.get('priority', 5)
                        if source_priority <= 2:
                            # 高优先级源：如果没有日期，假设是最近的文章（但标记为当前时间减去12小时，避免排在最新）
                            pub_date = datetime.now(timezone.utc) - timedelta(hours=12)
                        else:
                            # 低优先级源：如果没有日期，跳过（避免抓取到很旧的文章）
                            logger.debug(f"跳过无日期的文章: {entry.get('title', '')[:50]}")
                            continue
                    
                    # 验证和规范化链接
                    link = entry.get('link', '')
                    if not self._is_valid_link(link):
                        logger.debug(f"无效链接，跳过: {link[:50] if link else 'None'}")
                        continue
                    
                    # 规范化链接，确保可以正确跳转
                    link = self._normalize_link(link)

                    # 构建文章对象
                    article = {
                        'id': self._get_article_id({'title': entry.get('title', ''), 'link': link}),
                        'title': entry.get('title', '无标题'),
                        'link': link,  # 确保链接可跳转
                        'summary': self._clean_summary(entry.get('summary', entry.get('description', ''))),
                        'published': pub_date.isoformat(),
                        'source_id': feed_id,
                        'source_name': name,
                        'category': feed_config.get('category', 'other'),
                        'priority': feed_config.get('priority', 5),
                    }
                    
                    # 检查是否已抓取过
                    if article['id'] not in self.seen_articles:
                        articles.append(article)
                        self.seen_articles.add(article['id'])
                        
                        if len(articles) >= max_articles:
                            break
                            
                except Exception as e:
                    logger.warning(f"解析文章时出错: {e}")
                    continue
            
            logger.info(f"从 {name} 获取了 {len(articles)} 篇新文章")
            
        except Exception as e:
            logger.error(f"处理 {name} 时发生错误: {e}")
        
        return articles
    
    def _clean_summary(self, summary: str, max_length: int = 500) -> str:
        """清理摘要文本"""
        import re
        # 移除HTML标签
        clean = re.sub(r'<[^>]+>', '', summary)
        # 移除多余空白
        clean = ' '.join(clean.split())
        # 截断
        if len(clean) > max_length:
            clean = clean[:max_length] + '...'
        return clean
    
    def fetch_all_feeds(self, max_articles_per_source: int = 5,
                        hours_back: int = 24,
                        retry_attempts: int = 3,
                        retry_delay: int = 2) -> List[Dict]:
        """
        并行抓取所有RSS源
        
        Args:
            max_articles_per_source: 每个源最大文章数
            hours_back: 默认抓取多少小时内的文章
            retry_attempts: 重试次数
            retry_delay: 重试延迟（秒）
            
        Returns:
            所有文章列表
        """
        all_articles = []
        
        # 根据类别获取时间窗口
        hours_back_by_category = SYSTEM_CONFIG.get('hours_back_by_category', {})
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(
                    self.fetch_single_feed, 
                    feed_id, 
                    feed_config, 
                    max_articles_per_source,
                    hours_back_by_category.get(feed_config.get('category', 'other'), hours_back),
                    retry_attempts,
                    retry_delay
                ): feed_id 
                for feed_id, feed_config in self.feeds_config.items()
            }
            
            for future in as_completed(futures):
                feed_id = futures[future]
                try:
                    articles = future.result()
                    all_articles.extend(articles)
                except Exception as e:
                    logger.error(f"获取 {feed_id} 结果时出错: {e}")
        
        # 优化排序算法：综合考虑优先级、时间和相关性
        # 1. 先按发布时间排序（最新的在前）
        all_articles.sort(key=lambda x: x['published'], reverse=True)
        
        # 2. 然后按优先级调整（高优先级文章提升位置）
        # 计算每个文章的"分数"：时间分数 + 优先级分数
        now = datetime.now(timezone.utc)
        for article in all_articles:
            try:
                pub_time = datetime.fromisoformat(article['published'].replace('Z', '+00:00'))
                hours_ago = (now - pub_time).total_seconds() / 3600
                # 时间分数：越新分数越高（24小时内 = 100分，每过24小时减10分）
                time_score = max(0, 100 - (hours_ago / 24) * 10)
                # 优先级分数：优先级1 = 50分，优先级2 = 30分，优先级3 = 10分
                priority_score = {1: 50, 2: 30, 3: 10}.get(article['priority'], 0)
                article['_sort_score'] = time_score + priority_score
            except:
                article['_sort_score'] = 0
        
        # 3. 按综合分数排序
        all_articles.sort(key=lambda x: x.get('_sort_score', 0), reverse=True)
        
        # 移除临时排序分数
        for article in all_articles:
            article.pop('_sort_score', None)
        
        # 保存缓存
        self._save_cache(all_articles)
        
        logger.info(f"总共获取了 {len(all_articles)} 篇新文章")
        return all_articles


def test_fetcher():
    """测试抓取器"""
    from config import RSS_FEEDS
    
    fetcher = RSSFetcher(RSS_FEEDS, data_dir="/home/ubuntu/ai_daily_digest/data")
    articles = fetcher.fetch_all_feeds(max_articles_per_source=3, hours_back=24)
    
    print(f"\n获取到 {len(articles)} 篇文章:\n")
    for i, article in enumerate(articles[:10], 1):
        print(f"{i}. [{article['source_name']}] {article['title']}")
        print(f"   链接: {article['link']}")
        print(f"   时间: {article['published']}")
        print()


if __name__ == "__main__":
    import sys
    sys.path.insert(0, '/home/ubuntu/ai_daily_digest')
    test_fetcher()
