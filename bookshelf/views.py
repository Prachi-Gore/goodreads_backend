from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import BookshelfSerializer
from .models import Bookshelf
# Create your views here.

class BookshelfView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Retrieve all bookshelves for the authenticated user
        bookshelves = Bookshelf.objects.filter(user=request.user)
        serializer = BookshelfSerializer(bookshelves, many=True)
        # print("serializer.data ",serializer.data,bookshelves)

        return Response(serializer.data)
    
    def post(self, request):
        serializer = BookshelfSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        

# class AddBookToShelfView(APIView):
#     permission_classes = [IsAuthenticated]

#     def patch(self, request, shelf_id, book_id):
#         try:
#             # Get the user's bookshelf by name
#             bookshelf = Bookshelf.objects.get(id=shelf_id, user=request.user)
#             # Get the book by ID
#             book = Book.objects.get(id=book_id)
#             # Add the book to the bookshelf
#             bookshelf.books.add(book)
#             bookshelf.save()
#             return Response({"message": "Book successfully added to shelf"}, status=status.HTTP_200_OK)
#         except Bookshelf.DoesNotExist:
#             return Response({"error": "Bookshelf not found"}, status=status.HTTP_404_NOT_FOUND)
#         except Book.DoesNotExist:
#             return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)        