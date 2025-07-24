from django.db import models

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
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.price} SAR"
