import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

def fetch_github_trending(language="", period="daily", limit=5):
    """Fetch trending GitHub repositories"""
    try:
        # GitHub provides trending data through their web interface
        # We'll use the GitHub API to get popular repos
        
        headers = {
            'User-Agent': 'jdx-pulse/1.0 (https://jdxsoftware.com)',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Use search API to find trending repos
        query = f"stars:>1 created:>{_get_date_filter(period)}"
        if language:
            query += f" language:{language}"
        
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={limit}"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            repos = []
            
            for repo in data.get('items', []):
                repos.append({
                    "title": f"{repo['name']} - {repo['description'][:100]}..." if repo['description'] else repo['name'],
                    "url": repo['html_url'],
                    "score": repo['stargazers_count'],
                    "source": "github",
                    "language": repo.get('language', 'Unknown'),
                    "stars": repo['stargazers_count'],
                    "forks": repo['forks_count']
                })
            
            return repos
        else:
            print(f"Error fetching GitHub trending: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error fetching GitHub trending: {e}")
        return []

def _get_date_filter(period):
    """Get date filter for GitHub API based on period"""
    from datetime import datetime, timedelta
    
    if period == "daily":
        date = datetime.now() - timedelta(days=1)
    elif period == "weekly":
        date = datetime.now() - timedelta(weeks=1)
    elif period == "monthly":
        date = datetime.now() - timedelta(days=30)
    else:
        date = datetime.now() - timedelta(days=1)
    
    return date.strftime("%Y-%m-%d")

def fetch_github_topics(topics=None, limit=3):
    """Fetch trending repos by topics"""
    if topics is None:
        topics = ["javascript", "python", "react", "ai", "machine-learning", "web-development"]
    
    all_repos = []
    
    for topic in topics[:3]:  # Limit to avoid rate limits
        try:
            headers = {
                'User-Agent': 'jdx-pulse/1.0 (https://jdxsoftware.com)',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            url = f"https://api.github.com/search/repositories?q=topic:{topic}&sort=stars&order=desc&per_page=2"
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                for repo in data.get('items', []):
                    all_repos.append({
                        "title": f"{repo['name']} - {repo['description'][:100]}..." if repo['description'] else repo['name'],
                        "url": repo['html_url'],
                        "score": repo['stargazers_count'],
                        "source": "github",
                        "topic": topic,
                        "language": repo.get('language', 'Unknown'),
                        "stars": repo['stargazers_count']
                    })
                
                time.sleep(1)  # Rate limiting
            
        except Exception as e:
            print(f"Error fetching GitHub topic {topic}: {e}")
            continue
    
    # Sort by stars and return top repos
    all_repos.sort(key=lambda x: x['stars'], reverse=True)
    return all_repos[:limit]

def fetch_github_developers(limit=5):
    """Fetch trending developers (based on recent popular repos)"""
    try:
        headers = {
            'User-Agent': 'jdx-pulse/1.0 (https://jdxsoftware.com)',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Get repos from the last week
        query = f"stars:>50 created:>{_get_date_filter('weekly')}"
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={limit}"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            developers = []
            
            for repo in data.get('items', []):
                developers.append({
                    "title": f"{repo['owner']['login']} created {repo['name']}",
                    "url": repo['owner']['html_url'],
                    "score": repo['stargazers_count'],
                    "source": "github",
                    "developer": repo['owner']['login'],
                    "repo_name": repo['name'],
                    "stars": repo['stargazers_count']
                })
            
            return developers
        else:
            print(f"Error fetching GitHub developers: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error fetching GitHub developers: {e}")
        return []