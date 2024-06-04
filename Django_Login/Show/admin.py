from django.contrib import admin
from .models import Model_Post, Model_File

# Register your models here.
@admin.register(Model_Post)
class Post_Admin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title')

@admin.register(Model_File)
class File_Admin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name')
