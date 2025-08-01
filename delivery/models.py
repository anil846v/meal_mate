from django.db import models

# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    email = models.CharField(max_length = 20)
    mobile = models.CharField(max_length = 10)
    address = models.CharField(max_length = 50)
    
    def __str__(self):
        return f"{self.username} {self.password} {self.email} {self.mobile} {self.address}"
class Restaurant(models.Model):
    name = models.CharField(max_length = 20)
    picture = models.URLField(max_length = 200, default ="https://static01.nyt.com/images/2025/06/23/multimedia/23best-restaurants-philly-update1-gvkc/23best-restaurants-philly-update1-gvkc-articleLarge.jpg?quality=75&auto=webp&disable=upscale")
    cuisine = models.CharField(max_length=100)  
    rating = models.FloatField()
    
    def __str__(self):
        return f"{self.name} {self.cuisine} {self.rating}/5"
    
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant,on_delete = models.CASCADE, related_name ="menu_items")
    name = models.CharField(max_length = 20)
    picture = models.URLField(max_length = 200, default ="https://adstandards.com.au/wp-content/uploads/2023/08/food_and_beverage.svg")
    description = models.TextField(default="No description")
    price = models.FloatField()
    is_veg = models.BooleanField(default = True)

    
    def __str__(self):
        return f"{self.name} {self.description} {self.price}"    

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="cart")

    def total_price(self):
        return sum(item.subtotal() for item in self.cart_items.all())

    def __str__(self):
        return f"{self.customer.username} {self.total_price()}"


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='cart_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.menu_item.price * self.quantity
