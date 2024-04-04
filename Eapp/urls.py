
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.homepage, name='homepage'),

    path('registerpage/', views.registerpage, name='registerpage'),

    path('register/', views.register, name='register'),

    path('loginpage/', views.loginpage, name='loginpage'),

    path('login/', views.login, name='login'),

    path('user_homepage/', views.user_homepage, name='user_homepage'),

    path('admin_homepage/', views.admin_homepage, name='admin_homepage'),

    path('cartpage/', views.cartpage, name='cartpage'),

    path('add_category_page/', views.add_category_page, name='add_category_page'),

    path('add_category/', views.add_category, name='add_category'), 

    path('add_product_page/', views.add_product_page, name='add_product_page'),

    path('add_product/', views.add_product, name='add_product'), 

    path('mens_page/', views.mens_page, name='mens_page'),

    path('womens_page/', views.womens_page, name='womens_page'),

    path('kids_page/', views.kids_page, name='kids_page'),

    path('view_products/', views.view_products, name='view_products'),

    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

    path('view_users/', views.view_users, name='view_users'),

    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

    path('carts/', views.carts, name='carts'),

    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('cartpage/', views.cartpage, name='cartpage'), 

    path('increment_quantity/<int:pk>/', views.increment_quantity, name='increment_quantity'),

    path('decrement_quantity/<int:pk>/', views.decrement_quantity, name='decrement_quantity'),

    path('delete_product_from_cart/<int:product_id>/', views.delete_product_from_cart, name='delete_product_from_cart'),

    path('place_order/', views.place_order, name='place_order'),

    path('payment_page/', views.payment_page, name='payment_page'),

    path('logout_user/', views.logout_user, name='logout_user'),

    path('logout_admin/', views.logout_admin, name='logout_admin'),
]

