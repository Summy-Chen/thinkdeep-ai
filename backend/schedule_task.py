"""
定时任务脚本
用于每日自动执行简报生成任务
"""

import schedule
import time
import logging
import os
import sys
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import AIDailyDigest

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            os.path.join(os.path.dirname(__file__), 'logs', 'scheduler.log'),
            encoding='utf-8'
        )
    ]
)
logger = logging.getLogger(__name__)

def job():
    """执行每日任务"""
    logger.info("开始执行每日定时任务...")
    try:
        digest = AIDailyDigest()
        result = digest.run(send_email=True, save_file=True)
        
        if result['success']:
            logger.info("每日任务执行成功")
            
            # 如果有网页项目，更新网页数据
            # 这里是一个简单的示例，实际可能需要更复杂的数据同步逻辑
            web_data_path = "/home/ubuntu/ai-digest-web/client/src/lib/mock-data.ts"
            if os.path.exists(web_data_path) and result.get('file_path'):
                logger.info("正在更新网页数据...")
                # TODO: 实现将Markdown/JSON转换为TypeScript数据的逻辑
                pass
        else:
            logger.error(f"每日任务执行失败: {result.get('error')}")
            
    except Exception as e:
        logger.error(f"定时任务发生异常: {e}", exc_info=True)

def main():
    """主函数"""
    logger.info("AI Daily Digest 定时任务服务已启动")
    
    # 每天早上 8:00 执行
    schedule.every().day.at("08:00").do(job)
    
    logger.info("已设置定时任务: 每天 08:00 执行")
    
    # 立即执行一次以测试（可选）
    # job()
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
