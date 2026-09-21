from product.models import Product

CART_SESSION_ID = "cart"


class Cart:
    """
    یک سبد خرید ساده و بدون نیاز به لاگین که داخل session کاربر ذخیره می‌شود.
    فقط شناسه محصول و تعداد نگه‌داشته می‌شود؛ قیمت همیشه لحظه‌ای از دیتابیس خوانده می‌شود.
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] += quantity
        else:
            self.cart[product_id] = {"quantity": quantity}
        self.save()

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            return
        if quantity <= 0:
            self.remove(product)
            return
        self.cart[product_id]["quantity"] = quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session[CART_SESSION_ID] = {}
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            item = self.cart[str(product.id)]
            price = product.discounted_price
            yield {
                "product": product,
                "quantity": item["quantity"],
                "price": price,
                "total_price": price * item["quantity"],
            }

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return sum(
            product.discounted_price * self.cart[str(product.id)]["quantity"]
            for product in products
        )
