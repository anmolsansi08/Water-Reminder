import requests
import datetime
import pytz

# Mailgun API credentials
MAILGUN_API_KEY = "your-mailgun-api-key"
MAILGUN_DOMAIN = "your-mailgun-domain"


# Function to send email
def send_email(to_email):
    subject = "Drink Water Reminder 💧"
    message = "Hey! This is your friendly reminder to drink water. Stay hydrated! 🚰"

    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={"from": f"Water Reminder <no-reply@{MAILGUN_DOMAIN}>",
              "to": to_email,
              "subject": subject,
              "text": message})
    return response.status_code


# Check current PST time
pst = pytz.timezone('America/Los_Angeles')
now = datetime.datetime.now(pst)
hour = now.hour

if 8 <= hour < 22:  # Run only between 8 AM - 10 PM PST
    with open("emails.txt", "r") as file:
        emails = file.readlines()

    for email in emails:
        email = email.strip()
        if email:
            status = send_email(email)
            print(f"Sent to {email}: {status}")
else:
    print("Outside allowed time range. Skipping email.")
