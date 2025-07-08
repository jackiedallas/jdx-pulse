import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from .email_cache import EmailCache

load_dotenv()

def send_newsletter(subject, html_content, recipient_email, content_items=None, force_send=False):
    """Send newsletter with caching to prevent duplicate sends"""
    
    # Initialize email cache
    email_cache = EmailCache()
    
    # Check if we should send this email
    if content_items and not email_cache.should_send_email(content_items, recipient_email, force_send):
        return True  # Return True since we "successfully" avoided sending a duplicate
    
    message = Mail(
        from_email=os.getenv("FROM_EMAIL"),
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