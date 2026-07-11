from django.shortcuts import render,get_object_or_404, redirect
from .models import Category, FoodItem, Cart, Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def home(request):
    categories = Category.objects.all()
    food_items = FoodItem.objects.all()

    return render(request, 'home.html', {
        'categories': categories,
        'food_items': food_items
    })

def order(request,id):
    food = get_object_or_404(FoodItem,id=id)
    return render(request, 'order.html', {'food': food})


@login_required(login_url='user_login')
def cart(request):
    cart_items = Cart.objects.all()

    total=0
    for item in cart_items:
        total += item.food.price * item.quantity
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


@login_required(login_url='user_login')
def add_to_cart(request,id):
    food = get_object_or_404(FoodItem, id=id)

    cart_item = Cart.objects.filter(food=food).first()

    if cart_item:
        cart_item.quantity +=1
        cart_item.save()
    else:
        Cart.objects.create(
            food=food,
            quantity=1
        )   
    return redirect('cart')

def increase_quantity(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


def decrease_quantity(request, id):
    cart_item = get_object_or_404(Cart, id=id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

def remove_from_cart(request,id):
    cart_item = get_object_or_404(Cart,id=id)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='user_login')
def checkout(request):
    cart_items = Cart.objects.all()

    total = 0
    for item in cart_items:
        total += item.food.price * item.quantity

    if request.method == "POST":
        Order.objects.create(
            name=request.POST['name'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            total=total
        )
        cart_items.delete()
       
        return redirect('success')

    return render(request, 'checkout.html', {'total': total})
   
def success(request):
    return render(request, 'success.html')


@login_required(login_url='user_login')
def track_order(request):
    order= Order.objects.last()
    return render(request,'track_order.html',{'order':order})


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration Successful. Please Login.")
        return redirect("login")

    return render(request, "register.html") 


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect("home")
        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")  

def user_logout(request):
    logout(request)
    return redirect('home')

def menu(request):
    query = request.GET.get('q')

    if query:
        foods = FoodItem.objects.filter(
            Q(food_name__icontains=query)
        )
    else:
        foods = FoodItem.objects.all()
    return render(request, 'menu.html', {'foods': foods, 'query': query})    
    

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')