import requests
import pandas as pd


# 日收盤資訊
def d_closes_api2df(stock='*'):

    file_type = 'json'  # 傳輸格式
    column = '*'
    url = 'https://192.168.89.111:8080/d_closes?file_type={}&stock={}&column={}'.format(file_type, stock, column)
    res = requests.get(url, verify=False)
    data = res.text  # data為抓取下來的字串

    df = pd.read_json(data, dtype={'證券代號': 'str'})
    df.drop('日收盤資料編號', inplace=True, axis=1)
    df.drop('搜尋名稱', inplace=True, axis=1)
    df.drop('系統時間', inplace=True, axis=1)
    df.drop('更新時間', inplace=True, axis=1)
    return df


# 月營收資訊
def m_revenues_api2df(stock='*'):

    file_type = 'json'  # 傳輸格式
    column = '*'
    url = f'https://192.168.89.111:8080/m_revenues?file_type={file_type}&stock={stock}&column={column}'
    res = requests.get(url, verify=False)
    data = res.text  # data為抓取下來的字串

    df = pd.read_json(data, dtype={'證券代號': 'str'})
    df.drop('月營收資料編號', inplace=True, axis=1)
    df.drop('搜尋名稱', inplace=True, axis=1)
    df.drop('系統時間', inplace=True, axis=1)
    df.drop('更新時間', inplace=True, axis=1)
    return df


# 三大法人資訊
def three_investors_api2df(stock='*'):

    file_type = 'json'  # 傳輸格式
    column = '*'
    url = f'https://192.168.89.111:8080/three_investors?file_type={file_type}&stock={stock}&column={column}'
    res = requests.get(url, verify=False)
    data = res.text  # data為抓取下來的字串

    df = pd.read_json(data, dtype={'證券代號': 'str'})
    df.drop('三大法人資料編號', inplace=True, axis=1)
    df.drop('系統時間', inplace=True, axis=1)
    df.drop('更新時間', inplace=True, axis=1)
    return df


# 股利資訊
def dividend_policies_api2df(stock='*'):

    file_type = 'json'  # 傳輸格式
    column = '*'
    url = f'https://192.168.89.111:8080/dividend_information?file_type={file_type}&stock={stock}&column={column}'
    res = requests.get(url, verify=False)
    data = res.text  # data為抓取下來的字串

    df = pd.read_json(data, dtype={'證券代號': 'str'})
    df.drop('股利資料編號', inplace=True, axis=1)
    df.drop('搜尋名稱', inplace=True, axis=1)
    df.drop('系統時間', inplace=True, axis=1)
    df.drop('更新時間', inplace=True, axis=1)
    return df


# 公司資訊
def company_details_api2df(stock='*'):

    file_type = 'json'  # 傳輸格式
    column = '*'
    url = f'https://192.168.89.111:8080/company_details?file_type={file_type}&stock={stock}&column={column}'
    res = requests.get(url, verify=False)
    data = res.text  # data為抓取下來的字串

    df = pd.read_json(data, dtype={'證券代號': 'str'})
    df['實收資本額(百萬)'] = df['實收資本額(百萬)'] * 1000000
    df.drop('公司資料編號', inplace=True, axis=1)
    df.drop('搜尋名稱', inplace=True, axis=1)
    df.drop('系統時間', inplace=True, axis=1)
    df.drop('更新時間', inplace=True, axis=1)
    return df


# 市值計算
def market_capitalization(stock='*'):

    file_type = 'json'  # 傳輸格式
    column = '*'
    url = f'https://192.168.89.111:8080/company_details?file_type={file_type}&stock={stock}&column={column}'
    res = requests.get(url, verify=False)
    data = res.text  # data為抓取下來的字串

    company_df = pd.read_json(data, dtype={'證券代號': 'str'})
    company_df = company_df.set_index('證券代號')

    url = f'https://192.168.89.111:8080/d_closes?file_type={file_type}&stock={stock}&column={column}'
    res = requests.get(url, verify=False)
    data = res.text  # data為抓取下來的字串

    closes_df = pd.read_json(data, dtype={'證券代號': 'str'})

    closes_df.drop('證券簡稱', inplace=True, axis=1)
    closes_df.drop('資料時間', inplace=True, axis=1)
    closes_df.drop('搜尋名稱', inplace=True, axis=1)
    closes_df.drop('系統時間', inplace=True, axis=1)
    closes_df.drop('更新時間', inplace=True, axis=1)

    closes_df = closes_df.set_index('證券代號')

    company_df = company_df.join(closes_df['收盤價'])
    company_df['市值'] = company_df.apply(lambda x: x['交易所公告股本(千)'] * 1000 * x['收盤價'], axis=1)

    return company_df
