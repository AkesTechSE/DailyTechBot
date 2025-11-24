# DailyTechBot 🚀

**DailyTechInsights** – Tech News Telegram Channel

Stay updated with the latest in technology, gadgets, AI, software, and innovation!

## Features ✨

- 📰 **Curated daily tech news** from top sources like TechCrunch, The Verge, and Wired
- 🖼️ **Visually appealing posts** with images, clickable headlines, and links
- 🎯 **Covers trending topics**: AI, startups, apps, hardware, gadgets, and more
- ⏰ **Automated delivery** every day at 9:00 AM for your convenience
- 🤖 **Telegram channel** integration for easy access

Follow us to never miss a tech update! 📱💻

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Telegram Channel ID

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AkesTechSE/DailyTechBot.git
   cd DailyTechBot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your credentials:
     ```
     TELEGRAM_BOT_TOKEN=your_bot_token_here
     TELEGRAM_CHANNEL_ID=@your_channel_id_here
     POST_TIME=09:00
     ```

### Getting Your Telegram Credentials

1. **Create a Telegram Bot:**
   - Open Telegram and search for [@BotFather](https://t.me/botfather)
   - Send `/newbot` command
   - Follow the instructions to create your bot
   - Save the bot token provided

2. **Create a Telegram Channel:**
   - Create a new public or private channel in Telegram
   - Add your bot as an administrator to the channel
   - For public channels, use `@channelname` as the ID
   - For private channels, you'll need the numeric ID (use [@userinfobot](https://t.me/userinfobot))

### Usage

#### Run Locally

**Test the bot connection:**
```bash
python bot.py
```

**Test the news fetcher:**
```bash
python news_fetcher.py
```

**Run the scheduler (posts daily at configured time):**
```bash
python main.py
```

#### Run with Docker

**Build and run:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f
```

**Stop the bot:**
```bash
docker-compose down
```

### GitHub Actions Deployment

The bot includes two GitHub Actions workflows:

1. **Daily Post Workflow** (`.github/workflows/daily-post.yml`):
   - Automatically posts tech news daily at 9:00 AM UTC
   - Can be manually triggered from the Actions tab

2. **Deploy Workflow** (`.github/workflows/deploy.yml`):
   - Runs on push to main branch
   - Tests the bot functionality

**Setup GitHub Secrets:**
1. Go to your repository Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `TELEGRAM_BOT_TOKEN`: Your bot token
   - `TELEGRAM_CHANNEL_ID`: Your channel ID

## Project Structure

```
DailyTechBot/
├── bot.py              # Telegram bot logic
├── news_fetcher.py     # News fetching from RSS feeds
├── scheduler.py        # Daily scheduling functionality
├── main.py            # Main entry point
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variables template
├── Dockerfile         # Docker container configuration
├── docker-compose.yml # Docker Compose configuration
└── .github/
    └── workflows/
        ├── deploy.yml      # Deployment workflow
        └── daily-post.yml  # Daily posting workflow
```

## Tech Stack

- **Python 3.11**: Core programming language
- **python-telegram-bot**: Telegram Bot API wrapper
- **feedparser**: RSS feed parsing
- **schedule**: Job scheduling
- **BeautifulSoup4**: HTML parsing
- **Docker**: Containerization

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

Made with ❤️ for the tech community
