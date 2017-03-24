from app import create_app
from flask import request, make_response
from config import verify_token, page_access_token
from fbmq import Page, Attachment
from app.camera import VideoCamera

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
    # Response tests successful deployment of the bot..
    return make_response("Hello world, this is a Facebook"
                         " Video Chat Bot. Enjoy!!", 200)


@app.route('/', methods=['POST'])
def webhook():
    print(request.get_json())
    page.handle_webhook(request.get_data(as_text=True))
    return make_response("ok", 200)


@page.handle_message
def message_handler(event):
    """:type event: fbmq.Event"""
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    # message = event.message_text
    print ('Sender:', sender_id, 'Recipient: ', recipient_id)
    try:
        page.send(sender_id, Attachment.Image(gen(VideoCamera())))
        page.send(recipient_id, gen(VideoCamera()))
    except Exception as e:
        print('Error >>>>> {}'.format(e))
        page.send(sender_id, "........An error Occured........")


@page.after_send
def after_send(payload, response):
    """:type payload: fbmq.Payload"""
    print("complete")


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
