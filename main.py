from agent.youtube_scraper import fetch_youtube_trending, fetch_youtube_categories
from agent.reddit_scraper import fetch_multiple_subreddits
from agent.twitter_scraper import fetch_twitter_search
from agent.github_scraper import fetch_github_trending
from agent.hackernews_scraper import fetch_hackernews_trending
from agent.wired_scraper import fetch_wired_trending
from agent.summarizer import summarize_text
from agent.newsletter_builder import build_newsletter
from agent.email_sender import send_newsletter
from agent.cache_manager import cached_request
from agent.retry_handler import safe_execute, batch_execute, api_rate_limiter

def fetch_all_content():
    """Fetch content from all sources with error handling and caching"""
    
    # Define fetch functions for each source
    fetch_functions = [
        lambda: cached_request("youtube_trending", lambda: fetch_youtube_trending(max_results=3), ttl=1800),
        lambda: cached_request("reddit_multi", lambda: fetch_multiple_subreddits(limit_per_sub=3), ttl=1800),
        lambda: cached_request("twitter_trending", lambda: fetch_twitter_search("AI OR tech OR startup OR coding", limit=3), ttl=7200),
        lambda: cached_request("github_trending", lambda: fetch_github_trending(limit=3), ttl=3600),
        lambda: cached_request("hackernews_trending", lambda: fetch_hackernews_trending(limit=3), ttl=1800),
        lambda: cached_request("wired_trending", lambda: fetch_wired_trending(limit=3), ttl=3600)
    ]
    
    # Execute all fetch functions with error handling
    results = batch_execute(fetch_functions, continue_on_error=True)
    
    # Flatten and combine all results
    all_content = []
    source_names = ["YouTube", "Reddit", "Twitter", "GitHub", "Hacker News", "Wired"]
    
    for i, result in enumerate(results):
        if result:
            print(f"✓ Fetched {len(result)} items from {source_names[i]}")
            all_content.extend(result)
        else:
            print(f"✗ Failed to fetch from {source_names[i]}")
    
    return all_content

def process_content(content_items):
    """Process and summarize content items"""
    summarized_content = []
    
    for item in content_items:
        # Use rate limiting for AI summarization
        api_rate_limiter.wait_if_needed()
        
        # Create context based on source
        source = item.get('source', 'unknown')
        if source == 'youtube':
            context = f"YouTube Video: {item['title']} | Channel: {item.get('channel', 'Unknown')}"
        elif source == 'reddit':
            context = f"Reddit Post: {item['title']} | r/{item.get('subreddit', 'unknown')}"
        elif source == 'github':
            context = f"GitHub Repository: {item['title']} | Language: {item.get('language', 'Unknown')}"
        elif source == 'hackernews':
            context = f"Hacker News: {item['title']} | Comments: {item.get('comments', 0)}"
        elif source == 'devto':
            context = f"Dev.to Article: {item['title']} | Author: {item.get('author', 'Unknown')}"
        elif source == 'wired':
            context = f"Wired Article: {item['title']} | Description: {item.get('description', '')[:100]}"
        else:
            context = f"{source.title()}: {item['title']}"
        
        # Summarize with error handling
        summary = safe_execute(
            lambda: summarize_text(context),
            fallback_value=item['title'][:100] + "..." if len(item['title']) > 100 else item['title']
        )
        
        # Standardize the data structure
        summarized_content.append({
            "summary": summary,
            "url": item['url'],
            "views": item.get('score', item.get('views', 0)),
            "source": source
        })
    
    # Sort by engagement (views/score) and return top items
    summarized_content.sort(key=lambda x: x['views'], reverse=True)
    return summarized_content[:12]  # Top 12 items for newsletter

if __name__ == "__main__":
    print("🚀 Starting JDX Pulse content aggregation...")
    
    # Fetch content from all sources
    all_content = fetch_all_content()
    print(f"📊 Total items fetched: {len(all_content)}")
    
    if not all_content:
        print("❌ No content fetched. Check your API keys and network connection.")
        exit(1)
    
    # Process and summarize content
    print("🤖 Processing and summarizing content...")
    processed_content = process_content(all_content)
    print(f"📝 Processed {len(processed_content)} items")
    
    # Build the newsletter
    print("📧 Building newsletter...")
    newsletter = build_newsletter(processed_content)
    
    # Print preview (truncated)
    print("📋 Newsletter preview:")
    print("=" * 50)
    preview = newsletter[:500] + "..." if len(newsletter) > 500 else newsletter
    print(preview)
    print("=" * 50)
    
    # Send the newsletter
    print("📤 Sending newsletter...")
    success = send_newsletter(
        subject="📡 JDX Pulse - Today's Top Trends",
        html_content=newsletter,
        recipient_email="jackie.dallas@jdxsoftware.com"
    )
    
    if success:
        print("✅ Newsletter sent successfully!")
    else:
        print("❌ Failed to send newsletter")
