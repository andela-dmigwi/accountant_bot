import re
import jwt
import json
import random
import requests
# from datetime import datetime
from flask import redirect
from haikunator import Haikunator
from app.models import Transactions, Users
from app.kb import (reflections, call,
                    general, psychobabble)
from app.templates import *
from config import (fb_url, page_access_token, main_url,
                    JWT_ALGORITHM, JWT_SECRET)


json_headers = {"Content-Type": "application/json"}
params = {"access_token": page_access_token}
room_name = ''
user_not_found = 'User not registered in Facebook'
something_wrong = 'Something went wrong. We are working on it'
video_call = False


class Utils(object):
    '''Class hold methods you to make a webrtc call and send
    via facebook messager'''

    def __init__(self):
        print('*****MY name is Migwi*******')
        self.video_call = False

    def tokenize(self, data):
        token = jwt.encode(data, JWT_SECRET, JWT_ALGORITHM)
        return token

    def call_user(self, sender_id, recipient_id):
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
            Transactions.rollback()

        recipient_token = self.tokenize(recipient_data)
        url = '{}/call/{}'.format(main_url, recipient_token)
        user = self.get_user_details(sender_id)

        if user == user_not_found:
            self.send_message(sender_id, message_text=something_wrong)
        else:
            template = join_call_template(user.name, url)
            self.send_message(recipient_id, template=template)

            sender_token = self.tokenize(sender_data)
            return redirect('/call/{}'.format(sender_token))

    def send_message(self, recipient_id, message_text=None, template=None):
        data = {
            "recipient": {"id": recipient_id},
            "message": {"text": message_text}
        }

        if template:
            data['message'] = template

        data = json.dumps(data)
        url = "{}/me/messages".format(fb_url)
        response = requests.post(url, params=params,
                                 headers=json_headers, data=data)
        if response.status_code != 200:
            print('Error Code 1:', response.json())

    def get_user_details(self, user_id):
        url = "{}/{}".format(fb_url, user_id)
        response = requests.get(url, params=params)
        if 'error' in response:
            print('Error Code 2:', response)
            return error_message
        return response.json()

    def reflect(self, fragment):
        tokens = fragment.lower().split()
        for i, token in enumerate(tokens):
            if token in reflections:
                tokens[i] = reflections[token]
        return ' '.join(tokens)

    def analyze(self, statement, matching_statement):
        for pattern, responses in matching_statement:
            match = re.match(pattern, statement.rstrip(".!"))
            if match:
                response = random.choice(responses)
                return response.format(
                    *[self.reflect(g) for g in match.groups()])
        else:
            return ''

    def match_response(self, text_message):
        options = [call, psychobabble, general]
        response = ''
        for item in options:
            response = self.analyze(text_message, item)
            if re.match(r'(.*call.*)', text_message):
                print('match_response 1 : {}'.format(self.video_call))
                self.video_call = True
            if response:
                return response
        else:
            # This should happen if something goes wrong
            self.video_call = False
            return 'Something went wrong. We are working on it'

    def make_video_call(self, sender_id, text_message):
        matched_users = Users.query.filter(Users.name == text_message,
                                           Users.fb_id != sender_id).all()
        # print('Making a video call: Matched User :::{}'.format(
        # matched_users))
        if matched_users and len(matched_users) == 1:
            # If user found is one create a call and join them
            self.video_call = False
            recipient_id = matched_users[0].fb_id
            self.call_user(sender_id, recipient_id)

        elif matched_users and len(matched_users) < 6:
            # If less than six send the user options to pick from
            # Generate the template
            self.send_message(sender_id, message_text='MIgwi', template=None)

        elif matched_users and len(matched_users) >= 6:
            # if more than six, Inform the user to try and
            # complete the other names as in Facebook
            message_text = 'Too many matches found, Please complete the name..'
            self.send_message(sender_id, message_text=message_text)
        else:
            # If user not found invite them to join Samurai Community
            # Send a share template to invite them to Samurai Community
            self.video_call = False
            user = self.get_user_details(sender_id)
            if user == user_not_found:
                self.send_message(sender_id, message_text=error_message)
            else:
                self.send_message(sender_id, template=share_template(user))

    def user_registration(self):
        pass

    def eliza_response(self, sender_id, text_message):
        if self.video_call:
            # Make a Video call
            print('<<<<<', self.video_call, '>>>>>>')
            self.make_video_call(sender_id, text_message)
        else:
            # Generate response using eliza
            # Return a message after matching the keys
            print('>>>>>', self.video_call, '<<<<<<<')
            response = self.match_response(text_message)
            self.send_message(sender_id, message_text=response)
