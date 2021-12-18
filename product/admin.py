from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
# Register your models here.
from product.models import Product, Category, Comment

admin.site.register(Product, MarkdownxModelAdmin)
admin.site.register(Comment)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)