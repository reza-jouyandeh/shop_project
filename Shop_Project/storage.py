from whitenoise.storage import CompressedManifestStaticFilesStorage


class NonStrictManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """
    پروژه چند تا پوشه‌ی قالب قدیمی و بلااستفاده (prd, pd, acca, car) داره که
    فایل CSS‌شون به فونت/عکس‌هایی اشاره می‌کنه که اصلاً وجود ندارن (و هیچ صفحه‌ای
    هم واقعاً از این پوشه‌ها استفاده نمی‌کنه). حالت پیش‌فرض ManifestStaticFilesStorage
    با دیدن همچین ارجاع شکسته‌ای کل collectstatic رو با خطا متوقف می‌کنه.
    غیرفعال کردن manifest_strict فقط باعث می‌شه یه warning چاپ بشه و ادامه بده.
    """

    manifest_strict = False
