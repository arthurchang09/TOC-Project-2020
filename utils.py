import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage,ImageSendMessage


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def push_message(user_id,msg):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(user_id, TextMessage(text=msg))
    
    return "OK"


def send_image_url(id, img_url):
    line_bot_api = LineBotApi(channel_access_token)
    message=ImageSendMessage(
        original_content_url=img_url
        preview_img_url=img_url
        )
    line_bot_api.push_message(id,message)
"""
def send_button_message(id, text, buttons):
    pass
"""
