"""
Main entry point for DailyTechBot
"""

import sys
import logging
import asyncio
from scheduler import run_scheduler_async

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("=" * 50)
    logger.info("DailyTechBot - Tech News Telegram Channel")
    logger.info("=" * 50)

    try:
        await run_scheduler_async()
    except KeyboardInterrupt:
        logger.info("\nBot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
