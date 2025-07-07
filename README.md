# 📡 JDX Pulse

**JDX Pulse** is an AI-powered agent that curates the internet’s top trends from Reddit, YouTube, and other platforms, summarizing them into a clean, daily newsletter.

---

## 🔧 Features

- ✅ Pulls trending Reddit posts and YouTube videos
- ✅ Summarizes posts using OpenAI GPT-4 Turbo
- ✅ Builds a clean, readable daily newsletter
- ✅ Sends emails via MailerSend
- ✅ Runs on a daily schedule (Railway or other cron-based platforms)

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/jdx-pulse.git
cd jdx-pulse
```

## Project Structure

jdx-pulse/
├── agent/                   # Core logic for scrapers, summarizers, email
│   ├── __init__.py
│   ├── reddit_scraper.py    # Pulls trending Reddit posts
│   ├── youtube_scraper.py   # Pulls trending YouTube videos
│   ├── summarizer.py        # OpenAI summarization logic
│   ├── newsletter_builder.py# Builds the text/HTML body for email
│   ├── email_sender.py      # Sends emails via MailerSend
├── main.py                   # The main runner script (entry point)
├── .env                      # Your local environment variables (keep secret)
├── .env.example              # Example env file for reference
├── requirements.txt          # Python package dependencies
├── README.md
└── .gitignore                # Ignore env files, __pycache__, etc.
