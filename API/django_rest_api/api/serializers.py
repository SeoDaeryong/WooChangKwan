from rest_framework import serializers
from .models import Category
from .models import Item

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'category', 'order')

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'category', 'name', 'count', 'limit')
