from django.urls import path
from . import views
from .views import (
    OrderListCreateView, OrderDetailView,
    ECPayRepayView, ECPayNotifyView, ECPayResultView, ECPayReturnView,
    ValidateCouponView, UserCouponListView, ClaimCouponView,
    BulletinListAPIView,
    NewsCategoryListView, NewsListView, NewsDetailView,
    VarietyListView,
    DessertCategoryListView, DessertListView, DessertDetailView,
    ProductCategoryListView, BannerListView
)

urlpatterns = [
    # 首頁輪播圖 API
    path('banners/', BannerListView.as_view(), name='banner-list'),
    # 公告 API
    path('bulletins/', BulletinListAPIView.as_view(), name='bulletin-list'),

    # 最新消息 API
    path('news/categories/', NewsCategoryListView.as_view(), name='news-category-list'),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),

    # 品種介紹 API
    path('varieties/', VarietyListView.as_view(), name='variety-list'),

    # 甄點 API
    path('desserts/categories/', DessertCategoryListView.as_view(), name='dessert-category-list'),
    path('desserts/', DessertListView.as_view(), name='dessert-list'),
    path('desserts/<int:pk>/', DessertDetailView.as_view(), name='dessert-detail'),

    # 商品分類 API
    path('products/categories/', ProductCategoryListView.as_view(), name='product-category-list'),
    path('products/', views.get_products, name='get_products'),

    # 單一商品詳情
    # <str:pk> 代表網址後面接的 ID (例如 products/1/)
    path('products/<str:pk>/', views.get_product, name="product"),

    # 訂單 API
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<str:order_number>/', OrderDetailView.as_view(), name='order-detail'),

    # ECPay 金流
    path('payment/repay/<str:order_number>/', ECPayRepayView.as_view(), name='ecpay-repay'),   # 重新付款
    path('payment/notify/', ECPayNotifyView.as_view(), name='ecpay-notify'),      # Webhook (ECPay 主動通知)
    path('payment/result/', ECPayResultView.as_view(), name='ecpay-result'),      # 付款完頁面跳轉中轉
    path('payment/return/<str:order_number>/', ECPayReturnView.as_view(), name='ecpay-return'),  # 查詢付款狀態

    # 優惠券 API
    path('coupons/validate/', ValidateCouponView.as_view(), name='coupon-validate'),
    path('coupons/my/', UserCouponListView.as_view(), name='my-coupons'),
    path('coupons/claim/', ClaimCouponView.as_view(), name='claim-coupon'),
]