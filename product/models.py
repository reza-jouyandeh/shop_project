from django.db import models


class Size(models.Model):
    title = models.CharField(max_length=10)


    def __str__(self):
        return self.title

class Color(models.Model):
    title = models.CharField(max_length=10)


    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    price = models.IntegerField()
    descount = models.SmallIntegerField()
    image = models.ImageField(upload_to="products")
    size = models.ManyToManyField(Size, blank=True, related_name="products")
    color = models.ManyToManyField(Color, blank=True, related_name="products")


    def __str__(self):
        return self.title

    @property
    def discounted_price(self):
        if self.descount:
            return int(self.price - (self.price * self.descount / 100))
        return self.price

    @property
    def price_display(self):
        return "{:,}".format(self.price)

    @property
    def discounted_price_display(self):
        return "{:,}".format(self.discounted_price)