from django.db import models
from apps.category.models import Category
import uuid
import slugify

def book_file_directory(instance, filename):
  return 'book_files/{0}/{1}'.format(instance.title, filename)

class Book(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=255)
  slug = models.SlugField(max_length=255, unique=True)
  author = models.CharField(max_length=255)
  description = models.TextField()
  category = models.ManyToManyField(Category, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  file = models.FileField(upload_to=book_file_directory)  # Add the file field for uploading PDF files

  def __str__(self):
    return self.title
  
  def save(self, *args, **kwargs):
      if not self.slug:
        self.slug = slugify.slugify(self.title)
      super(Book, self).save(*args, **kwargs)
      
  class Meta:
    ordering = ['-created_at']
