def build_newsletter(summaries, title="JDX Pulse"):
    """Takes a list of {'summary': ..., 'url': ..., 'views': ...} dicts and formats into a minimalist HTML email."""

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'SF Pro Text', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
                line-height: 1.5;
                color: #000000;
                background-color: #ffffff;
                padding: 0;
                margin: 0;
            }}
            .container {{
                max-width: 680px;
                margin: 0 auto;
                background-color: #ffffff;
            }}
            .header {{
                background: #000000;
                color: #ffffff;
                padding: 60px 40px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 32px;
                font-weight: 300;
                letter-spacing: 2px;
                margin: 0;
            }}
            .subtitle {{
                font-size: 14px;
                font-weight: 400;
                margin-top: 12px;
                opacity: 0.8;
                letter-spacing: 1px;
                text-transform: uppercase;
            }}
            .content {{
                padding: 60px 40px;
            }}
            .item {{
                margin-bottom: 50px;
                padding-bottom: 40px;
                border-bottom: 1px solid #f0f0f0;
                display: flex;
                align-items: flex-start;
                gap: 24px;
            }}
            .item:last-child {{
                border-bottom: none;
                margin-bottom: 0;
                padding-bottom: 0;
            }}
            .item-number {{
                flex-shrink: 0;
                width: 40px;
                height: 40px;
                background: #000000;
                color: #ffffff;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 500;
                font-size: 16px;
                margin-top: 4px;
            }}
            .item-content {{
                flex: 1;
            }}
            .item-meta {{
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 12px;
            }}
            .source-icon {{
                font-size: 16px;
                opacity: 0.7;
            }}
            .source-name {{
                font-size: 12px;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 1px;
                color: #666666;
            }}
            .item-title {{
                font-size: 20px;
                font-weight: 400;
                margin-bottom: 16px;
                color: #000000;
                line-height: 1.4;
            }}
            .item-stats {{
                font-size: 14px;
                color: #666666;
                margin-bottom: 20px;
            }}
            .item-link {{
                display: inline-block;
                background: #000000;
                color: #ffffff;
                padding: 12px 24px;
                text-decoration: none;
                font-size: 14px;
                font-weight: 500;
                letter-spacing: 0.5px;
                border: 2px solid #000000;
                transition: all 0.2s ease;
            }}
            .item-link:hover {{
                background: #ffffff;
                color: #000000;
            }}
            .footer {{
                background-color: #f8f8f8;
                padding: 40px;
                text-align: center;
                border-top: 1px solid #e0e0e0;
            }}
            .footer-text {{
                font-size: 12px;
                color: #666666;
                letter-spacing: 1px;
                text-transform: uppercase;
            }}
            .footer-link {{
                color: #000000;
                text-decoration: none;
                font-weight: 500;
            }}
            @media only screen and (max-width: 600px) {{
                .container {{
                    max-width: 100%;
                }}
                .header, .content, .footer {{
                    padding: 40px 20px;
                }}
                .item {{
                    flex-direction: column;
                    gap: 16px;
                }}
                .item-number {{
                    align-self: flex-start;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{title}</h1>
                <p class="subtitle">Today's Viral Content</p>
            </div>
            <div class="content">
                {_build_content_items(summaries)}
            </div>
            <div class="footer">
                <p class="footer-text">
                    Powered by <a href="https://jdxsoftware.com" class="footer-link">JDX Software</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_template

def _build_content_items(summaries):
    """Helper function to build individual content items."""
    items_html = []
    
    # Source icons mapping
    source_icons = {
        'youtube': '▶',
        'reddit': '●',
        'twitter': '●',
        'tiktok': '♪',
        'github': '⧉',
        'hackernews': '▲',
        'producthunt': '⬟',
        'unknown': '●'
    }
    
    for i, item in enumerate(summaries, 1):
        source = item.get('source', 'unknown')
        icon = source_icons.get(source, '●')
        
        # Format engagement numbers
        views = item.get('views', 0)
        if source == 'youtube':
            stats_text = f"{views:,} views"
        elif source == 'reddit':
            stats_text = f"{views} points"
        elif source == 'github':
            stats_text = f"{views} stars"
        elif source == 'hackernews':
            stats_text = f"{views} points"
        elif source in ['twitter', 'tiktok', 'producthunt']:
            stats_text = f"{views:,} engagements"
        else:
            stats_text = f"{views:,} interactions"
        
        # Action text
        action_text = "View"
        
        item_html = f"""
        <div class="item">
            <div class="item-number">{i}</div>
            <div class="item-content">
                <div class="item-meta">
                    <span class="source-icon">{icon}</span>
                    <span class="source-name">{source.replace('hackernews', 'hacker news').title()}</span>
                </div>
                <div class="item-title">{item['summary']}</div>
                <div class="item-stats">{stats_text}</div>
                <a href="{item['url']}" class="item-link">{action_text}</a>
            </div>
        </div>
        """
        items_html.append(item_html)
    
    return "\n".join(items_html)
