import requests
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

def fetch_twitter_trending(limit=5):
    """Fetch trending topics from Twitter/X using API v2"""
    try:
        bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        if not bearer_token:
            print("Twitter Bearer Token not found, using placeholder data")
            return _get_placeholder_trending(limit)
        
        headers = {
            'Authorization': f'Bearer {bearer_token}',
            'User-Agent': 'jdx-pulse/1.0'
        }
        
        # Get trending topics for a specific location (US = 23424977)
        url = "https://api.twitter.com/1.1/trends/place.json?id=23424977"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            trends = []
            
            if data and len(data) > 0 and 'trends' in data[0]:
                for trend in data[0]['trends'][:limit]:
                    trends.append({
                        "title": trend['name'],
                        "url": trend.get('url', f"https://twitter.com/search?q={trend['name'].replace('#', '%23')}"),
                        "score": trend.get('tweet_volume', 0) or 10000,  # Default if no volume
                        "source": "twitter"
                    })
            
            return trends if trends else _get_placeholder_trending(limit)
        else:
            print(f"Twitter API error: {response.status_code} - {response.text}")
            return _get_placeholder_trending(limit)
        
    except Exception as e:
        print(f"Error fetching Twitter trends: {e}")
        return _get_placeholder_trending(limit)

def _get_placeholder_trending(limit):
    """Fallback placeholder data"""
    trending_topics = [
        {"title": "AI Revolution", "url": "https://twitter.com/search?q=AI", "score": 50000, "source": "twitter"},
        {"title": "Web3 Development", "url": "https://twitter.com/search?q=Web3", "score": 35000, "source": "twitter"},
        {"title": "Startup Funding", "url": "https://twitter.com/search?q=startup", "score": 25000, "source": "twitter"},
        {"title": "Remote Work", "url": "https://twitter.com/search?q=remote", "score": 20000, "source": "twitter"},
        {"title": "Tech News", "url": "https://twitter.com/search?q=tech", "score": 15000, "source": "twitter"}
    ]
    return trending_topics[:limit]

def fetch_twitter_search(query="AI OR tech OR startup", limit=5):
    """Search for trending tweets on specific topics with rate limit handling"""
    try:
        bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        if not bearer_token:
            print("Twitter Bearer Token not found, using placeholder data")
            return _get_placeholder_search(limit)
        
        headers = {
            'Authorization': f'Bearer {bearer_token}',
            'User-Agent': 'jdx-pulse/1.0'
        }
        
        # Use Twitter API v2 search endpoint
        url = "https://api.twitter.com/2/tweets/search/recent"
        params = {
            'query': f'{query} -is:retweet lang:en',
            'max_results': max(10, min(limit * 3, 100)),  # Get more to filter better
            'tweet.fields': 'public_metrics,created_at,author_id',
            'expansions': 'author_id',
            'user.fields': 'username,name'
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            tweets = []
            
            if 'data' in data:
                users = {user['id']: user for user in data.get('includes', {}).get('users', [])}
                
                for tweet in data['data']:
                    author_id = tweet.get('author_id')
                    author_info = users.get(author_id, {})
                    
                    # Clean up tweet text
                    tweet_text = tweet['text'].replace('\n', ' ').strip()
                    if len(tweet_text) > 100:
                        tweet_text = tweet_text[:97] + "..."
                    
                    tweets.append({
                        "title": tweet_text,
                        "url": f"https://twitter.com/{author_info.get('username', 'user')}/status/{tweet['id']}",
                        "score": tweet.get('public_metrics', {}).get('retweet_count', 0) + 
                                tweet.get('public_metrics', {}).get('like_count', 0),
                        "source": "twitter",
                        "author": author_info.get('name', 'Unknown')
                    })
            
            # Sort by engagement and return only the requested limit
            tweets.sort(key=lambda x: x['score'], reverse=True)
            return tweets[:limit] if tweets else _get_placeholder_search(limit)
            
        elif response.status_code == 429:
            print("Twitter API rate limit exceeded - using placeholder data")
            return _get_placeholder_search(limit)
        elif response.status_code == 401:
            print("Twitter API authentication failed - check your Bearer Token")
            return _get_placeholder_search(limit)
        else:
            print(f"Twitter search API error: {response.status_code} - {response.text[:200]}")
            return _get_placeholder_search(limit)
        
    except Exception as e:
        print(f"Error fetching Twitter search: {e}")
        return _get_placeholder_search(limit)

def _get_placeholder_search(limit):
    """Fallback placeholder search data"""
    tech_posts = [
        {
            "title": "The future of AI is here - breakthrough in neural networks",
            "url": "https://twitter.com/example/status/123",
            "score": 25000,
            "source": "twitter",
            "author": "Tech Leader"
        },
        {
            "title": "New programming language revolutionizes web development",
            "url": "https://twitter.com/example/status/124",
            "score": 18000,
            "source": "twitter",
            "author": "Developer"
        },
        {
            "title": "Startup raised $50M in Series A funding",
            "url": "https://twitter.com/example/status/125",
            "score": 12000,
            "source": "twitter",
            "author": "Investor"
        }
    ]
    return tech_posts[:limit]