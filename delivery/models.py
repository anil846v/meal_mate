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
    cuisine = models.CharField(max_length=100)  # ✅ This must exist!
    rating = models.FloatField()
    
    def __str__(self):
        return f"{self.name} {self.cuisine} {self.rating}/5"
