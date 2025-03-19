# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, get_object_or_404, redirect
# from django.db.models import Q
# from myapp.models import Category, Product, Customer, Order, Like
# from django.contrib import messages
# import re
# from .forms import CustomerForm
#
#
# def index(request):
#     search_query = request.GET.get('q', '')
#     categories = Category.objects.all()
#     products = Product.objects.all()
#
#     if search_query:
#         products = Product.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
#
#     context = {
#         'products': products,
#         'categories': categories
#     }
#
#     return render(request, 'myapp/index.html', context)
#
#
# def product_list(request):
#     return render(request, 'myapp/product-list.html')
#
#
# def product_detail(request, product_id):
#     categories = Category.objects.all()
#     product = get_object_or_404(Product, id=product_id)
#     context = {
#         'product': product,
#         'categories': categories
#     }
#     return render(request, 'myapp/product-details.html', context)
#
#
# def category_products(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
#     products = Product.objects.filter(category=category)
#
#     filter_type = request.GET.get('filter', None)
#
#     if filter_type == "new":
#         products = products.order_by('-created_at')
#     elif filter_type == "likes":
#         products = products.order_by('-likes')
#     elif filter_type == "expensive":
#         products = products.order_by('-price')
#     elif filter_type == "cheap":
#         products = products.order_by('price')
#
#     return render(request, 'myapp/product-list.html', {'category': category, 'products': products})
#
#
# def place_order(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     if request.method == "POST":
#         customer_name = request.POST.get('customer_name')
#         customer_phone = request.POST.get('customer_phone')
#         quantity = request.POST.get('quantity', '')
#         uzbekistan_phone_regex = re.compile(r'^\+998\d{9}$')
#         if not uzbekistan_phone_regex.match(customer_phone):
#             messages.error(request, 'Invalid phone number! Please enter a valid Uzbekistan number (+998 XX XXX-XX-XX)')
#             return redirect('myapp:index')
#
#         if not customer_name or not customer_phone or not quantity:
#             messages.error(request, 'Iltimos, barcha maydonlarni to‘ldiring!')
#             return redirect('place_order', product_id=product.id)
#
#         try:
#             quantity = int(quantity)
#             if quantity <= 0:
#                 raise ValueError
#         except ValueError:
#             messages.error(request, 'Noto‘g‘ri son! Iltimos, musbat butun son kiriting')
#             return redirect('place_order', product_id=product.id)
#
#         if product.quantity < quantity:
#             messages.error(request, f'Kechirasiz, faqat {product.quantity} ta mahsulot qolgan!')
#             return redirect('place_order', product_id=product.id)
#
#         order = Order.objects.create(
#             customer_name=customer_name,
#             customer_phone=customer_phone,
#             product=product,
#             quantity=quantity
#         )
#         order.save()
#
#         product.quantity -= quantity
#         product.save()
#
#         messages.success(request, 'Your order has been placed successfully!')
#         return redirect('myapp:index')
#
#     context = {
#         'product': product
#     }
#     return render(request, 'myapp/order.html', context)
#
#
# @login_required
# def like_product(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     user = request.user
#
#     if Like.objects.filter(user=user, product=product).exists():
#         messages.warning(request, 'You have already liked this product!')
#     else:
#         Like.objects.create(user=user, product=product)
#         product.likes += 1
#         product.save()
#         messages.success(request, 'You liked this product!')
#
#     return redirect('myapp:product_detail', product_id=product.id)
#
#
# def customer_table(request):
#     customers = Customer.objects.all()
#     return render(request, 'myapp/customers.html', {'customers': customers})
#
#
# def add_customer(request):
#     if request.method == 'POST':
#         form = CustomerForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('myapp:customer_table')
#     else:
#         form = CustomerForm()
#
#     return render(request, 'myapp/customer_add.html', {'form': form})
#
#
# def edit_customer(request, customer_id):
#     customer = get_object_or_404(Customer, id=customer_id)
#
#     if request.method == "POST":
#         form = CustomerForm(request.POST, instance=customer)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Customer updated successfully!")
#             return redirect('myapp:customer_table')
#     else:
#         form = CustomerForm(instance=customer)
#
#     return render(request, 'myapp/customer_edit.html', {'form': form})
#
#
# def delete_customer(request, customer_id):
#     customer = get_object_or_404(Customer, id=customer_id)
#     customer.delete()
#     messages.success(request, "Customer deleted successfully!")
#     return redirect('myapp:customer_table')
#
#
# def customer_details(request):
#     return render(request, 'myapp/customer-details.html')


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
import re
from .models import Category, Product, Customer, Order, Like
from .forms import CustomerForm


class IndexView(ListView):
    model = Product
    template_name = 'myapp/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            return Product.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'myapp/product-list.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'myapp/product-details.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryProductsView(ListView):
    model = Product
    template_name = 'myapp/product-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs['category_id'])
        products = Product.objects.filter(category=category)
        filter_type = self.request.GET.get('filter', None)
        if filter_type == "new":
            return products.order_by('-created_at')
        elif filter_type == "likes":
            return products.order_by('-likes')
        elif filter_type == "expensive":
            return products.order_by('-price')
        elif filter_type == "cheap":
            return products.order_by('price')
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, id=self.kwargs['category_id'])
        return context


class PlaceOrderView(FormView):
    template_name = 'myapp/order.html'
    success_url = reverse_lazy('myapp:index')

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        quantity = request.POST.get('quantity', '')

        uzbekistan_phone_regex = re.compile(r'^\+998\d{9}$')
        if not uzbekistan_phone_regex.match(customer_phone):
            messages.error(request, 'Invalid phone number! Please enter a valid Uzbekistan number (+998 XX XXX-XX-XX)')
            return redirect('myapp:index')

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

        Order.objects.create(customer_name=customer_name, customer_phone=customer_phone, product=product,
                             quantity=quantity)
        product.quantity -= quantity
        product.save()
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('myapp:index')


class LikeProductView(LoginRequiredMixin, DetailView):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        user = request.user
        if Like.objects.filter(user=user, product=product).exists():
            messages.warning(request, 'You have already liked this product!')
        else:
            Like.objects.create(user=user, product=product)
            product.likes += 1
            product.save()
            messages.success(request, 'You liked this product!')
        return redirect('myapp:product_detail', product_id=product.id)


class CustomerListView(ListView):
    model = Customer
    template_name = 'myapp/customers.html'
    context_object_name = 'customers'


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'myapp/customer_add.html'
    success_url = reverse_lazy('myapp:customer_table')


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'myapp/customer_edit.html'
    success_url = reverse_lazy('myapp:customer_table')

    def form_valid(self, form):
        messages.success(self.request, 'Customer updated successfully!')
        return super().form_valid(form)


class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('myapp:customer_table')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Customer deleted successfully!')
        return super().delete(request, *args, **kwargs)


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'myapp/customer-details.html'
