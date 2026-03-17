from django.contrib import admin
from .models import Post, Category, Location


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


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
