from bot import TechNewsBot
import os

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Make sure TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID are set in your environment.")

import asyncio

if __name__ == "__main__":
    bot = TechNewsBot()
    asyncio.run(bot.post_daily_digest(num_articles=5))
