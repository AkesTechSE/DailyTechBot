"""
Scheduler for DailyTechBot
Uses schedule + asyncio to run async daily posts
"""

import asyncio
import logging
from datetime import datetime
import schedule
from bot import TechNewsBot
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POST_TIME = os.getenv("POST_TIME", "09:00")

async def job(bot=None):
    """Async job to post daily digest"""
    bot = bot or TechNewsBot()
    logger.info(f"Starting scheduled job at {datetime.now()}")
    posted = await bot.post_daily_digest(num_articles=5)
    logger.info(f"Scheduled job completed. Posted {posted} articles.")

async def run_scheduler_async():
    """Run the scheduler asynchronously"""
    bot_instance = TechNewsBot()
    schedule.every().day.at(POST_TIME).do(lambda: asyncio.create_task(job(bot_instance)))
    logger.info(f"Scheduler started. Daily posts scheduled for {POST_TIME}")

    # Initial post on startup
    await job(bot_instance)

    while True:
        schedule.run_pending()
        await asyncio.sleep(30)
