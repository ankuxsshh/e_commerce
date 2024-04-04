from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    product_name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/product/', null=True, blank=True)
    price = models.IntegerField()

class UserMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=12, null=True)
    profile_pic = models.ImageField(upload_to='image/profile', null=True, blank=True)

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.prod.price