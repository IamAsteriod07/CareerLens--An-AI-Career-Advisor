import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email_sendgrid(receiver_email, subject, body):
    message = Mail(
        from_email=os.environ.get("SENDGRID_FROM_EMAIL"),
        to_emails=receiver_email,
        subject=subject,
        plain_text_content=body,
    )
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        return f"Email sent with status code {response.status_code}."
    except Exception as e:
        return f"Failed to send email: {str(e)}"
