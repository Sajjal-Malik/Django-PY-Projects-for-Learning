from django.urls import path
# from .views import BookAPIView, BookDetailAPIView
from .views import BookListCreateAPIView, BookRetrieveUpdateDestroyAPIView

urlpatterns = [
    # path('books/', BookAPIView.as_view(), name='book-list'),  # List all books, Create a new book
    # path('books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),  # Retrieve, Update, Delete
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book-detail'),
]