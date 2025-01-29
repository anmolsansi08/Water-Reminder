import requests
import datetime
import pytz
import os

# Mailgun API credentials
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY", "your-mailgun-api-key")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN", "your-mailgun-domain")

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


# Function to send email
def send_email(to_email):
    subject = "Drink Water Reminder 💧"
    message = "Current Time: " + \
              str(now) + \
              "\n\n\n\n\nHey! This is your friendly reminder to drink water. Stay hydrated! 🚰\n\n\n" + \
              "Current Time: " + \
              str(now)

    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={"from": f"Water Reminder <no-reply@{MAILGUN_DOMAIN}>",
                  "to": to_email,
                  "subject": subject,
                  "text": message})

        log_message(f"Sent to {to_email}: {response.status_code}, Response: {response.text}")
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(e)
        log_message(f"Failed to send to {to_email}: {e}")
        return None


if 8 <= hour < 22:  # Run only between 8 AM - 10 PM PST
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
                    status = send_email(email)
                else:
                    log_message("Skipped empty email entry.")
else:
    log_message("Outside allowed time range. Skipping email.")
