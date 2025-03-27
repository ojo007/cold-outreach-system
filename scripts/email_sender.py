import json
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import datetime


def load_email_settings():
    """Load email server settings"""
    with open('config/email_settings.json', 'r') as f:
        return json.load(f)


def load_config():
    """Load configuration settings"""
    with open('config/settings.json', 'r') as f:
        return json.load(f)


def send_email(recipient, subject, body, settings):
    """
    Send an email using SMTP
    Returns True if successful, False otherwise
    """
    # In test mode, we'll just print the email rather than sending it
    config = load_config()
    if config.get("test_mode", True):
        print(f"\n--- TEST EMAIL ---")
        print(f"To: {recipient}")
        print(f"Subject: {subject}")
        print(f"Body:\n{body}")
        print(f"--- END TEST EMAIL ---\n")
        return True

    # Real email sending implementation
    try:
        msg = MIMEMultipart()
        msg['From'] = f"{settings['sender_name']} <{settings['sender_email']}>"
        msg['To'] = recipient
        msg['Subject'] = subject
        msg['Reply-To'] = settings.get('reply_to', settings['sender_email'])

        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        server = smtplib.SMTP(settings['smtp_server'], settings['smtp_port'])
        if settings.get('use_tls', False):
            server.starttls()

        # If credentials are provided, login
        if 'username' in settings and 'password' in settings:
            server.login(settings['username'], settings['password'])

        server.send_message(msg)
        server.quit()
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_emails(emails_data=None):
    """
    Send emails to leads or test recipient
    Records sent emails in sent_emails.csv
    """
    if emails_data is None:
        # Load email data from CSV if not provided
        emails_data = []
        with open('data/personalized_emails.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                emails_data.append(row)

    settings = load_email_settings()
    config = load_config()
    sent_records = []

    # In test mode, send all emails to the test recipient
    if config.get("test_mode", True):
        recipient = settings['test_recipient']
        print(f"TEST MODE: Sending all emails to {recipient}")

        # Just send one test email
        if emails_data:
            lead = emails_data[0]
            subject = f"Propertyvisualizer: Ihre Immobilienverwaltung optimieren"
            body = lead['personalized_email']

            success = send_email(recipient, subject, body, settings)

            if success:
                sent_records.append({
                    "lead_id": lead['id'],
                    "recipient": recipient,
                    "subject": subject,
                    "sent_at": datetime.datetime.now().isoformat(),
                    "status": "sent (test)"
                })
                print(f"Test email sent successfully to {recipient}")
            else:
                print(f"Failed to send test email to {recipient}")

    else:
        # Real email sending logic
        for lead in emails_data:
            recipient = lead['email']
            subject = f"Propertyvisualizer: Ihre Immobilienverwaltung optimieren"
            body = lead['personalized_email']

            success = send_email(recipient, subject, body, settings)

            if success:
                sent_records.append({
                    "lead_id": lead['id'],
                    "recipient": recipient,
                    "subject": subject,
                    "sent_at": datetime.datetime.now().isoformat(),
                    "status": "sent"
                })
                print(f"Email sent successfully to {recipient}")
            else:
                print(f"Failed to send email to {recipient}")

    # Record sent emails
    Path("data").mkdir(exist_ok=True)
    with open('data/sent_emails.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=sent_records[0].keys() if sent_records else ["lead_id", "recipient",
                                                                                           "subject", "sent_at",
                                                                                           "status"])
        writer.writeheader()
        writer.writerows(sent_records)

    return sent_records


if __name__ == "__main__":
    send_emails()