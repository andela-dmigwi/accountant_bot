''' Created by Migwi Ndung'u
    @ The Samurai Community 2017
'''
# Constants
SHARE_INVITE = ("User not found, Share an Invite "
                "with them to join the Samurai Community.")
JOIN = "Join The Samurai Community"


json_headers = {"Content-Type": "application/json"}
welcome_text = ("Welcome to the The Samurai Community,"
                " you can chat with me; the Samurai Bot"
                " or easily make a video call to your FaceBook"
                " friends with my help.")
user_not_found = 'User not registered in Facebook'
something_wrong = 'Something went wrong. We are working on it'
many_matches = 'Too many matches found, Please complete the name..'
default_profile_pic = ("https://scontent-jnb1-1.xx.fbcdn.net/v/"
                       "t31.0-8/17854913_1884159151861527_"
                       "2986761805025366889_o.jpg?oh=54ed15f5280f"
                       "f5b3455ad6bdb80cafaf&oe=59974D19")

# Templates


def share_template():
    text = ("You've been invited to join "
            "The Samurai Community; "
            "inspired by Honor & Integrity.")
    profile_pic = ("https://scontent-jnb1-1.xx.fbcdn.net/v/"
                   "t31.0-8/17760915_1884046905206085_8625392042052170"
                   "49_o.jpg?oh=987d6e23d447869ed649c17a98b02"
                   "cc8&oe=599A7F12")
    template = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "Samurai Community, 'on FB Messanger'",
                        "subtitle": text,
                        "image_url": profile_pic,
                        "buttons": [
                            {
                                "type": "element_share"
                            }
                        ]
                    }
                ]
            }
        }
    }
    return template


def join_call_template(name, url):
    template = {
        "type": "template",
        "payload": {
            "template_type": "button",
            "text": "What do you want to do next?",
            "buttons": [
                {
                    "type": "web_url",
                    "title": "Join Call invited by {}".format(name),
                    "url": url
                }
            ]
        }
    }
    return template


def quick_replies_template(user_details):
    quick = []
    for user in user_details:
        quick.append(reply_template(user))
    template = {"message": {
        "text": "Choose one person:",
        "quick_replies": quick
    }}
    return template


def reply_template(user):
    template = {
        "content_type": "text",
        "title": user.name,
        "payload": user.name,
        "image_url": user.profile_pic
    }
    return template


def postback_template(title, payload):
    template = {
        "type": "template",
        "payload": {
            "template_type": "button",
            "text": "What do you want to do next?",
            "buttons": [
                {
                    "type": "postback",
                    "title": title,
                    "payload": payload
                }
            ]
        }
    }
    return template

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Get Started Button

# curl -X POST -H "Content-Type: application/json" -d '{
#   "get_started":{
#     "payload":"SIGN_UP"
#   }
# }' "https://graph.facebook.com/v2.6/me/messenger_profile"

# curl -X DELETE -H "Content-Type: application/json" -d '{
#   "fields":[
#     "get_started"
#   ]
# }' "https://graph.facebook.com/v2.6/me/messenger_profile"

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  Greetings Text

# curl -X POST -H "Content-Type: application/json" -d '{
#   "greeting":[
#     {
#       "locale":"default",
#       "text":"Hello {{user_full_name}}, Welcome text"
#     }, {
#       "locale":"en_US",
#       "text":"Timeless apparel for the masses."
#     }
#   ]
# }' "https://graph.facebook.com/v2.6/me/messenger_profile"

# curl -X DELETE -H "Content-Type: application/json" -d '{
#   "fields":[
#     "greeting"
#   ]
# }' "https://graph.facebook.com/v2.6/me/messenger_profile
# ?access_token=PAGE_ACCESS_TOKEN"

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Get Started Button

# curl -X POST -H "Content-Type: application/json" -d '{
#   "setting_type":"call_to_actions",
#   "thread_state":"new_thread",
#   "call_to_actions":[
#     {
#       "payload":"SIGN_UP"
#     }
#   ]
# }' "https://graph.facebook.com/v2.6/me/thread_settings?

# curl -X DELETE -H "Content-Type: application/json" -d '{
#   "setting_type":"call_to_actions",
#   "thread_state":"new_thread"
# }' "https://graph.facebook.com/v2.6/me/thread_settings

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

