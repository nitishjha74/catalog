from rest_framework import serializers
from course import models

class SkillVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SkillVideo
        fields = "__all__"