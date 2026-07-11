from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    

class FoodItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='food_images/', null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.food_name    
    
class Cart(models.Model):
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.food.food_name    
    
class Order(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    total = models.FloatField()
    status = models.CharField(max_length=50, default="Order Confirmed")

    def __str__(self):
        return self.name    