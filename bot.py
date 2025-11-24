"""
Telegram Bot Module
Handles posting tech news to Telegram channel.
"""

import os
import logging
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.error import TelegramError
from dotenv import load_dotenv
from news_fetcher import NewsFetcher

# Load environment variables
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TechNewsBot:
    """Telegram bot for posting tech news."""
    
    def __init__(self):
        """Initialize the bot with configuration from environment variables."""
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
        
        if not self.token or not self.channel_id:
            raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID must be set in .env file")
        
        self.bot = Bot(token=self.token)
        self.news_fetcher = NewsFetcher(max_articles=3)
    
    def format_article(self, article):
        """
        Format an article for Telegram posting.
        
        Args:
            article (dict): Article data
            
        Returns:
            str: Formatted message text
        """
        title = article['title']
        description = article['description']
        source = article['source']
        link = article['link']
        
        # Create a visually appealing message with emojis
        message = f"📰 *{title}*\n\n"
        
        if description:
            message += f"{description}\n\n"
        
        message += f"📌 Source: {source}\n"
        message += f"🔗 [Read full article]({link})"
        
        return message
    
    def post_article(self, article):
        """
        Post a single article to the Telegram channel.
        
        Args:
            article (dict): Article data
            
        Returns:
            bool: True if posted successfully, False otherwise
        """
        try:
            message = self.format_article(article)
            image_url = article.get('image_url', '')
            
            if image_url:
                # Post with image
                self.bot.send_photo(
                    chat_id=self.channel_id,
                    photo=image_url,
                    caption=message,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                # Post without image
                self.bot.send_message(
                    chat_id=self.channel_id,
                    text=message,
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=False
                )
            
            logger.info(f"Posted article: {article['title']}")
            return True
            
        except TelegramError as e:
            logger.error(f"Error posting article '{article['title']}': {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error posting article: {e}")
            return False
    
    def post_daily_digest(self, num_articles=10):
        """
        Post the daily tech news digest to the channel.
        
        Args:
            num_articles (int): Number of articles to post
            
        Returns:
            int: Number of articles successfully posted
        """
        logger.info("Starting daily digest posting...")
        
        # Post header message
        try:
            header = (
                "🚀 *Daily Tech Insights* 🚀\n\n"
                "Good morning! Here are today's top tech stories:\n"
                "━━━━━━━━━━━━━━━━━━━━━━"
            )
            self.bot.send_message(
                chat_id=self.channel_id,
                text=header,
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            logger.error(f"Error posting header: {e}")
        
        # Fetch and post articles
        articles = self.news_fetcher.get_daily_digest(num_articles=num_articles)
        
        posted_count = 0
        for article in articles:
            if self.post_article(article):
                posted_count += 1
        
        # Post footer message
        try:
            footer = (
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "✨ That's all for today! Stay curious and keep innovating! 💻\n\n"
                "📱 Follow us for daily tech updates!"
            )
            self.bot.send_message(
                chat_id=self.channel_id,
                text=footer,
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            logger.error(f"Error posting footer: {e}")
        
        logger.info(f"Daily digest completed. Posted {posted_count}/{len(articles)} articles.")
        return posted_count
    
    def test_connection(self):
        """
        Test the bot connection and channel access.
        
        Returns:
            bool: True if connection is successful
        """
        try:
            bot_info = self.bot.get_me()
            logger.info(f"Bot connected: @{bot_info.username}")
            
            # Try sending a test message
            test_message = "🤖 Bot connection test successful!"
            self.bot.send_message(
                chat_id=self.channel_id,
                text=test_message
            )
            logger.info(f"Successfully sent message to channel: {self.channel_id}")
            return True
            
        except TelegramError as e:
            logger.error(f"Connection test failed: {e}")
            return False


if __name__ == "__main__":
    # Test the bot
    try:
        bot = TechNewsBot()
        
        # Test connection
        if bot.test_connection():
            print("\n✅ Bot connection successful!")
            
            # Post daily digest
            print("\nPosting daily digest...")
            posted = bot.post_daily_digest(num_articles=5)
            print(f"\n✅ Posted {posted} articles!")
        else:
            print("\n❌ Bot connection failed. Check your credentials.")
            
    except ValueError as e:
        print(f"\n❌ Configuration error: {e}")
        print("Please create a .env file with TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID")
    except Exception as e:
        print(f"\n❌ Error: {e}")
