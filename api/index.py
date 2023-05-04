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

import openai
import os

# 設定 OpenAI API 密鑰
# openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = os.environ["OPENAI_API_KEY"]

# 輸入文本
input_text = "今天天氣很好，請用中文回答。請做一首跟天氣有關的詩"

# 設定 GPT-3.5 模型的檢索引擎
model_engine = "text-davinci-003"

# 設定生成的文本長度
output_length = 50




app = Flask(__name__)

line_bot_api = LineBotApi('k2QIY6qVkiO68vvSd5TFgwu4pQRDNwzANhe+o7DFazJlUp+zFLXgkH/dVwGHNaZLbwOg9a2O0UPmlPh9cXHvuMXIbosy22u7f1xcqQpCA8J+XPxfEm1kgtiGOMDDfYqM6klqiMLgD4IqwIvHzuJE6wdB04t89/1O/w1cDnyilFU=')
webhook_handler = WebhookHandler('37485edd9b3ce7acd55274c0e665bd2c')

@app.route("/")
def home():
    return "LINE BOT API SERVER IS RUNNING."

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 使用 GPT-3.5 模型生成文本
    response = openai.Completion.create(
        engine=model_engine,
        prompt=input_text,
        max_tokens=output_length,
    )

    # 取得生成的文本
    event.message.text = response.choices[0].text.strip()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(event.message.text))


if __name__ == "__main__":
    app.run()