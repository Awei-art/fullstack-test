from django import forms
from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserLoginRecord, UserAddress

# 動態產生 12 個月與 31 天的選項
MONTH_CHOICES = [('', '選擇月份')] + [(f"{i:02d}", f"{i} 月") for i in range(1, 13)]
DAY_CHOICES = [('', '選擇日期')] + [(f"{i:02d}", f"{i} 日") for i in range(1, 32)]

class CustomUserForm(forms.ModelForm):
    """
    客製化管理員後台的編輯表單，在這裡將生日轉換為兩個獨立下拉選單的體驗
    """
    # 我們在後台介面上拆成兩個獨立的選單欄位，但不把它們存進資料庫，只用來做畫面顯示
    display_birth_month = forms.ChoiceField(choices=MONTH_CHOICES, required=False, label="出生月份")
    display_birth_day = forms.ChoiceField(choices=DAY_CHOICES, required=False, label="出生日期")

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 載入資料時：把資料庫裡的 '0223' 切割開來，分別塞進兩個選單裡
        if self.instance and self.instance.birth_month_day and len(self.instance.birth_month_day) == 4:
            self.fields['display_birth_month'].initial = self.instance.birth_month_day[:2]
            self.fields['display_birth_day'].initial = self.instance.birth_month_day[2:]

    def clean(self):
        cleaned_data = super().clean()
        month = cleaned_data.get('display_birth_month')
        day = cleaned_data.get('display_birth_day')
        
        # 存檔時：把兩個選單的值合併回 '0223'，塞回真實的資料庫欄位
        if month and day:
            cleaned_data['birth_month_day'] = f"{month}{day}"
        elif not month and not day:
             cleaned_data['birth_month_day'] = ""
            
        return cleaned_data

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 讓 UserAdmin 使用我們的客製化表單
    form = CustomUserForm
    
    # 列表上顯示的欄位（讓您一眼看出重點資料）
    list_display = ('username', 'email', 'nickname', 'level', 'accept_promotions', 'is_staff')
    
    # 提供搜尋的欄位（客服找人超方便）
    search_fields = ('username', 'email', 'nickname', 'phone')
    
    # 右側的過濾器（行銷人員要發信，可以立刻篩選 accept_promotions=Yes）
    list_filter = ('level', 'accept_promotions', 'gender', 'is_staff', 'is_superuser', 'is_active')
    
    # 點進單一會員時，資料的群組排版
    fieldsets = UserAdmin.fieldsets + (
        ('🍇 田原葡萄 - 會員基本資料', {
            'fields': (
                'nickname', 
                'gender', 
                ('display_birth_month', 'display_birth_day'), # 讓這兩個選單並排顯示
                'level', 
                'phone', 
                'accept_promotions', 
                'avatar',
                'line_id',
                'google_id'
            ),
        }),
    )
    
    # 動態設定唯讀欄位 (Read-Only)
    def get_readonly_fields(self, request, obj=None):
        # 若 obj 存在，代表這是「修改既有會員」的狀態（而不是在新增一位全新的會員）
        if obj:
            # 我們強制把關乎他能不能順利登入的這三把鎖（帳號、LINE、Google ID），以及重要日期紀錄，徹底鎖起來不給改
            return self.readonly_fields + ('username', 'line_id', 'google_id', 'last_login', 'date_joined')
        return self.readonly_fields

@admin.register(UserLoginRecord)
class UserLoginRecordAdmin(admin.ModelAdmin):
    # 登入紀錄列表
    list_display = ('user', 'login_time', 'ip_address', 'location')
    list_filter = ('login_time',)
    search_fields = ('user__username', 'ip_address', 'location')
    # 為了安全性，登入紀錄通常是只讀的
    readonly_fields = ('user', 'login_time', 'ip_address', 'location', 'device_info')

@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    # 地址簿在後台列表的顯示方式
    list_display = ('user', 'title', 'receiver_name', 'receiver_phone', 'city', 'district', 'is_default')
    
    # 過濾條件（行銷可能想找特定縣市的客人）
    list_filter = ('is_default', 'city', 'district')
    
    # 搜尋框（可以搜尋客人帳號、收件人姓名或是電話）
    search_fields = ('user__username', 'receiver_name', 'receiver_phone', 'detail_address')
    
    # 預設地址打頭陣
    ordering = ('-is_default',)
