import jwt
from app import create_app
from flask import request, make_response, render_template, redirect
from app.utils import Utils
from config import JWT_ALGORITHM, JWT_SECRET

app = create_app()
utils = Utils()


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
    print('*******\n', data, '\n#######')
    if not data:
        return make_response("ok", 200)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                sender_id = messaging_event["sender"]["id"]
                # recipient_id = messaging_event["recipient"]["id"]

                if messaging_event.get("message"):
                    event = messaging_event["message"]

                    if "text" in event:
                        message_text = event["text"]
                        utils.eliza_response(sender_id, message_text)
                    else:
                        print('No Text Message sent')

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                # user clicked/tapped "postback" button in earlier message
                if messaging_event.get("postback"):
                    pass

    return make_response("ok", 200)


@app.route('/call/{id}', methods=['POST'])
def validate_user():
    if not id:
        return redirect('nonexistent.html')
    response = redirect('/video_call', code=307)
    response.set_cookie('data', value=id)
    return response


@app.route('/video_call', methods=['POST'])
def live_feed():
    try:
        data = request.get_cookie('data')
        data = jwt.decode(data, JWT_SECRET, algorithms=JWT_ALGORITHM)
        # Query the infomation from the database
        # result = Transaction.query.filter_by(data).first()
    except Exception:
        return redirect('nonexistent.html')
    return render_template('index.html')
