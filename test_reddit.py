from agent.reddit_scraper import fetch_top_posts

try:
    posts = fetch_top_posts(subreddit_name="technology", limit=3)
    print(f"Found {len(posts)} posts:")
    for post in posts:
        print(f"- {post['title']} (Score: {post['score']})")
        print(f"  {post['url']}")
        print()
except Exception as e:
    print("Error:", e)
