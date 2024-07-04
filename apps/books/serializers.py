from rest_framework import serializers
from .models import *
from apps.category.serializers import CategorySerializer


class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


class BookListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description', 'category', 'file', 'created_at', 'updated_at')
        
