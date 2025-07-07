import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

def send_newsletter(subject, html_content, recipient_email):
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
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_newsletter_to_list(subject, html_content, recipient_emails):
    success_count = 0
    for email in recipient_emails:
        if send_newsletter(subject, html_content, email):
            success_count += 1
    
    print(f"Successfully sent to {success_count}/{len(recipient_emails)} recipients")
    return success_count