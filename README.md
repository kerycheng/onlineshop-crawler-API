# 網路商店爬蟲API / Onlineshop Crawler API

使用Django Rest Framework API所開發的網路商店爬蟲API。可以爬取Momo購物網、蝦皮和露天拍賣的商品資訊。

## 目錄  

* [安裝](#安裝)  
  * [Docker](#docker)  
  * [GitHub](#github)  
* [使用說明](#使用說明)
  * [指令](#指令)
  * [建議更改](#建議更改)
* [程式與資料庫說明](#程式與資料庫說明)
  * [程式說明](#程式說明)
  * [資料庫說明](#資料庫說明)
* [API](#API)
  * [新增商品關鍵字](#新增商品關鍵字)
  * [刪除商品關鍵字](#刪除商品關鍵字)
  * [查看商品關鍵字](#查看商品關鍵字)
  * [查看商品資訊](#查看商品資訊)


<h2 id="安裝">安裝</h2>  
<h3 id="docker">Docker</h3>  

1. 下載映像檔  

```bash
docker pull kerycheng/django-crawler-api:0.3
```
2. 安裝容器

```bash
docker run -it kerycheng/django-crawler-api:0.3 /bin/bash
```

<h3 id="Github">GitHub</h3>  

1. 下載此專案  

```bash
git https://github.com/kerycheng/onlineshop-crawler-api.git
```

2. 切換目錄  

```bash
cd myproject
```

3. 安裝套件  

```bash
pip install -r requirements.txt
```

4. 執行資料庫遷移  

```bash
python manage.py migrate
```

<h2 id="使用說明">使用說明</h2>  

<h3 id="指令">指令</h3>  

1. 開啟MySQL  

```bash
service mysql start
```

2. 開啟Django

```bash
python manage.py runserver
```

3. 開啟爬蟲排程  

```bash
python /myproject/auto_crawler.py
```

<h3 id="建議更改">建議更改</h3>  

以下內部設定建議使用者做更改：  

1. 更改資料庫。可將連線的資料庫改為自己的資料庫。
```
myproject/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',   # 資料庫引擎
        'NAME': 'myproject',  # 資料庫名
        'USER': 'kery',     # 用户名
        'PASSWORD': '123456',  # 密碼
        'HOST': '127.0.0.1',  # mysql服務所在ip
        'PORT': '3306',         # mysql服務端口
    }
}
```

2. 更改爬蟲週期。預設為每隔24小時進行一次爬蟲，可將hours改為自己想要的時間單位。
```
auto_crawler.py


sched.add_job(run_crawler, 'interval', hours=24)
```

<h2 id="程式與資料庫說明">程式與資料庫說明</h3>  

<h3 id="程式說明">程式說明</h3>
目前爬蟲流程為：  

1. 讀取透過API存儲在ProductKeyword的商品關鍵字  

2. 將昨天所爬取所存取在資料庫的商品資訊刪除  

3. 爬取商品關鍵字相關商品資訊  

4. 將資訊存儲在資料庫

5. 隔24小時重複以上步驟

<h3 id="資料庫說明">資料庫說明</h3>
以下為各資料庫的名稱與欄位：

```
crawler_ProductKeyword (商品關鍵字)

keyword # 關鍵字
```

```
crawler_Momoshop (Momo購物網)

title # 標題
brand # 品牌
link # 連結
price # 原價
amount # 特價
cate # 類型
desc # 描述
```

```
crawler_Shopee (蝦皮)

title # 標題
specification # 規格
link # 連結
price_min # 最低價
price_max # 最高價
historical_sold # 已售出數量
```

```
crawler_Ruten (露天)

title # 標題
link # 連結
price_min # 最低價
price_max # 最高價
historical_sold # 已售出數量
```

<h2 id="API">API</h2>  

<h3 id="新增商品關鍵字">新增商品關鍵字</h3>  

```
Request

POST /api/products/
```

```
Response

POST /api/products/
Content-Type: application/json

{
    "keyword": "關鍵字"
}
```

```
範例：
def add(keyword, api_url = 'http://127.0.0.1:8000/api/products/'):
    data = {'keyword': keyword}
    add_resp = requests.post(api_url, json=data)

    print(add_resp.status_code)
    
add('關鍵字')
```

<h3 id="刪除商品關鍵字">刪除商品關鍵字</h3>  

```
Request

DELETE /api/products/<str:kw>/
```

```
Response

刪除成功
Status: 204 No Content

刪除失敗，關鍵字不存在
Status: 404 Not Found
```

```
範例：
def delete(keyword, api_url = 'http://127.0.0.1:8000/api/products/'):
    url = f'{api_url}{keyword}/'
    del_resp = requests.delete(url)
    
    print(del_resp.status_code)
    
delete('關鍵字')
```

<h3 id="查看商品關鍵字">查看商品關鍵字</h3>  

```
Request

GET /api/products/
```

```
Response

Status: 200 OK
[
    {
        "id": 1,
        "keyword": "關鍵字1"
    },
    {
        "id": 2,
        "keyword": "關鍵字2"
    }
]
```

```
範例：
def show(api_url = 'http://127.0.0.1:8000/api/products/'):
    detail_resp = requests.get(api_url)

    if detail_resp.status_code == 200:
        data = detail_resp.json()
        print(data)
    else:
        print('Failed')
    
show()
```
<h3 id="查看商品資訊">查看商品資訊</h3>  

```
Request

GET /api/products_detail/<str:store>/<str:kw>/
```

```
Response

Status: 200 OK
[
    {
          "id": 1,
          "title": "產品標題",
          "brand": "品牌名稱",
          "link": "產品頁面連結",
          "price": "產品價格",
          "amount": "產品庫存量",
          "cate": "產品類別",
          "desc": "產品描述"
      },
```

```
範例：
def find(keyword, store, api_url = 'http://127.0.0.1:8000/api/products_detail/'):
    url = f'{api_url}{store}/{keyword}/'
    find_resp = requests.get(url)

    if find_resp.status_code == 200:
        data = find_resp.json()
        print(data)
    else:
        print('Failed')
    
find('keyword', 'store')
```
