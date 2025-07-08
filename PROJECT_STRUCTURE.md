# JDX Pulse Project Structure

## Directory Organization

```
jdx-pulse/
├── main.py                    # Main application entry point
├── requirements.txt           # Python dependencies
├── README.md                 # Project documentation
├── PROJECT_STRUCTURE.md      # This file
├── .env                      # Environment variables (not in git)
├── .gitignore               # Git ignore rules
├── cache/                   # Application cache files
│   ├── *.json              # Content cache files
│   └── email_cache.json    # Email sending cache
├── src/                     # Source code
│   ├── __init__.py
│   ├── scrapers/           # Content scrapers
│   │   ├── __init__.py
│   │   ├── youtube_scraper.py
│   │   ├── reddit_scraper.py
│   │   ├── twitter_scraper.py
│   │   ├── github_scraper.py
│   │   ├── hackernews_scraper.py
│   │   ├── wired_scraper.py
│   │   └── unused/         # Deprecated scrapers
│   │       ├── devto_scraper.py
│   │       ├── producthunt_scraper.py
│   │       └── tiktok_scraper.py
│   ├── core/               # Core functionality
│   │   ├── __init__.py
│   │   ├── newsletter_builder.py  # HTML newsletter generation
│   │   ├── email_sender.py        # SendGrid email sending
│   │   └── summarizer.py          # AI content summarization
│   └── utils/              # Utility functions
│       ├── __init__.py
│       ├── cache_manager.py       # Content caching system
│       ├── retry_handler.py       # API retry logic
│       └── email_cache.py         # Email deduplication
├── scripts/                # Utility scripts
│   ├── force_send.py       # Force send newsletter (bypass cache)
│   └── test_reddit.py      # Reddit scraper testing
└── venv/                   # Virtual environment (not in git)
```

## Module Descriptions

### Main Application
- `main.py`: Orchestrates the entire newsletter generation process

### Scrapers (`src/scrapers/`)
- `youtube_scraper.py`: Fetches trending YouTube videos
- `reddit_scraper.py`: Scrapes multiple subreddits
- `twitter_scraper.py`: X/Twitter trending content
- `github_scraper.py`: GitHub trending repositories
- `hackernews_scraper.py`: Hacker News top stories
- `wired_scraper.py`: Wired.com RSS feeds

### Core (`src/core/`)
- `newsletter_builder.py`: Generates newspaper-style HTML newsletters
- `email_sender.py`: SendGrid integration with caching
- `summarizer.py`: AI-powered content summarization

### Utils (`src/utils/`)
- `cache_manager.py`: Content caching with TTL
- `retry_handler.py`: API rate limiting and retry logic
- `email_cache.py`: Prevents duplicate email sends

### Scripts (`scripts/`)
- `force_send.py`: Utility to bypass email cache
- `test_reddit.py`: Testing script for Reddit scraper

## Usage

### Regular Newsletter Generation
```bash
python main.py
```

### Force Send (Bypass Cache)
```bash
python scripts/force_send.py --recipient user@example.com
```

### Cache Management
```bash
python scripts/force_send.py --stats        # Show cache stats
python scripts/force_send.py --clear-cache  # Clear email cache
```

## Environment Variables

Required in `.env` file:
- `SENDGRID_API_KEY`: SendGrid API key
- `FROM_EMAIL`: Sender email address
- `OPENAI_API_KEY`: OpenAI API key for summarization
- `YOUTUBE_API_KEY`: YouTube Data API key
- `TWITTER_BEARER_TOKEN`: Twitter/X API bearer token
- `GITHUB_TOKEN`: GitHub personal access token (optional)