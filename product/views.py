from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView

from product.models import Product


class ProductDetailView(DetailView):
    template_name = "product/prod.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next_product"] = (
            Product.objects.filter(pk__gt=self.object.pk).order_by("pk").first()
        )
        context["previous_product"] = (
            Product.objects.filter(pk__lt=self.object.pk).order_by("-pk").first()
        )
        return context


class LopDetailView(DetailView):
    template_name = "product/de.html"
    model = Product


def start_reading(request):
    """
    دکمه «برای دانلود کتاب داستان کلیک کنید» در صفحه اصلی به این ویو می‌رود.
    اگر محصولی در دیتابیس باشد کاربر را به اولین کتاب می‌فرستد، وگرنه پیام مناسب نشان می‌دهد.
    """
    first_product = Product.objects.order_by("pk").first()
    if first_product:
        return redirect("product_detail", pk=first_product.pk)
    return render(request, "product/no_products.html")
