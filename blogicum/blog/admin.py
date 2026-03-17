from django.contrib import admin
from .models import Post, Category, Location, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'pub_date')
    list_filter = ('is_published', 'category', 'pub_date')
    search_fields = ('title', 'text', 'author__username')
    date_hierarchy = 'pub_date'
    list_editable = ('is_published',)
    ordering = ('-pub_date',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published')
    list_filter = ('is_published',)
    list_editable = ('is_published',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_filter = ('is_published',)
    list_editable = ('is_published',)
    search_fields = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'author__username', 'post__title')
    date_hierarchy = 'created_at'


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Comment, CommentAdmin)
