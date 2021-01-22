from django.contrib import admin
from .models import Category,Sub_Category,Item,Order,Feedback, Cart_Item, Payment, Successful_Order
# Register your models here.

admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Item)
admin.site.register(Cart_Item)
admin.site.register(Successful_Order)
admin.site.register(Order)
admin.site.register(Feedback)
admin.site.register(Payment)