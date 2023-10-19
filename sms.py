import argparse
import twilio_keys
from twilio.rest import Client

client = Client(username=twilio_keys.key, password=twilio_keys.secret, account_sid=twilio_keys.sid)
# client = Client("AC757fe88ca4cbac1e813879ed1da0c2d9","8dd4e15b248ded5619aa977124d3f5dd")

import re


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
        from_=twilio_keys.from_number,  # Replace with your Twilio phone number
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