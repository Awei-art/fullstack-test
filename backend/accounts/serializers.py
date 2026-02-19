from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    使用者資料序列化器
    作用：把 Python 物件轉成 JSON（前端看得懂的格式）
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'level', 'phone', 'date_joined', 'last_login']
        # 不要回傳 password！



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
    
    def validate_username(self, value):
        """
        檢查帳號是否已存在
        """
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