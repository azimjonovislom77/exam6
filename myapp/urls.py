from django.urls import path
from .views import index, product_list, product_detail, category_products, place_order, like_product, customer_table, add_customer

app_name = "myapp"

urlpatterns = [
    path('', index, name='index'),
    path('product_list', product_list, name='product_list'),
    path('product_detail/<int:product_id>/', product_detail, name='product_detail'),
    path('category_products/<int:category_id>/', category_products, name='category_products'),
    path('order/<int:product_id>/', place_order, name='place_order'),
    path('like/<int:product_id>/', like_product, name='like_product'),
    path('customers/', customer_table, name='customer_table'),
    path('customers/add/', add_customer, name='add_customer'),
]
