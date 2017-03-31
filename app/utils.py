import jwt
import json
import requests
# from datetime import datetime
from flask import redirect
from haikunator import Haikunator
from app.models import Transactions
from config import (fb_url, page_access_token, main_url,
                    JWT_ALGORITHM, JWT_SECRET)


json_headers = {"Content-Type": "application/json"}
params = {"access_token": page_access_token}
room_name = ''


def tokenize(data):
    token = jwt.encode(data, JWT_SECRET, JWT_ALGORITHM)
    return token


def call_user(sender_id, recipient_id):
    sender_details = Transactions.query.filter_by(
        sender_id=sender_id).first()
    sender_data = ''
    recipient_data = ''

    # Check if a session created by sender exists
    if (sender_details.session):
        session = sender_details.session
    else:
        sender_data = {"user": recipient_id,
                       "session": Haikunator.haikunate()}
        Transactions(sender_data).save()

    try:
        recipient_data = {"user": recipient_id,
                          "session": session}
        # Push data to a database
        Transactions(recipient_data).save()
    except Exception:
        pass

    recipient_token = tokenize(recipient_data)
    send_message(recipient_id,
                 'You have been invited to join the following call:'
                 ' {}/call/{}'.format(main_url, recipient_token))
    sender_token = tokenize(sender_data)
    return redirect('/call/{}'.format(sender_token))


def send_message(recipient_id, message_text, template=None):
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }

    if template:
        data['message'] = template

    data = json.dumps(data)
    url = "{}/me/messages".format(fb_url)
    r = requests.post(url, params=params,
                      headers=json_headers, data=data)
    if r.status_code != 200:
        print(r)


def get_user_details(user_id):
    url = "{}/{}".format(fb_url, user_id)
    r = requests.get(url, params=params)
    if r.error:
        return 'User not found'
    return r.get_json()


def get_response_one(text_message):
    # Return a message after matching the keys
    return 'got it, Thanks!'


def get_response_two(text_message):
    # If user found is one create a call and join them
    # If they are more than less than five send the user options to pick from
    # Inform the user to try and complete the other names as in Facebook
    return ''


def get_response_three(text_message):
    # Return a general message as the first two ptions failed
    return ''
