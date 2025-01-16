from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser

UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('date_of_birth', 'image')}),)

admin.site.register(MyUser, UserAdmin)
# Register your models here.
