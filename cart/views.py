from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from product.models import Product

from .cart import Cart
from .models import Order, OrderItem
from .zarinpal import ZarinpalError, get_payment_redirect_url, request_payment, verify_payment


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1
    quantity = max(1, quantity)
    cart.add(product=product, quantity=quantity)
    messages.success(request, f'«{product.title}» به سبد خرید اضافه شد.')
    return redirect(request.POST.get("next") or "cart:cart_detail")


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1
    cart.update(product=product, quantity=quantity)
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    messages.info(request, f'«{product.title}» از سبد خرید حذف شد.')
    return redirect("cart:cart_detail")


@login_required
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, "سبد خرید شما خالی است.")
        return redirect("cart:cart_detail")

    order = Order.objects.create(user=request.user, total_price=cart.get_total_price())
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item["product"],
            product_title=item["product"].title,
            price=item["price"],
            quantity=item["quantity"],
        )

    callback_url = request.build_absolute_uri(reverse("cart:payment_callback"))

    try:
        authority = request_payment(
            amount_toman=order.total_price,
            description=f"پرداخت سفارش شماره {order.pk}",
            callback_url=callback_url,
            mobile=getattr(request.user, "username", None),
        )
    except ZarinpalError as exc:
        messages.error(request, str(exc))
        order.delete()
        return redirect("cart:cart_detail")

    order.authority = authority
    order.save()

    return redirect(get_payment_redirect_url(authority))


def payment_callback(request):
    authority = request.GET.get("Authority")
    status = request.GET.get("Status")

    order = Order.objects.filter(authority=authority, is_paid=False).first()

    if not order:
        return render(request, "cart/payment_result.html", {"success": False})

    if status != "OK":
        order.delete()
        return render(request, "cart/payment_result.html", {"success": False})

    verified, ref_id = verify_payment(amount_toman=order.total_price, authority=authority)

    if verified:
        order.is_paid = True
        order.ref_id = ref_id
        order.save()
        Cart(request).clear()
        return render(request, "cart/payment_result.html", {"success": True, "order": order})

    order.delete()
    return render(request, "cart/payment_result.html", {"success": False})
