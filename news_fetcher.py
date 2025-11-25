"""
News Fetcher Module
Fetches tech news from multiple sources including TechCrunch, The Verge, and Wired.
"""

import feedparser
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsFetcher:
    """Fetches tech news from various sources."""

    RSS_FEEDS = {
        'TechCrunch': 'https://techcrunch.com/feed/',
        'The Verge': 'https://www.theverge.com/rss/index.xml',
        'Wired': 'https://www.wired.com/feed/rss',
    }

    def __init__(self, max_articles=5):
        self.max_articles = max_articles

    def fetch_feed(self, feed_url, source_name):
        try:
            feed = feedparser.parse(feed_url)
            articles = []

            for entry in feed.entries[:self.max_articles]:
                article = {
                    'title': entry.get('title', 'No Title'),
                    'link': entry.get('link', ''),
                    'description': self._clean_description(entry.get('summary', '')),
                    'source': source_name,
                    'image_url': self._extract_image(entry)
                }
                articles.append(article)

            logger.info(f"Fetched {len(articles)} articles from {source_name}")
            return articles

        except Exception as e:
            logger.error(f"Error fetching feed from {source_name}: {e}")
            return []

    def _clean_description(self, text):
        if not text:
            return ""
        soup = BeautifulSoup(text, 'lxml')
        cleaned = soup.get_text()
        return (cleaned[:197] + "...") if len(cleaned) > 200 else cleaned.strip()

    def _extract_image(self, entry):
        # Try different ways to get image
        if hasattr(entry, 'media_content'):
            for media in entry.media_content:
                if media.get('medium') == 'image':
                    return media.get('url', '')
        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            return entry.media_thumbnail[0].get('url', '')
        if hasattr(entry, 'content'):
            soup = BeautifulSoup(entry.content[0].value, 'lxml')
            img = soup.find('img')
            if img and img.get('src'):
                return img['src']
        if hasattr(entry, 'summary'):
            soup = BeautifulSoup(entry.summary, 'lxml')
            img = soup.find('img')
            if img and img.get('src'):
                return img['src']
        return ""

    def fetch_all_news(self):
        all_articles = []
        for source_name, feed_url in self.RSS_FEEDS.items():
            all_articles.extend(self.fetch_feed(feed_url, source_name))
        logger.info(f"Total articles fetched: {len(all_articles)}")
        return all_articles

    def get_daily_digest(self, num_articles=10):
        all_articles = self.fetch_all_news()
        return all_articles[:num_articles]
