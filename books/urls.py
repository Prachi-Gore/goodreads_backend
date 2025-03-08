from django.urls import path,include ;
from .views import BookListView,BookDetailView;
from rest_framework.routers import DefaultRouter;
from .views import ReviewViewSet

router = DefaultRouter()
# router.register(r'reviewsw', ReviewViewSet,basename='review')

urlpatterns=[
path('books/',BookListView.as_view({'get': 'list', 'post': 'create'})),
path('book/<uuid:pk>',BookDetailView.as_view()),
path('reviews/',ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
path('review/<uuid:pk>', ReviewViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})),  # Get, update, delete a single review
# path('reviews/<int:pk>',ReviewViewSet.as_view()), # delete put patch
# path('', include(router.urls)),
# path('bookshelfs/',BookShelfView.as_view()),
# path('bookshelf/<int:pk>',BookShelfDetailView.as_view())
]
