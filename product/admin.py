from django.contrib import admin

# Register your models here.

from .models import Category, Product, FeaturedProduct, Review

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(FeaturedProduct)
admin.site.register(Review)