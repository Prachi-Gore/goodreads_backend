from django.db import models
from bookshelf.models import Bookshelf
from cloudinary.models import CloudinaryField
from custom_authentication.models import CustomUser
from core.models import BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
# from django.utils import timezone

# Create your models here.
class Author(BaseModel):
    author_name=models.CharField(max_length = 255)
    def __str__(self):
        return f'{self.author_name}'

class Genre(BaseModel):
    genre_name=models.CharField(max_length=255)
    def __str__(self):
        return f'{self.genre_name}'

class Book(BaseModel):
   # book_cover = models.ImageField(upload_to='book_covers/',blank=False,null=False)  # Uploads to MEDIA_ROOT/book_covers/ here media/book_caover/exsmple.jpg
    book_cover =CloudinaryField('book_cover')  # Stores image in Cloudinary
    title = models.CharField(max_length = 255,blank=False)
    author = models.ForeignKey(Author,on_delete=models.SET_NULL,null=True, blank=False) # many to one(multiple book -> one author)
    description = models.TextField()
    genres = models.ManyToManyField(Genre,through='BookGenre') # many to many(multiple book -> multiple author)
    pages = models.PositiveBigIntegerField()
    publish_date = models.DateField(null=True)
    rating = models.FloatField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])  # Default rating is 0
    bookshelf=models.ForeignKey(Bookshelf,on_delete=models.SET_NULL,null=True, blank=True,related_name='books') # bookshelfobject.books.all return all books in that perticular self

    def __str__(self):
        return f'{self.title} - {self.author}'

class BookGenre (BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['book', 'genre']  # To ensure unique book-genre pairs

    def __str__(self):
        return f'{self.book.title} - {self.genre.genre_name}'
    

# review
class Review(models.Model):
    # updated_at = models.DateTimeField(null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True)  # when create first time
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name='reviews')
    review = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f'{self.review}'

    # def save(self, *args, **kwargs):
    #     print("review self ",self.pk)
    #     if self.pk:  # Only update if object already exists (i.e., not during creation)
    #         self.updated_at = timezone.now()
    #     super().save(*args, **kwargs)  

# bookshelf



# class Bookshelf(BaseModel):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # One user can have multiple bookshelves
#     name = models.CharField(max_length=255, blank=False, null=False)  # Name of the bookshelf
#     books = models.ManyToManyField(Book, blank=True)  # A bookshelf can have multiple books, optional at creation

#     def __str__(self):
#         return f"{self.name} - {self.user.username}" 