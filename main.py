"""
Main entry point for DailyTechBot
Runs the scheduler for daily posts
"""

import logging
from scheduler import bot  # import bot instance from scheduler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("DailyTechBot - Tech News Telegram Channel")
    logger.info("=" * 50)

    try:
        # The scheduler loop runs in scheduler.py
        import scheduler  # ensures the scheduler loop runs
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
