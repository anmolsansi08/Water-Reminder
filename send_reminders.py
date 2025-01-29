import smtplib
import datetime
import pytz
import os
from email.mime.text import MIMEText

# Brevo (Sendinblue) SMTP Credentials from Environment Variables
SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("BREVO_USERNAME", "your-brevo-username")
SMTP_PASSWORD = os.getenv("BREVO_PASSWORD", "your-brevo-password")

# Log file
LOG_FILE = "logs.txt"


def log_message(message):
    """Logs message to both console and a log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(log_entry.strip())  # Print to console
    with open(LOG_FILE, "a") as log_file:
        log_file.write(log_entry)  # Write to log file


# Check current PST time
pst = pytz.timezone('America/Los_Angeles')
now = datetime.datetime.now(pst)
hour = now.hour
log_message(f"Current PST Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")


# Function to send email using Brevo SMTP
def send_email(to_email):
    subject = "Drink Water Reminder 💧"
    message_text = f"""\
Current Time: {now}

Hey! This is your friendly reminder to drink water. Stay hydrated! 🚰

Current Time: {now}
"""

    msg = MIMEText(message_text)
    msg["Subject"] = subject
    msg["From"] = SMTP_USERNAME  # Must be the verified Brevo sender email
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure connection
            server.login(SMTP_USERNAME, SMTP_PASSWORD)  # Authenticate
            server.sendmail(msg["From"], [msg["To"]], msg.as_string())

        log_message(f"Sent to {to_email}: Success")
        return True
    except Exception as e:
        log_message(f"Failed to send to {to_email}: {e}")
        return False


# Send emails only between 8 AM - 10 PM PST
if 8 <= hour < 22:
    if not os.path.exists("emails.txt"):
        log_message("No email list found (emails.txt missing). Exiting.")
    else:
        with open("emails.txt", "r") as file:
            emails = file.readlines()

        if not emails:
            log_message("No emails found in emails.txt. Exiting.")
        else:
            for email in emails:
                email = email.strip()
                if email:
                    log_message(f"Processing email: {email}")
                    send_email(email)
                else:
                    log_message("Skipped empty email entry.")
else:
    log_message("Outside allowed time range. Skipping email.")
