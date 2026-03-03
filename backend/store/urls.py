from django.urls import path
from . import views
from .views import (
    OrderListCreateView, OrderDetailView,
    ECPayRepayView, ECPayNotifyView, ECPayResultView, ECPayReturnView,
    ValidateCouponView, UserCouponListView, ClaimCouponView,
    BulletinListAPIView
)

urlpatterns = [
    # 公告 API
    path('bulletins/', BulletinListAPIView.as_view(), name='bulletin-list'),

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