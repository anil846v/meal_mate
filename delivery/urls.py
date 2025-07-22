from django.urls import path
from delivery import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('handle_login/', views.handle_login, name='handle_login'),
    path('handle_signup/', views.handle_signup, name='handle_signup'),
    path('handle_login/restaurant_page/', views.restaurant_page, name='restaurant_page'),
    path('handle_login/add_restaurant/', views.add_restaurant, name='add_restaurant'),
]
