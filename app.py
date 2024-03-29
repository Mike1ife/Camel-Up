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
from tools._agent import *

line_bot_api = LineBotApi(getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(getenv("LINE_CHANNEL_SECRET"))
working_status = getenv("DEFALUT_TALKING", default="true").lower() == "true"

camels = None
switch = "off"
operations = ["結束", "開始", "地圖", "骰子", "投資", "陷阱", "下注"]

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

    global switch, camels, operations
    if switch == "off":
        # Only tolerate 開始
        if msg == "開始":
            switch = "on"
            camels = Camels()
            text_message = TextSendMessage(text="游戲開始")
            line_bot_api.reply_message(event.reply_token, text_message)
        else:
            text_message = TextSendMessage(text="請先開始游戲")
            line_bot_api.reply_message(event.reply_token, text_message)
    elif switch == "on":
        # Get various instruction
        if msg == "結束":
            switch = "off"
            camels = None
            text_message = TextSendMessage(text="游戲結束")
            line_bot_api.reply_message(event.reply_token, text_message)

        if msg == "開始":
            text_message = TextSendMessage(text="游戲進行中")
            line_bot_api.reply_message(event.reply_token, text_message)

        if msg == "地圖":
            image_message = ImageSendMessage(
                original_content_url="https://raw.githubusercontent.com/Mike1ife/Camel-Up/main/images/Board.png",
                preview_image_url="https://raw.githubusercontent.com/Mike1ife/Camel-Up/main/images/Board.png",
            )
            line_bot_api.reply_message(event.reply_token, image_message)

        if msg == "骰子":
            header, rows, worksheet = init()
            try:
                user_id = event.source.user_id
                profile = line_bot_api.get_profile(user_id)
                username = profile.display_name
                rows, color, step, board_image = roll_dice(rows, username, camels)

                color_hex = {
                    "紅色": "#EC4747",
                    "藍色": "#38D5FF",
                    "黃色": "#DBED2A",
                    "紫色": "#8E459C",
                    "綠色": "#0E8937",
                }
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
            except:
                text_message = TextSendMessage(text="Unknown User")
                line_bot_api.reply_message(event.reply_token, text_message)

        if msg == "投資":
            carousel_template = CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url="https://github.com/Mike1ife/Camel-Up/blob/main/images/Red5.png?raw=true",
                        title="紅色駱駝",
                        text="紅色駱駝賭塊",
                        actions=[
                            PostbackAction(
                                label="投資",
                                data="投資 紅色",
                            ),
                        ],
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://github.com/Mike1ife/Camel-Up/blob/main/images/Yellow5.png?raw=true",
                        title="黃色駱駝",
                        text="黃色駱駝賭塊",
                        actions=[
                            PostbackAction(
                                label="投資",
                                data="投資 黃色",
                            ),
                        ],
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://github.com/Mike1ife/Camel-Up/blob/main/images/Purple5.png?raw=true",
                        title="紫色駱駝",
                        text="紫色駱駝賭塊",
                        actions=[
                            PostbackAction(
                                label="投資",
                                data="投資 紫色",
                            ),
                        ],
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://github.com/Mike1ife/Camel-Up/blob/main/images/Green5.png?raw=true",
                        title="綠色駱駝",
                        text="綠色駱駝賭塊",
                        actions=[
                            PostbackAction(
                                label="投資",
                                data="投資 綠色",
                            ),
                        ],
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://github.com/Mike1ife/Camel-Up/blob/main/images/Blue5.png?raw=true",
                        title="藍色駱駝",
                        text="藍色駱駝賭塊",
                        actions=[
                            PostbackAction(
                                label="投資",
                                data="投資 藍色",
                            ),
                        ],
                    ),
                ]
            )
            line_bot_api.reply_message(
                event.reply_token,
                TemplateSendMessage(alt_text="下注", template=carousel_template),
            )

        if msg[:2] == "陷阱":
            kind, place = msg.split()[1:]
            text_message = TextSendMessage(text=f"放至陷阱({kind})到{place}")
            line_bot_api.reply_message(event.reply_token, text_message)

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
                                data="下注 紅色 第一",
                            ),
                            PostbackAction(
                                label="紅色墊底",
                                data="下注 紅色 墊底",
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
                                data="下注 黃色 第一",
                            ),
                            PostbackAction(
                                label="黃色墊底",
                                data="下注 黃色 墊底",
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
                                data="下注 紫色 第一",
                            ),
                            PostbackAction(
                                label="紫色墊底",
                                data="下注 紫色 墊底",
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
                                data="下注 綠色 第一",
                            ),
                            PostbackAction(
                                label="綠色墊底",
                                data="下注 綠色 墊底",
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
                                data="下注 藍色 第一",
                            ),
                            PostbackAction(
                                label="藍色墊底",
                                data="下注 藍色 墊底",
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
    data = data.split()
    if data[0] == "下注":
        color, place = data[1], data[2]
        color_hex = {
            "紅色": "#EC4747",
            "藍色": "#38D5FF",
            "黃色": "#DBED2A",
            "紫色": "#8E459C",
            "綠色": "#0E8937",
        }
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
                            "text": f"{color} {place}",
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
    elif data[0] == "投資":
        color = data[1]
        color_hex = {
            "紅色": "#EC4747",
            "藍色": "#38D5FF",
            "黃色": "#DBED2A",
            "紫色": "#8E459C",
            "綠色": "#0E8937",
        }
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
                            "text": f"{color}賭塊",
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


if __name__ == "__main__":
    app.run()
