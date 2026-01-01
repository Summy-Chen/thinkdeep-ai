"""
ThinkDeep.ai - 配置文件
请在此文件中填入您的邮箱配置信息
"""

# ==================== 邮件配置 ====================
EMAIL_CONFIG = {
    "smtp_server": "smtp.qq.com",      # SMTP服务器地址
    "smtp_port": 465,                   # SMTP端口 (SSL用465, TLS用587)
    "use_ssl": True,                    # 是否使用SSL (端口465时为True)
    "sender_email": "chenysh48@foxmail.com",                 # 发件人邮箱地址
    "sender_password": "byxjmepqwtnycabc",              # 邮箱授权码 (非登录密码，需在邮箱设置中获取)
    "recipient_email": "chenysh48@foxmail.com",  # 收件人邮箱
}

# ==================== RSS源配置 ====================
RSS_FEEDS = {
    # 商业与创投 (Business & VC) - 优先级最高
    "techcrunch_ai": {
        "name": "TechCrunch AI",
        "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
        "category": "business",
        "priority": 1,
    },
    "venturebeat_ai": {
        "name": "VentureBeat AI",
        "url": "https://venturebeat.com/category/ai/feed/",
        "category": "business",
        "priority": 1,
    },
    "the_verge_ai": {
        "name": "The Verge AI",
        "url": "https://www.theverge.com/rss/artificial-intelligence/index.xml",
        "category": "business",
        "priority": 1,
    },
    "mit_tech_review": {
        "name": "MIT Technology Review",
        "url": "https://www.technologyreview.com/feed/",
        "category": "business",
        "priority": 1,
    },
    "wired_ai": {
        "name": "Wired AI",
        "url": "https://www.wired.com/feed/rss",
        "category": "business",
        "priority": 2,
        "hours_back_override": 48,  # Wired 更新频率较低，使用更长的时间窗口
    },

    # AI公司官方博客
    "openai_blog": {
        "name": "OpenAI Blog",
        "url": "https://openai.com/blog/rss.xml",
        "category": "company",
        "priority": 1,
    },
    "google_ai": {
        "name": "Google AI Blog", 
        "url": "https://blog.google/technology/ai/rss/",
        "category": "company",
        "priority": 1,
    },
    "deepmind": {
        "name": "Google DeepMind",
        "url": "https://deepmind.google/blog/rss.xml",
        "category": "company", 
        "priority": 1,
    },
    "microsoft_ai": {
        "name": "Microsoft AI",
        "url": "https://blogs.microsoft.com/ai/feed/",
        "category": "company",
        "priority": 1,
    },
    "anthropic": {
        "name": "Anthropic",
        "url": "https://www.anthropic.com/news/rss",
        "category": "company",
        "priority": 1,
    },
    "nvidia_blog": {
        "name": "NVIDIA Blog",
        "url": "https://blogs.nvidia.com/feed/",
        "category": "company",
        "priority": 2,
    },
    
    # 学术研究
    "bair": {
        "name": "Berkeley AI Research",
        "url": "https://bair.berkeley.edu/blog/feed.xml",
        "category": "research",
        "priority": 2,
    },
    "mit_ai": {
        "name": "MIT AI News",
        "url": "https://news.mit.edu/rss/topic/artificial-intelligence2",
        "category": "research",
        "priority": 2,
    },
    "arxiv_cs_ai": {
        "name": "arXiv CS.AI",
        "url": "http://arxiv.org/rss/cs.AI",
        "category": "research",
        "priority": 3,
    },
    "arxiv_cs_lg": {
        "name": "arXiv CS.LG (Machine Learning)",
        "url": "http://arxiv.org/rss/cs.LG",
        "category": "research",
        "priority": 3,
    },
    
    # 技术博客
    "simon_willison": {
        "name": "Simon Willison's Blog",
        "url": "https://simonwillison.net/atom/everything/",
        "category": "blog",
        "priority": 1,
    },
    "lilian_weng": {
        "name": "Lilian Weng's Blog",
        "url": "https://lilianweng.github.io/index.xml",
        "category": "blog",
        "priority": 2,
    },
    "hugging_face": {
        "name": "Hugging Face Blog",
        "url": "https://huggingface.co/blog/feed.xml",
        "category": "blog",
        "priority": 1,
    },
    
    # 社区
    "hn_ai": {
        "name": "Hacker News AI",
        "url": "https://hnrss.org/newest?q=AI+OR+LLM+OR+GPT+OR+Claude+OR+OpenAI&points=50",
        "category": "community",
        "priority": 2,
    },
    "reddit_ml": {
        "name": "Reddit Machine Learning",
        "url": "https://www.reddit.com/r/MachineLearning/.rss",
        "category": "community",
        "priority": 3,
    },
}

# ==================== 系统配置 ====================
SYSTEM_CONFIG = {
    "max_articles_per_source": 5,       # 每个源最多抓取的文章数
    "max_total_articles": 40,           # 简报中最多包含的文章总数
    "summary_max_length": 200,          # 摘要最大字符数
    "digest_title": "ThinkDeep.ai 每日简报", # 简报标题
    "data_dir": "data",                  # 数据存储目录
    "output_dir": "output",              # 输出目录
    "log_dir": "logs",                   # 日志目录
    "hours_back": 48,                    # 默认抓取最近48小时的文章（提升抓取成功率）
    "hours_back_by_category": {          # 根据类别调整时间窗口
        "business": 48,                  # 商业新闻：48小时
        "company": 72,                   # 公司博客：72小时（更新频率较低）
        "research": 168,                 # 学术研究：7天（论文发布周期较长）
        "blog": 72,                      # 技术博客：72小时
        "community": 24,                 # 社区：24小时（更新频繁）
    },
    "retry_attempts": 3,                # 重试次数
    "retry_delay": 2,                    # 重试延迟（秒）
    "user_agent": "ThinkDeep.ai/1.0 (AI Digest Bot)"
}

# ==================== LLM配置 (用于智能摘要) ====================
LLM_CONFIG = {
    "enabled": True,
    "model": "gpt-4.1-mini",
    "max_tokens": 1000,
}
