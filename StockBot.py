# 載入LineBot所需要的套件
from flask import Flask, request, abort
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.exceptions import (
    InvalidSignatureError  # LINE 的驗證機制
)
from linebot.models import *

# 載入其他所需要的套件
# import pandas as pd
import os
# 載入其他python的檔案
import api2line

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('你的token')

# 必須放上自己的Channel Secret
handler = WebhookHandler('你的Secret code')


# 監聽所有來自 /callback 的 Post Request
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
        abort(400)

    return 'OK'


# 訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if "日資料" in message:
        buttons_template_message = TemplateSendMessage(
            alt_text="日資料資訊",
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
                                            "-181817320.jpg",
                        title=message[3:] + " 收盤資訊",
                        text="請點選想查詢的股票資訊",
                        actions=[
                            PostbackAction(
                                label=message[4:] + " 開盤價",
                                display_text="開盤價",
                                data="日資料&" + message[4:] + "&開盤價"),
                            PostbackAction(
                                label=message[4:] + " 收盤價",
                                display_text="收盤價",
                                data="日資料&" + message[4:] + "&收盤價"
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
                                            "-181817320.jpg",
                        title=message[4:] + " 收盤資訊",
                        text="請點選想查詢的股票資訊",
                        actions=[
                            PostbackAction(
                                label=message[4:] + " 最高價",
                                display_text="最高價",
                                data="日資料&" + message[4:] + "&最高價"
                            ),
                            PostbackAction(
                                label=message[4:] + " 最低價",
                                display_text="最低價",
                                data="日資料&" + message[4:] + "&最低價"
                            ),
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif "月資料" in message:
        buttons_template_message = TemplateSendMessage(
            alt_text="月資料資訊",
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
                                            "-181817320.jpg",
                        title=message[4:] + " 營收資訊",
                        text="請點選想查詢的營收資訊",
                        actions=[
                            PostbackAction(
                                label=message[4:] + " 本月營收(千)",
                                display_text="本月營收(千)",
                                data="月資料&" + message[4:] + "&本月營收(千)"),
                            PostbackAction(
                                label=message[4:] + " 去年單月營收(千)",
                                display_text="去年單月營收(千)",
                                data="月資料&" + message[4:] + "&去年單月營收(千)"
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
                                            "-181817320.jpg",
                        title=message[4:] + " 營收資訊",
                        text="請點選想查詢的營收資訊",
                        actions=[
                            PostbackAction(
                                label=message[4:] + " 本年累計營收(千)",
                                display_text="本年累計營收(千)",
                                data="月資料&" + message[4:] + "&本年累計營收(千)"
                            ),
                            PostbackAction(
                                label=message[4:] + " 去年累計營收(千)",
                                display_text="去年累計營收(千)",
                                data="月資料&" + message[4:] + "&本年累計營收(千)"
                            ),
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    # TODO 新聞資訊模塊
    elif "新聞" in message:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
    else:
        df = api2line.d_closes_api2df()
        try:
            if int(message):
                if df[df["證券代號"] == message].empty:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="查無此資料!!"))
                else:
                    reply_text = '{} {}\n收盤價 = {}\n成交筆數 = {}\n日期 = {}'.format(str(df[df["證券代號"] == message]["證券代號"].values[0]),
                                                                              str(df[df["證券代號"] == message]["證券簡稱"].values[0]),
                                                                              str(df[df["證券代號"] == message]["收盤價"].values[0]),
                                                                              str(df[df["證券代號"] == message]["成交筆數"].values[0]),
                                                                              str(df[df["證券代號"] == message]["資料時間"].values[0]))
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
        except ValueError:
            if df[df["證券簡稱"] == message].empty:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="查無此資料!!"))
            else:
                reply_text = '{} {}\n收盤價 = {}\n成交筆數 = {}\n日期 = {}'.format(str(df[df["證券簡稱"] == message]["證券代號"].values[0]),
                                                                          str(df[df["證券簡稱"] == message]["證券簡稱"].values[0]),
                                                                          str(df[df["證券簡稱"] == message]["收盤價"].values[0]),
                                                                          str(df[df["證券簡稱"] == message]["成交筆數"].values[0]),
                                                                          str(df[df["證券簡稱"] == message]["資料時間"].values[0]))
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
        except Exception as e:
            print(e)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="查無此資料!!"))


# 資料回傳區塊
@handler.add(PostbackEvent)
def handle_message(event):
    message = event.postback.data

    if "日資料查詢" in message:
        buttons_template_message = TemplateSendMessage(
            alt_text="日資料資訊",
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
                                            "-181817320.jpg",
                        title="每日盤後資訊",
                        text="請點選想查詢的每日盤後資訊",
                        actions=[
                            PostbackAction(
                                label="漲幅最高前三名",
                                display_text="漲幅最高前三名",
                                data="漲幅最高前三名"),
                            PostbackAction(
                                label="本益比最高前三名",
                                display_text="本益比最高前三名",
                                data="本益比最高前三名"
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
                                            "-181817320.jpg",
                        title="三大法人資訊",
                        text="請點選想查詢的三大法人資訊",
                        actions=[
                            PostbackAction(
                                label="外資買超前三名",
                                display_text="外資買超前三名",
                                data="外資買超前三名"
                            ),
                            PostbackAction(
                                label="外資賣超前三名",
                                display_text="外資賣超前三名",
                                data="外資賣超前三名"
                            ),
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif "月資料查詢" in message:
        buttons_template_message = TemplateSendMessage(
            alt_text="月資料資訊",
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
                                            "-181817320.jpg",
                        title="月營收資訊",
                        text="請點選想查詢的月營收資訊",
                        actions=[
                            PostbackAction(
                                label="單月營收成長最高前三名",
                                display_text="單月營收成長最高前三名",
                                data="單月營收成長最高前三名"
                            ),
                            PostbackAction(
                                label="年成長率最高前三名",
                                display_text="年成長率最高前三名",
                                data="年成長率最高前三名"
                            ),
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif "其他資料查詢" in message:
        buttons_template_message = TemplateSendMessage(
            alt_text="其他資料資訊",
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
                                            "-181817320.jpg",
                        title="股利資訊",
                        text="請點選想查詢的股利資訊",
                        actions=[
                            PostbackAction(
                                label="現金股利最高前三名",
                                display_text="現金股利最高前三名",
                                data="現金股利最高前三名"
                            ),
                            PostbackAction(
                                label="殖利率最高前三名",
                                display_text="殖利率最高前三名",
                                data="殖利率最高前三名"
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
                                            "-181817320.jpg",
                        title="公司價值",
                        text="請點選想查詢的公司價值資訊",
                        actions=[
                            PostbackAction(
                                label="市值最高前三名",
                                display_text="市值最高前三名",
                                data="市值最高前三名"
                            ),
                            PostbackAction(
                                label="實收資本額最高前三名",
                                display_text="實收資本額最高前三名",
                                data="實收資本額最高前三名"
                            ),
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif "漲幅最高前三名" in message:
        df = api2line.d_closes_api2df()
        df = df[df["漲跌(+/-)"] == "+"]
        df = df.sort_values(by=["漲跌價差"], ascending=False)

        reply_text = '''{}\n{}\n{}'''.format(str(df["證券簡稱"].values[0]), str(df["證券簡稱"].values[1]), str(df["證券簡稱"].values[2]))

        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=reply_text))
    elif "本益比最高前三名" in message:
        df = api2line.d_closes_api2df()
        df = df.sort_values(by=["本益比"], ascending=False)

        reply_text = '''{}\n{}\n{}'''.format(str(df["證券簡稱"].values[0]), str(df["證券簡稱"].values[1]), str(df["證券簡稱"].values[2]))

        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=reply_text))
    elif "外資買超前三名" in message:
        df = api2line.three_investors_api2df()
        df = df.sort_values(by=["外陸資買賣超股數(不含外資自營商)"], ascending=False)

        reply_text = '''{}\n{}\n{}'''.format(str(df["證券簡稱"].values[0]), str(df["證券簡稱"].values[1]), str(df["證券簡稱"].values[2]))

        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=reply_text))
    elif "外資賣超前三名" in message:
        df = api2line.three_investors_api2df()
        df = df.sort_values(by=["外陸資買賣超股數(不含外資自營商)"], ascending=True)

        reply_text = '''{}\n{}\n{}'''.format(str(df["證券簡稱"].values[0]), str(df["證券簡稱"].values[1]), str(df["證券簡稱"].values[2]))

        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=reply_text))
    elif "單月營收成長最高前三名" in message:
        df = api2line.m_revenues_api2df()
        df = df.sort_values(by=["本月營收(千)"], ascending=False)

        reply_text = '''{}\n{}\n{}'''.format(str(df["證券簡稱"].values[0]), str(df["證券簡稱"].values[1]), str(df["證券簡稱"].values[2]))

        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=reply_text))
    elif "年成長率最高前三名" in message:
        df = api2line.m_revenues_api2df()
        df = df.sort_values(by=["年成長率(%)"], ascending=False)

        reply_text = '''{}\n{}\n{}'''.format(str(df["證券簡稱"].values[0]), str(df["證券簡稱"].values[1]), str(df["證券簡稱"].values[2]))

        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=reply_text))
    elif "現金股利最高前三名" in message:
        df = api2line.dividend_policies_api2df()
        df = df.sort_values(by=["現金股利"], ascending=False)

        reply_text = '''{}\n{}\n{}'''.format(str(df["證券簡稱"].values[0]), str(df["證券簡稱"].values[1]), str(df["證券簡稱"].values[2]))

        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=reply_text))
    elif "實收資本額最高前三名" in message:
        df = api2line.company_details_api2df()
        df = df.sort_values(by=["實收資本額(百萬)"], ascending=False)

        reply_text = '''{}\n{}\n{}'''.format(str(df["證券簡稱"].values[0]), str(df["證券簡稱"].values[1]), str(df["證券簡稱"].values[2]))

        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=reply_text))
    elif "市值最高前三名" in message:
        df = api2line.market_capitalization()
        df = df.sort_values(by=["市值"], ascending=False)

        reply_text = '''{}\n{}\n{}'''.format(str(df["證券簡稱"].values[0]), str(df["證券簡稱"].values[1]), str(df["證券簡稱"].values[2]))

        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=reply_text))
    elif "殖利率最高前三名" in message:
        df = api2line.dividend_policies_api2df()
        df = df.sort_values(by=["合計殖利率"], ascending=False)

        reply_text = '''{}\n{}\n{}'''.format(str(df["證券簡稱"].values[0]), str(df["證券簡稱"].values[1]), str(df["證券簡稱"].values[2]))

        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=reply_text))
    elif "日資料" in message and len(event.postback.data.split('&')) == 3:
        stock = event.postback.data.split('&')[1]
        category = event.postback.data.split('&')[2]
        df = api2line.d_closes_api2df()

        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=category + " = " + str(df[df["證券簡稱"] == stock][category].values[0])))
    elif "月資料" in message and len(event.postback.data.split('&')) == 3:
        stock = event.postback.data.split('&')[1]
        category = event.postback.data.split('&')[2]
        df = api2line.m_revenues_api2df()

        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=category + " = " + str(df[df["證券簡稱"] == stock][category].values[0])))
    elif "三大法人資料" in message and len(event.postback.data.split('&')) == 2:
        category = event.postback.data.split('&')[1]
        df = api2line.three_investors_api2df()

        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=category + " = " + str(df[category].values[0])))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))


# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
