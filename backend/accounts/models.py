#AbstractUser: Django 內建的使用者模型基底類別
#已經包含：username、email、password、first_name、last_name、is_active、date_joined、last_login 等
from django.contrib.auth.models import AbstractUser

#自訂使用者模型
from django.db import models

class User(AbstractUser):
    """
    自訂使用者模型
    繼承 Django 內建的 AbstractUser（已包含 username, email, password 等）
    """
    # 額外欄位
    level = models.CharField(max_length=20, default='一般會員')
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.username