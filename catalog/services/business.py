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

class ProductService:
    @staticmethod
    def get_all(business_id):
        """Return all products for a specific business."""
        return models.Product.objects.filter(business_id=business_id, is_active=True).order_by("-created_at")

    @staticmethod
    def get_by_id(product_id, business_id):
        """Get a product belonging to the same business."""
        return get_object_or_404(models.Product, product_id=product_id, business_id=business_id)

    @staticmethod
    def create(data, business_id):
        """
        Create a product with business_id.
        Category validation is handled in serializer, so data['category'] should be a Category object.
        """
        # The category should already be a Category object due to serializer validation
        # Just set the business_id and create
        data["business_id"] = business_id
        return models.Product.objects.create(**data)

    @staticmethod
    def update(product_id, business_id, data):
        """Update product details."""
        product = get_object_or_404(models.Product, product_id=product_id, business_id=business_id)
        
        # The category should already be validated and converted by the serializer
        # No need for additional category validation here
        
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product

    @staticmethod
    def delete(product_id, business_id):
        """Delete product for the business."""
        product = get_object_or_404(models.Product, product_id=product_id, business_id=business_id)
        product.delete()
        return True

    @staticmethod
    def get_featured_products(business_id):
        """Return all featured products for a specific business."""
        return models.Product.objects.filter(
            business_id=business_id, 
            is_active=True, 
            is_feature=True
        ).order_by("-created_at")

    @staticmethod
    def get_products_by_category(category_id, business_id):
        """Return all products for a specific category and business."""
        return models.Product.objects.filter(
            category_id=category_id,
            business_id=business_id,
            is_active=True
        ).order_by("-created_at")