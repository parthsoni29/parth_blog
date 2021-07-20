from django.contrib import admin
from . models import Sub_category,Brands,Product,Order,OrderItem,Address,Coupon,Refund

# Register your models here.

admin.site.register(Order)

admin.site.register(OrderItem)

admin.site.register(Address)

admin.site.register(Coupon)

admin.site.register(Refund)
admin.site.register(Sub_category)
admin.site.register(Brands)
admin.site.register(Product)

