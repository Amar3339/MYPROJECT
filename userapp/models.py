
from django.contrib import messages


from django.db import models
from adminapp.models import *
from mainapp.models import *

class Cart(models.Model):
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.name}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"


class Order(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.user.name}"


class OrderedItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
