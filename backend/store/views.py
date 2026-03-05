from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Product, Order, Bulletin, NewsCategory, News, Variety, DessertCategory, Dessert, ProductCategory
from .serializers import (
    ProductSerializer, OrderSerializer, OrderListSerializer, CreateOrderSerializer, BulletinSerializer,
    NewsCategorySerializer, NewsListSerializer, NewsDetailSerializer,
    VarietyDetailSerializer,
    DessertCategorySerializer, DessertSerializer,
    ProductCategorySerializer
)
from .ecpay import create_ecpay_payment, verify_check_mac_value
import logging
from django.utils import timezone
from django.db.models import Q

logger = logging.getLogger(__name__)


# ========================================
# 品種介紹 API
# ========================================

class VarietyListView(generics.ListAPIView):
    """GET /api/varieties/ — 回傳所有的品種資料（不限是否有貨）"""
    serializer_class = VarietyDetailSerializer
    permission_classes = [AllowAny]
    queryset = Variety.objects.all()


# ========================================
# 甄點 API
# ========================================

class DessertCategoryListView(generics.ListAPIView):
    """GET /api/desserts/categories/ — 甄點分類列表"""
    serializer_class = DessertCategorySerializer
    permission_classes = [AllowAny]
    queryset = DessertCategory.objects.filter(is_active=True)


class DessertListView(generics.ListAPIView):
    """GET /api/desserts/ — 甄點品項列表（支援 ?category=ID 篩選）"""
    serializer_class = DessertSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Dessert.objects.filter(is_active=True).select_related('category')
        category_id = self.request.query_params.get('category')
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs


class DessertDetailView(generics.RetrieveAPIView):
    """GET /api/desserts/<id>/ — 單一甄點詳情"""
    serializer_class = DessertSerializer
    permission_classes = [AllowAny]
    queryset = Dessert.objects.filter(is_active=True).select_related('category')


# ========================================
# 網站快訊 API
# ========================================
class BulletinListAPIView(generics.ListAPIView):
    """
    GET /api/bulletins/
    回傳啟用中，且在設定時間內的公告（讓前台首頁使用）
    """
    serializer_class = BulletinSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        now = timezone.now()
        # 篩選條件：is_active 必須為 True，且判斷 start_date 與 end_date
        return Bulletin.objects.filter(
            is_active=True
        ).filter(
            Q(start_date__isnull=True) | Q(start_date__lte=now)
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=now)
        )


# ========================================
# 最新消息 API
# ========================================

class NewsCategoryListView(generics.ListAPIView):
    """GET /api/news/categories/ — 回傳所有消息分類"""
    serializer_class = NewsCategorySerializer
    permission_classes = [AllowAny]
    queryset = NewsCategory.objects.all()


class NewsListView(generics.ListAPIView):
    """GET /api/news/ — 回傳已發佈的最新消息列表（可選分類篩選）"""
    serializer_class = NewsListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = News.objects.filter(is_published=True).select_related('category')
        category_id = self.request.query_params.get('category')
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs


class NewsDetailView(generics.RetrieveAPIView):
    """GET /api/news/<pk>/ — 回傳單篇消息詳情"""
    serializer_class = NewsDetailSerializer
    permission_classes = [AllowAny]
    queryset = News.objects.filter(is_published=True).select_related('category')

@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    # 支援 ?category=ID 篩選
    category_id = request.query_params.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    # 支援 ?color=顏色名稱 篩選（透過品種的 color 欄位）
    color = request.query_params.get('color')
    if color:
        products = products.filter(varieties__color=color).distinct()
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


class ProductCategoryListView(generics.ListAPIView):
    """GET /api/products/categories/ — 商品分類列表"""
    serializer_class = ProductCategorySerializer
    permission_classes = [AllowAny]
    queryset = ProductCategory.objects.filter(is_active=True)


@api_view(['GET'])
def get_product(request, pk):
    # 嘗試用 ID (pk) 去找商品，找不到就回傳 404
    product = get_object_or_404(Product, id=pk)
    # many=False 代表只抓一筆
    serializer = ProductSerializer(product, many=False, context={'request': request})
    return Response(serializer.data)


# ========================================
# 訂單 API
# ========================================

class OrderListCreateView(APIView):
    """
    GET  /api/orders/     → 取得目前登入會員的所有訂單（列表精簡版）
    POST /api/orders/     → 建立新訂單（結帳提交）
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            try:
                order = serializer.save()

                # 如果是信用卡付款，產生 ECPay 付款資訊
                if order.payment_method == 'credit_card':
                    payment_data = create_ecpay_payment(order)
                    return Response({
                        'message': '訂單建立成功！請前往付款。',
                        'order': OrderSerializer(order).data,
                        'payment': payment_data,
                    }, status=status.HTTP_201_CREATED)

                # 非信用卡付款（貨到付款、轉帳），直接回傳
                return Response({
                    'message': '訂單建立成功！',
                    'order': OrderSerializer(order).data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    """
    GET /api/orders/<order_number>/  → 取得單一訂單完整詳情
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


# ========================================
# ECPay 金流 API
# ========================================

class ECPayRepayView(APIView):
    """
    POST /api/payment/repay/<order_number>/
    重新產生 ECPay 付款參數，讓使用者再次前往付款
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number, user=request.user)

        # 只有待付款 + 信用卡的訂單才能重新付款
        if order.status != 'pending_payment':
            return Response({'error': '此訂單不需要付款'}, status=status.HTTP_400_BAD_REQUEST)
        if order.payment_method != 'credit_card':
            return Response({'error': '此訂單非信用卡付款'}, status=status.HTTP_400_BAD_REQUEST)

        # 增加付款嘗試次數，產生不重複的交易編號
        order.payment_attempts += 1
        order.save()

        payment_data = create_ecpay_payment(order, retry_count=order.payment_attempts)
        return Response({
            'message': '付款資訊已建立',
            'payment': payment_data,
        })

class ECPayNotifyView(APIView):
    """
    POST /api/payment/notify/
    ECPay 付款完成後的「主動通知」(Webhook)
    ECPay 會在背景呼叫這支 API 告訴我們付款結果
    """
    permission_classes = [AllowAny]  # ECPay 不帶認證，需開放
    authentication_classes = []     # 不需認證

    def post(self, request):
        data = request.POST.dict() if request.POST else request.data
        logger.info(f'[ECPay Notify] 收到通知: {data}')

        # 1. 驗證 CheckMacValue
        if not verify_check_mac_value(data):
            logger.warning('[ECPay Notify] CheckMacValue 驗證失敗！')
            return HttpResponse('0|CheckMacValue Error')

        # 2. 取得訂單（MerchantTradeNo 可能帶 R1/R2 後綴，需還原）
        trade_no = data.get('MerchantTradeNo', '')
        order_number = trade_no.split('R')[0] if 'R' in trade_no else trade_no
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            logger.error(f'[ECPay Notify] 訂單不存在: {order_number} (trade_no={trade_no})')
            return HttpResponse('0|Order Not Found')

        # 3. 檢查付款結果
        rtn_code = data.get('RtnCode', '')
        if rtn_code == '1':
            # 付款成功！
            order.payment_status = 'paid'
            order.status = 'pending_shipment'  # 付款成功 → 待出貨
            order.save()
            logger.info(f'[ECPay Notify] 訂單 {order_number} 付款成功！')
        else:
            # 付款失敗
            rtn_msg = data.get('RtnMsg', '未知錯誤')
            logger.warning(f'[ECPay Notify] 訂單 {order_number} 付款失敗: {rtn_msg}')

        # 4. 回傳 1|OK 告訴 ECPay 我們已收到
        return HttpResponse('1|OK')


class ECPayResultView(APIView):
    """
    POST /api/payment/result/
    ECPay 付款完成後的「頁面跳轉」(OrderResultURL)
    ECPay 用 POST 方式把用戶瀏覽器導到這裡
    我們接收結果後，用 302 GET 跳轉到前端成功頁
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        from django.shortcuts import redirect

        data = request.POST.dict() if request.POST else request.data
        logger.info(f'[ECPay Result] 收到跳轉: {data}')

        # MerchantTradeNo 可能帶 R1/R2 後綴
        trade_no = data.get('MerchantTradeNo', '')
        order_number = trade_no.split('R')[0] if 'R' in trade_no else trade_no
        rtn_code = data.get('RtnCode', '')

        # 順便更新付款狀態（當 Webhook 沒打到時的保底）
        if order_number and rtn_code == '1':
            try:
                order = Order.objects.get(order_number=order_number)
                if order.payment_status != 'paid':
                    order.payment_status = 'paid'
                    order.status = 'pending_shipment'  # 付款成功 → 待出貨
                    order.save()
                    logger.info(f'[ECPay Result] 訂單 {order_number} 付款狀態已更新')
            except Order.DoesNotExist:
                pass

        # 跳轉到前端成功頁
        from django.conf import settings
        frontend_url = settings.FRONTEND_URL
        return redirect(f'{frontend_url}/checkout/success?order={order_number}')


class ECPayReturnView(APIView):
    """
    GET /api/payment/return/<order_number>/
    前端查詢付款狀態用
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
        return Response({
            'order_number': order.order_number,
            'payment_status': order.payment_status,
            'payment_status_display': order.get_payment_status_display(),
            'status': order.status,
            'status_display': order.get_status_display(),
            'total_amount': order.total_amount,
        })


# ========================================
# 優惠券 API
# ========================================
# ========================================
# 優惠券 API
# ========================================
from .models import Coupon, UserCoupon
from .serializers import UserCouponSerializer
from django.utils import timezone

class ValidateCouponView(APIView):
    """
    POST /api/coupons/validate/
    驗證優惠券代碼並計算折抵金額
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get('coupon_code', '').strip()
        subtotal = request.data.get('subtotal', 0)
        shipping_fee = request.data.get('shipping_fee', 0)

        if not code:
            return Response({'error': '請輸入優惠代碼'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            coupon = Coupon.objects.get(code=code)
            is_valid, msg = coupon.is_valid(subtotal)
            
            if not is_valid:
                return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)
                
            discount_amount = coupon.calculate_discount(subtotal, shipping_fee)
            
            return Response({
                'valid': True,
                'title': coupon.title,
                'discount_amount': discount_amount,
                'message': '優惠碼套用成功'
            })
            
        except Coupon.DoesNotExist:
            return Response({'error': '優惠代碼不存在或輸入錯誤'}, status=status.HTTP_400_BAD_REQUEST)


class UserCouponListView(generics.ListAPIView):
    """
    GET /api/coupons/my/
    取得登入使用者的錢包優惠券列表
    """
    serializer_class = UserCouponSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 依照 未使用、到期日 近到遠 排序
        return UserCoupon.objects.filter(user=self.request.user).order_by('is_used', '-coupon__valid_to')


class ClaimCouponView(APIView):
    """
    POST /api/coupons/claim/
    會員輸入優惠碼進行領取歸戶（存入錢包）
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get('coupon_code', '').strip()
        if not code:
            return Response({"error": "請提供優惠碼"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return Response({"error": "無效的優惠碼"}, status=status.HTTP_404_NOT_FOUND)
            
        # 1. 檢查優惠券本身是否可以領取
        now = timezone.now()
        if not coupon.is_active:
            return Response({"error": "此優惠券已停用"}, status=status.HTTP_400_BAD_REQUEST)
        if coupon.valid_to < now:
            return Response({"error": "此優惠券已過期"}, status=status.HTTP_400_BAD_REQUEST)
            
        if coupon.usage_limit > 0 and coupon.used_count >= coupon.usage_limit:
             return Response({"error": "此優惠券已被領取或兌換完畢"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. 檢查是否已領取過
        if UserCoupon.objects.filter(user=request.user, coupon=coupon).exists():
            return Response({"error": "您已經領取過此優惠券了"}, status=status.HTTP_400_BAD_REQUEST)
            
        # 3. 建立關聯存入錢包
        UserCoupon.objects.create(user=request.user, coupon=coupon)
        
        return Response({
            "success": True, 
            "message": "優惠券領取成功，已存入您的錢包！", 
            "coupon": {
                "title": coupon.title,
                "code": coupon.code
            }
        }, status=status.HTTP_200_OK)
