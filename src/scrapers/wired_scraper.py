import requests
import xml.etree.ElementTree as ET
import json
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def fetch_wired_rss(limit=5):
    """Fetch latest articles from Wired RSS feed"""
    try:
        headers = {
            'User-Agent': 'jdx-pulse/1.0 (https://jdxsoftware.com)'
        }
        
        # Wired RSS feed URL
        url = "https://www.wired.com/feed/rss"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            articles = []
            
            # Find all item elements
            items = root.findall('.//item')
            
            for item in items[:limit]:
                title = item.find('title').text if item.find('title') is not None else ''
                link = item.find('link').text if item.find('link') is not None else ''
                description = item.find('description').text if item.find('description') is not None else ''
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                
                # Clean up title and description
                title = title.strip()
                if description:
                    # Remove HTML tags from description
                    import re
                    description = re.sub(r'<[^>]+>', '', description).strip()
                
                articles.append({
                    "title": title,
                    "url": link,
                    "score": 100,  # Default score since RSS doesn't provide engagement
                    "source": "wired",
                    "description": description[:200] + "..." if len(description) > 200 else description,
                    "published_date": pub_date
                })
            
            return articles
        else:
            print(f"Error fetching Wired RSS: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error fetching Wired RSS: {e}")
        return []

def fetch_wired_tech_news(limit=5):
    """Fetch tech-specific articles from Wired"""
    try:
        headers = {
            'User-Agent': 'jdx-pulse/1.0 (https://jdxsoftware.com)'
        }
        
        # Wired tech section RSS (using category instead of tag)
        url = "https://www.wired.com/feed/category/gear/rss"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            articles = []
            
            items = root.findall('.//item')
            
            for item in items[:limit]:
                title = item.find('title').text if item.find('title') is not None else ''
                link = item.find('link').text if item.find('link') is not None else ''
                description = item.find('description').text if item.find('description') is not None else ''
                
                # Clean up content
                title = title.strip()
                if description:
                    import re
                    description = re.sub(r'<[^>]+>', '', description).strip()
                
                articles.append({
                    "title": title,
                    "url": link,
                    "score": 150,  # Slightly higher score for tech-focused content
                    "source": "wired",
                    "description": description[:200] + "..." if len(description) > 200 else description,
                    "category": "tech"
                })
            
            return articles
        else:
            print(f"Error fetching Wired tech RSS: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error fetching Wired tech RSS: {e}")
        return []

def fetch_wired_business(limit=3):
    """Fetch business articles from Wired"""
    try:
        headers = {
            'User-Agent': 'jdx-pulse/1.0 (https://jdxsoftware.com)'
        }
        
        # Wired business section RSS
        url = "https://www.wired.com/feed/category/business/rss"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            articles = []
            
            items = root.findall('.//item')
            
            for item in items[:limit]:
                title = item.find('title').text if item.find('title') is not None else ''
                link = item.find('link').text if item.find('link') is not None else ''
                description = item.find('description').text if item.find('description') is not None else ''
                
                title = title.strip()
                if description:
                    import re
                    description = re.sub(r'<[^>]+>', '', description).strip()
                
                articles.append({
                    "title": title,
                    "url": link,
                    "score": 120,
                    "source": "wired",
                    "description": description[:200] + "..." if len(description) > 200 else description,
                    "category": "business"
                })
            
            return articles
        else:
            print(f"Error fetching Wired business RSS: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error fetching Wired business RSS: {e}")
        return []

def fetch_wired_mixed(limit=5):
    """Fetch mixed content from different Wired sections"""
    try:
        # Get articles from different sections
        tech_articles = fetch_wired_tech_news(2)
        business_articles = fetch_wired_business(2)
        general_articles = fetch_wired_rss(2)
        
        # Combine all articles
        all_articles = tech_articles + business_articles + general_articles
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_articles = []
        
        for article in all_articles:
            if article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                unique_articles.append(article)
        
        # Sort by score (tech articles will rank higher)
        unique_articles.sort(key=lambda x: x['score'], reverse=True)
        
        return unique_articles[:limit]
        
    except Exception as e:
        print(f"Error fetching mixed Wired content: {e}")
        return []

def fetch_wired_trending(limit=5):
    """Main function to fetch trending Wired articles"""
    return fetch_wired_mixed(limit)