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
line_bot_api = LineBotApi(
    'KacBUPXf2w1AfgI6lcN6nHu4d+joQHYRym5/vheX/Msvj5WhcWbVt8HRMJrKn0c7cQaDlNsTx5uH3RMTjpd5DEp+2rHnQcMOtbA6I'
    '+/7V2MgRdtVO5zOk5d1emCK3CeJ+I/YMVY+oCL0aH+LrHXxSAdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('129ad0d8f9c6c3c24e26f98d30c9dafb')

# push語法，目前用來測試連線
# line_bot_api.push_message('U21f21eb94a4443c313a6b308f171cf3e', TextSendMessage(text='你可以開始了'))


# 監聽所有來自 /callback 的 Post Request
@app.route("/abit/callback", methods=['POST'])
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

#
# # 必須放上自己的Channel Access Token
# HDUT_line_bot_api = LineBotApi(
#     '739rk2YFFTk4azgl5BJhPiYzaersYDdrIZ3UebCizIItEv3SjSVljzw3SmNRHWgzL6uLpOZzThZvcPVi5+n8N5mtDS+i'
#     '/+IG5ucwAkAj8L5WueJ1nTrx7lQWCRpM/oBB78gqwoNRB/huStVzGihNWwdB04t89/1O/w1cDnyilFU=')
#
# # 必須放上自己的Channel Secret
# HDUT_handler = WebhookHandler('d1ed3947f0b51299c46cacffeda2f401')
#
#
# # 監聽所有來自 /callback 的 Post Request
# @app.route("/HDUT/callback", methods=['POST'])
# def HDUT_callback():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']
#
#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
#
#     # handle webhook body
#     try:
#         HDUT_handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#
#     return 'OK'
#
#
# # 訊息傳遞區塊
# @HDUT_handler.add(MessageEvent, message=TextMessage)
# def HDUT_handler_message(event):
#     message = event.message.text
#     if "日資料" in message:
#         buttons_template_message = TemplateSendMessage(
#             alt_text="日資料資訊",
#             template=CarouselTemplate(
#                 columns=[
#                     CarouselColumn(
#                         thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
#                                             "-181817320.jpg",
#                         title=message[3:] + " 收盤資訊",
#                         text="請點選想查詢的股票資訊",
#                         actions=[
#                             PostbackAction(
#                                 label=message[4:] + " 開盤價",
#                                 display_text="開盤價",
#                                 data="日資料&" + message[4:] + "&開盤價"),
#                             PostbackAction(
#                                 label=message[4:] + " 收盤價",
#                                 display_text="收盤價",
#                                 data="日資料&" + message[4:] + "&收盤價"
#                             ),
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
#                                             "-181817320.jpg",
#                         title=message[4:] + " 收盤資訊",
#                         text="請點選想查詢的股票資訊",
#                         actions=[
#                             PostbackAction(
#                                 label=message[4:] + " 最高價",
#                                 display_text="最高價",
#                                 data="日資料&" + message[4:] + "&最高價"
#                             ),
#                             PostbackAction(
#                                 label=message[4:] + " 最低價",
#                                 display_text="最低價",
#                                 data="日資料&" + message[4:] + "&最低價"
#                             ),
#                         ]
#                     )
#                 ]
#             )
#         )
#         HDUT_line_bot_api.reply_message(event.reply_token, buttons_template_message)
#     elif "月資料" in message:
#         buttons_template_message = TemplateSendMessage(
#             alt_text="月資料資訊",
#             template=CarouselTemplate(
#                 columns=[
#                     CarouselColumn(
#                         thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
#                                             "-181817320.jpg",
#                         title=message[4:] + " 營收資訊",
#                         text="請點選想查詢的營收資訊",
#                         actions=[
#                             PostbackAction(
#                                 label=message[4:] + " 本月營收(千)",
#                                 display_text="本月營收(千)",
#                                 data="月資料&" + message[4:] + "&本月營收(千)"),
#                             PostbackAction(
#                                 label=message[4:] + " 去年單月營收(千)",
#                                 display_text="去年單月營收(千)",
#                                 data="月資料&" + message[4:] + "&去年單月營收(千)"
#                             ),
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
#                                             "-181817320.jpg",
#                         title=message[4:] + " 營收資訊",
#                         text="請點選想查詢的營收資訊",
#                         actions=[
#                             PostbackAction(
#                                 label=message[4:] + " 本年累計營收(千)",
#                                 display_text="本年累計營收(千)",
#                                 data="月資料&" + message[4:] + "&本年累計營收(千)"
#                             ),
#                             PostbackAction(
#                                 label=message[4:] + " 去年累計營收(千)",
#                                 display_text="去年累計營收(千)",
#                                 data="月資料&" + message[4:] + "&本年累計營收(千)"
#                             ),
#                         ]
#                     )
#                 ]
#             )
#         )
#         HDUT_line_bot_api.reply_message(event.reply_token, buttons_template_message)
#     # TODO 新聞資訊模塊
#     elif "新聞" in message:
#         HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#     else:
#         df = api2line.d_closes_api2df()
#         try:
#             if int(message):
#                 if df[df["證券代號"] == message].empty:
#                     HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(text="查無此資料!!"))
#                 else:
#                     reply_text = f'{str(df[df["證券代號"] == message]["證券代號"].values[0])} {str(df[df["證券代號"] == message]["證券簡稱"].values[0])}\n收盤價 = {str(df[df["證券代號"] == message]["收盤價"].values[0])}\n成交筆數 = {str(df[df["證券代號"] == message]["成交筆數"].values[0])}\n日期 = {str(df[df["證券代號"] == message]["資料時間"].values[0])}'
#                     HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
#         except ValueError:
#             if df[df["證券簡稱"] == message].empty:
#                 HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(text="查無此資料!!"))
#             else:
#                 reply_text = f'{str(df[df["證券簡稱"] == message]["證券代號"].values[0])} {str(df[df["證券簡稱"] == message]["證券簡稱"].values[0])}\n收盤價 = {str(df[df["證券簡稱"] == message]["收盤價"].values[0])}\n成交筆數 = {str(df[df["證券簡稱"] == message]["成交筆數"].values[0])}\n日期 = {str(df[df["證券簡稱"] == message]["資料時間"].values[0])} '
#                 HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
#         except Exception as e:
#             print(e)
#             HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(text="查無此資料!!"))
#
#
# # 資料回傳區塊
# @HDUT_handler.add(PostbackEvent)
# def HDUT_handle_message(event):
#     message = event.postback.data
#
#     if "日資料查詢" in message:
#         buttons_template_message = TemplateSendMessage(
#             alt_text="日資料資訊",
#             template=CarouselTemplate(
#                 columns=[
#                     CarouselColumn(
#                         thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
#                                             "-181817320.jpg",
#                         title="每日盤後資訊",
#                         text="請點選想查詢的每日盤後資訊",
#                         actions=[
#                             PostbackAction(
#                                 label="漲幅最高前三名",
#                                 display_text="漲幅最高前三名",
#                                 data="漲幅最高前三名"),
#                             PostbackAction(
#                                 label="本益比最高前三名",
#                                 display_text="本益比最高前三名",
#                                 data="本益比最高前三名"
#                             ),
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
#                                             "-181817320.jpg",
#                         title="三大法人資訊",
#                         text="請點選想查詢的三大法人資訊",
#                         actions=[
#                             PostbackAction(
#                                 label="外資買超前三名",
#                                 display_text="外資買超前三名",
#                                 data="外資買超前三名"
#                             ),
#                             PostbackAction(
#                                 label="外資賣超前三名",
#                                 display_text="外資賣超前三名",
#                                 data="外資賣超前三名"
#                             ),
#                         ]
#                     )
#                 ]
#             )
#         )
#         HDUT_line_bot_api.reply_message(event.reply_token, buttons_template_message)
#     elif "月資料查詢" in message:
#         buttons_template_message = TemplateSendMessage(
#             alt_text="月資料資訊",
#             template=CarouselTemplate(
#                 columns=[
#                     CarouselColumn(
#                         thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
#                                             "-181817320.jpg",
#                         title="月營收資訊",
#                         text="請點選想查詢的月營收資訊",
#                         actions=[
#                             PostbackAction(
#                                 label="單月營收成長最高前三名",
#                                 display_text="單月營收成長最高前三名",
#                                 data="單月營收成長最高前三名"
#                             ),
#                             PostbackAction(
#                                 label="年成長率最高前三名",
#                                 display_text="年成長率最高前三名",
#                                 data="年成長率最高前三名"
#                             ),
#                         ]
#                     )
#                 ]
#             )
#         )
#         HDUT_line_bot_api.reply_message(event.reply_token, buttons_template_message)
#     elif "其他資料查詢" in message:
#         buttons_template_message = TemplateSendMessage(
#             alt_text="其他資料資訊",
#             template=CarouselTemplate(
#                 columns=[
#                     CarouselColumn(
#                         thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
#                                             "-181817320.jpg",
#                         title="股利資訊",
#                         text="請點選想查詢的股利資訊",
#                         actions=[
#                             PostbackAction(
#                                 label="現金股利最高前三名",
#                                 display_text="現金股利最高前三名",
#                                 data="現金股利最高前三名"
#                             ),
#                             PostbackAction(
#                                 label="殖利率最高前三名",
#                                 display_text="殖利率最高前三名",
#                                 data="殖利率最高前三名"
#                             ),
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url="https://content.fortune.com/wp-content/uploads/2016/08/gettyimages"
#                                             "-181817320.jpg",
#                         title="公司價值",
#                         text="請點選想查詢的公司價值資訊",
#                         actions=[
#                             PostbackAction(
#                                 label="市值最高前三名",
#                                 display_text="市值最高前三名",
#                                 data="市值最高前三名"
#                             ),
#                             PostbackAction(
#                                 label="實收資本額最高前三名",
#                                 display_text="實收資本額最高前三名",
#                                 data="實收資本額最高前三名"
#                             ),
#                         ]
#                     )
#                 ]
#             )
#         )
#         HDUT_line_bot_api.reply_message(event.reply_token, buttons_template_message)
#     elif "漲幅最高前三名" in message:
#         df = api2line.d_closes_api2df()
#         df = df[df["漲跌(+/-)"] == "+"]
#         df = df.sort_values(by=["漲跌價差"], ascending=False)
#
#         reply_text = f'''{str(df["證券簡稱"].values[0])}\n{str(df["證券簡稱"].values[1])}\n{str(df["證券簡稱"].values[2])}'''
#
#         HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(
#             text=reply_text))
#     elif "本益比最高前三名" in message:
#         df = api2line.d_closes_api2df()
#         df = df.sort_values(by=["本益比"], ascending=False)
#
#         reply_text = f'''{str(df["證券簡稱"].values[0])}\n{str(df["證券簡稱"].values[1])}\n{str(df["證券簡稱"].values[2])}'''
#
#         HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(
#             text=reply_text))
#     elif "外資買超前三名" in message:
#         df = api2line.three_investors_api2df()
#         df = df.sort_values(by=["外陸資買賣超股數(不含外資自營商)"], ascending=False)
#
#         reply_text = f'''{str(df["證券簡稱"].values[0])}\n{str(df["證券簡稱"].values[1])}\n{str(df["證券簡稱"].values[2])}'''
#
#         HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(
#             text=reply_text))
#     elif "外資賣超前三名" in message:
#         df = api2line.three_investors_api2df()
#         df = df.sort_values(by=["外陸資買賣超股數(不含外資自營商)"], ascending=True)
#
#         reply_text = f'''{str(df["證券簡稱"].values[0])}\n{str(df["證券簡稱"].values[1])}\n{str(df["證券簡稱"].values[2])}'''
#
#         HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(
#             text=reply_text))
#     elif "單月營收成長最高前三名" in message:
#         df = api2line.m_revenues_api2df()
#         df = df.sort_values(by=["本月營收(千)"], ascending=False)
#
#         reply_text = f'''{str(df["證券簡稱"].values[0])}\n{str(df["證券簡稱"].values[1])}\n{str(df["證券簡稱"].values[2])}'''
#
#         HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(
#             text=reply_text))
#     elif "年成長率最高前三名" in message:
#         df = api2line.m_revenues_api2df()
#         df = df.sort_values(by=["年成長率(%)"], ascending=False)
#
#         reply_text = f'''{str(df["證券簡稱"].values[0])}\n{str(df["證券簡稱"].values[1])}\n{str(df["證券簡稱"].values[2])}'''
#
#         HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(
#             text=reply_text))
#     elif "現金股利最高前三名" in message:
#         df = api2line.dividend_policies_api2df()
#         df = df.sort_values(by=["現金股利"], ascending=False)
#
#         reply_text = f'''{str(df["證券簡稱"].values[0])}\n{str(df["證券簡稱"].values[1])}\n{str(df["證券簡稱"].values[2])}'''
#
#         HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(
#             text=reply_text))
#     elif "實收資本額最高前三名" in message:
#         df = api2line.company_details_api2df()
#         df = df.sort_values(by=["實收資本額(百萬)"], ascending=False)
#
#         reply_text = f'''{str(df["證券簡稱"].values[0])}\n{str(df["證券簡稱"].values[1])}\n{str(df["證券簡稱"].values[2])}'''
#
#         HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(
#             text=reply_text))
#     elif "市值最高前三名" in message:
#         df = api2line.market_capitalization()
#         df = df.sort_values(by=["市值"], ascending=False)
#
#         reply_text = f'''{str(df["證券簡稱"].values[0])}\n{str(df["證券簡稱"].values[1])}\n{str(df["證券簡稱"].values[2])}'''
#
#         HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(
#             text=reply_text))
#     elif "殖利率最高前三名" in message:
#         df = api2line.dividend_policies_api2df()
#         df = df.sort_values(by=["合計殖利率"], ascending=False)
#
#         reply_text = f'''{str(df["證券簡稱"].values[0])}\n{str(df["證券簡稱"].values[1])}\n{str(df["證券簡稱"].values[2])}'''
#
#         HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(
#             text=reply_text))
#     elif "日資料" in message and len(event.postback.data.split('&')) == 3:
#         stock = event.postback.data.split('&')[1]
#         category = event.postback.data.split('&')[2]
#         df = api2line.d_closes_api2df()
#
#         HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(
#             text=category + " = " + str(df[df["證券簡稱"] == stock][category].values[0])))
#     elif "月資料" in message and len(event.postback.data.split('&')) == 3:
#         stock = event.postback.data.split('&')[1]
#         category = event.postback.data.split('&')[2]
#         df = api2line.m_revenues_api2df()
#
#         HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(
#             text=category + " = " + str(df[df["證券簡稱"] == stock][category].values[0])))
#     elif "三大法人資料" in message and len(event.postback.data.split('&')) == 2:
#         category = event.postback.data.split('&')[1]
#         df = api2line.three_investors_api2df()
#
#         HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(
#             text=category + " = " + str(df[category].values[0])))
#     else:
#         HDUT_line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#
#
# # 必須放上自己的Channel Access Token
# RC_line_bot_api = LineBotApi(
#     'PMqaeSZs1ZvH46GmmHtLCNUoz4dagHhS6/OdzgsZBtFVPWDwNe+NXxV8qJstGgox5FEloJmLDJEgU42HsEPNd3/5lSGAj'
#     '/m9odTwoA84e1A2M7mpaHLCMts/WZTGYrMtktu/3tvjCAaFSmZZyPOpagdB04t89/1O/w1cDnyilFU=')
#
# # 必須放上自己的Channel Secret
# RC_handler = WebhookHandler('e7b2cc3db319829bf2d30cb53f8bf3d0')
#
#
# # 監聽所有來自 /callback 的 Post Request
# @app.route("/RotaryClub/callback", methods=['POST'])
# def RC_callback():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']
#
#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
#
#     # handle webhook body
#     try:
#         RC_handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#
#     return 'OK'
#
#
# # 訊息傳遞區塊
# @RC_handler.add(MessageEvent, message=TextMessage)
# def RC_handle_message(event):
#     message = event.message.text
#     reply_text = "修正目標為...\n"
#     if "目標" in message:
#         if "早點睡" in message:
#             reply_text = reply_text + "10點前睡覺\n"
#         if "設定鬧鐘" in message:
#             reply_text = reply_text + "設定6點鬧鐘\n"
#         if "點出門" in message:
#             reply_text = reply_text + "7點前出門\n"
#         if "睡醒喝水" in message:
#             reply_text = reply_text + "床頭放杯溫水,睡醒喝\n"
#         if "請別人叫" in message:
#             reply_text = reply_text + "請XXX打電話\n"
#         if reply_text == "修正目標為...\n":
#             reply_text = "好棒棒!!"
#         RC_line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
#     else:
#         reply_text = "輸入錯誤請更正後重新輸入!!"
#         RC_line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))
#
#
# # 資料回傳區塊
# @RC_handler.add(PostbackEvent)
# def RC_handle_message(event):
#     message = event.postback.data
#
#     if "活動資訊" in message:
#         image_message = ImageSendMessage(
#             original_content_url="https://lineedu.a-bit.com.tw/static/123456.png",
#             preview_image_url="https://lineedu.a-bit.com.tw/static/123456.png"
#         )
#         RC_line_bot_api.reply_message(event.reply_token, image_message)
#     elif "目標資訊" in message:
#         reply_text = '''1.「具體」的目標(包含人、事、時、地、物)。\n2.可以「檢核」的明確做法如『明確的時間、數量』、「具體為』...使計畫具體,並可以每天被檢核。'''
#         RC_line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
#     elif "目標範例" in message:
#         reply_text = '目標為...\n5個執行方法...\n1.10點前睡覺\n2.設定6點鬧鐘\n3.7:10前要出門\n4.床頭放杯溫水,睡醒喝\n5.找XXX打電話叫我'
#         RC_line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
#     else:
#         RC_line_bot_api.reply_message(event.reply_token, TextSendMessage(message))


# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, ssl_context=('server.crt', 'server.key'))
