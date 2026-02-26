from rest_framework import serializers
import re
from .models import User, UserLoginRecord

class UserLoginRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLoginRecord
        fields = ['login_time', 'ip_address', 'device_info', 'location']

class UserSerializer(serializers.ModelSerializer):
    """
    使用者資料序列化器
    作用：把 Python 物件轉成 JSON（前端看得懂的格式）
    """
    recent_logins = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'avatar', 'level', 'phone', 'date_joined', 'last_login', 'recent_logins']
        # 不要回傳 password！
    
    def get_recent_logins(self, obj):
        # 取得最近 3 筆登入紀錄
        records = obj.login_records.all()[:3]
        return UserLoginRecordSerializer(records, many=True).data



#建立註冊序列化器
class RegisterSerializer(serializers.ModelSerializer):
    """
    註冊序列化器
    """
    password = serializers.CharField(
        write_only=True,  # 不會在回應中顯示
        min_length=8,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('密碼必須至少 8 碼')
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError('密碼必須包含至少 1 個大寫英文字母')
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError('密碼必須包含至少 1 個小寫英文字母')
        if not re.search(r'\d', value):
            raise serializers.ValidationError('密碼必須包含至少 1 個數字')
        return value
    
    def validate_username(self, value):
        """
        檢查帳號是否已存在及格式是否正確
        """
        if len(value) < 8:
            raise serializers.ValidationError('帳號必須至少 8 碼')
        # 確保至少有一種英文字母（大小寫皆可）以及至少一個數字，並且全部只有英數字
        if not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]+$', value):
            raise serializers.ValidationError('帳號必須包含英文與數字混合，且不可包含特殊符號')
        
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('此帳號已被使用')
        return value
    
    def validate_email(self, value):
        """
        檢查 Email 是否已存在
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('此 Email 已被註冊')
        return value
    
    def create(self, validated_data):
        """
        建立新使用者
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user