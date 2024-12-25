from rest_framework import serializers
from api import models

class ModelRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ModelRequest
        fields = ['request']

class ModelResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ModelRequest
        fields = ['response']