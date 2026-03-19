from rest_framework import serializers
from .models import Product, ProductImage, Variety, ProductGrade, Coupon, UserCoupon, DessertCategory, Dessert, ProductCategory, DessertGrade, DessertImage, Banner

#選擇品種回傳前端格式
class VarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = Variety
        fields = ['id', 'name', 'color'] # 確保有 name 和 color 


class BannerSerializer(serializers.ModelSerializer):
    """首頁輪播圖序列化器"""
    image = serializers.SerializerMethodField()
    mobile_image = serializers.SerializerMethodField()
    link_url = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ['id', 'title', 'subtitle', 'image', 'mobile_image', 'link_url', 'order']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None
        
    def get_mobile_image(self, obj):
        request = self.context.get('request')
        if obj.mobile_image:
            return request.build_absolute_uri(obj.mobile_image.url)
        return None

    def get_link_url(self, obj):
        if obj.target_product:
            return f"/products/{obj.target_product.id}"
        if obj.target_dessert:
            return f"/desserts/{obj.target_dessert.id}"
        return obj.custom_link


# 品種介紹頁專用（完整資料）
class VarietyDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Variety
        fields = ['id', 'name', 'color', 'description', 'image', 'origin', 'flavor', 'season', 'is_active']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


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



class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name']


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
        'grades',       # 等級 庫存 價格
        'category',     # 分類 ID
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

from .models import Bulletin

class BulletinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bulletin
        fields = ['id', 'title', 'content', 'start_date', 'end_date', 'created_at']


from .models import NewsCategory, News

class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ['id', 'name']


class NewsListSerializer(serializers.ModelSerializer):
    """列表頁用（精簡版）"""
    category_name = serializers.CharField(source='category.name', default='', read_only=True)
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'summary', 'category_name', 'cover_image', 'published_date', 'is_pinned']

    def get_cover_image(self, obj):
        request = self.context.get('request')
        if obj.cover_image:
            return request.build_absolute_uri(obj.cover_image.url)
        return None


class NewsDetailSerializer(serializers.ModelSerializer):
    """單篇詳情用"""
    category_name = serializers.CharField(source='category.name', default='', read_only=True)
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'summary', 'content', 'category_name', 'cover_image', 'published_date', 'created_at', 'is_pinned']

    def get_cover_image(self, obj):
        request = self.context.get('request')
        if obj.cover_image:
            return request.build_absolute_uri(obj.cover_image.url)
        return None

# ========================================
# 優惠券與錢包 Serializers
# ========================================

class CouponSummarySerializer(serializers.ModelSerializer):
    """只回傳必要的優惠券資訊給前端錢包"""
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'title', 'discount_type', 'discount_value', 'min_spend', 'valid_from', 'valid_to', 'is_active']

class UserCouponSerializer(serializers.ModelSerializer):
    """會員專屬優惠券"""
    coupon = CouponSummarySerializer(read_only=True)
    status_msg = serializers.SerializerMethodField()

    class Meta:
        model = UserCoupon
        fields = ['id', 'coupon', 'is_used', 'used_at', 'status_msg']

    def get_status_msg(self, obj):
        from django.utils import timezone
        now = timezone.now()
        
        if obj.is_used:
            return "已使用"
        if not obj.coupon.is_active:
            return "已停用"
        if obj.coupon.valid_to < now:
            return "已過期"
        if obj.coupon.valid_from > now:
            return "尚未生效"
        return "可使用"

# ========================================
# 訂單相關 Serializers
# ========================================
from .models import Order, OrderItem
from django.db import transaction


class OrderItemSerializer(serializers.ModelSerializer):
    """訂單品項序列化器（用於讀取/回傳）"""
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product_name', 'grade_name', 'variety_names',
            'product_image', 'unit_price', 'quantity', 'item_total'
        ]


class OrderSerializer(serializers.ModelSerializer):
    """訂單序列化器（用於讀取完整訂單詳情）"""
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'receiver_name', 'receiver_phone',
            'shipping_city', 'shipping_district', 'shipping_address',
            'subtotal', 'shipping_fee', 'coupon_code', 'discount_amount', 'total_amount',
            'status', 'status_display',
            'payment_method', 'payment_method_display',
            'payment_status', 'payment_status_display',
            'note', 'created_at', 'items'
        ]


class OrderListSerializer(serializers.ModelSerializer):
    """訂單列表序列化器（精簡版，用於會員訂單列表）"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    item_count = serializers.SerializerMethodField()
    first_item_image = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'total_amount',
            'status', 'status_display',
            'payment_method', 'payment_method_display',
            'created_at', 'item_count', 'first_item_image'
        ]

    def get_item_count(self, obj):
        return obj.items.count()

    def get_first_item_image(self, obj):
        first_item = obj.items.first()
        return first_item.product_image if first_item else ''


class CreateOrderSerializer(serializers.Serializer):
    """建立訂單的輸入序列化器（驗證前端傳進來的資料）"""
    receiver_name = serializers.CharField(max_length=100)
    receiver_phone = serializers.CharField(max_length=20)
    shipping_city = serializers.CharField(max_length=20)
    shipping_district = serializers.CharField(max_length=20)
    shipping_address = serializers.CharField(max_length=255)
    payment_method = serializers.ChoiceField(choices=['cod', 'transfer', 'credit_card'])
    coupon_code = serializers.CharField(max_length=20, required=False, allow_blank=True, default='')
    note = serializers.CharField(required=False, allow_blank=True, default='')
    shipping_fee = serializers.IntegerField(min_value=0)
    items = serializers.ListField(child=serializers.DictField(), min_length=1)

    def validate_items(self, value):
        """驗證每個品項都有必要欄位"""
        for item in value:
            if 'product_id' not in item:
                raise serializers.ValidationError("每個品項必須包含 product_id")
            if 'quantity' not in item or item['quantity'] < 1:
                raise serializers.ValidationError("每個品項的數量必須 >= 1")
            # 確保有 item_type
            if 'item_type' not in item:
                item['item_type'] = 'product' # 若無提供，預設為葡萄
        return value

    @transaction.atomic
    def create(self, validated_data):
        """
        核心：建立訂單的完整流程
        使用 @transaction.atomic 確保「扣庫存」和「建訂單」要嘛全部成功，要嘛全部回滾
        """
        user = self.context['request'].user
        items_data = validated_data.pop('items')
        shipping_fee = validated_data.pop('shipping_fee')
        coupon_code = validated_data.pop('coupon_code', '')

        # 1. 遍歷所有品項，驗證庫存 & 計算金額
        order_items_to_create = []
        subtotal = 0

        for item_data in items_data:
            item_type = item_data.get('item_type', 'product')
            quantity = item_data['quantity']

            # 根據 item_type 去找對應的 Model
            if item_type == 'dessert':
                product_obj = Dessert.objects.select_for_update().get(id=item_data['product_id'])
            else:
                product_obj = Product.objects.select_for_update().get(id=item_data['product_id'])
            
            # 取得等級（如果有）
            grade = None
            grade_name = ''
            if item_data.get('grade_id'):
                if item_type == 'dessert':
                    grade = DessertGrade.objects.select_for_update().get(id=item_data['grade_id'], dessert=product_obj)
                else:
                    grade = ProductGrade.objects.select_for_update().get(id=item_data['grade_id'], product=product_obj)
                
                unit_price = grade.price
                grade_name = grade.name

                # 檢查等級庫存
                if grade.stock < quantity:
                    raise serializers.ValidationError(
                        f"「{product_obj.name} - {grade.name}」庫存不足（剩餘 {grade.stock} 件）"
                    )
            else:
                unit_price = product_obj.price
                # 檢查商品庫存
                if product_obj.stock < quantity:
                    raise serializers.ValidationError(
                        f"「{product_obj.name}」庫存不足（剩餘 {product_obj.stock} 件）"
                    )

            # 品種名稱快照
            variety_names = item_data.get('variety_names', '')

            # 商品圖片快照
            product_image = item_data.get('product_image', '')

            item_total = unit_price * quantity
            subtotal += item_total

            order_items_to_create.append({
                'item_type': item_type,
                'product': product_obj if item_type == 'product' else None,
                'dessert': product_obj if item_type == 'dessert' else None,
                'grade': grade,
                'product_name': product_obj.name,
                'grade_name': grade_name,
                'variety_names': variety_names,
                'product_image': product_image,
                'unit_price': unit_price,
                'quantity': quantity,
                'item_total': item_total,
            })

        # 2. 驗證並套用優惠券
        discount_amount = 0
        coupon = None
        if coupon_code:
            from .models import Coupon, UserCoupon
            try:
                coupon = Coupon.objects.select_for_update().get(code=coupon_code)
                is_valid, msg = coupon.is_valid(subtotal)
                if not is_valid:
                    raise serializers.ValidationError(f"優惠券無效：{msg}")
                if UserCoupon.objects.filter(user=user, coupon=coupon, is_used=True).exists():
                    raise serializers.ValidationError("您已經使用過此優惠代碼，無法重複使用。")
                discount_amount = coupon.calculate_discount(subtotal, shipping_fee)
            except Coupon.DoesNotExist:
                raise serializers.ValidationError("優惠代碼不存在")

        # 3. 建立訂單主表
        # total_amount = 商品小計 - 折抵 + 運費
        total_amount = subtotal - discount_amount + shipping_fee
        if total_amount < 0:
            total_amount = 0

        payment_method = validated_data['payment_method']

        # 根據付款方式決定初始訂單狀態
        # 貨到付款 → 直接「待出貨」（不需要先付款）
        # 銀行轉帳 → 「待付款」（等確認匯款）
        # 信用卡 → 「待付款」（付完款後自動變「待出貨」）
        if payment_method == 'cod':
            initial_status = 'pending_shipment'
            initial_payment = 'unpaid'  # 貨到才付
        elif payment_method == 'transfer':
            initial_status = 'pending_payment'
            initial_payment = 'unpaid'
        else:  # credit_card
            initial_status = 'pending_payment'
            initial_payment = 'unpaid'

        order = Order.objects.create(
            user=user,
            order_number=Order.generate_order_number(),
            receiver_name=validated_data['receiver_name'],
            receiver_phone=validated_data['receiver_phone'],
            shipping_city=validated_data['shipping_city'],
            shipping_district=validated_data['shipping_district'],
            shipping_address=validated_data['shipping_address'],
            payment_method=payment_method,
            note=validated_data.get('note', ''),
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            coupon_code=coupon_code,
            discount_amount=discount_amount,
            total_amount=total_amount,
            status=initial_status,
            payment_status=initial_payment,
        )

        # 4. 扣除優惠券使用次數
        if coupon:
            coupon.used_count += 1
            coupon.save()
            # 若為錢包內的優惠券，則標記為已使用並記錄關聯訂單
            # 若為錢包內的優惠券，或者是曾經用過的
            user_coupon = UserCoupon.objects.filter(user=user, coupon=coupon).first()
            from django.utils import timezone
            if user_coupon:
                user_coupon.is_used = True
                user_coupon.used_at = timezone.now()
                user_coupon.order = order
                user_coupon.save()
            else:
                # 若客人在結帳頁「手動輸入」了有效的代碼結帳，系統自動幫他把這張建檔成已使用的券，留下歷史痕跡
                UserCoupon.objects.create(
                    user=user,
                    coupon=coupon,
                    is_used=True,
                    used_at=timezone.now(),
                    order=order
                )

        # 5. 建立訂單品項 + 扣庫存
        for item_info in order_items_to_create:
            OrderItem.objects.create(
                order=order,
                item_type=item_info['item_type'],
                product=item_info['product'],
                dessert=item_info['dessert'],
                product_name=item_info['product_name'],
                grade_name=item_info['grade_name'],
                variety_names=item_info['variety_names'],
                product_image=item_info['product_image'],
                unit_price=item_info['unit_price'],
                quantity=item_info['quantity'],
                item_total=item_info['item_total'],
            )

            # 扣庫存
            if item_info['grade']:
                item_info['grade'].stock -= item_info['quantity']
                item_info['grade'].save()
            else:
                target_model = item_info['dessert'] if item_info['item_type'] == 'dessert' else item_info['product']
                if target_model:
                    target_model.stock -= item_info['quantity']
                    target_model.save()

        return order


# ========================================
# 甄點 Serializers
# ========================================

class DessertCategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = DessertCategory
        fields = ['id', 'name', 'image', 'description']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class DessertGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DessertGrade
        fields = ['id', 'name', 'count', 'price', 'stock']

class DessertImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DessertImage
        fields = ['id', 'image', 'order']

class DessertSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    grades = DessertGradeSerializer(many=True, read_only=True)
    images = DessertImageSerializer(many=True, read_only=True)

    class Meta:
        model = Dessert
        fields = ['id', 'category', 'category_name', 'name', 'flavor', 'price', 'image', 'images', 'description', 'stock', 'is_active', 'grades']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None