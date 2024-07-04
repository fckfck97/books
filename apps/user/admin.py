from django.contrib import admin
from . import models
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
# Register your models here.
from unfold.decorators import display
admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(GroupAdmin, ModelAdmin):
    pass
# Register your models here.
@admin.register(models.UserAccount)
class UserAdminClass(ModelAdmin):
  form = UserChangeForm
  add_form = UserCreationForm
  change_password_form = AdminPasswordChangeForm
  ordering = ['id']
  list_display = ['user', 'is_active', 'is_staff', ]
  @display(header=True)
  def user(self, obj):
    initials = f"{obj.first_name[0].upper()}{obj.last_name[0].upper()}"
    return f"{obj.first_name} {obj.last_name}", f"{obj.email}", initials
