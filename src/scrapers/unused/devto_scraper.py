import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

def fetch_devto_trending(limit=5):
    """Fetch trending articles from Dev.to using their public API"""
    try:
        headers = {
            'User-Agent': 'jdx-pulse/1.0 (https://jdxsoftware.com)'
        }
        
        # Get top articles from the last week
        url = "https://dev.to/api/articles"
        params = {
            'top': '7',  # Top articles from last 7 days
            'per_page': limit
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            articles = response.json()
            dev_articles = []
            
            for article in articles:
                dev_articles.append({
                    "title": article['title'],
                    "url": article['url'],
                    "score": article.get('public_reactions_count', 0),
                    "source": "devto",
                    "author": article['user']['name'],
                    "tags": article.get('tag_list', []),
                    "published_at": article.get('published_at', ''),
                    "reading_time": article.get('reading_time_minutes', 0)
                })
            
            return dev_articles
        else:
            print(f"Error fetching Dev.to articles: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error fetching Dev.to articles: {e}")
        return []

def fetch_devto_by_tag(tag="javascript", limit=3):
    """Fetch articles by specific tag from Dev.to"""
    try:
        headers = {
            'User-Agent': 'jdx-pulse/1.0 (https://jdxsoftware.com)'
        }
        
        url = "https://dev.to/api/articles"
        params = {
            'tag': tag,
            'top': '7',
            'per_page': limit
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            articles = response.json()
            tagged_articles = []
            
            for article in articles:
                tagged_articles.append({
                    "title": article['title'],
                    "url": article['url'],
                    "score": article.get('public_reactions_count', 0),
                    "source": "devto",
                    "author": article['user']['name'],
                    "tag": tag,
                    "reading_time": article.get('reading_time_minutes', 0)
                })
            
            return tagged_articles
        else:
            print(f"Error fetching Dev.to articles for tag {tag}: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error fetching Dev.to articles for tag {tag}: {e}")
        return []

def fetch_devto_multiple_tags(tags=None, limit_per_tag=2):
    """Fetch articles from multiple popular tech tags"""
    if tags is None:
        tags = ['javascript', 'python', 'react', 'ai', 'webdev', 'startup']
    
    all_articles = []
    
    for tag in tags[:3]:  # Limit to 3 tags to avoid rate limits
        try:
            articles = fetch_devto_by_tag(tag, limit_per_tag)
            all_articles.extend(articles)
            time.sleep(0.5)  # Rate limiting
        except Exception as e:
            print(f"Error fetching Dev.to tag {tag}: {e}")
            continue
    
    # Sort by reactions and return top articles
    all_articles.sort(key=lambda x: x['score'], reverse=True)
    return all_articles[:limit_per_tag * 2]

def fetch_devto_latest(limit=5):
    """Fetch latest articles from Dev.to"""
    try:
        headers = {
            'User-Agent': 'jdx-pulse/1.0 (https://jdxsoftware.com)'
        }
        
        url = "https://dev.to/api/articles/latest"
        params = {
            'per_page': limit
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            articles = response.json()
            latest_articles = []
            
            for article in articles:
                latest_articles.append({
                    "title": article['title'],
                    "url": article['url'],
                    "score": article.get('public_reactions_count', 0),
                    "source": "devto",
                    "author": article['user']['name'],
                    "published_at": article.get('published_at', ''),
                    "reading_time": article.get('reading_time_minutes', 0)
                })
            
            return latest_articles
        else:
            print(f"Error fetching latest Dev.to articles: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error fetching latest Dev.to articles: {e}")
        return []