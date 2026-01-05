"""
Main entry point for DailyTechBot.
Starts the async scheduler loop that posts the daily digest.
"""

import asyncio
import logging
from scheduler import main as start_scheduler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("DailyTechBot - Tech News Telegram Channel")
    logger.info("=" * 50)

    try:
        asyncio.run(start_scheduler())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
