from django.urls import path
from .views import UserProfileView, RegisterView  # ← 加上 RegisterView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('register/', RegisterView.as_view(), name='register'),
]