import requests
import json
from linebot import LineBotApi


headers = {"Authorization": "Bearer 53LLHDTHwwijScC8HXTXWzSBKEo92Ke8kKLy3z7MZfeI2ciLcEzEa2ZLS6DlTnzLsRWfIbTpp4qMSBU+Dm+P+gZL"
           "/Bns86AYyyso46GWQhC52znsXfHB23Rj8yZySp6+pPzg0lNwNDRJRe0GfPb/IwdB04t89/1O/w1cDnyilFU=", "Content-Type": "application/json"}
line_bot_api = LineBotApi("53LLHDTHwwijScC8HXTXWzSBKEo92Ke8kKLy3z7MZfeI2ciLcEzEa2ZLS6DlTnzLsRWfIbTpp4qMSBU+Dm+P+gZL"
           "/Bns86AYyyso46GWQhC52znsXfHB23Rj8yZySp6+pPzg0lNwNDRJRe0GfPb/IwdB04t89/1O/w1cDnyilFU=")

# # 設定rich_menu
# body = {
#     "size": {"width": 2500, "height": 1686},
#     "selected": "true",
#     "name": "Controller",
#     "chatBarText": "☆~圖文選單~☆",
#     "areas": [
#         {
#           "bounds": {"x": 0, "y": 0, "width": 1250, "height": 843},
#           "action": {"type": "postback", "data": "日資料查詢"}
#         },
#         {
#           "bounds": {"x": 1251, "y": 0, "width": 1250, "height": 843},
#           "action": {"type": "postback", "data": "月資料查詢"}
#         },
#         {
#           "bounds": {"x": 1251, "y": 844, "width": 1250, "height": 843},
#           "action": {"type": "uri", "uri": "https://www.aeust.edu.tw/"}
#         }
#     ]
#   }
#
# req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
#                        headers=headers, data=json.dumps(body).encode('utf-8'))

# 查詢所有rich_menu
rich_menu_list = line_bot_api.get_rich_menu_list()

for rich_menu in rich_menu_list:
    print(rich_menu.rich_menu_id)

# # 設定rich_menu圖片
# with open("rich_menu.jpg", 'rb') as f:
#     line_bot_api.set_rich_menu_image(rich_menu.rich_menu_id, "image/jpeg", f)
#
# req = requests.request('POST', f'https://api.line.me/v2/bot/user/all/richmenu/{rich_menu.rich_menu_id}',
#                        headers=headers)

# # 刪除rich_menu設定
# line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)
