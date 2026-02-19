from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer

@api_view(['GET'])
def get_products(request):
    # 只抓有庫存的商品，或者您可以拿掉 filter 抓全部
    products = Product.objects.all() 
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def get_product(request, pk):
    # 嘗試用 ID (pk) 去找商品，找不到就回傳 404
    product = get_object_or_404(Product, id=pk)
    # many=False 代表只抓一筆
    serializer = ProductSerializer(product, many=False, context={'request': request})
    return Response(serializer.data)
