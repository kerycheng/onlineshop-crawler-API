from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.chrome.service import Service as ChromeSerive
import json
import time
import pandas as pd
import re

import mysql.connector
from sqlalchemy import create_engine

chrome_service = ChromeSerive('chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-3d-apis")
chrome_options.add_argument('--log-level=3')

driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options, service=chrome_service)

def remove_emoji(string):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def shopee_crawler(keyword, pages=2):
    # 將要抓取的頁面連結存到urls[]裡
    urls = []
    if pages == 1:
        url = f'https://shopee.tw/search?keyword={keyword}&page=0'
        urls.append(url)
    else:
        for i in range(0, pages - 1): # 蝦皮頁面是從page=0開始算，所以這邊做-1
            url = f'https://shopee.tw/search?keyword={keyword}&page={i}'
            urls.append(url)

    dt_all = []

    for url in urls:
        driver.get(url) # 瀏覽器取得網頁連結
        time.sleep(5)
        for request in driver.requests:
            if request.response:
                if request.url.startswith('https://shopee.tw/api/v4/search/search_items?by=relevancy&keyword='): # 若網頁成功跳轉到目標頁面才開始執行
                    response = request.response
                    body = decode(response.body, response.headers.get('Content-Encoding', 'Identity'))
                    decode_body = body.decode('utf8')
                    json_data = json.loads(decode_body) # 將網頁資料全部存進json_data裡

                    data = []
                    rows = json_data['items'] # 總共獲取幾筆資料
                    for i in range(0, len(rows)): # 遍歷每一筆商品
                        product_name = json_data['items'][i]['item_basic']['name'] # 商品標題
                        product_name = re.sub('[^\w\s]', '', product_name)

                        if json_data['items'][i]['item_basic']['tier_variations'] is None:
                            spec = {}
                        else:
                            spec = json_data['items'][i]['item_basic']['tier_variations'][0].get('options', {})
                        specification = [remove_emoji(spec[i]) for i in range(len(spec))] # 規格去emoji

                        price_min = str(json_data['items'][i]['item_basic']['price_min'])[:-5] # 商品最低價

                        price_max = str(json_data['items'][i]['item_basic']['price_max'])[:-5] # 商品最高價

                        historical_sold = json_data['items'][i]['item_basic']['historical_sold'] # 已售出

                        shop_id = json_data['items'][i]['item_basic']['shopid'] # 店家id

                        item_id = json_data['items'][i]['itemid'] # 商品id

                        link = f'https://shopee.tw/{product_name} -i.{shop_id}.{item_id}' # 商品連結

                        # 儲存資料: 商品標題 規格 最低價 最高價 已售出數量 賣場名稱 商品連結
                        data.append(
                            (product_name, specification, link, price_min, price_max, historical_sold)
                        )
                    dt_all.extend(data)
    dt_all_df = pd.DataFrame(dt_all, columns=['title', 'specification', 'link', 'price_min', 'price_max', 'historical_sold'])
    dt_all_df['specification'] = dt_all_df['specification'].apply(lambda x: ', '.join(x))

    return dt_all_df

def shopee_controller(keyword, pages=2):  
    shopee_df = shopee_crawler(keyword, pages)

    # MySQL連線設定
    cnx = mysql.connector.connect(
        user='kery', # 用戶名
        password='123456', # 密碼
        host='127.0.0.1', # 資料庫ip
        database='myproject', # 資料庫名稱
        auth_plugin='mysql_native_password',
        charset='utf8mb4',
        use_unicode=True
    )
    engine = create_engine('mysql+mysqlconnector://kery:123456@127.0.0.1:3306/myproject')

    # 將df寫入MySQL資料表
    shopee_df.to_sql(name='crawler_shopee', con=engine, if_exists='append', index=False)

    # 關閉MySQL連線
    cnx.close()