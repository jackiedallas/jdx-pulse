import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

def fetch_hackernews_top(limit=10):
    """Fetch top stories from Hacker News"""
    try:
        # Get top story IDs
        top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(top_stories_url)
        
        if response.status_code == 200:
            story_ids = response.json()[:limit]
            stories = []
            
            for story_id in story_ids:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_response = requests.get(story_url)
                
                if story_response.status_code == 200:
                    story_data = story_response.json()
                    if story_data and story_data.get('type') == 'story':
                        stories.append({
                            "title": story_data.get('title', ''),
                            "url": story_data.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                            "score": story_data.get('score', 0),
                            "source": "hackernews",
                            "comments": story_data.get('descendants', 0),
                            "author": story_data.get('by', ''),
                            "time": story_data.get('time', 0)
                        })
                
                time.sleep(0.1)  # Rate limiting
            
            return stories
        else:
            print(f"Error fetching Hacker News top stories: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error fetching Hacker News stories: {e}")
        return []

def fetch_hackernews_best(limit=10):
    """Fetch best stories from Hacker News"""
    try:
        # Get best story IDs
        best_stories_url = "https://hacker-news.firebaseio.com/v0/beststories.json"
        response = requests.get(best_stories_url)
        
        if response.status_code == 200:
            story_ids = response.json()[:limit]
            stories = []
            
            for story_id in story_ids:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_response = requests.get(story_url)
                
                if story_response.status_code == 200:
                    story_data = story_response.json()
                    if story_data and story_data.get('type') == 'story':
                        stories.append({
                            "title": story_data.get('title', ''),
                            "url": story_data.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                            "score": story_data.get('score', 0),
                            "source": "hackernews",
                            "comments": story_data.get('descendants', 0),
                            "author": story_data.get('by', ''),
                            "time": story_data.get('time', 0)
                        })
                
                time.sleep(0.1)  # Rate limiting
            
            return stories
        else:
            print(f"Error fetching Hacker News best stories: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error fetching Hacker News best stories: {e}")
        return []

def fetch_hackernews_new(limit=10):
    """Fetch new stories from Hacker News"""
    try:
        # Get new story IDs
        new_stories_url = "https://hacker-news.firebaseio.com/v0/newstories.json"
        response = requests.get(new_stories_url)
        
        if response.status_code == 200:
            story_ids = response.json()[:limit]
            stories = []
            
            for story_id in story_ids:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_response = requests.get(story_url)
                
                if story_response.status_code == 200:
                    story_data = story_response.json()
                    if story_data and story_data.get('type') == 'story':
                        stories.append({
                            "title": story_data.get('title', ''),
                            "url": story_data.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                            "score": story_data.get('score', 0),
                            "source": "hackernews",
                            "comments": story_data.get('descendants', 0),
                            "author": story_data.get('by', ''),
                            "time": story_data.get('time', 0)
                        })
                
                time.sleep(0.1)  # Rate limiting
            
            return stories
        else:
            print(f"Error fetching Hacker News new stories: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error fetching Hacker News new stories: {e}")
        return []

def fetch_hackernews_trending(limit=5):
    """Fetch trending stories (combination of top and best with high engagement)"""
    try:
        # Get both top and best stories
        top_stories = fetch_hackernews_top(20)
        best_stories = fetch_hackernews_best(20)
        
        # Combine and deduplicate
        all_stories = []
        seen_titles = set()
        
        for story in top_stories + best_stories:
            if story['title'] not in seen_titles:
                seen_titles.add(story['title'])
                all_stories.append(story)
        
        # Sort by a combination of score and comments for "trending"
        all_stories.sort(key=lambda x: (x['score'] + x['comments'] * 2), reverse=True)
        
        return all_stories[:limit]
        
    except Exception as e:
        print(f"Error fetching Hacker News trending: {e}")
        return []