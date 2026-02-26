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
    line_id = models.CharField(max_length=255, unique=True, blank=True, null=True, verbose_name="LINE ID")
    google_id = models.CharField(max_length=255, unique=True, blank=True, null=True, verbose_name="Google ID")
    avatar = models.URLField(max_length=500, blank=True, null=True, verbose_name="大頭貼URL")
    
    def __str__(self):
        return self.username

class UserLoginRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_records', verbose_name="使用者")
    login_time = models.DateTimeField(auto_now_add=True, verbose_name="登入時間")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP位址")
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name="登入地點")
    device_info = models.CharField(max_length=255, null=True, blank=True, verbose_name="裝置資訊")

    class Meta:
        ordering = ['-login_time']
        verbose_name = "登入紀錄"
        verbose_name_plural = "登入紀錄"

    def __str__(self):
        return f"{self.user.username} 於 {self.login_time} 登入"