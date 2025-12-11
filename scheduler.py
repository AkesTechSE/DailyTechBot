import schedule
import time
import logging
import os
from bot import TechNewsBot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POST_TIME = os.getenv("POST_TIME", "09:00")

bot = TechNewsBot()

def job():
    logger.info("Running scheduled job...")
    bot.post_daily_digest(num_articles=5)

# Schedule daily job
schedule.every().day.at(POST_TIME).do(job)
logger.info(f"Scheduler started. Daily posts scheduled for {POST_TIME}")

# Initial post on startup
job()

# Run scheduler loop
while True:
    schedule.run_pending()
    time.sleep(30)
