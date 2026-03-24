"""
測試資料工廠
每個 Factory 對應一個 Model，用來快速產生假資料。
使用方式：UserFactory() 就會自動建一筆使用者，所有必填欄位都幫你填好。
"""
import factory
from datetime import date
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


# ========================================
# 🔐 帳號相關
# ========================================

class UserFactory(factory.django.DjangoModelFactory):
    """快速產生測試用的使用者"""
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'testuser{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.PostGenerationMethodCall('set_password', 'test1234')
    level = '一般會員'


class UserAddressFactory(factory.django.DjangoModelFactory):
    """快速產生測試用的收件地址"""
    class Meta:
        model = 'accounts.UserAddress'

    user = factory.SubFactory(UserFactory)
    receiver_name = factory.Sequence(lambda n: f'收件人{n}')
    receiver_phone = '0912345678'
    city = '台北市'
    district = '大安區'
    detail_address = factory.Sequence(lambda n: f'測試路{n}號')
    is_default = False


# ========================================
# 🖼️ 網站內容 (輪播圖/素材)
# ========================================

class BannerFactory(factory.django.DjangoModelFactory):
    """快速產生輪播圖"""
    class Meta:
        model = 'store.Banner'

    title = factory.Sequence(lambda n: f'測試輪播圖{n}')
    image = 'banners/test.jpg'
    is_active = True
    order = 1


class SiteImageFactory(factory.django.DjangoModelFactory):
    """快速產生網站素材庫"""
    class Meta:
        model = 'store.SiteImage'

    key = factory.Sequence(lambda n: f'test_img_{n}')
    label = '素材標籤'
    image = 'site_images/test.jpg'
    description = '測試素材說明'


# ========================================
# 🍇 葡萄商品相關
# ========================================

class ProductCategoryFactory(factory.django.DjangoModelFactory):
    """快速產生商品分類"""
    class Meta:
        model = 'store.ProductCategory'

    name = factory.Sequence(lambda n: f'測試分類{n}')
    is_active = True


class VarietyFactory(factory.django.DjangoModelFactory):
    """快速產生葡萄品種"""
    class Meta:
        model = 'store.Variety'

    name = factory.Sequence(lambda n: f'測試品種{n}')
    color = '紫黑色'
    is_active = True
    origin = '台灣彰化'
    season = '6~8月'


class ProductFactory(factory.django.DjangoModelFactory):
    """快速產生葡萄禮盒商品"""
    class Meta:
        model = 'store.Product'

    category = factory.SubFactory(ProductCategoryFactory)
    name = factory.Sequence(lambda n: f'測試葡萄禮盒{n}')
    price = 1200
    stock = 50
    is_mixed = False
    mix_limit = 1
    unit_type = 'catty'
    unit_value = Decimal('4.0')


class ProductGradeFactory(factory.django.DjangoModelFactory):
    """快速產生商品規格/等級"""
    class Meta:
        model = 'store.ProductGrade'

    product = factory.SubFactory(ProductFactory)
    name = factory.Sequence(lambda n: f'測試等級{n}')
    price = 1500
    stock = 30


# ========================================
# 🍰 甜點相關
# ========================================

class DessertCategoryFactory(factory.django.DjangoModelFactory):
    """快速產生甜點分類"""
    class Meta:
        model = 'store.DessertCategory'

    name = factory.Sequence(lambda n: f'測試甜點分類{n}')
    is_active = True


class DessertFactory(factory.django.DjangoModelFactory):
    """快速產生甜點品項"""
    class Meta:
        model = 'store.Dessert'

    category = factory.SubFactory(DessertCategoryFactory)
    name = factory.Sequence(lambda n: f'測試甜點{n}')
    flavor = '草莓'
    price = 480
    stock = 100
    is_active = True


class DessertGradeFactory(factory.django.DjangoModelFactory):
    """快速產生甜點規格"""
    class Meta:
        model = 'store.DessertGrade'

    dessert = factory.SubFactory(DessertFactory)
    name = '6顆裝'
    count = 6
    price = 480
    stock = 20


# ========================================
# 🎟️ 優惠券相關
# ========================================

class CouponFactory(factory.django.DjangoModelFactory):
    """快速產生優惠券"""
    class Meta:
        model = 'store.Coupon'

    code = factory.Sequence(lambda n: f'TEST{n:04d}')
    title = factory.Sequence(lambda n: f'測試優惠券{n}')
    discount_type = 'fixed'
    discount_value = Decimal('100.00')
    min_spend = 500
    valid_from = factory.LazyFunction(lambda: timezone.now() - timezone.timedelta(days=1))
    valid_to = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=30))
    is_active = True
    usage_limit = 100
    used_count = 0


class ExpiredCouponFactory(CouponFactory):
    """已過期的優惠券（繼承自 CouponFactory，只改時間）"""
    code = factory.Sequence(lambda n: f'EXPIRED{n:04d}')
    valid_from = factory.LazyFunction(lambda: timezone.now() - timezone.timedelta(days=60))
    valid_to = factory.LazyFunction(lambda: timezone.now() - timezone.timedelta(days=1))


class UserCouponFactory(factory.django.DjangoModelFactory):
    """快速產生會員持有的優惠券"""
    class Meta:
        model = 'store.UserCoupon'

    user = factory.SubFactory(UserFactory)
    coupon = factory.SubFactory(CouponFactory)
    is_used = False


# ========================================
# 📦 訂單相關
# ========================================

class OrderFactory(factory.django.DjangoModelFactory):
    """快速產生訂單"""
    class Meta:
        model = 'store.Order'

    user = factory.SubFactory(UserFactory)
    order_number = factory.Sequence(lambda n: f'GS20260323{n:03d}')
    receiver_name = '測試收件人'
    receiver_phone = '0912345678'
    shipping_city = '台北市'
    shipping_district = '大安區'
    shipping_address = '測試路100號'
    subtotal = 2400
    shipping_fee = 0
    discount_amount = 0
    total_amount = 2400
    status = 'pending_payment'
    payment_method = 'credit_card'
    payment_status = 'unpaid'


class OrderItemFactory(factory.django.DjangoModelFactory):
    """快速產生訂單明細"""
    class Meta:
        model = 'store.OrderItem'

    order = factory.SubFactory(OrderFactory)
    item_type = 'product'
    product = factory.SubFactory(ProductFactory)
    product_name = factory.LazyAttribute(lambda obj: obj.product.name if obj.product else '測試商品')
    unit_price = 1200
    quantity = 2
    item_total = 2400


# ========================================
# 📰 最新消息
# ========================================

class NewsCategoryFactory(factory.django.DjangoModelFactory):
    """快速產生消息分類"""
    class Meta:
        model = 'store.NewsCategory'

    name = factory.Sequence(lambda n: f'消息分類{n}')


class NewsFactory(factory.django.DjangoModelFactory):
    """快速產生最新消息"""
    class Meta:
        model = 'store.News'

    category = factory.SubFactory(NewsCategoryFactory)
    title = factory.Sequence(lambda n: f'測試消息{n}')
    summary = '這是測試摘要'
    content = '這是測試內容'
    is_published = True
    published_date = factory.LazyFunction(date.today)


# ========================================
# 📢 公告
# ========================================

class BulletinFactory(factory.django.DjangoModelFactory):
    """快速產生首頁公告"""
    class Meta:
        model = 'store.Bulletin'

    title = factory.Sequence(lambda n: f'測試公告{n}')
    content = '這是測試公告內容'
    is_active = True
