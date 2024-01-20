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
from random import randint, choice

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

    if msg == "地圖":
        image_message = ImageSendMessage(
            original_content_url="https://raw.githubusercontent.com/Mike1ife/Camel-Up/main/images/Board.png",
            preview_image_url="https://raw.githubusercontent.com/Mike1ife/Camel-Up/main/images/Board.png",
        )
        line_bot_api.reply_message(event.reply_token, image_message)

    if msg == "骰子":
        color = choice(["紅色", "藍色", "黃色", "紫色", "綠色"])
        color_hex = {
            "紅色": "#EC4747",
            "藍色": "#38D5FF",
            "黃色": "#DBED2A",
            "紫色": "#8E459C",
            "綠色": "#0E8937",
        }
        step = choice(["1", "2", "3"])
        flex_message = FlexSendMessage(
            alt_text="Roll",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": color,
                            "size": "xl",
                            "align": "center",
                            "weight": "bold",
                            "color": color_hex[color],
                        },
                        {
                            "type": "text",
                            "text": "駱駝走",
                            "size": "xl",
                            "align": "center",
                            "weight": "bold",
                            "color": "#000000",
                        },
                        {
                            "type": "text",
                            "text": f"{step}步",
                            "size": "xl",
                            "align": "center",
                            "weight": "bold",
                            "color": color_hex[color],
                        },
                    ],
                },
            },
        )
        line_bot_api.reply_message(event.reply_token, flex_message)

    if msg == "投資":
        carousel_template = CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url="https://raw.githubusercontent.com/Mike1ife/Camel-Up/main/images/Coin5.png",
                    title="紅色駱駝",
                    text="紅色駱駝賭塊",
                    actions=[
                        PostbackAction(
                            label="紅色駱駝賭塊",
                            data="#EC4747 1",
                        ),
                    ],
                )
            ]
        )
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text="下注", template=carousel_template),
        )
    if msg == "陷阱":
        pass
    if msg == "下注":
        carousel_template = CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url="https://raw.githubusercontent.com/Mike1ife/Camel-Up/main/images/Red.png",
                    title="紅色駱駝",
                    text="選擇你要下注的獎池",
                    actions=[
                        PostbackAction(
                            label="紅色第一",
                            data="#EC4747 1",
                        ),
                        PostbackAction(
                            label="紅色墊底",
                            data="#EC4747 -1",
                        ),
                    ],
                ),
                CarouselColumn(
                    thumbnail_image_url="https://raw.githubusercontent.com/Mike1ife/Camel-Up/main/images/Yellow.png",
                    title="黃色駱駝",
                    text="選擇你要下注的獎池",
                    actions=[
                        PostbackAction(
                            label="黃色第一",
                            data="#DBED2A 1",
                        ),
                        PostbackAction(
                            label="黃色墊底",
                            data="#DBED2A -1",
                        ),
                    ],
                ),
                CarouselColumn(
                    thumbnail_image_url="https://raw.githubusercontent.com/Mike1ife/Camel-Up/main/images/Purple.png",
                    title="紫色駱駝",
                    text="選擇你要下注的獎池",
                    actions=[
                        PostbackAction(
                            label="紫色第一",
                            data="#8E459C 1",
                        ),
                        PostbackAction(
                            label="紫色墊底",
                            data="#8E459C -1",
                        ),
                    ],
                ),
                CarouselColumn(
                    thumbnail_image_url="https://raw.githubusercontent.com/Mike1ife/Camel-Up/main/images/Green.png",
                    title="綠色駱駝",
                    text="選擇你要下注的獎池",
                    actions=[
                        PostbackAction(
                            label="綠色第一",
                            data="#0E8937 1",
                        ),
                        PostbackAction(
                            label="綠色墊底",
                            data="#0E8937 -1",
                        ),
                    ],
                ),
                CarouselColumn(
                    thumbnail_image_url="https://raw.githubusercontent.com/Mike1ife/Camel-Up/main/images/Blue.png",
                    title="藍色駱駝",
                    text="選擇你要下注的獎池",
                    actions=[
                        PostbackAction(
                            label="藍色第一",
                            data="#38D5FF 1",
                        ),
                        PostbackAction(
                            label="藍色墊底",
                            data="#38D5FF -1",
                        ),
                    ],
                ),
            ]
        )
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text="下注", template=carousel_template),
        )


@line_handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    color, num = data.split()
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
                        "text": num,
                        "size": "xl",
                        "align": "center",
                        "weight": "bold",
                        "color": color,
                    },
                ],
            },
        },
    )
    line_bot_api.reply_message(event.reply_token, flex_message)


if __name__ == "__main__":
    app.run()
