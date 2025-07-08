import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To
from dotenv import load_dotenv
from ..utils.email_cache import EmailCache
from datetime import datetime

load_dotenv()

def send_newsletter_to_contact_list(subject, html_content=None, content_items=None, force_send=False, list_id=None):
    """Send newsletter to SendGrid contact list"""
    
    # Get contact list ID from environment or parameter
    contact_list_id = list_id or os.getenv("SENDGRID_CONTACT_LIST_ID")
    
    if not contact_list_id:
        print("❌ No SendGrid contact list ID found. Set SENDGRID_CONTACT_LIST_ID in your .env file")
        return False
    
    # Build email content if content_items provided
    if content_items:
        print("📧 Building email-optimized newsletter...")
        html_content = build_email_newsletter(content_items, title="JDX PULSE")
    
    if not html_content:
        print("❌ No HTML content to send")
        return False
    
    try:
        sg = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
        
        # Create the email with contact list
        message = Mail(
            from_email="pulse@jdxsoftware.com",
            subject=subject,
            html_content=html_content
        )
        
        # Add the contact list as recipients
        message.add_to(To(email="list-placeholder@example.com"))  # This gets replaced by SendGrid
        
        # Add custom args to track the send
        message.custom_arg = {
            "newsletter": "jdx-pulse",
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        # Send to contact list
        response = sg.send(message, contact_list_ids=[contact_list_id])
        print(f"✅ Newsletter sent to contact list! Status code: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error sending to contact list: {e}")
        return False

def get_contact_lists():
    """Get all your SendGrid contact lists"""
    try:
        sg = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
        
        response = sg.client.marketing.lists.get()
        
        if response.status_code == 200:
            lists = response.body.get('result', [])
            
            print("📋 Your SendGrid Contact Lists:")
            for contact_list in lists:
                print(f"   • {contact_list['name']} (ID: {contact_list['id']}) - {contact_list['contact_count']} contacts")
            
            return lists
        else:
            print(f"❌ Error fetching contact lists: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error fetching contact lists: {e}")
        return []

def add_contact_to_list(email, first_name=None, last_name=None, list_id=None):
    """Add a contact to your SendGrid list"""
    
    contact_list_id = list_id or os.getenv("SENDGRID_CONTACT_LIST_ID")
    
    if not contact_list_id:
        print("❌ No contact list ID provided")
        return False
    
    try:
        sg = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
        
        # Prepare contact data
        contact_data = {
            "list_ids": [contact_list_id],
            "contacts": [
                {
                    "email": email,
                    "first_name": first_name or "",
                    "last_name": last_name or ""
                }
            ]
        }
        
        response = sg.client.marketing.contacts.put(request_body=contact_data)
        
        if response.status_code == 202:
            print(f"✅ Added {email} to contact list")
            return True
        else:
            print(f"❌ Error adding contact: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error adding contact: {e}")
        return False

def get_contact_list_stats(list_id=None):
    """Get stats for a specific contact list"""
    
    contact_list_id = list_id or os.getenv("SENDGRID_CONTACT_LIST_ID")
    
    if not contact_list_id:
        print("❌ No contact list ID provided")
        return None
    
    try:
        sg = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
        
        # Get list details
        response = sg.client.marketing.lists._(contact_list_id).get()
        
        if response.status_code == 200:
            list_data = response.body
            
            stats = {
                "name": list_data.get("name"),
                "contact_count": list_data.get("contact_count"),
                "created_at": list_data.get("created_at"),
                "updated_at": list_data.get("updated_at")
            }
            
            print(f"📊 List Stats for '{stats['name']}':")
            print(f"   • Contacts: {stats['contact_count']}")
            print(f"   • Created: {stats['created_at']}")
            print(f"   • Updated: {stats['updated_at']}")
            
            return stats
        else:
            print(f"❌ Error fetching list stats: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error fetching list stats: {e}")
        return None

def send_newsletter(subject, html_content, recipient_email=None, content_items=None, force_send=False, use_contact_list=False):
    """Send newsletter with option to use contact list or single recipient"""
    
    # If using contact list, delegate to contact list function
    if use_contact_list:
        return send_newsletter_to_contact_list(subject, html_content, content_items, force_send)
    
    # Original single recipient logic
    if not recipient_email:
        print("❌ No recipient email provided and contact list not enabled")
        return False
    
    # Initialize email cache
    email_cache = EmailCache()
    
    # Check if we should send this email
    if content_items and not email_cache.should_send_email(content_items, recipient_email, force_send):
        return True  # Return True since we "successfully" avoided sending a duplicate
    
    # If content_items provided, build the email-optimized newsletter instead of using html_content
    if content_items:
        print("📧 Building email-optimized newsletter...")
        html_content = build_email_newsletter(content_items, title="JDX PULSE")
    
    message = Mail(
        from_email="pulse@jdxsoftware.com",
        to_emails=recipient_email,
        subject=subject,
        html_content=html_content
    )
    
    try:
        sg = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"Email sent successfully! Status code: {response.status_code}")
        
        # Mark email as sent in cache
        if content_items:
            email_cache.mark_email_sent(content_items, recipient_email, success=True)
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        
        # Mark as failed in cache
        if content_items:
            email_cache.mark_email_sent(content_items, recipient_email, success=False)
        
        return False

def build_email_newsletter(summaries, title="JDX PULSE"):
    """Build email-optimized newsletter HTML"""
    
    # Ensure title is always JDX PULSE
    title = "JDX PULSE"
    
    # Sort content by engagement and separate main story
    sorted_content = sorted(summaries, key=lambda x: x.get('views', 0), reverse=True)
    main_story = sorted_content[0] if sorted_content else None
    other_stories = sorted_content[1:6] if len(sorted_content) > 1 else []
    trending_items = sorted_content[6:11] if len(sorted_content) > 6 else sorted_content[1:6]
    
    # Calculate stats
    total_engagement = sum(item.get('views', 0) for item in summaries)
    total_platforms = len(set(item.get('source', 'unknown') for item in summaries))
    
    # Format engagement for display
    if total_engagement >= 1000000:
        engagement_display = f"{total_engagement/1000000:.1f}M"
    elif total_engagement >= 1000:
        engagement_display = f"{total_engagement/1000:.0f}K"
    else:
        engagement_display = str(total_engagement)
    
    # Get today's date info
    today = datetime.now()
    date_str = today.strftime("%A, %B %d, %Y")
    edition_num = today.timetuple().tm_yday
    current_year = today.year
    
    # Build main story content
    main_story_html = ""
    headlines_html = ""
    
    if main_story:
        # Use a static, newspaper-style main headline
        main_headline = "Today's Top Tech Stories Break the Internet"
        source = main_story.get('source', 'unknown')
        views = main_story.get('views', 0)
        
        # Create a proper subheadline based on the top story
        if source == 'youtube' and views > 10000000:
            subheadline = f"Viral content reaches {views/1000000:.1f}M views as digital trends reshape entertainment"
        elif source == 'reddit' and views > 5000:
            subheadline = f"Community discussion with {views:,} upvotes sparks tech industry debate"
        elif source == 'hackernews' and views > 500:
            subheadline = f"Developer community analyzes trending topics with {views:,} points"
        elif source == 'github' and views > 100:
            subheadline = f"Open source project gains {views:,} stars from global developer community"
        else:
            subheadline = "Breaking developments in technology, social media, and digital innovation"
        
        source_emoji = _get_source_emoji(source)
        action_text = _get_action_text(source)
        section_label = _get_section_name(source)
        section_color = _get_section_color(source)
        
        headlines_html = f"""
        <tr>
            <td style="padding: 30px 40px; border-bottom: 2px solid #2c2c2c;">
                <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                    <tr>
                        <td align="center">
                            <div style="background: #ff4444; color: white; padding: 8px 16px; font-size: 14px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; display: inline-block; margin-bottom: 16px;">🔥 BREAKING</div>
                            <h2 style="font-size: 42px; font-weight: bold; line-height: 1.2; text-align: center; margin: 0 0 16px 0; color: #1a1a1a; border-bottom: 3px solid #ff4444; padding-bottom: 16px;">{main_headline}</h2>
                            <p style="font-size: 24px; font-weight: normal; text-align: center; color: #444; margin: 0; font-style: italic;">{subheadline}</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        """
        
        # Build media content - YouTube gets thumbnail, others get button
        if source == 'youtube':
            media_content = _build_youtube_thumbnail_email(main_story['url'], main_story['summary'])
        else:
            media_content = f'<a href="{main_story["url"]}" style="display: inline-block; background: #2c2c2c; color: white; padding: 8px 16px; text-decoration: none; font-size: 14px; font-weight: bold; border: 2px solid #2c2c2c;">{action_text}</a>'
        
        main_story_html = f"""
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #eee;">
            <tr>
                <td>
                    <div style="background: {section_color}; color: white; padding: 4px 8px; font-size: 12px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; display: inline-block; margin-bottom: 8px;">{section_label}</div>
                    <h3 style="font-size: 20px; font-weight: bold; line-height: 1.3; margin: 0 0 8px 0; color: #1a1a1a;">{main_story['summary'][:100]}{'...' if len(main_story['summary']) > 100 else ''}</h3>
                    <div style="font-size: 12px; color: #888; margin-bottom: 12px; border-left: 3px solid #ccc; padding-left: 12px;">
                        {source_emoji} {source.title()} • {_format_engagement(views, source)}
                    </div>
                    {media_content}
                </td>
            </tr>
        </table>
        """
    else:
        headlines_html = f"""
        <tr>
            <td style="padding: 30px 40px; border-bottom: 2px solid #2c2c2c;">
                <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                    <tr>
                        <td align="center">
                            <div style="background: #ff4444; color: white; padding: 8px 16px; font-size: 14px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; display: inline-block; margin-bottom: 16px;">📰 NEWS</div>
                            <h2 style="font-size: 42px; font-weight: bold; line-height: 1.2; text-align: center; margin: 0 0 16px 0; color: #1a1a1a; border-bottom: 3px solid #ff4444; padding-bottom: 16px;">Today's Tech Roundup</h2>
                            <p style="font-size: 24px; font-weight: normal; text-align: center; color: #444; margin: 0; font-style: italic;">The latest trends and discussions from across the web</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        """
    
    # Build other stories
    other_stories_html = ""
    if other_stories:
        for story in other_stories:
            source = story.get('source', 'unknown')
            views = story.get('views', 0)
            views_text = _format_engagement(views, source)
            source_emoji = _get_source_emoji(source)
            action_text = _get_action_text(source)
            section_label = _get_section_name(source)
            section_color = _get_section_color(source)
            title = story['summary'][:80] + ('...' if len(story['summary']) > 80 else '')
            
            # Build media content - YouTube gets thumbnail, others get button
            if source == 'youtube':
                media_content = _build_youtube_thumbnail_email(story['url'], story['summary'])
            else:
                media_content = f'<a href="{story["url"]}" style="display: inline-block; background: #2c2c2c; color: white; padding: 8px 16px; text-decoration: none; font-size: 14px; font-weight: bold; border: 2px solid #2c2c2c;">{action_text}</a>'
            
            other_stories_html += f"""
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #eee;">
                <tr>
                    <td>
                        <div style="background: {section_color}; color: white; padding: 4px 8px; font-size: 12px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; display: inline-block; margin-bottom: 8px;">{section_label}</div>
                        <h3 style="font-size: 20px; font-weight: bold; line-height: 1.3; margin: 0 0 8px 0; color: #1a1a1a;">{title}</h3>
                        <div style="font-size: 12px; color: #888; margin-bottom: 12px; border-left: 3px solid #ccc; padding-left: 12px;">
                            {source_emoji} {source.title()} • {views_text}
                        </div>
                        {media_content}
                    </td>
                </tr>
            </table>
            """
    else:
        other_stories_html = f"""
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 30px; padding-bottom: 20px;">
            <tr>
                <td>
                    <div style="background: #2c2c2c; color: white; padding: 4px 8px; font-size: 12px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; display: inline-block; margin-bottom: 8px;">NEWS</div>
                    <h3 style="font-size: 20px; font-weight: bold; line-height: 1.3; margin: 0 0 8px 0; color: #1a1a1a;">No Stories Available</h3>
                    <div style="font-size: 12px; color: #888; margin-bottom: 12px; border-left: 3px solid #ccc; padding-left: 12px;">
                        📄 System • Check back tomorrow for fresh content
                    </div>
                </td>
            </tr>
        </table>
        """
    
    # Build trending sidebar
    trending_html = ""
    if trending_items:
        trending_content = ""
        for i, item in enumerate(trending_items[:5], 1):
            source = item.get('source', 'unknown')
            title = item['summary']  # Use full title instead of truncated
            url = item.get('url', '#')
            
            trending_content += f"""
            <div style="margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px dotted #ccc;">
                <span style="font-weight: bold; color: #ff4444; margin-right: 8px;">{i}.</span>
                <div style="font-size: 14px; line-height: 1.4;">
                    <a href="{url}" style="color: #2c2c2c; text-decoration: none;">{title}</a>
                </div>
                <div style="font-size: 11px; color: #888; text-transform: uppercase; margin-top: 4px;">{source.title()}</div>
            </div>
            """
        
        trending_html = f"""
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background: #f8f8f8; border: 1px solid #ddd;">
            <tr>
                <td style="padding: 20px;">
                    <h4 style="font-size: 18px; font-weight: bold; margin: 0 0 16px 0; text-transform: uppercase; letter-spacing: 1px; border-bottom: 2px solid #2c2c2c; padding-bottom: 8px; color: #2c2c2c;">Trending Now</h4>
                    {trending_content}
                </td>
            </tr>
        </table>
        """
    
    # Build complete HTML
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Daily Tech Tribune</title>
    <!--[if mso]>
    <noscript>
        <xml>
            <o:OfficeDocumentSettings>
                <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
        </xml>
    </noscript>
    <![endif]-->
</head>
<body style="margin: 0; padding: 0; font-family: 'Times New Roman', Georgia, serif; background-color: #f5f5f0;">
    
    <!-- Wrapper Table for Email Clients -->
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #f5f5f0; padding: 20px 0;">
        <tr>
            <td align="center">
                
                <!-- Main Container -->
                <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="800" style="max-width: 800px; background-color: #fefefe; border: 1px solid #ddd; font-family: 'Times New Roman', Georgia, serif;">
                    
                    <!-- Masthead -->
                    <tr>
                        <td style="border-bottom: 4px solid #2c2c2c; padding: 30px 40px 20px; background: linear-gradient(180deg, #fefefe 0%, #f8f8f8 100%);">
                            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                                <tr>
                                    <td align="center">
                                        <h1 style="font-family: 'Times New Roman', serif; font-size: 48px; font-weight: bold; color: #2c2c2c; letter-spacing: 2px; margin: 0 0 8px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">JDX PULSE</h1>
                                        <p style="text-align: center; font-style: italic; font-size: 16px; color: #666; border-bottom: 1px solid #ccc; padding-bottom: 12px; margin: 0 0 16px 0;">"All the Tech News That's Fit to Code"</p>
                                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                                            <tr>
                                                <td style="font-size: 14px; color: #666; font-weight: bold; width: 40%;">{date_str}</td>
                                                <td align="center" style="font-size: 14px; color: #666; font-style: italic; width: 40%;">Digital Edition • Vol. 1, No. {edition_num}</td>
                                                <td align="right" style="width: 20%;">
                                                    <span style="display: inline-block; font-weight: bold; background: #2c2c2c; color: white; padding: 4px 8px; border-radius: 4px; font-size: 14px;">FREE</span>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Headlines Section -->
                    {headlines_html}
                    
                    <!-- News Content -->
                    <tr>
                        <td style="padding: 0 40px 40px;">
                            
                            <!-- Two Column Layout using Tables -->
                            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                                <tr>
                                    <!-- Main Column -->
                                    <td width="65%" style="border-right: 1px solid #ddd; padding-right: 30px; vertical-align: top;">
                                        {main_story_html}
                                        {other_stories_html}
                                    </td>
                                    
                                    <!-- Sidebar -->
                                    <td width="35%" style="padding-left: 30px; vertical-align: top;">
                                        
                                        <!-- Stats Box -->
                                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background: #2c2c2c; color: white; margin-bottom: 30px;">
                                            <tr>
                                                <td style="padding: 20px; text-align: center;">
                                                    <div style="font-size: 16px; font-weight: bold; margin-bottom: 12px; color: white;">TODAY'S PULSE</div>
                                                    
                                                    <div style="margin-bottom: 8px;">
                                                        <div style="font-size: 24px; font-weight: bold; color: #ff4444;">{engagement_display}</div>
                                                        <div style="font-size: 12px; text-transform: uppercase; color: white;">Total Engagements</div>
                                                    </div>
                                                    
                                                    <div style="margin-bottom: 8px;">
                                                        <div style="font-size: 24px; font-weight: bold; color: #ff4444;">{len(summaries)}</div>
                                                        <div style="font-size: 12px; text-transform: uppercase; color: white;">Trending Topics</div>
                                                    </div>
                                                    
                                                    <div>
                                                        <div style="font-size: 24px; font-weight: bold; color: #ff4444;">{total_platforms}</div>
                                                        <div style="font-size: 12px; text-transform: uppercase; color: white;">Platforms Monitored</div>
                                                    </div>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <!-- Trending Section -->
                                        {trending_html}
                                        
                                    </td>
                                </tr>
                            </table>
                            
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background: #2c2c2c; color: white; padding: 30px 40px; text-align: center;">
                            <p style="font-size: 14px; margin: 0 0 16px 0; color: white;">© {current_year} • Powered by JDX Software</p>
                            <div style="font-size: 12px; color: white;">
                                <a href="#" style="color: #ccc; text-decoration: none; margin: 0 12px;">Subscribe</a> |
                                <a href="#" style="color: #ccc; text-decoration: none; margin: 0 12px;">Archive</a> |
                                <a href="#" style="color: #ccc; text-decoration: none; margin: 0 12px;">Contact</a> |
                                <a href="#" style="color: #ccc; text-decoration: none; margin: 0 12px;">Advertise</a> |
                                <a href="#" style="color: #ccc; text-decoration: none; margin: 0 12px;">Unsubscribe</a>
                            </div>
                        </td>
                    </tr>
                    
                </table>
                
            </td>
        </tr>
    </table>
    
</body>
</html>"""
    
    return html_template

def send_newsletter_to_list(subject, html_content, recipient_emails, content_items=None, force_send=False):
    """Send newsletter to multiple recipients with caching"""
    success_count = 0
    for email in recipient_emails:
        if send_newsletter(subject, html_content, email, content_items, force_send):
            success_count += 1
    
    print(f"Successfully sent to {success_count}/{len(recipient_emails)} recipients")
    return success_count

def clear_email_cache():
    """Clear the email cache (useful for testing or manual resets)"""
    email_cache = EmailCache()
    email_cache.clear_cache()

def get_email_cache_stats():
    """Get email cache statistics"""
    email_cache = EmailCache()
    return email_cache.get_cache_stats()

def get_last_sent_info(recipient_email):
    """Get info about last email sent to recipient"""
    email_cache = EmailCache()
    return email_cache.get_last_sent_info(recipient_email)

# Utility functions
def _create_headline(summary):
    """Create a newspaper-style headline"""
    if len(summary) > 60:
        words = summary.split()
        headline_words = []
        char_count = 0
        
        for word in words:
            if char_count + len(word) + 1 > 60:
                break
            headline_words.append(word)
            char_count += len(word) + 1
        
        headline = " ".join(headline_words)
        if not headline.endswith('.'):
            headline += "..."
    else:
        headline = summary
    
    return headline.title() if len(headline) < 30 else headline

def _create_subheadline(story):
    """Create a subheadline with engagement info"""
    source = story.get('source', 'unknown')
    views = story.get('views', 0)
    
    if source == 'youtube':
        return f"{views:,.0f} views as content creator pushes viral boundaries"
    elif source == 'reddit':
        return f"{views:,} upvotes spark community discussion"
    elif source == 'github':
        return f"{views:,} stars from developer community"
    elif source == 'hackernews':
        return f"Tech community debates with {views:,} points"
    elif source == 'wired':
        return f"Professional journalism covering the latest in technology"
    else:
        return f"{views:,} engagements across social platforms"

def _format_engagement(views, source):
    """Format engagement numbers based on source"""
    if views >= 1000000:
        formatted = f"{views/1000000:.1f}M"
    elif views >= 1000:
        formatted = f"{views/1000:.0f}K"
    else:
        formatted = f"{views:,}"
    
    if source == 'youtube':
        return f"{formatted} views"
    elif source == 'reddit':
        return f"{formatted} upvotes"
    elif source == 'github':
        return f"{formatted} stars"
    elif source == 'hackernews':
        return f"{formatted} points"
    elif source == 'wired':
        return f"Featured article"
    else:
        return f"{formatted} engagements"

def _get_source_emoji(source):
    """Get emoji for each source"""
    emojis = {
        'youtube': '📺',
        'reddit': '🔴',  # Reddit's signature red circle/logo
        'github': '⚡',
        'hackernews': '🔺',
        'twitter': '𝕏',
        'wired': '📰'
    }
    return emojis.get(source, '📄')

def _get_action_text(source):
    """Get appropriate action text for each source"""
    actions = {
        'youtube': 'WATCH NOW',
        'reddit': 'READ MORE',
        'github': 'VIEW CODE', 
        'hackernews': 'JOIN DISCUSSION',
        'twitter': 'VIEW POST',
        'wired': 'READ ARTICLE'
    }
    return actions.get(source, 'READ MORE')

def _get_section_name(source):
    """Get newspaper section name for each source"""
    sections = {
        'youtube': 'VIRAL',
        'reddit': 'SOCIAL',
        'github': 'TECH', 
        'hackernews': 'ANALYSIS',
        'twitter': 'X',
        'wired': 'WIRED'
    }
    return sections.get(source, 'NEWS')

def _get_section_color(source):
    """Get section label color for each source"""
    colors = {
        'youtube': '#ff0000',
        'reddit': '#ff4500',
        'github': '#24292e',
        'hackernews': '#ff6600',
        'twitter': '#000000',
        'wired': '#000000'
    }
    return colors.get(source, '#2c2c2c')

def _extract_youtube_id(url):
    """Extract YouTube video ID from URL"""
    import re
    
    # Regular expressions for different YouTube URL formats
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]+)',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def _build_youtube_thumbnail_email(video_url, title):
    """Build YouTube thumbnail HTML for email"""
    video_id = _extract_youtube_id(video_url)
    if not video_id:
        return f'<a href="{video_url}" style="display: inline-block; background: #2c2c2c; color: white; padding: 8px 16px; text-decoration: none; font-size: 14px; font-weight: bold; border: 2px solid #2c2c2c;">WATCH NOW</a>'
    
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    
    return f"""
    <a href="{video_url}" style="display: block; text-decoration: none;">
        <img src="{thumbnail_url}" alt="{title}" style="width: 100%; max-width: 300px; height: auto; border-radius: 6px; margin: 12px 0;">
    </a>
    """