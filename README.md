# 📚 Shop Project — فروشگاه آنلاین کتاب

پروژه‌ی نمونه‌ی یک فروشگاه اینترنتی کتاب، ساخته‌شده با Django. این پروژه صرفاً جهت نمونه‌کار (پورتفولیو) ساخته شده و هیچ کتابی واقعاً به فروش نمی‌رسد.

## امکانات

- نمایش لیست و جزئیات محصولات (کتاب‌ها)
- ثبت‌نام و ورود کاربران (با اعتبارسنجی رمز عبور استاندارد جنگو)
- سبد خرید مبتنی بر سشن (بدون نیاز به لاگین برای افزودن به سبد)
- اتصال به درگاه پرداخت زرین‌پال (حالت sandbox به‌صورت پیش‌فرض)
- پنل مدیریت جنگو با پشتیبانی فارسی (`admin_persian`)
- استفاده از WhiteNoise برای سرو فایل‌های استاتیک در پروداکشن

## پیش‌نیازها

- Python 3.11+
- pip

## نصب و اجرا (محیط توسعه)

```bash
git clone <repo-url>
cd shop_project

python -m venv venv
source venv/bin/activate      # ویندوز: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env          # مقادیر داخلش رو با اطلاعات خودت پر کن
```

سپس متغیرهای محیطی زیر را در فایل `.env` تنظیم کن (یا export کن):

| متغیر | توضیح | پیش‌فرض |
|---|---|---|
| `SECRET_KEY` | کلید امنیتی جنگو — در پروداکشن حتماً یک مقدار تصادفی و مخفی بگذار | یک مقدار نمونه‌ی نامعتبر برای پروداکشن |
| `DEBUG` | حالت دیباگ | `True` |
| `ALLOWED_HOSTS` | دامنه‌های مجاز، جدا شده با کاما | `127.0.0.1,localhost` |
| `ZARINPAL_MERCHANT_ID` | مرچنت‌کد زرین‌پال | مرچنت‌کد آزمایشی |
| `ZARINPAL_SANDBOX` | حالت آزمایشی درگاه پرداخت | `True` |
| `GHASEDAK_API_KEY` | فقط برای اجرای `account/testsms.py` | - |
| `TEST_PHONE_NUMBER` | فقط برای اجرای `account/testsms.py` | - |

اجرای مایگریشن‌ها و بالا آوردن سرور:

```bash
python manage.py migrate
python manage.py createsuperuser   # اختیاری، برای دسترسی به /admin
python manage.py runserver
```

پروژه روی `http://127.0.0.1:8000` بالا می‌آید.

## اجرا در پروداکشن

پروژه با `gunicorn` و `Procfile` آماده‌ی دیپلوی روی پلتفرم‌هایی مثل Railway/Render/Heroku است:

```
release: python manage.py migrate
web: gunicorn Shop_Project.wsgi --log-file -
```

قبل از دیپلوی حتماً:
- `SECRET_KEY` واقعی و `DEBUG=False` را تنظیم کن.
- `ALLOWED_HOSTS` را با دامنه‌ی واقعی پر کن.
- در صورت استفاده از درگاه واقعی، `ZARINPAL_MERCHANT_ID` و `ZARINPAL_SANDBOX=False` را تنظیم کن.

## ساختار پروژه

```
shop_project/
├── Shop_Project/    # تنظیمات اصلی جنگو
├── home/            # صفحه‌ی اصلی
├── product/         # مدل و ویوهای محصولات
├── cart/            # سبد خرید، سفارش و اتصال به زرین‌پال
├── account/         # ثبت‌نام / ورود / خروج کاربران
├── statics/         # فایل‌های استاتیک (CSS/JS/تصاویر/فونت)
├── media/           # تصاویر آپلودشده‌ی محصولات
└── templates/       # قالب پایه
```

## نکته

طراحی HTML/CSS این پروژه از قالب‌های آماده استفاده شده و صرفاً برای نمایش توانایی بک‌اند (جنگو) به کار رفته است.
