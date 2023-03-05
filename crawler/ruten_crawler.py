from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.chrome.service import Service as ChromeSerive
import json
import time
import pandas as pd

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

def ruten_crawler(keyword, pages):
# 將要抓取的頁面連結存到urls[]裡

    urls = []
    for i in range(0, pages):
        url = f'https://www.ruten.com.tw/find/?q={keyword}&p={i+1}'
        urls.append(url)

    dt_all = []

    for url in urls:
        driver.get(url) # 瀏覽器取得網頁連結
        time.sleep(5)
        for request in driver.requests:
            if request.response:
                if request.url.startswith('https://rtapi.ruten.com.tw/api/prod/v2/index.php/prod?id='): # 若網頁成功跳轉到目標頁面才開始執行
                    response = request.response
                    body = decode(response.body, response.headers.get('Content-Encoding', 'Identity'))
                    decode_body = body.decode('utf8')
                    json_data = json.loads(decode_body) # 將網頁資料全部存進json_data裡

                    data = []
                    rows = json_data # 總共獲取幾筆資料
                    for i in range(0, len(rows)): # 遍歷每一筆商品
                        product_name = json_data[i]['ProdName'] # 商品標題
                        price_min = json_data[i]['PriceRange'][0] # 商品最低價
                        price_max = json_data[i]['PriceRange'][1] # 商品最高價
                        historical_sold = json_data[i]['SoldQty'] # 已售出
                        prod_id = json_data[i]['ProdId'] # 商品id
                        link = f'https://www.ruten.com.tw/item/show?{prod_id}' # 商品連結

                        # 儲存資料: 商品標題 商品連結 最低價 最高價 已售出數量 
                        data.append(
                            (product_name, link, price_min, price_max, historical_sold)
                        )
                    dt_all.extend(data)
    dt_all_df = pd.DataFrame(dt_all, columns=['title', 'link', 'price_min', 'price_max', 'historical_sold'])

    return dt_all_df

def ruten_controller(keyword, pages=2):
    ruten_df = ruten_crawler(keyword, pages)

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
    ruten_df.to_sql(name='crawler_ruten', con=engine, if_exists='append', index=False)

    # 關閉MySQL連線
    cnx.close()