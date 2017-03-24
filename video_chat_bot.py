from app import create_app
from flask import request, make_response
from config import verify_token, page_access_token
from fbmq import page as Page

app = create_app()
page = Page(page_access_token)


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


@app.route('/webhook', methods=['POST'])
def webhook():
    page.handle_webhook(request.get_data(as_text=True))
    return "ok"


@page.handle_message
def message_handler(event):
    """:type event: fbmq.Event"""
    sender_id = event.sender_id
    message = event.message_text

    page.send(sender_id, "thank you! your message is '%s'" % message)


@page.after_send
def after_send(payload, response):
    """:type payload: fbmq.Payload"""
    print("complete")
