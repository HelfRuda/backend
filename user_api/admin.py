from django.contrib import admin
from .models import AppUser, Category, Product, Order, Cart, CartItem

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(AppUser)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)