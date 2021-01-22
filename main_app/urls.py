from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    
    path('index/',views.index, name='index'),
    path('contact/',views.contact, name='contact'),
    path('cart/',views.cart, name='cart'),
    path('category/',views.category, name='category'),
    path('sub-category/<int:id>',views.subcategory, name='subcategory'),
    path('product-detail/<int:id>',views.product_detail, name='product_detail'),
    path('search-product/',views.search_product, name='search_product'),
    path('feedback/',views.feedback, name='feedback'),
    path('add_to_cart/<int:id>',views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>',views.remove_from_cart, name='remove_from_cart'),
    path('change_quantity/<int:id>',views.change_quantity, name='change_quantity'),
    path('payment/<int:id>', views.payment, name='payment'),
    path('pay/', views.pay, name='pay'),
    path('cancelled/', views.cancelled, name='cancelled'),
]