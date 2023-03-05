import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()


from crawler.models import ProductKeyword, Shopee, Ruten, Momoshop
from crawler.shopee_crawler import shopee_controller
from crawler.ruten_crawler import ruten_controller
from crawler.momoshop_crawler import momoshop_controller
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def run_crawler():
    print(datetime.datetime.now())

    keywords = ProductKeyword.objects.all()
    print(f'需要爬取的商品關鍵字: {keywords}')

    Shopee.objects.all().delete()
    Ruten.objects.all().delete()
    Momoshop.objects.all().delete()

    for keyword in keywords:
        print(f'執行蝦皮爬蟲, 關鍵字: {keyword}')
        shopee_controller(keyword)

        print(f'執行露天爬蟲, 關鍵字: {keyword}')
        ruten_controller(keyword)

        print(f'執行MOMO爬蟲, 關鍵字: {keyword}')
        momoshop_controller(keyword)

    print('資料已爬取完畢並存進資料庫中')

run_crawler()