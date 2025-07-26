from django.contrib import admin
from .models import Product, Cart, CartItem, Comment

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Comment)