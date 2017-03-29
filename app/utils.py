import jwt
import json
import requests
from datetime import datetime
from config import fb_url, page_access_token, main_url

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
json_headers = {"Content-Type": "application/json"}
params = {"access_token": page_access_token}


def call_user(user_id, room_name):
    data = {"user_id": user_id,
            "time": datetime.date() + 300000,
            "room": room_name}
    token = jwt.encode(data, JWT_SECRET, JWT_ALGORITHM)
    return '{}/call/{}'.format(main_url, token)


def send_message(recipient_id, message_text):
    data = json.dumps({
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    })
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
    return r.json()


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
