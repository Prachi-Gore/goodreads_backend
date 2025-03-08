from rest_framework import serializers
from .models import Bookshelf
from books.serializers import BookSerializer

class BookshelfSerializer(serializers.ModelSerializer):
 books = BookSerializer(many=True, required=False)  # Use the nested BookSerializer
 class Meta:
    model = Bookshelf
    fields = '__all__'
    read_only_fields = ['user', 'created_at', 'updated_at']