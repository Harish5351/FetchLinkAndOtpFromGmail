from dotenv import load_dotenv
from imap_tools import MailBox, AND
import os
import re

# Load .env file
load_dotenv()

# read variables
email_user = os.getenv('EMAIL_USER')
email_pass = os.getenv('EMAIL_PASS')


def check_latest_email():
    # connect to Gmail's IMAP server
    with MailBox('imap.gmail.com').login(email_user, email_pass, 'INBOX') as mailbox:
        # Fetch the latest unread email
        emails = list(mailbox.fetch(AND(seen=False), limit=1, reverse=True))

        if len(emails) == 0:
            return None, None, None  # No Emails Found
        return emails[0]


def extract_link(email_text):
    # Regex pattern to match URLs 

    url_pattern = re.compile(r'https?://[^\s]+')

    match = url_pattern.search(email_text)

    if match:
        return match.group()

    return None


def extract_otp(email_text):
    # Regex pattern to match a 6-digit number 

    otp_pattern = re.compile(r'\b\d{6}\b')

    match = otp_pattern.search(email_text)

    if match:
        return match.group()

    return None


if __name__ == "__main__":
    email = check_latest_email()
    print("email subject: ", email.subject)
    print(email.text)
    print(email.from_)
    # To Fetch Email Link
    link = extract_link(email.text)
    if link:
        print("Extracted Link: ", link)
    else:
        print("No link found in the email content.")
    # To extract otp from email
    otp = extract_otp(email.text)
    if otp:
        print("Extracted OTP: ", otp)
    else:
        print("No OTP found in the email content.")
