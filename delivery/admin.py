from django.contrib import admin

# Register your models here.
from .models import Customer,Restaurant
admin.site.register(Customer)
admin.site.register(Restaurant)
