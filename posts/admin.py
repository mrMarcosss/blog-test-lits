from django.contrib import admin
from posts.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'category', 'is_active', 'updated')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('category', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
