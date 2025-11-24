"""
Main entry point for DailyTechBot
"""

import sys
import logging
from scheduler import run_scheduler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Main function to start the bot."""
    logger.info("=" * 50)
    logger.info("DailyTechBot - Tech News Telegram Channel")
    logger.info("=" * 50)
    
    try:
        run_scheduler()
    except KeyboardInterrupt:
        logger.info("\nBot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
