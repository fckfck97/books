from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Category


from django.db.models import Count, Q

class ListCategoriesView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        # Obtener categorías que tienen al menos un post publicado
        categories_with_posts = Category.objects.annotate(
            num_posts=Count('book__id')
        )

        result = []

        for category in categories_with_posts:
            if not category.parent:
                item = {
                    'id': category.id,
                    'name': category.name,
                    'slug': category.slug,
                    'views': category.views,
                    'sub_categories': []
                }

                # Verificar subcategorías con posts publicados
                for sub_category in categories_with_posts:
                    if sub_category.parent and sub_category.parent.id == category.id:
                        sub_item = {
                            'id': sub_category.id,
                            'name': sub_category.name,
                            'slug': sub_category.slug,
                            'views': sub_category.views
                        }
                        item['sub_categories'].append(sub_item)

                result.append(item)

        if result:
            return Response({'categories': result}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No categories with published posts found'}, status=status.HTTP_404_NOT_FOUND)
