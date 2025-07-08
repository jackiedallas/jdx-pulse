import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

def fetch_top_posts(subreddit_name="technology", limit=5):
    """Fetch top posts from Reddit using read-only API without authentication"""
    try:
        headers = {
            'User-Agent': 'jdx-pulse/1.0 (https://jdxsoftware.com)'
        }
        
        url = f"https://www.reddit.com/r/{subreddit_name}/hot.json?limit={limit}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            posts = []
            
            for post_data in data['data']['children']:
                post = post_data['data']
                if not post.get('stickied', False):
                    posts.append({
                        "title": post['title'],
                        "url": f"https://reddit.com{post['permalink']}",
                        "score": post['score'],
                        "author": post['author'],
                        "subreddit": post['subreddit'],
                        "created_utc": post['created_utc'],
                        "source": "reddit"
                    })
            
            return posts
        else:
            print(f"Error fetching Reddit posts: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error fetching Reddit posts: {e}")
        return []

def fetch_multiple_subreddits(subreddits=None, limit_per_sub=3):
    """Fetch posts from multiple subreddits"""
    if subreddits is None:
        subreddits = ['technology', 'programming', 'startups', 'webdev', 'MachineLearning']
    
    all_posts = []
    for subreddit in subreddits:
        posts = fetch_top_posts(subreddit, limit_per_sub)
        all_posts.extend(posts)
        time.sleep(1)  # Rate limiting
    
    # Sort by score and return top posts
    all_posts.sort(key=lambda x: x['score'], reverse=True)
    return all_posts[:limit_per_sub * 2]  # Return top posts overall

