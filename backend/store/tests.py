"""
🧪 田園葡萄 — 後端 API 測試
按照你的 API 端點，涵蓋：商品、甜點、訂單、優惠券、會員、地址
"""
import pytest
from decimal import Decimal
from django.utils import timezone
from rest_framework.test import APIClient
from store.factories import (
    UserFactory, UserAddressFactory,
    ProductFactory, ProductCategoryFactory, ProductGradeFactory, VarietyFactory,
    DessertFactory, DessertCategoryFactory, DessertGradeFactory,
    CouponFactory, ExpiredCouponFactory, UserCouponFactory,
    OrderFactory, OrderItemFactory,
    NewsFactory, NewsCategoryFactory,
    BulletinFactory,
    BannerFactory, SiteImageFactory,
)


# ===================================
# 🔧 共用的 fixture
# ===================================

@pytest.fixture
def api_client():
    """未登入的 API Client"""
    return APIClient()


@pytest.fixture
def auth_client():
    """已登入的 API Client（自動建一個使用者）"""
    user = UserFactory()
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user


# ===================================
# 🍇 商品 API 測試
# GET /api/products/
# GET /api/products/<id>/
# GET /api/products/categories/
# ===================================

@pytest.mark.django_db
class TestProductAPI:
    """葡萄禮盒商品相關 API"""

    def test_商品列表_不用登入就能看(self, api_client):
        ProductFactory()
        response = api_client.get('/api/products/')
        assert response.status_code == 200

    def test_商品列表_回傳正確筆數(self, api_client):
        ProductFactory.create_batch(5)
        response = api_client.get('/api/products/')
        assert response.status_code == 200
        assert len(response.data) == 5

    def test_商品列表_支援分類篩選(self, api_client):
        cat_a = ProductCategoryFactory(name='單品種禮盒')
        cat_b = ProductCategoryFactory(name='混搭禮盒')
        ProductFactory.create_batch(3, category=cat_a)
        ProductFactory.create_batch(2, category=cat_b)

        response = api_client.get(f'/api/products/?category={cat_a.id}')
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_商品詳情_存在的商品(self, api_client):
        product = ProductFactory()
        response = api_client.get(f'/api/products/{product.id}/')
        assert response.status_code == 200
        assert response.data['name'] == product.name

    def test_商品詳情_不存在回傳404(self, api_client):
        response = api_client.get('/api/products/99999/')
        assert response.status_code == 404

    def test_商品分類列表(self, api_client):
        ProductCategoryFactory.create_batch(3)
        response = api_client.get('/api/products/categories/')
        assert response.status_code == 200
        assert len(response.data) == 3


# ===================================
# 🍰 甜點 API 測試
# GET /api/desserts/
# GET /api/desserts/<id>/
# GET /api/desserts/categories/
# ===================================

@pytest.mark.django_db
class TestDessertAPI:
    """甜點相關 API"""

    def test_甜點列表_不用登入就能看(self, api_client):
        DessertFactory()
        response = api_client.get('/api/desserts/')
        assert response.status_code == 200

    def test_甜點列表_支援分類篩選(self, api_client):
        cat = DessertCategoryFactory(name='大福')
        DessertFactory.create_batch(2, category=cat)
        DessertFactory()  # 其他分類

        response = api_client.get(f'/api/desserts/?category={cat.id}')
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_甜點詳情(self, api_client):
        dessert = DessertFactory()
        response = api_client.get(f'/api/desserts/{dessert.id}/')
        assert response.status_code == 200
        assert response.data['name'] == dessert.name

    def test_甜點分類列表(self, api_client):
        DessertCategoryFactory.create_batch(2)
        response = api_client.get('/api/desserts/categories/')
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_已下架甜點_不出現在列表(self, api_client):
        DessertFactory(is_active=True)
        DessertFactory(is_active=False)
        response = api_client.get('/api/desserts/')
        assert response.status_code == 200
        assert len(response.data) == 1


# ===================================
# 📦 訂單 API 測試
# GET  /api/orders/
# POST /api/orders/
# GET  /api/orders/<order_number>/
# ===================================

@pytest.mark.django_db
class TestOrderAPI:
    """訂單相關 API"""

    def test_未登入_不能查看訂單(self, api_client):
        response = api_client.get('/api/orders/')
        assert response.status_code == 401

    def test_登入後_可以查看自己的訂單(self, auth_client):
        client, user = auth_client
        OrderFactory(user=user)

        response = client.get('/api/orders/')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_看不到別人的訂單(self, auth_client):
        client, user = auth_client
        other_user = UserFactory()
        OrderFactory(user=other_user)  # 別人的訂單

        response = client.get('/api/orders/')
        assert response.status_code == 200
        assert len(response.data) == 0  # 不應該看到

    def test_訂單詳情_自己的訂單(self, auth_client):
        client, user = auth_client
        order = OrderFactory(user=user)

        response = client.get(f'/api/orders/{order.order_number}/')
        assert response.status_code == 200
        assert response.data['order_number'] == order.order_number

    def test_訂單詳情_別人的訂單_被擋(self, auth_client):
        client, user = auth_client
        other_order = OrderFactory()  # 別人的訂單

        response = client.get(f'/api/orders/{other_order.order_number}/')
        assert response.status_code == 404  # get_object_or_404 會回 404

    def test_未登入_不能建立訂單(self, api_client):
        response = api_client.post('/api/orders/', {})
        assert response.status_code == 401


# ===================================
# 🎟️ 優惠券 API 測試
# POST /api/coupons/validate/
# GET  /api/coupons/my/
# POST /api/coupons/claim/
# ===================================

@pytest.mark.django_db
class TestCouponAPI:
    """優惠券相關 API"""

    # -- 驗證優惠券 --

    def test_驗證優惠券_未登入被擋(self, api_client):
        response = api_client.post('/api/coupons/validate/', {})
        assert response.status_code == 401

    def test_驗證優惠券_有效優惠碼(self, auth_client):
        client, user = auth_client
        coupon = CouponFactory(code='SAVE100', discount_value=Decimal('100'), min_spend=500)

        response = client.post('/api/coupons/validate/', {
            'coupon_code': 'SAVE100',
            'subtotal': 1000,
        })
        assert response.status_code == 200
        assert response.data['valid'] is True
        assert response.data['discount_amount'] == 100

    def test_驗證優惠券_不存在的優惠碼(self, auth_client):
        client, user = auth_client
        response = client.post('/api/coupons/validate/', {
            'coupon_code': 'FAKE999',
            'subtotal': 1000,
        })
        assert response.status_code == 400

    def test_驗證優惠券_已過期(self, auth_client):
        client, user = auth_client
        ExpiredCouponFactory(code='OLD100')

        response = client.post('/api/coupons/validate/', {
            'coupon_code': 'OLD100',
            'subtotal': 1000,
        })
        assert response.status_code == 400

    def test_驗證優惠券_未達最低消費(self, auth_client):
        client, user = auth_client
        CouponFactory(code='MIN500', min_spend=500)

        response = client.post('/api/coupons/validate/', {
            'coupon_code': 'MIN500',
            'subtotal': 200,  # 低於門檻
        })
        assert response.status_code == 400

    def test_驗證優惠券_空的優惠碼(self, auth_client):
        client, user = auth_client
        response = client.post('/api/coupons/validate/', {
            'coupon_code': '',
            'subtotal': 1000,
        })
        assert response.status_code == 400

    # -- 領取優惠券 --

    def test_領取優惠券_成功(self, auth_client):
        client, user = auth_client
        coupon = CouponFactory(code='WELCOME')

        response = client.post('/api/coupons/claim/', {
            'coupon_code': 'WELCOME',
        })
        assert response.status_code == 200
        assert response.data['success'] is True

    def test_領取優惠券_重複領取被擋(self, auth_client):
        client, user = auth_client
        coupon = CouponFactory(code='ONCE')
        UserCouponFactory(user=user, coupon=coupon)  # 已領過

        response = client.post('/api/coupons/claim/', {
            'coupon_code': 'ONCE',
        })
        assert response.status_code == 400

    def test_領取優惠券_已過期被擋(self, auth_client):
        client, user = auth_client
        ExpiredCouponFactory(code='OLDCOUPON')

        response = client.post('/api/coupons/claim/', {
            'coupon_code': 'OLDCOUPON',
        })
        assert response.status_code == 400

    # -- 我的優惠券 --

    def test_我的優惠券_未登入被擋(self, api_client):
        response = api_client.get('/api/coupons/my/')
        assert response.status_code == 401

    def test_我的優惠券_顯示自己的(self, auth_client):
        client, user = auth_client
        UserCouponFactory(user=user)
        UserCouponFactory(user=user)
        UserCouponFactory()  # 別人的

        response = client.get('/api/coupons/my/')
        assert response.status_code == 200
        assert len(response.data) == 2


# ===================================
# 👤 會員 API 測試
# GET/PUT /api/profile/
# POST    /api/register/
# POST    /api/token/
# ===================================

@pytest.mark.django_db
class TestAccountAPI:
    """會員帳號相關 API"""

    def test_個人資料_未登入被擋(self, api_client):
        response = api_client.get('/api/profile/')
        assert response.status_code == 401

    def test_個人資料_登入後可以看(self, auth_client):
        client, user = auth_client
        response = client.get('/api/profile/')
        assert response.status_code == 200
        assert response.data['email'] == user.email

    def test_註冊_成功(self, api_client):
        response = api_client.post('/api/register/', {
            'username': 'newuser1a',
            'email': 'new@test.com',
            'password': 'Strong1pass',
        })
        assert response.status_code == 201
        assert response.data['username'] == 'newuser1a'

    def test_註冊_密碼不符合規則(self, api_client):
        response = api_client.post('/api/register/', {
            'username': 'baduser1a',
            'email': 'bad@test.com',
            'password': 'weakpass',  # 沒有大寫和數字
        })
        assert response.status_code == 400

    def test_註冊_重複的username(self, api_client):
        UserFactory(username='takenuser1')
        response = api_client.post('/api/register/', {
            'username': 'takenuser1',
            'email': 'new2@test.com',
            'password': 'Strong1pass',
        })
        assert response.status_code == 400

    def test_JWT登入_正確帳密(self, api_client):
        UserFactory(username='logintest')
        response = api_client.post('/api/token/', {
            'username': 'logintest',
            'password': 'test1234',  # UserFactory 預設密碼
        })
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_JWT登入_錯誤密碼(self, api_client):
        UserFactory(username='logintest2')
        response = api_client.post('/api/token/', {
            'username': 'logintest2',
            'password': 'wrongpassword',
        })
        assert response.status_code == 401


# ===================================
# 📬 會員地址簿 API 測試
# GET  /api/address/
# POST /api/address/
# PUT  /api/address/<id>/
# DELETE /api/address/<id>/
# ===================================

@pytest.mark.django_db
class TestAddressAPI:
    """會員地址簿 API"""

    def test_地址列表_未登入被擋(self, api_client):
        response = api_client.get('/api/address/')
        assert response.status_code == 401

    def test_地址列表_只看到自己的(self, auth_client):
        client, user = auth_client
        UserAddressFactory(user=user)
        UserAddressFactory(user=user)
        UserAddressFactory()  # 別人的地址

        response = client.get('/api/address/')
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_新增地址(self, auth_client):
        client, user = auth_client
        response = client.post('/api/address/', {
            'receiver_name': '王小明',
            'receiver_phone': '0987654321',
            'city': '台中市',
            'district': '西區',
            'detail_address': '測試街1號',
            'is_default': True,
        })
        assert response.status_code == 201

    def test_刪除地址(self, auth_client):
        client, user = auth_client
        addr = UserAddressFactory(user=user)

        response = client.delete(f'/api/address/{addr.id}/')
        assert response.status_code == 204


# ===================================
# 📰 最新消息 API 測試
# GET /api/news/
# GET /api/news/categories/
# GET /api/news/<id>/
# ===================================

@pytest.mark.django_db
class TestNewsAPI:
    """最新消息 API"""

    def test_消息列表_不用登入(self, api_client):
        NewsFactory.create_batch(3)
        response = api_client.get('/api/news/')
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_消息列表_未發佈的不顯示(self, api_client):
        NewsFactory(is_published=True)
        NewsFactory(is_published=False)
        response = api_client.get('/api/news/')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_消息詳情(self, api_client):
        news = NewsFactory()
        response = api_client.get(f'/api/news/{news.id}/')
        assert response.status_code == 200
        assert response.data['title'] == news.title

    def test_消息分類列表(self, api_client):
        NewsCategoryFactory.create_batch(2)
        response = api_client.get('/api/news/categories/')
        assert response.status_code == 200
        assert len(response.data) == 2


# ===================================
# 📢 公告 API 測試
# GET /api/bulletins/
# ===================================

@pytest.mark.django_db
class TestBulletinAPI:
    """首頁公告 API"""

    def test_公告列表_不用登入(self, api_client):
        BulletinFactory.create_batch(2)
        response = api_client.get('/api/bulletins/')
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_已停用公告_不顯示(self, api_client):
        BulletinFactory(is_active=True)
        BulletinFactory(is_active=False)
        response = api_client.get('/api/bulletins/')
        assert response.status_code == 200
        assert len(response.data) == 1


# ===================================
# 🍇 品種介紹 API 測試
# GET /api/varieties/
# ===================================

@pytest.mark.django_db
class TestVarietyAPI:
    """品種介紹 API"""

    def test_品種列表_不用登入(self, api_client):
        VarietyFactory.create_batch(4)
        response = api_client.get('/api/varieties/')
        assert response.status_code == 200
        assert len(response.data) == 4


# ===================================
# 🎫 優惠券 Model 邏輯測試（不經過 API）
# ===================================

@pytest.mark.django_db
class TestCouponModel:
    """直接測試 Coupon Model 的 is_valid 和 calculate_discount"""

    def test_有效優惠券(self):
        coupon = CouponFactory(min_spend=500)
        is_valid, msg = coupon.is_valid(order_subtotal=1000)
        assert is_valid is True

    def test_過期優惠券(self):
        coupon = ExpiredCouponFactory()
        is_valid, msg = coupon.is_valid(order_subtotal=1000)
        assert is_valid is False
        assert '過期' in msg

    def test_未達最低消費(self):
        coupon = CouponFactory(min_spend=1000)
        is_valid, msg = coupon.is_valid(order_subtotal=500)
        assert is_valid is False
        assert '門檻' in msg

    def test_使用次數已滿(self):
        coupon = CouponFactory(usage_limit=10, used_count=10)
        is_valid, msg = coupon.is_valid(order_subtotal=1000)
        assert is_valid is False
        assert '兌換完畢' in msg

    def test_已停用(self):
        coupon = CouponFactory(is_active=False)
        is_valid, msg = coupon.is_valid(order_subtotal=1000)
        assert is_valid is False
        assert '停用' in msg

    def test_固定金額折扣計算(self):
        coupon = CouponFactory(discount_type='fixed', discount_value=Decimal('200'))
        discount = coupon.calculate_discount(subtotal=1000)
        assert discount == 200

    def test_固定金額不超過商品金額(self):
        coupon = CouponFactory(discount_type='fixed', discount_value=Decimal('500'))
        discount = coupon.calculate_discount(subtotal=300)
        assert discount == 300  # 不會折超過商品價

    def test_免運費折扣(self):
        coupon = CouponFactory(discount_type='free_shipping', discount_value=Decimal('0'))
        discount = coupon.calculate_discount(subtotal=1000, shipping_fee=120)
        assert discount == 120  # 應該折抵全部運費

# ===================================
# 🖼️ 網站內容 API (輪播圖/素材)
# ===================================
@pytest.mark.django_db
class TestSiteContentAPI:
    def test_輪播圖列表_不用登入_且只顯示啟用(self, api_client):
        BannerFactory(title='輪播1', is_active=True, order=1)
        BannerFactory(title='輪播2', is_active=False)  # 應該不顯示
        
        response = api_client.get('/api/banners/')
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['title'] == '輪播1'

    def test_網站素材列表_不用登入(self, api_client):
        SiteImageFactory(key='logo', label='Logo')
        SiteImageFactory(key='footer_img', label='Footer')
        
        response = api_client.get('/api/site-images/')
        assert response.status_code == 200
        assert len(response.data) == 2
