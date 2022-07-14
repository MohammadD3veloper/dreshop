from django.contrib import admin
from .models import Category,Coupon,Order,Product,ProductImage,ProductItem
# Register your models here.

admin.site.register(Category)
admin.site.register(Coupon)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductItem)