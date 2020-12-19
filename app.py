import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from transitions.extensions import GraphMachine
from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user","option","music","random","play", "guest_num","right","wrong_large","wrong_small","riddle","riddle_right","riddle_wrong"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "option",  
        },
        #music
        {
            "trigger": "advance",
            "source": "option",
            "dest": "music",
            "conditions": "is_going_to_music",
        },
        #play music
        {
            "trigger": "advance",
            "source": "music",
            "dest": "play",
            "conditions": "is_going_to_play",
        },
        {
            "trigger": "advance",
            "source": "play",
            "dest": "music",
            "conditions":"is_going_to_music",
        },
        {
            "trigger": "advance",
            "source": "play",
            "dest": "option",
            "conditions":"is_going_back",
        },
        #------
        #random play music
        {
            "trigger": "advance",
            "source": "music",
            "dest": "random",
            "conditions": "is_going_to_random",
        },
        {
            "trigger": "advance",
            "source": "random",
            "dest": "music",
            "conditions":"is_going_to_music",
        },
        #--------
        #guess number
        {
            "trigger": "advance",
            "source": "option",
            "dest": "guest_num",
            "conditions": "is_going_to_guest_num",
        },
        {
            "trigger": "advance",
            "source": "guest_num",
            "dest": "right",
            "conditions": "is_going_to_right",
        },
        {
            "trigger": "advance",
            "source": "guest_num",
            "dest": "wrong_large",
            "conditions": "is_going_to_wrong_large",
        },
        {
            "trigger": "advance",
            "source": "guest_num",
            "dest": "wrong_small",
            "conditions": "is_going_to_wrong_small",
        },
        {
            "trigger": "advance",
            "source": "wrong_large",
            "dest": "right",
            "conditions": "is_going_to_right",
        },
        {
            "trigger": "advance",
            "source": "wrong_small",
            "dest": "right",
            "conditions": "is_going_to_right",
        },
        {
            "trigger": "advance",
            "source": "wrong_large",
            "dest": "wrong_large",
            "conditions": "is_going_to_wrong_large",
        },
        {
            "trigger": "advance",
            "source": "wrong_large",
            "dest": "wrong_small",
            "conditions": "is_going_to_wrong_small",
        },
        {
            "trigger": "advance",
            "source": "wrong_small",
            "dest": "wrong_large",
            "conditions": "is_going_to_wrong_large",
        },
        {
            "trigger": "advance",
            "source": "wrong_small",
            "dest": "wrong_small",
            "conditions": "is_going_to_wrong_small",
        },        
        
        #-------
        #猜謎
        {
            "trigger": "advance",
            "source": "option",
            "dest": "riddle",
            "conditions": "is_going_to_riddle",
        },
        {
            "trigger": "advance",
            "source": "riddle",
            "dest": "riddle_right",
            "conditions": "is_going_to_riddle_right",
        },
        {
            "trigger": "advance",
            "source": "riddle",
            "dest": "riddle_wrong",
            "conditions": "is_going_to_riddle_wrong",
        },
        {
            "trigger": "advance",
            "source": "riddle_wrong",
            "dest": "riddle_wrong",
            "conditions": "is_going_to_riddle_wrong",
        },
        {
            "trigger": "advance",
            "source": "riddle_wrong",
            "dest": "riddle_right",
            "conditions": "is_going_to_riddle_right",
        },
        #---------
        #---------
        {"trigger": "advance", 
         "source": ["music","random","play", "guest_num","right","wrong_large","wrong_small","riddle","riddle_right","riddle_wrong"], 
         "dest": "option",
         "conditions":"is_going_back"
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)


app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
   # machine.get_graph().draw("fsm.png", format='png',prog="dot")
    port = os.environ['PORT']
    app.run(host="0.0.0.0", port=port, debug=True)
