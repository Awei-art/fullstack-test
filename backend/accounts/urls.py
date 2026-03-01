from django.urls import path
from .views import (
    UserProfileView, RegisterView, LineLoginView, GoogleLoginView, 
    ForgotPasswordView, ResetPasswordView, ChangePasswordView,
    UserAddressListView, UserAddressDetailView
)

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('auth/line/', LineLoginView.as_view(), name='line-login'),
    path('auth/google/', GoogleLoginView.as_view(), name='google-login'),
    path('auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('auth/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('auth/password/change/', ChangePasswordView.as_view(), name='change-password'),
    
    # 會員地址簿
    path('address/', UserAddressListView.as_view(), name='user-address-list'),
    path('address/<int:pk>/', UserAddressDetailView.as_view(), name='user-address-detail'),
]