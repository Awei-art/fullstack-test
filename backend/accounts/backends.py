from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameModelBackend:
    """
    允許客戶在「帳號」輸入框，自由輸入 Email 或是 Username 來登入
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('username')
            
        try:
            # 同時核對資料庫的 username 與 email 欄位
            user = User.objects.get(Q(username=username) | Q(email=username))
            # 核對密碼
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
            
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
