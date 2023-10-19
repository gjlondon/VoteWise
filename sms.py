import argparse
from twilio.rest import Client


import re
from environs import Env

env = Env()
# Read .env into os.environ
env.read_env()

TWILIO_SID = env.str("TWILIO_SID")
TWILIO_KEY = env.str("TWILIO_KEY")
TWILIO_SECRET = env.str("TWILIO_SECRET")
TWILIO_FROM_NUMBER = env.str("TWILIO_FROM_NUMBER")

client = Client(username=TWILIO_KEY, password=TWILIO_SECRET, account_sid=TWILIO_SID)

def normalize_number(us_number):
    # Remove all non-digits
    digits_only = re.sub(r"[^\d]", "", us_number)

    # Check if it's 10 digits (without country code)
    if len(digits_only) == 10:
        return "+1" + digits_only
    elif len(digits_only) == 11 and digits_only[0] == '1':
        return "+" + digits_only
    else:
        raise ValueError("Invalid U.S. phone number format")


def send(number, text, media=None):
    # implementation of send function
    # Send an MMS
    message = client.messages.create(
        to=normalize_number(number),       # Replace with recipient phone number
        from_=TWILIO_FROM_NUMBER,  # Replace with your Twilio phone number
        body=text,
        media_url=media #"https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Arnold_Schwarzenegger_by_Gage_Skidmore_4.jpg/440px-Arnold_Schwarzenegger_by_Gage_Skidmore_4.jpg"  # Replace with the URL to your media
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send SMS message')
    parser.add_argument('number', type=str, help='phone number to send SMS to')
    parser.add_argument('text', type=str, help='text message to send')
    parser.add_argument('media', type=str, help='media', default=None, nargs='?')

    args = parser.parse_args()

    send(args.number, args.text, args.media)