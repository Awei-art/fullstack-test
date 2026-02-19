from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.get_products, name='get_products'),

    # 單一商品詳情
    # <str:pk> 代表網址後面接的 ID (例如 products/1/)
    path('products/<str:pk>/', views.get_product, name="product"),
]