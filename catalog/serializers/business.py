from rest_framework import serializers
from catalog import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"
        read_only_fields = ["business_id","category_id", "created_at", "updated_at"]

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = models.Product
        fields = [
            "product_id", "business_id", "category", "category_name", 
            "name", "description", "price", "image_url", "is_active",
            "created_at", "updated_at"
        ]
        read_only_fields = ["business_id", "product_id", "created_at", "updated_at"]