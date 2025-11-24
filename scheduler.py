"""
Scheduler Module
Handles automated daily posting at 9:00 AM.
"""

import os
import schedule
import time
import logging
from datetime import datetime
from dotenv import load_dotenv
from bot import TechNewsBot

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def post_daily_news():
    """Job function to post daily tech news."""
    logger.info(f"Starting scheduled job at {datetime.now()}")
    
    try:
        bot = TechNewsBot()
        posted = bot.post_daily_digest(num_articles=10)
        logger.info(f"Scheduled job completed. Posted {posted} articles.")
    except Exception as e:
        logger.error(f"Error in scheduled job: {e}")


def run_scheduler():
    """Run the scheduler to post news daily at configured time."""
    post_time = os.getenv('POST_TIME', '09:00')
    
    logger.info(f"Scheduler started. Daily posts scheduled for {post_time}")
    
    # Schedule the daily job
    schedule.every().day.at(post_time).do(post_daily_news)
    
    # Run immediately on startup (optional - comment out if not desired)
    logger.info("Running initial post on startup...")
    post_daily_news()
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    logger.info("Starting DailyTechBot Scheduler...")
    
    try:
        run_scheduler()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    except Exception as e:
        logger.error(f"Scheduler error: {e}")
