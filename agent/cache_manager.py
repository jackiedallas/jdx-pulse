import json
import os
import time
from datetime import datetime, timedelta
import hashlib

class CacheManager:
    def __init__(self, cache_dir="cache", default_ttl=3600):
        """
        Initialize cache manager
        
        Args:
            cache_dir: Directory to store cache files
            default_ttl: Default time-to-live in seconds (1 hour default)
        """
        self.cache_dir = cache_dir
        self.default_ttl = default_ttl
        
        # Create cache directory if it doesn't exist
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def _get_cache_key(self, key):
        """Generate a safe filename from cache key"""
        return hashlib.md5(key.encode()).hexdigest()
    
    def _get_cache_path(self, key):
        """Get full path to cache file"""
        cache_key = self._get_cache_key(key)
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def get(self, key):
        """
        Get value from cache
        
        Args:
            key: Cache key string
            
        Returns:
            Cached value or None if not found/expired
        """
        try:
            cache_path = self._get_cache_path(key)
            
            if not os.path.exists(cache_path):
                return None
            
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
            
            # Check if cache is expired
            if time.time() > cache_data['expires_at']:
                os.remove(cache_path)
                return None
            
            return cache_data['data']
            
        except Exception as e:
            print(f"Error reading cache for key {key}: {e}")
            return None
    
    def set(self, key, value, ttl=None):
        """
        Set value in cache
        
        Args:
            key: Cache key string
            value: Value to cache (must be JSON serializable)
            ttl: Time-to-live in seconds (uses default if None)
        """
        try:
            cache_path = self._get_cache_path(key)
            ttl = ttl or self.default_ttl
            
            cache_data = {
                'data': value,
                'created_at': time.time(),
                'expires_at': time.time() + ttl,
                'key': key
            }
            
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f, indent=2)
                
        except Exception as e:
            print(f"Error writing cache for key {key}: {e}")
    
    def delete(self, key):
        """Delete specific cache entry"""
        try:
            cache_path = self._get_cache_path(key)
            if os.path.exists(cache_path):
                os.remove(cache_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting cache for key {key}: {e}")
            return False
    
    def clear_expired(self):
        """Clear all expired cache entries"""
        try:
            cleared_count = 0
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.cache_dir, filename)
                    try:
                        with open(filepath, 'r') as f:
                            cache_data = json.load(f)
                        
                        if time.time() > cache_data['expires_at']:
                            os.remove(filepath)
                            cleared_count += 1
                    except:
                        # If we can't read the file, delete it
                        os.remove(filepath)
                        cleared_count += 1
            
            print(f"Cleared {cleared_count} expired cache entries")
            return cleared_count
            
        except Exception as e:
            print(f"Error clearing expired cache: {e}")
            return 0
    
    def clear_all(self):
        """Clear all cache entries"""
        try:
            cleared_count = 0
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.cache_dir, filename)
                    os.remove(filepath)
                    cleared_count += 1
            
            print(f"Cleared {cleared_count} cache entries")
            return cleared_count
            
        except Exception as e:
            print(f"Error clearing all cache: {e}")
            return 0
    
    def get_cache_info(self):
        """Get information about cache status"""
        try:
            total_files = 0
            total_size = 0
            expired_files = 0
            
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.cache_dir, filename)
                    total_files += 1
                    total_size += os.path.getsize(filepath)
                    
                    try:
                        with open(filepath, 'r') as f:
                            cache_data = json.load(f)
                        
                        if time.time() > cache_data['expires_at']:
                            expired_files += 1
                    except:
                        expired_files += 1
            
            return {
                'total_files': total_files,
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'expired_files': expired_files,
                'active_files': total_files - expired_files
            }
            
        except Exception as e:
            print(f"Error getting cache info: {e}")
            return {}

# Global cache instance
cache = CacheManager()

def cached_request(key, fetch_function, ttl=3600):
    """
    Decorator-like function for caching API requests
    
    Args:
        key: Unique cache key
        fetch_function: Function that fetches the data
        ttl: Time-to-live in seconds
        
    Returns:
        Cached data or fresh data from fetch_function
    """
    # Try to get from cache first
    cached_data = cache.get(key)
    if cached_data is not None:
        print(f"Cache hit for key: {key}")
        return cached_data
    
    # Cache miss - fetch fresh data
    print(f"Cache miss for key: {key}")
    try:
        fresh_data = fetch_function()
        cache.set(key, fresh_data, ttl)
        return fresh_data
    except Exception as e:
        print(f"Error fetching fresh data for key {key}: {e}")
        return []