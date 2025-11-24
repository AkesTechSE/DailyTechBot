"""
News Fetcher Module
Fetches tech news from multiple sources including TechCrunch, The Verge, and Wired.
"""

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsFetcher:
    """Fetches tech news from various sources."""
    
    RSS_FEEDS = {
        'TechCrunch': 'https://techcrunch.com/feed/',
        'The Verge': 'https://www.theverge.com/rss/index.xml',
        'Wired': 'https://www.wired.com/feed/rss',
    }
    
    CATEGORIES = ['AI', 'startups', 'apps', 'hardware', 'gadgets', 'software', 'innovation']
    
    def __init__(self, max_articles=5):
        """
        Initialize the news fetcher.
        
        Args:
            max_articles (int): Maximum number of articles to fetch per source
        """
        self.max_articles = max_articles
    
    def fetch_feed(self, feed_url, source_name):
        """
        Fetch articles from an RSS feed.
        
        Args:
            feed_url (str): URL of the RSS feed
            source_name (str): Name of the news source
            
        Returns:
            list: List of article dictionaries
        """
        try:
            feed = feedparser.parse(feed_url)
            articles = []
            
            for entry in feed.entries[:self.max_articles]:
                article = {
                    'title': entry.get('title', 'No Title'),
                    'link': entry.get('link', ''),
                    'description': self._clean_description(entry.get('summary', '')),
                    'published': entry.get('published', ''),
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
        """
        Clean HTML tags from description text.
        
        Args:
            text (str): Raw description text
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        soup = BeautifulSoup(text, 'lxml')
        cleaned = soup.get_text()
        
        # Limit to first 200 characters
        if len(cleaned) > 200:
            cleaned = cleaned[:197] + "..."
        
        return cleaned.strip()
    
    def _extract_image(self, entry):
        """
        Extract image URL from feed entry.
        
        Args:
            entry: Feed entry object
            
        Returns:
            str: Image URL or empty string
        """
        # Try different ways to get image
        if hasattr(entry, 'media_content'):
            for media in entry.media_content:
                if media.get('medium') == 'image':
                    return media.get('url', '')
        
        if hasattr(entry, 'media_thumbnail'):
            if entry.media_thumbnail:
                return entry.media_thumbnail[0].get('url', '')
        
        # Try to extract from content
        if hasattr(entry, 'content'):
            soup = BeautifulSoup(entry.content[0].value, 'lxml')
            img = soup.find('img')
            if img and img.get('src'):
                return img['src']
        
        # Try summary
        if hasattr(entry, 'summary'):
            soup = BeautifulSoup(entry.summary, 'lxml')
            img = soup.find('img')
            if img and img.get('src'):
                return img['src']
        
        return ""
    
    def fetch_all_news(self):
        """
        Fetch news from all sources.
        
        Returns:
            list: Combined list of articles from all sources
        """
        all_articles = []
        
        for source_name, feed_url in self.RSS_FEEDS.items():
            articles = self.fetch_feed(feed_url, source_name)
            all_articles.extend(articles)
        
        # Sort by relevance (could be improved with better ranking)
        logger.info(f"Total articles fetched: {len(all_articles)}")
        return all_articles
    
    def get_daily_digest(self, num_articles=10):
        """
        Get a curated daily digest of tech news.
        
        Args:
            num_articles (int): Number of articles to include in digest
            
        Returns:
            list: List of top articles for the day
        """
        all_articles = self.fetch_all_news()
        
        # Return top articles (could add more sophisticated filtering)
        return all_articles[:num_articles]


if __name__ == "__main__":
    # Test the news fetcher
    fetcher = NewsFetcher(max_articles=3)
    articles = fetcher.get_daily_digest(num_articles=5)
    
    print(f"\nFetched {len(articles)} articles:\n")
    for i, article in enumerate(articles, 1):
        print(f"{i}. {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   Link: {article['link']}")
        print(f"   Has image: {'Yes' if article['image_url'] else 'No'}")
        print()
