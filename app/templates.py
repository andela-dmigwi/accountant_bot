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

# Templates


def share_template():
    text = ("You have been invited to join "
            "The Samurai Community; "
            "powered by Honor and Integrity")
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
                        "title": "Samurai Community, 'On FB Messanger'",
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


def quick_replies_template(title):
    template = {
        "content_type": "text",
        "title": title,
        "payload": title
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
