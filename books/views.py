from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Book # used to query the data# Create your views here.
from .serializers import BookSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Review
from .serializers import ReviewSerializer,BookIdSerializer
from django.db.models import Prefetch
from django.utils.timezone import now
import requests
from django.conf import settings

# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from rest_framework.permissions import IsAuthenticated
# from django.shortcuts import get_object_or_404

class BookListView(ModelViewSet) :
 queryset = Book.objects.all()
 serializer_class=BookSerializer
 filter_backends = [SearchFilter]
 search_fields = ['title'] 
#  def get(self,request):
    
#     books=Book.objects.all()
  
#     serialized_books = BookSerializer(books,many=True)
#    #  print("serialized_books",serialized_books)
#     return Response(serialized_books.data)
 
 def create(self,request):
   
   books_data = request.data
  
   if isinstance(books_data, dict):
        books_data = [books_data]
   valid_book=[]
   error_book={}
   for book in books_data :
      serialize_book=BookSerializer(data=book)
      if serialize_book.is_valid():
         serialize_book.save()
         valid_book.append(serialize_book.data)

      else:
         error_book[book['title']]=serialize_book.errors

   response_data = {
    'message': "Some books could not be created." if error_book else "Successfully created the books",
    'err': error_book if error_book else {},
    'data': valid_book,
    'success': False if error_book else True
}
   status_code=status.HTTP_400_BAD_REQUEST if error_book else status.HTTP_201_CREATED
   return Response(response_data,status=status_code)

# @method_decorator(csrf_exempt, name="dispatch") # was getting error while book update
class BookDetailView(APIView):

   def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # Public access for GET
        return [IsAuthenticated()]  # Auth required for other methods 
   
   def get(self,request,pk):
      print('request ',request)
      book = Book.objects.prefetch_related(
            Prefetch(
                'reviews', # this is related name from Review Model
                queryset=Review.objects.order_by('-created_at')
            )
        ).get(pk=pk)
      serialized_book=BookSerializer(book)
      return Response(serialized_book.data)
   
   def put(self,request,pk):
      print('request ',request)
      book=Book.objects.get(pk=pk)
      serialized_book=BookSerializer(book,data=request.data)
      if(serialized_book.is_valid()):
        serialized_book.save()
        return Response(serialized_book.data, status=status.HTTP_200_OK)      
      return Response(serialized_book.errors,status=status.HTTP_400_BAD_REQUEST)
   
   def patch(self,request,pk):
      book=Book.objects.get(pk=pk)
      if 'bookshelf' in request.data and request.data['bookshelf'] == 'None':
         book.bookshelf=None
         
      else:   
        serialized_book=BookSerializer(book,data=request.data,partial=True)
        if(serialized_book.is_valid()):
          serialized_book.save()
          return Response(serialized_book.data, status=status.HTTP_200_OK)      
      
      book.save()
      return Response({'message': 'Book removed from shelf successfully!'}, status=status.HTTP_200_OK)

   def delete(self,request,pk):
      
      book=Book.objects.get(pk=pk)
      book.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
   
# Bookshelf   
# class BookShelfView(APIView) :
#    permission_classes = [IsAuthenticated]  # Only authenticated users can access
#    def get(self,request):
#      bookshelves = Bookshelf.objects.all()
#      serialized_bookshelves=BookshelfSerializer(bookshelves,many=True)
#      return Response(serialized_bookshelves.data)

#    def post(self,request):
#    #   bookshelf_data=request.data
#       serialized_bookshelves=BookshelfSerializer(data=request.data)
#       if(serialized_bookshelves.is_valid()):
#          # bookshelf = serialized_bookshelves.save(user=request.user)  # Automatically associate with the authenticated user
#          # serialized_bookshelf = BookshelfSerializer(bookshelf)  # Serialize the created bookshelf
#          serialized_bookshelves.save()
#          return Response(serialized_bookshelves.data, status=status.HTTP_201_CREATED)
#       return Response(serialized_bookshelves.errors, status=status.HTTP_400_BAD_REQUEST)
   
# class BookShelfDetailView(APIView):
#     permission_classes = [IsAuthenticated]  # Ensure user is authenticated

#     # Get details of a specific bookshelf
#     def get(self, request, pk):
#       #   bookshelf = get_object_or_404(Bookshelf, pk=pk, user=request.user)
#          bookshelf = get_object_or_404(Bookshelf, pk=pk)
#          serializer = BookshelfSerializer(bookshelf)
#          return Response(serializer.data, status=status.HTTP_200_OK)

#     # Update details of a specific bookshelf
#     def put(self, request, pk):
#       #   bookshelf = get_object_or_404(Bookshelf, pk=pk, user=request.user)
#          bookshelf = get_object_or_404(Bookshelf, pk=pk)
#          serializer = BookshelfSerializer(bookshelf, data=request.data)
        
#          if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
#          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # Delete a specific bookshelf
#     def delete(self, request, pk):
#       #   bookshelf = get_object_or_404(Bookshelf, pk=pk, user=request.user)
#          bookshelf = get_object_or_404(Bookshelf, pk=pk)
#          bookshelf.delete()
#          return Response({"message": "Bookshelf deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class ReviewViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all().order_by("-created_at") 
    serializer_class = ReviewSerializer
   #  parser_classes = (MultiPartParser, FormParser)  # Enable file uploads
   #  def perform_create(self, serializer):
   #      # Automatically associate the user with the review
   #      serializer.save(user=self.request.user)  # Set user here

    def create(self,request):
       serialize=ReviewSerializer(data=request.data)
       if(serialize.is_valid()):
          serialize.save(user=request.user)
          return Response({ "message": "Review created successfully.", "data":serialize.data},status=status.HTTP_201_CREATED)
       else:
          return Response({ "message": "Review creation failed.", "errors":serialize.errors},status=status.HTTP_400_BAD_REQUEST)
   # no need of getAllReviews api    
   #  def list(self,request):
   #      reviews=Review.objects.all()  
   #      serializer=ReviewSerializer(reviews,many=True) 
   #      return Response({"message": "Reviews retrieved successfully.", "data":serializer.data},status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """Only allow users to update their own reviews"""
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {"message": "You can edit only your own review"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        instance.updated_at = now()
        instance.save(update_fields=["updated_at"])

        response = super().partial_update(request, *args, **kwargs)

        return Response(
            {"message": "Review updated successfully", "data": response.data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        """Only allow users to delete their own reviews"""
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {"message": "You can delete only your own review"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Review deleted successfully"}, status=status.HTTP_200_OK)    
    
class GenerateQuizWrapper(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class=BookIdSerializer
    def create(self, request):
        payload = {"book_id": request.data["book_id"]}
        resp = requests.post(f"{settings.FASTAPI_URL}/generate_quiz", json=payload)
        return Response(resp.json())

class EvaluateAnswersWrapper(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        payload = {
            "book_id": request.data["book_id"],
            "user_answers": request.data["user_answers"]
        }
        resp = requests.post(f"{settings.FASTAPI_URL}/evaluate_answers", json=payload)
        return Response(resp.json())    