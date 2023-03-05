from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ProductKeyword, Momoshop, Shopee, Ruten
from .serializers import ProductKeywordSerializer, MomoshopSerializer, ShopeeSerializer, RutenSerializer
        
@api_view(['GET', 'POST', 'DELETE'])
def products(request):
    if request.method == 'GET':
        keywords = ProductKeyword.objects.all()
        serializer = ProductKeywordSerializer(keywords, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductKeywordSerializer(data=request.data)

        if serializer.is_valid():
            # 檢查新增的值是否與資料庫中已有的值重複
            keyword = serializer.validated_data.get('keyword')
            if ProductKeyword.objects.filter(keyword=keyword).exists():
                return Response({'message': '該值已存在'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['DELETE'])
def del_products(request, kw):
    try: 
        product_keyword = ProductKeyword.objects.get(keyword=kw)
    except ProductKeyword.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        product_keyword.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
def products_detail(request, store, kw): 
    if request.method == 'GET':
        if store == 'momoshop':
            try:
                product = Momoshop.objects.filter(title__contains=kw)
            except Momoshop.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = MomoshopSerializer(product, many=True)
            return Response(serializer.data)
        
        elif store == 'shopee':
            try:
                product = Shopee.objects.filter(title__contains=kw)
            except Shopee.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = ShopeeSerializer(product, many=True)
            return Response(serializer.data)
        
        elif store == 'ruten':
            try:
                product = Ruten.objects.filter(title__contains=kw)
            except Ruten.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = RutenSerializer(product, many=True)
            return Response(serializer.data)
        
