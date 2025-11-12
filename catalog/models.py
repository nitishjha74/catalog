import random
from django.db import models

# Category ID generator
def generate_category_id():
    """Generate a unique 4-digit random category ID."""
    while True:
        category_id = random.randint(1000, 9999)
        if not Category.objects.filter(category_id=category_id).exists():
            return category_id

# Product ID generator  
def generate_product_id():
    """Generate a unique 6-digit random product ID."""
    while True:
        product_id = random.randint(100000, 999999)
        if not Product.objects.filter(product_id=product_id).exists():
            return product_id

class Category(models.Model):
    category_id = models.PositiveIntegerField(unique=True, editable=False, blank=True, null=True)
    business_id = models.IntegerField(null=True, blank=True, help_text="Business ID from authentication server")
    name = models.CharField(max_length=100)  
    slug = models.SlugField(max_length=120)  
    image_url = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # ADD THIS - Enforce uniqueness per business
        unique_together = [['business_id', 'name'], ['business_id', 'slug']]

    def save(self, *args, **kwargs):
        if not self.category_id:
            self.category_id = generate_category_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Business: {self.business_id})"

class Product(models.Model):
    product_id = models.PositiveIntegerField(unique=True, editable=False, blank=True, null=True)
    business_id = models.IntegerField(null=True, blank=True, help_text="Business ID from authentication server")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.TextField(blank=True, null=True)  # S3 image URL
    is_active = models.BooleanField(default=True)
    is_feature = models.BooleanField(default=False, help_text="Mark product as featured for top picks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_id = generate_product_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name