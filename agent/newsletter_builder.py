from datetime import datetime

def build_newsletter(summaries, title="JDX PULSE"):
    """Build a newspaper-style newsletter from content summaries"""
    
    # Get today's date for masthead
    today = datetime.now()
    date_str = today.strftime("%A, %B %d, %Y")
    edition_num = today.timetuple().tm_yday  # Day of year as edition number
    
    # Sort content by engagement and separate main story
    sorted_content = sorted(summaries, key=lambda x: x.get('views', 0), reverse=True)
    main_story = sorted_content[0] if sorted_content else None
    other_stories = sorted_content[1:6] if len(sorted_content) > 1 else []
    trending_items = sorted_content[6:11] if len(sorted_content) > 6 else sorted_content[1:6]
    
    # Calculate stats
    total_engagement = sum(item.get('views', 0) for item in summaries)
    total_platforms = len(set(item.get('source', 'unknown') for item in summaries))
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} - Daily Tech Tribune</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Times New Roman', Georgia, serif;
                line-height: 1.6;
                color: #2c2c2c;
                background-color: #f5f5f0;
                padding: 20px 0;
            }}
            .newspaper {{
                max-width: 800px;
                margin: 0 auto;
                background-color: #fefefe;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                border: 1px solid #ddd;
            }}
            
            /* Newspaper Header */
            .masthead {{
                border-bottom: 4px solid #2c2c2c;
                padding: 30px 40px 20px;
                background: linear-gradient(180deg, #fefefe 0%, #f8f8f8 100%);
            }}
            .newspaper-name {{
                font-family: 'Old English Text MT', 'Times New Roman', serif;
                font-size: 48px;
                font-weight: bold;
                text-align: center;
                color: #2c2c2c;
                letter-spacing: 2px;
                margin-bottom: 8px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            }}
            .tagline {{
                text-align: center;
                font-style: italic;
                font-size: 16px;
                color: #666;
                border-bottom: 1px solid #ccc;
                padding-bottom: 12px;
                margin-bottom: 16px;
            }}
            .header-info {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 14px;
                color: #666;
            }}
            .date-info {{
                font-weight: bold;
            }}
            .edition-info {{
                font-style: italic;
                margin-left: 8px;
            }}
            .price {{
                font-weight: bold;
                background: #2c2c2c;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                margin-left: auto;
            }}
            
            /* Headlines Section */
            .headlines {{
                padding: 30px 40px;
                border-bottom: 2px solid #2c2c2c;
            }}
            .main-headline {{
                font-size: 42px;
                font-weight: bold;
                line-height: 1.2;
                text-align: center;
                margin-bottom: 16px;
                color: #1a1a1a;
                border-bottom: 3px solid #ff4444;
                padding-bottom: 16px;
            }}
            .sub-headline {{
                font-size: 24px;
                font-weight: normal;
                text-align: center;
                color: #444;
                margin-bottom: 20px;
                font-style: italic;
            }}
            .breaking-news {{
                background: #ff4444;
                color: white;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
                display: inline-block;
                margin-bottom: 16px;
                transform: rotate(-2deg);
                box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }}
            
            /* News Columns */
            .news-content {{
                padding: 0 40px 40px;
            }}
            .columns {{
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 30px;
                margin-bottom: 30px;
            }}
            .main-column {{
                border-right: 1px solid #ddd;
                padding-right: 30px;
            }}
            .sidebar {{
                padding-left: 0;
            }}
            
            /* Article Styles */
            .article {{
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 1px solid #eee;
            }}
            .article:last-child {{
                border-bottom: none;
            }}
            .article-header {{
                margin-bottom: 12px;
            }}
            .section-label {{
                background: #2c2c2c;
                color: white;
                padding: 4px 8px;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                display: inline-block;
                margin-bottom: 8px;
            }}
            .section-label.youtube {{ background: #ff0000; }}
            .section-label.reddit {{ background: #ff4500; }}
            .section-label.github {{ background: #24292e; }}
            .section-label.hackernews {{ background: #ff6600; }}
            .section-label.twitter {{ background: #1da1f2; }}
            .section-label.wired {{ background: #000000; }}
            
            .article-title {{
                font-size: 20px;
                font-weight: bold;
                line-height: 1.3;
                margin-bottom: 8px;
                color: #1a1a1a;
            }}
            .article-subtitle {{
                font-size: 16px;
                color: #666;
                font-style: italic;
                margin-bottom: 12px;
            }}
            .article-meta {{
                font-size: 12px;
                color: #888;
                margin-bottom: 12px;
                border-left: 3px solid #ccc;
                padding-left: 12px;
            }}
            .article-link {{
                display: inline-block;
                background: #2c2c2c;
                color: white;
                padding: 8px 16px;
                text-decoration: none;
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #2c2c2c;
                transition: all 0.3s ease;
            }}
            .article-link:hover {{
                background: white;
                color: #2c2c2c;
                text-decoration: none;
            }}
            .youtube-thumbnail {{
                width: 100%;
                max-width: 300px;
                height: auto;
                border-radius: 6px;
                margin: 12px 0;
                cursor: pointer;
                transition: opacity 0.3s ease;
            }}
            .youtube-thumbnail:hover {{
                opacity: 0.8;
            }}
            
            /* Sidebar Styles */
            .sidebar-section {{
                margin-bottom: 30px;
                padding: 20px;
                background: #f8f8f8;
                border: 1px solid #ddd;
            }}
            .sidebar-title {{
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 16px;
                text-transform: uppercase;
                letter-spacing: 1px;
                border-bottom: 2px solid #2c2c2c;
                padding-bottom: 8px;
            }}
            .trending-item {{
                margin-bottom: 16px;
                padding-bottom: 12px;
                border-bottom: 1px dotted #ccc;
            }}
            .trending-item:last-child {{
                border-bottom: none;
                margin-bottom: 0;
            }}
            .trending-number {{
                font-weight: bold;
                color: #ff4444;
                margin-right: 8px;
            }}
            .trending-title {{
                font-size: 14px;
                line-height: 1.4;
            }}
            .trending-source {{
                font-size: 11px;
                color: #888;
                text-transform: uppercase;
                margin-top: 4px;
            }}
            
            /* Stats Box */
            .stats-box {{
                background: #2c2c2c;
                color: white;
                padding: 20px;
                text-align: center;
                margin-bottom: 30px;
            }}
            .stats-title {{
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 12px;
            }}
            .stat-item {{
                margin-bottom: 8px;
            }}
            .stat-number {{
                font-size: 24px;
                font-weight: bold;
                color: #ff4444;
            }}
            .stat-label {{
                font-size: 12px;
                text-transform: uppercase;
            }}
            
            /* Footer */
            .newspaper-footer {{
                background: #2c2c2c;
                color: white;
                padding: 30px 40px;
                text-align: center;
            }}
            .footer-text {{
                font-size: 14px;
                margin-bottom: 16px;
            }}
            .footer-links {{
                font-size: 12px;
            }}
            .footer-links a {{
                color: #ccc;
                text-decoration: none;
                margin: 0 12px;
            }}
            .footer-links a:hover {{
                color: white;
                text-decoration: underline;
            }}
            
            /* Mobile Responsive */
            @media only screen and (max-width: 600px) {{
                .newspaper {{
                    margin: 0 10px;
                }}
                .masthead, .news-content {{
                    padding: 20px;
                }}
                .newspaper-name {{
                    font-size: 32px;
                }}
                .main-headline {{
                    font-size: 28px;
                }}
                .sub-headline {{
                    font-size: 18px;
                }}
                .columns {{
                    grid-template-columns: 1fr;
                    gap: 20px;
                }}
                .main-column {{
                    border-right: none;
                    padding-right: 0;
                }}
                .headlines {{
                    padding: 20px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="newspaper">
            <!-- Masthead -->
            <div class="masthead">
                <h1 class="newspaper-name">{title}</h1>
                <p class="tagline">"All the Tech News That's Fit to Code"</p>
                <div class="header-info">
                    <span class="date-info">{date_str}</span>
                    <span class="edition-info">Digital Edition • Vol. 1, No. {edition_num}</span>
                    <span class="price">FREE</span>
                </div>
            </div>
            
            {_build_headlines_section(main_story)}
            
            <!-- News Content -->
            <div class="news-content">
                <div class="columns">
                    <!-- Main Column -->
                    <div class="main-column">
                        {_build_main_story(main_story)}
                        {_build_other_stories(other_stories)}
                    </div>
                    
                    <!-- Sidebar -->
                    <div class="sidebar">
                        {_build_stats_box(total_engagement, len(summaries), total_platforms)}
                        {_build_trending_sidebar(trending_items)}
                    </div>
                </div>
            </div>
            
            <!-- Footer -->
            <div class="newspaper-footer">
                <p class="footer-text">© 2025 {title} • Powered by JDX Software</p>
                <div class="footer-links">
                    <a href="#">Subscribe</a> |
                    <a href="#">Archive</a> |
                    <a href="#">Contact</a> |
                    <a href="#">Advertise</a> |
                    <a href="#">Unsubscribe</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_template

def _build_headlines_section(main_story):
    """Build the headlines section with the top story"""
    if not main_story:
        return """
        <div class="headlines">
            <div class="breaking-news">🔥 BREAKING</div>
            <h2 class="main-headline">No Major Stories Today</h2>
            <p class="sub-headline">Check back tomorrow for the latest tech trends</p>
        </div>
        """
    
    # Create a compelling headline from the summary
    headline = _create_headline(main_story)
    subheadline = _create_subheadline(main_story)
    
    return f"""
    <div class="headlines">
        <div class="breaking-news">🔥 BREAKING</div>
        <h2 class="main-headline">{headline}</h2>
        <p class="sub-headline">{subheadline}</p>
    </div>
    """

def _build_main_story(main_story):
    """Build the main story article"""
    if not main_story:
        return ""
    
    source = main_story.get('source', 'unknown')
    views = main_story.get('views', 0)
    
    # Format views based on source
    views_text = _format_engagement(views, source)
    
    # Get source emoji and action text
    source_emoji = _get_source_emoji(source)
    action_text = _get_action_text(source)
    
    # Build appropriate media based on source
    if source == 'youtube':
        media_content = _build_youtube_thumbnail(main_story['url'], main_story.get('title', ''))
    else:
        media_content = f'<a href="{main_story['url']}" class="article-link">{action_text}</a>'
    
    return f"""
    <article class="article">
        <div class="article-header">
            <span class="section-label {source}">{source.upper()}</span>
            <h3 class="article-title">{_create_headline(main_story)}</h3>
            <p class="article-subtitle">{_create_subheadline(main_story)}</p>
        </div>
        <div class="article-meta">
            {source_emoji} {source.title()} • {views_text}
        </div>
        {media_content}
    </article>
    """

def _build_other_stories(stories):
    """Build other news stories"""
    if not stories:
        return ""
    
    stories_html = []
    for story in stories:
        source = story.get('source', 'unknown')
        views = story.get('views', 0)
        views_text = _format_engagement(views, source)
        source_emoji = _get_source_emoji(source)
        action_text = _get_action_text(source)
        
        # Build appropriate media based on source
        if source == 'youtube':
            media_content = _build_youtube_thumbnail(story['url'], story.get('title', ''))
        else:
            media_content = f'<a href="{story['url']}" class="article-link">{action_text}</a>'
        
        story_html = f"""
        <article class="article">
            <div class="article-header">
                <span class="section-label {source}">{_get_section_name(source)}</span>
                <h3 class="article-title">{story['summary'][:80]}{'...' if len(story['summary']) > 80 else ''}</h3>
            </div>
            <div class="article-meta">
                {source_emoji} {source.title()} • {views_text}
            </div>
            {media_content}
        </article>
        """
        stories_html.append(story_html)
    
    return "\n".join(stories_html)

def _build_stats_box(total_engagement, total_stories, total_platforms):
    """Build the stats box for sidebar"""
    # Format large numbers
    if total_engagement >= 1000000:
        engagement_str = f"{total_engagement/1000000:.1f}M"
    elif total_engagement >= 1000:
        engagement_str = f"{total_engagement/1000:.0f}K"
    else:
        engagement_str = str(total_engagement)
    
    return f"""
    <div class="stats-box">
        <div class="stats-title">TODAY'S PULSE</div>
        <div class="stat-item">
            <div class="stat-number">{engagement_str}</div>
            <div class="stat-label">Total Engagements</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{total_stories}</div>
            <div class="stat-label">Trending Topics</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{total_platforms}</div>
            <div class="stat-label">Platforms Monitored</div>
        </div>
    </div>
    """

def _build_trending_sidebar(trending_items):
    """Build the trending sidebar"""
    if not trending_items:
        return ""
    
    trending_html = []
    for i, item in enumerate(trending_items[:5], 1):
        source = item.get('source', 'unknown')
        title = item['summary'][:60] + ('...' if len(item['summary']) > 60 else '')
        
        trending_html.append(f"""
        <div class="trending-item">
            <span class="trending-number">{i}.</span>
            <div class="trending-title">{title}</div>
            <div class="trending-source">{source.title()}</div>
        </div>
        """)
    
    return f"""
    <div class="sidebar-section">
        <h4 class="sidebar-title">Trending Now</h4>
        {"".join(trending_html)}
    </div>
    """

def _create_headline(story):
    """Create a newspaper-style headline from story"""
    summary = story['summary']
    
    # If summary is too long, truncate and make it more headline-like
    if len(summary) > 60:
        # Try to find a good breaking point
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
    else:
        return f"{formatted} engagements"

def _get_source_emoji(source):
    """Get emoji for each source"""
    emojis = {
        'youtube': '📺',
        'reddit': '📱',
        'github': '⚡',
        'hackernews': '🔺',
        'twitter': '🐦',
        'wired': '⚡',
        'devto': '📝'
    }
    return emojis.get(source, '📄')

def _get_action_text(source):
    """Get appropriate action text for each source"""
    actions = {
        'youtube': 'WATCH NOW',
        'reddit': 'READ MORE',
        'github': 'VIEW CODE',
        'hackernews': 'JOIN DISCUSSION',
        'twitter': 'VIEW TWEET',
        'wired': 'READ ARTICLE',
        'devto': 'READ ARTICLE'
    }
    return actions.get(source, 'READ MORE')

def _get_section_name(source):
    """Get newspaper section name for each source"""
    sections = {
        'youtube': 'VIRAL',
        'reddit': 'SOCIAL',
        'github': 'TECH',
        'hackernews': 'ANALYSIS',
        'twitter': 'SOCIAL',
        'wired': 'TECH',
        'devto': 'ARTICLES'
    }
    return sections.get(source, 'NEWS')

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

def _build_youtube_thumbnail(video_url, title):
    """Build YouTube thumbnail HTML"""
    video_id = _extract_youtube_id(video_url)
    if not video_id:
        return f'<a href="{video_url}" class="article-link">WATCH NOW</a>'
    
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    
    return f"""
    <a href="{video_url}" target="_blank">
        <img src="{thumbnail_url}" alt="{title}" class="youtube-thumbnail">
    </a>
    """