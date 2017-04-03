import re
import jwt
import json
import random
import requests
# from datetime import datetime
from flask import redirect
from haikunator import Haikunator
from app.models import Transactions
from app.kb import *
from config import (fb_url, page_access_token, main_url,
                    JWT_ALGORITHM, JWT_SECRET)


json_headers = {"Content-Type": "application/json"}
params = {"access_token": page_access_token}
room_name = ''
video_call = False


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
        return 'User not registered or Incorrect name used'
    return r.get_json()


def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)


def analyze(statement, matching_statement):
    for pattern, responses in matching_statement:
        match = re.match(pattern, statement.rstrip(".!"))
        if match:
            response = random.choice(responses)
            return response.format(*[reflect(g) for g in match.groups()])
    else:
        return ''


def match_response(text_message):
    options = ['call', 'psychobabble', 'general']
    response = ''
    for item in options:
        response = analyze(text_message, item)
        if re.match(r'(.*)call(.*)', 'call'):
            video_call = True
        if response:
            return response
    else:
        # This should never happen
        return 'Something went wrong. We are working on it'


def make_video_call(sender_id, text_message):
    matched_users = Users.query.filter_by(name=text_message).all()
    if matched_users and len(matched_users) == 1:
        recipient_id = matched_users[0].fb_id
        call_user(sender_id, recipient_id)
    elif matched_users and len(matched_users) < 6:
        # Generate the template
        send_message(sender_id, message_text=None, template='MIgwi')
    elif matched_users and len(matched_users) >= 6:
        message_text = 'Too many matches found, Please complete the name..'
        send_message(sender_id, message_text=message_text)
    else:
        message_text = match_response(text_message)
        send_message(sender_id, message_text=message_text)


def eliza_response(sender_id, text_message):
    if video_call:
        # Make a Video call
        make_video_call(sender_id, text_message)
    else:
        video_call = False
        # Generate response using eliza
        # Return a message after matching the keys
        print (video_call)
        return 'got it, Thanks!'


def get_response_two(text_message):
    # If user found is one create a call and join them
    # If they are more than less than five send the user options to pick from
    # Inform the user to try and complete the other names as in Facebook
    send_message(recipient_id, response, template=None)
    return ''


def get_response_three(text_message):
    # Return a general message as the first two ptions failed
    return ''
