#AbstractUser: Django 內建的使用者模型基底類別
#已經包含：username、email、password、first_name、last_name、is_active、date_joined、last_login 等
from django.contrib.auth.models import AbstractUser

#自訂使用者模型
from django.db import models

# ========================================
# 會員系統
# ========================================
class User(AbstractUser):
    """
    自訂使用者模型
    繼承 Django 內建的 AbstractUser（已包含 username, email, password 等）
    """
    # 額外欄位
    level = models.CharField(max_length=20, default='一般會員')
    phone = models.CharField(max_length=20, blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name="暱稱")
    
    GENDER_CHOICES = [
        ('M', '男性'),
        ('F', '女性'),
        ('O', '保密')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O', verbose_name="稱謂")
    birth_month_day = models.CharField(max_length=4, blank=True, null=True, verbose_name="出生月日")
    accept_promotions = models.BooleanField(default=True, verbose_name="接受優惠通知")
    
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

class UserAddress(models.Model):
    """
    會員地址簿 (一對多：一個會員可以有多個地址)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name="所屬會員")
    title = models.CharField(max_length=50, blank=True, null=True, verbose_name="地址標籤", help_text="例如：公司、住家、公婆家")
    receiver_name = models.CharField(max_length=100, verbose_name="收件人姓名")
    receiver_phone = models.CharField(max_length=20, verbose_name="收件人聯絡電話")
    
    # 台灣地址通常分為：縣市、鄉鎮市區、詳細地址
    city = models.CharField(max_length=20, verbose_name="縣市")
    district = models.CharField(max_length=20, verbose_name="鄉鎮市區")
    detail_address = models.CharField(max_length=255, verbose_name="詳細地址")
    
    is_default = models.BooleanField(default=False, verbose_name="設為預設收件地址")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最後修改時間")

    class Meta:
        # 排序：預設地址永遠排最上面，其次是最近修改的
        ordering = ['-is_default', '-updated_at']
        verbose_name = "收件地址"
        verbose_name_plural = "會員地址簿"

    def __str__(self):
        label = f"[{self.title}] " if self.title else ""
        return f"{self.user.username} - {label}{self.receiver_name} ({self.city}{self.district})"

    def save(self, *args, **kwargs):
        # 【防呆機制】如果這筆地址被設為「預設」，系統自動去把這位客人的「其他所有地址」的預設取消掉
        # 確保一位客人永遠只會有一個預設地址！
        if self.is_default:
            UserAddress.objects.filter(user=self.user).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)