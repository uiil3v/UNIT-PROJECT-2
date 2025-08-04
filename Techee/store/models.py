from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('phones', 'Phones'),
        ('laptops', 'Laptops'),
        ('headphones', 'Headphones'),
        ('watches', 'Watches'),
        ('tablets', 'Tablets'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=100, blank=True, null=True)
    image = CloudinaryField('image')
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.price} SAR"


class Comment(models.Model):
    
    RATING_CHOICES = [
        (1, '⭐ - Poor'),
        (2, '⭐⭐ - Fair'),
        (3, '⭐⭐⭐ - Good'),
        (4, '⭐⭐⭐⭐ - Very Good'),
        (5, '⭐⭐⭐⭐⭐ - Excellent'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.name}"
    



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
