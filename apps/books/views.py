from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q

from .models import Book
from .serializers import BookListSerializer, BookSerializer
from .pagination import SmallSetPagination
from apps.category.models import Category


class BookListView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        if Book.objects.all().exists():
            books = Book.objects.order_by('-created_at').all()

            paginator = SmallSetPagination()
            results = paginator.paginate_queryset(books, request)
            serializer = BookListSerializer(results, many=True)

            return paginator.get_paginated_response({'books': serializer.data})
        else:
            return Response({'error': 'No books found'}, status=status.HTTP_404_NOT_FOUND)


class ListBooksByCategoryView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        slug = request.query_params.get('slug')
        if slug is None:
            return Response({'error': 'Category slug is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        # Filtrar libros que están en la categoría o en cualquiera de sus subcategorías
        books = Book.objects.order_by('-created_at').filter(category__in=[category])

        # Si esta categoría tiene subcategorías, incluir también los libros de esas subcategorías
        sub_categories = Category.objects.filter(parent=category)
        if sub_categories.exists():
            books = books | Book.objects.order_by('-created_at').filter(category__in=sub_categories)

        paginator = SmallSetPagination()
        results = paginator.paginate_queryset(books, request)
        serializer = BookListSerializer(results, many=True)

        return paginator.get_paginated_response({'books': serializer.data})


class BookDetailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, slug, format=None):
        if Book.objects.filter(slug=slug).exists():
            book = Book.objects.get(slug=slug)
            serializer = BookSerializer(book)

            return Response({'book': serializer.data})
        else:
            return Response({'error': 'Book does not exist'}, status=status.HTTP_404_NOT_FOUND)


class SearchBookView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        search_term = request.query_params.get('s')
        matches = Book.objects.filter(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(author__icontains=search_term) |
            Q(category__name__icontains=search_term)
        )

        paginator = SmallSetPagination()
        results = paginator.paginate_queryset(matches, request)
        serializer = BookListSerializer(results, many=True)

        return paginator.get_paginated_response({'filtered_books': serializer.data})
