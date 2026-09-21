"""
اتصال ساده به درگاه پرداخت زرین‌پال (نسخه REST v4).
پیش‌فرض روی محیط sandbox (آزمایشی) تنظیم شده تا بدون مرچنت‌کد واقعی هم قابل تست باشد.
برای رفتن به حالت واقعی، مقادیر ZARINPAL_MERCHANT_ID و ZARINPAL_SANDBOX را در settings.py تغییر بده.
"""

import requests
from django.conf import settings

REQUEST_URL = (
    "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    if settings.ZARINPAL_SANDBOX
    else "https://api.zarinpal.com/pg/v4/payment/request.json"
)

VERIFY_URL = (
    "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    if settings.ZARINPAL_SANDBOX
    else "https://api.zarinpal.com/pg/v4/payment/verify.json"
)

STARTPAY_URL = (
    "https://sandbox.zarinpal.com/pg/StartPay/{authority}"
    if settings.ZARINPAL_SANDBOX
    else "https://www.zarinpal.com/pg/StartPay/{authority}"
)


class ZarinpalError(Exception):
    pass


def request_payment(amount_toman, description, callback_url, mobile=None):
    """
    ایجاد یک درخواست پرداخت جدید.
    amount_toman باید به تومان باشد؛ خودمان آن را به ریال تبدیل می‌کنیم (زرین‌پال ریال می‌گیرد).
    خروجی: authority (رشته) برای هدایت کاربر به درگاه.
    """
    payload = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": int(amount_toman) * 10,
        "description": description,
        "callback_url": callback_url,
    }
    if mobile:
        payload["metadata"] = {"mobile": mobile}

    try:
        response = requests.post(REQUEST_URL, json=payload, timeout=10)
        data = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise ZarinpalError("امکان ارتباط با درگاه پرداخت وجود ندارد.") from exc

    result = data.get("data") or {}
    if result.get("code") == 100:
        return result["authority"]

    errors = data.get("errors") or result.get("errors") or {}
    raise ZarinpalError(f"درخواست پرداخت رد شد: {errors}")


def get_payment_redirect_url(authority):
    return STARTPAY_URL.format(authority=authority)


def verify_payment(amount_toman, authority):
    """
    تایید پرداخت بعد از بازگشت کاربر از درگاه.
    خروجی: (True, ref_id) در صورت موفقیت، یا (False, None).
    """
    payload = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": int(amount_toman) * 10,
        "authority": authority,
    }

    try:
        response = requests.post(VERIFY_URL, json=payload, timeout=10)
        data = response.json()
    except (requests.RequestException, ValueError):
        return False, None

    result = data.get("data") or {}
    if result.get("code") in (100, 101):
        return True, result.get("ref_id")

    return False, None
