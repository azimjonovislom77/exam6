# from django.urls import path
# from .views import index, product_list, product_detail, category_products, place_order, like_product, customer_table, \
#     add_customer, edit_customer, delete_customer, customer_details
# from django.conf import settings
# from django.conf.urls.static import static
#
# app_name = "myapp"
#
# urlpatterns = [
#     path('', index, name='index'),
#     path('product_list', product_list, name='product_list'),
#     path('product_detail/<int:product_id>/', product_detail, name='product_detail'),
#     path('category_products/<int:category_id>/', category_products, name='category_products'),
#     path('order/<int:product_id>/', place_order, name='place_order'),
#     path('like/<int:product_id>/', like_product, name='like_product'),
#     path('customers/', customer_table, name='customer_table'),
#     path('add-customer/', add_customer, name='add_customer'),
#     path('edit-customer/<int:customer_id>/', edit_customer, name='edit_customer'),
#     path('delete-customer/<int:customer_id>/', delete_customer, name='delete_customer'),
#     path('customer_detail/', customer_details, name='customer_detail')
# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#


from django.urls import path
from .views import IndexView, ProductListView, ProductDetailView, CategoryProductsView, place_order, LikeProductView, CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView, CustomerDetailView
from django.conf import settings
from django.conf.urls.static import static

app_name = "myapp"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('category_products/<int:category_id>/', CategoryProductsView.as_view(), name='category_products'),
    path('order/<int:product_id>/', place_order, name='place_order'),
    path('like/<int:product_id>/', LikeProductView.as_view(), name='like_product'),
    path('customers/', CustomerListView.as_view(), name='customer_table'),
    path('add-customer/', CustomerCreateView.as_view(), name='add_customer'),
    path('edit-customer/<int:pk>/', CustomerUpdateView.as_view(), name='edit_customer'),
    path('delete-customer/<int:pk>/', CustomerDeleteView.as_view(), name='delete_customer'),
    path('customer_detail/', CustomerDetailView.as_view(), name='customer_detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)