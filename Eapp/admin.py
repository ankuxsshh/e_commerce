from django.contrib import admin
from .models import Category, Product, UserMember, Cart

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserMember)
admin.site.register(Cart)



