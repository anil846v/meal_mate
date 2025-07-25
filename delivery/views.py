from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from delivery.models import Customer, Restaurant, MenuItem, Cart
from django.contrib import messages  # To display messages to the user

import razorpay
from django.conf import settings


# Home Page
def index(request):
    return render(request, 'delivery/index.html')

# Sign In Page
def signin(request):
    return render(request, 'delivery/signin.html')

# Sign Up Page
def signup(request):
    return render(request, 'delivery/signup.html')

# Handle Login
def handle_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Check if the customer exists
            Customer.objects.get(username=username, password=password)
             # ✅ Store username in session
            request.session['username'] = username
            if username == 'admin':
                return render(request, 'delivery/admin_home.html')
            else:
                restaurants = Restaurant.objects.all()
                cart_count = get_cart_count(username)
                return render(request, 'delivery/customer_home.html', {"restaurants": restaurants,  "cart_count": cart_count,"username":username})
            
        except Customer.DoesNotExist:
            return render(request, 'delivery/fail.html')
    return HttpResponse("Invalid request")

# Handle Sign Up
def handle_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        # Check for duplicate username
        if not Customer.objects.filter(username=username).exists():
            Customer.objects.create(
                username=username,
                password=password,
                email=email,
                mobile=mobile,
                address=address
            )
            return render(request, 'delivery/signin.html')

    return HttpResponse("Invalid request")

# Add Restaurant Page
def add_restaurant_page(request):
    return render(request, 'delivery/add_restaurant.html')

# Add Restaurant
def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')

        Restaurant.objects.create(name=name, picture=picture, cuisine=cuisine, rating=rating)

        restaurants = Restaurant.objects.all()
        return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})

    return HttpResponse("Invalid request")

# Show Restaurants
def show_restaurant_page(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})

# Restaurant Menu
def restaurant_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        is_veg = request.POST.get('is_veg') == 'on'
        picture = request.POST.get('picture')

        MenuItem.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price,
            is_veg=is_veg,
            picture=picture
        )
        return redirect('restaurant_menu', restaurant_id=restaurant.id)

    menu_items = restaurant.menu_items.all()
    return render(request, 'delivery/menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
    })

# Update Restaurant Page
def update_restaurant_page(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'delivery/update_restaurant_page.html', {"restaurant": restaurant})

# Update Restaurant
def update_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        restaurant.name = request.POST.get('name')
        restaurant.picture = request.POST.get('picture')
        restaurant.cuisine = request.POST.get('cuisine')
        restaurant.rating = request.POST.get('rating')
        restaurant.save()

        restaurants = Restaurant.objects.all()
        return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})

# Delete Restaurant
def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    restaurant.delete()

    restaurants = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})


# Update Menu item Page
def update_menuItem_page(request, menuItem_id):
    menuItem = get_object_or_404(MenuItem, id=menuItem_id)
    return render(request, 'delivery/update_menuItem_page.html', {"item": menuItem})

# Update MenuItem
def update_menuItem(request, menuItem_id):
    menuItem = get_object_or_404(MenuItem, id=menuItem_id)

    if request.method == 'POST':
        menuItem.name = request.POST.get('name')
        menuItem.description = request.POST.get('description')
        menuItem.price = request.POST.get('price')
        menuItem.is_veg = request.POST.get('is_veg') == 'on'
        menuItem.picture = request.POST.get('picture')

        menuItem.save()

        restaurants = Restaurant.objects.all()
        return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})

# Delete menuItem
def delete_menuItem(request, menuItem_id):
    menuItem = get_object_or_404(MenuItem, id=menuItem_id)
    menuItem.delete()

    restaurants = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})


# Customer Menu
def customer_menu(request, restaurant_id, username):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = restaurant.menu_items.all()
    cart_count = get_cart_count(username)

    return render(request, 'delivery/customer_menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'username':username,
        'cart_count': cart_count
    })

# Add items to cart
def add_to_cart(request, item_id, username):
    # Check user and item
    customer = get_object_or_404(Customer, username=username)
    item = get_object_or_404(MenuItem, id=item_id)

    # Get or create a cart for the customer
    cart, created = Cart.objects.get_or_create(customer=customer)

    # Add the item to the cart
    cart.items.add(item)

    # Add a success message
    messages.success(request, f"{item.name} added to your cart!")

    # Stay on the same menu page
    return redirect('customer_menu', restaurant_id=item.restaurant.id, username=username)


# Show Cart
def show_cart_page(request, username):
    # Fetch the customer's cart
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    # Fetch cart items and total price
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0
    cart_count = get_cart_count(username)


    return render(request, 'delivery/cart.html', {
        'items': items,
        'total_price': total_price,
        'username': username,
        'cart_count': cart_count
    })



# Checkout View
def checkout(request, username):
    # Fetch customer and their cart
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'delivery/checkout.html', {
            'error': 'Your cart is empty!',
        })

    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create Razorpay order
    order_data = {
        'amount': int(total_price * 100),  # Amount in paisa
        'currency': 'INR',
        'payment_capture': '1',  # Automatically capture payment
    }
    order = client.order.create(data=order_data)  
    cart_count = get_cart_count(username)

    # Pass the order details to the frontend
    return render(request, 'delivery/checkout.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],  # Razorpay order ID
        'amount': total_price,
        'cart_count': cart_count
    })


# Orders Page
def orders(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    cart_count = get_cart_count(username)


    # Fetch cart items and total price before clearing the cart
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    # Clear the cart after fetching its details
    if cart:
        cart.items.clear()

    return render(request, 'delivery/orders.html', {
        'username': username,
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count
    })
    
    

# 3. Logout View
def logout_view(request):
    request.session.flush()  # Clears all session data
    return redirect('index')  # Redirect to home

# 4. Navbar Full Page View
def navbar_full_page(request):
    username = request.session.get('username', 'Guest')

    if username != 'Guest':
        cart_count = get_cart_count(username)
    else:
        cart_count = 0

    return render(request, 'delivery/navbar_full.html', {
        'cart_count': cart_count,
        'request': request,  # Needed for session access
        'username': username
    })

def get_cart_count(username):
    try:
        customer = Customer.objects.get(username=username)
        cart = Cart.objects.filter(customer=customer).first()
        return cart.items.count() if cart else 0
    except Customer.DoesNotExist:
        return 0
