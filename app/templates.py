# Constants
SHARE_INVITE = ("User not found, Share an Invite"
                "with them to join Samurai Community.")
JOIN = "Join The Samurai Community"

# Templates


def share_template(user):
    template = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": SHARE_INVITE,
                        "buttons": [
                            {
                                "type": "element_share",
                                "share_contents": {
                                    "attachment": {
                                        "type": "template",
                                        "image_url": user.image_url,
                                        "payload": {
                                            "template_type": "button",
                                            "text": (
                                                "You have been invited by {}"
                                                " To Join The Samurai"
                                                " Community").format(
                                                user.name),
                                            "buttons": [
                                                {
                                                    "type": "postback",
                                                    "title": JOIN,
                                                    "payload": "SIGN UP"
                                                }
                                            ]
                                        }
                                    }
                                }
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
