from django.urls import path
from .views import BookListView, ListBooksByCategoryView, BookDetailView
urlpatterns = [
    path("list/", BookListView.as_view(), name="book-list"),
    path("category/", ListBooksByCategoryView.as_view(), name="book-list-by-category"),
    path("<slug:slug>/", BookDetailView.as_view(), name="book-detail"),
    
]
