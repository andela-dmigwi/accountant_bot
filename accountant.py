import json
import requests
from app import create_app
from flask import request, make_response
from config import verify_token, page_access_token, fb_url

app = create_app()


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    hub_mode = request.args.get("hub.mode")
    hub_challenge = request.args.get("hub.challenge")
    if (hub_mode == "subscribe" and hub_challenge):
        hub_verify_token = request.args.get("hub.verify_token")
        if not hub_verify_token == verify_token:
            return make_response("Verification token mismatch", 403)
        return make_response(hub_challenge, 200)

    return make_response("Hello world", 200)


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

                if messaging_event.get("message"):  # someone sent us a message

                    # the facebook ID of the person sending you the message
                    sender_id = messaging_event["sender"]["id"]
                    # the recipient's ID, which should be your page's facebook
                    # ID
                    recipient_id = messaging_event["recipient"]["id"]
                    message_text = messaging_event["message"]["text"]
                    # the message's text
                    print('Response Id:', recipient_id,
                          'message text:', message_text)

                    send_message(sender_id, "got it, thanks!")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                # user clicked/tapped "postback" button in earlier message
                if messaging_event.get("postback"):
                    pass

    return make_response("ok", 200)


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(
        recipient=recipient_id, text=message_text))

    params = {"access_token": page_access_token}
    headers = {"Content-Type": "application/json"}
    data = json.dumps({
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    })
    url = fb_url + "/me/messages"
    print('URL', url)
    r = requests.post(url, params=params,
                      headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print(message)


if __name__ == '__main__':
    app.run(debug=True)
