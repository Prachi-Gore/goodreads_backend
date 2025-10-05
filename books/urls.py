from django.urls import path,include ;
from .views import BookListView,BookDetailView,GenerateQuizWrapper,EvaluateAnswersWrapper ;
from rest_framework.routers import DefaultRouter;
from .views import ReviewViewSet

router = DefaultRouter()
# router.register(r'reviewsw', ReviewViewSet,basename='review')

urlpatterns=[
path('books/',BookListView.as_view({'get': 'list', 'post': 'create'})),
path('book/<uuid:pk>',BookDetailView.as_view()),
path('reviews/',ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
path('review/<uuid:pk>', ReviewViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})),  # Get, update, delete a single review
path("generate_quiz/", GenerateQuizWrapper.as_view({'post': 'create'}), name="generate_quiz"),
path("evaluate_answers/", EvaluateAnswersWrapper.as_view({'post': 'create'}), name="evaluate_answers"),
# path('reviews/<int:pk>',ReviewViewSet.as_view()), # delete put patch
# path('', include(router.urls)),
# path('bookshelfs/',BookShelfView.as_view()),
# path('bookshelf/<int:pk>',BookShelfDetailView.as_view())
]
