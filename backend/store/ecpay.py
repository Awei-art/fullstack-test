"""
ECPay 綠界金流工具模組
負責產生付款參數、CheckMacValue 驗證等
"""
import hashlib
import urllib.parse
from datetime import datetime
from django.conf import settings


def generate_check_mac_value(params):
    """
    產生 ECPay 的 CheckMacValue (SHA256)
    1. 按照 key 字母排序
    2. 組成 key=value& 格式
    3. 前面加 HashKey=, 後面加 &HashIV=
    4. URL encode (小寫)
    5. 轉小寫後 SHA256
    """
    # 排除 CheckMacValue 本身
    sorted_params = sorted(params.items(), key=lambda x: x[0].lower())
    
    # 組合字串
    raw = '&'.join(f'{k}={v}' for k, v in sorted_params)
    raw = f'HashKey={settings.ECPAY_HASH_KEY}&{raw}&HashIV={settings.ECPAY_HASH_IV}'
    
    # URL encode
    encoded = urllib.parse.quote_plus(raw, safe='')
    
    # 轉小寫
    encoded = encoded.lower()
    
    # SHA256 雜湊，轉大寫
    mac_value = hashlib.sha256(encoded.encode('utf-8')).hexdigest().upper()
    
    return mac_value


def create_ecpay_payment(order, retry_count=0):
    """
    建立 ECPay 付款表單參數
    回傳一個 dict，前端用來自動提交表單到 ECPay
    retry_count: 重試次數，用來產生不同的 MerchantTradeNo
    """
    now = datetime.now()
    
    # 商品名稱（ECPay 限制 200 字）
    item_names = []
    for item in order.items.all():
        item_names.append(f'{item.product_name} x{item.quantity}')
    item_name_str = '#'.join(item_names)
    if len(item_name_str) > 200:
        item_name_str = item_name_str[:197] + '...'
    
    # MerchantTradeNo（ECPay 限制 20 碼，不可重複）
    # 首次用訂單編號，重試時加上 R1, R2... 後綴
    trade_no = order.order_number
    if retry_count > 0:
        trade_no = f'{order.order_number}R{retry_count}'
    # 確保不超過 20 碼
    trade_no = trade_no[:20]
    
    # 基本參數
    params = {
        'MerchantID': settings.ECPAY_MERCHANT_ID,
        'MerchantTradeNo': trade_no,  # 交易編號（不可重複）
        'MerchantTradeDate': now.strftime('%Y/%m/%d %H:%M:%S'),
        'PaymentType': 'aio',
        'TotalAmount': str(order.total_amount),
        'TradeDesc': '田園葡萄線上訂購',
        'ItemName': item_name_str,
        'ReturnURL': f'{settings.BACKEND_URL}/api/payment/notify/',           # ECPay 主動通知（Webhook）
        'OrderResultURL': f'{settings.BACKEND_URL}/api/payment/result/',     # 付款完跳回（後端中轉）
        'ChoosePayment': 'Credit',  # 信用卡
        'EncryptType': '1',         # SHA256
        'NeedExtraPaidInfo': 'Y',   # 回傳額外付款資訊
    }
    
    # 計算 CheckMacValue
    params['CheckMacValue'] = generate_check_mac_value(params)
    
    return {
        'payment_url': settings.ECPAY_PAYMENT_URL,
        'params': params,
    }


def verify_check_mac_value(data):
    """
    驗證 ECPay 回傳的 CheckMacValue 是否正確
    用來確認 Webhook 通知確實來自 ECPay
    """
    received_mac = data.get('CheckMacValue', '')
    
    # 複製一份，移除 CheckMacValue
    params = {k: v for k, v in data.items() if k != 'CheckMacValue'}
    
    expected_mac = generate_check_mac_value(params)
    
    return received_mac == expected_mac
