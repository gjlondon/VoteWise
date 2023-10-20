import argparse
import json
import re
import time
import datetime

from environs import Env
from twilio.rest import Client

env = Env()
# Read .env into os.environ
env.read_env()

TWILIO_SID = env.str("TWILIO_SID")
TWILIO_KEY = env.str("TWILIO_KEY")
TWILIO_SECRET = env.str("TWILIO_SECRET")
TWILIO_FROM_NUMBER = env.str("TWILIO_FROM_NUMBER")

client = Client(username=TWILIO_KEY, password=TWILIO_SECRET, account_sid=TWILIO_SID)


def save_to_json(number, user_values, initial_messages=None):
    """
    Save user data and pending messages to a JSON file.

    Args:
    - number (int): The user's unique identifier.
    - user_values (dict): Dictionary of user values.
    - initial_messages (list): List of initial messages to send to the user.
    """
    if initial_messages is None:
        initial_messages = []
    data = {}
    # Load existing data from the JSON file, if it exists.
    try:
        with open('sms-db.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        pass

    # Update the user's data and messages.
    user_values["pending_messages"] = initial_messages
    data[str(number)] = user_values

    # Save the updated data back to the JSON file.
    with open('sms-db.json', 'w') as f:
        json.dump(data, f, indent=4)


def process_messages(send_message_func):
    """
    Process outstanding messages for each user and update the JSON file.

    Args:
    - send_message_func (function): A function to send messages. It should accept two parameters:
                                   1. user_data (dict): The user's data.
                                   2. message (str): The message to send.
    """
    print(f"Processing at {datetime.datetime.now()}")

    # Load data from the JSON file.
    with open('sms-db.json', 'r') as f:
        data = json.load(f)

    for number, user_values in data.items():
        sent_messages = user_values.get("sent_messages", [])
        pending_messages = user_values.get("pending_messages", [])
        # Process each pending message for the user.
        for message in pending_messages[:]:
            send_message_func(user_values, message)
            sent_messages.append(message)
            pending_messages.remove(message)

        # Update the user's data with the processed messages.
        user_values["sent_messages"] = sent_messages
        user_values["pending_messages"] = pending_messages

    # Save the updated data back to the JSON file.
    with open('sms-db.json', 'w') as f:
        json.dump(data, f, indent=4)


# Example usage:
def example_send_message(user_data, message):
    print(f"Sending message to {user_data}: {message}")


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
    # Assuming you might want to parse some arguments here
    args = parser.parse_args()

    while True:  # This will create an infinite loop
        process_messages(example_send_message)
        time.sleep(1)  # This will pause the loop for 1 second
