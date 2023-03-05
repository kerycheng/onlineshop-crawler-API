import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

import mysql.connector
from sqlalchemy import create_engine

def momoshop_crawler(keyword, pages):
    url = f'https://m.momoshop.com.tw/search.momo?searchKeyword={keyword}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'
    }

    urls = []
    for page in range(1, pages):
        url = f'https://m.momoshop.com.tw/search.momo?_advFirst=N&_advCp=N&curPage={page}&searchType=1&cateLevel=2&ent=k&searchKeyword={keyword}&_advThreeHours=N&_isFuzzy=0&_imgSH=fourCardType'
        resp = requests.get(url, headers=headers)

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text)
            for item in soup.select('li.goodsItemLi > a'):
                urls.append('https://m.momoshop.com.tw'+item['href'])
        urls = list(set(urls))

    df = []
    for i, url in enumerate(urls):
        columns = []
        values = []
        
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text)
        # 標題
        title = soup.find('meta',{'property':'og:title'})['content']
        # 品牌
        brand = soup.find('meta',{'property':'product:brand'})['content']
        # 連結
        link = soup.find('meta',{'property':'og:url'})['content']
        # 原價
        try:
            price = re.sub(r'\r\n| ','',soup.find('del').text)
        except:
            price = ''
        # 特價
        amount = soup.find('meta',{'property':'product:price:amount'})['content']
        # 類型
        cate = ''.join([i.text for i in soup.findAll('article',{'class':'pathArea'})])
        cate = re.sub('\n|\xa0',' ',cate)
        # 描述
        try:
            desc = soup.find('div',{'class':'Area101'}).text
            desc = re.sub('\r|\n| ', '', desc)
        except:
            desc = ''
        
        columns += ['title', 'brand', 'link', 'price', 'amount', 'cate', 'desc']
        values += [title, brand, link, price, amount, cate, desc]

        ndf = pd.DataFrame(data=values, index=columns).T
        df.append(ndf)
    df=pd.concat(df, ignore_index=True)

    return df

def momoshop_controller(keyword, pages=2):
    momo_df = momoshop_crawler(keyword, pages)

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
    momo_df.to_sql(name='crawler_momoshop', con=engine, if_exists='append', index=False)

    # 關閉MySQL連線
    cnx.close()