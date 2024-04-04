from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserMember, Category, Product, Cart
from django.shortcuts import get_object_or_404

# Create your views here.

def homepage(request):
    categories = Category.objects.all()
    return render(request, 'homepage.html', {'categories': categories})


def registerpage(request):
    return render(request, 'registerpage.html')


def register(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        address = request.POST['address']
        contact_number = request.POST['contactNumber']
        email = request.POST['emailAddress']
        image = request.FILES.get('image', None)

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('registerpage')

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        user_member = UserMember(user=user, address=address, contact_number=contact_number, profile_pic=image)
        user_member.save()

        messages.success(request, 'User registered successfully. You can now log in.')

        return redirect('registerpage')

    return render(request, 'registerpage.html')


def loginpage(request):
    messages_info = messages.get_messages(request)
    return render(request, 'loginpage.html', {'messages_info': messages_info})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            if user.is_staff:
                return redirect('admin_homepage')
            else:
                return redirect('user_homepage')
        else:
            messages.error(request, 'Invalid login credentials.')
            
            return redirect('loginpage')

    return render(request, 'loginpage.html')

def user_homepage(request):

    categories = Category.objects.all()
    messages_info = messages.get_messages(request)

    return render(request, 'user_homepage.html', {'categories': categories, 'messages_info': messages_info})


def admin_homepage(request):
    categories = Category.objects.all()
    return render(request, 'admin_homepage.html', {'categories': categories})


def cartpage(request):
    return render(request, "cartpage.html")


def add_category_page(request):
    return render(request, 'add_category.html')

def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('categoryName')

        if Category.objects.filter(name=category_name).exists():
            messages.error(request, 'Category already exists')
        else:
            new_category = Category(name=category_name)
            new_category.save()
            messages.success(request, 'Category added successfully')

    return redirect('add_category_page')


def add_product_page(request):
    categories = Category.objects.all()
    return render(request, 'add_product.html', {'categories': categories})

def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        try:
            category = Category.objects.get(pk=category_id)

            new_product = Product(
                product_name=product_name,
                description=description,
                category=category,
                price=price,
                image=image
            )
            new_product.save()
            messages.success(request, 'Product added successfully')
        except Exception as e:
            messages.error(request, f'Error adding product: {str(e)}')

    return redirect('add_product_page')

def mens_page(request):
    categories = Category.objects.all()
    men_products = Product.objects.filter(category__name='Men')
    return render(request, "men.html", {'products': men_products, 'categories': categories})

def womens_page(request):
    categories = Category.objects.all()
    women_products = Product.objects.filter(category__name='Women')
    return render(request, "women.html", {'products': women_products, 'categories': categories})

def kids_page(request):
    categories = Category.objects.all()
    kids_products = Product.objects.filter(category__name='Kids')
    return render(request, "kids.html", {'products': kids_products, 'categories': categories})


def view_products(request):
    products = Product.objects.all()
    return render(request, 'view_products.html', {'products': products})

def delete_product(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        product.delete()
        messages.info(request, f'The product "{product.product_name}" has been deleted successfully.')
    except Product.DoesNotExist:
        messages.error(request, 'Product not found.')
    return redirect('view_products')


def view_users(request):
    users = UserMember.objects.all()
    return render(request, 'view_users.html', {'users': users})


def delete_user(request, user_id):
    try:
        user_member = UserMember.objects.get(pk=user_id)
        deleted_username = user_member.user.username  
        user_member.user.delete()
        messages.success(request, f'User {deleted_username} deleted successfully.')
    except UserMember.DoesNotExist:
        messages.error(request, 'User not found.')
    return redirect('view_users')


def carts(request):
    if request.user.is_authenticated:
        user=Cart.objects.all()
        return render(request,'cartpage.html',{'user':user})


def add_to_cart(request, product_id):
    product_instance = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product_instance)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, 'Product added to cart successfully.')
    return redirect('cartpage')  

def cartpage(request):
    user_cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.product.price * item.quantity for item in user_cart_items)
    return render(request, "cartpage.html", {'user_cart_items': user_cart_items, 'total_amount': total_amount})


def increment_quantity(request, pk):
    cart_item = Cart.objects.get(id=pk, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cartpage')

def decrement_quantity(request, pk):
    cart_item = Cart.objects.get(id=pk, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cartpage')

def delete_product_from_cart(request, product_id):
    try:
        cart_item = Cart.objects.get(user=request.user, product__id=product_id)
        cart_item.delete()
        messages.success(request, 'Product removed from cart successfully.')
    except Cart.DoesNotExist:
        messages.error(request, 'Product not found in the cart.')
    return redirect('cartpage')


def place_order(request):
    messages.success(request, 'Order placed successfully. Thank you for shopping!')
    return redirect('payment_page')

def payment_page(request):
    user_cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.product.price * item.quantity for item in user_cart_items)
    return render(request, "payment.html", {'user_cart_items': user_cart_items, 'total_amount': total_amount})

def logout_user(request):
    return redirect('homepage')


def logout_admin(request):
    return redirect('homepage')

