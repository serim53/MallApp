from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
# Register your models here.
from product.models import Product, Category, Comment, Manufacturer

admin.site.register(Product, MarkdownxModelAdmin)
admin.site.register(Comment)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# class TagAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug':('name',)}

class ManufacturerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)

admin.site.register(Manufacturer, ManufacturerAdmin)