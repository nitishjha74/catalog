from catalog import models
from django.shortcuts import get_object_or_404

class CategoryService:
    @staticmethod
    def get_all(business_id):
        """Return all categories for a specific business."""
        return models.Category.objects.filter(business_id=business_id, is_active=True).order_by("-created_at")

    @staticmethod
    def get_by_id(category_id, business_id):
        """Get a category belonging to the same business."""
        return get_object_or_404(models.Category, category_id=category_id, business_id=business_id)

    @staticmethod
    def create(data, business_id):
        """Create a category with business_id."""
        data["business_id"] = business_id
        return models.Category.objects.create(**data)

    @staticmethod
    def update(category_id, business_id, data):
        """Update category details."""
        category = get_object_or_404(models.Category, category_id=category_id, business_id=business_id)
        for key, value in data.items():
            setattr(category, key, value)
        category.save()
        return category

    @staticmethod
    def delete(category_id, business_id):
        """Delete category for the business."""
        category = get_object_or_404(models.Category, category_id=category_id, business_id=business_id)
        category.delete()
        return True
