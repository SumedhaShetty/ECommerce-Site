from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
from django.utils.translation import gettext as _
import datetime   
from partial_date import PartialDateField
 
 
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/',null=True,blank=True)   

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("main_app:subcategory",kwargs={"id": self.id})


class Sub_Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/',null=True,blank=True)   
   

    category_link = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='cat_id',null=True,blank=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("main_app:subcategory",kwargs={"id": self.id})


class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='uploads/',null=True,blank=True)   
    image1 = models.ImageField(upload_to='uploads/',null=True,blank=True)   
    image2 = models.ImageField(upload_to='uploads/',null=True,blank=True)   
    image3 = models.ImageField(upload_to='uploads/',null=True,blank=True)              
    discount = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    description = models.CharField(max_length=1000)
    subcategory_link = models.ForeignKey(Sub_Category,on_delete=models.CASCADE,related_name='subcat_id',null=True,blank=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("main_app:product_detail",kwargs={"id": self.id})

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE ,related_name='order', default=1)
    def get_absolute_url(self):
        return reverse("main_app:cart")        
    @property
    def subtotal(self):
        price = 0
        list = self.order_id.all()
        for product in list:
            price += product.product_amount
        return(price)
    @property
    def total_quantity(self):
        no_of_products = 0
        list = self.order_id.all()
        for product in list:
            no_of_products += product.quantity
        return(no_of_products)
    @property
    def tax(self):
        return(self.subtotal *0.05)
    @property    
    def amount(self):
        return(self.subtotal + self.tax)


class Cart_Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE ,related_name='cart_item', default=1)
    quantity = models.IntegerField(default=1)
    items_link = models.ForeignKey(Item,on_delete=models.CASCADE,related_name='cart_item_id',null=True,blank=True)
    order_link = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_id',null=True,blank=True)

    def get_absolute_url(self):
        return reverse("main_app:add_to_cart")
    @property
    def product_amount(self):
        return(self.quantity * self.items_link.price)

class Successful_Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE ,related_name='successful_order', default=1)
    ordered_link = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='completed_order_id',null=True,blank=True)
    order_timestamp = models.DateTimeField(null=True, blank=True)

@receiver(pre_delete, sender=Cart_Item, dispatch_uid='order_delete_signal')
def create_backup(sender, instance, using, **kwargs):
    successful_order_obj = Successful_Order()
    successful_order_obj.user = instance.user
    successful_order_obj.ordered_link = instance.order_link
    successful_order_obj.order_timestamp = datetime.datetime.now() 
    successful_order_obj.save()

class Payment(models.Model):
    full_name  = models.CharField(max_length=30, default="Sumedha")
    email = models.EmailField(max_length=254)
    name_on_card  = models.CharField(max_length=30, default="Sumedha")
    address = models.CharField(max_length=100, default="Mumbai")
    city = models.CharField(max_length=30, default="Mumbai")
    state = models.CharField(max_length=30, default="Maharastra")
    zip_code = models.IntegerField(max_length=6, default=400111)
    card_no = CardNumberField(_('card number'))
    card_date = models.CharField(max_length=8, default="01-01-2021")
    cvc = SecurityCodeField(_('security code'))
    order_link = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='payment',null=True,blank=True)


class Feedback(models.Model):
    CHOICES =( 
    ("1", "India"), 
    ("2", "USA"), 
    ("3", "Cannada"), 
    ("4", "Australia"), 
    ) 
    fname = models.CharField(max_length=10, default="Sumedha")
    lname = models.CharField(max_length=10, default="Shetty")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE ,related_name='user_feedback', default=1)
    country = models.CharField(max_length=1, choices=CHOICES, default=1)
    data = models.CharField(max_length=1000)
    item_link = models.ForeignKey(Item,on_delete=models.CASCADE,related_name='item_id',null=True,blank=True)

    def __str__(self):
        return self.data


