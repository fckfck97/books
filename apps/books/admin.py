from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin

@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'category')
    search_fields = ('title', 'author', 'description', 'category__name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Cuando se edita un objeto existente
            return self.readonly_fields + ('slug',)
        return self.readonly_fields