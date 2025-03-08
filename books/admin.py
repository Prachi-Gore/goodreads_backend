from django.contrib import admin
from .models import Author,Genre,Book,BookGenre

# Register your models here.

class BookGenreInline(admin.TabularInline):
    model = BookGenre
    extra = 1  # Number of extra fields for genres when adding a new book

class BookAdmin(admin.ModelAdmin):
    inlines = (BookGenreInline,)  # Adds the genres inline in the Book admin

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Genre)
