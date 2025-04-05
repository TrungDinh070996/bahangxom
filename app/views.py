from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse 
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
import uuid
import traceback
from django.core.mail import send_mail

# Create your views here.
def thank_you(request):
    return render(request, 'app/thank_you.html')

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        name_receiver = request.POST.get('name_receiver')
        adrress_receiver = request.POST.get('adrress_receiver')
        phone_receiver = request.POST.get('phone_receiver')
        note_receiver = request.POST.get('note_receiver')

        try:
            # Nếu đã có đơn hàng tạm, dùng lại luôn:
            if isinstance(order, dict):
                return JsonResponse({'message': 'Bạn cần đăng nhập để đặt hàng.'}, status=401)

            # Gắn mã giao dịch
            order.transaction_id = str(uuid.uuid4())
            order.save()

            shipping_address = ShippingAddress.objects.create(
                customer=customer,
                order=order,
                name=name,
                email=email,
                phone=phone,
                name_receiver=name_receiver,
                adrress_receiver=adrress_receiver,
                phone_receiver=phone_receiver,
                note_receiver=note_receiver
            )

            return redirect('thank_you') 

        except Exception as e:
            print(traceback.format_exc())  # In lỗi ra terminal
            return JsonResponse({"message": traceback.format_exc()}, status=500)

    categories = Category.objects.filter(is_sub=False)
    context = {
        'categories': categories,
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login
    }

    return render(request, 'app/checkout.html', context)

def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0 }
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    id = request.GET.get('id', '')
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub =False) 
    context={ 'products': products,'categories': categories, 'items': items, 'order': order, 'cartItems': cartItems, 'user_not_login': user_not_login, 'user_login': user_login}   
    return render(request, 'app/detail.html',context)

def category(request):
    categories = Category.objects.filter(is_sub =False) 
    active_category = request.GET.get('category', '')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    context = {'categories': categories, 'products': products, 'active_category': active_category}
    return render(request, 'app/category.html', context)

def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
        
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0 }
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub =False) 
    products = Product.objects.all()
    context={'categories': categories, "searched": searched, "keys": keys, 'products': products, 'cartItems': cartItems, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/search.html', context)

def register(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show" 
    else:
        user_not_login = "show"
        user_login = "hidden" 
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('login')
    categories = Category.objects.filter(is_sub =False) 
    context = {'categories': categories, 'form': form, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
        return redirect('home')
    else:
        user_not_login = "show"
        user_login = "hidden"
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else: messages.info(request, 'user or password not correct!')            
    categories = Category.objects.filter(is_sub =False) 
    context = {'categories': categories, 'user_not_login': user_not_login, 'user_login': user_login }
    return render(request, 'app/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0 }
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub =False) 
    products = Product.objects.all()
    context={'categories': categories, 'products': products, 'cartItems': cartItems, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/home.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0 }
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub =False) 
    context={'categories': categories, 'items': items, 'order': order, 'cartItems': cartItems, 'user_not_login': user_not_login, 'user_login': user_login}   
    return render(request, 'app/cart.html',context)



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added', safe=False)