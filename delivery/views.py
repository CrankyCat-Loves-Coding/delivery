from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .models import Menu, Order, OrderItem, OrderModel, Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CreateUserForm, AddressForm
from django.core.mail import send_mail


import json

# login, logout and regester
class RegisterPage(View):
    def get(self, request, *args, **kwargs):
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
            
                return redirect('login')
        else:
            form = UserCreationForm()

        context = {
            'form': form
        }
        return render(request, 'accounts/signup.html', context)


class LoginPage(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect('index')

        context = {

        }
        return render(request, 'accounts/login.html', context)


class Customer(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        # using LoginRequiredMixin to restrict access
        login_url = 'accounts/login.html'

        return render(request, 'customer.html')

# place order
class Main(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer,
                complete=False
            )
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_item':0 }
            #cartItems = order['get_cart_items']
        
        # context = {
        #     'cartItems': cartItems
        # }

        return render(request, 'index.html')


class MenuItem(View):
    model = Menu

    def get(self, request, *args, **kwargs):
       
        meals = Menu.objects.filter(category__name__contains='Meals')
        desserts = Menu.objects.filter(category__name__contains='Desserts')
        drinks = Menu.objects.filter(category__name__contains='Drinks')

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer,
                complete=False
            )
            items = order.orderitem_set.all()
            # cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_item':0 }
            # cartItems = order['get_cart_items']

        context = {
            'meals': meals,
            'desserts': desserts,
            'drinks': drinks,
            # 'cartItems': cartItems
        }

        return render(request, 'menu.html', context)


class Cart(LoginRequiredMixin, View):
    model = Order
    model = OrderItem
    model = OrderModel


    def get(self, request, *args, **kwargs): 

        # using LoginRequiredMixin to restrict access
        login_url = 'accounts/login.html' 

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer,
                complete=False
            )
            items = order.orderitem_set.all()
            # cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_item':0 }
            # cartItems = or der['get_cart_items']
        
        context = {
            'items': items,
            'order': order,
            # 'cartItems': cartItems
            'form': AddressForm()
        }

        return render(request, 'cart.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        eircode = request.POST.get('eircode')


        order = OrderModel.objects.create (
            name=name,
            phone=phone,
            email=email,
            address=address,
            eircode=eircode
        )

        body = (
            'Thank you for your order!'
            'Your food is being made and will be delivered soon!\n'
            

        )
        #send order confirmation
        send_mail(
            'Order confirmation',
            body,
            'j35306406@gmail.com',
            [email],
            fail_silently=False
        )
        
        context = {
            'form': AddressForm()
        }

        return render(request, 'cart.html', context)

class Pay(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pay.html')


class UpdateCart(View):

    def post(self, request, *args, **kwargs):
        
        data = json.loads(request.body)
        menuId = data['menuId'] 
        action = data['action']

        print('action:', action)
        print('menuId:', menuId)

        customer = request.user.customer
        menu = Menu.objects.get(id=menuId)
        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False,
        )

        orderItem, created = OrderItem.objects.get_or_create(
            order=order,
            menu=menu
        )

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()
        
        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse('Item was added', safe=False)


class OrderConfirmation(View):

    def get(self, request, pk, *args, **kwargs):
        order = Menu.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'price': order.price
        }
        return render(request, 'order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        print(request.body)


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'order-pay-confirmation.html')


