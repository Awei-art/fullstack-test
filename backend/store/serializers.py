from rest_framework import serializers
from .models import Product, ProductImage, Variety, ProductGrade

#選擇品種回傳前端格式
class VarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = Variety
        fields = ['id', 'name'] # 確保有 name 


# 小圖片的 Serializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'order']


# 等級規格 Serializer
class ProductGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGrade
        fields = ['id', 'name', 'price', 'stock']


class ProductSerializer(serializers.ModelSerializer):
    # 為了讓前端直接拿到完整的圖片網址，我們需要特別處理 image
    image = serializers.SerializerMethodField()
    # 把關聯的圖片全部抓出來
    images = ProductImageSerializer(many=True, read_only=True)
    # 增加一個 helper field 把 "4 台斤" 組好直接給前端用
    spec_display = serializers.CharField(source='get_spec_display', read_only=True)
    # 也要把單位中文抓出來
    unit_name = serializers.CharField(source='get_unit_type_display', read_only=True)

    # varieties 要用上面的規則展開
    varieties = serializers.SerializerMethodField()

    # 等級清單
    grades = ProductGradeSerializer(many=True, read_only=True)


    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'image', 'images', 'stock','varieties', 'is_mixed', 'short_description',
        'badge',        # 標籤
        'unit_type',    # 單位代號 (catty)
        'unit_name',    # 單位中文 (台斤)
        'unit_value',   # 數值 (4)
        'spec_display', # 組合好的 (4 台斤)
        'mix_limit',    # 混合上限
        'grades', # 等級 庫存 價格
        ]
        


    # 專門用來過濾「有貨」的品種
    def get_varieties(self, obj):
        # 1. 抓出這個商品的所有品種
        # 2. 用 .filter(is_active=True) 只保留有勾選「有貨」的
        # (前提：您的 Variety 模型裡面要有 is_active 這個欄位)
        active_varieties = obj.varieties.filter(is_active=True)
        
        # 3. 最後再轉成 JSON 格式送出
        return VarietySerializer(active_varieties, many=True).data

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None