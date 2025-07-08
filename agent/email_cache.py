import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class EmailCache:
    def __init__(self, cache_dir="cache"):
        self.cache_dir = cache_dir
        self.cache_file = os.path.join(cache_dir, "email_cache.json")
        self.ensure_cache_dir()
        
    def ensure_cache_dir(self):
        """Ensure cache directory exists"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def _generate_content_hash(self, content_items: List[Dict]) -> str:
        """Generate hash from content items (excluding styling/formatting)"""
        # Extract only the core content that matters for uniqueness
        core_content = []
        for item in content_items:
            core_item = {
                'title': item.get('summary', ''),
                'url': item.get('url', ''),
                'source': item.get('source', ''),
                'views': item.get('views', 0)
            }
            core_content.append(core_item)
        
        # Sort by URL to ensure consistent ordering
        core_content.sort(key=lambda x: x['url'])
        
        # Create hash from the core content
        content_str = json.dumps(core_content, sort_keys=True)
        return hashlib.md5(content_str.encode()).hexdigest()
    
    def _load_cache(self) -> Dict:
        """Load existing cache data"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def _save_cache(self, cache_data: Dict):
        """Save cache data to file"""
        with open(self.cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
    
    def should_send_email(self, content_items: List[Dict], recipient: str, force_send: bool = False) -> bool:
        """Check if email should be sent based on content uniqueness"""
        if force_send:
            return True
            
        content_hash = self._generate_content_hash(content_items)
        cache_data = self._load_cache()
        
        # Create unique key for this recipient
        cache_key = f"{recipient}:{content_hash}"
        
        # Check if we've sent this exact content before
        if cache_key in cache_data:
            last_sent = datetime.fromisoformat(cache_data[cache_key]['sent_at'])
            
            # Don't resend same content within 24 hours
            if datetime.now() - last_sent < timedelta(hours=24):
                print(f"📧 Skipping email to {recipient} - same content sent recently")
                return False
        
        return True
    
    def mark_email_sent(self, content_items: List[Dict], recipient: str, success: bool = True):
        """Mark email as sent in cache"""
        if not success:
            return
            
        content_hash = self._generate_content_hash(content_items)
        cache_data = self._load_cache()
        
        cache_key = f"{recipient}:{content_hash}"
        cache_data[cache_key] = {
            'sent_at': datetime.now().isoformat(),
            'content_hash': content_hash,
            'recipient': recipient,
            'item_count': len(content_items)
        }
        
        # Clean up old entries (older than 7 days)
        self._cleanup_old_entries(cache_data)
        
        self._save_cache(cache_data)
        print(f"📧 Email cache updated for {recipient}")
    
    def _cleanup_old_entries(self, cache_data: Dict):
        """Remove cache entries older than 7 days"""
        cutoff_date = datetime.now() - timedelta(days=7)
        keys_to_remove = []
        
        for key, data in cache_data.items():
            try:
                sent_date = datetime.fromisoformat(data['sent_at'])
                if sent_date < cutoff_date:
                    keys_to_remove.append(key)
            except (ValueError, KeyError):
                # Remove malformed entries
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del cache_data[key]
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        cache_data = self._load_cache()
        
        stats = {
            'total_entries': len(cache_data),
            'unique_recipients': len(set(data['recipient'] for data in cache_data.values())),
            'recent_sends': 0
        }
        
        # Count recent sends (last 24 hours)
        cutoff = datetime.now() - timedelta(hours=24)
        for data in cache_data.values():
            try:
                sent_date = datetime.fromisoformat(data['sent_at'])
                if sent_date > cutoff:
                    stats['recent_sends'] += 1
            except (ValueError, KeyError):
                pass
        
        return stats
    
    def clear_cache(self):
        """Clear all cache entries"""
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        print("📧 Email cache cleared")
    
    def get_last_sent_info(self, recipient: str) -> Optional[Dict]:
        """Get info about last email sent to recipient"""
        cache_data = self._load_cache()
        
        # Find most recent entry for this recipient
        recipient_entries = [
            (key, data) for key, data in cache_data.items() 
            if data.get('recipient') == recipient
        ]
        
        if not recipient_entries:
            return None
        
        # Sort by sent date and get most recent
        recipient_entries.sort(key=lambda x: x[1]['sent_at'], reverse=True)
        
        return recipient_entries[0][1]