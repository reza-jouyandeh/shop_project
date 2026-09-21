from django.conf import settings
from django.db import models

from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    authority = models.CharField(max_length=100, blank=True, null=True)
    ref_id = models.CharField(max_length=100, blank=True, null=True)
    total_price = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"سفارش #{self.pk} - {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="order_items")
    product_title = models.CharField(max_length=60)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product_title} × {self.quantity}"
