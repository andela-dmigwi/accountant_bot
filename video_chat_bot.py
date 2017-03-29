import json
import requests
from app import create_app
from flask import request, make_response, render_template
from config import page_access_token, fb_url


app = create_app()
params = {"access_token": page_access_token}


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    hub_challenge = request.args.get("hub.challenge")
    if (hub_challenge):
        return make_response(hub_challenge, 200)
    # Response tests successful deployment of the bot..
    return make_response("Hello world, this is a Facebook"
                         " Video and Chat Bot. Enjoy!!", 200)


@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events

    data = request.get_json()
    # you may not want to log every incoming message
    # in production, but it's good for testing
    log(data)
    if not data:
        return make_response("ok", 200)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                sender_id = messaging_event["sender"]["id"]
                # recipient_id = messaging_event["recipient"]["id"]

                if messaging_event.get("message"):  # someone sent us a message
                    # message_text = messaging_event["message"]["text"]
                    send_message(sender_id, "got it({}), thanks!")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                # user clicked/tapped "postback" button in earlier message
                if messaging_event.get("postback"):
                    pass

    return make_response("ok", 200)


@app.route('/call/{id}', methods=['GET'])
def live_feed():
    return render_template('index.html')


def send_message(recipient_id, message_text):
    headers = {"Content-Type": "application/json"}
    data = json.dumps({
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    })
    url = fb_url + "/me/messages"
    r = requests.post(url, params=params,
                      headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print(message)
