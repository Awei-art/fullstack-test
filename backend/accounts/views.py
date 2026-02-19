from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated#權限檢查，要求必須登入
from rest_framework import status
from .serializers import UserSerializer, RegisterSerializer

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