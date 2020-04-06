from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

# class Category(models.Model):
#     category_name = models.CharField(max_length=40)
#     def __str__(self):
#         return self.category_name
#
Category_choices =(
    ('Sw', 'Sports Wear'),
    ('S', 'Shirt' ),
    ('OW', 'Outwear')
)

Label_choices =(
    ('P', 'Primary'),
    ('S', 'Shirt' ),
    ('D', 'Danger')
)

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    overview = models.CharField(max_length=120)
    category = models.CharField(choices=Category_choices, max_length=2)
    label = models.CharField(choices=Label_choices, max_length=1)
    price = models.FloatField()
    description = models.TextField()
    thumbnail = models.ImageField()

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse("shop", kwargs={
            "pk": self.pk

        })

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            "pk": self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            "pk": self.pk
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"

    def get_item_price(self):
        return self.item.price*self.quantity

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.get_item_price()
        return total

    def get_after_ship_price(self):
        return self.total_price()+(self.total_price()*(0.01))
    def get_after_tax_price(self):
        return self.get_after_ship_price()+(self.total_price()*(0.18))
    def get_ship_price(self):
        return self.total_price()*(0.01)
    def get_tax_price(self):
        return self.total_price()*(0.18)