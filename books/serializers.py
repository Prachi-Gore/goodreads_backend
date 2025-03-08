from rest_framework.serializers import ModelSerializer,ValidationError;
from .models import Book,Author,Genre,Review
from custom_authentication.serializers import UserSerializer;

class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields ="__all__" 

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields ="__all__" 

# review
class ReviewSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
     # book=BookSerializer(read_only=True)
    class Meta:
        model=Review
        fields="__all__"
        read_only_fields = ['created_at', 'updated_at']

        
class BookSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)  # Include author details
    genres = GenreSerializer(many=True, read_only=True)  # Include list of genre details
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model=Book
        fields="__all__"
        read_only_fields = ['createdAt', 'updatedAt']

     # Custom validation to check if genres are provided
    def validate_genres(self, value):
        if not value:
            raise ValidationError("A book must have at least one genre.")
        return value


# bookshelf

# class BookshelfSerializer(ModelSerializer):
#      class Meta:
#         model=Bookshelf
#         fields="__all__"