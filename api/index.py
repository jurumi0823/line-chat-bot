from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('k2QIY6qVkiO68vvSd5TFgwu4pQRDNwzANhe+o7DFazJlUp+zFLXgkH/dVwGHNaZLbwOg9a2O0UPmlPh9cXHvuMXIbosy22u7f1xcqQpCA8J+XPxfEm1kgtiGOMDDfYqM6klqiMLgD4IqwIvHzuJE6wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('37485edd9b3ce7acd55274c0e665bd2c')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()