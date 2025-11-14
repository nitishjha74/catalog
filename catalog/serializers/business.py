from rest_framework import serializers
from catalog import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"
        read_only_fields = ["business_id","category_id", "created_at", "updated_at"]

    def validate(self, data):
        """
        Custom validation to handle unique constraints during updates.
        """
        # Get the instance if it exists (during update)
        instance = getattr(self, 'instance', None)
        
        # Get business_id from instance or context
        business_id = None
        if instance:
            business_id = instance.business_id
        elif self.context.get('request') and hasattr(self.context['request'].user, 'business_id'):
            business_id = self.context['request'].user.business_id
        
        # If we have business_id, validate uniqueness
        if business_id:
            # Check for unique name constraint
            if 'name' in data:
                queryset = models.Category.objects.filter(
                    name=data['name'], 
                    business_id=business_id
                )
                if instance:
                    queryset = queryset.exclude(pk=instance.pk)
                
                if queryset.exists():
                    raise serializers.ValidationError({
                        "name": "Category with this name already exists for your business."
                    })
            
            # Check for unique slug constraint
            if 'slug' in data:
                queryset = models.Category.objects.filter(
                    slug=data['slug'], 
                    business_id=business_id
                )
                if instance:
                    queryset = queryset.exclude(pk=instance.pk)
                
                if queryset.exists():
                    raise serializers.ValidationError({
                        "slug": "Category with this slug already exists for your business."
                    })
        
        return data

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = models.Product
        fields = [
            "product_id", "business_id", "category", "category_name", 
            "name", "description", "price", "image_url", "is_active",
            "is_feature", "created_at", "updated_at"
        ]
        read_only_fields = ["business_id", "product_id", "created_at", "updated_at"]

    def validate_category(self, value):
        """
        Validate that the category exists and belongs to the current business.
        """
        request = self.context.get('request')
        if request and hasattr(request.user, 'business_id'):
            business_id = request.user.business_id
            try:
                category = models.Category.objects.get(category_id=value, business_id=business_id)
                return category  # Return the Category OBJECT, not just the ID
            except models.Category.DoesNotExist:
                raise serializers.ValidationError(
                    f"Category with ID {value} does not exist for your business."
                )
        raise serializers.ValidationError("Unable to validate category without business context.")

    def create(self, validated_data):
        # The category field now contains the Category object due to validate_category
        # No need to pop and lookup again
        business_id = self.context['request'].user.business_id
        validated_data['business_id'] = business_id
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Handle update - category is already validated and converted to object.
        """
        business_id = self.context['request'].user.business_id
        # business_id is handled automatically, no need to set it
        
        return super().update(instance, validated_data)