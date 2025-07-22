from django.shortcuts import render
from django.http import HttpResponse
from delivery.models import Customer
from delivery.models import Restaurant



def index(request):
    return render(request,'delivery/index.html')

def signin(request):
    return render(request,'delivery/signin.html')

def signup(request):
    return render(request,'delivery/signup.html')
def handle_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Username:", username)  # debug
        print("Password:", password)  # debug
        try:
         cust = Customer.objects.get(username = username,password = password) #this will see any username and password are present or not if not it will throw exception
         return render(request, 'delivery/success.html')
        except:
            return render(request, 'delivery/fail.html', {
                'error': 'Invalid username or password'
            })
    else:
        return HttpResponse("Invalid Request")

def handle_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        # Check if the username already exists
        if Customer.objects.filter(username=username).exists():
            return render(request, 'delivery/signup.html', {
                'error': 'Username already exists. Please choose a different one.'
            })

        # If username is unique, create the new customer
        c = Customer(username=username, password=password, email=email, mobile=mobile, address=address)
        c.save()
        
        return render(request, 'delivery/userdata.html', {
            'message': 'User created successfully!'
        })
    else:
        return HttpResponse("Invalid Request")
    
def restaurant_page(request):
    return render(request, 'delivery/add_restaurant.html')

def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine =  request.POST.get('cuisine')
        rating =  request.POST.get('rating')
        
        rest = Restaurant(name = name,picture = picture, cuisine = cuisine,rating = rating)
        rest.save()
        
        restaurants = Restaurant.objects.all()
        return render(request,'delivery/show_restaurants.html',{"restaurants":restaurants})
    else:
         return HttpResponse("Invalid Request")
    