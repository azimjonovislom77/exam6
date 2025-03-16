from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from myapp.models import Category, Product
from django.contrib import messages
from .models import Order, Like
import re
from django.http import JsonResponse


def index(request):
    search_query = request.GET.get('q', '')
    categories = Category.objects.all()
    products = Product.objects.all()

    if search_query:
        products = Product.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    context = {
        'products': products,
        'categories': categories
    }

    return render(request, 'myapp/index.html', context)


def product_list(request):
    return render(request, 'myapp/product-list.html')


def product_detail(request, product_id):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
        'categories': categories
    }
    return render(request, 'myapp/product-details.html', context)


def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)

    filter_type = request.GET.get('filter', None)

    if filter_type == "new":
        products = products.order_by('-created_at')
    elif filter_type == "likes":
        products = products.order_by('-likes')
    elif filter_type == "expensive":
        products = products.order_by('-price')
    elif filter_type == "cheap":
        products = products.order_by('price')

    return render(request, 'myapp/product-list.html', {'category': category, 'products': products})


def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        quantity = request.POST.get('quantity', '')
        uzbekistan_phone_regex = re.compile(r'^\+998\d{9}$')
        if not uzbekistan_phone_regex.match(customer_phone):
            messages.error(request, 'Invalid phone number! Please enter a valid Uzbekistan number (+998 XX XXX-XX-XX)')
            return redirect('myapp:index')

        if not customer_name or not customer_phone or not quantity:
            messages.error(request, 'Iltimos, barcha maydonlarni to‘ldiring!')
            return redirect('place_order', product_id=product.id)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, 'Noto‘g‘ri son! Iltimos, musbat butun son kiriting')
            return redirect('place_order', product_id=product.id)

        if product.quantity < quantity:
            messages.error(request, f'Kechirasiz, faqat {product.quantity} ta mahsulot qolgan!')
            return redirect('place_order', product_id=product.id)

        order = Order.objects.create(
            customer_name=customer_name,
            customer_phone=customer_phone,
            product=product,
            quantity=quantity
        )
        order.save()

        product.quantity -= quantity
        product.save()

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('myapp:index')

    context = {
        'product': product
    }
    return render(request, 'myapp/order.html', context)


@login_required
def like_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    if Like.objects.filter(user=user, product=product).exists():
        messages.warning(request, 'You have already liked this product!')
    else:
        Like.objects.create(user=user, product=product)
        product.likes += 1
        product.save()
        messages.success(request, 'You liked this product!')

    return redirect('myapp:product_detail', product_id=product.id)
