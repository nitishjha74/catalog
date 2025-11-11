from rest_framework import serializers
from catalog import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"
        read_only_fields = ["business_id","category_id", "created_at", "updated_at"]
