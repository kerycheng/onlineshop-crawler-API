from rest_framework import serializers
from crawler.models import ProductKeyword, Momoshop, Shopee, Ruten

class ProductKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductKeyword
        fields = ('keyword',)

class MomoshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Momoshop
        fields = ('title', 'brand', 'link', 'price', 'amount', 'cate', 'desc')

class ShopeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopee
        fields = ['id', 'title', 'specification', 'link', 'price_min', 'price_max', 'historical_sold']

class RutenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruten
        fields = ['id', 'title', 'link', 'price_min', 'price_max', 'historical_sold']