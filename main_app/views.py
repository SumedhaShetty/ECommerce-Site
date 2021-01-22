from django.conf import settings 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User,auth
from .models import Category,Sub_Category,Item,Order,Feedback, Cart_Item, Payment
from django.core.paginator import Paginator
from django.db.models import Q
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt 
import stripe


def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')

def category(request):
    categories = Category.objects.all()
    context = {
        "categories" : categories,
    }
    return render(request, 'category.html', context)

def subcategory(request,id):
    subcat_instance = get_object_or_404(Sub_Category, id=id)
    context = {
        "subcat_instance" : subcat_instance,
    }
    return render(request, 'subcategory.html', context)

def cart_item_obj(request,id):
    subcat_instance = get_object_or_404(Sub_Category, id=id)
    context = {
        "subcat_instance" : subcat_instance,
    }
    return render(request, 'search_product.html', context)

def product_detail(request,id):
    product_instance = get_object_or_404(Item, id=id)
    context = {
        "product_instance" : product_instance,

    }
    return render(request, 'product_detail.html', context)

def search_product(request):
    queryset_list = Item.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(name__icontains=query)|
            Q(price__icontains=query)|
            Q(description__icontains=query)|
            Q(subcategory_link__name__icontains=query)|
            Q(subcategory_link__category_link__name__icontains=query)
        ).distinct()

    paginator = Paginator(queryset_list, 12) 
    page_request_var ="page"
    page = request.GET.get(page_request_var)
    queryset = paginator.get_page(page)

    context = {
        "object_list" : queryset,
        "page_request_var": page_request_var, 

    }
    return render(request, 'search_product.html', context)

def feedback(request):
    feedback_obj = Feedback()

    if request.method == 'POST':
        feedback_obj.user = request.user
        feedback_obj.fname = request.POST['fname']
        feedback_obj.lname = request.POST['lname']        
        feedback_obj.country = request.POST['country']
        feedback_obj.item_link = get_object_or_404(Item, name=request.POST['product'])
        feedback_obj.save()
        feedback_obj.data = request.POST['subject']
        feedback_obj.save()

        return render(request,'index.html')

    else:
        return render(request,'contact.html')

def add_to_cart(request,id):    
    selected_item = get_object_or_404(Item, id=id)
    order_obj ,created_order = Order.objects.get_or_create(user=request.user)
    order_obj.save() 
    print(created_order)
    cart_item_obj,created_cart_item = Cart_Item.objects.get_or_create(user=request.user, items_link = selected_item)


    if (created_cart_item == False):
        cart_item_obj.quantity += int(request.POST['quantity'])
        cart_item_obj.save()
        print(request.POST['quantity'])
        return redirect('cart')

    cart_item_obj.items_link = selected_item
    cart_item_obj.quantity = request.POST['quantity']
    cart_item_obj.order_link = order_obj
    order_obj.save() 
    cart_item_obj.save()

    return redirect('cart')

def remove_from_cart(request,id):
    selected_item = get_object_or_404(Item, id=id)
    cart_item_obj = Cart_Item.objects.get(user=request.user, items_link = selected_item)
    cart_item_obj.delete()
    return redirect('cart')

def change_quantity(request,id):
    selected_item = get_object_or_404(Item, id=id)
    cart_item_obj= Cart_Item.objects.get(user=request.user, items_link = selected_item)
    cart_item_obj.quantity = int(request.POST['quantity'])
    cart_item_obj.save()
    return redirect('cart')

def cart(request):
    products = Cart_Item.objects.filter(user = request.user)
    order_instance = Order.objects.get(user = request.user)
    context = {
            "order_instance" : order_instance,
            "products" : products,
        }

    return render(request,'cart.html',context)

def payment(request,id):
    products = Cart_Item.objects.filter(user = request.user)
    order_instance = Order.objects.get(user = request.user)
    context = {
            "order_instance" : order_instance,
            "products" : products,
        }

    return render(request,'payment.html',context)

def pay(request):
    cart_item_obj = Cart_Item.objects.filter(user=request.user)
    order_instance = Order.objects.get(user = request.user)
    payment_obj = Payment()
    payment_obj.order_link = order_instance
    payment_obj.save()


    if request.method == 'POST':
        payment_obj.full_name = request.POST['firstname']        
        payment_obj.email  = request.POST['email']
        payment_obj.name_on_card = request.POST['cardname']
        payment_obj.address = request.POST['address']
        payment_obj.city = request.POST['city']
        payment_obj.state = request.POST['state']
        payment_obj.zip = request.POST['zip']
        payment_obj.card_no = request.POST['cardnumber']
        payment_obj.cvc = request.POST['cvv']
        payment_obj.card_date = request.POST['expyear']
        payment_obj.save()
        cart_item_obj.delete()


        return render(request,'success.html')

    else:
        return render(request,'payment.html')

    order_instance.delete()

    return render(request,'payment.html')

def cancelled(request):
    return render(request,'cancelled.html')
