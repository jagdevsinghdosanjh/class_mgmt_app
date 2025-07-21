import smtplib
from email.message import EmailMessage
from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()

# account_sid = os.getenv("TWILIO_SID")
# auth_token = os.getenv("TWILIO_TOKEN")


# --- EMAIL FUNCTION ---
def send_email_receipt(to_email, subject, body, attachment_path=None):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "jagdevsinghdosanjh@gmail.com"
    msg["To"] = to_email
    msg.set_content(body)

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("jagdevsinghdosanjh@gmail.com", "smartscienceai")  # Replace with secure app password
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"[Email Error] {e}")
        return False

# --- SMS FUNCTION ---
def send_sms(to_number, message):
    try:
        account_sid = os.getenv("TWILIO_SID")        # Use environment variables for security
        auth_token = os.getenv("TWILIO_TOKEN")
        client = Client(account_sid, auth_token)
        client.messages.create(
            body=message,
            from_="+1234567890",  # Replace with your Twilio number
            to=to_number
        )
        return True
    except Exception as e:
        print(f"[SMS Error] {e}")
        return False

