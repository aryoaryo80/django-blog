from django.contrib import admin
from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created')
    prepopulated_fields = {'slug': ('title', )}


@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'is_sub')


admin.site.register(Vote)
