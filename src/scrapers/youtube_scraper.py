import os
import requests
import time
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

def fetch_youtube_trending(region_code="US", max_results=5):
    """Fetch trending videos using YouTube API with fallback"""
    try:
        youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))

        request = youtube.videos().list(
            part="snippet,statistics",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=max_results,
        )
        response = request.execute()

        videos = []
        for item in response.get("items", []):
            videos.append({
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={item['id']}",
                "views": int(item["statistics"].get("viewCount", 0)),
                "channel": item["snippet"]["channelTitle"],
                "source": "youtube"
            })

        return videos
    except Exception as e:
        print(f"Error fetching YouTube trending: {e}")
        return fetch_youtube_trending_fallback(max_results)

def fetch_youtube_trending_fallback(max_results=5):
    """Fallback method using web scraping"""
    try:
        # This would use yt-dlp or similar, but for now return empty
        # to avoid adding complex dependencies
        print("Using YouTube fallback method")
        return []
    except Exception as e:
        print(f"Error in YouTube fallback: {e}")
        return []

def fetch_youtube_categories(categories=None, max_per_category=2):
    """Fetch trending videos from multiple categories"""
    if categories is None:
        categories = ["10", "15", "17", "19", "20", "22", "23", "24", "25", "26", "27", "28"]
        # 10=Music, 15=Pets, 17=Sports, 19=Travel, 20=Gaming, 22=People, 23=Comedy, 24=Entertainment, 25=News, 26=Style, 27=Education, 28=Science
    
    all_videos = []
    for category in categories[:3]:  # Limit to first 3 categories to avoid quota
        try:
            youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
            request = youtube.videos().list(
                part="snippet,statistics",
                chart="mostPopular",
                regionCode="US",
                maxResults=max_per_category,
                videoCategoryId=category
            )
            response = request.execute()
            
            for item in response.get("items", []):
                all_videos.append({
                    "title": item["snippet"]["title"],
                    "url": f"https://www.youtube.com/watch?v={item['id']}",
                    "views": int(item["statistics"].get("viewCount", 0)),
                    "channel": item["snippet"]["channelTitle"],
                    "category": category,
                    "source": "youtube"
                })
            
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"Error fetching category {category}: {e}")
            continue
    
    # Sort by views and return top videos
    all_videos.sort(key=lambda x: x['views'], reverse=True)
    return all_videos[:max_per_category * 2]
