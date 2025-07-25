from django.urls import path
from . import views
 
urlpatterns = [
    # Home and authentication paths
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.handle_login, name='handle_login'),
    path('signup/submit/', views.handle_signup, name='handle_signup'),

    # Restaurant-related paths
    path('restaurants/add', views.add_restaurant_page, name='add_restaurant_page'),
    path('restaurants/', views.show_restaurant_page, name='show_restaurant_page'),
    path('restaurants/add/', views.add_restaurant, name='add_restaurant'),
    path('restaurants/<int:restaurant_id>/menu/', views.restaurant_menu, name='restaurant_menu'),
    path('restaurants/<int:restaurant_id>/update/', views.update_restaurant, name='update_restaurant'),
    path('restaurants/<int:restaurant_id>/update/page/', views.update_restaurant_page, name='update_restaurant_page'),
    path('restaurants/<int:restaurant_id>/delete/', views.delete_restaurant, name='delete_restaurant'),

    path('menu/<int:menuItem_id>/update/', views.update_menuItem, name='update_menuItem'),
    path('menu/<int:menuItem_id>/update/page/', views.update_menuItem_page, name='update_menuItem_page'),
    path('menu/<int:menuItem_id>/delete/', views.delete_menuItem, name='delete_menuItem'),

    path('restaurants/<int:restaurant_id>/menu/customer/<str:username>/', views.customer_menu, name='customer_menu'),
    path('cart/<str:username>/', views.show_cart_page, name='show_cart_page'),
    path('cart/<int:item_id>/add/<str:username>/', views.add_to_cart, name='add_to_cart'),

    path('checkout/<str:username>/', views.checkout, name='checkout'),

    path('orders/<str:username>/', views.orders, name='orders'),
    
    path('logout/', views.logout_view, name='logout_view'),
    path('navbar/', views.navbar_full_page, name='navbar_full_page'),
    # path('customer_home/<str:username>/<int:restaurant_id>/', views.customer_menu, name='customer_home'),
    path('customer_home/<str:username>/', views.customer_menu_no_restaurant, name='customer_home_no_restaurant'),



]