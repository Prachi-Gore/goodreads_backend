from django.urls import path
from .views import BookshelfView

urlpatterns = [
    path('bookshelf/', BookshelfView.as_view(), name='bookshelf'),
    # path('bookshelf/<int:shelf_id>/add/<int:book_id>/', AddBookToShelfView.as_view(), name='add-book-to-shelf'),
]
