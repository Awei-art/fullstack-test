from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated#權限檢查，要求必須登入
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from .serializers import UserSerializer, RegisterSerializer, UserProfileUpdateSerializer, UserAddressSerializer
from .models import User, UserLoginRecord, UserAddress
from django.db import models
from django.contrib.auth.models import update_last_login
from rest_framework import generics

#建立個人資料視圖
class UserProfileView(APIView):#建立一個 API 視圖類別
    """
    取得登入使用者的個人資料
    GET /api/profile/
    """
    # 要求必須登入（有 Token）才能存取
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # request.user 是登入的使用者（由 JWT 自動解析）
        serializer = UserSerializer(request.user)#把 User 物件轉成 JSON
        return Response(serializer.data)#回傳 JSON 給前端

    def put(self, request):
        """
        更新個人資料（只允許安全欄位這部分由 serializer 控制）
        """
        serializer = UserProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # 儲存後回傳最新的完整資料
            return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import requests

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

def get_location_from_ip(ip):
    if not ip or ip == '127.0.0.1' or ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.'):
        return 'Taiwan Taipei (內部網路)'
    
    try:
        res = requests.get(f'http://ip-api.com/json/{ip}?lang=zh-TW', timeout=2)
        if res.status_code == 200:
            data = res.json()
            if data.get('status') == 'success':
                country = data.get('country', '')
                city = data.get('city', '')
                if country or city:
                    return f"{country} {city}".strip()
    except Exception:
        pass
    return '未知地點'

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    自訂 JWT 登入 API，登入成功時寫入 UserLoginRecord
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            username = request.data.get('username')
            if username:
                try:
                    user = User.objects.get(username=username)
                    ip = get_client_ip(request)
                    location = get_location_from_ip(ip)
                    UserLoginRecord.objects.create(
                        user=user,
                        ip_address=ip,
                        location=location,
                        device_info=request.META.get('HTTP_USER_AGENT')
                    )
                    # 更新最後登入時間
                    update_last_login(None, user)
                except User.DoesNotExist:
                    pass
        return response



#建立註冊視圖
class RegisterView(APIView):
    """
    註冊 API
    POST /api/register/
    """
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': '註冊成功',
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import requests
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class LineLoginView(APIView):
    """
    LINE 登入/註冊 API
    POST /api/auth/line/
    """
    def post(self, request):
        code = request.data.get('code')
        redirect_uri = request.data.get('redirect_uri', settings.LINE_CALLBACK_URL)
        if not code:
            return Response({'error': '缺少授權碼'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. 拿 authorization code 去向 LINE 換取 access token
        token_url = "https://api.line.me/oauth2/v2.1/token"
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': settings.LINE_CHANNEL_ID,
            'client_secret': settings.LINE_CHANNEL_SECRET,
        }
        token_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        token_res = requests.post(token_url, data=token_data, headers=token_headers)
        
        if token_res.status_code != 200:
            return Response({'error': '無法取得 LINE Token', 'details': token_res.json()}, status=status.HTTP_400_BAD_REQUEST)

        line_access_token = token_res.json().get('access_token')

        # 2. 拿 access token 去向 LINE 取得用戶資料 (User Profile)
        profile_url = "https://api.line.me/v2/profile"
        profile_headers = {'Authorization': f'Bearer {line_access_token}'}
        profile_res = requests.get(profile_url, headers=profile_headers)

        if profile_res.status_code != 200:
            return Response({'error': '無法取得 LINE 用戶資料'}, status=status.HTTP_400_BAD_REQUEST)

        profile_data = profile_res.json()
        line_id = profile_data.get('userId')
        display_name = profile_data.get('displayName')
        picture_url = profile_data.get('pictureUrl')

        # LINE 的 Email 需要特殊請求與審查，若有取得，就在這裡抓
        email = profile_data.get('email')

        if not line_id:
            return Response({'error': '無法取得有效的 LINE ID'}, status=status.HTTP_400_BAD_REQUEST)

        # 3. 尋找或建立該使用者
        # 先以 line_id 找，若找不到但有 email，則看 email 有沒有重複（合併帳號）
        try:
            if email:
                user = User.objects.filter(models.Q(line_id=line_id) | models.Q(email=email)).first()
            else:
                user = User.objects.filter(line_id=line_id).first()

            if user:
                # 既然登入了，順便更新使用者的 LINE 姓名與頭貼保持最新
                user.line_id = line_id
                user.first_name = display_name or user.first_name
                user.avatar = picture_url or user.avatar
                user.save()
            else:
                import secrets
                # 建立新使用者
                base_username = email.split('@')[0] if email else f'line_{line_id}'
                username = f"{base_username}_{secrets.token_hex(4)}"
                user = User.objects.create_user(
                    username=username,
                    email=email or '',
                    password=secrets.token_urlsafe(16),  # 隨機密碼
                )
                user.line_id = line_id
                user.first_name = display_name or ''
                user.avatar = picture_url
                user.save()
        except Exception as e:
            return Response({'error': '建立使用者失敗', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 4. 手動幫這名使用者產生 JWT Token
        refresh = RefreshToken.for_user(user)

        # 更新最後登入時間
        update_last_login(None, user)

        # 寫入登入紀錄
        ip = get_client_ip(request)
        location = get_location_from_ip(ip)
        UserLoginRecord.objects.create(
            user=user,
            ip_address=ip,
            location=location,
            device_info=request.META.get('HTTP_USER_AGENT')
        )

        return Response({
            'message': '登入成功',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username,
            'name': user.first_name,
            'avatar': user.avatar,
        }, status=status.HTTP_200_OK)


# ========================================
# Google 登入 API
# ========================================
class GoogleLoginView(APIView):
    """
    Google 登入 API
    POST /api/auth/google/
    """
    def post(self, request):
        code = request.data.get('code')
        redirect_uri = request.data.get('redirect_uri', settings.GOOGLE_CALLBACK_URL)
        if not code:
            return Response({'error': '缺少授權碼'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. 換取 access token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
        }
        token_res = requests.post(token_url, data=token_data)
        
        if token_res.status_code != 200:
            return Response({'error': '無法取得 Google Token', 'details': token_res.json()}, status=status.HTTP_400_BAD_REQUEST)

        google_access_token = token_res.json().get('access_token')

        # 2. 取得用戶資料
        profile_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        profile_headers = {'Authorization': f'Bearer {google_access_token}'}
        profile_res = requests.get(profile_url, headers=profile_headers)

        if profile_res.status_code != 200:
            return Response({'error': '無法取得 Google 用戶資料'}, status=status.HTTP_400_BAD_REQUEST)

        profile_data = profile_res.json()
        google_id = profile_data.get('id')
        email = profile_data.get('email')
        name = profile_data.get('name')
        picture = profile_data.get('picture')

        if not google_id or not email:
            return Response({'error': '無法取得有效的 Google 帳號資訊'}, status=status.HTTP_400_BAD_REQUEST)

        # 3. 尋找或建立使用者
        try:
            # 優先用 google_id 找，再來用 email 找，確保相同信箱只會有一個帳號
            user = User.objects.filter(models.Q(google_id=google_id) | models.Q(email=email)).first()
            if user:
                user.google_id = google_id
                user.first_name = name or user.first_name
                user.avatar = picture or user.avatar
                user.save()
            else:
                import secrets
                # 如果都找不到，建立新帳號
                base_username = email.split('@')[0]
                username = f"google_{base_username}_{secrets.token_hex(4)}"
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=secrets.token_urlsafe(16),
                )
                user.google_id = google_id
                user.first_name = name or ''
                user.avatar = picture
                user.save()
        except Exception as e:
            return Response({'error': '建立使用者失敗', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 4. 手動幫這名使用者產生 JWT Token
        refresh = RefreshToken.for_user(user)

        # 更新最後登入時間
        update_last_login(None, user)

        # 寫入登入紀錄
        ip = get_client_ip(request)
        location = get_location_from_ip(ip)
        UserLoginRecord.objects.create(
            user=user,
            ip_address=ip,
            location=location,
            device_info=request.META.get('HTTP_USER_AGENT')
        )

        return Response({
            'message': '登入成功',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username,
            'name': user.first_name,
            'avatar': user.avatar,
        }, status=status.HTTP_200_OK)


# ========================================
# 忘記密碼 API
# ========================================
class ForgotPasswordView(APIView):
    """
    忘記密碼 API (向信箱寄發重設連結)
    POST /api/auth/forgot-password/
    """
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': '請提供 Email 信箱'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email).first()
        if user:
            # 產生此人專屬的、限時有效的一回性安全解鎖鑰匙 (Token) 與經過安全編碼的 ID (Uid)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            # 使用前端網頁重設密碼的入口點
            # 改由環境變數傳入正式網域以支援 Vercel 與 localhost
            front_url = settings.FRONTEND_URL.rstrip('/')
            reset_link = f"{front_url}/reset-password?uid={uid}&token={token}"
            
            # 寄送重設信件給客人
            subject = '【田園葡萄】密碼重設通知'
            message = f"親愛的 {user.first_name or user.username} 您好：\n\n系統收到了您的密碼重設請求。\n\n請點擊以下專屬安全連結重設您的密碼（此連結基於安全考量，數日內即將失效）：\n{reset_link}\n\n如果您並未提出此請求，請忽略本信件您的帳號仍是安全的。\n\n田園葡萄 團隊敬上"
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"SMTP 發信引擎寄信失敗: {e}")
                
        # 資安防護最高原則：即使他亂拆黑客測試不存在的 Email，系統絕對不告訴他到底有沒有這個人
        # 故無論信箱正不正確，永遠回傳 OK 等待對方去信箱看
        return Response({'message': '重設密碼信件已寄出（若您輸入的信箱註冊過本網站的話）'}, status=status.HTTP_200_OK)


# ========================================
# 重設密碼 API
# ========================================
class ResetPasswordView(APIView):
    """
    重設密碼驗證 API (核對鑰匙並真正改寫密碼)
    POST /api/auth/reset-password/
    """
    def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('password')
        
        if not all([uidb64, token, new_password]):
            return Response({'error': '資料不完整，無法執行重設作業'}, status=status.HTTP_400_BAD_REQUEST)
            
        # 驗證新密碼強度
        if len(new_password) < 8:
            return Response({'error': '密碼必須至少 8 碼'}, status=status.HTTP_400_BAD_REQUEST)
        import re
        if not re.search(r'[A-Z]', new_password):
            return Response({'error': '密碼必須包含至少 1 個大寫英文字母'}, status=status.HTTP_400_BAD_REQUEST)
        if not re.search(r'[a-z]', new_password):
            return Response({'error': '密碼必須包含至少 1 個小寫英文字母'}, status=status.HTTP_400_BAD_REQUEST)
        if not re.search(r'\d', new_password):
            return Response({'error': '密碼必須包含至少 1 個數字'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # 嘗試解碼 ID 並找到這位客人
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': '連結已嚴重失效或是偽造的'}, status=status.HTTP_400_BAD_REQUEST)
            
        # 最後關卡：請 Django 內建的安全檢查機制核對這把 Token 鑰匙是否有效、有沒有過期、是否被用過
        if default_token_generator.check_token(user, token):
            # 恭喜，鑰匙正確！幫他換上新密碼
            user.set_password(new_password)
            user.save()
            return Response({'message': '密碼已成功重設！馬上就可以用新密碼登入了。'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': '這組重設連結已經過期，或者您已經使用它重設過密碼了。請重新發送忘記密碼。'}, status=status.HTTP_400_BAD_REQUEST)

class UserAddressListView(generics.ListCreateAPIView):
    """
    獲取使用者的所有地址 (GET) 或是 新增一筆地址 (POST)
    """
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 只能拿到「自己的」地址
        return UserAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 建立地址時，強制綁定目前登入的 user
        # 並檢查如果他是第一筆地址，自動設為預設
        is_first = UserAddress.objects.filter(user=self.request.user).count() == 0
        is_default = self.request.data.get('is_default', False)
        serializer.save(user=self.request.user, is_default=is_default or is_first)

class UserAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    獲取 (GET)、更新 (PUT)、或刪除 (DELETE) 某一筆特定地址
    """
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
        
    def perform_update(self, serializer):
        # 修改地址的處理
        serializer.save()


# ========================================
# 修改密碼 API
# ========================================
class ChangePasswordView(APIView):
    """
    登入會員獨立的修改密碼頁面專用 API
    POST /api/auth/password/change/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        
        # 1. 如果這位客人是 LINE / Google 登入且從來沒有設過密碼
        if not user.has_usable_password():
            return Response({'error': '您目前是使用社群帳號登入，無需修改密碼。'}, status=status.HTTP_400_BAD_REQUEST)
            
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response({'error': '舊密碼與新密碼皆為必填。'}, status=status.HTTP_400_BAD_REQUEST)
            
        # 2. 驗證舊密碼是否正確
        if not user.check_password(old_password):
            return Response({'error': '您輸入的舊密碼不正確，請重新確認。'}, status=status.HTTP_400_BAD_REQUEST)
            
        # 3. 驗證新密碼強度
        if len(new_password) < 8:
            return Response({'error': '新密碼必須至少 8 碼'}, status=status.HTTP_400_BAD_REQUEST)
        
        import re
        if not re.search(r'[A-Z]', new_password):
            return Response({'error': '新密碼必須包含至少 1 個大寫英文字母'}, status=status.HTTP_400_BAD_REQUEST)
        if not re.search(r'[a-z]', new_password):
            return Response({'error': '新密碼必須包含至少 1 個小寫英文字母'}, status=status.HTTP_400_BAD_REQUEST)
        if not re.search(r'\d', new_password):
            return Response({'error': '新密碼必須包含至少 1 個數字'}, status=status.HTTP_400_BAD_REQUEST)
            
        if old_password == new_password:
            return Response({'error': '新密碼不能與原密碼相同。'}, status=status.HTTP_400_BAD_REQUEST)
            
        # 4. 一切安全，更換密碼
        user.set_password(new_password)
        user.save()
        
        # 注意：雖然更換密碼可能會造成舊的 token 失效（視 JWT 設定而定），
        # 但有些設定中 access token 還會有效直到過期，這裡我們先不強制剔除。
        return Response({'message': '密碼更新成功！'}, status=status.HTTP_200_OK)