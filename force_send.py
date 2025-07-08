#!/usr/bin/env python3
"""
Force send utility - bypasses email cache to resend newsletter
Usage: python force_send.py [recipient_email]
"""

import sys
from main import fetch_all_content, process_content
from agent.newsletter_builder import build_newsletter
from agent.email_sender import send_newsletter, get_email_cache_stats, clear_email_cache

def force_send_newsletter(recipient_email=None):
    """Force send newsletter bypassing cache"""
    print("🚀 Force sending JDX Pulse newsletter...")
    
    # Use default recipient if none provided
    if not recipient_email:
        recipient_email = "jackie.dallas@jdxsoftware.com"
    
    # Fetch and process content
    print("📊 Fetching content...")
    all_content = fetch_all_content()
    
    if not all_content:
        print("❌ No content fetched. Check your API keys and network connection.")
        return False
    
    print("🤖 Processing content...")
    processed_content = process_content(all_content)
    
    # Build newsletter
    print("📧 Building newsletter...")
    newsletter = build_newsletter(processed_content)
    
    # Force send (bypass cache)
    print(f"📤 Force sending to {recipient_email}...")
    success = send_newsletter(
        subject="📡 JDX Pulse - Today's Top Trends (Force Send)",
        html_content=newsletter,
        recipient_email=recipient_email,
        content_items=processed_content,
        force_send=True  # This bypasses the cache
    )
    
    if success:
        print("✅ Newsletter force sent successfully!")
        return True
    else:
        print("❌ Failed to send newsletter")
        return False

def show_cache_stats():
    """Show email cache statistics"""
    print("📊 Email Cache Statistics:")
    stats = get_email_cache_stats()
    print(f"  Total cached entries: {stats['total_entries']}")
    print(f"  Unique recipients: {stats['unique_recipients']}")
    print(f"  Recent sends (24h): {stats['recent_sends']}")

def clear_cache():
    """Clear email cache"""
    print("🗑️  Clearing email cache...")
    clear_email_cache()
    print("✅ Email cache cleared!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Force send newsletter or manage email cache")
    parser.add_argument("--recipient", "-r", help="Recipient email address")
    parser.add_argument("--stats", "-s", action="store_true", help="Show cache statistics")
    parser.add_argument("--clear-cache", "-c", action="store_true", help="Clear email cache")
    
    args = parser.parse_args()
    
    if args.stats:
        show_cache_stats()
    elif args.clear_cache:
        clear_cache()
    else:
        force_send_newsletter(args.recipient)