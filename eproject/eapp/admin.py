from django.contrib import admin
from .models import Product,Cart,Order

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','pdetails','category','is_active']

class CartAdmin(admin.ModelAdmin):
    list_display=['uid','pid','quantity']  

class OrderAdmin(admin.ModelAdmin):
    list_display=['order_id','uid','pid','quantity']


admin.site.register(Product,ProductAdmin)
admin.site.register(Cart,CartAdmin) 
admin.site.register(Order,OrderAdmin)