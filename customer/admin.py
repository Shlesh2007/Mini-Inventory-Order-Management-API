from django.contrib import admin
from . models import Product,Customer,OrderItem,Order
# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(Order)