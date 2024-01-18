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

    carousel_template = CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url="https://github.com/Mike1ife/Camel-Up/blob/main/images/camels.png?raw=true",
                title="第一名下注",
                text="選擇你要下注贏得比賽的駱駝",
                actions=[
                    PostbackAction(
                        label="橘色",
                        data="#FF5733",
                    ),
                    PostbackAction(
                        label="黃色",
                        data="#FFFF00",
                    ),
                    PostbackAction(
                        label="紫色",
                        data="#8E459C",
                    ),
                    PostbackAction(
                        label="綠色",
                        data="#0E8937",
                    ),
                    PostbackAction(
                        label="藍色",
                        data="#38D5FF",
                    ),
                ],
            ),
            CarouselColumn(
                thumbnail_image_url="https://github.com/Mike1ife/Camel-Up/blob/main/images/camels.png?raw=true",
                title="最後一名下注",
                text="選擇你要下注比賽最後一名的駱駝",
                actions=[
                    PostbackAction(
                        label="橘色",
                        data="#FF5733",
                    ),
                    PostbackAction(
                        label="黃色",
                        data="#FFFF00",
                    ),
                    PostbackAction(
                        label="紫色",
                        data="#8E459C",
                    ),
                    PostbackAction(
                        label="綠色",
                        data="#0E8937",
                    ),
                    PostbackAction(
                        label="藍色",
                        data="#38D5FF",
                    ),
                ],
            ),
        ]
    )
    line_bot_api.reply_message(event.reply_token, carousel_template)


@line_handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
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
                        "text": "hahaha",
                        "size": "xl",
                        "align": "center",
                        "weight": "bold",
                        "color": data,
                    },
                ],
            },
        },
    )


if __name__ == "__main__":
    app.run()
