import os
import logging
from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError
from news_fetcher import NewsFetcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TechNewsBot:
    """Telegram bot for posting tech news (sync)"""

    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.channel_id = os.getenv("TELEGRAM_CHANNEL_ID")

        if not self.token or not self.channel_id:
            raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID must be set")

        self.bot = Bot(token=self.token)
        self.news_fetcher = NewsFetcher(max_articles=5)

    def format_article(self, article):
        title = article['title']
        description = article['description']
        source = article['source']
        link = article['link']

        message = f"📰 *{title}*\n\n"
        if description:
            message += f"{description}\n\n"
        message += f"📌 Source: {source}\n"
        message += f"🔗 [Read full article]({link})"
        return message

    async def post_article(self, article):
        try:
            message = self.format_article(article)
            image_url = article.get('image_url', '')

            if image_url:
                await self.bot.send_photo(
                    chat_id=self.channel_id,
                    photo=image_url,
                    caption=message,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await self.bot.send_message(
                    chat_id=self.channel_id,
                    text=message,
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=False
                )

            logger.info(f"Posted article: {article['title']}")
            return True
        except TelegramError as e:
            logger.error(f"TelegramError posting article '{article['title']}': {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error posting article: {e}")
            return False

    async def post_daily_digest(self, num_articles=5):
        logger.info("Posting daily digest...")
        header = "🚀 *Daily Tech Insights* 🚀\n\nGood morning! Here are today's top tech stories:\n━━━━━━━━━━━━━━━━━━━━━━"
        await self.bot.send_message(chat_id=self.channel_id, text=header, parse_mode=ParseMode.MARKDOWN)

        articles = self.news_fetcher.get_daily_digest(num_articles=num_articles)
        posted_count = 0
        for article in articles:
            if await self.post_article(article):
                posted_count += 1

        footer = "✨ That's all for today! Stay curious and keep innovating! 💻\n\n📱 Follow us for daily tech updates!"
        await self.bot.send_message(chat_id=self.channel_id, text=footer, parse_mode=ParseMode.MARKDOWN)

        logger.info(f"Daily digest completed. Posted {posted_count}/{len(articles)} articles.")
        return posted_count

    async def test_connection(self):
        try:
            bot_info = await self.bot.get_me()
            logger.info(f"Bot connected: @{bot_info.username}")
            await self.bot.send_message(chat_id=self.channel_id, text="🤖 Bot connection test successful!")
            return True
        except TelegramError as e:
            logger.error(f"Connection test failed: {e}")
            return False
