import random
from django.db import models

def generate_category_id():
    """Generate a unique 4-digit random category ID."""
    while True:
        category_id = random.randint(1000, 9999)
        if not Category.objects.filter(category_id=category_id).exists():
            return category_id

class Category(models.Model):
    category_id = models.PositiveIntegerField(unique=True, editable=False, blank=True, null=True)
    business_id = models.IntegerField(null=True, blank=True, help_text="Business ID from authentication server")
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    image_url = models.TextField(blank=True, null=True)  # S3 image URL
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.category_id:
            self.category_id = generate_category_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
