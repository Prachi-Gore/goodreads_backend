from django.db import models
from bookshelf.models import Bookshelf
from cloudinary.models import CloudinaryField
from custom_authentication.models import CustomUser
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author_name=models.CharField(max_length = 255)
    def __str__(self):
        return f'{self.author_name}'

class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    genre_name=models.CharField(max_length=255)
    def __str__(self):
        return f'{self.genre_name}'

class Book (models.Model):
   # book_cover = models.ImageField(upload_to='book_covers/',blank=False,null=False)  # Uploads to MEDIA_ROOT/book_covers/ here media/book_caover/exsmple.jpg
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book_cover =CloudinaryField('book_cover')  # Stores image in Cloudinary
    title = models.CharField(max_length = 255,blank=False)
    author = models.ForeignKey(Author,on_delete=models.SET_NULL,null=True, blank=False) # many to one(multiple book -> one author)
    description = models.TextField()
    genres = models.ManyToManyField(Genre,through='BookGenre') # many to many(multiple book -> multiple author)
    pages = models.PositiveBigIntegerField()
    publish_date = models.DateField(null=True)
    rating = models.FloatField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])  # Default rating is 0
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    bookshelf=models.ForeignKey(Bookshelf,on_delete=models.SET_NULL,null=True, blank=True,related_name='books') # bookshelfobject.books.all return all books in that perticular self

    def __str__(self):
        return f'{self.title} - {self.author}'

class BookGenre (models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['book', 'genre']  # To ensure unique book-genre pairs

    def __str__(self):
        return f'{self.book.title} - {self.genre.genre_name}'
    

# review
class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name='reviews')
    review = models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.review}'

# bookshelf

# class Bookshelf(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # One user can have multiple bookshelves
#     name = models.CharField(max_length=255, blank=False, null=False)  # Name of the bookshelf
#     books = models.ManyToManyField(Book, blank=True)  # A bookshelf can have multiple books, optional at creation
#     created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for bookshelf creation
#     updated_at = models.DateTimeField(auto_now=True)  # Timestamp for last update

#     def __str__(self):
#         return f"{self.name} - {self.user.username}"    