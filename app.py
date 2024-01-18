from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    ImageSendMessage,
    TemplateSendMessage,
    CarouselTemplate,
    CarouselColumn,
    PostbackAction,
    PostbackEvent,
    FlexSendMessage,
)

from os import getenv
from re import compile
from urllib.parse import quote
from random import choice, randint
from requests import get

line_bot_api = LineBotApi(getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(getenv("LINE_CHANNEL_SECRET"))
working_status = getenv("DEFALUT_TALKING", default="true").lower() == "true"

app = Flask(__name__)

kkkk = "LAL"


# domain root
@app.route("/")
def home():
    return "Hello, World!"


@app.route("/webhook", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    global kkkk
    if kkkk == "LAL":
        kkkk = "MLK"
    else:
        kkkk = "LAL"

    flex_message = FlexSendMessage(
        alt_text="test",
        contents={
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": kkkk,
                        "size": "xl",
                        "align": "center",
                        "weight": "bold",
                        "color": "#0000ff",
                    },
                ],
            },
        },
    )
    line_bot_api.reply_message(event.reply_token, flex_message)


if __name__ == "__main__":
    app.run()
