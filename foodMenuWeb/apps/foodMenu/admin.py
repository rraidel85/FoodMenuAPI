from django.contrib import admin
from .models import Category, Local, MenuCategory, Product, Comment

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class LocalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'local', 'category')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'image')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Local, LocalAdmin)
admin.site.register(MenuCategory, MenuCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)

