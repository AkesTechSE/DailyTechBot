
import logging
import os
import asyncio
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Make sure TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID are set in your environment.")
from bot import TechNewsBot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POST_TIME = os.getenv("POST_TIME", "09:00")

bot = TechNewsBot()

async def job():
    logger.info("Running scheduled job...")
    await bot.post_daily_digest(num_articles=5)

def get_cron_time(post_time):
    hour, minute = post_time.split(":")
    return int(hour), int(minute)

async def main():
    scheduler = AsyncIOScheduler()
    hour, minute = get_cron_time(POST_TIME)
    scheduler.add_job(job, CronTrigger(hour=hour, minute=minute))
    logger.info(f"Scheduler started. Daily posts scheduled for {POST_TIME}")
    scheduler.start()
    # Initial post on startup
    await job()
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    asyncio.run(main())
