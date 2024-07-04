from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin
# Register your models here.
@admin.register(Category)
class CategoryAdminClass(ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    list_filter = ('parent',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ViewCount)
class ViewCountAdminClass(ModelAdmin):
  list_display = ('category', 'ip_address')
  list_filter = ('category',)
  search_fields = ('category__name', 'ip_address')
