from rest_framework import serializers
from catalog import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"
        read_only_fields = ["business_id","category_id", "created_at", "updated_at"]

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category = serializers.IntegerField(write_only=True)  # Accept integer input
    
    class Meta:
        model = models.Product
        fields = [
            "product_id", "business_id", "category", "category_name", 
            "name", "description", "price", "image_url", "is_active",
            "is_feature", "created_at", "updated_at"
        ]
        read_only_fields = ["business_id", "product_id", "created_at", "updated_at"]

    def create(self, validated_data):
        # Get the category_id from input
        category_id = validated_data.pop('category')
        business_id = self.context['request'].user.business_id
        
        # Find the actual category object
        try:
            category = models.Category.objects.get(category_id=category_id, business_id=business_id)
        except models.Category.DoesNotExist:
            raise serializers.ValidationError({"category": f"Category with ID {category_id} does not exist."})
        
        # Create product with the actual category object
        validated_data['category'] = category
        return super().create(validated_data)